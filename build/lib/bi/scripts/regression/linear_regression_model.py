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
from bi.common import NormalChartData, ChartJson


from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.common import NarrativesTree

from pyspark.sql.functions import udf
from pyspark.sql import functions as FN
from pyspark.sql.types import *
from pyspark.ml.regression import LinearRegression as Lr
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

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ParameterGrid
from sklearn.linear_model import ElasticNet


class LinearRegressionModelScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser,mLEnvironment):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["linearregression"]
        self._analysisName = "linearRegression"
        self._dataframe_context.set_analysis_name(self._analysisName)
        self._mlEnv = mLEnvironment#self._dataframe_context.get_ml_environment()
        self._datasetName = CommonUtils.get_dataset_name(self._dataframe_context.CSV_FILE)

        self._completionStatus = self._dataframe_context.get_completion_status()
        print(self._completionStatus,"initial completion status")
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._ignoreMsg = self._dataframe_context.get_message_ignore()
        print(self._scriptWeightDict)
        print("="*400)

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Linear Regression Scripts",
                "weight":1
                },
            "training":{
                "summary":"Linear Regression Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Linear Regression Model Training Finished",
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
        result_column = self._dataframe_context.get_result_column()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        numerical_columns = [x for x in numerical_columns if x != result_column]
        print("categorical_columns",categorical_columns)

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
        if self._mlEnv == "spark":
            pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns,categorical_columns,result_column,algoType="regression")

            pipelineModel = pipeline.fit(df)
            indexed = pipelineModel.transform(df)
            featureMapping = sorted((attr["idx"], attr["name"]) for attr in (chain(*list(indexed.schema["features"].metadata["ml_attr"]["attrs"].values()))))

            # print indexed.select([result_column,"features"]).show(5)
            MLUtils.save_pipeline_or_model(pipelineModel,pipeline_filepath)
            linr = Lr(labelCol=result_column, featuresCol='features',predictionCol="prediction",maxIter=10, regParam=0.3, elasticNetParam=0.8)
            if not algoSetting.is_hyperparameter_tuning_enabled():
                algoParams = algoSetting.get_params_dict()
            else:
                algoParams = algoSetting.get_params_dict_hyperparameter()
            clfParams = [prm.name for prm in linr.params]
            algoParams = {getattr(linr, k):v if isinstance(v, list) else [v] for k,v in algoParams.items() if k in clfParams}

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
                    paramGrid = ParamGridBuilder()\
                    .addGrid(linr.regParam, [0.1, 0.01]) \
                    .addGrid(linr.fitIntercept, [False, True])\
                    .addGrid(linr.elasticNetParam, [0.1,0.01,0.5,1.0])\
                    .build()
                trainingData,validationData = indexed.randomSplit([defaultSplit,1-defaultSplit], seed=12345)
                #paramGrid = ParamGridBuilder()\
                #    .addGrid(linr.regParam, [0.1, 0.01]) \
                #    .addGrid(linr.fitIntercept, [False, True])\
                #    .addGrid(linr.elasticNetParam, [0.0, 0.5, 1.0])\
                #    .build()
                crossval = CrossValidator(estimator=linr,
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
                tvs = TrainValidationSplit(estimator=linr,
                              estimatorParamMaps=paramGrid,
                              evaluator=RegressionEvaluator(predictionCol="prediction", labelCol=result_column),
                              trainRatio=train_test_ratio)
                fit = tvs.fit(indexed)
                trainingTime = time.time()-st
                print("time to train",trainingTime)
                bestEstimator = fit.bestModel
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName)
                bestEstimator.save("/".join(modelFilepathArr))
            # modelPmmlPipeline = PMMLPipeline([
            #   ("pretrained-estimator", objs["trained_model"])
            # ])
            # try:
            #     modelPmmlPipeline.target_field = result_column
            #     modelPmmlPipeline.active_fields = np.array([col for col in x_train.columns if col != result_column])
            #     sklearn2pmml(modelPmmlPipeline, pmml_filepath, with_repr = True)
            #     pmmlfile = open(pmml_filepath,"r")
            #     pmmlText = pmmlfile.read()
            #     pmmlfile.close()
            #     self._result_setter.update_pmml_object({self._slug:pmmlText})
            # except:
            #     pass

            coefficientsArray = [(name, bestEstimator.coefficients[idx]) for idx, name in featureMapping]
            MLUtils.save_pipeline_or_model(bestEstimator,model_filepath)
            transformed = bestEstimator.transform(validationData)
            transformed = transformed.withColumn(result_column,transformed[result_column].cast(DoubleType()))
            transformed = transformed.select([result_column,"prediction",transformed[result_column]-transformed["prediction"]])
            transformed = transformed.withColumnRenamed(transformed.columns[-1],"difference")
            transformed = transformed.select([result_column,"prediction","difference",old_div(FN.abs(transformed["difference"])*100,transformed[result_column])])
            transformed = transformed.withColumnRenamed(transformed.columns[-1],"mape")
            sampleData = None
            nrows = transformed.count()
            modelmanagement_={param[0].name: param[1] for param in linr.extractParamMap().items()}
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
            "feature_importance":None,
            "featureList":list(categorical_columns) + list(numerical_columns)}
            self._model_summary.set_model_type("regression")
            self._model_summary.set_algorithm_name("Linear Regression")
            self._model_summary.set_algorithm_display_name("Linear Regression")
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
            self._model_summary.set_coefficinets_array(coefficientsArray)
            self._model_summary.set_model_mse(metrics["neg_mean_squared_error"])
            self._model_summary.set_model_mae(metrics["neg_mean_absolute_error"])
            self._model_summary.set_rmse(metrics["RMSE"])
            self._model_summary.set_model_rsquared(metrics["r2"])
            # print CommonUtils.convert_python_object_to_json(self._model_summary)
            print(modelmanagement_)
            self._model_management = MLModelSummary()
            self._model_management.set_datasetName(self._datasetName)
            self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M')))#creation date
            self._model_management.set_target_variable(result_column)#target column name
            self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
            self._model_management.set_algorithm_name("Linear Regression")#algorithm name
            self._model_management.set_training_time(runtime) # run time
            self._model_management.set_training_status(data="completed")# training status
            self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
            self._model_management.set_fit_intercept(data=modelmanagement_['fitIntercept'])
            self._model_management.set_rmse(metrics["RMSE"])
            self._model_management.set_model_mse(metrics["neg_mean_squared_error"])
            self._model_management.set_model_mae(metrics["neg_mean_absolute_error"])
            self._model_management.set_model_rsquared(metrics["r2"])

            modelManagementModelSettingsJson =[
                        ["Training Dataset", self._model_management.get_datasetName()],
                        ["Target Column", self._model_management.get_target_variable()],
                        ["Algorithm", self._model_management.get_algorithm_name()],
                        ["Model Validation", self._model_management.get_validation_method()],
                        ["Fit Intercept", str(self._model_management.get_fit_intercept())],
                        ["Normalize",self._model_management.get_normalize_value()],
                        ["Copy_X", self._model_management.get_copy_x()]
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
            # x_train.to_csv("/home/gulshan/marlabs/datasets/lrTest/x_train.csv",index=False)
            # x_test.to_csv("/home/gulshan/marlabs/datasets/lrTest/x_test.csv",index=False)
            # y_train.to_csv("/home/gulshan/marlabs/datasets/lrTest/y_train.csv",index=False)
            # y_test.to_csv("/home/gulshan/marlabs/datasets/lrTest/y_test.csv",index=False)

            # print "features before VIF-"*100
            # print x_train.columns.tolist()
            # print len(x_train.columns)

            ############# Uncomment following part if you want to use VIF feature selection #############
            ######################## VIF feature slection block of code ########################

            # x_train_new = MLUtils.feature_selection_vif(x_train)
            # x_test_new =x_test[x_train_new.columns.tolist()]

            # print "features after VIF-"*100
            # print x_test_new.columns.tolist()
            # print len(x_test_new.columns)

            # x_train = x_train_new
            # x_test = x_test_new

            ######################## VIF feature slection block of code ########################

            st = time.time()
            est = LinearRegression()

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            self._dataframe_context.update_completion_status(self._completionStatus)
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
                    est = ElasticNet()
                    params_grid=param_grid = {"max_iter": [1, 5, 10],
                                            "alpha": [0,0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
                                            "l1_ratio": np.arange(0, 1.0, 0.1)}
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
                    print("Linear Regression AuTO ML GridSearch CV#######################3")
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
            # print x_train.columns
            trainingTime = time.time()-st
            y_score = bestEstimator.predict(x_test)
            try:
                y_prob = bestEstimator.predict_proba(x_test)
            except:
                y_prob = [0]*len(y_score)
            featureImportance={}

            objs = {"trained_model":bestEstimator,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":featureImportance,"featureList":list(x_train.columns),"labelMapping":{}}
            coefficients = objs["trained_model"].coef_
            coefficientsArray = [(col_name, coefficients[idx]) for idx, col_name in enumerate(x_train.columns)]
            interceptValue = None
            interceptValue = objs["trained_model"].intercept_


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
            runtime = round((time.time() - st_global),2)
            if algoSetting.is_hyperparameter_tuning_enabled() or automl_enable:
                modelName = resultArray[0]["Model Id"]
            self._model_summary.set_model_type("regression")
            self._model_summary.set_algorithm_name("Linear Regression")
            self._model_summary.set_algorithm_display_name("Linear Regression")
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
            self._model_summary.set_feature_importance(featureImportance)
            self._model_summary.set_feature_list(list(x_train.columns))
            self._model_summary.set_coefficinets_array(coefficientsArray)
            self._model_summary.set_intercept(interceptValue)
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
            modelmanagement_ = self._model_summary.get_model_params()
            self._model_management = MLModelSummary()
            if not algoSetting.is_hyperparameter_tuning_enabled():
                self._model_management.set_datasetName(self._datasetName)
                self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M')))#creation date
                self._model_management.set_target_variable(result_column)#target column name
                self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
                self._model_management.set_algorithm_name("Linear Regression")#algorithm name
                self._model_management.set_training_time(runtime) # run time
                self._model_management.set_training_status(data="completed")# training status
                self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
                self._model_management.set_rmse(data=self._model_summary.get_model_evaluation_metrics()["RMSE"])
                self._model_management.set_fit_intercept(data=modelmanagement_['fit_intercept'])
                self._model_management.set_normalize_value(data=str(modelmanagement_['normalize']))
                self._model_management.set_copy_x(data=str(modelmanagement_['copy_X']))
                if automl_enable:
                    self._model_management.set_l1_ratio(data=str(modelmanagement_['l1_ratio']))
                    self._model_management.set_alpha(data=str(modelmanagement_['alpha']))
                else:
                    self._model_management.set_no_of_jobs(data=str(modelmanagement_['n_jobs']))

            else:
                self._model_management.set_datasetName(self._datasetName)
                self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M')))#creation date
                self._model_management.set_target_variable(result_column)#target column name
                self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
                self._model_management.set_algorithm_name("Linear Regression")#algorithm name
                self._model_management.set_training_time(runtime) # run time
                self._model_management.set_training_status(data="completed")# training status
                self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
                self._model_management.set_rmse(data=self._model_summary.get_model_evaluation_metrics()["RMSE"])
                self._model_management.set_no_of_jobs(data=str(modelmanagement_['n_jobs']))
                self._model_management.set_fit_intercept(data=modelmanagement_['fit_intercept'])
                self._model_management.set_normalize_value(data=str(modelmanagement_['normalize']))
                self._model_management.set_copy_x(data=str(modelmanagement_['copy_X']))

            modelManagementModelSettingsJson =[
                        ["Training Dataset", self._model_management.get_datasetName()],
                        ["Target Column", self._model_management.get_target_variable()],
                        ["Algorithm", self._model_management.get_algorithm_name()],
                        ["Model Validation", self._model_management.get_validation_method()],
                        ["Fit Intercept", str(self._model_management.get_fit_intercept())],
                        ["Normalize",self._model_management.get_normalize_value()],
                        ["Copy_X", self._model_management.get_copy_x()]
                        ]
            if automl_enable:
                modelManagementModelSettingsJson.append(["Alpha", self._model_management.get_alpha()])
                modelManagementModelSettingsJson.append(["L1 ratio",self._model_management.get_l1_ratio()])
            else:
                modelManagementModelSettingsJson.append(["N jobs", self._model_management.get_no_of_jobs()])

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

        modelManagementSummaryJson =[
                    ["Project Name",self._model_management.get_job_type()],
                    ["Algorithm",self._model_management.get_algorithm_name()],
                    ["Training Status",self._model_management.get_training_status()],
                    ["Root Mean Squared Error",self._model_management.get_rmse()],
                    ["RunTime",self._model_management.get_training_time()],
                    #["Owner",None],
                    ["Created On",self._model_management.get_creation_date()]
                    ]

        linrOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
        linrPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards_regression(self._model_summary)]
        linrDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
        # linrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]

        linrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]

        linR_Overview_Node = NarrativesTree()
        linR_Performance_Node = NarrativesTree()
        linR_Deployment_Node = NarrativesTree()
        linR_Overview_Node.set_name("Overview")
        linR_Performance_Node.set_name("Performance")
        linR_Deployment_Node.set_name("Deployment")
        for card in linrOverviewCards:
            linR_Overview_Node.add_a_card(card)
        for card in linrPerformanceCards:
            linR_Performance_Node.add_a_card(card)
        for card in linrDeploymentCards:
            linR_Deployment_Node.add_a_card(card)
        for card in linrCards:
            self._prediction_narrative.add_a_card(card)
        self._result_setter.set_model_summary({"linearregression":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_linear_regression_model_summary(modelSummaryJson)
        self._result_setter.set_linr_cards(linrCards)
        self._result_setter.set_lreg_nodes([linR_Overview_Node, linR_Performance_Node, linR_Deployment_Node])
        self._result_setter.set_lr_fail_card({"Algorithm_Name":"linearregression","Success":"True"})

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")


    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Linear Regression Scripts",
                "weight":2
                },
            "predictionStart":{
                "summary":"Linear Regression Model Prediction Started",
                "weight":2
                },
            "predictionFinished":{
                "summary":"Linear Regression Model Prediction Finished",
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
        targetVariable = result_column

        if self._mlEnv == "spark":
            score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
            trained_model_path = self._dataframe_context.get_model_path()
            trained_model_path += "/model"
            pipeline_path = "/".join(trained_model_path.split("/")[:-1])+"/pipeline"
            print("trained_model_path",trained_model_path)
            print("pipeline_path",pipeline_path)
            print("score_data_path",score_data_path)
            pipelineModel = MLUtils.load_pipeline(pipeline_path)
            trained_model = MLUtils.load_linear_regresssion_pyspark_model(trained_model_path)
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
            # print "model_columns",model_columns
            try:
                df = self._data_frame.toPandas()
            except:
                df = self._data_frame.copy()
            # pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.create_dummy_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.fill_missing_columns(pandas_df,model_columns,result_column)
            if uid_col:
                pandas_df = pandas_df[[x for x in pandas_df.columns if x != uid_col]]
            print(len(model_columns),len(pandas_df.columns))
            pandas_df = pandas_df[trained_model.feature_names]
            y_score = trained_model.predict(pandas_df)
            coefficients = trained_model.coef_
            coefficientsArray = [(col_name, coefficients[idx]) for idx, col_name in enumerate(pandas_df.columns)]

            coefficientsCard = NormalCard()
            coefficientsArray = sorted(coefficientsArray,key=lambda x:abs(x[1]),reverse=True)
            coefficientsArray = [{"key":tup[0],"value":tup[1]} for tup in coefficientsArray]
            coefficientsArray = MLUtils.normalize_coefficients(coefficientsArray)
            chartDataValues = [x["value"] for x in coefficientsArray]
            coefficientsChartJson = ChartJson()
            coefficientsChartJson.set_data(coefficientsArray)
            coefficientsChartJson.set_chart_type("bar")
            coefficientsChartJson.set_label_text({'x':' ','y':'Coefficients'})
            coefficientsChartJson.set_axes({"x":"key","y":"value"})
            # coefficientsChartJson.set_title("Influence of Key Features on {}".format(targetVariable))
            # coefficientsChartJson.set_yaxis_number_format(".4f")
            coefficientsChartJson.set_yaxis_number_format(CommonUtils.select_y_axis_format(chartDataValues))
            coefficientsChart = C3ChartData(data=coefficientsChartJson)
            coefficientsCardData = [HtmlData(data="<h4>Influence of Key Features on {}</h4>".format(targetVariable)),coefficientsChart]
            coefficientsCard.set_card_data(coefficientsCardData)
            coefficientsCard = json.loads(CommonUtils.convert_python_object_to_json(coefficientsCard))
            self._result_setter.set_coeff_card_regression_score(coefficientsCard)

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


            print(df.columns)
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
        try:
            fs = time.time()
            descr_stats_obj = DescriptiveStatsScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,scriptWeight=self._scriptWeightDict,analysisName="Descriptive analysis")
            descr_stats_obj.Run()
            print("DescriptiveStats Analysis Done in ", time.time() - fs, " seconds.")
        except:
            print("DescriptiveStats Analysis Failed ")

        # try:
        #     fs = time.time()
        #     df_helper.fill_na_dimension_nulls()
        #     df = df_helper.get_data_frame()
        #     dt_reg = DecisionTreeRegressionScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,self._metaParser,scriptWeight=self._scriptWeightDict,analysisName="Predictive modeling")
        #     dt_reg.Run()
        #     print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
        # except:
        #     print "DTREE FAILED"
        #
        try:
            fs = time.time()
            two_way_obj = TwoWayAnovaScript(df, df_helper, self._dataframe_context, self._result_setter, self._spark,self._prediction_narrative,self._metaParser,scriptWeight=self._scriptWeightDict,analysisName="Measure vs. Dimension")
            two_way_obj.Run()
            print("OneWayAnova Analysis Done in ", time.time() - fs, " seconds.")
        except:
            print("Anova Analysis Failed")



        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Score Summary Finished",100,100,display=True)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=False)
