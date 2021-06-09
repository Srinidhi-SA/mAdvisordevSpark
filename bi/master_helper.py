from __future__ import print_function
from builtins import str
from builtins import range
import json
import time
import re
import numpy as np
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils

from bi.algorithms import data_preprocessing as data_preprocessing
from bi.algorithms import feature_engineering as feature_engineering
from bi.scripts.metadata import MetaDataScript
from bi.common import NarrativesTree
from bi.settings import setting as GLOBALSETTINGS
from bi.common import DataLoader,MetaParser, DataFrameHelper,ContextSetter,ResultSetter,NormalCard,HtmlData
from bi.scripts.classification.ensemble_model import EnsembleModelScript
from bi.scripts.classification.random_forest import RFClassificationModelScript

from bi.scripts.classification.random_forest_pyspark import RandomForestPysparkScript
from bi.scripts.classification.multilayer_perceptron_pyspark import MultilayerPerceptronPysparkScript
from bi.scripts.classification.xgboost_pyspark import XGBoostPysparkScript
from bi.scripts.classification.logistic_regression_pyspark import LogisticRegressionPysparkScript
from bi.scripts.classification.naive_bayes import NBBClassificationModelScript
from bi.scripts.classification.naive_bayes import NBGClassificationModelScript
from bi.scripts.classification.naive_bayes import NBMClassificationModelScript
from bi.scripts.classification.naive_bayes_pyspark import NaiveBayesPysparkScript
from bi.scripts.classification.xgboost_pyspark import XGBoostPysparkScript
from bi.scripts.classification.xgboost_classification import XgboostScript
from bi.scripts.classification.lgbm_classification import LgbmScript
from bi.scripts.classification.adaboost_classification import AdaboostScript
from bi.scripts.classification.logistic_regression import LogisticRegressionScript
from bi.scripts.classification.neural_network import NeuralNetworkScript
from bi.scripts.classification.tensor_flow_nn import TensorFlowScript
from bi.scripts.regression.tensor_flow_reg_nn import TensorFlowRegScript
from bi.scripts.classification.neural_networks_pytorch_classification import NNPTClassificationScript
from bi.scripts.regression.neural_networks_pytorch_regression import NNPTRegressionScript
from bi.scripts.classification.svm import SupportVectorMachineScript
from bi.scripts.regression.linear_regression_model import LinearRegressionModelScript
from bi.scripts.regression.generalized_linear_regression_model import GeneralizedLinearRegressionModelScript
from bi.scripts.regression.gbt_regression_model import GBTRegressionModelScript
from bi.scripts.regression.rf_regression_model import RFRegressionModelScript
from bi.scripts.regression.dtree_regression_model import DTREERegressionModelScript
from bi.scripts.metadata_pandas import MetaDataScriptPandas
from bi.transformations import DataFrameFilterer
from bi.transformations import DataFrameTransformer

from bi.scripts.dimensionAnalysis.frequency_dimensions import FreqDimensionsScript
from bi.scripts.dimensionAnalysis.chisquare import ChiSquareScript
from bi.scripts.dimensionAnalysis.decision_tree import DecisionTreeScript
from bi.scripts.measureAnalysis.correlation import CorrelationScript
from bi.scripts.measureAnalysis.descr_stats import DescriptiveStatsScript
from bi.scripts.measureAnalysis.two_way_anova import TwoWayAnovaScript
from bi.scripts.measureAnalysis.linear_regression import LinearRegressionScript
from bi.scripts.timeseries import TrendScript
from bi.scripts.measureAnalysis.decision_tree_regression import DecisionTreeRegressionScript

from bi.scripts.business_impact import BusinessCard


def load_dataset(spark,dataframe_context):
    datasource_type = dataframe_context.get_datasource_type()
    if datasource_type == "fileUpload":
        try:
            df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())
            cols = [re.sub('\W+','_', col.strip()) for col in df.columns]
            df = df.toDF(*cols)
            df = df.replace(GLOBALSETTINGS.DEFAULT_NULL_VALUES, 'null')
            dataframe_context._pandas_flag = False
            print("####### PYSPARK ########### STARTED PYSPARK FLOW ################ PYSPARK #########")
            pyspark=True
        except:
            df = DataLoader.load_csv_file_pandas(dataframe_context.get_input_file())
            df.columns = [re.sub('\W+','_', col.strip()) for col in df.columns]
            bool_cols= list(df.select_dtypes(include=['bool']).columns)
            df[bool_cols] =df[bool_cols].astype('object')
            df = df.replace(GLOBALSETTINGS.DEFAULT_NULL_VALUES, np.nan)
            df = df.replace([' ',','],'_', regex=True)
            print("######## PANDAS ########### STARTED PANDAS FLOW ############# PANDAS ##############")
            dataframe_context._pandas_flag = True
            pyspark=False

        # cols = [re.sub("[[]|[]]|[<]|[\.]|[*]|[$]|[#]","", col) for col in df.columns]
        # df = reduce(lambda data, idx: data.withColumnRenamed(df.columns[idx], cols[idx]), xrange(len(df.columns)), df)
    else:
        dbConnectionParams = dataframe_context.get_dbconnection_params()
        df = DataLoader.create_dataframe_from_jdbc_connector(spark, datasource_type, dbConnectionParams)
        # cols = [re.sub("[[]|[]]|[<]|[\.]|[*]|[$]|[#]", "", col) for col in df.columns]
        cols = [re.sub('\W+','_', col.strip()) for col in df.columns]
        df = df.toDF(*cols)
        pyspark=True
        # df = reduce(lambda data, idx: data.withColumnRenamed(df.columns[idx], cols[idx]), xrange(len(df.columns)), df)
    if pyspark:
        if df != None:
            # Dropping blank rows
            df = df.dropna(how='all', thresh=None, subset=None)

        if df != None:
            print("DATASET LOADED")
            print(df.printSchema())
        else:
            print("DATASET NOT LOADED")
    else:
        try:
            df = df.dropna(how='all', thresh=None, subset=None)
            print(df.dtypes)
            print("DATASET LOADED")
        except:
            print("DATASET NOT LOADED")
    return df

