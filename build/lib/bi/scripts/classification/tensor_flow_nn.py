from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import json
import time
import re
import humanize
import numpy as np
import pandas as pd
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

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
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import ParameterGrid


from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.narratives import utils as NarrativesUtils
from bi.common import MLModelSummary,NormalCard,KpiData,C3ChartData,HtmlData,SklearnGridSearchResult,SkleanrKFoldResult
from bi.algorithms import LogisticRegression
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.common import C3ChartData,TableData, NormalCard
from bi.common import NormalChartData,ChartJson
from bi.algorithms import DecisionTrees
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative
from bi.common import NarrativesTree
from bi.settings import setting as GLOBALSETTINGS
from bi.algorithms import GainLiftKS


class TensorFlowScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser,mlEnvironment="sklearn"):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._pandas_flag = df_context._pandas_flag
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{}}
        self._score_summary = {}
        self._column_separator = "|~|"
        self._model_slug_map = GLOBALSETTINGS.MODEL_SLUG_MAPPING
        self._slug = self._model_slug_map["Neural Network (TensorFlow)"]
        self._targetLevel = self._dataframe_context.get_target_level_for_model()
        self._datasetName = CommonUtils.get_dataset_name(self._dataframe_context.CSV_FILE)
        try:
            if not self._pandas_flag:
                self._data_frame = self._data_frame.toPandas()
                self._data_frame.columns = [re.sub("[[]|[]]|[<]","", col) for col in self._data_frame.columns.values]
                self._dataframe_helper.set_train_test_data(self._data_frame)
        except:
            pass
        self._completionStatus = self._dataframe_context.get_completion_status()
        print(self._completionStatus,"initial completion status")
        self._analysisName = self._slug
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._mlEnv = mlEnvironment

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Neural Network (TensorFlow) Scripts",
                "weight":1
                },
            "training":{
                "summary":"Neural Network (TensorFlow) Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Neural Network (TensorFlow) Model Training Finished",
                "weight":1
                },
            }

    def Train(self):
        st_global = time.time()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"initialization","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = [x for x in algosToRun if x.get_algorithm_slug()==self._slug][0]
        categorical_columns = self._dataframe_helper.get_string_columns()
        uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(uid_col):
            categorical_columns = list(set(categorical_columns) - {uid_col})
        allDateCols = self._dataframe_context.get_date_columns()
        categorical_columns = list(set(categorical_columns)-set(allDateCols))
        print(categorical_columns)
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()

        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()
        print("model_path",model_path)
        pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        if  self._mlEnv == "spark":
            pass
        elif self._mlEnv == "sklearn":
            model_filepath = model_path+"/"+self._slug+"/model.pkl"
            pmml_filepath = str(model_path)+"/"+str(self._slug)+"/traindeModel.pmml"

            x_train,x_test,y_train,y_test = self._dataframe_helper.get_train_test_data()
            x_train = MLUtils.create_dummy_columns(x_train,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.create_dummy_columns(x_test,[x for x in categorical_columns if x != result_column])
            x_test = MLUtils.fill_missing_columns(x_test,x_train.columns,result_column)

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

            st = time.time()
            levels = df[result_column].unique()

            labelEncoder = preprocessing.LabelEncoder()
            labelEncoder.fit(np.concatenate([y_train,y_test]))
            y_train = pd.Series(labelEncoder.transform(y_train))
            y_test = labelEncoder.transform(y_test)
            classes = labelEncoder.classes_
            transformed = labelEncoder.transform(classes)
            transformed_classes_list = list(transformed)
            labelMapping = dict(list(zip(transformed,classes)))
            inverseLabelMapping = dict(list(zip(classes,transformed)))
            posLabel = inverseLabelMapping[self._targetLevel]
            appType = self._dataframe_context.get_app_type()

            print("="*150)
            print("TRANSFORMED CLASSES - ", transformed_classes_list)
            print("LEVELS - ", levels)
            print("NUMBER OF LEVELS - ", len(levels))
            print("CLASSES - ", classes)
            print("LABEL MAPPING - ", labelMapping)
            print("INVERSE LABEL MAPPING - ", inverseLabelMapping)
            print("POSITIVE LABEL - ", posLabel)
            print("TARGET LEVEL - ", self._targetLevel)
            print("APP TYPE - ", appType)
            print("="*150)
            evaluationMetricDict = {"name":GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
            self._result_setter.set_hyper_parameter_results(self._slug,None)

            if self._dataframe_context.get_trainerMode() == "autoML":
                # automl_enable = True
                train_size = x_train.shape[0]
                if train_size < 10000:
                    units = '32'
                    if len(levels) > 2 and train_size >= 500:
                        units = '64'
                    rate = '0.1'
                elif train_size >= 10000 and train_size < 20000:
                    units = '32'
                    if len(levels) > 2:
                        units = '64'
                    rate = '0.2'
                elif train_size >= 20000 and train_size < 40000:
                    units = '64'
                    if len(levels) > 2:
                        units = '128'
                    rate = '0.3'
                elif train_size >= 60000:
                    units = '128'
                    if len(levels) > 2:
                        units = '256'
                    rate = '0.5'
                else:
                    rate = '0.5'
                    units = '256'
                params_tf = {
                              'hidden_layer_info':
                              {
                                '1': {
                                  'layerId': 2,
                                  'rate': rate,
                                  'layer': 'Dropout'
                                },
                                '3': {
                                  'layerId': 4,
                                  'rate': rate,
                                  'layer': 'Dropout'
                                },
                                '4': {
                                  'bias_constraint': None,
                                  'units': str(len(levels)),
                                  'use_bias': True,
                                  'layer': 'Dense',
                                  'bias_initializer': 'glorot_uniform',
                                  'layerId': 5,
                                  'activity_regularizer': None,
                                  'kernel_constraint': None,
                                  'activation': 'softmax',
                                  'kernel_initializer': 'glorot_uniform',
                                  'kernel_regularizer': None,
                                  'batch_normalization': 'True',
                                  'bias_regularizer': None
                                },
                                '0': {
                                  'bias_constraint': None,
                                  'units': units,
                                  'use_bias': True,
                                  'layer': 'Dense',
                                  'bias_initializer': 'glorot_uniform',
                                  'layerId': 1,
                                  'activity_regularizer': None,
                                  'kernel_constraint': None,
                                  'activation': 'relu',
                                  'kernel_initializer': 'glorot_uniform',
                                  'kernel_regularizer': None,
                                  'batch_normalization': 'True',
                                  'bias_regularizer': None
                                },
                                '2': {
                                  'bias_constraint': None,
                                  'units': int(int(units)/2),
                                  'use_bias': True,
                                  'layer': 'Dense',
                                  'bias_initializer': 'glorot_uniform',
                                  'layerId': 3,
                                  'activity_regularizer': None,
                                  'kernel_constraint': None,
                                  'activation': 'relu',
                                  'kernel_initializer': 'glorot_uniform',
                                  'kernel_regularizer': None,
                                  'batch_normalization': 'True',
                                  'bias_regularizer': None
                                }
                              }
                            }
                algoParams = {
                                  'layer': 'Dense',
                                  'loss': 'sparse_categorical_crossentropy',
                                  'optimizer': 'Adam',
                                  'batch_size': min(int(train_size/100), 300),
                                  'number_of_epochs': 100,
                                  'metrics': 'sparse_categorical_crossentropy'
                                  }

                if len(levels) == 2:
                    params_tf['hidden_layer_info']['4']['activation'] = 'sigmoid'
                    algoParams['loss'] = 'binary_crossentropy'
                    algoParams['metrics'] = 'binary_crossentropy'
                elif len(levels) > 2:
                    pass

                if train_size <= 500:
                    algoParams['batch_size'] = int(train_size/10)
                elif len(levels) == 2 and train_size > 500 and train_size < 2000:
                    algoParams['batch_size'] = int(train_size/50)
                elif len(levels) > 2 and train_size > 500 and train_size < 30000:
                    batch_size = list(np.random.uniform(low = 100, high = 300, size = (29500,)))
                    batch_size.sort()
                    algoParams['batch_size'] = int(batch_size[train_size - 500])
            else:
                params_tf = algoSetting.get_tf_params_dict()
                algoParams = algoSetting.get_params_dict()
                algoParams = {k:v for k,v in list(algoParams.items())}

            print('\n\nparams_tf:\n\n', params_tf)
            print('\n\nalgoParams:\n\n', algoParams)
            print('\n\n')
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

            try:
                model.fit(x_train,y_train,epochs=algoParams["number_of_epochs"],verbose=1,batch_size=algoParams["batch_size"])
            except:
                y_train=tf.keras.utils.to_categorical(y_train)
                model.fit(x_train,y_train,epochs=algoParams["number_of_epochs"],verbose=1,batch_size=algoParams["batch_size"])


            bestEstimator=model
            trainingTime = time.time()-st
            y_score = bestEstimator.predict_classes(x_test)
            try:
                y_prob = bestEstimator.predict(x_test)
            except:
                y_prob = [0]*len(y_score)

            accuracy = metrics.accuracy_score(y_test,y_score)
            if len(levels) <= 2:
                precision = metrics.precision_score(y_test,y_score,pos_label=posLabel,average="binary")
                recall = metrics.recall_score(y_test,y_score,pos_label=posLabel,average="binary")
                roc_auc = metrics.roc_auc_score(y_test,y_score)
                log_loss = metrics.log_loss(y_test,y_prob)
                F1_score = metrics.f1_score(y_test,y_score,pos_label=posLabel,average="binary")
            elif len(levels) > 2:
                precision = metrics.precision_score(y_test,y_score,pos_label=posLabel,average="macro")
                recall = metrics.recall_score(y_test,y_score,pos_label=posLabel,average="macro")
                log_loss = metrics.log_loss(y_test,y_prob)
                F1_score = metrics.f1_score(y_test,y_score,pos_label=posLabel,average="macro")
                # auc = metrics.roc_auc_score(y_test,y_score,average="weighted")
                roc_auc = None
            print((precision,recall,roc_auc,log_loss,F1_score))
            #import sys
            #sys.exit()
            y_prob_for_eval = []
            for i in range(len(y_prob)):
                if len(y_prob[i]) == 1:
                    if y_score[i] == posLabel:
                        y_prob_for_eval.append(float(y_prob[i][1]))
                    else:
                        y_prob_for_eval.append(float(1 - y_prob[i][1]))
                else:
                    y_prob_for_eval.append(float(y_prob[i][int(posLabel)]))


            '''ROC CURVE IMPLEMENTATION'''
            if len(levels) <= 2:
                positive_label_probs = []
                for val in y_prob:
                    positive_label_probs.append(val[posLabel])

                roc_data_dict = {
                                    "y_score" : y_score,
                                    "y_test" : y_test,
                                    "positive_label_probs" : positive_label_probs,
                                    "y_prob" : y_prob,
                                    "positive_label" : posLabel
                                }
                roc_dataframe = pd.DataFrame(
                                                {
                                                    "y_score" : y_score,
                                                    "y_test" : y_test,
                                                    "positive_label_probs" : positive_label_probs
                                                }
                                            )
                #roc_dataframe.to_csv("binary_roc_data.csv")
                fpr, tpr, thresholds = roc_curve(y_test, positive_label_probs, pos_label = posLabel)
                roc_df = pd.DataFrame({"FPR" : fpr, "TPR" : tpr, "thresholds" : thresholds})
                roc_df["tpr-fpr"] = roc_df["TPR"] - roc_df["FPR"]

                optimal_index = np.argmax(np.array(roc_df["tpr-fpr"]))
                fpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "FPR"]
                tpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "TPR"]

                rounded_roc_df = roc_df.round({'FPR': 2, 'TPR': 4})

                unique_fpr = rounded_roc_df["FPR"].unique()

                final_roc_df = rounded_roc_df.groupby("FPR", as_index = False)[["TPR"]].mean()
                endgame_roc_df = final_roc_df.round({'FPR' : 2, 'TPR' : 3})

            elif len(levels) > 2:
                positive_label_probs = []
                for val in y_prob:
                    positive_label_probs.append(val[posLabel])

                y_test_roc_multi = []
                for val in y_test:
                    if val != posLabel:
                        val = posLabel + 1
                        y_test_roc_multi.append(val)
                    else:
                        y_test_roc_multi.append(val)

                y_score_roc_multi = []
                for val in y_score:
                    if val != posLabel:
                        val = posLabel + 1
                        y_score_roc_multi.append(val)
                    else:
                        y_score_roc_multi.append(val)

                roc_auc = metrics.roc_auc_score(y_test_roc_multi, y_score_roc_multi)

                fpr, tpr, thresholds = roc_curve(y_test_roc_multi, positive_label_probs, pos_label = posLabel)
                roc_df = pd.DataFrame({"FPR" : fpr, "TPR" : tpr, "thresholds" : thresholds})
                roc_df["tpr-fpr"] = roc_df["TPR"] - roc_df["FPR"]

                optimal_index = np.argmax(np.array(roc_df["tpr-fpr"]))
                fpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "FPR"]
                tpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "TPR"]

                rounded_roc_df = roc_df.round({'FPR': 2, 'TPR': 4})
                unique_fpr = rounded_roc_df["FPR"].unique()
                final_roc_df = rounded_roc_df.groupby("FPR", as_index = False)[["TPR"]].mean()
                endgame_roc_df = final_roc_df.round({'FPR' : 2, 'TPR' : 3})

            temp_df = pd.DataFrame({'y_test': y_test,'y_score': y_score,'y_prob_for_eval': y_prob_for_eval})
            if self._pandas_flag:
                gain_lift_ks_obj = GainLiftKS(temp_df, 'y_prob_for_eval', 'y_score', 'y_test', posLabel, self._spark)
                gain_lift_KS_dataframe = gain_lift_ks_obj.Rank_Ordering()
            else:
                pys_df = self._spark.createDataFrame(temp_df)
                gain_lift_ks_obj = GainLiftKS(pys_df, 'y_prob_for_eval', 'y_score', 'y_test', posLabel, self._spark)
                gain_lift_KS_dataframe = gain_lift_ks_obj.Run().toPandas()

            y_score = labelEncoder.inverse_transform(y_score)
            y_test = labelEncoder.inverse_transform(y_test)

            feature_importance = {}

            objs = {"trained_model":bestEstimator,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":feature_importance,"featureList":list(x_train.columns),"labelMapping":labelMapping}
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
                print(model_filepath)

                modelFilepathArr = model_filepath.split("/")[:-1]
                modelFilepathArr.append(modelName+".h5")
                print(modelFilepathArr,"/".join(modelFilepathArr))

                #joblib.dump(objs["trained_model"],"/".join(modelFilepathArr))
                objs["trained_model"].save("/".join(modelFilepathArr))
                runtime = round((time.time() - st),2)
            else:
                runtime = round((time.time() - hyper_st),2)

            try:
                if automl_enable:
                    modelPmmlPipeline = PMMLPipeline([
                        ("pretrained-estimator", objs["trained_model"].bestEstimator)
                    ])
                else:
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

            cat_cols = list(set(categorical_columns) - {result_column})
            overall_precision_recall = MLUtils.calculate_overall_precision_recall(objs["actual"],objs["predicted"],targetLevel=self._targetLevel)
            self._model_summary = MLModelSummary()
            self._model_summary.set_algorithm_name("Neural Network (TensorFlow)")
            self._model_summary.set_algorithm_display_name("Neural Network (TensorFlow)")
            self._model_summary.set_slug(self._slug)
            self._model_summary.set_training_time(runtime)
            self._model_summary.set_confusion_matrix(MLUtils.calculate_confusion_matrix(objs["actual"],objs["predicted"]))
            self._model_summary.set_feature_importance(objs["feature_importance"])
            self._model_summary.set_feature_list(objs["featureList"])
            self._model_summary.set_model_accuracy(round(metrics.accuracy_score(objs["actual"], objs["predicted"]),2))
            self._model_summary.set_training_time(round((time.time() - st),2))
            self._model_summary.set_precision_recall_stats(overall_precision_recall["classwise_stats"])
            self._model_summary.set_model_precision(overall_precision_recall["precision"])
            self._model_summary.set_model_recall(overall_precision_recall["recall"])
            self._model_summary.set_model_F1_score(F1_score)
            self._model_summary.set_model_log_loss(log_loss)
            self._model_summary.set_target_variable(result_column)
            self._model_summary.set_prediction_split(overall_precision_recall["prediction_split"])
            self._model_summary.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")
            self._model_summary.set_level_map_dict(objs["labelMapping"])
            self._model_summary.set_gain_lift_KS_data(gain_lift_KS_dataframe)
            self._model_summary.set_AUC_score(roc_auc)
            # self._model_summary.set_model_features(list(set(x_train.columns)-set([result_column])))
            self._model_summary.set_model_features([col for col in x_train.columns if col != result_column])
            self._model_summary.set_level_counts(self._metaParser.get_unique_level_dict(list(set(categorical_columns))))
            self._model_summary.set_target_level(self._targetLevel)
            # self._model_summary["trained_model_features"] = self._column_separator.join(list(x_train.columns)+[result_column])
            if not algoSetting.is_hyperparameter_tuning_enabled():
                modelDropDownObj = {
                            "name":self._model_summary.get_algorithm_name(),
                            "evaluationMetricValue": locals()[evaluationMetricDict["name"]], # self._model_summary.get_model_accuracy(),
                            "evaluationMetricName": evaluationMetricDict["name"],
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
                            "evaluationMetricValue": locals()[evaluationMetricDict["name"]], # self._model_summary.get_model_accuracy(),
                            "evaluationMetricName": evaluationMetricDict["name"],
                            "slug":self._model_summary.get_slug(),
                            "Model Id":resultArray[0]["Model Id"]
                            }
                modelSummaryJson = {
                    "dropdown":modelDropDownObj,
                    "levelcount":self._model_summary.get_level_counts(),
                    "modelFeatureList":self._model_summary.get_feature_list(),
                    "levelMapping":self._model_summary.get_level_map_dict(),
                    "slug":self._model_summary.get_slug(),
                    "name":self._model_summary.get_algorithm_name()
                }

            self._model_management = MLModelSummary()
            modelmanagement_=params_tf
            modelmanagement_.update(algoParams)
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
                self._model_management.set_target_level(self._targetLevel) # target column value
                self._model_management.set_training_time(runtime) # run time
                self._model_management.set_model_accuracy(round(metrics.accuracy_score(objs["actual"], objs["predicted"]),2))#accuracy
                self._model_management.set_algorithm_name("Neural Network (TensorFlow)")#algorithm name
                self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
                self._model_management.set_target_variable(result_column)#target column name
                self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M ')))#creation date
                self._model_management.set_datasetName(self._datasetName)


            modelManagementSummaryJson =[

                        ["Project Name",self._model_management.get_job_type()],
                        ["Algorithm",self._model_management.get_algorithm_name()],
                        ["Training Status",self._model_management.get_training_status()],
                        ["Accuracy",str(self._model_management.get_model_accuracy())],
                        ["RunTime",str(self._model_management.get_training_time())],
                        #["Owner",None],
                        ["Created On",str(self._model_management.get_creation_date())]

                        ]

            modelManagementModelSettingsJson =[

                        ["Training Dataset",self._model_management.get_datasetName()],
                        ["Target Column",self._model_management.get_target_variable()],
                        ["Target Column Value",self._model_management.get_target_level()],
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



            tfOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
            tfPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards(self._model_summary, endgame_roc_df)]
            tfDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
            tfCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
            TF_Overview_Node = NarrativesTree()
            TF_Overview_Node.set_name("Overview")
            TF_Performance_Node = NarrativesTree()
            TF_Performance_Node.set_name("Performance")
            TF_Deployment_Node = NarrativesTree()
            TF_Deployment_Node.set_name("Deployment")
            for card in tfOverviewCards:
                TF_Overview_Node.add_a_card(card)
            for card in tfPerformanceCards:
                TF_Performance_Node.add_a_card(card)
            for card in tfDeploymentCards:
                TF_Deployment_Node.add_a_card(card)
            for card in tfCards:
                self._prediction_narrative.add_a_card(card)

            self._result_setter.set_model_summary({"Neural Network (TensorFlow)":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
            self._result_setter.set_tf_model_summary(modelSummaryJson)
            self._result_setter.set_tf_cards(tfCards)
            self._result_setter.set_tf_nodes([TF_Overview_Node,TF_Performance_Node,TF_Deployment_Node])
            self._result_setter.set_tf_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","success":"True"})

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")




    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Neural Network (TensorFlow) Scripts",
                "weight":2
                },
            "prediction":{
                "summary":"Neural Network (TensorFlow) Model Prediction Finished",
                "weight":2
                },
            "frequency":{
                "summary":"Descriptive Analysis Finished",
                "weight":2
                },
            "chisquare":{
                "summary":"Chi Square Analysis Finished",
                "weight":4
                },
            "completion":{
                "summary":"All Analysis Finished",
                "weight":4
                },
            }

        self._completionStatus += old_div(self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["initialization"]["weight"],10)
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        cat_cols = self._dataframe_helper.get_string_columns()
        # level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,cat_cols,self._dataframe_context.get_column_separator(),output_type="dict")
        # if level_counts_train != {}:
        #     for key in level_counts_train:
        #         if key in level_counts_score:
        #             if level_counts_train[key] != level_counts_score[key]:
        #                 dataSanity = False
        #         else:
        #             dataSanity = False

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

            score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
            if score_data_path.startswith("file"):
                score_data_path = score_data_path[7:]
            trained_model_path = self._dataframe_context.get_model_path()
            trained_model_path += "/"+self._dataframe_context.get_model_for_scoring()+".h5"

            if trained_model_path.startswith("file"):
                trained_model_path = trained_model_path[7:]
            score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"
            if score_summary_path.startswith("file"):
                score_summary_path = score_summary_path[7:]
            model_columns = self._dataframe_context.get_model_features()
            #trained_model = joblib.load(trained_model_path)
            trained_model = tf.keras.models.load_model(trained_model_path)
            try:
                df = self._data_frame.toPandas()
            except:
                df = self._data_frame.copy()
            # pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.create_dummy_columns(df,[x for x in categorical_columns if x != result_column])
            pandas_df = MLUtils.fill_missing_columns(pandas_df,model_columns,result_column)
            if uid_col:
                pandas_df = pandas_df[[x for x in pandas_df.columns if x != uid_col]]
            y_score = trained_model.predict_classes(pandas_df)
            y_prob = trained_model.predict(pandas_df)
            y_prob = MLUtils.calculate_predicted_probability(y_prob)
            y_prob=list([round(x,2) for x in y_prob])
            score = {"predicted_class":y_score,"predicted_probability":y_prob}

        df["predicted_class"] = score["predicted_class"]
        labelMappingDict = self._dataframe_context.get_label_map()
        df["predicted_class"] = df["predicted_class"].apply(lambda x:labelMappingDict[x] if x != None else "NA")
        df["predicted_probability"] = score["predicted_probability"]
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(df)
        self._score_summary["result_column"] = result_column
        if result_column in df.columns:
            df.drop(result_column, axis=1, inplace=True)
        df = df.rename(index=str, columns={"predicted_class": result_column})
        df.to_csv(score_data_path,header=True,index=False)
        uidCol = self._dataframe_context.get_uid_column()
        if uidCol == None:
            uidCols = self._metaParser.get_suggested_uid_columns()
            if len(uidCols) > 0:
                uidCol = uidCols[0]
        uidTableData = []
        predictedClasses = list(df[result_column].unique())
        if uidCol:
            if uidCol in df.columns:
                for level in predictedClasses:
                    levelDf = df[df[result_column] == level]
                    levelDf = levelDf[[uidCol,"predicted_probability",result_column]]
                    levelDf.sort_values(by="predicted_probability", ascending=False,inplace=True)
                    levelDf["predicted_probability"] = levelDf["predicted_probability"].apply(lambda x: humanize.apnumber(x*100)+"%" if x*100 >=10 else str(int(x*100))+"%")
                    uidTableData.append(levelDf[:5])
                uidTableData = pd.concat(uidTableData)
                uidTableData  = [list(arr) for arr in list(uidTableData.values)]
                uidTableData = [[uidCol,"Probability",result_column]] + uidTableData
                uidTable = TableData()
                uidTable.set_table_width(25)
                uidTable.set_table_data(uidTableData)
                uidTable.set_table_type("normalHideColumn")
                self._result_setter.set_unique_identifier_table(json.loads(CommonUtils.convert_python_object_to_json(uidTable)))


        self._completionStatus += old_div(self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["prediction"]["weight"],10)
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "prediction",\
                                    "info",\
                                    self._scriptStages["prediction"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        # CommonUtils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))

        print("STARTING DIMENSION ANALYSIS ...")
        columns_to_keep = []
        columns_to_drop = []
        # considercolumnstype = self._dataframe_context.get_score_consider_columns_type()
        # considercolumns = self._dataframe_context.get_score_consider_columns()
        # if considercolumnstype != None:
        #     if considercolumns != None:
        #         if considercolumnstype == ["excluding"]:
        #             columns_to_drop = considercolumns
        #         elif considercolumnstype == ["including"]:
        #             columns_to_keep = considercolumns
        columns_to_keep = self._dataframe_context.get_score_consider_columns()
        if len(columns_to_keep) > 0:
            columns_to_drop = list(set(df.columns)-set(columns_to_keep))
        else:
            columns_to_drop += ["predicted_probability"]
        if set(columns_to_drop) == set(df.columns):
            columns_to_drop = ["predicted_probability"]
        columns_to_drop = [x for x in columns_to_drop if x in df.columns and x != result_column]
        df.drop(columns_to_drop, axis=1, inplace=True)
        # # Dropping predicted_probability column
        # df.drop('predicted_probability', axis=1, inplace=True)
        resultColLevelCount = dict(df[result_column].value_counts())
        # self._metaParser.update_level_counts(result_column,resultColLevelCount)
        self._metaParser.update_column_dict(result_column,{"LevelCount":resultColLevelCount,"numberOfUniqueValues":len(list(resultColLevelCount.keys()))})
        self._dataframe_context.set_story_on_scored_data(True)
        if self._pandas_flag:
            scored_df = df.copy()
        else:
            SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
            scored_df = SQLctx.createDataFrame(df)
        self._dataframe_context.update_consider_columns(columns_to_keep)
        df_helper = DataFrameHelper(scored_df, self._dataframe_context,self._metaParser)
        df_helper.set_params()
        scored_df = df_helper.get_data_frame()
        # try:
        #     fs = time.time()
        #     narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
        #     if narratives_file.startswith("file"):
        #         narratives_file = narratives_file[7:]
        #     result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
        #     if result_file.startswith("file"):
        #         result_file = result_file[7:]
        #     init_freq_dim = FreqDimensions(df, df_helper, self._dataframe_context,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
        #     df_freq_dimension_obj = init_freq_dim.test_all(dimension_columns=[result_column])
        #     df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
        #     narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj,self._result_setter,self._prediction_narrative,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
        #     narratives = CommonUtils.as_dict(narratives_obj)
        #
        #     print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        #     self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["frequency"]["weight"]/10
        #     progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
        #                                 "frequency",\
        #                                 "info",\
        #                                 self._scriptStages["frequency"]["summary"],\
        #                                 self._completionStatus,\
        #                                 self._completionStatus)
        #     CommonUtils.save_progress_message(self._messageURL,progressMessage)
        #     self._dataframe_context.update_completion_status(self._completionStatus)
        #     print "Frequency ",self._completionStatus
        # except:
        #     print "Frequency Analysis Failed "
        #
        # try:
        #     fs = time.time()
        #     narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
        #     if narratives_file.startswith("file"):
        #         narratives_file = narratives_file[7:]
        #     result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
        #     if result_file.startswith("file"):
        #         result_file = result_file[7:]
        #     init_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
        #     df_chisquare_obj = init_chisquare_obj.test_all(dimension_columns= [result_column])
        #     df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
        #     chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df,self._prediction_narrative,self._result_setter,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName))
        # except:
        #     print "ChiSquare Analysis Failed "
        if len(predictedClasses) >=2:
            try:
                fs = time.time()
                df_decision_tree_obj = DecisionTrees(scored_df, df_helper, self._dataframe_context,self._spark,self._metaParser,scriptWeight=self._scriptWeightDict, analysisName=self._analysisName).test_all(dimension_columns=[result_column])
                narratives_obj = CommonUtils.as_dict(DecisionTreeNarrative(result_column, df_decision_tree_obj, self._dataframe_helper, self._dataframe_context,self._metaParser,self._result_setter,story_narrative=None, analysisName=self._analysisName,scriptWeight=self._scriptWeightDict))
                print(narratives_obj)
            except:
                print("DecisionTree Analysis Failed ")
        else:
            data_dict = {"npred": len(predictedClasses), "nactual": len(list(labelMappingDict.values()))}

            if data_dict["nactual"] > 2:
                levelCountDict ={}
                levelCountDict[predictedClasses[0]] = resultColLevelCount[predictedClasses[0]]
                levelCountDict["Others"]  = sum([v for k,v in list(resultColLevelCount.items()) if k != predictedClasses[0]])
            else:
                levelCountDict = resultColLevelCount
                otherClass = list(set(labelMappingDict.values())-set(predictedClasses))[0]
                levelCountDict[otherClass] = 0

                print(levelCountDict)

            total = float(sum([x for x in list(levelCountDict.values()) if x != None]))
            levelCountTuple = [({"name":k,"count":v,"percentage":humanize.apnumber(old_div(v*100,total))+"%"}) for k,v in list(levelCountDict.items()) if v != None]
            levelCountTuple = sorted(levelCountTuple,key=lambda x:x["count"],reverse=True)
            data_dict["blockSplitter"] = "|~NEWBLOCK~|"
            data_dict["targetcol"] = result_column
            data_dict["nlevel"] = len(list(levelCountDict.keys()))
            data_dict["topLevel"] = levelCountTuple[0]
            data_dict["secondLevel"] = levelCountTuple[1]
            maincardSummary = NarrativesUtils.get_template_output("/apps/",'scorewithoutdtree.html',data_dict)

            main_card = NormalCard()
            main_card_data = []
            main_card_narrative = NarrativesUtils.block_splitter(maincardSummary,"|~NEWBLOCK~|")
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
            self._result_setter.set_score_dtree_cards([main_card],{})
