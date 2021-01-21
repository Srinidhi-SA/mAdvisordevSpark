import os
import sys
import json
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.Sampling import Sampling
from bi.algorithms.autoML.feature_selection import FeatureSelection
import pandas as pd
import re
from bi.common import utils as CommonUtils


class AutoMl:

    def __init__(self, df, dataframe_context, app_type):

        # self.config = config
        # self.data_path = data_path
        self.df = df
        self.target = dataframe_context.get_result_column()
        self.app_type = app_type
        self.final_json = {}
        self.tree_df = None
        self.linear_df = None
        self.LOGGER = dataframe_context.get_logger()
        self.errorURL = dataframe_context.get_error_url()
        self.ignoreMsg = dataframe_context.get_message_ignore()

    def run(self):
        """DATA VALIDATION"""

        # path = self.df
        # obj =  Data_Validation(path,target =self.target,method = self.app_type)
        try:
            data_validation_auto_obj = DataValidation(self.df,self.target,self.app_type)
            data_validation_auto_obj.data_validation_run()

            # print(obj.df.head())
            # print(obj.data_dict.keys())

            # data_dict = data_validation_auto_obj.data_dict
            # Dataframe = data_validation_auto_obj.df
            print("DATA VALIDATION", '\n')
            #         print(Dataframe.info())
            print("#" * 50)

            # self.target = obj.data_dict["target"]
            data_validation_auto_obj.data_change_dict["target"] = self.target
            if not data_validation_auto_obj.data_change_dict["target_fitness_check"]:
                sys.exit()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "datavalidation", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        """DATA PREPROCESSING"""

        # this line used before # data_preprocessing_auto_obj =   Data_Preprocessing(data_dict)
        # Dataframe,data_dict  = data_preprocessing_auto_obj.main(Dataframe)
        try:
            data_preprocessing_auto_obj = DataPreprocessingAutoML(data_validation_auto_obj.data_frame,data_validation_auto_obj.target,data_validation_auto_obj.data_change_dict,data_validation_auto_obj.numeric_cols,
                                                                 data_validation_auto_obj.dimension_cols,data_validation_auto_obj.datetime_cols, data_validation_auto_obj.problem_type)
            data_dict = data_preprocessing_auto_obj.data_preprocessing_run()
            print("DATA PREPROCESSING", '\n')
            #         print(Dataframe.info())
            print("#" * 50)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "dataPreprocessing", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        # print(obj1.df1.head())
        # print(obj1.data_dict1.keys())

        #         data_dict = obj1.data_dict1
        #         Dataframe = obj1.df1
        #         print(Dataframe.info())

        # f = open("dict1.txt","w")
        # f.write( str(data_dict) )
        # f.close()
        ########################################################################################
        """Feature Engineering"""
        try:
            feature_engineering_auto_obj = FeatureEngineeringAutoML(data_preprocessing_auto_obj.data_frame,data_preprocessing_auto_obj.target,data_preprocessing_auto_obj.data_change_dict,data_preprocessing_auto_obj.numeric_cols,data_preprocessing_auto_obj.dimension_cols,data_preprocessing_auto_obj.datetime_cols,data_preprocessing_auto_obj.problem_type)
            feature_engineering_auto_obj.feature_engineering_run()

            mr_df1 = feature_engineering_auto_obj.data_frame

            date_col = feature_engineering_auto_obj.datetime_cols
            cols = list(set(mr_df1) - set(date_col))
            mr_df1 = mr_df1[cols]
            print("Feature Engineering", '\n')
            print("#" * 50)
            print("#" * 50)
            print("Target in AutoML: ", self.target, feature_engineering_auto_obj.data_change_dict["target_fitness_check"])
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Engineering", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        try:
            data_validation_auto_obj2 = DataValidation(feature_engineering_auto_obj.data_frame, self.target,
                                                       self.app_type)
            data_validation_auto_obj2.data_validation_run()


            print("DATA VALIDATION pass2", '\n')
            #         print(Dataframe3.info())
            print("#" * 50)

        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "DATA VALIDATION pass2", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        try:
            data_preprocessing_auto_obj2 = DataPreprocessingAutoML(data_validation_auto_obj2.data_frame,data_validation_auto_obj2.target,data_validation_auto_obj2.data_change_dict,data_validation_auto_obj2.numeric_cols,
                                                                 data_validation_auto_obj2.dimension_cols,data_validation_auto_obj2.datetime_cols, data_validation_auto_obj2.problem_type)
            # Dataframe,data_dict  = obj4.fe_main(Dataframe3)
            data_dict = data_preprocessing_auto_obj2.data_preprocessing_run()
            ### mr_df2,data_dict  = data_preprocessing_auto_obj2.fe_main(data_validation_auto_obj2.df,data_validation_auto_obj2.data_dict)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Data_Preprocessing pass2", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        print("Data_Preprocessing pass2", '\n')

        try:
            data_preprocessing_auto_obj2.data_frame.drop([self.target], axis=1, inplace=True)

            result = pd.merge(mr_df1, data_preprocessing_auto_obj2.data_frame)
            result.drop_duplicates(inplace=True)
            print(result.info())
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "merging of dataframes automl", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        # result.to_csv("for_sampling.csv")

        """ Sampling """
        try:
            sampling_obj = Sampling(result, self.target)
            sampling_obj.over_sampling()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "sampling automl", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        # result = sampling_obj.dataset

        #         print(sum(list(result.isna().sum().values)),"NULLL VALUE")

        """ Feature Selection """

        ### feature_selection_obj = FeatureSelection(result,fdata_dict1,data_dict)
        try:
            feature_selection_obj = FeatureSelection(sampling_obj.dataset,data_validation_auto_obj2.target,feature_engineering_auto_obj.data_change_dict,
                                                     data_validation_auto_obj2.numeric_cols,data_validation_auto_obj2.dimension_cols,data_validation_auto_obj2.datetime_cols, data_validation_auto_obj2.problem_type)

            linear_df_cols=feature_selection_obj.feat_importance_linear()
            linear_df=sampling_obj.dataset[linear_df_cols]
            tree_df_cols = feature_selection_obj.feat_importance_tree()
            tree_df=sampling_obj.dataset[tree_df_cols]
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "FEATURE SELECTION AUTOML", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)

        self.final_json = feature_selection_obj.data_change_dict
        self.linear_df = linear_df
        self.tree_df = tree_df

    def return_values(self):
        return self.final_json, self.linear_df, self.tree_df
        # print(obj6.info,'\n')