def get_metadata(df,spark,dataframe_context,new_cols_added):
    debugMode = dataframe_context.get_debug_mode()
    jobType = dataframe_context.get_job_type()
    if df is not None:
        metaParserInstance = MetaParser()
        if debugMode != True:
            if jobType != "metaData":
                print("Retrieving MetaData")
                if new_cols_added != None:
                    try:
                        df_new_added_cols = df.select([c for c in df.columns if c in new_cols_added])
                    except:
                        df_new_added_cols = df[[c for c in df.columns if c in new_cols_added]]
                    print("starting Metadata for newly added columns")
                    dataframe_context.set_metadata_ignore_msg_flag(True)
                    try:
                        meta_data_class_new = MetaDataScript(df_new_added_cols,spark,dataframe_context)
                        meta_data_object_new = meta_data_class_new.run()
                        metaDataObj_new = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object_new))
                        metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                        for x in range(len(metaDataObj_new['headers'])):
                            metaDataObj['headers'].append(metaDataObj_new['headers'][x])
                        # metaDataObj['sampleData'].append(metaDataObj_new['sampleData'])
                        for x in range(len(metaDataObj_new['metaData'])):
                            metaDataObj['metaData'].append(metaDataObj_new['metaData'][x])
                        for x in range(len(metaDataObj_new['columnData'])):
                            metaDataObj['columnData'].append(metaDataObj_new['columnData'][x])
                    except:
                        fs = time.time()
                        print("starting Metadata")
                        dataframe_context.set_metadata_ignore_msg_flag(True)
                        meta_data_class = MetaDataScript(df,spark,dataframe_context)
                        meta_data_object = meta_data_class.run()
                        metaDataObj = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object))
                        print("metaData Analysis Done in ", time.time() - fs, " seconds.")
                        metaParserInstance.set_params(metaDataObj)

                else:
                    metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                if metaDataObj:
                    metaParserInstance.set_params(metaDataObj)
                else:
                    fs = time.time()
                    print("starting Metadata")
                    dataframe_context.set_metadata_ignore_msg_flag(True)
                    meta_data_class = MetaDataScript(df,spark,dataframe_context)
                    meta_data_object = meta_data_class.run()
                    metaDataObj = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object))
                    print("metaData Analysis Done in ", time.time() - fs, " seconds.")
                    metaParserInstance.set_params(metaDataObj)
        elif debugMode == True:
            if jobType != "metaData":
                # checking if metadata exist for the dataset
                # else it will run metadata first
                # while running in debug mode the dataset_slug should be correct or some random String
                try:
                    if new_cols_added != None:
                        try:
                            df_new_added_cols = df.select([c for c in df.columns if c in new_cols_added])
                        except:
                            df_new_added_cols = df[[c for c in df.columns if c in new_cols_added]]
                        print("starting Metadata for newly added columns")
                        dataframe_context.set_metadata_ignore_msg_flag(True)
                        meta_data_class_new = MetaDataScript(df_new_added_cols,spark,dataframe_context)
                        meta_data_object_new = meta_data_class_new.run()
                        metaDataObj_new = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object_new))
                        metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                        for x in range(len(metaDataObj_new['headers'])):
                            metaDataObj['headers'].append(metaDataObj_new['headers'][x])
                        # metaDataObj['sampleData'].append(metaDataObj_new['sampleData'])
                        for x in range(len(metaDataObj_new['metaData'])):
                            metaDataObj['metaData'].append(metaDataObj_new['metaData'][x])
                        for x in range(len(metaDataObj_new['columnData'])):
                            metaDataObj['columnData'].append(metaDataObj_new['columnData'][x])
                    else:
                        metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                except:
                    metaDataObj = None
                if metaDataObj:
                    metaParserInstance.set_params(metaDataObj)
                else:
                    fs = time.time()
                    print("starting Metadata")
                    dataframe_context.set_metadata_ignore_msg_flag(True)
                    meta_data_class = MetaDataScript(df,spark,dataframe_context)
                    meta_data_object = meta_data_class.run()
                    metaDataObj = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object))
                    print("metaData Analysis Done in ", time.time() - fs, " seconds.")
                    metaParserInstance.set_params(metaDataObj)

        if jobType != "metaData":
            dataframe_context.set_ignore_column_suggestions(metaParserInstance.get_ignore_columns())
            dataframe_context.set_utf8_columns(metaParserInstance.get_utf8_columns())
            dataframe_context.set_date_format(metaParserInstance.get_date_format())

            percentageColumns = metaParserInstance.get_percentage_columns()
            dollarColumns = metaParserInstance.get_dollar_columns()
            dataframe_context.set_percentage_columns(percentageColumns)
            dataframe_context.set_dollar_columns(dollarColumns)
        return metaParserInstance
    else:
        return None

def set_dataframe_helper(df,dataframe_context,metaParserInstance):
    dataframe_helper = DataFrameHelper(df, dataframe_context, metaParserInstance)
    dataframe_helper.set_params()
    df = dataframe_helper.get_data_frame()
    return df,dataframe_helper

