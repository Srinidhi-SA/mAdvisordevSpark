from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import json
import time
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

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

from pyspark.sql.functions import udf
from pyspark.sql import functions as FN
from pyspark.sql.types import *
from pyspark.ml.regression import DecisionTreeRegressor
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

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ParameterGrid

from bi.common import NarrativesTree





class TensorFlowRegScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser,mlEnvironment="sklearn"):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (TensorFlow)"]
        self._analysisName = "Neural Network (TensorFlow)"
        self._dataframe_context.set_analysis_name(self._analysisName)
        self._mlEnv = mlEnvironment
        self._datasetName = CommonUtils.get_dataset_name(self._dataframe_context.CSV_FILE)

        self._completionStatus = self._dataframe_context.get_completion_status()
        print(self._completionStatus,"initial completion status")
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._ignoreMsg = self._dataframe_context.get_message_ignore()


        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Neural Network (TensorFlow) Regression Scripts",
                "weight":1
                },
            "training":{
                "summary":"Neural Network (TensorFlow) Regression Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Neural Network (TensorFlow) Regression Model Training Finished",
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
        pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        if self._mlEnv == "spark":
            pass
        elif self._mlEnv == "sklearn":
            model_filepath = model_path+"/"+self._slug+"/model.pkl"
            x_train,x_test,y_train,y_test = self._dataframe_helper.get_train_test_data()
            x_train = MLUtils.create_dummy_columns(x_train,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.create_dummy_columns(x_test,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.fill_missing_columns(x_test,x_train.columns,result_column)

            st = time.time()

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            if algoSetting.is_hyperparameter_tuning_enabled():
                pass
            else:
                self._result_setter.set_hyper_parameter_results(self._slug,None)
                evaluationMetricDict = algoSetting.get_evaluvation_metric(Type="Regression")
                evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
                params_tf=algoSetting.get_tf_params_dict()
                algoParams = algoSetting.get_params_dict()
                algoParams = {k:v for k,v in list(algoParams.items())}

                model = tf.keras.models.Sequential()
                first_layer_flag=True

                for i in range(len(list(params_tf['hidden_layer_info'].keys()))):
                    if params_tf['hidden_layer_info'][str(i)]["layer"]=="Dense":

                        if first_layer_flag:
                            model.add(tf.keras.layers.Dense(params_tf['hidden_layer_info'][str(i)]["units"],
                            activation=params_tf['hidden_layer_info'][str(i)]["activation"],
                            input_shape=(len(x_train.columns),),
                            use_bias=params_tf['hidden_layer_info'][str(i)]["use_bias"],
                            kernel_initializer=params_tf['hidden_layer_info'][str(i)]["kernel_initializer"],
                            bias_initializer=params_tf['hidden_layer_info'][str(i)]["bias_initializer"],
                            kernel_regularizer=params_tf['hidden_layer_info'][str(i)]["kernel_regularizer"],
                            bias_regularizer=params_tf['hidden_layer_info'][str(i)]["bias_regularizer"],
                            activity_regularizer=params_tf['hidden_layer_info'][str(i)]["activity_regularizer"],
                            kernel_constraint=params_tf['hidden_layer_info'][str(i)]["kernel_constraint"],
                            bias_constraint=params_tf['hidden_layer_info'][str(i)]["bias_constraint"]))
                            try:
                                if params_tf['hidden_layer_info'][str(i)]["batch_normalization"]=="True":
                                    model.add(tf.keras.layers.BatchNormalization())
                            except:
                                print("BATCH_NORM_FAILED ##########################")
                                pass
                            first_layer_flag=False
                        else:
                            model.add(tf.keras.layers.Dense(params_tf['hidden_layer_info'][str(i)]["units"],
                            activation=params_tf['hidden_layer_info'][str(i)]["activation"],
                            use_bias=params_tf['hidden_layer_info'][str(i)]["use_bias"],
                            kernel_initializer=params_tf['hidden_layer_info'][str(i)]["kernel_initializer"],
                            bias_initializer=params_tf['hidden_layer_info'][str(i)]["bias_initializer"],
                            kernel_regularizer=params_tf['hidden_layer_info'][str(i)]["kernel_regularizer"],
                            bias_regularizer=params_tf['hidden_layer_info'][str(i)]["bias_regularizer"],
                            activity_regularizer=params_tf['hidden_layer_info'][str(i)]["activity_regularizer"],
                            kernel_constraint=params_tf['hidden_layer_info'][str(i)]["kernel_constraint"],
                            bias_constraint=params_tf['hidden_layer_info'][str(i)]["bias_constraint"]))
                            try:
                                if params_tf['hidden_layer_info'][str(i)]["batch_normalization"]=="True":
                                    model.add(tf.keras.layers.BatchNormalization())
                            except:
                                print("BATCH_NORM_FAILED ##########################")
                                pass

                    elif params_tf['hidden_layer_info'][str(i)]["layer"]=="Dropout":
                        model.add(tf.keras.layers.Dropout(float(params_tf['hidden_layer_info'][str(i)]["rate"])))

                    elif params_tf['hidden_layer_info'][str(i)]["layer"]=="Lambda":
                        if params_tf['hidden_layer_info'][str(i)]["lambda"]=="Addition":
                            model.add(tf.keras.layers.Lambda(lambda x:x+int(params_tf['hidden_layer_info'][str(i)]["units"])))
                        if params_tf['hidden_layer_info'][str(i)]["lambda"]=="Multiplication":
                            model.add(tf.keras.layers.Lambda(lambda x:x*int(params_tf['hidden_layer_info'][str(i)]["units"])))
                        if params_tf['hidden_layer_info'][str(i)]["lambda"]=="Subtraction":
                            model.add(tf.keras.layers.Lambda(lambda x:x-int(params_tf['hidden_layer_info'][str(i)]["units"])))
                        if params_tf['hidden_layer_info'][str(i)]["lambda"]=="Division":
                            model.add(tf.keras.layers.Lambda(lambda x:old_div(x,int(params_tf['hidden_layer_info'][str(i)]["units"]))))

                model.compile(optimizer=algoParams["optimizer"],loss = algoParams["loss"], metrics=[algoParams['metrics']])


                model.fit(x_train,y_train,epochs=algoParams["number_of_epochs"],verbose=1,batch_size=algoParams["batch_size"])

                bestEstimator = model
            print(model.summary())
            trainingTime = time.time()-st
            y_score = bestEstimator.predict(x_test)
            y_score= list(y_score.flatten())
            try:
                y_prob = bestEstimator.predict_proba(x_test)
            except:
                y_prob = [0]*len(y_score)
            featureImportance={}

            objs = {"trained_model":bestEstimator,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":featureImportance,"featureList":list(x_train.columns),"labelMapping":{}}
            #featureImportance = objs["trained_model"].feature_importances_
            #featuresArray = [(col_name, featureImportance[idx]) for idx, col_name in enumerate(x_train.columns)]
            featuresArray = []
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName+".h5")
                objs["trained_model"].save("/".join(modelFilepathArr))
                #joblib.dump(objs["trained_model"],"/".join(modelFilepathArr))
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
            print(mapeStatsArr)
            print(mapeCountArr)
            predictionColSummary = transformed["prediction"].describe().to_dict()
            quantileBins = [predictionColSummary["min"],predictionColSummary["25%"],predictionColSummary["50%"],predictionColSummary["75%"],predictionColSummary["max"]]
            print(quantileBins)
            quantileBins = sorted(list(set(quantileBins)))
            transformed["quantileBinId"] = pd.cut(transformed["prediction"],quantileBins)
            quantileDf = transformed.groupby("quantileBinId").agg({"prediction":[np.sum,np.mean,np.size]}).reset_index()
            quantileDf.columns = ["prediction","sum","mean","count"]
            print(quantileDf)
            quantileArr = list(quantileDf.T.to_dict().items())
            quantileSummaryArr = [(obj[0],{"splitRange":(obj[1]["prediction"].left,obj[1]["prediction"].right),"count":obj[1]["count"],"mean":obj[1]["mean"],"sum":obj[1]["sum"]}) for obj in quantileArr]
            print(quantileSummaryArr)
            runtime = round((time.time() - st_global),2)

            self._model_summary.set_model_type("regression")
            self._model_summary.set_algorithm_name("Neural Network (TensorFlow)")
            self._model_summary.set_algorithm_display_name("Neural Network (TensorFlow)")
            self._model_summary.set_slug(self._slug)
            self._model_summary.set_training_time(runtime)
            self._model_summary.set_training_time(trainingTime)
            self._model_summary.set_target_variable(result_column)
            self._model_summary.set_validation_method(validationDict["displayName"])
            self._model_summary.set_model_evaluation_metrics(metrics)
            self._model_summary.set_model_params(params_tf)
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


        if algoSetting.is_hyperparameter_tuning_enabled():
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
        modelmanagement_=params_tf
        modelmanagement_.update(algoParams)

        self._model_management=MLModelSummary()
        if algoSetting.is_hyperparameter_tuning_enabled():
            pass
        else:
            self._model_management.set_layer_info(data=modelmanagement_['hidden_layer_info'])
            self._model_management.set_loss_function(data=modelmanagement_['loss'])
            self._model_management.set_optimizer(data=modelmanagement_['optimizer'])
            self._model_management.set_batch_size(data=modelmanagement_['batch_size'])
            self._model_management.set_no_epochs(data=modelmanagement_['number_of_epochs'])
            self._model_management.set_model_evaluation_metrics(data=modelmanagement_['metrics'])
            self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
            self._model_management.set_training_status(data="completed")# training status
            self._model_management.set_no_of_independent_variables(data=x_train) #no of independent varables
            self._model_management.set_training_time(runtime) # run time
            self._model_management.set_rmse(metrics["RMSE"])
            self._model_management.set_algorithm_name("Neural Network (TensorFlow)")#algorithm name
            self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
            self._model_management.set_target_variable(result_column)#target column name
            self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M ')))#creation date
            self._model_management.set_datasetName(self._datasetName)
        modelManagementSummaryJson =[

                    ["Project Name",self._model_management.get_job_type()],
                    ["Algorithm",self._model_management.get_algorithm_name()],
                    ["Training Status",self._model_management.get_training_status()],
                    ["RMSE",self._model_management.get_rmse()],
                    ["RunTime",self._model_management.get_training_time()],
                    #["Owner",None],
                    ["Created On",self._model_management.get_creation_date()]

                    ]
        if algoSetting.is_hyperparameter_tuning_enabled():
            modelManagementModelSettingsJson =[]
        else:
            modelManagementModelSettingsJson =[

                        ["Training Dataset",self._model_management.get_datasetName()],
                        ["Target Column",self._model_management.get_target_variable()],
                        ["Number Of Independent Variables",self._model_management.get_no_of_independent_variables()],
                        ["Algorithm",self._model_management.get_algorithm_name()],
                        ["Model Validation",self._model_management.get_validation_method()],
                        ["batch_size",str(self._model_management.get_batch_size())],
                        ["Loss",self._model_management.get_loss_function()],
                        ["Optimizer",self._model_management.get_optimizer()],
                        ["Epochs",self._model_management.get_no_epochs()],
                        ["Metrics",self._model_management.get_model_evaluation_metrics()]

                        ]
            for i in range(len(list(modelmanagement_['hidden_layer_info'].keys()))):
                string=""
                key="layer No-"+str(i)+"-"+str(modelmanagement_["hidden_layer_info"][str(i)]["layer"]+"-")
                for j in modelmanagement_["hidden_layer_info"][str(i)]:
                    modelManagementModelSettingsJson.append([key+j+":",modelmanagement_["hidden_layer_info"][str(i)][j]])
        print(modelManagementModelSettingsJson)

        tfregCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]

        tfregPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards_regression(self._model_summary)]
        tfregOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
        tfregDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
        TFReg_Overview_Node = NarrativesTree()
        TFReg_Overview_Node.set_name("Overview")
        TFReg_Performance_Node = NarrativesTree()
        TFReg_Performance_Node.set_name("Performance")
        TFReg_Deployment_Node = NarrativesTree()
        TFReg_Deployment_Node.set_name("Deployment")
        for card in tfregOverviewCards:
            TFReg_Overview_Node.add_a_card(card)
        for card in tfregPerformanceCards:
            TFReg_Performance_Node.add_a_card(card)
        for card in tfregDeploymentCards:
            TFReg_Deployment_Node.add_a_card(card)
        for card in tfregCards:
            self._prediction_narrative.add_a_card(card)
        self._result_setter.set_model_summary({"Neural Network (TensorFlow)":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_tfreg_regression_model_summart(modelSummaryJson)
        self._result_setter.set_tfreg_cards(tfregCards)
        self._result_setter.set_tfreg_nodes([TFReg_Overview_Node,TFReg_Performance_Node,TFReg_Deployment_Node])
        self._result_setter.set_tfreg_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","Success":"True"})
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")



    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Neural Network (TensorFlow) Regression Scripts",
                "weight":2
                },
            "predictionStart":{
                "summary":"Neural Network (TensorFlow) Regression Model Prediction Started",
                "weight":2
                },
            "predictionFinished":{
                "summary":"Neural Network (TensorFlow) Regression Model Prediction Finished",
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
            pass

        elif self._mlEnv == "sklearn":
            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"predictionStart","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
            score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
            trained_model_path = "file://" + self._dataframe_context.get_model_path()
            trained_model_path += "/"+self._dataframe_context.get_model_for_scoring()+".h5"
            print("trained_model_path",trained_model_path)
            print("score_data_path",score_data_path)
            if trained_model_path.startswith("file"):
                trained_model_path = trained_model_path[7:]
            #trained_model = joblib.load(trained_model_path)
            trained_model = tf.keras.models.load_model(trained_model_path)
            model_columns = self._dataframe_context.get_model_features()
            print("model_columns",model_columns)

            df = self._data_frame.toPandas()
            # pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.create_dummy_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.fill_missing_columns(pandas_df,model_columns,result_column)

            if uid_col:
                pandas_df = pandas_df[[x for x in pandas_df.columns if x != uid_col]]
            y_score = trained_model.predict(pandas_df)
            y_score= list(y_score.flatten())
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
            pandas_scored_df = df[list(set(columns_to_keep+[result_column]))]
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
