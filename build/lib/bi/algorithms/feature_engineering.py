from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from .feature_engineering_helper import FeatureEngineeringHelper
from .feature_engineering_pandas_helper import FeatureEngineeringHelperPandas
import re


class FeatureEngineering(object):

    def __init__(self, spark, df,  featureEngineeringDict,  dataframe_context):
        self._spark = spark
        self._df = df
        self._dataframe_context = dataframe_context
        ## TO DO : this flag will be taken from dataframe context later.
        self._pandas_flag = dataframe_context._pandas_flag 
        # self._dataframe_helper = dataframe_helper
        # self._metaParserInstance = metaParserInstance
        self._featureEngineeringDict = featureEngineeringDict


    def feature_engineering(self):
        print("Performing Feature Engineering Operations")
        if self._pandas_flag == True:
            feature_engineering_helper_obj = FeatureEngineeringHelperPandas(self._df, self._dataframe_context)
        else :
            feature_engineering_helper_obj = FeatureEngineeringHelper(self._df, self._dataframe_context)
        feature_engineering_helper_obj.consider_columns=self.consider_columns
        columns_to_be_considered_for_binning=self.consider_columns
        for settings in self._featureEngineeringDict['overall_settings']:
            if settings['name'] == "binning_all_measures" and settings['selected'] == True:
                self._df = feature_engineering_helper_obj.binning_all_measures(settings['number_of_bins'],columns_to_be_considered_for_binning)

        for key in list(self._featureEngineeringDict['column_wise_settings'].keys()):
            if self._featureEngineeringDict['column_wise_settings'][key]['selected']:
                if self._featureEngineeringDict['column_wise_settings'][key]['name'] == "creating_new_bins_or_levels":
                    for operation in self._featureEngineeringDict['column_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'create_equal_sized_bins':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_equal_sized_measure_bins(column["name"], column["number_of_bins"])
                            if operation['name'] == 'create_custom_bins':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_custom_measure_bins(column["name"], column["list_of_intervals"])
                            if operation['name'] == 'create_new_levels':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_new_levels_dimension(column["name"], column["mapping_dict"])
                            if operation['name'] == 'create_new_datetime_levels':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_new_levels_datetimes(column["name"], column["mapping_dict"])

                if self._featureEngineeringDict['column_wise_settings'][key]['name'] == "transformation_settings":
                    for operation in self._featureEngineeringDict['column_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'replace_values_with':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.replace_values_in_column(column["name"], column["replace_value"], column["replace_by"])
                            if operation['name'] == 'variable_transformation':
                                for column in operation['columns']:
                                    if column["transformation_type"] == "log_transform":
                                        self._df = feature_engineering_helper_obj.logTransform_column(column["name"])
                                    if column["transformation_type"] == "modulus_transform":
                                        self._df = feature_engineering_helper_obj.modulus_transform_column(column["name"])
                                    if column["transformation_type"] == "cube_root_transform":
                                        self._df = feature_engineering_helper_obj.cuberoot_transform_column(column["name"])
                                    if column["transformation_type"] == "square_root_transform":
                                        self._df = feature_engineering_helper_obj.squareroot_transform_column(column["name"])
                            col = []
                            if operation['name'] == 'encoding_dimensions':
                                for column in operation['columns']:
                                    if column["encoding_type"] == "label_encoding":
                                        self._df = feature_engineering_helper_obj.label_encoding_column(column["name"])
                                        col.append(column["name"])
                                    if column["encoding_type"] == "one_hot_encoding":
                                        self._df = feature_engineering_helper_obj.onehot_encoding_column(column["name"])
                                        col.append(column["name"])
                                try:
                                    self._df = self._df.drop([*col],axis=1)
                                except:
                                    self._df = self._df.drop(*col)
                            if operation['name'] == 'return_character_count':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.character_count_string(column["name"])
                            if operation['name'] == 'is_custom_string_in':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.contains_word(column["name"], column["user_given_string"])
                            if operation['name'] == 'is_date_weekend':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.is_weekend(column["name"])
                            if operation['name'] == 'extract_time_feature':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.extract_datetime_info(column["name"], column["time_feature_to_extract"])
                            if operation['name'] == 'time_since':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.count_time_since(column["name"], column["time_since"])
                            if operation['name'] == 'perform_standardization':
                                for column in operation['columns']:
                                    if column["standardization_type"] == "standardization":
                                        self._df = feature_engineering_helper_obj.standardize_column(column["name"])
                                for column in operation['columns']:
                                    if column["standardization_type"] == "normalization":
                                        self._df = feature_engineering_helper_obj.normalize_column(column["name"])
        if not self._pandas_flag:
            cols = [re.sub('\W+','_', col.strip()) for col in self._df.columns]
            self._df = self._df.toDF(*cols)
        print("Feature Engineering Operations successfully Performed")
        return self._df