def train_models_automl(spark,linear_df,tree_df,dataframe_context,dataframe_helper_linear_df,dataframe_helper_tree_df,metaParserInstance_linear_df,metaParserInstance_tree_df,one_click_json):
    automl_clf_models=[]
    st = time.time()
    LOGGER = dataframe_context.get_logger()
    jobUrl = dataframe_context.get_job_url()
    errorURL = dataframe_context.get_error_url()
    xmlUrl = dataframe_context.get_xml_url()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    appid = dataframe_context.get_app_id()
    mlEnv = dataframe_context.get_ml_environment()
    print("appid",appid)
    dataframe_context.initialize_ml_model_training_weight()
    pandas_flag = dataframe_context._pandas_flag
    prediction_narrative = NarrativesTree()
    prediction_narrative.set_name("models")
    result_setter = ResultSetter(dataframe_context)

    uid_col = dataframe_context.get_uid_column()
    result_column = dataframe_context.get_result_column()
    allDateCols = dataframe_context.get_date_columns()

    # Linear
    dataframe_helper_linear_df.remove_null_rows(dataframe_context.get_result_column())
    linear_df = dataframe_helper_linear_df.fill_missing_values(linear_df)
    categorical_columns_linear_df = dataframe_helper_linear_df.get_string_columns()
    if metaParserInstance_linear_df.check_column_isin_ignored_suggestion(uid_col):
        categorical_columns_linear_df = list(set(categorical_columns_linear_df) - {uid_col})
    categorical_columns_linear_df = list(set(categorical_columns_linear_df)-set(allDateCols))

    # Tree
    dataframe_helper_tree_df.remove_null_rows(dataframe_context.get_result_column())
    tree_df = dataframe_helper_tree_df.fill_missing_values(tree_df)
    categorical_columns_tree_df = dataframe_helper_tree_df.get_string_columns()
    if metaParserInstance_tree_df.check_column_isin_ignored_suggestion(uid_col):
        categorical_columns_tree_df = list(set(categorical_columns_tree_df) - {uid_col})
    categorical_columns_tree_df = list(set(categorical_columns_tree_df)-set(allDateCols))

    if pandas_flag:
        try:
            linear_df = linear_df.toPandas()
            tree_df = tree_df.toPandas()
        except:
            pass

        linear_df.columns = [re.sub("[[]|[]]|[<]","", col) for col in linear_df.columns.values]        # df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        tree_df.columns = [re.sub("[[]|[]]|[<]","", col) for col in tree_df.columns.values]        # df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])

        dataframe_helper_linear_df.set_train_test_data(linear_df)
        dataframe_helper_tree_df.set_train_test_data(tree_df)
        mlEnvironment = "sklearn"
    else:
        mlEnvironment = "spark"

    model_slug = dataframe_context.get_model_path()
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_MODELS
    subfolders = list(GLOBALSETTINGS.SLUG_MODEL_MAPPING.keys())
    model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=subfolders)
    dataframe_context.set_model_path(model_file_path)
    app_type = GLOBALSETTINGS.APPS_ID_MAP[appid]["type"]
    algosToRun = dataframe_context.get_algorithms_to_run()
    scriptWeightDict = dataframe_context.get_ml_model_training_weight()
    scriptStages = {
        "preprocessing":{
            "summary":"Dataset Loading Completed",
            "weight":4
            }
        }
    CommonUtils.create_update_and_save_progress_message(dataframe_context,scriptWeightDict,scriptStages,"initialization","preprocessing","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
    if len(algosToRun) == 3:
        completionStatus = 40
        dataframe_context.update_completion_status(completionStatus)
    if len(algosToRun) == 2:
        completionStatus = 50
        dataframe_context.update_completion_status(completionStatus)
    if len(algosToRun) == 1:
        completionStatus = 60
        dataframe_context.update_completion_status(completionStatus)

    if app_type == "CLASSIFICATION":
        for obj in algosToRun:
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["randomforest"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        rf_obj = RFClassificationModelScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                        # rf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance)
                        rf_obj.Train()
                        automl_clf_models.append(rf_obj._model)
                    else:
                        sprf_obj = RandomForestPysparkScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                        # rf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                        sprf_obj.Train()
                    print("Random Forest Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_rf_fail_card({"Algorithm_Name":"randomforest","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["xgboost"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        xgb_obj = XgboostScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                        xgb_obj.Train()
                        automl_clf_models.append(xgb_obj._model)
                    else:
                        spxgb_obj = XGBoostPysparkScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                        spxgb_obj.Train()
                    print("XGBoost Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_xgb_fail_card({"Algorithm_Name":"xgboost","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["LightGBM"]:
                try:
                    st = time.time()
                    lgb_obj = LgbmScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                    lgb_obj.Train()
                    #automl_clf_models.append(lgb_obj._model)
                    print("lightgbm Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lgbm_fail_card({"Algorithm_Name":"LightGBM","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"LightGBM",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["adaboost"]:
                try:
                    st = time.time()
                    adab_obj = AdaboostScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                    adab_obj.Train()
                    automl_clf_models.append(adab_obj._model)
                    print("Adaboost Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_adab_fail_card({"Algorithm_Name":"Adaboost","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Adaboost",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["logisticregression"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        lr_obj = LogisticRegressionScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                        lr_obj.Train()
                        #automl_clf_models.append(lr_obj._model)
                    else:
                        print("##########################SPARK LOG STARTED")
                        lr_obj = LogisticRegressionPysparkScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                        lr_obj.Train()
                    print("Logistic Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"Logistic Regression","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naivebayesber"] and obj.get_algorithm_name() == "naivebayesber":
                try:
                    st = time.time()
                    nb_obj = NBBClassificationModelScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                    nb_obj.Train()
                    automl_clf_models.append(nb_obj._model)
                    print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naivebayesgau"] and obj.get_algorithm_name() == "naivebayesgau":
                try:
                    st = time.time()
                    nb_obj = NBGClassificationModelScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                    nb_obj.Train()
                    automl_clf_models.append(nb_obj._model)
                    print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naive bayes"] and obj.get_algorithm_name() == "naive bayes":
                try:
                    st = time.time()
                    if pandas_flag:
                        nb_obj = NBMClassificationModelScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                        # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                        nb_obj.Train()
                        print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                    else:
                        try:
                            spnb_obj = NaiveBayesPysparkScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                            spnb_obj .Train()
                            print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                        except Exception as e:
                            result_setter.set_nb_fail_card({"Algorithm_Name":"Naive Bayes","success":"False"})
                            CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",'dataset not suitable for naive bayes')
                            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)


                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
                    try:
                        print("Calling Gaussian NB script ..............")
                        st = time.time()
                        nb_obj = NBGClassificationModelScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_linear_df)
                        nb_obj.Train()
                        automl_clf_models.append(nb_obj._model)
                        print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                    except Exception as e:
                        result_setter.set_nb_fail_card({"Algorithm_Name":"Naive Bayes","success":"False"})
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (Sklearn)"] and obj.get_algorithm_name() == "Neural Network (Sklearn)":
                try:
                    st = time.time()
                    nn_obj = NeuralNetworkScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                    nn_obj.Train()
                    #automl_clf_models.append(nn_obj._model)
                    print("Neural Network (Sklearn) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nn_fail_card({"Algorithm_Name":"Neural Network (Sklearn)","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (Sklearn)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if  obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (TensorFlow)"]:
                try:
                    st = time.time()
                    tf_obj = TensorFlowScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                    tf_obj.Train()
                    #automl_clf_models.append(tf_obj._model)
                    print("Neural Network (TensorFlow) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_tf_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if  obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (PyTorch)"]:
                try:
                    st = time.time()
                    nnptc_obj = NNPTClassificationScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df)
                    nnptc_obj.Train()
                    #automl_clf_models.append(nnptc_obj._model)
                    print("Neural Network (PyTorch) trained in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nnptc_fail_card({"Algorithm_Name": "Neural Network (PyTorch)", "success": "False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER, "Neural Network (PyTorch)", e)
                    CommonUtils.save_error_messages(errorURL, APP_NAME, e, ignore=ignoreMsg)
        try:
           st = time.time()
           en_obj = EnsembleModelScript(tree_df,linear_df, dataframe_helper_tree_df,dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance_tree_df,automl_clf_models,)
           en_obj.Train()
           print("Ensemble Model trained in ", time.time() - st,  " seconds.")
        except Exception as e:
           result_setter.set_en_fail_card({"Algorithm_Name": "Ensemble", "success": "False"})
           CommonUtils.print_errors_and_store_traceback(LOGGER, "Ensemble", e)
           CommonUtils.save_error_messages(errorURL, APP_NAME, e, ignore=ignoreMsg)
    elif app_type == "REGRESSION":
        for obj in algosToRun:
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["linearregression"]:
                try:
                    st = time.time()
                    lin_obj = LinearRegressionModelScript(linear_df, dataframe_helper_linear_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_linear_df,mlEnvironment)
                    lin_obj.Train()
                    print("Linear Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"linearregression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"linearRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (TensorFlow)"]:
                try:
                    st = time.time()
                    lin_obj = TensorFlowRegScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_tree_df)
                    lin_obj.Train()
                    print("Neural Network (TensorFlow) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (PyTorch)"]:
                try:
                    st = time.time()
                    nnptr_obj = NNPTRegressionScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_tree_df)
                    nnptr_obj.Train()
                    print("Neural Network (PyTorch) -R trained in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nnptr_fail_card({"Algorithm_Name":"Neural Network (PyTorch)","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (PyTorch)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["gbtregression"]:
                try:
                    st = time.time()
                    gbt_obj = GBTRegressionModelScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
                    gbt_obj.Train()
                    print("GBT Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_gbt_fail_card({"Algorithm_Name":"gbtregression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"gbtRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["dtreeregression"]:
                try:
                    st = time.time()
                    dtree_obj = DTREERegressionModelScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
                    dtree_obj.Train()
                    print("DTREE Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_dtr_fail_card({"Algorithm_Name":"DecisionTree","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"dtreeRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["rfregression"]:
                print("randomn forest is running")
                try:
                    st = time.time()
                    rf_obj = RFRegressionModelScript(tree_df, dataframe_helper_tree_df, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
                    rf_obj.Train()
                    print("RF Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_rf_fail_card({"Algorithm_Name":"rfRegression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"rfRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        pass
        """
        # TODO
        """

    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Evaluating And Comparing Performance Of All Predictive Models",85,85,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    modelJsonOutput = MLUtils.collated_model_summary_card(result_setter,prediction_narrative,app_type,appid=appid,)
    modelJsonOutput['one_click'] = one_click_json
    response = CommonUtils.save_result_json(jobUrl,json.dumps(modelJsonOutput))
    print(modelJsonOutput)

    pmmlModels = result_setter.get_pmml_object()
    savepmml = CommonUtils.save_pmml_models(xmlUrl,pmmlModels)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","mAdvisor Has Successfully Completed Building Machine Learning Models",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print("Model Training Completed in ", time.time() - st, " seconds.")

def train_models(spark,df,dataframe_context,dataframe_helper,metaParserInstance,one_click_json):
    st = time.time()
    LOGGER = dataframe_context.get_logger()
    jobUrl = dataframe_context.get_job_url()
    errorURL = dataframe_context.get_error_url()
    xmlUrl = dataframe_context.get_xml_url()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    appid = dataframe_context.get_app_id()
    mlEnv = dataframe_context.get_ml_environment()
    pandas_flag = dataframe_context._pandas_flag
    # dataCleansingDict = dataframe_context.get_dataCleansing_info()
    # featureEngineeringDict = dataframe_context.get_featureEngginerring_info()

    print("appid",appid)
    dataframe_context.initialize_ml_model_training_weight()

    prediction_narrative = NarrativesTree()
    prediction_narrative.set_name("models")
    result_setter = ResultSetter(dataframe_context)

    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    ####New Feature Engineering Implementation#############

    # time_before_preprocessing = time.time()
    # if dataCleansingDict['selected']:
    #     data_preprocessing_obj = data_preprocessing.DataPreprocessing(spark, df, dataframe_context, dataframe_helper, metaParserInstance, dataCleansingDict, featureEngineeringDict)
    #     df = data_preprocessing_obj.data_cleansing()
    #
    # if featureEngineeringDict['selected']:
    #     feature_engineering_obj = feature_engineering.FeatureEngineering(spark, df, dataframe_context, dataframe_helper, metaParserInstance, featureEngineeringDict)
    #     df = feature_engineering_obj.feature_engineering()
    #
    # time_after_preprocessing = time.time()
    # time_required_for_preprocessing = time_after_preprocessing - time_before_preprocessing
    # print "Time Required for Data Preprocessing = ", time_required_for_preprocessing
    # df,dataframe_helper = set_dataframe_helper(df,dataframe_context,metaParserInstance)
    df = dataframe_helper.fill_missing_values(df)
    categorical_columns = dataframe_helper.get_string_columns()
    uid_col = dataframe_context.get_uid_column()
    if metaParserInstance.check_column_isin_ignored_suggestion(uid_col):
        categorical_columns = list(set(categorical_columns) - {uid_col})
    result_column = dataframe_context.get_result_column()
    allDateCols = dataframe_context.get_date_columns()
    categorical_columns = list(set(categorical_columns)-set(allDateCols))

    if pandas_flag:
        try:
            df = df.toPandas()
        except:
            pass
        df.columns = [re.sub("[[]|[]]|[<]","", col) for col in df.columns.values]
        # df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        dataframe_helper.set_train_test_data(df)
        mlEnvironment = 'sklearn'
    else:
        mlEnvironment = 'spark'

    model_slug = dataframe_context.get_model_path()
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_MODELS
    subfolders = list(GLOBALSETTINGS.SLUG_MODEL_MAPPING.keys())
    model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=subfolders)
    dataframe_context.set_model_path(model_file_path)
    app_type = GLOBALSETTINGS.APPS_ID_MAP[appid]["type"]
    algosToRun = dataframe_context.get_algorithms_to_run()
    for obj in algosToRun:
        print ('###########################', obj.get_algorithm_name(), obj.get_algorithm_slug(), '#############################')
    scriptWeightDict = dataframe_context.get_ml_model_training_weight()
    scriptStages = {
        "preprocessing":{
            "summary":"Dataset Loading Completed",
            "weight":4
            }
        }
    CommonUtils.create_update_and_save_progress_message(dataframe_context,scriptWeightDict,scriptStages,"initialization","preprocessing","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
    if len(algosToRun) == 3:
        completionStatus = 40
        dataframe_context.update_completion_status(completionStatus)
    if len(algosToRun) == 2:
        completionStatus = 50
        dataframe_context.update_completion_status(completionStatus)
    if len(algosToRun) == 1:
        completionStatus = 60
        dataframe_context.update_completion_status(completionStatus)
    if app_type == "CLASSIFICATION":
        for obj in algosToRun:
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["randomforest"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        rf_obj = RFClassificationModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        # rf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance)
                        rf_obj.Train()
                    else:
                        sprf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        # rf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                        sprf_obj.Train()
                    print("Random Forest Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_rf_fail_card({"Algorithm_Name":"randomforest","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["xgboost"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        xgb_obj = XgboostScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        xgb_obj.Train()
                    else:
                        spxgb_obj = XGBoostPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        spxgb_obj.Train()
                    print("XGBoost Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_xgb_fail_card({"Algorithm_Name":"xgboost","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["LightGBM"]:
                try:
                    st = time.time()
                    lgb_obj = LgbmScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    lgb_obj.Train()
                    print("lightgbm Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lgbm_fail_card({"Algorithm_Name":"LightGBM","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"LightGBM",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["adaboost"]:
                try:
                    st = time.time()
                    adab_obj = AdaboostScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    adab_obj.Train()
                    print("Adaboost Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_adab_fail_card({"Algorithm_Name":"Adaboost","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Adaboost",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["logisticregression"]:
                try:
                    st = time.time()
                    if pandas_flag:
                        lr_obj = LogisticRegressionScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        lr_obj.Train()
                    else:
                        print("##########################SPARK LOG STARTED")
                        lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        lr_obj.Train()
                    print("Logistic Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"Logistic Regression","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)


            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naivebayesber"] and obj.get_algorithm_name() == "naivebayesber":
                try:
                    st = time.time()
                    nb_obj = NBBClassificationModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                    nb_obj.Train()
                    print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naivebayesgau"] and obj.get_algorithm_name() == "naivebayesgau":
                try:
                    st = time.time()
                    nb_obj = NBGClassificationModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                    nb_obj.Train()
                    print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["naive bayes"] and obj.get_algorithm_name() == "naive bayes":
                try:
                    st = time.time()
                    if pandas_flag:
                        nb_obj = NBMClassificationModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                        nb_obj.Train()
                    else:
                        spnb_obj = NaiveBayesPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        spnb_obj .Train()
                    print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
                    try:
                        print("Calling Gaussian NB script ..............")
                        st = time.time()
                        nb_obj = NBGClassificationModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                        # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                        nb_obj.Train()
                        print("Naive Bayes Model Done in ", time.time() - st,  " seconds.")
                    except Exception as e:
                        result_setter.set_nb_fail_card({"Algorithm_Name":"Naive Bayes","success":"False"})
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"naivebayes",e)
                        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (Sklearn)"] and obj.get_algorithm_name() == "Neural Network (Sklearn)":
                try:
                    st = time.time()
                    nn_obj = NeuralNetworkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                    nn_obj.Train()
                    print("Neural Network (Sklearn) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nn_fail_card({"Algorithm_Name":"Neural Network (Sklearn)","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (Sklearn)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if  obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (TensorFlow)"]:
                try:
                    st = time.time()
                    tf_obj = TensorFlowScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
                    tf_obj.Train()
                    print("Neural Network (TensorFlow) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_tf_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if  obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (PyTorch)"]:
                try:
                    st = time.time()
                    nnptc_obj = NNPTClassificationScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
                    nnptc_obj.Train()
                    print("Neural Network (PyTorch)  trained in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nnptc_fail_card({"Algorithm_Name": "Neural Network (PyTorch)", "success": "False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER, "Neural Network (PyTorch)", e)
                    CommonUtils.save_error_messages(errorURL, APP_NAME, e, ignore=ignoreMsg)

    elif app_type == "REGRESSION":
        for obj in algosToRun:
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["linearregression"]:
                try:
                    st = time.time()
                    lin_obj = LinearRegressionModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance,mlEnvironment)
                    lin_obj.Train()
                    print("Linear Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"linearregression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"linearRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (TensorFlow)"]:
                try:
                    st = time.time()
                    lin_obj = TensorFlowRegScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance)
                    lin_obj.Train()
                    print("Neural Network (TensorFlow) Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_lr_fail_card({"Algorithm_Name":"Neural Network (TensorFlow)","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["Neural Network (PyTorch)"]:
                try:
                    st = time.time()
                    nnptr_obj = NNPTRegressionScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance)
                    nnptr_obj.Train()
                    print("Neural Network (PyTorch) -R trained in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_nnptr_fail_card({"Algorithm_Name":"Neural Network (PyTorch)","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (PyTorch)",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            # if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["generalizedlinearregression"]:
            #     try:
            #         st = time.time()
            #         lin_obj = GeneralizedLinearRegressionModelScript(df,
            # , dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance)
            #         lin_obj.Train()
            #         print "Generalized Linear Regression Model Done in ", time.time() - st,  " seconds."
            #     except Exception as e:
            #         CommonUtils.print_errors_and_store_traceback(LOGGER,"generalizedLinearRegression",e)
            #         CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["gbtregression"]:
                try:
                    st = time.time()
                    gbt_obj = GBTRegressionModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance,mlEnvironment)
                    gbt_obj.Train()
                    print("GBT Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_gbt_fail_card({"Algorithm_Name":"gbtregression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"gbtRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["dtreeregression"]:
                try:
                    st = time.time()
                    dtree_obj = DTREERegressionModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance,mlEnvironment)
                    dtree_obj.Train()
                    print("DTREE Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_dtr_fail_card({"Algorithm_Name":"DecisionTree","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"dtreeRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            if obj.get_algorithm_slug() == GLOBALSETTINGS.MODEL_SLUG_MAPPING["rfregression"]:
                try:
                    st = time.time()
                    rf_obj = RFRegressionModelScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative, result_setter, metaParserInstance,mlEnvironment)
                    rf_obj.Train()
                    print("RF Regression Model Done in ", time.time() - st,  " seconds.")
                except Exception as e:
                    result_setter.set_rf_fail_card({"Algorithm_Name":"rfRegression","Success":"False"})
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"rfRegression",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Evaluating And Comparing Performance Of All Predictive Models",85,85,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    modelJsonOutput = MLUtils.collated_model_summary_card(result_setter,prediction_narrative,app_type,appid=appid,)
    modelJsonOutput['one_click'] = one_click_json
    response = CommonUtils.save_result_json(jobUrl,json.dumps(modelJsonOutput))
    print(modelJsonOutput)

    pmmlModels = result_setter.get_pmml_object()
    savepmml = CommonUtils.save_pmml_models(xmlUrl,pmmlModels)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","mAdvisor Has Successfully Completed Building Machine Learning Models",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print("Model Training Completed in ", time.time() - st, " seconds.")

def score_model_autoML(spark,linear_df,tree_df,dataframe_context,df_helper_linear_df,df_helper_tree_df,metaParserInstance_linear_df,metaParserInstance_tree_df):
    dataframe_context.set_anova_on_scored_data(True)
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    jobName = dataframe_context.get_job_name()
    ignoreMsg = dataframe_context.get_message_ignore()
    targetLevel = dataframe_context.get_target_level_for_model()
    dataCleansingDict = dataframe_context.get_dataCleansing_info()
    featureEngineeringDict = dataframe_context.get_featureEngginerring_info()
    print("Prediction Started")
    dataframe_context.initialize_ml_model_prediction_weight()
    pandas_flag = dataframe_context._pandas_flag
    st = time.time()
    story_narrative = NarrativesTree()
    story_narrative.set_name("scores")
    result_setter = ResultSetter(dataframe_context)
    model_path = dataframe_context.get_model_path()
    print("model path",model_path)
    result_column = dataframe_context.get_result_column()



    # Linear
    if result_column in linear_df.columns:
        df_helper_linear_df.remove_null_rows(result_column)
    linear_df = df_helper_linear_df.get_data_frame()
    ## TO DO : Unnecessary function , mostly need to be removed on discussion
    linear_df = df_helper_linear_df.fill_missing_values(linear_df)

    # Tree
    if result_column in tree_df.columns:
        df_helper_tree_df.remove_null_rows(result_column)
    tree_df = df_helper_tree_df.get_data_frame()
    tree_df = df_helper_tree_df.fill_missing_values(tree_df)
    if pandas_flag:
        mlEnvironment = "sklearn"
    else:
        mlEnvironment = "spark"




    model_slug = model_path
    score_slug = dataframe_context.get_score_path()
    print("score_slug",score_slug)
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_SCORES
    score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
    appid = str(dataframe_context.get_app_id())
    app_type = dataframe_context.get_app_type()
    algorithm_name = dataframe_context.get_algorithm_slug()[0]
    print("algorithm_name",algorithm_name)
    print("score_file_path",score_file_path)
    print("model_slug",model_slug)

    scriptWeightDict = dataframe_context.get_ml_model_prediction_weight()
    scriptStages = {
        "preprocessing":{
            "summary":"Dataset Loading Completed",
            "weight":4
            }
        }
    print(scriptWeightDict)
    CommonUtils.create_update_and_save_progress_message(dataframe_context,scriptWeightDict,scriptStages,"initialization","preprocessing","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

    if app_type == "CLASSIFICATION":
        model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
        print("selected_model_for_prediction", selected_model_for_prediction)
        if "randomforest" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = RFClassificationModelScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            else:
                trainedModel = RandomForestPysparkScript(tree_df, df_helper_tree_df, dataframe_context, spark,story_narrative,result_setter,metaParserInstance_tree_df)
            # trainedModel = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "sparkrandomforest" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = RandomForestPysparkScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"sparkrandomforest",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "xgboost" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = XgboostScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            else:
                trainedModel = XGBoostPysparkScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (Sklearn)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = NeuralNetworkScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural_Network_Sklearn",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "logisticregression" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = LogisticRegressionScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
            else:
                trainedModel = LogisticRegressionPysparkScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (TensorFlow)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = TensorFlowScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (PyTorch)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = NNPTClassificationScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (PyTorch)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "naive bayes" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = NBMClassificationModelScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
                # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
                try:
                    trainedModel.Predict()
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
                    try:
                        trainedModel = NBGClassificationModelScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
                        trainedModel.Predict()
                    except Exception as e:
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            else:
                trainedModel = NaiveBayesPysparkScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
                try:
                    trainedModel.Predict()
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "LightGBM" in selected_model_for_prediction:
            trainedModel = LgbmScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"LightGBM",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "adaboost" in selected_model_for_prediction:
            trainedModel = AdaboostScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Adaboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "ensemble" in selected_model_for_prediction:
            automl_clf_models = []
            trainedModel = EnsembleModelScript(tree_df,linear_df, df_helper_tree_df,df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df,automl_clf_models)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Ensemble",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        else:
            print("Could Not Load the Model for Scoring")

        # scoreSummary = CommonUtils.convert_python_object_to_json(story_narrative)
        storycards = result_setter.get_score_cards()
        storyNode = NarrativesTree()
        storyNode.add_cards(storycards)
        # storyNode = {"listOfCards":[storycards],"listOfNodes":[],"name":None,"slug":None}
        scoreSummary = CommonUtils.convert_python_object_to_json(storyNode)
        print(scoreSummary)
        jobUrl = dataframe_context.get_job_url()
        response = CommonUtils.save_result_json(jobUrl,scoreSummary)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","mAdvisor Has Successfully Completed Building Machine Learning Models",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print("Model Scoring Completed in ", time.time() - st, " seconds.")

    elif app_type == "REGRESSION":

        '''
        To be done later when regression scoring is wired
        '''
        model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        dataframe_context.set_story_on_scored_data(True)
        selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
        print("selected_model_for_prediction", selected_model_for_prediction)
        if "linearregression" in  selected_model_for_prediction:
            trainedModel = LinearRegressionModelScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative, result_setter, metaParserInstance_linear_df,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"linearregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "gbtregression" in  selected_model_for_prediction:
            trainedModel = GBTRegressionModelScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"gbtregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "dtreeregression" in  selected_model_for_prediction:
            trainedModel = DTREERegressionModelScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"dtreeregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "rfregression" in  selected_model_for_prediction:
            trainedModel = RFRegressionModelScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative, result_setter, metaParserInstance_tree_df,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"rfregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        headNode = NarrativesTree()
        if headNode != None:
            headNode.set_name(jobName)
        # headNode["name"] = jobName
        # distributionNode = result_setter.get_distribution_node()
        # if distributionNode != None:
        #     headNode["listOfNodes"].append(distributionNode)
        # anovaNode = result_setter.get_anova_node()
        # if anovaNode != None:
        #     headNode["listOfNodes"].append(anovaNode)
        # decisionTreeNode = result_setter.get_decision_tree_node()
        # if decisionTreeNode != None:
        #     headNode["listOfNodes"].append(decisionTreeNode)

        kpiCard = result_setter.get_kpi_card_regression_score()
        kpiCard = json.loads(CommonUtils.convert_python_object_to_json(kpiCard))

        coeffCard = result_setter.get_coeff_card_regression_score()

        overviewCard = NormalCard(cardData=[HtmlData("<h4>Overview</h4>")])
        headNode.add_a_card(overviewCard)
        headNode.add_a_card(kpiCard)
        distributionNode = result_setter.get_distribution_node()
        if distributionNode != None:
            headNode.add_cards(distributionNode["listOfCards"])
        if coeffCard != None:
            headNode.add_a_card(coeffCard)
        anovaNarratives = result_setter.get_anova_narratives_scored_data()
        anovaCharts = result_setter.get_anova_charts_scored_data()
        if anovaNarratives != {}:
            anovaHeaderCard = NormalCard(cardData=[HtmlData("<h4>Analysis by Key Factors</h4>")])
            headNode.add_a_card(anovaHeaderCard)
            significantDims = len(anovaNarratives)
            anovaNarrativesArray = list(anovaNarratives.items())
            anovaCardWidth = 100
            if significantDims == 1:
                anovaCardWidth = 100
            elif significantDims % 2 == 0:
                anovaCardWidth = 50
            else:
                anovaCardWidth = 50
                anovaNarrativesArray = anovaNarrativesArray[:-1]

            for k,v in anovaNarrativesArray:
                anovaCard = NormalCard()
                anovaCard.set_card_width(anovaCardWidth)
                chartobj = anovaCharts[k].get_dict_object()
                anovaCard.add_card_data([anovaCharts[k],HtmlData(data=v)])
                headNode.add_a_card(anovaCard)
        headNodeJson = CommonUtils.convert_python_object_to_json(headNode)
        print(headNodeJson)
        response = CommonUtils.save_result_json(jobUrl,headNodeJson)
        # print "Dimension Analysis Completed in", time.time()-st," Seconds"
        print("Model Scoring Completed in ", time.time() - st, " seconds.")





def score_model(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    dataframe_context.set_anova_on_scored_data(True)
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    jobName = dataframe_context.get_job_name()
    ignoreMsg = dataframe_context.get_message_ignore()
    targetLevel = dataframe_context.get_target_level_for_model()
    dataCleansingDict = dataframe_context.get_dataCleansing_info()
    featureEngineeringDict = dataframe_context.get_featureEngginerring_info()
    print("Prediction Started")
    dataframe_context.initialize_ml_model_prediction_weight()
    pandas_flag = dataframe_context._pandas_flag

    st = time.time()
    story_narrative = NarrativesTree()
    story_narrative.set_name("scores")
    result_setter = ResultSetter(dataframe_context)
    model_path = dataframe_context.get_model_path()
    print("model path",model_path)
    result_column = dataframe_context.get_result_column()
    if result_column in df.columns:
        dataframe_helper.remove_null_rows(result_column)
####New Feature Engineering Implementation#############
    # time_before_preprocessing = time.time()
    # if dataCleansingDict['selected']:
    #     data_preprocessing_obj = data_preprocessing.DataPreprocessing(spark, df, dataframe_context, dataframe_helper, metaParserInstance, dataCleansingDict, featureEngineeringDict)
    #     df = data_preprocessing_obj.data_cleansing()
    #
    # if featureEngineeringDict['selected']:
    #     feature_engineering_obj = feature_engineering.FeatureEngineering(spark, df, dataframe_context, dataframe_helper, metaParserInstance, featureEngineeringDict)
    #     df = feature_engineering_obj.feature_engineering()
    #
    # time_after_preprocessing = time.time()
    # time_required_for_preprocessing = time_after_preprocessing - time_before_preprocessing
    # print "Time Required for Data Preprocessing = ", time_required_for_preprocessing

    df = dataframe_helper.get_data_frame()
    df = dataframe_helper.fill_missing_values(df)
    model_slug = model_path
    score_slug = dataframe_context.get_score_path()
    print("score_slug",score_slug)
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_SCORES
    score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
    appid = str(dataframe_context.get_app_id())
    app_type = dataframe_context.get_app_type()
    algorithm_name = dataframe_context.get_algorithm_slug()[0]
    print("algorithm_name",algorithm_name)
    print("score_file_path",score_file_path)
    print("model_slug",model_slug)
    if pandas_flag:
        mlEnvironment = "sklearn"
    else:
        mlEnvironment = "spark"
    scriptWeightDict = dataframe_context.get_ml_model_prediction_weight()
    scriptStages = {
        "preprocessing":{
            "summary":"Dataset Loading Completed",
            "weight":4
            }
        }
    print(scriptWeightDict)
    CommonUtils.create_update_and_save_progress_message(dataframe_context,scriptWeightDict,scriptStages,"initialization","preprocessing","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

    if app_type == "CLASSIFICATION":
        model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
        print("selected_model_for_prediction", selected_model_for_prediction)
        if "randomforest" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = RFClassificationModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            else:
                trainedModel = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark,story_narrative,result_setter,metaParserInstance)
            # trainedModel = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "sparkrandomforest" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"sparkrandomforest",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "xgboost" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = XgboostScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            else:
                trainedModel = XGBoostPysparkScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (Sklearn)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = NeuralNetworkScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "logisticregression" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = LogisticRegressionScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            else:
                trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (TensorFlow)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = TensorFlowScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (TensorFlow)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network (PyTorch)" in selected_model_for_prediction:
            # df = df.toPandas()
            trainedModel = NNPTClassificationScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (PyTorch)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "naive bayes" in selected_model_for_prediction:
            # df = df.toPandas()
            if pandas_flag:
                trainedModel = NBMClassificationModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
                # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
                try:
                    trainedModel.Predict()
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
                    try:
                        trainedModel = NBGClassificationModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
                        trainedModel.Predict()
                    except Exception as e:
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            else:
                trainedModel = NaiveBayesPysparkScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
                try:
                    trainedModel.Predict()
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "LightGBM" in selected_model_for_prediction:
            trainedModel = LgbmScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"LightGBM",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "adaboost" in selected_model_for_prediction:
            trainedModel = AdaboostScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Adaboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        else:
            print("Could Not Load the Model for Scoring")

        # scoreSummary = CommonUtils.convert_python_object_to_json(story_narrative)
        storycards = result_setter.get_score_cards()
        storyNode = NarrativesTree()
        storyNode.add_cards(storycards)
        # storyNode = {"listOfCards":[storycards],"listOfNodes":[],"name":None,"slug":None}
        scoreSummary = CommonUtils.convert_python_object_to_json(storyNode)
        print(scoreSummary)
        jobUrl = dataframe_context.get_job_url()
        response = CommonUtils.save_result_json(jobUrl,scoreSummary)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","mAdvisor Has Successfully Completed Building Machine Learning Models",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print("Model Scoring Completed in ", time.time() - st, " seconds.")
    elif app_type == "REGRESSION":
        model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        dataframe_context.set_story_on_scored_data(True)

        selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
        print("selected_model_for_prediction", selected_model_for_prediction)
        if "linearregression" in  selected_model_for_prediction:
            trainedModel = LinearRegressionModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"linearregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "gbtregression" in  selected_model_for_prediction:
            trainedModel = GBTRegressionModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"gbtregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "dtreeregression" in  selected_model_for_prediction:
            trainedModel = DTREERegressionModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"dtreeregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "rfregression" in  selected_model_for_prediction:
            trainedModel = RFRegressionModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance,mlEnvironment)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"rfregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        if "generalizedlinearregression" in  selected_model_for_prediction:
            trainedModel = GeneralizedLinearRegressionModelScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"generalizedlinearregression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        if "Neural Network (PyTorch)" in  selected_model_for_prediction:
            trainedModel = NNPTRegressionScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Network (PyTorch)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")

        headNode = NarrativesTree()
        if headNode != None:
            headNode.set_name(jobName)
        # headNode["name"] = jobName
        # distributionNode = result_setter.get_distribution_node()
        # if distributionNode != None:
        #     headNode["listOfNodes"].append(distributionNode)
        # anovaNode = result_setter.get_anova_node()
        # if anovaNode != None:
        #     headNode["listOfNodes"].append(anovaNode)
        # decisionTreeNode = result_setter.get_decision_tree_node()
        # if decisionTreeNode != None:
        #     headNode["listOfNodes"].append(decisionTreeNode)

        kpiCard = result_setter.get_kpi_card_regression_score()
        kpiCard = json.loads(CommonUtils.convert_python_object_to_json(kpiCard))

        coeffCard = result_setter.get_coeff_card_regression_score()

        overviewCard = NormalCard(cardData=[HtmlData("<h4>Overview</h4>")])
        headNode.add_a_card(overviewCard)
        headNode.add_a_card(kpiCard)
        distributionNode = result_setter.get_distribution_node()
        if distributionNode != None:
            headNode.add_cards(distributionNode["listOfCards"])
        if coeffCard != None:
            headNode.add_a_card(coeffCard)
        anovaNarratives = result_setter.get_anova_narratives_scored_data()
        anovaCharts = result_setter.get_anova_charts_scored_data()
        if anovaNarratives != {}:
            anovaHeaderCard = NormalCard(cardData=[HtmlData("<h4>Analysis by Key Factors</h4>")])
            headNode.add_a_card(anovaHeaderCard)
            significantDims = len(anovaNarratives)
            anovaNarrativesArray = list(anovaNarratives.items())
            anovaCardWidth = 100
            if significantDims == 1:
                anovaCardWidth = 100
            elif significantDims % 2 == 0:
                anovaCardWidth = 50
            else:
                anovaCardWidth = 50
                anovaNarrativesArray = anovaNarrativesArray[:-1]

            for k,v in anovaNarrativesArray:
                anovaCard = NormalCard()
                anovaCard.set_card_width(anovaCardWidth)
                chartobj = anovaCharts[k].get_dict_object()
                anovaCard.add_card_data([anovaCharts[k],HtmlData(data=v)])
                headNode.add_a_card(anovaCard)

        headNodeJson = CommonUtils.convert_python_object_to_json(headNode)
        print(headNodeJson)
        response = CommonUtils.save_result_json(jobUrl,headNodeJson)
        # print "Dimension Analysis Completed in", time.time()-st," Seconds"
        print("Model Scoring Completed in ", time.time() - st, " seconds.")


def run_metadata(spark,df,dataframe_context):
    fs = time.time()
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    ignoreMsg = dataframe_context.get_message_ignore()
    ## TO DO : remove hard coded pandas flag
    # pandas_flag = True
    # dataframe_context._pandas_flag = pandas_flag
    meta_data_class = MetaDataScript(df,spark,dataframe_context)
    completionStatus = dataframe_context.get_completion_status()
    progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Creating Metadata For The Dataset",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    try:
        meta_data_object = meta_data_class.run()
        metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
        print(metaDataJson)
        print("metaData Analysis Done in ", time.time() - fs, " seconds.")
        response = CommonUtils.save_result_json(jobUrl,metaDataJson)
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Your Data Is Uploaded",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        return response
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"metadata",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

def run_subsetting(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    st = time.time()
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    print("starting subsetting")
    subsetting_class = DataFrameFilterer(df,dataframe_helper,dataframe_context)
    try:
        filtered_df = subsetting_class.applyFilter()
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"filterDf",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
    pandas_flag = dataframe_context._pandas_flag
    try:
        if pandas_flag:
            if len(filtered_df) >0:
                transform_class = DataFrameTransformer(filtered_df, dataframe_helper, dataframe_context,metaParserInstance)
                transform_class.applyTransformations()
                try:
                    update_metadata_datatype_change = transform_class.actual_col_datatype_update
                except:
                    pass
                transformed_df = transform_class.get_transformed_data_frame()
            if len(filtered_df) > 0 and len(transformed_df) > 0:
                output_filepath = dataframe_context.get_output_filepath()
                print("output_filepath", output_filepath)
                try:
                    transformed_df.write.csv(output_filepath, mode="overwrite", header=True)
                except:
                    pass
                    # print("####################could not save the pandas flow dataset in the output path ###################")

                print("starting Metadata for the Filtered Dataframe")
                meta_data_class = MetaDataScript(transformed_df, spark, dataframe_context)
                try:
                    meta_data_class.actual_col_datatype_update = update_metadata_datatype_change
                except:
                    pass
                meta_data_object = meta_data_class.run()
                metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
                print(metaDataJson)
                response = CommonUtils.save_result_json(jobUrl, metaDataJson)
            else:
                response = CommonUtils.save_result_json(jobUrl, {"status": "failed",
                                                                 "message": "Filtered Dataframe has no data"})
            return response
        else:
            if filtered_df.count() > 0:
                transform_class = DataFrameTransformer(filtered_df,dataframe_helper,dataframe_context,metaParserInstance)
                transform_class.applyTransformations()
                try:
                    update_metadata_datatype_change=transform_class.actual_col_datatype_update
                except:
                    pass
                transformed_df = transform_class.get_transformed_data_frame()
            if filtered_df.count() > 0 and transformed_df.count() > 0:
                output_filepath = dataframe_context.get_output_filepath()
                print("output_filepath",output_filepath)
                try:
                    transformed_df.write.csv(output_filepath, mode="overwrite",header=True)
                except:
                    print ("####################could not save the dataset in the output path ###################")

                print("starting Metadata for the Filtered Dataframe")
                meta_data_class = MetaDataScript(transformed_df,spark,dataframe_context)
                try:
                    meta_data_class.actual_col_datatype_update=update_metadata_datatype_change
                except:
                    pass
                meta_data_object = meta_data_class.run()
                metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
                print(metaDataJson)
                response = CommonUtils.save_result_json(jobUrl,metaDataJson)
            else:
                response = CommonUtils.save_result_json(jobUrl,{"status":"failed","message":"Filtered Dataframe has no data"})
            return response
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"transformDf",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print("SubSetting Analysis Completed in", time.time()-st," Seconds")

def run_dimension_analysis(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    targetVal = dataframe_context.get_result_column()
    jobName = dataframe_context.get_job_name()
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    scripts_to_run = dataframe_context.get_analysis_name_list()
    print("scripts_to_run",scripts_to_run)
    measure_columns = dataframe_helper.get_numeric_columns()
    dimension_columns = dataframe_helper.get_string_columns()

    result_setter = ResultSetter(dataframe_context)
    story_narrative = NarrativesTree()
    story_narrative.set_name("{} Performance Report".format(targetVal))
    scriptWeightDict = dataframe_context.get_script_weights()
    print(scriptWeightDict)

    st = time.time()
    print("STARTING DIMENSION ANALYSIS ...")
    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    df = dataframe_helper.get_data_frame()

    if ('Descriptive analysis' in scripts_to_run):
        dataframe_context.set_analysis_name("Descriptive analysis")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing Statistical And Machine Learning Techniques For Analysis",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            freq_obj = FreqDimensionsScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter)
            freq_obj.Run()
            print("Frequency Analysis Done in ", time.time() - fs,  " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Frequency analysis","failedState","error","Descriptive Stats Failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if ((len(dimension_columns)>=2 or len(measure_columns)>=1) and 'Dimension vs. Dimension' in scripts_to_run):
        dataframe_context.set_analysis_name("Dimension vs. Dimension")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Evaluating Variables For Statistical Association",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            chisquare_obj = ChiSquareScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            chisquare_obj.Run()
            print("ChiSquare Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Dimension vs. Dimension",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Dimension vs. Dimension"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Dimension vs. Dimension","failedState","error","Dimension vs. Dimension failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if ('Trend' in scripts_to_run):
        dataframe_context.set_analysis_name("Trend")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Analyzing Trend For {}".format(targetVal),completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            trend_obj = TrendScript(dataframe_helper, dataframe_context, result_setter, spark, story_narrative, metaParserInstance)
            trend_obj.Run()
            print("Trend Analysis Done in ", time.time() - fs, " seconds.")

        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Trend"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend Failed !!!",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if ('Predictive modeling' in scripts_to_run):
        dataframe_context.set_analysis_name("Predictive modeling")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Prediction Model For {}".format(targetVal),completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            dataframe_helper.fill_na_dimension_nulls()
            df = dataframe_helper.get_data_frame()
            decision_tree_obj = DecisionTreeScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            decision_tree_obj.Run()
            print("DecisionTrees Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Predictive modeling"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive Modeling Failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    completionStatus = dataframe_context.get_completion_status()
    progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Validating Analysis Results",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    time.sleep(3)
    progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Visualizations",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    time.sleep(3)
    progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Narratives",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    time.sleep(3)
    dataframe_context.update_completion_status(max(completionStatus,100))

    ordered_node_name_list = ["Overview","Trend","Association","Prediction"]
    # story_narrative.reorder_nodes(ordered_node_name_list)
    dimensionResult = CommonUtils.convert_python_object_to_json(story_narrative)
    headNode = result_setter.get_head_node()

    business_impact_nodes = []
    if headNode != None:
        headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
    headNode["name"] = jobName
    dimensionNode = result_setter.get_distribution_node()
    if dimensionNode != None:
        business_impact_nodes.append("Overview")
        headNode["listOfNodes"].append(dimensionNode)
    trendNode = result_setter.get_trend_node()
    if trendNode != None:
        business_impact_nodes.append("Trend")
        headNode["listOfNodes"].append(trendNode)
    chisquareNode = result_setter.get_chisquare_node()
    if chisquareNode != None:
        business_impact_nodes.append("Association")
        headNode["listOfNodes"].append(chisquareNode)
    decisionTreeNode = result_setter.get_decision_tree_node()
    if decisionTreeNode != None:
        business_impact_nodes.append("Prediction")
        headNode["listOfNodes"].append(decisionTreeNode)

    # Business Impact Card Implementation #
    business_card_calculation = True
    if business_card_calculation:
        try:
            fs = time.time()
            business_card_obj = BusinessCard(headNode, metaParserInstance, result_setter, dataframe_context, dataframe_helper, st, "dimension")
            business_card_obj.Run()
            print("Business Card Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            print("Business Card Calculation failed : ", str(e))
    businessImpactNode = result_setter.get_business_impact_node()
    # print "businessImpactNode : ", json.dumps(businessImpactNode, indent=2)

    if businessImpactNode != None:
        headNode["listOfNodes"].append(businessImpactNode)

    # print json.dumps(headNode,indent=2)
    response = CommonUtils.save_result_json(jobUrl,json.dumps(headNode))
    print("Dimension Analysis Completed in", time.time()-st," Seconds")
    progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Your Signal Is Ready",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

def run_measure_analysis(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    targetVal = dataframe_context.get_result_column()
    jobName = dataframe_context.get_job_name()
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    scripts_to_run = dataframe_context.get_analysis_name_list()
    print("scripts_to_run",scripts_to_run)
    measure_columns = dataframe_helper.get_numeric_columns()
    dimension_columns = dataframe_helper.get_string_columns()

    result_setter = ResultSetter(dataframe_context)
    story_narrative = NarrativesTree()
    story_narrative.set_name("{} Performance Report".format(targetVal))
    scriptWeightDict = dataframe_context.get_script_weights()
    print(scriptWeightDict)


    st = time.time()
    print("STARTING MEASURE ANALYSIS ...")
    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    df = dataframe_helper.get_data_frame()

    #df = df.na.drop(subset=dataframe_context.get_result_column())

    if ('Descriptive analysis' in scripts_to_run):
        dataframe_context.set_analysis_name("Descriptive analysis")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing Statistical And Machine Learning Techniques For Analysis",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            descr_stats_obj = DescriptiveStatsScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative)
            descr_stats_obj.Run()
            print("DescriptiveStats Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Descriptive analysis","failedState","error","Descriptive Stats Failed !!!",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if len(dimension_columns)>0 and 'Measure vs. Dimension' in scripts_to_run:
        dataframe_context.set_analysis_name("Measure vs. Dimension")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Evaluating Variables For Performance Analysis",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            two_way_obj = TwoWayAnovaScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative,metaParserInstance)
            two_way_obj.Run()
            print("OneWayAnova Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Dimension",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Measure vs. Dimension"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Measure vs. Dimension","failedState","error","Anova Failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
        dataframe_context.set_analysis_name("Measure vs. Measure")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Finding Factors That Influence Target Variable",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            correlation_obj = CorrelationScript(df, dataframe_helper, dataframe_context, spark)
            correlations = correlation_obj.Run()
            print("Correlation Analysis Done in ", time.time() - fs ," seconds.")
            try:
                try:
                    df = df.na.drop(subset=measure_columns)
                except:
                    df = df.drop_duplicates()
                fs = time.time()
                regression_obj = LinearRegressionScript(df, dataframe_helper, dataframe_context, result_setter, spark, correlations, story_narrative,metaParserInstance)
                regression_obj.Run()
                print("Regression Analysis Done in ", time.time() - fs, " seconds.")
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"regression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Measure",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Measure vs. Measure"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Measure vs. Measure","failedState","error","Regression Failed !!!",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if ('Trend' in scripts_to_run):
        dataframe_context.set_analysis_name("Trend")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Analyzing Trend For {}".format(targetVal),completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            trend_obj = TrendScript(dataframe_helper,dataframe_context,result_setter,spark,story_narrative, metaParserInstance)
            trend_obj.Run()
            print("Trend Analysis Done in ", time.time() - fs, " seconds.")

        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Trend"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend Failed !!!",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if ('Predictive modeling' in scripts_to_run):
        dataframe_context.set_analysis_name("Predictive modeling")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Prediction Model For {}".format(targetVal),completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            dataframe_helper.fill_na_dimension_nulls()
            df = dataframe_helper.get_data_frame()
            dt_reg = DecisionTreeRegressionScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative,metaParserInstance)
            dt_reg.Run()
            print("DecisionTrees Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Predictive modeling"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive Modeling Failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    # try:
    #     fs = time.time()
    #     exec_obj = ExecutiveSummaryScript(dataframe_helper,dataframe_context,result_setter,spark)
    #     exec_obj.Run()
    #     print "Executive Summary Done in ", time.time() - fs, " seconds."
    # except Exception as e:
    #     CommonUtils.print_errors_and_store_traceback(LOGGER,"Executive Summary",e)

    completionStatus = dataframe_context.get_completion_status()
    progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Validating Analysis Results",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    # time.sleep(3)
    progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Visualizations",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    # time.sleep(3)
    progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Narratives",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    # time.sleep(3)
    dataframe_context.update_completion_status(max(completionStatus,100))

    measureResult = CommonUtils.convert_python_object_to_json(story_narrative)
    headNode = result_setter.get_head_node()
    if headNode != None:
        headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
    headNode["name"] = jobName
    distributionNode = result_setter.get_distribution_node()
    if distributionNode != None:
        headNode["listOfNodes"].append(distributionNode)
    trendNode = result_setter.get_trend_node()
    if trendNode != None:
        headNode["listOfNodes"].append(trendNode)
    anovaNode = result_setter.get_anova_node()
    if anovaNode != None:
        headNode["listOfNodes"].append(anovaNode)
    regressionNode = result_setter.get_regression_node()
    if regressionNode != None:
        headNode["listOfNodes"].append(regressionNode)
    decisionTreeNode = result_setter.get_decision_tree_node()
    if decisionTreeNode != None:
        headNode["listOfNodes"].append(decisionTreeNode)

    # Business Impact Card Implementation #
    business_card_calculation = True
    if business_card_calculation:
        try:
            fs = time.time()
            business_card_obj = BusinessCard(headNode, metaParserInstance, result_setter, dataframe_context, dataframe_helper, st, "measure")
            business_card_obj.Run()
            print("Business Card Analysis Done in ", time.time() - fs, " seconds.")
        except Exception as e:
            print("Business Card Calculation failed : ", str(e))
    businessImpactNode = result_setter.get_business_impact_node()
    # print "businessImpactNode : ", json.dumps(businessImpactNode, indent=2)

    if businessImpactNode != None:
        headNode["listOfNodes"].append(businessImpactNode)


    # print json.dumps(headNode)
    response = CommonUtils.save_result_json(jobUrl,json.dumps(headNode))
    print("Measure Analysis Completed in :", time.time()-st," Seconds")
    progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Your Signal Is Ready",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
