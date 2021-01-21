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

import humanize
import numpy as np
import pandas as pd
from datetime import datetime

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.utils.data as torch_data_utils

try:
    import pickle as pickle
except:
    import pickle

try:
    from sklearn.externals import joblib
except:
    import joblib
from sklearn import metrics
from sklearn2pmml import sklearn2pmml
from sklearn2pmml import PMMLPipeline
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import ParameterGrid

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score,explained_variance_score
from math import sqrt

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.narratives import utils as NarrativesUtils
from bi.common import MLModelSummary, NormalCard, KpiData, C3ChartData, HtmlData, SklearnGridSearchResult, SkleanrKFoldResult
from bi.algorithms import utils as MLUtils
from bi.algorithms import nnpt_utils as PYTORCHUTILS
from bi.algorithms.pyTorch import PyTorchNetwork
from bi.common import DataFrameHelper
from bi.common import C3ChartData,TableData, NormalCard
from bi.common import NormalChartData,ChartJson
from bi.algorithms import DecisionTrees
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative
from bi.scripts.measureAnalysis.descr_stats import DescriptiveStatsScript
from bi.scripts.measureAnalysis.two_way_anova import TwoWayAnovaScript
from bi.scripts.measureAnalysis.decision_tree_regression import DecisionTreeRegressionScript
from bi.common import NarrativesTree
from bi.settings import setting as GLOBALSETTINGS
from bi.algorithms import GainLiftKS


