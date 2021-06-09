import pandas as pd
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection
import time as time
import time
import json
import sys
from bi.common import utils as CommonUtils

class AutoMl:

    def __init__(self, df, dataframe_context, app_type):
        print ("Auto ML train Running "*10)

        self.df = df
        self.target = dataframe_context.get_result_column()
        self.app_type = app_type
        self.final_json = {}
        self.tree_df = None
        self.linear_df = None
        self.LOGGER = dataframe_context.get_logger()
        self.errorURL = dataframe_context.get_error_url()
        self.ignoreMsg = dataframe_context.get_message_ignore()
        self._pandas_flag = dataframe_context._pandas_flag
    def run(self):
        try:
            val_start_time = time.time()
            DataValidation_obj = DataValidation(self.df, self.target, self.app_type, self._pandas_flag)
            DataValidation_obj.data_validation_run()
            print("time taken to data validation:{} seconds".format((time.time()-val_start_time)))
            if not DataValidation_obj.data_change_dict["target_fitness_check"]:
                raise ValueError("Target not suitable for "+ str(self.app_type) + " analysis")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "datavalidation", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
            if str(e) == "Target not suitable for "+ str(self.app_type) + " analysis":
                raise ValueError("Target not suitable for "+ str(self.app_type) + " analysis")
        try:
            pre_start_time=time.time()
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(DataValidation_obj.data_frame, DataValidation_obj.target, DataValidation_obj.data_change_dict, DataValidation_obj.numeric_cols, DataValidation_obj.dimension_cols, DataValidation_obj.datetime_cols,DataValidation_obj.problem_type,self._pandas_flag)
            DataPreprocessingAutoML_obj.data_preprocessing_run()
            print("time taken to data Preprocessing:{} seconds".format((time.time()-pre_start_time)))
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "dataPreprocessing", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            fe_start_time = time.time()
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(DataPreprocessingAutoML_obj.data_frame, DataPreprocessingAutoML_obj.target, DataPreprocessingAutoML_obj.data_change_dict, DataPreprocessingAutoML_obj.numeric_cols, DataPreprocessingAutoML_obj.dimension_cols, DataPreprocessingAutoML_obj.datetime_cols, DataPreprocessingAutoML_obj.problem_type,self._pandas_flag)
            FeatureEngineeringAutoML_obj.feature_engineering_run()
            print("time taken to feature engineering:{} seconds".format((time.time()-fe_start_time)))
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Engineering", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            fs_start_time = time.time()
            FeatureSelection_obj = FeatureSelection(FeatureEngineeringAutoML_obj.data_frame, FeatureEngineeringAutoML_obj.target, FeatureEngineeringAutoML_obj.data_change_dict, FeatureEngineeringAutoML_obj.numeric_cols, FeatureEngineeringAutoML_obj.dimension_cols, FeatureEngineeringAutoML_obj.datetime_cols, FeatureEngineeringAutoML_obj.problem_type,self._pandas_flag)
            if not self._pandas_flag:
                tree_start_time = time.time()
                cols_considered_tree = FeatureSelection_obj.feature_imp_pyspark()
                print("time taken to Tree Based Feature Selection:{} seconds".format((time.time()-tree_start_time)))
            else:
                cols_considered_tree = FeatureSelection_obj.feat_importance_tree()
            linear_start_time = time.time()
            cols_considered_linear = FeatureSelection_obj.feat_importance_linear()
            print("time taken to Linear Based Feature Selection:{} seconds".format((time.time()-linear_start_time)))
            print("time taken to Feature Selection:{} seconds".format((time.time()-fs_start_time)))
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Selection", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        self.df = FeatureEngineeringAutoML_obj.data_frame
        #cols_considered_tree  = cols_considered_linear
        if self._pandas_flag:
            if len(cols_considered_linear) == 1:
                self.linear_df = self.df[cols_considered_tree]
            else:
                self.linear_df = self.df[cols_considered_linear]
            self.tree_df=self.df[cols_considered_tree]
        else:
            if len(cols_considered_linear) == 1:
                self.linear_df = self.df.select(*[cols_considered_tree])
            else:
                self.linear_df = self.df.select(*[cols_considered_linear])
            self.tree_df=self.df.select(*[cols_considered_tree])
        self.final_json = FeatureSelection_obj.data_change_dict
        if self._pandas_flag:
            self.final_json["SelectedColsLinear"] = self.linear_df.columns.tolist()
        else:
            self.final_json["SelectedColsLinear"] = self.linear_df.columns
        print(self.final_json["SelectedColsLinear"])
        self.final_json["target"] = FeatureEngineeringAutoML_obj.target
        return self.final_json, self.linear_df, self.tree_df
