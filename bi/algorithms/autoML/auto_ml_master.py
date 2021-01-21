import pandas as pd
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection
import time as time
import json
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
            DataValidation_obj = DataValidation(self.df, self.target, self.app_type, self._pandas_flag)
            DataValidation_obj.data_validation_run()
            if not DataValidation_obj.data_change_dict["target_fitness_check"]:
                raise ValueError("Target not suitable for "+ str(self.app_type) + " analysis")
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "datavalidation", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
            if str(e) == "Target not suitable for "+ str(self.app_type) + " analysis":
                raise ValueError("Target not suitable for "+ str(self.app_type) + " analysis")
        try:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(DataValidation_obj.data_frame, DataValidation_obj.target, DataValidation_obj.data_change_dict, DataValidation_obj.numeric_cols, DataValidation_obj.dimension_cols, DataValidation_obj.datetime_cols,DataValidation_obj.problem_type,self._pandas_flag)
            DataPreprocessingAutoML_obj.data_preprocessing_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "dataPreprocessing", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(DataPreprocessingAutoML_obj.data_frame, DataPreprocessingAutoML_obj.target, DataPreprocessingAutoML_obj.data_change_dict, DataPreprocessingAutoML_obj.numeric_cols, DataPreprocessingAutoML_obj.dimension_cols, DataPreprocessingAutoML_obj.datetime_cols, DataPreprocessingAutoML_obj.problem_type,self._pandas_flag)
            FeatureEngineeringAutoML_obj.feature_engineering_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Engineering", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            FeatureSelection_obj = FeatureSelection(FeatureEngineeringAutoML_obj.data_frame, FeatureEngineeringAutoML_obj.target, FeatureEngineeringAutoML_obj.data_change_dict, FeatureEngineeringAutoML_obj.numeric_cols, FeatureEngineeringAutoML_obj.dimension_cols, FeatureEngineeringAutoML_obj.datetime_cols, FeatureEngineeringAutoML_obj.problem_type,self._pandas_flag)
            if not self._pandas_flag:
                cols_considered_tree = FeatureSelection_obj.feature_imp_pyspark()
            else:
                cols_considered_tree = FeatureSelection_obj.feat_importance_tree()
            cols_considered_linear = FeatureSelection_obj.feat_importance_linear()
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
