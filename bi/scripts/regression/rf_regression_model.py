from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from past.utils import old_div
import json
import time
from datetime import datetime

try:
    import pickle as pickle
except:
    import pickle

from itertools import chain

from pyspark.sql import SQLContext
from pyspark.sql.types import DoubleType
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.common import MLModelSummary,NormalCard,KpiData,C3ChartData,HtmlData,SklearnGridSearchResult,SkleanrKFoldResult

from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.common import NarrativesTree

from pyspark.sql.functions import udf
from pyspark.sql import functions as FN
from pyspark.sql.types import *
from pyspark.ml.regression import RandomForestRegressor as pysparkRandomForestRegressor
from pyspark.ml.feature import IndexToString
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit,CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator

from bi.settings import setting as GLOBALSETTINGS
from bi.algorithms import DecisionTrees
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative
from bi.scripts.measureAnalysis.descr_stats import DescriptiveStatsScript
from bi.scripts.measureAnalysis.two_way_anova import TwoWayAnovaScript
from bi.scripts.measureAnalysis.decision_tree_regression import DecisionTreeRegressionScript

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score,explained_variance_score
from math import sqrt
import pandas as pd
import numpy as np
try:
    from sklearn.externals import joblib
except:
    import joblib
from sklearn2pmml import sklearn2pmml
from sklearn2pmml import PMMLPipeline

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ParameterGrid





class RFRegressionModelScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser,mlEnvironment):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["rfregression"]
        self._datasetName = CommonUtils.get_dataset_name(self._dataframe_context.CSV_FILE)

        self._analysisName = "rfRegression"
        self._dataframe_context.set_analysis_name(self._analysisName)
        self._mlEnv = mlEnvironment

        self._completionStatus = self._dataframe_context.get_completion_status()
        print(self._completionStatus,"initial completion status")
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._ignoreMsg = self._dataframe_context.get_message_ignore()


        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Random Forest Regression Scripts",
                "weight":1
                },
            "training":{
                "summary":"Random Forest Regression Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Random Forest Regression Model Training Finished",
                "weight":1
                },
            }

    def Train(self):
        st_global = time.time()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"initialization","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        appType = self._dataframe_context.get_app_type()
        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = [x for x in algosToRun if x.get_algorithm_slug()==self._slug][0]
        categorical_columns = self._dataframe_helper.get_string_columns()
        uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(uid_col):
            categorical_columns = list(set(categorical_columns) - {uid_col})
        allDateCols = self._dataframe_context.get_date_columns()
        categorical_columns = list(set(categorical_columns)-set(allDateCols))
        print(categorical_columns)
        result_column = self._dataframe_context.get_result_column()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        numerical_columns = [x for x in numerical_columns if x != result_column]

        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()
        print("model_path",model_path)
        pipeline_filepath = str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        if self._dataframe_context.get_trainerMode() == "autoML":
            automl_enable=True
        else:
            automl_enable=False
        if  self._mlEnv == "spark":
            pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns,categorical_columns,result_column,algoType="regression")
            # trainingData, validationData = MLUtils.get_training_and_validation_data(df ,result_column,0.8)
            pipelineModel = pipeline.fit(df)
            indexed = pipelineModel.transform(df)
            featureMapping = sorted((attr["idx"], attr["name"]) for attr in (chain(*list(indexed.schema["features"].metadata["ml_attr"]["attrs"].values()))))

            # print indexed.select([result_column,"features"]).show(5)
            MLUtils.save_pipeline_or_model(pipelineModel,pipeline_filepath)
            # OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")
            clf = pysparkRandomForestRegressor(labelCol=result_column, featuresCol='features',predictionCol="prediction")
            if not algoSetting.is_hyperparameter_tuning_enabled():
                algoParams = algoSetting.get_params_dict()
            else:
                algoParams = algoSetting.get_params_dict_hyperparameter()
            clfParams = [prm.name for prm in clf.params]
            algoParams = {getattr(clf, k):v if isinstance(v, list) else [v] for k,v in algoParams.items() if k in clfParams}

            paramGrid = ParamGridBuilder()
            for k,v in algoParams.items():
                if v == [None] * len(v):
                    continue
                paramGrid = paramGrid.addGrid(k,v)
            paramGrid = paramGrid.build()

            if len(paramGrid) > 1:
                hyperParamInitParam = algoSetting.get_hyperparameter_params()
                evaluationMetricDict = {"name":hyperParamInitParam["evaluationMetric"]}
                evaluationMetricDict["displayName"] = GLOBALSETTINGS.PYSPARK_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
            else:
                evaluationMetricDict = algoSetting.get_evaluvation_metric(Type="Regression")
                evaluationMetricDict["displayName"] = GLOBALSETTINGS.PYSPARK_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]

            if validationDict["name"] == "kFold":
                defaultSplit = GLOBALSETTINGS.DEFAULT_VALIDATION_OBJECT["value"]
                numFold = int(validationDict["value"])
                if automl_enable:
                    params_grid = {
                                    'minInstancesPerNode': [2,3],
                                    'numTrees': [10,20,100]}
                    algoParams = {getattr(clf, k):v if isinstance(v, list) else \
                                   [v] for k,v in params_grid.items() if k in clfParams}
                    paramGrid = ParamGridBuilder()
                    for k,v in algoParams.items():
                        if v == [None] * len(v):
                             continue
                        paramGrid = paramGrid.addGrid(k,v)
                    paramGrid = paramGrid.build()
                trainingData,validationData = indexed.randomSplit([defaultSplit,1-defaultSplit], seed=12345)
                crossval = CrossValidator(estimator=clf,
                              estimatorParamMaps=paramGrid,
                              evaluator=RegressionEvaluator(metricName=evaluationMetricDict["displayName"],predictionCol="prediction", labelCol=result_column),
                              numFolds=numFold)
                st = time.time()
                cvModel = crossval.fit(indexed)
                trainingTime = time.time()-st
                print("cvModel training takes",trainingTime)
                bestEstimator = cvModel.bestModel
            elif validationDict["name"] == "trainAndtest":
                train_test_ratio = float(self._dataframe_context.get_train_test_split())
                trainingData,validationData = indexed.randomSplit([train_test_ratio,1-(train_test_ratio)], seed=12345)
                st = time.time()
                tvs = TrainValidationSplit(estimator=clf,
                              estimatorParamMaps=paramGrid,
                              evaluator=RegressionEvaluator(predictionCol="prediction", labelCol=result_column),
                              trainRatio=train_test_ratio)
                fit = tvs.fit(indexed)
                trainingTime = time.time()-st
                print("time to train",trainingTime)
                bestEstimator = fit.bestModel
            featureImportance = bestEstimator.featureImportances
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName)
                bestEstimator.save("/".join(modelFilepathArr))
            print(len(featureMapping))
            featuresArray = [(name, featureImportance[idx]) for idx, name in featureMapping]
            print(featuresArray)
            MLUtils.save_pipeline_or_model(bestEstimator,model_filepath)
            transformed = bestEstimator.transform(validationData)
            transformed = transformed.withColumn(result_column,transformed[result_column].cast(DoubleType()))
            transformed = transformed.select([result_column,"prediction",transformed[result_column]-transformed["prediction"]])
            transformed = transformed.withColumnRenamed(transformed.columns[-1],"difference")
            transformed = transformed.select([result_column,"prediction","difference",old_div(FN.abs(transformed["difference"])*100,transformed[result_column])])
            transformed = transformed.withColumnRenamed(transformed.columns[-1],"mape")
            sampleData = None
            nrows = transformed.count()
            modelmanagement_={param[0].name: param[1] for param in clf.extractParamMap().items()}
            if nrows > 100:
                sampleData = transformed.sample(False, float(100)/nrows, seed=420)
            else:
                sampleData = transformed
            print(sampleData.show())
            evaluator = RegressionEvaluator(predictionCol="prediction",labelCol=result_column)
            metrics = {}
            metrics["r2"] = evaluator.evaluate(transformed,{evaluator.metricName: "r2"})
            metrics["RMSE"] = evaluator.evaluate(transformed,{evaluator.metricName: "rmse"})
            metrics["neg_mean_squared_error"] = evaluator.evaluate(transformed,{evaluator.metricName: "mse"})
            metrics["neg_mean_absolute_error"] = evaluator.evaluate(transformed,{evaluator.metricName: "mae"})
            runtime = round((time.time() - st_global),2)
            # print transformed.count()
            mapeDf = transformed.select("mape")
            self._result_setter.set_hyper_parameter_results(self._slug,None)
            # print mapeDf.show()
            mapeStats = MLUtils.get_mape_stats(mapeDf,"mape")
            mapeStatsArr = list(mapeStats.items())
            mapeStatsArr = sorted(mapeStatsArr,key=lambda x:int(x[0]))
            # print mapeStatsArr
            quantileDf = transformed.select("prediction")
            # print quantileDf.show()
            quantileSummaryDict = MLUtils.get_quantile_summary(quantileDf,"prediction")
            quantileSummaryArr = list(quantileSummaryDict.items())
            quantileSummaryArr = sorted(quantileSummaryArr,key=lambda x:int(x[0]))
            pred_list = transformed.select('prediction').collect()
            predicted=[int(row.prediction) for row in pred_list]
            objs = {"trained_model":bestEstimator,"predicted":predicted,
            "feature_importance":featureImportance,
            "featureList":list(categorical_columns) + list(numerical_columns)}
            self._model_summary.set_model_type("regression")
            self._model_summary.set_algorithm_name("RF Regression")
            self._model_summary.set_algorithm_display_name("Random Forest Regression")
            self._model_summary.set_slug(self._slug)
            self._model_summary.set_training_time(runtime)
            self._model_summary.set_training_time(trainingTime)
            self._model_summary.set_target_variable(result_column)
            self._model_summary.set_validation_method(validationDict["displayName"])
            self._model_summary.set_model_evaluation_metrics(metrics)
            self._model_summary.set_feature_importance(objs["feature_importance"])
            self._model_summary.set_feature_list(objs["featureList"])
            self._model_summary.set_model_features(objs["featureList"])
            self._model_summary.set_model_params(modelmanagement_)
            self._model_summary.set_quantile_summary(quantileSummaryArr)
            self._model_summary.set_mape_stats(mapeStatsArr)
            self._model_summary.set_sample_data(sampleData.toPandas().to_dict())
            self._model_summary.set_feature_importance(featuresArray)
            self._model_summary.set_model_mse(metrics["neg_mean_squared_error"])
            self._model_summary.set_model_mae(metrics["neg_mean_absolute_error"])
            self._model_summary.set_rmse(metrics["RMSE"])
            self._model_summary.set_model_rsquared(metrics["r2"])
            # print CommonUtils.convert_python_object_to_json(self._model_summary)
            print(modelmanagement_)
            self._model_management = MLModelSummary()
            self._model_management.set_max_bins(data=modelmanagement_['maxBins'])
            self._model_management.set_max_depth(data=modelmanagement_['maxDepth'])
            self._model_management.set_min_instances_per_node(data=modelmanagement_['minInstancesPerNode'])
            self._model_management.set_min_info_gain(data=modelmanagement_['minInfoGain'])
            self._model_management.set_cacheNodeIds(data=modelmanagement_['cacheNodeIds'])
            self._model_management.set_checkpoint_interval(data=modelmanagement_['checkpointInterval'])
            self._model_management.set_impurity(data=modelmanagement_['impurity'])
            self._model_management.set_num_of_trees(data=modelmanagement_['numTrees'])
            self._model_management.set_feature_subset_strategy(data=modelmanagement_['featureSubsetStrategy'])
            self._model_management.set_subsampling_rate(data=modelmanagement_['subsamplingRate'])
            self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
            self._model_management.set_training_status(data="completed")# training status
            self._model_management.set_no_of_independent_variables(data=df) #no of independent varables
            self._model_management.set_training_time(runtime) # run time
            self._model_management.set_algorithm_name("Random Forest Regression")#algorithm name
            self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
            self._model_management.set_target_variable(result_column)#target column name
            self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M ')))#creation date
            self._model_management.set_datasetName(self._datasetName)
            self._model_management.set_rmse(metrics["RMSE"])
            self._model_management.set_model_mse(metrics["neg_mean_squared_error"])
            self._model_management.set_model_mae(metrics["neg_mean_absolute_error"])
            self._model_management.set_model_rsquared(metrics["r2"])

            modelManagementModelSettingsJson = [

                                      ["Training Dataset",self._model_management.get_datasetName()],
                                      ["Target Column",self._model_management.get_target_variable()],
                                      ["Target Column Value",self._model_management.get_target_level()],
                                      ["Number Of Independent Variables",self._model_management.get_no_of_independent_variables()],
                                      ["Algorithm",self._model_management.get_algorithm_name()],
                                      ["Model Validation",self._model_management.get_validation_method()],
                                      ["Max Bins",self._model_management.get_max_bins()],
                                      ["Max Depth",self._model_management.get_max_depth()],
                                      ["Minimum Instances Per Node",self._model_management.get_min_instances_per_node()],
                                      ["Minimum Information Gain",self._model_management.get_min_info_gain()],
                                      ["CacheNodeIds",self._model_management.get_cacheNodeIds()],
                                      ["Checkpoint Interval",self._model_management.get_checkpoint_interval()],
                                      ["Impurity",self._model_management.get_impurity()],
                                      ["No of Trees",str(self._model_management.get_num_of_trees())],
                                      ["Feature Subset Strategy",self._model_management.get_feature_subset_strategy()],
                                      ["subsampling_rate",self._model_management.get_subsampling_rate()]
                                                      ]
        elif self._mlEnv == "sklearn":
            model_filepath = model_path+"/"+self._slug+"/model.pkl"
            x_train,x_test,y_train,y_test = self._dataframe_helper.get_train_test_data()
            x_train = MLUtils.create_dummy_columns(x_train,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.create_dummy_columns(x_test,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.fill_missing_columns(x_test,x_train.columns,result_column)
            if self._dataframe_context.get_trainerMode() == "autoML":
                automl_enable=True
            else:
                automl_enable=False

            st = time.time()
            est = RandomForestRegressor()

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            if algoSetting.is_hyperparameter_tuning_enabled():
                hyperParamInitParam = algoSetting.get_hyperparameter_params()
                evaluationMetricDict = {"name":hyperParamInitParam["evaluationMetric"]}
                evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
                hyperParamAlgoName = algoSetting.get_hyperparameter_algo_name()
                params_grid = algoSetting.get_params_dict_hyperparameter()
                params_grid = {k:v for k,v in list(params_grid.items()) if k in est.get_params()}
                print(params_grid)
                if hyperParamAlgoName == "gridsearchcv":
                    estGrid = GridSearchCV(est,params_grid)
                    gridParams = estGrid.get_params()
                    hyperParamInitParam = {k:v for k,v in list(hyperParamInitParam.items()) if k in gridParams}
                    estGrid.set_params(**hyperParamInitParam)
                    # estGrid.fit(x_train,y_train)
                    grid_param={}
                    grid_param['params']=ParameterGrid(params_grid)
                    #bestEstimator = estGrid.best_estimator_
                    modelFilepath = "/".join(model_filepath.split("/")[:-1])
                    sklearnHyperParameterResultObj = SklearnGridSearchResult(grid_param,est,x_train,x_test,y_train,y_test,appType,modelFilepath,evaluationMetricDict=evaluationMetricDict)
                    resultArray = sklearnHyperParameterResultObj.train_and_save_models()
                    self._result_setter.set_hyper_parameter_results(self._slug,resultArray)
                    self._result_setter.set_metadata_parallel_coordinates(self._slug,{"ignoreList":sklearnHyperParameterResultObj.get_ignore_list(),"hideColumns":sklearnHyperParameterResultObj.get_hide_columns(),"metricColName":sklearnHyperParameterResultObj.get_comparison_metric_colname(),"columnOrder":sklearnHyperParameterResultObj.get_keep_columns()})
                    bestEstimator = sklearnHyperParameterResultObj.getBestModel()
                    bestParams = sklearnHyperParameterResultObj.getBestParam()
                    bestEstimator = bestEstimator.set_params(**bestParams)
                    bestEstimator.fit(x_train,y_train)

                elif hyperParamAlgoName == "randomsearchcv":
                    estRand = RandomizedSearchCV(est,params_grid)
                    estRand.set_params(**hyperParamInitParam)
                    bestEstimator = None
            else:
                evaluationMetricDict = algoSetting.get_evaluvation_metric(Type="Regression")
                evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
                algoParams = algoSetting.get_params_dict()
                algoParams = {k:v for k,v in list(algoParams.items()) if k in list(est.get_params().keys())}
                self._result_setter.set_hyper_parameter_results(self._slug,None)
                if automl_enable:
                    params_grid = { 'random_state': [42] }

                    if x_train.shape[0]*x_train.shape[1] < 10000:
                        params_grid.update({
                                            'bootstrap': [False, True],
                                            'n_estimators': [10, 25, 50, 100],
                                            'max_depth': [None, 3, 4, 5],
                                            'min_samples_split': [2, 3, 5],
                                            'min_samples_leaf': [1, 2, 3],
                                            'max_features': ['auto', 'sqrt', 'log2'] })
                        print('\n****************SMALL DATASET PARAMS****************\n')

                    elif (x_train.shape[0]*x_train.shape[1] >= 10000) & (x_train.shape[0]*x_train.shape[1] < 75000):
                        params_grid.update({
                                            'n_estimators': [50, 100, 150, 200],
                                            'max_depth': [None, 5, 10, 15],
                                            'min_samples_leaf': [1, 3, 5],
                                            'max_features': ['auto', 'sqrt'] })
                        print('\n****************MEDIUM DATASET PARAMS****************\n')

                    else:
                        params_grid.update({
                                            'n_estimators': [50, 100, 200, 400],
                                            'max_depth': [None, 10, 25, 50],
                                            'min_samples_leaf': [1, 5, 10],
                                            'max_features': ['auto', 'sqrt'] })
                        print('\n****************LARGE DATASET PARAMS****************\n')

                    hyperParamInitParam={'evaluationMetric': 'accuracy', 'kFold': 10}
                    grid_param={}
                    grid_param['params']=ParameterGrid(params_grid)
                    #bestEstimator = estGrid.best_estimator_
                    modelFilepath = "/".join(model_filepath.split("/")[:-1])
                    sklearnHyperParameterResultObj = SklearnGridSearchResult(grid_param,est,x_train,x_test,y_train,y_test,appType,modelFilepath,evaluationMetricDict=evaluationMetricDict)
                    resultArray = sklearnHyperParameterResultObj.train_and_save_models()
                    #self._result_setter.set_hyper_parameter_results(self._slug,resultArray)
                    #self._result_setter.set_metadata_parallel_coordinates(self._slug,{"ignoreList":sklearnHyperParameterResultObj.get_ignore_list(),"hideColumns":sklearnHyperParameterResultObj.get_hide_columns(),"metricColName":sklearnHyperParameterResultObj.get_comparison_metric_colname(),"columnOrder":sklearnHyperParameterResultObj.get_keep_columns()})
                    bestEstimator = sklearnHyperParameterResultObj.getBestModel()
                    bestParams = sklearnHyperParameterResultObj.getBestParam()
                    bestEstimator = bestEstimator.set_params(**bestParams)
                    bestEstimator.fit(x_train,y_train)
                    print("RandomForest Regression AuTO ML GridSearch#######################3")
                else:
                    est.set_params(**algoParams)

                    if validationDict["name"] == "kFold":
                        defaultSplit = GLOBALSETTINGS.DEFAULT_VALIDATION_OBJECT["value"]
                        numFold = int(validationDict["value"])
                        if numFold == 0:
                            numFold = 3
                        kFoldClass = SkleanrKFoldResult(numFold,est,x_train,x_test,y_train,y_test,appType,evaluationMetricDict=evaluationMetricDict)
                        kFoldClass.train_and_save_result()
                        kFoldOutput = kFoldClass.get_kfold_result()
                        bestEstimator = kFoldClass.get_best_estimator()
                    elif validationDict["name"] == "trainAndtest":
                        est.fit(x_train, y_train)
                        est.feature_names = list(x_train.columns.values)
                        bestEstimator = est
            trainingTime = time.time()-st
            y_score = bestEstimator.predict(x_test)
            try:
                y_prob = bestEstimator.predict_proba(x_test)
            except:
                y_prob = [0]*len(y_score)
            featureImportance={}

            objs = {"trained_model":bestEstimator,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":featureImportance,"featureList":list(x_train.columns),"labelMapping":{}}
            featureImportance = objs["trained_model"].feature_importances_
            featuresArray = [(col_name, featureImportance[idx]) for idx, col_name in enumerate(x_train.columns)]

            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName+".pkl")
                joblib.dump(objs["trained_model"],"/".join(modelFilepathArr))
            metrics = {}
            metrics["r2"] = r2_score(y_test, y_score)
            metrics["neg_mean_squared_error"] = mean_squared_error(y_test, y_score)
            metrics["neg_mean_absolute_error"] = mean_absolute_error(y_test, y_score)
            metrics["RMSE"] = sqrt(metrics["neg_mean_squared_error"])
            metrics["explained_variance_score"]=explained_variance_score(y_test, y_score)
            transformed = pd.DataFrame({"prediction":y_score,result_column:y_test})
            transformed["difference"] = transformed[result_column] - transformed["prediction"]
            transformed["mape"] = old_div(np.abs(transformed["difference"])*100,transformed[result_column])

            sampleData = None
            nrows = transformed.shape[0]
            if nrows > 100:
                sampleData = transformed.sample(n=100,random_state=420)
            else:
                sampleData = transformed
            print(sampleData.head())
            if transformed["mape"].max() > 100:
                GLOBALSETTINGS.MAPEBINS.append(transformed["mape"].max())
                mapeCountArr = list(pd.cut(transformed["mape"],GLOBALSETTINGS.MAPEBINS).value_counts().to_dict().items())
                GLOBALSETTINGS.MAPEBINS.pop(5)
            else:
                mapeCountArr = list(pd.cut(transformed["mape"],GLOBALSETTINGS.MAPEBINS).value_counts().to_dict().items())
            mapeStatsArr = [(str(idx),dictObj) for idx,dictObj in enumerate(sorted([{"count":x[1],"splitRange":(x[0].left,x[0].right)} for x in mapeCountArr],key = lambda x:x["splitRange"][0]))]

            predictionColSummary = transformed["prediction"].describe().to_dict()
            quantileBins = [predictionColSummary["min"],predictionColSummary["25%"],predictionColSummary["50%"],predictionColSummary["75%"],predictionColSummary["max"]]
            quantileBins = sorted(list(set(quantileBins)))
            transformed["quantileBinId"] = pd.cut(transformed["prediction"],quantileBins,include_lowest = True)
            quantileDf = transformed.groupby("quantileBinId").agg({"prediction":[np.sum,np.mean,np.size]}).reset_index()
            quantileDf.columns = ["prediction","sum","mean","count"]
            quantileDf = quantileDf.dropna(axis=0)
            quantileArr = list(quantileDf.T.to_dict().items())
            quantileSummaryArr = [(obj[0],{"splitRange":(obj[1]["prediction"].left,obj[1]["prediction"].right),"count":obj[1]["count"],"mean":obj[1]["mean"],"sum":obj[1]["sum"]}) for obj in quantileArr]
            print(quantileSummaryArr)
            runtime = round((time.time() - st_global),2)
            if algoSetting.is_hyperparameter_tuning_enabled() or automl_enable:
                modelName = resultArray[0]["Model Id"]
            self._model_summary.set_model_type("regression")
            self._model_summary.set_algorithm_name("RF Regression")
            self._model_summary.set_algorithm_display_name("Random Forest Regression")
            self._model_summary.set_slug(self._slug)
            self._model_summary.set_training_time(runtime)
            self._model_summary.set_training_time(trainingTime)
            self._model_summary.set_target_variable(result_column)
            self._model_summary.set_validation_method(validationDict["displayName"])
            self._model_summary.set_model_evaluation_metrics(metrics)
            self._model_summary.set_model_params(bestEstimator.get_params())
            self._model_summary.set_quantile_summary(quantileSummaryArr)
            self._model_summary.set_mape_stats(mapeStatsArr)
            self._model_summary.set_sample_data(sampleData.to_dict())
            self._model_summary.set_feature_importance(featuresArray)
            self._model_summary.set_feature_list(list(x_train.columns))
            self._model_summary.set_model_mse(metrics["neg_mean_squared_error"])
            self._model_summary.set_model_mae(metrics["neg_mean_absolute_error"])
            self._model_summary.set_rmse(metrics["RMSE"])
            self._model_summary.set_model_rsquared(metrics["r2"])
            self._model_summary.set_model_exp_variance_score(metrics["explained_variance_score"])


            try:
                pmml_filepath = str(model_path)+"/"+str(self._slug)+"/traindeModel.pmml"
                modelPmmlPipeline = PMMLPipeline([
                  ("pretrained-estimator", objs["trained_model"])
                ])
                modelPmmlPipeline.target_field = result_column
                modelPmmlPipeline.active_fields = np.array([col for col in x_train.columns if col != result_column])
                sklearn2pmml(modelPmmlPipeline, pmml_filepath, with_repr = True)
                pmmlfile = open(pmml_filepath,"r")
                pmmlText = pmmlfile.read()
                pmmlfile.close()
                self._result_setter.update_pmml_object({self._slug:pmmlText})
            except:
                pass
            modelmanagement_=self._model_summary.get_model_params()
            if not algoSetting.is_hyperparameter_tuning_enabled():
                self._model_management = MLModelSummary()
                self._model_management.set_criterion(data=modelmanagement_['criterion'])
                self._model_management.set_max_depth(data=modelmanagement_['max_depth'])
                self._model_management.set_min_instance_for_split(data=modelmanagement_['min_samples_split'])
                self._model_management.set_min_instance_for_leaf_node(data=modelmanagement_['min_samples_leaf'])
                self._model_management.set_max_leaf_nodes(data=modelmanagement_['max_leaf_nodes'])
                self._model_management.set_impurity_decrease_cutoff_for_split(data=str(modelmanagement_['min_impurity_decrease']))
                self._model_management.set_no_of_estimators(data=modelmanagement_['n_estimators'])
                self._model_management.set_bootstrap_sampling(data=modelmanagement_['bootstrap'])
                self._model_management.set_no_of_jobs(data=str(modelmanagement_['n_jobs']))
                self._model_management.set_warm_start(data=modelmanagement_['warm_start'])
                self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
                self._model_management.set_training_status(data="completed")# training status
                self._model_management.set_no_of_independent_variables(data=x_train) #no of independent varables
                #self._model_management.set_target_level(self._targetLevel) # target column value
                self._model_management.set_training_time(runtime) # run time
                self._model_management.set_algorithm_name("Random Forest Regression")#algorithm name
                self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
                self._model_management.set_target_variable(result_column)#target column name
                self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M ')))#creation date
                self._model_management.set_datasetName(self._datasetName)
                self._model_management.set_rmse(metrics["RMSE"])
                self._model_management.set_model_mse(metrics["neg_mean_squared_error"])
                self._model_management.set_model_mae(metrics["neg_mean_absolute_error"])
                self._model_management.set_model_rsquared(metrics["r2"])


            else:
                self._model_management = MLModelSummary()
                self._model_management.set_criterion(data=modelmanagement_['criterion'])
                self._model_management.set_max_depth(data=modelmanagement_['max_depth'])
                self._model_management.set_min_instance_for_split(data=modelmanagement_['min_samples_split'])
                self._model_management.set_min_instance_for_leaf_node(data=modelmanagement_['min_samples_leaf'])
                self._model_management.set_max_leaf_nodes(data=modelmanagement_['max_leaf_nodes'])
                self._model_management.set_impurity_decrease_cutoff_for_split(data=str(modelmanagement_['min_impurity_split']))
                self._model_management.set_no_of_estimators(data=modelmanagement_['n_estimators'])
                self._model_management.set_bootstrap_sampling(data=modelmanagement_['bootstrap'])
                self._model_management.set_no_of_jobs(data=str(modelmanagement_['n_jobs']))
                self._model_management.set_warm_start(data=modelmanagement_['warm_start'])
                self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
                self._model_management.set_training_status(data="completed")# training status
                self._model_management.set_no_of_independent_variables(data=x_train) #no of independent varables
                self._model_management.set_training_time(runtime) # run tim
                self._model_management.set_algorithm_name("Random Forest Regression")#algorithm name
                self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
                self._model_management.set_target_variable(result_column)#target column name
                self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M')))#creation date
                self._model_management.set_datasetName(self._datasetName)
                self._model_management.set_rmse(metrics["RMSE"])
                self._model_management.set_model_mse(metrics["neg_mean_squared_error"])
                self._model_management.set_model_mae(metrics["neg_mean_absolute_error"])
                self._model_management.set_model_rsquared(metrics["r2"])
            modelManagementModelSettingsJson = [

                                  ["Training Dataset",self._model_management.get_datasetName()],
                                  ["Target Column",self._model_management.get_target_variable()],
                                  ["Algorithm",self._model_management.get_algorithm_name()],
                                  ["Model Validation",self._model_management.get_validation_method()],
                                  ["Criterion",self._model_management.get_criterion()],
                                  ["Max Depth",self._model_management.get_max_depth()],
                                  ["Minimum Instances For Split",self._model_management.get_min_instance_for_split()],
                                  ["Minimum Instances For Leaf Node",self._model_management.get_min_instance_for_leaf_node()],
                                  ["Max Leaf Nodes",str(self._model_management.get_max_leaf_nodes())],
                                  ["Impurity Decrease cutoff for Split",self._model_management.get_impurity_decrease_cutoff_for_split()],
                                  ["No of Estimators",self._model_management.get_no_of_estimators()],
                                  ["Bootstrap Sampling",str(self._model_management.get_bootstrap_sampling())],
                                  ["No Of Jobs",self._model_management.get_no_of_jobs()]


                                                  ]
        if not algoSetting.is_hyperparameter_tuning_enabled():
            modelDropDownObj = {
                        "name":self._model_summary.get_algorithm_name(),
                        "evaluationMetricValue":metrics[evaluationMetricDict["name"]],
                        "evaluationMetricName":evaluationMetricDict["name"],
                        "slug":self._model_summary.get_slug(),
                        "Model Id":modelName
                        }

            modelSummaryJson = {
                "dropdown":modelDropDownObj,
                "levelcount":self._model_summary.get_level_counts(),
                "modelFeatureList":self._model_summary.get_feature_list(),
                "levelMapping":self._model_summary.get_level_map_dict(),
                "slug":self._model_summary.get_slug(),
                "name":self._model_summary.get_algorithm_name()
            }
        else:
            modelDropDownObj = {
                        "name":self._model_summary.get_algorithm_name(),
                        "evaluationMetricValue":metrics[evaluationMetricDict["name"]],
                        "evaluationMetricName":evaluationMetricDict["name"],
                        "slug":self._model_summary.get_slug(),
                        "Model Id":modelName
                        }
            modelSummaryJson = {
                "dropdown":modelDropDownObj,
                "levelcount":self._model_summary.get_level_counts(),
                "modelFeatureList":self._model_summary.get_feature_list(),
                "levelMapping":self._model_summary.get_level_map_dict(),
                "slug":self._model_summary.get_slug(),
                "name":self._model_summary.get_algorithm_name()
            }






        modelManagementSummaryJson = [

                        ["Project Name",self._model_management.get_job_type()],
                        ["Algorithm",self._model_management.get_algorithm_name()],
                        ["Training Status",self._model_management.get_training_status()],
                        ["RMSE",self._model_management.get_rmse()],
                        ["RunTime",self._model_management.get_training_time()],
                        #["Owner",None],
                        ["Created On",self._model_management.get_creation_date()]

                                    ]

        rfOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
        rfPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards_regression(self._model_summary)]
        rfDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
        #rfrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards_regression(self._model_summary)]
        rfrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        RF_Overview_Node = NarrativesTree()
        RF_Overview_Node.set_name("Overview")
        RF_Performance_Node = NarrativesTree()
        RF_Performance_Node.set_name("Performance")
        RF_Deployment_Node = NarrativesTree()
        RF_Deployment_Node.set_name("Deployment")
        for card in rfOverviewCards:
            RF_Overview_Node.add_a_card(card)
        for card in rfDeploymentCards:
            RF_Deployment_Node.add_a_card(card)
        for card in rfPerformanceCards:
            RF_Performance_Node.add_a_card(card)

        rfrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]

        for card in rfrCards:
            self._prediction_narrative.add_a_card(card)
        self._result_setter.set_model_summary({"rfregression":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_rf_regression_model_summart(modelSummaryJson)
        self._result_setter.set_rfr_cards(rfrCards)
        self._result_setter.set_rfreg_nodes([RF_Overview_Node,RF_Performance_Node,RF_Deployment_Node])
        self._result_setter.set_rf_fail_card({"Algorithm_Name":"rfregression","Success":"True"})

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")



    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Random Forest Regression Scripts",
                "weight":2
                },
            "predictionStart":{
                "summary":"Random Forest Regression Model Prediction Started",
                "weight":2
                },
            "predictionFinished":{
                "summary":"Random Forest Regression Model Prediction Finished",
                "weight":6
                }
            }
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"initialization","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        dataSanity = True
        categorical_columns = self._dataframe_helper.get_string_columns()
        uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(uid_col):
            categorical_columns = list(set(categorical_columns) - {uid_col})
        allDateCols = self._dataframe_context.get_date_columns()
        categorical_columns = list(set(categorical_columns)-set(allDateCols))
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        test_data_path = self._dataframe_context.get_input_file()

        if self._mlEnv == "spark":
            score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
            trained_model_path = self._dataframe_context.get_model_path()
            trained_model_path += "/model"
            pipeline_path = "/".join(trained_model_path.split("/")[:-1])+"/pipeline"
            print("trained_model_path",trained_model_path)
            print("pipeline_path",pipeline_path)
            print("score_data_path",score_data_path)
            pipelineModel = MLUtils.load_pipeline(pipeline_path)
            trained_model = MLUtils.load_rf_regresssion_pyspark_model(trained_model_path)
            df = self._data_frame
            indexed = pipelineModel.transform(df)
            transformed = trained_model.transform(indexed)
            if result_column in transformed.columns:
                transformed = transformed.withColumnRenamed(result_column,"originalLabel")
            transformed = transformed.withColumnRenamed("prediction",result_column)
            pandas_scored_df = transformed.select(list(set(self._data_frame.columns+[result_column]))).toPandas()
            if score_data_path.startswith("file"):
                score_data_path = score_data_path[7:]
            pandas_scored_df.to_csv(score_data_path,header=True,index=False)
            if uid_col:
                pandas_scored_df = pandas_scored_df[[x for x in pandas_df.columns if x != uid_col]]
            y_score = pandas_scored_df[result_column]

            scoreKpiArray = MLUtils.get_scored_data_summary(y_score)
            kpiCard = NormalCard()
            kpiCardData = [KpiData(data=x) for x in scoreKpiArray]
            kpiCard.set_card_data(kpiCardData)
            kpiCard.set_cente_alignment(True)
            print(CommonUtils.convert_python_object_to_json(kpiCard))
            self._result_setter.set_kpi_card_regression_score(kpiCard)
            pandas_scored_df.to_csv(score_data_path,header=True,index=False)
            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"predictionFinished","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
            print("STARTING Measure ANALYSIS ...")
            columns_to_keep = []
            columns_to_drop = []
            columns_to_keep = self._dataframe_context.get_score_consider_columns()
            if len(columns_to_keep) > 0:
                columns_to_drop = list(set(df.columns)-set(columns_to_keep))
            else:
                columns_to_drop += ["predicted_probability"]
            columns_to_drop = [x for x in columns_to_drop if x in df.columns and x != result_column]
            print("columns_to_drop",columns_to_drop)
            spark_scored_df = transformed.select(list(set(columns_to_keep+[result_column])))

        elif self._mlEnv == "sklearn":
            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"predictionStart","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
            score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
            trained_model_path = "file://" + self._dataframe_context.get_model_path()
            trained_model_path += "/"+self._dataframe_context.get_model_for_scoring()+".pkl"
            print("trained_model_path",trained_model_path)
            print("score_data_path",score_data_path)
            if trained_model_path.startswith("file"):
                trained_model_path = trained_model_path[7:]
            trained_model = joblib.load(trained_model_path)
            model_columns = self._dataframe_context.get_model_features()
            print("model_columns",model_columns)
            try:
                df = self._data_frame.toPandas()
            except:
                df = self._data_frame.copy()
            # pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.create_dummy_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.fill_missing_columns(pandas_df,model_columns,result_column)

            if uid_col:
                pandas_df = pandas_df[[x for x in pandas_df.columns if x != uid_col]]
            pandas_df = pandas_df[trained_model.feature_names]
            y_score = trained_model.predict(pandas_df)

            scoreKpiArray = MLUtils.get_scored_data_summary(y_score)
            kpiCard = NormalCard()
            kpiCardData = [KpiData(data=x) for x in scoreKpiArray]
            kpiCard.set_card_data(kpiCardData)
            kpiCard.set_cente_alignment(True)
            print(CommonUtils.convert_python_object_to_json(kpiCard))
            self._result_setter.set_kpi_card_regression_score(kpiCard)

            pandas_df[result_column] = y_score
            df[result_column] = y_score
            df.to_csv(score_data_path,header=True,index=False)
            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"predictionFinished","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            print("STARTING Measure ANALYSIS ...")
            columns_to_keep = []
            columns_to_drop = []
            columns_to_keep = self._dataframe_context.get_score_consider_columns()
            if len(columns_to_keep) > 0:
                columns_to_drop = list(set(df.columns)-set(columns_to_keep))
            else:
                columns_to_drop += ["predicted_probability"]

            columns_to_drop = [x for x in columns_to_drop if x in df.columns and x != result_column]
            print("columns_to_drop",columns_to_drop)
            try:
                pandas_scored_df = df[list(set(columns_to_keep+[result_column]))]
            except:
                pandas_scored_df = df.copy()
            spark_scored_df = SQLctx.createDataFrame(pandas_scored_df)
            # spark_scored_df.write.csv(score_data_path+"/data",mode="overwrite",header=True)
            # TODO update metadata for the newly created dataframe
            self._dataframe_context.update_consider_columns(columns_to_keep)
            print(spark_scored_df.printSchema())

        df_helper = DataFrameHelper(spark_scored_df, self._dataframe_context,self._metaParser)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        # self._dataframe_context.set_dont_send_message(True)
        try:
            fs = time.time()
            descr_stats_obj = DescriptiveStatsScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,scriptWeight=self._scriptWeightDict,analysisName="Descriptive analysis")
            descr_stats_obj.Run()
            print("DescriptiveStats Analysis Done in ", time.time() - fs, " seconds.")
        except:
            print("Frequency Analysis Failed ")

        # try:
        #     fs = time.time()
        #     df_helper.fill_na_dimension_nulls()
        #     df = df_helper.get_data_frame()
        #     dt_reg = DecisionTreeRegressionScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,self._metaParser,scriptWeight=self._scriptWeightDict,analysisName="Predictive modeling")
        #     dt_reg.Run()
        #     print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
        # except:
        #     print "DTREE FAILED"

        try:
            fs = time.time()
            two_way_obj = TwoWayAnovaScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,self._metaParser,scriptWeight=self._scriptWeightDict,analysisName="Measure vs. Dimension")
            two_way_obj.Run()
            print("OneWayAnova Analysis Done in ", time.time() - fs, " seconds.")
        except:
            print("Anova Analysis Failed")
