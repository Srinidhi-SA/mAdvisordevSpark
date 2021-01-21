import pandas as pd


class DataPreprocessingHelperPandas(object):
    """Data Preprocessing Operations in Pandas"""

    def __init__(self, df, dataframe_context):
        self._data_frame = df
        self.removed_col = []
        self._dataframe_context = dataframe_context

    def drop_duplicate_rows(self):
        self._data_frame = self._data_frame.drop_duplicates()
        return self._data_frame

    def drop_duplicate_cols(self):
        """https://github.com/pandas-dev/pandas/issues/11250"""
        groups = self._data_frame.columns.to_series().groupby(self._data_frame.dtypes).groups

        duplicate_columns = []
        for t, v in groups.items():

            cs = self._data_frame[v].columns
            vs = self._data_frame[v]
            lcs = len(cs)

            for i in range(lcs):
                iv = vs.iloc[:, i].tolist()
                for j in range(i + 1, lcs):
                    jv = vs.iloc[:, j].tolist()
                    if iv == jv:
                        duplicate_columns.append(cs[j])  # i for keep last column, j for keep first column
                        break

        self.removed_col = duplicate_columns
        self._data_frame = self._data_frame.drop(duplicate_columns, axis=1)

        return self._data_frame

    # def get_frequency_of_unique_val(self, col_for_uvf):
    #     df_counts = self._data_frame.astype(str).groupby(col_for_uvf).size().reset_index(name="count")
    #     return df_counts

    # def get_n_most_common(self, col_for_nmc, n):
    #     """Only returns first n most common even if there are multiple duplicate values"""
    #     df_nmc = self.get_frequency_of_unique_val(col_for_nmc)
    #     df_nmc.sort_values(by='count', ascending=False)
    #     row_count = len(df_nmc)
    #     if n >= row_count:
    #         return df_nmc
    #     else:
    #         df_nmc = df_nmc[0:n]
    #         return df_nmc

    # def get_proportion_of_unique_val(self, col_for_uvpro):
    #     df_counts = self._data_frame.astype(str).groupby(col_for_uvpro).size().reset_index(name="count")
    #     total = df_counts['count'].sum()
    #     df_counts['PROPORTION'] = df_counts['count'] / total
    #     return df_counts.drop('count', axis=1)

    # def get_percentage_of_unique_val(self, col_for_uvper):
    #     df_counts = self._data_frame.astype(str).groupby(col_for_uvper).size().reset_index(name="count")
    #     total = df_counts['count'].sum()
    #     df_counts['PERCENTAGE'] = (df_counts['count'] / total) * 100
    #     return df_counts.drop('count', axis=1)

    def get_removed_columns(self):
        return self.removed_col

    def get_mode(self, df, col_for_mode):
        mode = df[col_for_mode].mode()[0]
        return mode

    def get_median(self, df, col_for_median):
        median = df[col_for_median].median()
        return median

    def mean_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame[~self._data_frame[col_to_impute].isnull()]
        mean_value = df_copy[col_to_impute].mean()
        self._data_frame = self._data_frame.fillna({col_to_impute: mean_value})
        return self._data_frame

    def median_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame[~self._data_frame[col_to_impute].isnull()]
        median_value = self.get_median(df_copy, col_to_impute)
        self._data_frame = self._data_frame.fillna({col_to_impute: median_value})
        return self._data_frame

    def mode_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame[~self._data_frame[col_to_impute].isnull()]
        mode_value = self.get_mode(df_copy, col_to_impute)
        self._data_frame = self._data_frame.fillna({col_to_impute: mode_value})
        return self._data_frame

    def user_impute_missing_values(self, col_to_impute, mvt_value):
        self._data_frame = self._data_frame.fillna({col_to_impute: mvt_value})
        return self._data_frame

    def remove_missing_values(self):
        self._data_frame = self._data_frame.dropna(axis=0)
        return self._data_frame

    def detect_outliers_z(self, col):
        df_stats = {"mean": self._data_frame[col].mean(), "std_dev": self._data_frame[col].std()}
        mean_val = df_stats['mean']
        std_val = df_stats['std_dev']
        upper_val = float(mean_val) + float(3 * std_val)
        lower_val = float(mean_val) - float(3 * std_val)
        # outliers = [lower_val, upper_val]
        df_out = self._data_frame.loc[(self._data_frame[col] < lower_val) & (self._data_frame[col] > upper_val)]
        outlier_count = df_out.count().sum()
        return outlier_count, lower_val, upper_val

    def remove_outliers(self, outlier_removal_col):
        """Need to check how it will affect multiple columns"""

        outlier_count, ol_lower_range, ol_upper_range = self.detect_outliers_z(outlier_removal_col)
        self._data_frame = self._data_frame[(self._data_frame[outlier_removal_col] > ol_lower_range) & (
                    self._data_frame[outlier_removal_col] < ol_upper_range)]
        return self._data_frame

    def cap_outliers(self, outlier_replacement_col):
        df1 = self._data_frame[outlier_replacement_col]
        outlier_count, ol_lower_range, ol_upper_range = self.detect_outliers_z(outlier_replacement_col)
        df1 = df1.replace(to_replace=df1[df1 < ol_lower_range], value=ol_lower_range)
        df1 = df1.replace(to_replace=df1[df1 > ol_upper_range], value=ol_upper_range)
        self._data_frame[outlier_replacement_col] = df1
        return self._data_frame

    def mean_impute_outliers(self, outlier_imputation_col):
        df1 = self._data_frame[outlier_imputation_col]
        outlier_count, ol_lower_range, ol_upper_range = self.detect_outliers_z(outlier_imputation_col)
        df_without_outliers = self.remove_outliers(outlier_imputation_col)
        mean_without_outliers = df_without_outliers[outlier_imputation_col].mean()
        df1 = df1.replace(to_replace=df1[df1 < ol_lower_range], value=mean_without_outliers)
        df1 = df1.replace(to_replace=df1[df1 > ol_upper_range], value=mean_without_outliers)
        self._data_frame[outlier_imputation_col] = df1
        return self._data_frame

    def median_impute_outliers(self, outlier_imputation_col):
        df1 = self._data_frame[outlier_imputation_col]
        outlier_count, ol_lower_range, ol_upper_range = self.detect_outliers_z(outlier_imputation_col)
        # df_without_outliers = self.remove_outliers(outlier_imputation_col)
        median_without_outliers = self.get_median(self._data_frame, outlier_imputation_col)
        df1 = df1.replace(to_replace=df1[df1 < ol_lower_range], value=median_without_outliers)
        df1 = df1.replace(to_replace=df1[df1 > ol_upper_range], value=median_without_outliers)
        self._data_frame[outlier_imputation_col] = df1
        return self._data_frame
