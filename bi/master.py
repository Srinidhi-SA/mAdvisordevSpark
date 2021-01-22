from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from past.builtins import basestring
import sys
import time
import json
import pyhocon
import unittest
import requests
#reload(sys)
#sys.setdefaultencoding('utf-8')

from bi.settings import *
from bi.algorithms import data_preprocessing as data_preprocessing
from bi.algorithms import feature_engineering as feature_engineering
from bi.algorithms.autoML import auto_ml_master as autoML
from bi.algorithms.autoML import auto_ml_score1 as autoMLScore

from bi.common import utils as CommonUtils
from bi.common import DataLoader,MetaParser, DataFrameHelper,ContextSetter,ResultSetter
from bi.common import NarrativesTree,ConfigValidator
from bi.common import scriptStages
from bi.scripts.stockAdvisor.stock_advisor import StockAdvisor
from bi.settings import setting as GLOBALSETTINGS
# from bi.tests.chisquare.test_chisquare import TestChiSquare
from bi.tests.chisquare import TestChiSquare
import bi.master_helper as MasterHelper
from bi.parser import configparser

def main(configJson):
    LOGGER = {}
    deployEnv = False  # running the scripts from job-server env
    debugMode = True   # runnning the scripts for local testing and development
    cfgMode = False    # runnning the scripts by passing config.cfg path
    scriptStartTime = time.time()
    if isinstance(configJson,pyhocon.config_tree.ConfigTree) or isinstance(configJson,dict):
        deployEnv = True
        debugMode = False
        ignoreMsg = False
    elif isinstance(configJson,basestring):
        if configJson.endswith(".cfg"):
            print("||############################## Running in cfgMode ##############################||")
            cfgMode = True
            debugMode = False
            ignoreMsg = False
        else:
            print("||############################## Running in debugMode ##############################||")
            cfgMode = False
            debugMode = True
            ignoreMsg = True
            # Test Configs are defined in bi/settings/configs/localConfigs
            jobType = "story"
            if jobType == "testCase":
                configJson = get_test_configs(jobType,testFor = "chisquare")
            else:
                configJson = get_test_configs(jobType)

    print("||############################## Creating Spark Session ##############################||")
    if debugMode:
        APP_NAME = "mAdvisor_running_in_debug_mode"
    else:
        config = configJson["config"]
        if config is None:
            configJson = requests.get(configJson["job_config"]["config_url"])
            configJson = configJson.json()

        if "job_config" in list(configJson.keys()) and "job_name" in configJson["job_config"]:
            APP_NAME = configJson["job_config"]["job_name"]
        else:
            APP_NAME = "--missing--"
    if debugMode:
        spark = CommonUtils.get_spark_session(app_name=APP_NAME,hive_environment=False)
    else:
        spark = CommonUtils.get_spark_session(app_name=APP_NAME)

    spark.sparkContext.setLogLevel("ERROR")
    # applicationIDspark = spark.sparkContext.applicationId

    # spark.conf.set("spark.sql.execution.arrow.enabled", "true")

    print("||############################## Parsing Config file inside main ##############################||")
    print("-------------------------------******************************", configJson)
    config = configJson["config"]
    print("1111111111111111111111111111111", "TRAINER_MODE" in config and config["TRAINER_MODE"] == "autoML")
    if "TRAINER_MODE" in config and config["TRAINER_MODE"] == "autoML" :
        if "app_type" in config["FILE_SETTINGS"] and config["FILE_SETTINGS"]["app_type"] == "classification":
            if config['FILE_SETTINGS']['inputfile'][0].startswith("https:"):
                config['ALGORITHM_SETTING'] = GLOBALSETTINGS.algorithm_settings_pandas
            else:
                config['ALGORITHM_SETTING'] = GLOBALSETTINGS.algorithm_settings_pyspark
    jobConfig = configJson["job_config"]
    jobType = jobConfig["job_type"]
    if jobType == "prediction":
        one_click = config["one_click"]
    jobName = jobConfig["job_name"]
    jobURL = jobConfig["job_url"]
    messageURL = jobConfig["message_url"]
    initialMessageURL = jobConfig["initial_messages"]
    print("2222222222222222222222222222222222" )
    messages = scriptStages.messages_list(config, jobConfig, jobType, jobName)
    print("3333333333333333333333333333333333333", messages)
    messages_for_API = messages.send_messages()
    print("55555555555555555555555555555555555555",messages_for_API)
    messages_for_API = json.dumps(messages_for_API)
    print("---------------------start ---------------------", messages_for_API)
    print("---------------------Pipeline changes------------------")
    try:
        res = requests.put(url=initialMessageURL,data=messages_for_API)
    except Exception as e:
        print("----------------------Exception----------------------------")
        print(e)
    print("-------------------------------end-------------------------------",res)
    try:
        errorURL = jobConfig["error_reporting_url"]
    except:
        errorURL = None
    if "app_id" in jobConfig:
        appid = jobConfig["app_id"]
    else:
        appid = None
    configJsonObj = configparser.ParserConfig(config)
    configJsonObj.set_json_params()

    dataframe_context = ContextSetter(configJsonObj)
    dataframe_context.set_job_type(jobType)                                     #jobType should be set before set_params call of dataframe_context
    dataframe_context.set_params()
    dataframe_context.set_message_url(messageURL)
    dataframe_context.set_app_id(appid)
    dataframe_context.set_debug_mode(debugMode)
    dataframe_context.set_job_url(jobURL)
    dataframe_context.set_app_name(APP_NAME)
    dataframe_context.set_error_url(errorURL)
    dataframe_context.set_logger(LOGGER)
    dataframe_context.set_xml_url(jobConfig["xml_url"])
    dataframe_context.set_job_name(jobName)


    if debugMode == True:
        dataframe_context.set_environment("debugMode")
        dataframe_context.set_message_ignore(True)

    analysistype = dataframe_context.get_analysis_type()
    result_setter = ResultSetter(dataframe_context)
    appid = dataframe_context.get_app_id()
    completionStatus = 0
    print("||############################## Validating the Config ##############################||")
    configValidator = ConfigValidator(dataframe_context)
    configValid = configValidator.get_sanity_check()

    if not configValid:
        progressMessage = CommonUtils.create_progress_message_object("mAdvisor Job","custom","info","Please Provide A Valid Configuration",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        response = CommonUtils.save_result_json(dataframe_context.get_job_url(),json.dumps({}))
        CommonUtils.save_error_messages(errorURL,APP_NAME,"Invalid Config Provided",ignore=ignoreMsg)
    else:
        ########################## Initializing messages ##############################
        if jobType == "story":
            if analysistype == "measure":
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
            else:
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
            dataframe_context.update_completion_status(completionStatus)
        elif jobType == "metaData":
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Preparing Data For Loading",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Initializing The Loading Process",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Uploading Data",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            dataframe_context.update_completion_status(completionStatus)
        if jobType != "stockAdvisor":
            df = None
            data_loading_st = time.time()
            progressMessage = CommonUtils.create_progress_message_object("scriptInitialization","scriptInitialization","info","Loading The Dataset",completionStatus,completionStatus)
            if jobType != "story" and jobType != "metaData":
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
                dataframe_context.update_completion_status(completionStatus)
            ########################## Load the dataframe ##############################
            df = MasterHelper.load_dataset(spark,dataframe_context)
            ######  pandas Flag  ################
            #dataframe_context._pandas_flag = False
            try:
                df = df.persist()
            except:
                pass
            rowscols = (df.count(), len(df.columns))
            removed_col=[]
            new_cols_added = None
            if jobType != "metaData":
                # df,df_helper = MasterHelper.set_dataframe_helper(df,dataframe_context,metaParserInstance)
                if jobType == "training" or jobType == "prediction":
                    automl_enable = False
                    if dataframe_context.get_trainerMode() == "autoML":
                        automl_enable = True
                    one_click_json = {}
                    if dataframe_context.get_trainerMode() == "autoML":
                        # dataframe_context._pandas_flag = True
                        if jobType == "training":
                            # if dataframe_context._pandas_flag :
                            #     df = df.toPandas()
                            fs = time.time()
                            autoML_obj =  autoML.AutoMl(df, dataframe_context, GLOBALSETTINGS.APPS_ID_MAP[appid]["type"])

                            one_click_json, linear_df, tree_df = autoML_obj.run()
                            print("Automl Done in ", time.time() - fs, " seconds.")
                        elif jobType == "prediction":
                            #try:
                            #    df = df.toPandas()
                            #except:
                            #    pass
                            score_obj =  autoMLScore.Scoring(df, one_click, dataframe_context._pandas_flag)
                            linear_df, tree_df = score_obj.run()
                        # linear
                        print('No. of columns in Linear data :',len(list(linear_df.columns)))
                        #linear_df = spark.createDataFrame(linear_df)
                        metaParserInstance_linear_df = MasterHelper.get_metadata(linear_df,spark,dataframe_context,new_cols_added)
                        linear_df,df_helper_linear_df = MasterHelper.set_dataframe_helper(linear_df,dataframe_context,metaParserInstance_linear_df)
                        dataTypeChangeCols_linear_df= dataframe_context.get_change_datatype_details()
                        colsToBin_linear_df = df_helper_linear_df.get_cols_to_bin()
                        updateLevelCountCols_linear_df = colsToBin_linear_df
                        try:
                            for i in dataTypeChangeCols_linear_df:
                                if i["columnType"]=="dimension" and i['colName'] in list(linear_df.columns):
                                    updateLevelCountCols_linear_df.append(i["colName"])
                        except:
                            pass
                        levelCountDict_linear_df = df_helper_linear_df.get_level_counts(updateLevelCountCols_linear_df)
                        metaParserInstance_linear_df.update_level_counts(updateLevelCountCols_linear_df,levelCountDict_linear_df)

                        # Tree
                        print('No. of columns in Tree data :',len(list(tree_df.columns)))
                        #tree_df = spark.createDataFrame(tree_df)
                        metaParserInstance_tree_df = MasterHelper.get_metadata(tree_df,spark,dataframe_context,new_cols_added)
                        tree_df,df_helper_tree_df = MasterHelper.set_dataframe_helper(tree_df,dataframe_context,metaParserInstance_tree_df)
                        dataTypeChangeCols_tree_df = dataframe_context.get_change_datatype_details()
                        colsToBin_tree_df = df_helper_tree_df.get_cols_to_bin()
                        updateLevelCountCols_tree_df = colsToBin_tree_df
                        try:
                            for i in dataTypeChangeCols_tree_df:
                                if i["columnType"]=="dimension" and i['colName'] in list(tree_df.columns):
                                    updateLevelCountCols_tree_df.append(i["colName"])
                        except:
                            pass
                        levelCountDict_tree_df = df_helper_tree_df.get_level_counts(updateLevelCountCols_tree_df)
                        metaParserInstance_tree_df.update_level_counts(updateLevelCountCols_tree_df,levelCountDict_tree_df)
                    else:
                        dataCleansingDict = dataframe_context.get_dataCleansing_info()
                        featureEngineeringDict = dataframe_context.get_featureEngginerring_info()
                        if dataCleansingDict['selected'] or featureEngineeringDict['selected']:
                            old_cols_list = df.columns
                            completionStatus = 10
                            progressMessage = CommonUtils.create_progress_message_object("scriptInitialization","scriptInitialization","info","Performing Required Data Preprocessing And Feature Transformation Tasks",completionStatus,completionStatus)
                            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
                            dataframe_context.update_completion_status(completionStatus)
                            ## TO DO : Change flag later this is only for testing
                            pandas_flag = dataframe_context._pandas_flag
                            if pandas_flag :
                                try:
                                    df = df.toPandas()
                                except:
                                    pass
                            if dataCleansingDict['selected']:
                                data_preprocessing_obj = data_preprocessing.DataPreprocessing(spark, df, dataCleansingDict, dataframe_context)
                                df = data_preprocessing_obj.data_cleansing()
                                removed_col=data_preprocessing_obj.removed_col
                            dataframe_context.set_ignore_column_suggestions(removed_col)

                            if featureEngineeringDict['selected']:
                                feature_engineering_obj = feature_engineering.FeatureEngineering(spark, df,  featureEngineeringDict, dataframe_context)
                                feature_engineering_obj.consider_columns =dataframe_context.get_consider_columns()
                                df = feature_engineering_obj.feature_engineering()
                            new_cols_list = df.columns
                            old_cols_list = list(set(old_cols_list) - set(removed_col))
                            if len(old_cols_list) < len(new_cols_list):
                                new_cols_added = list(set(new_cols_list) - set(old_cols_list))
                            else:
                                 new_cols_added = None
                            # if pandas_flag:
                            #     ## TODO: has to be removed now that metadata and DFhelper are in pandas
                            #     df=spark.createDataFrame(df)
                            try:
                                print(df.printSchema())
                            except:
                                print(df.dtypes)

                        metaParserInstance = MasterHelper.get_metadata(df,spark,dataframe_context,new_cols_added)
                        df,df_helper = MasterHelper.set_dataframe_helper(df,dataframe_context,metaParserInstance)
                        # updating metaData for binned Cols
                        dataTypeChangeCols=dataframe_context.get_change_datatype_details()
                        colsToBin = df_helper.get_cols_to_bin()
                        updateLevelCountCols=colsToBin
                        try:
                            for i in dataTypeChangeCols:
                                if i["columnType"]=="dimension":
                                    if  jobType != "prediction":
                                        updateLevelCountCols.append(i["colName"])
                                    elif i["colName"] != self.dataframe_context.get_result_column() and jobType == "prediction":#in prediction we should not add target
                                        updateLevelCountCols.append(i["colName"])
                        except:
                            pass
                        levelCountDict = df_helper.get_level_counts(updateLevelCountCols)
                        metaParserInstance.update_level_counts(updateLevelCountCols,levelCountDict)

                else:
                    metaParserInstance = MasterHelper.get_metadata(df,spark,dataframe_context,new_cols_added)
                    df,df_helper = MasterHelper.set_dataframe_helper(df,dataframe_context,metaParserInstance)
                    # updating metaData for binned Cols
                    dataTypeChangeCols=dataframe_context.get_change_datatype_details()
                    colsToBin = df_helper.get_cols_to_bin()
                    updateLevelCountCols=colsToBin
                    try:
                        for i in dataTypeChangeCols:
                            if i["columnType"]=="dimension":
                                updateLevelCountCols.append(i["colName"])
                    except:
                        pass
                    levelCountDict = df_helper.get_level_counts(updateLevelCountCols)
                    metaParserInstance.update_level_counts(updateLevelCountCols,levelCountDict)
        ############################ MetaData Calculation ##########################

        if jobType == "metaData":
            MasterHelper.run_metadata(spark,df,dataframe_context)
        ############################################################################

        ################################ Data Sub Setting ##########################
        if jobType == "subSetting":
            MasterHelper.run_subsetting(spark,df,dataframe_context,df_helper,metaParserInstance)
        ############################################################################

        ################################ Story Creation ############################
        if jobType == "story":
            if analysistype == "dimension":
                MasterHelper.run_dimension_analysis(spark,df,dataframe_context,df_helper,metaParserInstance)
            elif analysistype == "measure":
                MasterHelper.run_measure_analysis(spark,df,dataframe_context,df_helper,metaParserInstance)

            progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        ############################################################################

        ################################ Model Training ############################
        elif jobType == 'training':
            # dataframe_context.set_ml_environment("sklearn")
            if automl_enable is True:
                MasterHelper.train_models_automl(spark,linear_df,tree_df,dataframe_context,df_helper_linear_df,df_helper_tree_df,metaParserInstance_linear_df,metaParserInstance_tree_df,one_click_json)
            else:
                MasterHelper.train_models(spark,df,dataframe_context,df_helper,metaParserInstance,one_click_json)
        ############################################################################

        ############################## Model Prediction ############################
        elif jobType == 'prediction':
            if automl_enable is True:
                MasterHelper.score_model_autoML(spark,linear_df,tree_df,dataframe_context,df_helper_linear_df,df_helper_tree_df,metaParserInstance_linear_df,metaParserInstance_tree_df)
            else:
                # dataframe_context.set_ml_environment("sklearn")
                MasterHelper.score_model(spark,df,dataframe_context,df_helper,metaParserInstance)

        ############################################################################
        ################################### Test Cases  ############################

        if jobType == "testCase":
            print("Running Test Case for Chi-square Analysis---------------")
            # TestChiSquare().setUp()
            unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestChiSquare))

            # TestChiSquare(df,df_helper,dataframe_context,metaParserInstance).run_chisquare_test()
            # TestChiSquare().setup()
            # TestChiSquare().run_chisquare_test()
            # TestChiSquare().test_upper()
            # test = test_chisquare.run_chisquare_test(df,df_helper,dataframe_context,metaParserInstance)
            # suit = unittest.TestLoader().loadTestsFromTestCase(TestChiSquare)

        ############################################################################


        ################################### Stock ADVISOR ##########################
        if jobType == 'stockAdvisor':
            # spark.conf.set("spark.sql.execution.arrow.enabled", "false")
            file_names = dataframe_context.get_stock_symbol_list()
            stockObj = StockAdvisor(spark, file_names,dataframe_context,result_setter)
            stockAdvisorData = stockObj.Run()
            stockAdvisorDataJson = CommonUtils.convert_python_object_to_json(stockAdvisorData)
            # stockAdvisorDataJson["name"] = jobName
            print("*"*100)
            print("Result : ", stockAdvisorDataJson)
            response = CommonUtils.save_result_json(jobURL,stockAdvisorDataJson)

        ############################################################################
        scriptEndTime = time.time()
        runtimeDict = {"startTime":scriptStartTime,"endTime":scriptEndTime}
        print(runtimeDict)
        CommonUtils.save_error_messages(errorURL,"jobRuntime",runtimeDict,ignore=ignoreMsg)
        print("Scripts Time : ", scriptEndTime - scriptStartTime, " seconds.")
        #spark.stop()