class NNPTRegressionScript(object):
    def __init__(self, data_frame, df_helper, df_context, spark, prediction_narrative, result_setter, meta_parser, mlEnvironment="sklearn"):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (PyTorch)"]
        self._analysisName = self._slug
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
                "summary":"Initialized The Neural Network (PyTorch)  Scripts",
                "weight":1
                },
            "training":{
                "summary":"Neural Network (PyTorch)  Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Neural Network (PyTorch)  Training Finished",
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
        print("CATEGORICAL COLS - ", categorical_columns)
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

            x_train, x_test, y_train, y_test = self._dataframe_helper.get_train_test_data()
            x_train = MLUtils.create_dummy_columns(x_train,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.create_dummy_columns(x_test,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.fill_missing_columns(x_test,x_train.columns,result_column)

            print("="*150)
            print("X-Train Shape - ", x_train.shape)
            print("Y-Train Shape - ", y_train.shape)
            print("X-Test Shape - ", x_test.shape)
            print("Y-Test Shape - ", y_test.shape)
            print("~"*50)
            print("X-Train dtype - ", type(x_train))
            print("Y-Train dtype - ", type(y_train))
            print("X-Test dtype - ", type(x_test))
            print("Y-Test dtype - ", type(y_test))
            print("~"*50)

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            st = time.time()

            self._result_setter.set_hyper_parameter_results(self._slug, None)
            evaluationMetricDict = algoSetting.get_evaluvation_metric(Type="REGRESSION")
            evaluationMetricDict = {"name":GLOBALSETTINGS.REGRESSION_MODEL_EVALUATION_METRIC}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]

            x_train_tensored, y_train_tensored, x_test_tensored, y_test_tensored = PYTORCHUTILS.get_tensored_data(x_train, y_train, x_test, y_test)
            trainset = torch_data_utils.TensorDataset(x_train_tensored, y_train_tensored)
            testset = torch_data_utils.TensorDataset(x_test_tensored, y_test_tensored)

            nnptr_params = algoSetting.get_nnptr_params_dict()[0]
            layers_for_network = PYTORCHUTILS.get_layers_for_network_module(nnptr_params, task_type = "REGRESSION",first_layer_units = x_train.shape[1])

            # Use GPU if available
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            network = PyTorchNetwork(layers_for_network).to(device)
            network.eval()

            other_params_dict = PYTORCHUTILS.get_other_pytorch_params(nnptr_params, task_type = "REGRESSION", network_params = network.parameters())

            print("~"*50)
            print("NNPTR-PARAMS - ", nnptr_params)
            print("~"*50)
            print("OTHER-PARAMS-DICT - ", other_params_dict)
            print("~"*50)
            print("NEURAL-NETWORK - ", network)
            print("~"*50)

            criterion = other_params_dict["loss_criterion"]
            n_epochs = other_params_dict["number_of_epochs"]
            batch_size = other_params_dict["batch_size"]
            optimizer = other_params_dict["optimizer"]

            dataloader_params = {
            "batch_size": batch_size,
            "shuffle": True
            # "num_workers":
            }

            train_loader = torch_data_utils.DataLoader(trainset, **dataloader_params)
            test_loader = torch_data_utils.DataLoader(testset, **dataloader_params)

            '''
            Training the network;
            Batchnormalization(num_features) should be equal to units_op for that layer in training config;
            else --> RuntimeError('running_mean should contain 100 elements not 200',)
            '''

            for epoch in range(n_epochs):
                batchwise_losses = []
                average_loss = 0.0

                for i, (inputs, labels) in enumerate(train_loader):
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # Zero the parameter gradients
                    optimizer.zero_grad()

                    # Forward + backward + optimize
                    outputs = network(inputs.float())
                    loss = criterion(outputs, labels.float())
                    loss.backward()
                    optimizer.step()

                    average_loss += loss.item()
                    batchwise_losses.append(loss.item())

                average_loss_per_epoch = old_div(average_loss,(i + 1))
                print("+"*80)
                print("EPOCH - ", epoch)
                print("BATCHWISE_LOSSES shape - ", len(batchwise_losses))
                print("AVERAGE LOSS PER EPOCH - ", average_loss_per_epoch)
                print("+"*80)

            trainingTime = time.time()-st
            bestEstimator = network

            outputs_x_test_tensored = network(x_test_tensored.float())
            y_score_mid = outputs_x_test_tensored.tolist()
            y_score = [x[0] for x in y_score_mid]
            print("Y-SCORE - ", y_score)
            print("Y-SCORE length - ", len(y_score))
            y_prob = None

            featureImportance={}
            objs = {"trained_model":bestEstimator,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":featureImportance,"featureList":list(x_train.columns),"labelMapping":{}}
            #featureImportance = objs["trained_model"].feature_importances_
            #featuresArray = [(col_name, featureImportance[idx]) for idx, col_name in enumerate(x_train.columns)]
            featuresArray = []
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName+".pt")
                torch.save(objs["trained_model"], "/".join(modelFilepathArr))
                #joblib.dump(objs["trained_model"],"/".join(modelFilepathArr))
                runtime = round((time.time() - st),2)
            else:
                runtime = round((time.time() - hyper_st),2)

            try:
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

            metrics = {}
            metrics["r2"] = r2_score(y_test, y_score)
            metrics["neg_mean_squared_error"] = mean_squared_error(y_test, y_score)
            metrics["neg_mean_absolute_error"] = mean_absolute_error(y_test, y_score)
            metrics["RMSE"] = sqrt(metrics["neg_mean_squared_error"])
            metrics["explained_variance_score"]=explained_variance_score(y_test, y_score)
            transformed = pd.DataFrame({"prediction":y_score,result_column:y_test})
            print("TRANSFORMED PREDICTION TYPE - ", type(transformed["prediction"]))
            print(transformed["prediction"])
            print("TRANSFORMED RESULT COL TYPE - ", type(transformed[result_column]))
            print(transformed[result_column])
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
            self._model_summary.set_algorithm_name("Neural Network (PyTorch)")
            self._model_summary.set_algorithm_display_name("Neural Network (PyTorch)")
            self._model_summary.set_slug(self._slug)
            self._model_summary.set_training_time(runtime)
            self._model_summary.set_training_time(trainingTime)
            self._model_summary.set_target_variable(result_column)
            self._model_summary.set_validation_method(validationDict["displayName"])
            self._model_summary.set_model_evaluation_metrics(metrics)
            self._model_summary.set_model_params(nnptr_params)
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
        modelmanagement_=nnptr_params

        self._model_management=MLModelSummary()
        if algoSetting.is_hyperparameter_tuning_enabled():
            pass
        else:
            self._model_management.set_layer_info(data=modelmanagement_['hidden_layer_info'])
            self._model_management.set_loss_function(data=modelmanagement_['loss'])
            self._model_management.set_optimizer(data=modelmanagement_['optimizer'])
            self._model_management.set_batch_size(data=modelmanagement_['batch_size'])
            self._model_management.set_no_epochs(data=modelmanagement_['number_of_epochs'])
            # self._model_management.set_model_evaluation_metrics(data=modelmanagement_['metrics'])
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
            for i in modelmanagement_["hidden_layer_info"]:
                string=""
                key=str(modelmanagement_["hidden_layer_info"][i]["layer"])+" "+str(i)+":"
                for j in modelmanagement_["hidden_layer_info"][i]:
                    string=string+str(j)+":"+str(modelmanagement_["hidden_layer_info"][i][j])+",   "
                modelManagementModelSettingsJson.append([key,string] )
        print(modelManagementModelSettingsJson)

        nnptrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        nnptrPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards_regression(self._model_summary)]
        nnptrOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
        nnptrDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
        nnptr_Overview_Node = NarrativesTree()
        nnptr_Overview_Node.set_name("Overview")
        nnptr_Performance_Node = NarrativesTree()
        nnptr_Performance_Node.set_name("Performance")
        nnptr_Deployment_Node = NarrativesTree()
        nnptr_Deployment_Node.set_name("Deployment")
        for card in nnptrOverviewCards:
            nnptr_Overview_Node.add_a_card(card)
        for card in nnptrPerformanceCards:
            nnptr_Performance_Node.add_a_card(card)
        for card in nnptrDeploymentCards:
            nnptr_Deployment_Node.add_a_card(card)
        for card in nnptrCards:
            self._prediction_narrative.add_a_card(card)
        self._result_setter.set_model_summary({"Neural Network (PyTorch)":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_nnptr_regression_model_summary(modelSummaryJson)
        self._result_setter.set_nnptr_cards(nnptrCards)
        self._result_setter.set_nnptr_nodes([nnptr_Overview_Node, nnptr_Performance_Node, nnptr_Deployment_Node])
        self._result_setter.set_nnptr_fail_card({"Algorithm_Name":"Neural Network (PyTorch)","Success":"True"})
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")





    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Neural Network (PyTorch)  Scripts",
                "weight":2
                },
            "predictionStart":{
                "summary":"Neural Network (PyTorch)  Prediction Started",
                "weight":2
                },
            "predictionFinished":{
                "summary":"Neural Network (PyTorch)  Prediction Finished",
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
            trained_model_path += "/"+self._dataframe_context.get_model_for_scoring()+".pt"
            print("trained_model_path",trained_model_path)
            print("score_data_path",score_data_path)
            if trained_model_path.startswith("file"):
                trained_model_path = trained_model_path[7:]
            #trained_model = joblib.load(trained_model_path)
            trained_model = torch.load(trained_model_path, map_location=torch.device('cpu'))
            model_columns = self._dataframe_context.get_model_features()
            print("model_columns",model_columns)
            try:
                df = self._data_frame.toPandas()
            except:
                df = self._data_frame
            # pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.create_dummy_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.fill_missing_columns(pandas_df,model_columns,result_column)

            if uid_col:
                pandas_df = pandas_df[[x for x in pandas_df.columns if x != uid_col]]

            test_df = np.stack([pandas_df[col].values for col in pandas_df.columns], 1)
            tensored_test_df = torch.tensor(test_df, dtype=torch.float)

            outputs_test_df_tensored = trained_model(tensored_test_df.float())

            y_score_mid = outputs_test_df_tensored.tolist()
            y_score = [x[0] for x in y_score_mid]

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
