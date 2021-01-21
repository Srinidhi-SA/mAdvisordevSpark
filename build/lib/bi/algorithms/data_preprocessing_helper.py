from __future__ import print_function
from __future__ import division
from builtins import zip
from builtins import range
from builtins import object
from past.utils import old_div
from bi.stats.util import Stats
from pyspark.sql import functions as F
from pyspark.sql.functions import avg, when, stddev as _stddev, col


# from pyspark.sql.functions import mean as _mean, stddev as _stddev, col
# from pyspark.sql.functions import *


class DataPreprocessingHelper(object):
    """Docstring for data Preprocessing Operations"""

    def __init__(self, df, dataframe_context):
        self._data_frame = df
        self.removed_col = []
        self._dataframe_context = dataframe_context

    def drop_duplicate_rows(self):
        self._data_frame = self._data_frame.dropDuplicates()
        # self._data_frame.show()
        return self._data_frame

    def drop_duplicate_cols(self):
        '''
        Needs optimization
        '''

        numerical_col = [i_val for (i_val, i_type) in self._data_frame.dtypes if
                         i_type == 'int' or i_type == 'double' or i_type == 'float']
        categorical_col = [i_val for (i_val, i_type) in self._data_frame.dtypes if i_type == 'string']
        boolean_col = [i_val for (i_val, i_type) in self._data_frame.dtypes if i_type == 'boolean']

        categorical_list1 = []
        categorical_list2 = []
        numerical_list1 = []
        numerical_list2 = []
        boolean_list1 = []
        boolean_list2 = []
        remove_list = []

        for i in range(len(categorical_col) - 1):
            for j in range(i + 1, len(categorical_col)):
                if self._data_frame.groupby(
                        self._data_frame[categorical_col[i]]).count().collect() == self._data_frame.groupby(
                        categorical_col[j]).count().collect():
                        if categorical_col[j] == self._dataframe_context.get_result_column():
                            categorical_list1.append(categorical_col[i])
                            categorical_list2.append(categorical_col[j])
                        else :
                            categorical_list1.append(categorical_col[j])
                            categorical_list2.append(categorical_col[i])

        count_dict1 = dict(list(zip(categorical_list1, categorical_list2)))

        elements_list1 = []
        elements_list2 = []

        for k, v in list(count_dict1.items()):
            elements_list1 = self._data_frame.select(k)
            elements_list2 = self._data_frame.select(v)
            if elements_list1.collect() == elements_list2.collect():
                remove_list.append(k)

        for i in range(len(numerical_col) - 1):
            for j in range(i + 1, len(numerical_col)):
                df_col1_std = self._data_frame.select(_stddev(col(numerical_col[i])).alias('std')).collect()[0][0]
                df_col2_std = self._data_frame.select(_stddev(col(numerical_col[j])).alias('std')).collect()[0][0]
                if (df_col1_std == df_col2_std):
                    if numerical_col[j] == self._dataframe_context.get_result_column():
                        numerical_list1.append(numerical_col[i])
                        numerical_list2.append(numerical_col[j])
                    else :
                        numerical_list1.append(numerical_col[j])
                        numerical_list2.append(numerical_col[i])


        count_dict2 = dict(list(zip(numerical_list1, numerical_list2)))

        elements_list3 = []
        elements_list4 = []

        for k, v in list(count_dict2.items()):
            elements_list3 = self._data_frame.select(k)
            elements_list4 = self._data_frame.select(v)
            if elements_list3.collect() == elements_list4.collect():
                remove_list.append(k)

        for i in range(len(boolean_col) - 1):
            for j in range(i + 1, len(boolean_col)):
                if self._data_frame.groupby(df[boolean_col[i]]).count().collect() == self._data_frame.groupby(
                        boolean_col[j]).count().collect():
                        if boolean_col[j] == self._dataframe_context.get_result_column():
                            boolean_list1.append(boolean_col[i])
                            boolean_list2.append(boolean_col[j])
                        else :
                            boolean_list1.append(boolean_col[j])
                            boolean_list2.append(boolean_col[i])

        count_dict3 = dict(list(zip(boolean_list1, boolean_list2)))

        elements_list5 = []
        elements_list6 = []

        for k, v in list(count_dict3.items()):
            elements_list5 = self._data_frame.select(k)
            elements_list6 = self._data_frame.select(v)
            if elements_list5.collect() == elements_list6.collect():
                remove_list.append(k)

        # print(remove_list)
        # return remove_list

        self.removed_col = remove_list
        self._data_frame = self._data_frame.drop(*remove_list)
        return self._data_frame

    def get_removed_columns(self):
        return self.removed_col

    def get_frequency_of_unique_val(self, df, col_for_uvf):
        df_counts = df.groupBy(col_for_uvf).count()
        return df_counts

    def get_n_most_common(self, col_for_nmc, n):
        '''Only returns first n most commmon even if there are multiple duplicate values'''
        df_nmc = self.get_frequency_of_unique_val(col_for_nmc)
        df_nmc = df_nmc.orderBy("count", ascending=False)
        row_count = df_nmc.count()
        if n >= row_count:
            n = row_count
            df_nmc = df_nmc.limit(n)
        else:
            df_nmc = df_nmc.limit(n)
        return df_nmc

    def get_proportion_of_unique_val(self, col_for_uvpro):
        df_counts = self._data_frame.groupBy(col_for_uvpro).count()
        total = df_counts.select(F.sum("count")).collect()[0][0]
        df_prop = df_counts.withColumn("PROPORTION", (old_div(df_counts["count"], total)))
        df_prop = df_prop.drop("count")
        return df_prop

    def get_percentage_of_unique_val(self, col_for_uvper):
        df_counts = self._data_frame.groupBy(col_for_uvper).count()
        total = df_counts.select(F.sum("count")).collect()[0][0]
        df_prop = df_counts.withColumn("PERCENTAGE", 100 * (old_div(df_counts["count"], total)))
        df_prop = df_prop.drop("count")
        return df_prop

    def get_count_of_unique_val(self):
        df_temp = self._data_frame.agg(*(countDistinct(col(c)).alias(c) for c in self._data_frame.columns))
        df_pandas = df_temp.toPandas().transpose()
        print(df_pandas)

    def get_mode(self, df, col_for_mode):
        '''Only returns one mode even in case of multiple available modes'''
        df_mode = self.get_frequency_of_unique_val(df, col_for_mode)
        df_mode = df_mode.orderBy("count", ascending=False)
        df_mode = df_mode.limit(1)
        mode = df_mode.collect()[0][0]
        return mode

    def get_median(self, df, col_for_median):
        median_val = df.approxQuantile(col_for_median, [0.5], 0)
        median = median_val[0]
        return median

    def mean_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        mean_value = df_copy.agg(avg(col_to_impute)).first()[0]
        self._data_frame = self._data_frame.fillna({col_to_impute: mean_value})
        return self._data_frame

    def median_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        median_value = self.get_median(df_copy, col_to_impute)
        self._data_frame = self._data_frame.fillna({col_to_impute: median_value})
        return self._data_frame

    def mode_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        mode_value = self.get_mode(df_copy, col_to_impute)
        self._data_frame = self._data_frame.fillna({col_to_impute: mode_value})
        return self._data_frame

    def user_impute_missing_values(self, col_to_impute, mvt_value):
        df_copy = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        self._data_frame = self._data_frame.fillna({col_to_impute: mvt_value})
        return self._data_frame

    def remove_missing_values(self, null_removal_col):
        self._data_frame = self._data_frame.na.drop()
        return self._data_frame

    def detect_outliers(self, outlier_detection_col):
        '''
        for optimization purpose need to get the outlier information
        for given column from front end only in traning config as generated
        and shared in metadata optimization
        '''
        df_stats = self._data_frame.select(mean(col(outlier_detection_col)).alias('mean'),
                                           stddev(col(outlier_detection_col)).alias('std')).collect()
        mean_val = df_stats[0]['mean']
        std_val = df_stats[0]['std']
        upper_val = mean_val + (3 * std_val)
        lower_val = mean_val - (3 * std_val)
        outliers = [lower_val, upper_val]
        return outliers

    def remove_outliers(self, df, outlier_removal_col):
        '''Need to check how it will affect multiple columns'''
        outlier_count, ol_lower_range, ol_upper_range = Stats.detect_outliers_z(self._data_frame, outlier_removal_col)
        df = self._data_frame.filter(self._data_frame[outlier_removal_col] > ol_lower_range)
        df = self._data_frame.filter(self._data_frame[outlier_removal_col] < ol_upper_range)
        return df

    def cap_outliers(self, outlier_replacement_col):
        outlier_count, ol_lower_range, ol_upper_range = Stats.detect_outliers_z(self._data_frame, outlier_replacement_col)
        df_dup = self._data_frame
        self._data_frame = df_dup.withColumn(outlier_replacement_col, when((df_dup[outlier_replacement_col] < ol_lower_range), ol_lower_range).otherwise(df_dup[outlier_replacement_col]))
        self._data_frame = self._data_frame.withColumn(outlier_replacement_col, when((self._data_frame[outlier_replacement_col] > ol_upper_range), ol_upper_range).otherwise(self._data_frame[outlier_replacement_col]))
        return self._data_frame


    def mean_impute_outliers(self, outlier_imputation_col):
        outlier_count, ol_lower_range, ol_upper_range = Stats.detect_outliers_z(self._data_frame,
                                                                                outlier_imputation_col)
        # df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(self._data_frame, outlier_imputation_col)
        mean_without_outliers = df_without_outliers.agg(avg(outlier_imputation_col)).first()[0]
        self._data_frame = self._data_frame.withColumn(outlier_imputation_col,
                                                       when((self._data_frame[
                                                                 outlier_imputation_col] < ol_lower_range) | (
                                                                        self._data_frame[
                                                                            outlier_imputation_col] > ol_upper_range),
                                                            mean_without_outliers)
                                                       .otherwise(self._data_frame[outlier_imputation_col]))
        return self._data_frame

    def median_impute_outliers(self, outlier_imputation_col):
        outlier_count, ol_lower_range, ol_upper_range = Stats.detect_outliers_z(self._data_frame,
                                                                                outlier_imputation_col)
        # df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(self._data_frame, outlier_imputation_col)
        median_without_outliers = self.get_median(self._data_frame, outlier_imputation_col)
        self._data_frame = self._data_frame.withColumn(outlier_imputation_col,
                                                       when((self._data_frame[
                                                                 outlier_imputation_col] < ol_lower_range) | (
                                                                        self._data_frame[
                                                                            outlier_imputation_col] > ol_upper_range),
                                                            median_without_outliers)
                                                       .otherwise(
                                                           self._data_frame[outlier_imputation_col]))
        return self._data_frame

    def mode_impute_outliers(self, outlier_imputation_col):
        outlier_count, ol_lower_range, ol_upper_range = Stats.detect_outliers_z(self._data_frame,
                                                                                outlier_imputation_col)
        # df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(self._data_frame, outlier_imputation_col)
        mode_without_outliers = self.get_mode(self._data_frame, df_without_outliers[outlier_imputation_col])
        self._data_frame = self._data_frame.withColumn(outlier_imputation_col,
                                                       when((self._data_frame[
                                                                 outlier_imputation_col] < ol_lower_range) | (
                                                                        self._data_frame[
                                                                            outlier_imputation_col] > ol_upper_range),
                                                            mode_without_outliers)
                                                       .otherwise(self._data_frame[outlier_imputation_col]))
        return self._data_frame

    def user_impute_outliers(self, outlier_imputation_col, mvt_value):
        pass
