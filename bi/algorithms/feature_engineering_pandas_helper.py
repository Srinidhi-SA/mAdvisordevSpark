from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import numpy as np
import math
from datetime import datetime
from scipy import linspace
from bi.common.column import ColumnType
from bi.common import MetaDataHelper
from bi.settings import setting as GLOBALSETTINGS

from .data_preprocessing_helper_pandas import DataPreprocessingHelperPandas
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder as OneHotEncoder_pandas
import pandas as pd


class FeatureEngineeringHelperPandas(object):
    """Contains Feature Engineering Operation Functions"""

    def __init__(self, df, dataframe_context):
        self._data_frame = df
        self._metaHelperInstance = MetaDataHelper(self._data_frame, self._data_frame.shape[0])
        self._dataframe_context = dataframe_context

        # self._dataframe_helper = dataframe_helper

    def binning_all_measures(self, number_of_bins, consider_cols):
        numeric_columns = []
        cols_to_be_binned = [x[:-4] for x in consider_cols if x[-4:] == "_bin"]
        numeric_columns = [col for col in self._data_frame.columns if
                           self._data_frame[col].dtypes in ['int32', 'int64', 'float32', 'float64', 'int', 'float']]
        for column_name in numeric_columns and cols_to_be_binned:
            self._data_frame = self.create_equal_sized_measure_bins(column_name, number_of_bins)
        return self._data_frame

    def check_key(self, x, bin_label):
        if x is not None:
            for key in list(bin_label.keys()):
                if x >= bin_label[key][0] and x <= bin_label[key][1]:
                    return key
        else:
            return "None"

    def create_level(self, x, level_dict, selected_list):
        for key in list(level_dict.keys()):
            if x in selected_list:
                if x in level_dict[key]:
                    return key
            else:
                return x

    def create_new_levels_dimension(self, column_name, level_dict):
        selected_list = []
        for key in list(level_dict.keys()):
            selected_list = selected_list + level_dict[key]
        self._data_frame[column_name + "_level"] = self._data_frame[column_name].apply(self.create_level,
                                                                                       level_dict=level_dict,
                                                                                       selected_list=selected_list)
        return self._data_frame

    def create_level_udf_time(self, dict, date_format):
        pass

    def convert_to_date(self, value, date_format):
        if isinstance(value, str):
            value = pd.to_datetime(value, format='%d/%m/%Y')
        elif isinstance(value, str):
            value = pd.to_datetime(value, format='%d/%m/%Y')
        else:
            value = value
        return value

    def convert_to_date_from_level_value(self, value):
        value = pd.to_datetime(value, format='%d/%m/%Y')
        return value

    def check_key_date_bins(self, date, dict, date_format):
        if date is not None:
            date = self.convert_to_date(date, date_format)
            for key, value in list(dict.items()):
                val1_date = self.convert_to_date_from_level_value(value[0])
                val2_date = self.convert_to_date_from_level_value(value[1])
                date_range = [val1_date, val2_date]
                if date >= date_range[0] and date <= date_range[1]:
                    return key
                else:
                    return "None"

    def create_new_levels_datetimes(self, col_for_timelevels, dict):
        self._data_frame[col_for_timelevels + '_temp'] = pd.to_datetime(self._data_frame[col_for_timelevels],
                                                                        errors='ignore')
        unique_vals = self._data_frame[col_for_timelevels + '_temp'].head(15)
        try:
            date_format = self._metaHelperInstance.get_datetime_format_pandas(unique_vals)
        except:
            date_format = None
        self._data_frame[col_for_timelevels + '_t_level'] = self._data_frame[col_for_timelevels + '_temp'].apply(
            self.check_key_date_bins, dict=dict, date_format=date_format)
        self._data_frame = self._data_frame.drop(col_for_timelevels + '_temp', axis=1)
        return self._data_frame

    def create_equal_sized_measure_bins(self, column_name, number_of_bins):
        def create_dict_for_bin():
            min_value = np.min(self._data_frame[column_name])
            max_value = np.max(self._data_frame[column_name])
            interval_size = (old_div((max_value - min_value) * 1.0, (number_of_bins - 1)))
            bin_dict = {}
            temp = min_value
            while temp <= max_value:
                bin_dict[str(round(temp, 3)) + "-" + str(round(temp + interval_size, 3))] = [temp, temp + interval_size]
                temp = temp + interval_size
            return bin_dict

        bin_dict = create_dict_for_bin()
        self._data_frame[column_name + "_bin"] = self._data_frame[column_name].apply(self.check_key, bin_label=bin_dict)
        return self._data_frame

    def create_custom_measure_bins(self, column_name, list_of_intervals):
        def create_dict_for_bin():
            min_value = np.min(self._data_frame[column_name])
            max_value = np.max(self._data_frame[column_name])
            bin_dict = {}
            if list_of_intervals[0] > min_value:
                bin_dict[str(min_value) + "-" + str(list_of_intervals[0])] = [min_value, list_of_intervals[0]]
            for i in range(len(list_of_intervals)):
                if i + 2 <= len(list_of_intervals):
                    bin_dict[str(list_of_intervals[i]) + "-" + str(list_of_intervals[i + 1])] = [list_of_intervals[i],
                                                                                                 list_of_intervals[
                                                                                                     i + 1]]
            if list_of_intervals[-1] < max_value:
                bin_dict[str(list_of_intervals[-1]) + "-" + str(max_value)] = [list_of_intervals[-1], max_value]

            return bin_dict

        bin_dict = create_dict_for_bin()
        self._data_frame[column_name + "_c_bin"] = self._data_frame[column_name].apply(self.check_key,
                                                                                       bin_label=bin_dict)
        return self._data_frame

    def replace_values_in_column(self, column_name, range, value):
        if value == "median":
            dp_helper_obj = DataPreprocessingHelperPandas(self._data_frame, self._dataframe_context)
            median_val = dp_helper_obj.get_median(self._data_frame, column_name)
            replace_value = median_val
            self._data_frame[column_name + "_treated_" + str(range) + "_median"] = self._data_frame[column_name].apply(
                lambda x: replace_value if x == range else x)
        elif value == "mode":
            dp_helper_obj = DataPreprocessingHelperPandas(self._data_frame, self._dataframe_context)
            mode_val = dp_helper_obj.get_mode(self._data_frame, column_name)
            replace_value = mode_val
            self._data_frame[column_name + "_treated_" + str(range) + "_mode"] = self._data_frame[column_name].apply(
                lambda x: replace_value if x == range else x)
        elif value == "mean":
            mean_value = np.mean(self._data_frame[column_name])
            replace_value = mean_value
            self._data_frame[column_name + "_treated_" + str(range) + "_mean"] = self._data_frame[column_name].apply(
                lambda x: replace_value if x == range else x)
        else:
            replace_value = value
            self._data_frame[column_name + "_treated_" + str(range) + "_" + str(replace_value)] = self._data_frame[
                column_name].apply(lambda x: replace_value if x == range else x)
        return self._data_frame

    def standardize_column(self, column_name):
        def standardize_column_helper(mean, sd):
            return [lambda x: round(float((x - mean) * 1.0 / sd), 3) if x is not None else x]

        mean, std_dev = self._data_frame[column_name].mean(), self._data_frame[column_name].std()
        self._data_frame[column_name + '_fs_standardized'] = self._data_frame[column_name].apply(
            standardize_column_helper(mean, std_dev))
        return self._data_frame

    def normalize_column(self, column_name):
        def normalize_column_helper(min, max):
            return [lambda x: round(float((x - min) * 1.0 / (max - min)), 3) if x is not None else x]

        max_value, min_value = self._data_frame[column_name].max(), self._data_frame[column_name].min()
        self._data_frame[column_name + '_fs_normalized'] = self._data_frame[column_name].apply(
            normalize_column_helper(min_value, max_value))
        return self._data_frame

    def replacerUDF(self, value, operation):
        if operation == "prod":
            return [lambda x: x * value if x is not None else x]
        if operation == "add":
            return [lambda x: x + value if x is not None else x]
        if operation == "subs":
            return [lambda x: x - value if x is not None else x]
        if operation == "divide":
            return [(lambda x: int(x, value) if x is not None else x)]
        if operation == "Reciprocal":
            return [(lambda x: int(1, x) if x is not None else x)]
        if operation == "NthRoot":
            try:
                return [(lambda x: x ** (1.0 / value) if x is not None else x)]
            except:
                return [(lambda x: x)]
        if operation == "exponential":
            return [(lambda x: x ** value if x is not None else x)]
        if operation == "logTransform":
            return [lambda x: math.log(x, 10) if x is not None else x]
        if operation == "modulus":
            return [(lambda x: abs(x) if x is not None else x)]

    def logTransform_column(self, column_name):
        column_min = self._data_frame[column_name].min()
        value_to_be_added = abs(column_min) + 1
        if column_min > 0:
            self._data_frame[column_name + "_vt_log_transformed"] = self._data_frame[column_name].apply(
                self.replacerUDF(10, "logTransform"))
            self._data_frame[column_name + "_vt_log_transformed"] = self._data_frame[
                column_name + "_vt_log_transformed"].astype('float')
        else:
            self._data_frame[column_name + "_temp_transformed"] = self._data_frame[column_name].apply(
                self.replacerUDF(value_to_be_added, "add"))
            self._data_frame[column_name + "_vt_log_transformed"] = self._data_frame[
                column_name + "_temp_transformed"].apply(self.replacerUDF(10, "logTransform"))
            self._data_frame[column_name + "_vt_log_transformed"] = self._data_frame[
                column_name + "_vt_log_transformed"].astype('float')
            self._data_frame = self._data_frame.drop(column_name + "_temp_transformed", axis=1)
        return self._data_frame

    def modulus_transform_column(self, column_name):
        self._data_frame[column_name + "_vt_modulus_transformed"] = self._data_frame[column_name].apply(
            self.replacerUDF(10, "modulus"))
        self._data_frame[column_name + "_vt_modulus_transformed"] = self._data_frame[
            column_name + "_vt_modulus_transformed"].astype('float')
        return self._data_frame

    def cuberoot_transform_column(self, column_name):
        self._data_frame[column_name + "_vt_cuberoot_transformed"] = self._data_frame[column_name].apply(
            self.replacerUDF(3, "NthRoot"))
        self._data_frame[column_name + "_vt_cuberoot_transformed"] = self._data_frame[
            column_name + "_vt_cuberoot_transformed"].astype('float')
        return self._data_frame

    def squareroot_transform_column(self, column_name):
        column_min = self._data_frame[column_name].min()
        if column_min >= 0:
            self._data_frame[column_name + "_vt_squareroot_transformed"] = self._data_frame[column_name].apply(
                self.replacerUDF(2, "NthRoot"))
            self._data_frame[column_name + "_vt_squareroot_transformed"] = self._data_frame[
                column_name + "_vt_squareroot_transformed"].astype('float')
        else:
            self._data_frame[column_name + "_vt_squareroot_transformed"] = 0
        return self._data_frame

    def label_encoding_column(self, column_name):
        self._data_frame[column_name + '_ed_label_encoded'] = LabelEncoder().fit_transform(
            self._data_frame[column_name].astype(str))
        return self._data_frame

    def onehot_encoding_column(self, column_name):
        if self._data_frame[column_name].isnull().any():
            self._data_frame[column_name].fillna(self._data_frame[column_name].mode()[0], inplace=True)
        temp = self._data_frame[[column_name]]
        enc = OneHotEncoder_pandas(drop='first')
        k1 = enc.fit_transform(temp).toarray()
        temp = pd.DataFrame(k1, columns=list(enc.get_feature_names()))
        feature_names = list(enc.get_feature_names())
        temp.set_index(self._data_frame.index, inplace=True)
        for col_name in feature_names:
            self._data_frame[column_name + '_' + col_name.partition('_')[2] + '_one_hot'] = temp[col_name].astype('int')
        # X.drop(column_name,axis = 1,inplace = True)
        return self._data_frame

    def character_count_string(self, column_name):
        self._data_frame[column_name + "_character_count"] = self._data_frame[column_name].apply(
            lambda x: x.count("") - 1 if x is not None else 0)
        self._data_frame[column_name + "_character_count"] = self._data_frame[column_name + "_character_count"].astype(
            'float')
        return self._data_frame

    def contains_word(self, column_name, word):
        # word = word.lower()
        self._data_frame[column_name + "_contains_" + word] = self._data_frame[column_name].apply(
            lambda x: False if x is None or x.lower().find(word) == -1 else True)
        return self._data_frame

    def convert_to_timestamp(self, datetime_col, timeformat):
        pass

    def count_time_since(self, col_for_time_since, time_since_date):
        self._data_frame[col_for_time_since + '_temp'] = pd.to_datetime(self._data_frame[col_for_time_since],
                                                                        errors='coerce')
        unique_vals = self._data_frame[col_for_time_since].drop_duplicates().head(10)
        try:
            date_format = self._metaHelperInstance.get_datetime_format_pandas(unique_vals)
            self._data_frame['TIME_SINCE_DATE'] = time_since_date
            self._data_frame[col_for_time_since + '_temp'] = pd.to_datetime(
                self._data_frame[col_for_time_since + '_temp'], format=date_format)
            self._data_frame['TIME_SINCE_DATE_Timestamped'] = pd.to_datetime(self._data_frame['TIME_SINCE_DATE'],
                                                                             format='%d/%m/%Y')
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame['TIME_SINCE_DATE_Timestamped'] - \
                                                                   self._data_frame[col_for_time_since + '_temp']
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame[
                                                                       col_for_time_since + "_time_since"] / np.timedelta64(
                1, 'D')
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame[
                col_for_time_since + "_time_since"].apply(np.ceil)
        except:
            self._data_frame['TIME_SINCE_DATE'] = time_since_date
            self._data_frame['TIME_SINCE_DATE_Timestamped'] = pd.to_datetime(self._data_frame['TIME_SINCE_DATE'],
                                                                             format='%d/%m/%Y',
                                                                             infer_datetime_format=True)
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame['TIME_SINCE_DATE_Timestamped'] - \
                                                                   self._data_frame[col_for_time_since + '_temp']
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame[
                                                                       col_for_time_since + "_time_since"] / np.timedelta64(
                1, 'D')
            self._data_frame[col_for_time_since + "_time_since"] = self._data_frame[
                col_for_time_since + "_time_since"].apply(np.ceil)
        self._data_frame = self._data_frame.drop(["TIME_SINCE_DATE", "TIME_SINCE_DATE_Timestamped"], axis=1)
        self._data_frame = self._data_frame.drop([col_for_time_since + '_temp'], axis=1)
        return self._data_frame

    def month_to_string(self, dict):
        pass

    def extract_datetime_info(self, datetime_col, info_to_extract):
        self._data_frame[datetime_col] = pd.to_datetime(self._data_frame[datetime_col], errors='ignore')
        self._data_frame[datetime_col + '_temp'] = self._data_frame[datetime_col].dt.date
        unique_vals = self._data_frame[datetime_col + '_temp'].head(15)
        try:
            date_format = self._metaHelperInstance.get_datetime_format_pandas(unique_vals)
            if info_to_extract == "year":
                self._data_frame[datetime_col + '_year'] = self._data_frame[datetime_col].dt.year
            if info_to_extract == "month_of_year":
                self._data_frame[datetime_col + '_etf_month_of_year'] = self._data_frame[datetime_col].dt.month
            if info_to_extract == "day_of_month":
                self._data_frame[datetime_col + '_day_of_month'] = self._data_frame[datetime_col].dt.day
            if info_to_extract == "day_of_year":
                self._data_frame[datetime_col + '_day_of_year'] = self._data_frame[datetime_col].dt.dayofyear
            if info_to_extract == "day_of_week":
                self._data_frame[datetime_col + '_etf_day_of_week'] = self._data_frame[datetime_col].dt.dayofweek
            if info_to_extract == "week_of_year":
                self._data_frame[datetime_col + '_week_of_year'] = self._data_frame[datetime_col].dt.weekofyear
            if info_to_extract == "hour":
                self._data_frame[datetime_col + '_hour'] = self._data_frame[datetime_col].dt.hour
            if info_to_extract == "minute":
                self._data_frame[datetime_col + '_minute'] = self._data_frame[datetime_col].dt.minute
            if info_to_extract == "date":
                self._data_frame[datetime_col + '_date'] = self._data_frame[datetime_col].dt.date
            else:
                pass
        except:
            if info_to_extract == "year":
                self._data_frame[datetime_col + '_year'] = self._data_frame[datetime_col].dt.year
            if info_to_extract == "month_of_year":
                self._data_frame[datetime_col + '_etf_month_of_year'] = self._data_frame[datetime_col].dt.month
            if info_to_extract == "day_of_month":
                self._data_frame[datetime_col + '_day_of_month'] = self._data_frame[datetime_col].dt.day
            if info_to_extract == "day_of_year":
                self._data_frame[datetime_col + '_day_of_year'] = self._data_frame[datetime_col].dt.dayofyear
            if info_to_extract == "day_of_week":
                self._data_frame[datetime_col + '_etf_day_of_week'] = self._data_frame[datetime_col].dt.dayofweek
            if info_to_extract == "week_of_year":
                self._data_frame[datetime_col + '_week_of_year'] = self._data_frame[datetime_col].dt.weekofyear
            if info_to_extract == "hour":
                self._data_frame[datetime_col + '_hour'] = self._data_frame[datetime_col].dt.hour
            if info_to_extract == "minute":
                self._data_frame[datetime_col + '_minute'] = self._data_frame[datetime_col].dt.minute
            if info_to_extract == "date":
                self._data_frame[datetime_col + '_date'] = self._data_frame[datetime_col].dt.date
        self._data_frame = self._data_frame.drop(datetime_col + '_temp', axis=1)
        return self._data_frame

    def is_weekend_helper(self):
        pass

    def is_weekend(self, datetime_col):
        self._data_frame[datetime_col + '_temp'] = pd.to_datetime(self._data_frame[datetime_col], errors='coerce')
        unique_vals = self._data_frame[datetime_col].drop_duplicates().head(10)
        try:
            date_format = self._metaHelperInstance.get_datetime_format_pandas(unique_vals)
            self._data_frame[datetime_col + '_temp'] = pd.to_datetime(self._data_frame[datetime_col + '_temp'],
                                                                      format=date_format)
            self._data_frame[datetime_col + 'is_weekend'] = np.where(self._data_frame[datetime_col].dt.dayofweek >= 5,
                                                                     'True', 'False')
        except:
            self._data_frame[datetime_col + 'is_weekend'] = np.where(
                self._data_frame[datetime_col + '_temp'].dt.dayofweek >= 5, 'True', 'False')
        self._data_frame = self._data_frame.drop(datetime_col + '_temp', axis=1)
        return self._data_frame