def killer_setting(configJson):
    LOGGER = {}
    deployEnv = False  # running the scripts from job-server env
    debugMode = True   # runnning the scripts for local testing and development
    cfgMode = False    # runnning the scripts by passing config.cfg path
    scriptStartTime = time.time()
    if isinstance(configJson,pyhocon.config_tree.ConfigTree) or isinstance(configJson,dict):
        deployEnv = True
        debugMode = False
        ignoreMsg = False
    elif isinstance(configJson,basestring):
        jobType = "training"
        if jobType == "testCase":
            configJson = get_test_configs(jobType,testFor = "chisquare")
        else:
            configJson = get_test_configs(jobType)

    print("||############################## Parsing Config File killer_setting ##############################||")
    print("-------------------------------", configJson)

    config = configJson["config"]
    jobConfig = configJson["job_config"]
    jobName = jobConfig["job_name"]
    jobURL = jobConfig["job_url"]
    killURL = jobConfig["kill_url"]
    messageURL = jobConfig["message_url"]

    return jobURL, killURL, messageURL


def send_kill_command(url, jsonData):
    res = requests.put(url=url,data=jsonData)
    return res

def submit_job_through_yarn():
    # print sys.argv
    # print json.loads(sys.argv[1])
    json_config = json.loads(sys.argv[1])
    # json_config["config"] = ""
    configJson = json_config["job_config"]
    config = configJson["config"]
    jobConfig = configJson["job_config"]
    jobType = jobConfig["job_type"]
    jobName = jobConfig["job_name"]
    jobURL = jobConfig["job_url"]
    messageURL = jobConfig["message_url"]
    killURL = jobConfig["kill_url"]
    #try:
    main(json_config["job_config"])
    # except Exception as e:
    #     # print jobURL, killURL
    #     data = {"status": "killed", "jobURL": jobURL}
    #     resp = send_kill_command(killURL, data)
    #     while str(resp.text) != '{"result": "success"}':
    #         data = {"status": "killed", "jobURL": jobURL}
    #         resp = send_kill_command(killURL, data)
    #     # print resp.text
    #     print('Main Method Did Not End ....., ', str(e))
    #     progressMessage = CommonUtils.create_progress_message_object("Main Method Did Not End .....",
    #                                                                  "Main Method Did Not End .....",
    #                                                                  "Error",
    #                                                                  str(e),
    #                                                                  "Failed", 100)
    #     CommonUtils.save_progress_message(messageURL, progressMessage, emptyBin=True)

if __name__ == '__main__':
    jobURL, killURL, messageURL = killer_setting(sys.argv[1])
    #try:
    main(sys.argv[1])
    print('Main Method End .....')
    # except Exception as e:
    #      print (jobURL, killURL)
    #      data = {"status": "killed", "jobURL": jobURL}
    #      resp = send_kill_command(killURL, data)
    #      while str(resp.text) != '{"result": "success"}':
    #          data = {"status": "killed", "jobURL": jobURL}
    #          resp = send_kill_command(killURL, data)
    #      progressMessage = CommonUtils.create_progress_message_object("Main Method Did Not End .....", "Main Method Did Not End .....",
    #                                                                   "Error",
    #                                                                   str(e),
    #                                                                   "Failed", 100)
    #      CommonUtils.save_progress_message(messageURL, progressMessage, emptyBin=True)

    #      print('Main Method Did Not End ....., ', str(e))
