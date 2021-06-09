import json
import time
import humanize
import pandas as pd

try:
    import cPickle as pickle
except:
    import pickle

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.algorithms import DecisionTrees
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf
from pyspark.sql.types import *

from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark2pmml import PMMLBuilder

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper, NormalChartData, ChartJson
from bi.common import MLModelSummary, NormalCard, KpiData, C3ChartData, HtmlData, TableData
from bi.common import PySparkTrainTestResult, PySparkGridSearchResult
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative
from bi.narratives import utils as NarrativesUtils


from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.algorithms import GainLiftKS

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.mllib.evaluation import BinaryClassificationMetrics, MulticlassMetrics
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf,col
from pyspark.sql.types import *

from bi.settings import setting as GLOBALSETTINGS
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.pipeline import PipelineModel

from py4j.protocol import Py4JError


class MultilayerPerceptronPysparkScript(object):
    def __init__(self, data_frame, df_helper, df_context, spark, prediction_narrative, result_setter, meta_parser,
                 mlEnvironment="pyspark"):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._ignoreMsg = self._dataframe_context.get_message_ignore()
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["sparkmlpclassifier"]
        self._targetLevel = self._dataframe_context.get_target_level_for_model()

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._analysisName = self._slug
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._mlEnv = mlEnvironment

        self._scriptStages = {
            "initialization": {
                "summary": "Initialized the Multilayer Perceptron Scripts",
                "weight": 4
            },
            "training": {
                "summary": "Multilayer Perceptron Model Training Started",
                "weight": 2
            },
            "completion": {
                "summary": "Multilayer Perceptron Model Training Finished",
                "weight": 4
            },
        }

    def Train(self):
        st_global = time.time()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context, self._scriptWeightDict,
                                                            self._scriptStages, self._slug, "initialization", "info",
                                                            display=True, emptyBin=False, customMsg=None,
                                                            weightKey="total")

        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = [x for x in algosToRun if x.get_algorithm_slug()==self._slug][0]
        categorical_columns = self._dataframe_helper.get_string_columns()
        uid_col = self._dataframe_context.get_uid_column()

        if self._metaParser.check_column_isin_ignored_suggestion(uid_col):
            categorical_columns = list(set(categorical_columns) - {uid_col})

        allDateCols = self._dataframe_context.get_date_columns()
        categorical_columns = list(set(categorical_columns) - set(allDateCols))
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        appType = self._dataframe_context.get_app_type()

        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()

        # pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        # model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        # pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        levels = df.select(result_column).distinct().count()

        appType = self._dataframe_context.get_app_type()

        model_filepath = model_path + "/" + self._slug + "/model"
        pmml_filepath = str(model_path) + "/" + str(self._slug) + "/trainedModel.pmml"

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context, self._scriptWeightDict,
                                                            self._scriptStages, self._slug, "training", "info",
                                                            display=True, emptyBin=False, customMsg=None,
                                                            weightKey="total")

        st = time.time()
        pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns, categorical_columns, result_column)
        vectorFeats = pipeline.getStages()[-1].transform(df)
        input_feats = len(vectorFeats.select('features').take(1)[0][0])

        trainingData, validationData = MLUtils.get_training_and_validation_data(df, result_column, 0.8)  # indexed

        labelIndexer = StringIndexer(inputCol=result_column, outputCol="label")
        # OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")

        # Label Mapping and Inverse
        labelIdx = labelIndexer.fit(trainingData)
        labelMapping = {k: v for k, v in enumerate(labelIdx.labels)}
        inverseLabelMapping = {v: float(k) for k, v in enumerate(labelIdx.labels)}

        clf = MultilayerPerceptronClassifier()
        if not algoSetting.is_hyperparameter_tuning_enabled():
            algoParams = algoSetting.get_params_dict()
        else:
            algoParams = algoSetting.get_params_dict_hyperparameter()
        clfParams = [prm.name for prm in clf.params]

        algoParams = {getattr(clf, k): v if isinstance(v, list) else [v] for k, v in algoParams.items() if
                      k in clfParams}

        paramGrid = ParamGridBuilder()
        layer_param_val = algoParams[getattr(clf, 'layers')]

        for layer in layer_param_val:
            layer.insert(0, input_feats)
            layer.append(levels)

        print('layer_param_val =', layer_param_val)

        # if not algoSetting.is_hyperparameter_tuning_enabled():
        #     for k,v in algoParams.items():
        #         if k.name == 'layers':
        #             paramGrid = paramGrid.addGrid(k,layer_param_val)
        #         else:
        #             paramGrid = paramGrid.addGrid(k,v)
        #     paramGrid = paramGrid.build()
        # else:
        for k, v in algoParams.items():
            if v == [None] * len(v):
                continue
            if k.name == 'layers':
                paramGrid = paramGrid.addGrid(k, layer_param_val)
            else:
                paramGrid = paramGrid.addGrid(k, v)
        paramGrid = paramGrid.build()

        if len(paramGrid) > 1:
            hyperParamInitParam = algoSetting.get_hyperparameter_params()
            evaluationMetricDict = {"name": hyperParamInitParam["evaluationMetric"]}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[
                evaluationMetricDict["name"]]
        else:
            evaluationMetricDict = {"name": GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[
                evaluationMetricDict["name"]]

        self._result_setter.set_hyper_parameter_results(self._slug, None)

        if validationDict["name"] == "kFold":
            numFold = int(validationDict["value"])
            estimator = Pipeline(stages=[pipeline, labelIndexer, clf])
            if algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepath = "/".join(model_filepath.split("/")[:-1])
                pySparkHyperParameterResultObj = PySparkGridSearchResult(estimator, paramGrid, appType, modelFilepath,
                                                                         levels,
                                                                         evaluationMetricDict, trainingData,
                                                                         validationData, numFold, self._targetLevel,
                                                                         labelMapping, inverseLabelMapping,
                                                                         df)
                resultArray = pySparkHyperParameterResultObj.train_and_save_classification_models()
                self._result_setter.set_hyper_parameter_results(self._slug, resultArray)
                self._result_setter.set_metadata_parallel_coordinates(self._slug,
                                                                      {
                                                                          "ignoreList": pySparkHyperParameterResultObj.get_ignore_list(),
                                                                          "hideColumns": pySparkHyperParameterResultObj.get_hide_columns(),
                                                                          "metricColName": pySparkHyperParameterResultObj.get_comparison_metric_colname(),
                                                                          "columnOrder": pySparkHyperParameterResultObj.get_keep_columns()})

                bestModel = pySparkHyperParameterResultObj.getBestModel()
                prediction = pySparkHyperParameterResultObj.getBestPrediction()
                bestModelName = resultArray[0]["Model Id"]

            else:
                crossval = CrossValidator(estimator=estimator,
                                          estimatorParamMaps=paramGrid,
                                          evaluator=BinaryClassificationEvaluator() if levels == 2 else MulticlassClassificationEvaluator(),
                                          numFolds=3 if numFold is None else numFold)  # use 3+ folds in practice
                cvrf = crossval.fit(trainingData)
                prediction = cvrf.transform(validationData)
                bestModel = cvrf.bestModel
                bestModelName = "M" + "0" * (GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH - 1) + "1"

        else:
            train_test_ratio = float(self._dataframe_context.get_train_test_split())
            estimator = Pipeline(stages=[pipeline, labelIndexer, clf])
            if algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepath = "/".join(model_filepath.split("/")[:-1])
                pySparkHyperParameterResultObj = PySparkTrainTestResult(estimator, paramGrid, appType, modelFilepath,
                                                                        levels,
                                                                        evaluationMetricDict, trainingData,
                                                                        validationData, train_test_ratio,
                                                                        self._targetLevel, labelMapping,
                                                                        inverseLabelMapping,
                                                                        df)
                resultArray = pySparkHyperParameterResultObj.train_and_save_classification_models()
                self._result_setter.set_hyper_parameter_results(self._slug, resultArray)
                self._result_setter.set_metadata_parallel_coordinates(self._slug,
                                                                      {
                                                                          "ignoreList": pySparkHyperParameterResultObj.get_ignore_list(),
                                                                          "hideColumns": pySparkHyperParameterResultObj.get_hide_columns(),
                                                                          "metricColName": pySparkHyperParameterResultObj.get_comparison_metric_colname(),
                                                                          "columnOrder": pySparkHyperParameterResultObj.get_keep_columns()})

                bestModel = pySparkHyperParameterResultObj.getBestModel()
                prediction = pySparkHyperParameterResultObj.getBestPrediction()
                bestModelName = resultArray[0]["Model Id"]

            else:
                tvs = TrainValidationSplit(estimator=estimator,
                                           estimatorParamMaps=paramGrid,
                                           evaluator=BinaryClassificationEvaluator() if levels == 2 else MulticlassClassificationEvaluator(),
                                           trainRatio=train_test_ratio)

                tvrf = tvs.fit(trainingData)
                prediction = tvrf.transform(validationData)
                bestModel = tvrf.bestModel
                bestModelName = "M" + "0" * (GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH - 1) + "1"

        MLUtils.save_pipeline_or_model(bestModel,model_filepath)
        predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
        metrics = MulticlassMetrics(predsAndLabels)
        posLabel = inverseLabelMapping[self._targetLevel]

        conf_mat_ar = metrics.confusionMatrix().toArray()
        print(conf_mat_ar)
        confusion_matrix = {}
        for i in range(len(conf_mat_ar)):
            confusion_matrix[labelMapping[i]] = {}
            for j, val in enumerate(conf_mat_ar[i]):
                confusion_matrix[labelMapping[i]][labelMapping[j]] = val
        print(confusion_matrix)

        trainingTime = time.time() - st

        f1_score = metrics.fMeasure(inverseLabelMapping[self._targetLevel], 1.0)
        precision = metrics.precision(inverseLabelMapping[self._targetLevel])
        recall = metrics.recall(inverseLabelMapping[self._targetLevel])
        accuracy = metrics.accuracy
        roc_auc = 'Undefined'
        if levels == 2:
            bin_metrics = BinaryClassificationMetrics(predsAndLabels)
            roc_auc = bin_metrics.areaUnderROC
            precision = metrics.precision(inverseLabelMapping[self._targetLevel])
            recall = metrics.recall(inverseLabelMapping[self._targetLevel])
        print(f1_score,precision,recall,accuracy)

        #gain chart implementation
        def cal_prob_eval(x):
            if len(x) == 1:
                if x == posLabel:
                    return(float(x[1]))
                else:
                    return(float(1 - x[1]))
            else:
                return(float(x[int(posLabel)]))


        column_name= 'probability'
        def y_prob_for_eval_udf():
            return udf(lambda x:cal_prob_eval(x))
        prediction = prediction.withColumn("y_prob_for_eval", y_prob_for_eval_udf()(col(column_name)))

        try:
            pys_df = prediction.select(['y_prob_for_eval','prediction','label'])
            gain_lift_ks_obj = GainLiftKS(pys_df, 'y_prob_for_eval', 'prediction', 'label', posLabel, self._spark)
            gain_lift_KS_dataframe = gain_lift_ks_obj.Run().toPandas()
        except:
            try:
                temp_df = pys_df.toPandas()
                gain_lift_ks_obj = GainLiftKS(temp_df, 'y_prob_for_eval', 'prediction', 'label', posLabel, self._spark)
                gain_lift_KS_dataframe = gain_lift_ks_obj.Rank_Ordering()
            except:
                print("gain chant failed")
                gain_lift_KS_dataframe = None


        objs = {"trained_model": bestModel, "actual": prediction.select('label'),
                "predicted": prediction.select('prediction'),
                "probability": prediction.select('probability'), "feature_importance": None,
                "featureList": list(categorical_columns) + list(numerical_columns), "labelMapping": labelMapping}

        # Calculating prediction_split
        val_cnts = prediction.groupBy('label').count()
        val_cnts = map(lambda row: row.asDict(), val_cnts.collect())
        prediction_split = {}
        total_nos = objs['actual'].count()
        for item in val_cnts:
            classname = labelMapping[item['label']]
            prediction_split[classname] = round(item['count'] * 100 / float(total_nos), 2)

        if not algoSetting.is_hyperparameter_tuning_enabled():
            # modelName = "M" + "0" * (GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH - 1) + "1"
            modelFilepathArr = model_filepath.split("/")[:-1]
            modelFilepathArr.append(bestModelName)
            bestModel.save("/".join(modelFilepathArr))
        runtime = round((time.time() - st_global), 2)

        try:
            print(pmml_filepath)
            pmmlBuilder = PMMLBuilder(self._spark, trainingData, bestModel).putOption(clf, 'compact', True)
            pmmlBuilder.buildFile(pmml_filepath)
            pmmlfile = open(pmml_filepath, "r")
            pmmlText = pmmlfile.read()
            pmmlfile.close()
            self._result_setter.update_pmml_object({self._slug: pmmlText})
        except Exception as e:
            print("PMML failed...", str(e))
            pass

        cat_cols = list(set(categorical_columns) - {result_column})
        self._model_summary = MLModelSummary()
        self._model_summary.set_algorithm_name("Spark ML Multilayer Perceptron")
        self._model_summary.set_algorithm_display_name("Spark ML Multilayer Perceptron")
        self._model_summary.set_slug(self._slug)
        self._model_summary.set_training_time(runtime)
        self._model_summary.set_confusion_matrix(confusion_matrix)
        self._model_summary.set_feature_importance(objs["feature_importance"])
        self._model_summary.set_feature_list(objs["featureList"])
        self._model_summary.set_model_accuracy(accuracy)
        self._model_summary.set_training_time(round((time.time() - st), 2))
        self._model_summary.set_precision_recall_stats([precision, recall])
        self._model_summary.set_model_precision(precision)
        self._model_summary.set_model_recall(recall)
        self._model_summary.set_target_variable(result_column)
        self._model_summary.set_prediction_split(prediction_split)
        self._model_summary.set_validation_method("KFold")
        self._model_summary.set_level_map_dict(objs["labelMapping"])
        self._model_summary.set_model_features(objs["featureList"])
        self._model_summary.set_level_counts(
            self._metaParser.get_unique_level_dict(list(set(categorical_columns)) + [result_column]))
        self._model_summary.set_num_trees(None)
        self._model_summary.set_num_rules(300)
        self._model_summary.set_target_level(self._targetLevel)

        modelManagementJson = {
            "Model ID": "SPMLP-" + bestModelName,
            "Project Name": self._dataframe_context.get_job_name(),
            "Algorithm": self._model_summary.get_algorithm_name(),
            "Status": 'Completed',
            "Accuracy": accuracy,
            "Runtime": runtime,
            "Created On": "",
            "Owner": "",
            "Deployment": 0,
            "Action": ''
        }

        # if not algoSetting.is_hyperparameter_tuning_enabled():
        #     modelDropDownObj = {
        #         "name": self._model_summary.get_algorithm_name(),
        #         "evaluationMetricValue": locals()[evaluationMetricDict["name"]], # accuracy
        #         "evaluationMetricName": evaluationMetricDict["displayName"], # accuracy
        #         "slug": self._model_summary.get_slug(),
        #         "Model Id": bestModelName
        #     }
        #     modelSummaryJson = {
        #         "dropdown": modelDropDownObj,
        #         "levelcount": self._model_summary.get_level_counts(),
        #         "modelFeatureList": self._model_summary.get_feature_list(),
        #         "levelMapping": self._model_summary.get_level_map_dict(),
        #         "slug": self._model_summary.get_slug(),
        #         "name": self._model_summary.get_algorithm_name()
        #     }
        # else:
        modelDropDownObj = {
            "name": self._model_summary.get_algorithm_name(),
            "evaluationMetricValue": accuracy, #locals()[evaluationMetricDict["name"]],
            "evaluationMetricName": "accuracy", # evaluationMetricDict["name"],
            "slug": self._model_summary.get_slug(),
            "Model Id": bestModelName
        }
        modelSummaryJson = {
            "dropdown": modelDropDownObj,
            "levelcount": self._model_summary.get_level_counts(),
            "modelFeatureList": self._model_summary.get_feature_list(),
            "levelMapping": self._model_summary.get_level_map_dict(),
            "slug": self._model_summary.get_slug(),
            "name": self._model_summary.get_algorithm_name()
        }

        mlpcCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in
                     MLUtils.create_model_summary_cards(self._model_summary)]
        for card in mlpcCards:
            self._prediction_narrative.add_a_card(card)

        self._result_setter.set_model_summary(
            {"sparkperceptron": json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_spark_multilayer_perceptron_model_summary(modelSummaryJson)
        self._result_setter.set_spark_multilayer_perceptron_management_summary(modelManagementJson)
        self._result_setter.set_mlpc_cards(mlpcCards)

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context, self._scriptWeightDict,
                                                            self._scriptStages, self._slug, "completion", "info",
                                                            display=True, emptyBin=False, customMsg=None,
                                                            weightKey="total")

    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization": {
                "summary": "Initialized the Multilayer Perceptron Scripts",
                "weight": 2
            },
            "prediction": {
                "summary": "Spark ML Multilayer Perceptron Model Prediction Finished",
                "weight": 2
            },
            "frequency": {
                "summary": "descriptive analysis finished",
                "weight": 2
            },
            "chisquare": {
                "summary": "chi Square analysis finished",
                "weight": 4
            },
            "completion": {
                "summary": "all analysis finished",
                "weight": 4
            },
        }

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"] * \
                                  self._scriptStages["initialization"]["weight"] / 10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,
                                                                     "initialization",
                                                                     "info",
                                                                     self._scriptStages["initialization"]["summary"],
                                                                     self._completionStatus,
                                                                     self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL, progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        time_dimension_columns = self._dataframe_helper.get_timestamp_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame, categorical_columns,
                                                              self._dataframe_context.get_column_separator(),
                                                              output_type="dict", dataType="spark")
        for key in level_counts_train:
            if key in level_counts_score:
                if level_counts_train[key] != level_counts_score[key]:
                    dataSanity = False
            else:
                dataSanity = False

        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path() + "/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        trained_model_path = "/".join(trained_model_path.split("/")[
                                      :-1]) + "/" + self._slug + "/" + self._dataframe_context.get_model_for_scoring()
        # score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        pipelineModel = MLUtils.load_pipeline(trained_model_path)

        df = self._data_frame
        transformed = pipelineModel.transform(df)
        label_indexer_dict = MLUtils.read_string_indexer_mapping(trained_model_path, SQLctx)
        prediction_to_levels = udf(lambda x: label_indexer_dict[x], StringType())
        transformed = transformed.withColumn(result_column, prediction_to_levels(transformed.prediction))
        # transformed.show()

        if "probability" in transformed.columns:
            probability_dataframe = transformed.select([result_column, "probability"]).toPandas()
            probability_dataframe = probability_dataframe.rename(index=str, columns={result_column: "predicted_class"})
            probability_dataframe["predicted_probability"] = probability_dataframe["probability"].apply(
                lambda x: max(x))
            self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(probability_dataframe)
            self._score_summary["result_column"] = result_column
            scored_dataframe = transformed.select(
                categorical_columns + time_dimension_columns + numerical_columns + [result_column,
                                                                                    "probability"]).toPandas()
            # scored_dataframe = scored_dataframe.rename(index=str, columns={"predicted_probability": "probability"})
        else:
            self._score_summary["prediction_split"] = []
            self._score_summary["result_column"] = result_column
            scored_dataframe = transformed.select(
                categorical_columns + time_dimension_columns + numerical_columns + [result_column]).toPandas()

        labelMappingDict = self._dataframe_context.get_label_map()
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        scored_dataframe.to_csv(score_data_path, header=True, index=False)

        uidCol = self._dataframe_context.get_uid_column()
        if uidCol == None:
            uidCols = self._metaParser.get_suggested_uid_columns()
            if len(uidCols) > 0:
                uidCol = uidCols[0]
        uidTableData = []
        predictedClasses = list(scored_dataframe[result_column].unique())
        if uidCol:
            if uidCol in df.columns:
                for level in predictedClasses:
                    levelDf = scored_dataframe[scored_dataframe[result_column] == level]
                    levelDf = levelDf[[uidCol, "predicted_probability", result_column]]
                    levelDf.sort_values(by="predicted_probability", ascending=False, inplace=True)
                    levelDf["predicted_probability"] = levelDf["predicted_probability"].apply(
                        lambda x: humanize.apnumber(x * 100) + "%" if x * 100 >= 10 else str(int(x * 100)) + "%")
                    uidTableData.append(levelDf[:5])
                uidTableData = pd.concat(uidTableData)
                uidTableData = [list(arr) for arr in list(uidTableData.values)]
                uidTableData = [[uidCol, "Probability", result_column]] + uidTableData
                uidTable = TableData()
                uidTable.set_table_width(25)
                uidTable.set_table_data(uidTableData)
                uidTable.set_table_type("normalHideColumn")
                self._result_setter.set_unique_identifier_table(
                    json.loads(CommonUtils.convert_python_object_to_json(uidTable)))

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"] * \
                                  self._scriptStages["prediction"]["weight"] / 10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName, \
                                                                     "prediction", \
                                                                     "info", \
                                                                     self._scriptStages["prediction"]["summary"], \
                                                                     self._completionStatus, \
                                                                     self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL, progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        print("STARTING DIMENSION ANALYSIS ...")
        columns_to_keep = []
        columns_to_drop = []

        columns_to_keep = self._dataframe_context.get_score_consider_columns()

        if len(columns_to_keep) > 0:
            columns_to_drop = list(set(df.columns) - set(columns_to_keep))
        else:
            columns_to_drop += ["predicted_probability"]

        scored_df = transformed.select(
            categorical_columns + time_dimension_columns + numerical_columns + [result_column])
        columns_to_drop = [x for x in columns_to_drop if x in scored_df.columns]
        modified_df = scored_df.select([x for x in scored_df.columns if x not in columns_to_drop])
        resultColLevelCount = dict(modified_df.groupby(result_column).count().collect())
        self._metaParser.update_column_dict(result_column, {"LevelCount": resultColLevelCount,
                                                            "numberOfUniqueValues": len(resultColLevelCount.keys())})
        self._dataframe_context.set_story_on_scored_data(True)

        self._dataframe_context.update_consider_columns(columns_to_keep)
        df_helper = DataFrameHelper(modified_df, self._dataframe_context, self._metaParser)
        df_helper.set_params()
        spark_scored_df = df_helper.get_data_frame()

        if len(predictedClasses) >= 2:
            try:
                fs = time.time()
                df_decision_tree_obj = DecisionTrees(spark_scored_df, df_helper, self._dataframe_context, self._spark,
                                                     self._metaParser, scriptWeight=self._scriptWeightDict,
                                                     analysisName=self._analysisName).test_all(
                    dimension_columns=[result_column])
                narratives_obj = CommonUtils.as_dict(
                    DecisionTreeNarrative(result_column, df_decision_tree_obj, self._dataframe_helper,
                                          self._dataframe_context, self._metaParser, self._result_setter,
                                          story_narrative=None, analysisName=self._analysisName,
                                          scriptWeight=self._scriptWeightDict))
                print(narratives_obj)
            except Exception as e:
                print("DecisionTree Analysis Failed ", str(e))
        else:
            data_dict = {"npred": len(predictedClasses), "nactual": len(labelMappingDict.values())}

            if data_dict["nactual"] > 2:
                levelCountDict[predictedClasses[0]] = resultColLevelCount[predictedClasses[0]]
                levelCountDict["Others"] = sum([v for k, v in resultColLevelCount.items() if k != predictedClasses[0]])
            else:
                levelCountDict = resultColLevelCount
                otherClass = list(set(labelMappingDict.values()) - set(predictedClasses))[0]
                levelCountDict[otherClass] = 0

                print(levelCountDict)

            total = float(sum([x for x in levelCountDict.values() if x != None]))
            levelCountTuple = [({"name": k, "count": v, "percentage": humanize.apnumber(v * 100 / total) + "%"}) for
                               k, v in levelCountDict.items() if v != None]
            levelCountTuple = sorted(levelCountTuple, key=lambda x: x["count"], reverse=True)
            data_dict["blockSplitter"] = "|~NEWBLOCK~|"
            data_dict["targetcol"] = result_column
            data_dict["nlevel"] = len(levelCountDict.keys())
            data_dict["topLevel"] = levelCountTuple[0]
            data_dict["secondLevel"] = levelCountTuple[1]
            maincardSummary = NarrativesUtils.get_template_output("/apps/", 'scorewithoutdtree.html', data_dict)

            main_card = NormalCard()
            main_card_data = []
            main_card_narrative = NarrativesUtils.block_splitter(maincardSummary, "|~NEWBLOCK~|")
            main_card_data += main_card_narrative

            chartData = NormalChartData([levelCountDict]).get_data()
            chartJson = ChartJson(data=chartData)
            chartJson.set_title(result_column)
            chartJson.set_chart_type("donut")
            mainCardChart = C3ChartData(data=chartJson)
            mainCardChart.set_width_percent(33)
            main_card_data.append(mainCardChart)

            uidTable = self._result_setter.get_unique_identifier_table()
            if uidTable != None:
                main_card_data.append(uidTable)
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Predicting Key Drivers of {}".format(result_column))
            self._result_setter.set_score_dtree_cards([main_card])
