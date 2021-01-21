from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from .data_preprocessing_helper import DataPreprocessingHelper
from .data_preprocessing_helper_pandas import DataPreprocessingHelperPandas


class DataPreprocessing(object):

    def __init__(self,spark,df,dataCleansingDict,dataframe_context):
        self._spark = spark
        self._df = df
        self._dataframe_context = dataframe_context
        self._pandas_flag = dataframe_context._pandas_flag
        # self._dataframe_helper = dataframe_helper
        # self._metaParserInstance = metaParserInstance
        self._dataCleansingDict = dataCleansingDict
        # self._featureEngineeringDict = featureEngineeringDict

    def data_cleansing(self):
        print("Cleaning The Data")
        if self._pandas_flag == True:
            data_preprocessing_helper_obj = DataPreprocessingHelperPandas(self._df, self._dataframe_context)
        else:
            data_preprocessing_helper_obj = DataPreprocessingHelper(self._df, self._dataframe_context)

        for settings in self._dataCleansingDict['overall_settings']:
            if settings['name'] == "duplicate_row" and settings['selected'] == True:
                self._df = data_preprocessing_helper_obj.drop_duplicate_rows()
            if settings['name'] == "duplicate_column" and settings['selected'] == True:
                self._df = data_preprocessing_helper_obj.drop_duplicate_cols()

        data_preprocessing_helper_obj.get_removed_columns()
        self.removed_col=data_preprocessing_helper_obj.removed_col

        for key in list(self._dataCleansingDict['columns_wise_settings'].keys()):
            if self._dataCleansingDict['columns_wise_settings'][key]['selected']:
                if self._dataCleansingDict['columns_wise_settings'][key]['name'] == "missing_value_treatment":
                    for operation in self._dataCleansingDict['columns_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'remove_observations':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.remove_missing_values(column["name"])
                            if operation['name'] == 'mean_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mean_impute_missing_values(column["name"])
                            if operation['name'] == 'median_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.median_impute_missing_values(column["name"])
                            if operation['name'] == 'mode_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mode_impute_missing_values(column["name"])
                            if operation['name'] == 'user_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.user_impute_missing_values(column["name"], column["mvt_value"])


                    #call respective function
                if self._dataCleansingDict['columns_wise_settings'][key]['name'] == "outlier_treatment":
                    for operation in self._dataCleansingDict['columns_wise_settings'][key]['operations']:
                        if operation['selected']:
                            # if operation['name'] == 'remove_outliers':
                            #     for column in operation['columns']:
                            #         self._df = data_preprocessing_helper_obj.remove_outliers(column["name"])
                            if operation['name'] == 'cap_outliers':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.cap_outliers(column["name"])
                            if operation['name'] == 'replace_with_mean':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mean_impute_outliers(column["name"])
                            if operation['name'] == 'replace_with_median':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.median_impute_outliers(column["name"])
                            if operation['name'] == 'replace_with_mode':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mode_impute_outliers(column["name"])

        print("Data Cleaning Completed")
        return self._df
