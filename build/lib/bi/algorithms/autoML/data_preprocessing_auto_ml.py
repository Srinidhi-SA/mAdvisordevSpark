import locale
import pandas as pd
import numpy as np
import re
import pint
import sys
from pint import UnitRegistry
import random
import pickle
import time
from validate_email import validate_email
from scipy import stats
from bi.algorithms.autoML.utils_automl import *
from pyspark.sql.types import StringType
from pyspark.sql.functions import *
import pyspark.sql.functions as F
class DataPreprocessingAutoML:

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type,pandas_flag):
        self.data_frame = data_frame
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict["MeasureColsToDim"] = []
        self.data_change_dict['MeanImputeCols'] = []
        self.data_change_dict['ModeImputeCols'] = []
        self._pandas_flag = pandas_flag
        if self._pandas_flag:
            self.col_with_nulls = list(self.data_frame .loc[:, (self.data_frame.isna().sum() > 0)])
        else:
            self.col_with_nulls = [col for col in self.data_frame.columns if (self.data_frame.filter((self.data_frame[col] == "") | (self.data_frame[col].isNull())).count())>0]


    def drop_duplicate_rows(self):
        """Drops Duplicate rows of a dataframe and returns a new dataframe"""
        if self._pandas_flag:
            self.data_frame = self.data_frame.drop_duplicates()
        else:
            self.data_frame = self.data_frame.dropDuplicates()

    def drop_constant_unique_cols(self):
        if not self._pandas_flag:
            cnt = self.data_frame.agg(*(F.countDistinct(c).alias(c) for c in self.data_frame.columns)).first()
            self.data_frame = self.data_frame.drop(*[c for c in cnt.asDict() if cnt[c] == 1 or cnt[c] == self.data_frame.count()])
        else:
           # self.data_frame  = self.data_frame.loc[:, (self.data_frame .nunique() != 1)]
           # new_df  = self.data_frame.loc[:, (self.data_frame.nunique() != self.data_frame .shape[0])]
           # if self.target not in new_df.columns:
           #     new_df[self.target] = self.data_frame[self.target]
           # self.data_frame = new_df
           self.data_frame = self.data_frame.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)
           self.data_frame = self.data_frame.loc[:, (self.data_frame.nunique() != 1)]
           float_df = self.data_frame.loc[:, (self.data_frame.dtypes == 'float64')]
           date_df = self.data_frame[self.datetime_cols]
           int_df = self.data_frame.loc[:, (self.data_frame.dtypes == 'int64')]
           other_df  = self.data_frame .loc[:, ((self.data_frame.dtypes=='object')&(self.data_frame.nunique()!=self.data_frame.shape[0]))]
           new_df = pd.concat([other_df, float_df, int_df , date_df], axis=1)
           #new_df = new_df.loc[:, (new_df.nunique() != new_df.shape[0])]
           #new_df  = self.data_frame .loc[:, (self.data_frame.nunique() != self.data_frame .shape[0])]
           #new_df=self.data_frame
           if self.target not in new_df.columns:
               new_df[self.target] = self.data_frame[self.target]
               self.data_frame = new_df
           else:
               self.data_frame = new_df
        self.data_change_dict['dropped_columns_list'] = []
        def dropped_col_update(list_element):
            if list_element["column_name"] not in self.data_frame.columns:
                list_element["dropped_column_flag"] = True
                self.data_change_dict['dropped_columns_list'].append(list_element["column_name"])
                self.numeric_cols, self.dimension_cols, self.col_with_nulls = drop_cols_from_list(list_element["column_name"],self.numeric_cols, self.dimension_cols, self.col_with_nulls)
            else:
                pass
            return list_element
        self.data_change_dict['Column_settings'] = [dropped_col_update(list_element) for list_element in self.data_change_dict['Column_settings']]

    def drop_null_cols(self):
        '''Dropping columns with more than 75% null values'''
        if not self._pandas_flag:
            cnt = self.data_frame.agg(*(F.count(c).alias(c) for c in self.data_frame.columns)).first()
            self.data_frame = self.data_frame.drop(*[c for c in cnt.asDict() if cnt[c] < 0.75*self.data_frame.count()])
            # filter_cols = [col for col in self.data_frame.columns if self.data_frame.filter((self.data_frame[col] == "") | (self.data_frame[col].isNull())).count() < 0.75*self.data_frame.count()]
            # self.data_frame  = self.data_frame.select(filter_cols)
        else:
            self.data_frame  = self.data_frame .loc[:, (self.data_frame.isna().sum() < (0.75 * self.data_frame.shape[0]))]
        def dropped_col_update(list_element):
            if list_element["column_name"] not in self.data_frame.columns:
                list_element["dropped_column_flag"] = True
                self.data_change_dict['dropped_columns_list'].append(list_element["column_name"])
                self.numeric_cols, self.dimension_cols, self.col_with_nulls = drop_cols_from_list(list_element["column_name"],self.numeric_cols, self.dimension_cols, self.col_with_nulls)
            else:
                pass
            return list_element
        self.data_change_dict['Column_settings'] = [dropped_col_update(list_element) for list_element in self.data_change_dict['Column_settings']]

    def dimension_measure(self, columns):
        """Identifies columns which are measures and have been wrongly identified as dimension
        returns a list of columns to be converted to measure and removes the rows which have other than numeric
        for that particular column"""
        # column_val = self.data_frame[column]
        if not self._pandas_flag:
            for column in columns:
                r1 = random.randint(0, self.data_frame.count() - 1)
                if re.match("^\d*[.]?\d*$", str(self.data_frame.collect()[r1][column])):
                    self.data_frame = self.data_frame.withColumn("is_numeric_col",\
                                    col(column).\
                                    rlike("^[0-9]+[.]{0,1}[0-9]*\s*$"))
                    val_count = self.data_frame.cube("is_numeric_col").count()
                    val_count_list =list(map(lambda row: row.asDict(), val_count.collect()))
                    dict_vals = {each['is_numeric_col']:each['count']/self.data_frame.count()\
                                                for each in val_count_list}
                    if False in dict_vals.keys():
                        if dict_vals[False] <= 0.01:
                            self.data_frame = self.data_frame.filter(self.data_frame.is_numeric_col.isin([True]))
                            self.data_frame = self.data_frame.drop('is_numeric_col')
                            self.data_change_dict["MeasureColsToDim"].append(column)
                            self.dimension_cols.remove(column)
                            ## below line code change during optimization
                            self.data_frame = self.data_frame.withColumn(column, self.data_frame[column].cast("float"))
                            self.numeric_cols.append(column)
        else:
            for column in columns:
                column_val = self.data_frame[column]
                updated_row_num = self.data_frame[column].index
                r1 = random.randint(0, len(updated_row_num) - 1)
                if re.match("^\d*[.]?\d*$", str(self.data_frame.iloc[r1][column])):
                    # out=column_val.str.isdigit()
                    out = column_val.str.contains("^[0-9]+[.]{0,1}[0-9]*\s*$")
                    if out[out == False].count() <= 0.01 * self.data_frame.shape[0]:
                        row_index = out.index[out == False].tolist()

                        self.data_frame = self.data_frame.drop(row_index, axis=0)
                        self.data_change_dict["MeasureColsToDim"].append(column)
                        self.dimension_cols.remove(column)
                        ## below line code change during optimization
                        self.data_frame[column] = pd.to_numeric(self.data_frame[column])
                        self.numeric_cols.append(column)

    def dimension_measure_test(self, columns):
        for column in columns:
            if (str(self.data_frame[column].dtype).startswith('int')) | (str(self.data_frame[column].dtype).startswith('float')):
                continue
            else:
                if self._pandas_flag:
                    column_val = self.data_frame[column]
                    out = column_val.str.contains("^[0-9]+[.]{0,1}[0-9]*\s*$")
                    if out[out == False].count() <= 0.01 * self.data_frame.shape[0]:
                        row_index = out.index[out == False].tolist()
                        pure_column = self.data_frame[column].drop(row_index, axis=0)
                        self.data_frame[column] = pd.to_numeric(self.data_frame[column])
                        self.data_frame.iloc[row_index] = int(np.mean(pure_column))
                        self.dimension_cols.remove(column)
                        self.numeric_cols.append(column)
                else:
                    self.data_frame = self.data_frame.withColumn("is_numeric_col",\
                                    col(column).\
                                    rlike("^[0-9]+[.]{0,1}[0-9]*\s*$"))
                    val_count = self.data_frame.cube("is_numeric_col").count()
                    val_count_list =list(map(lambda row: row.asDict(), val_count.collect()))
                    dict_vals = {each['is_numeric_col']:each['count']/self.data_frame.count()\
                                                for each in val_count_list}
                    if dict_vals[False] <= 0.01:
                        self.data_frame = self.data_frame.filter(self.data_frame.is_numeric_col.isin([True]))
                        self.data_frame = self.data_frame.drop('is_numeric_col')
                        self.dimension_cols.remove(column)
                        ## below line code change during optimization
                        self.data_frame = self.data_frame.withColumn(column, self.data_frame[column].cast("float"))
                        self.numeric_cols.append(column)



    def handle_outliers(self):
        '''
        Needs to be fixed
        '''
        # #Ref: https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-data-frame
        # df = self.data_frame[columns]
        # df1 = self.data_frame[self.dimension_cols]
        # idx = np.all(stats.zscore(df) < 3, axis=1)
        # self.data_frame.loc[idx]

    def mean_impute(self, column_val):
        """Returns a column with mean impute"""
        mean = np.mean(column_val)
        column_val = column_val.fillna(mean)
        return column_val

    def median_impute(self, column_val):
        """Returns a column with median impute"""
        median = np.median(column_val)
        column_val = column_val.fillna(median)
        return column_val

    def mode_impute(self, column_val):
        """Returns a column with mode impute"""
        mode = column_val.mode()[0]
        column_val = column_val.fillna(mode)
        return column_val

    def measure_col_imputation(self, columns):
        """Does missing value imputation for measure columns"""
        mean_impute_cols = []
        median_impute_cols = []
        for column in columns:
            if column in self.col_with_nulls:
                if not self._pandas_flag:
                    mean = self.data_frame.agg({column: "mean"}).head()[0]
                    self.data_frame = self.data_frame.fillna({ column:mean })
                else:
                    self.data_frame[column] = self.mean_impute(self.data_frame[column])
                self.data_change_dict['MeanImputeCols'].append(column)

    def dim_col_imputation(self, columns):
        """Does missing value imputation for dimension columns"""
        for column in columns:
            if column in self.col_with_nulls:
                if not self._pandas_flag:
                    mode  = self.data_frame.select(column).toPandas().mode().values[0][0]
                    self.data_frame = self.data_frame.fillna({ column:mode })
                else:
                    self.data_frame[column] = self.mode_impute(self.data_frame[column])
                self.data_change_dict['ModeImputeCols'].append(column)

    def date_col_imputation(self, columns):
        """Does missing value imputation for date columns"""
        for column in columns:
            if column in self.col_with_nulls:
                if not self._pandas_flag:
                    mode  = self.data_frame.select(column).toPandas().mode().values[0][0]
                    self.data_frame = self.data_frame.fillna({ column:mode })
                else:
                    self.data_frame[column] = self.mode_impute(self.data_frame[column])
                self.data_change_dict['ModeImputeCols'].append(column)

    def test_data_imputation(self):
        if self._pandas_flag:
            null_cols = self.data_frame.columns[self.data_frame.isna().any()].tolist()
            if len(null_cols) != 0:
                numeric_columns = self.data_frame[null_cols]._get_numeric_data().columns
                cat_col_names = list(set(null_cols) - set(numeric_columns))
                for col in null_cols:
                    if col in cat_col_names:
                        mode_df = self.mode_impute(self.data_frame[col])
                        self.data_frame[col] = mode_df
                    else:
                        mean_df = self.mean_impute(self.data_frame[col])
                        self.data_frame[col] = mean_df
        else:
            if len(self.col_with_nulls) !=0:
                for column in self.col_with_nulls:
                    if (self.data_frame.select(column).dtypes[0][1]== 'int') | (self.data_frame.select(column).dtypes[0][1]== 'double'):
                        mean = self.data_frame.agg({column: "mean"}).head()[0]
                        self.data_frame = self.data_frame.fillna({column:mean })
                    else:
                        mode  = self.data_frame.select(column).toPandas().mode().values[0][0]
                        self.data_frame = self.data_frame.fillna({column:mode })

    #ON HOLD
    def regex_catch(self, column):
        """Returns a list of columns and the pattern it has"""
        ## considering currency_list and metric_list are globally defined.
        pattern_dict = {"Column_name": column, "email-id": False, "website": False, "Percentage": False,
                "CurrencyCol": {"value": False, "currency": None}, "MetricCol": {"value": False, "metric": None},
                "SepSymbols": {"value": False, "Symbol": None}}
        column_val = self.data_frame[column].astype(str).str.strip()
        df1 = self.data_frame[column_val.apply(validate_email)]
        if df1.shape[0] >= (0.8 * self.data_frame.shape[0]):
            pattern_dict["email-id"] = True
        elif column_val.str.contains("%$", na=True).all():
            pattern_dict["Percentage"] = True
        elif column_val.str.contains("^https:|^http:|^www.", na=True).all():
            pattern_dict["website"] = True
        elif column_val.str.contains("[0-9]+[.]{0,1}[0-9]*\s*[Aa-zZ]{1,2}$").all():
            metric = list(map(lambda x: re.sub("[0-9]+[.]{0,1}[0-9]*\s*", "", x), column_val))
            if len(set(metric)) == 1:
                if metric[0] in Metric_list:
                    pattern_dict["MetricCol"]["value"] = True
                    pattern_dict["MetricCol"]["metric"] = metric[0]
        elif column_val.str.contains("([0-9]+[.]{0,1}[0-9]*\s*\W$)|(^\W[0-9]+[.]{0,1}[0-9]*)").all():
            currency = list(map(lambda x: re.sub("[0-9.\s]+", "", x), column_val))
            if len(set(currency)) == 1:
                if currency[0] in currency_list:
                    pattern_dict["CurrencyCol"]["value"] = True
                    pattern_dict["CurrencyCol"]["currency"] = currency[0]
        elif column_val.str.contains("\S+\s*[\W_]+\s*\S+").all():
            seperators = list(map(lambda x: re.sub("\s*[a-zA-Z0-9]+$", "", x),
                                  list(map(lambda x: re.sub('^[a-zA-Z0-9]+\s*', '', x), column_val))))
            if len(set(seperators)) == 1:
                if seperators[0] == "":
                    seperators[0] = ' '
                pattern_dict["SepSymbols"]["value"] = True
                pattern_dict["SepSymbols"]["Symbol"] = seperators[0]
        return pattern_dict

    #ON HOLD
    def target_analysis(self, targetname, m_type):
        '''Gives information of target column'''
        self.dataframe = self.dataframe.dropna(axis=0, subset=[targetname])
        output_dict = {
            "target_analysis": {"target": targetname, "unique_count": int, "value_counts": {}, "balanced": None,
                                "binary": None}}
        target_variable = self.dataframe[targetname]
        counts = target_variable.value_counts()
        self.dataframe = self.dataframe[~target_variable.isin(counts[counts <= 10].index)]
        if (m_type.lower() == 'classification'):
            ## convert target column into object
            output_dict['target_analysis']['converted_to_str'] = False
            if self.dataframe[targetname].dtype != 'O':
                self.dataframe[targetname] = "'" + self.dataframe[targetname].astype(str) + "'"
                output_dict['target_analysis']['converted_to_str'] = True
                print("!!!!!!! Converted to str!!!!!!")
            unique_count = target_variable.nunique()
            output_dict['target_analysis']['unique_count'] = unique_count
            level_count = target_variable.value_counts()
            count_check = level_count[level_count >= 10]
            output_dict['target_analysis']['value_counts'] = count_check.to_dict()
            percen_level_count = round((count_check / count_check.sum()) * 100)
            n = len(count_check)
            if (n == 0):
                out_dict = {"target_analysis": {"target_name": targetname, "descrp_status": {}}}
                out_dict['target_analysis']['descrp_status'] = target_variable.describe().to_dict()
                return out_dict, self.dataframe
            if not (percen_level_count[percen_level_count < ((1 / (2 * n)) * 100)]).empty:
                output_dict['target_analysis']['balanced'] = False
                if (len(count_check) == 2):
                    output_dict['target_analysis']['binary'] = True  # binary (true)
                else:
                    output_dict['target_analysis']['binary'] = False  # not binary(False)
            else:
                output_dict['target_analysis']['balanced'] = True  # balanced (True)
                if (len(count_check) == 2):
                    output_dict['target_analysis']['binary'] = True  # binary (true)
                else:
                    output_dict['target_analysis']['binary'] = False  # not binary(False)
            return output_dict
        else:
            out_dict = {"target_analysis": {"target_name": targetname, "descrp_status": {}}}
            out_dict['target_analysis']['descrp_status'] = target_variable.describe().to_dict()
            return out_dict

    def data_preprocessing_run(self):
        start_time=time.time()
        self.drop_duplicate_rows()
        print("time taken for drop_duplicate_rows:{} seconds".format((time.time()-start_time)))

        start_time=time.time()
        self.drop_constant_unique_cols()
        print("time taken for drop_constant_unique_cols:{} seconds".format((time.time()-start_time)))

        start_time=time.time()
        self.drop_null_cols()
        print("time taken for drop_null_cols:{} seconds".format((time.time()-start_time)))
        start_time=time.time()
        self.dimension_measure(self.dimension_cols)
        print("time taken for dimension_measure:{} seconds".format((time.time()-start_time)))

        # self.handle_outliers()
        start_time=time.time()
        self.measure_col_imputation(self.numeric_cols)
        print("time taken for measure_col_imputation:{} seconds".format((time.time()-start_time)))

        start_time=time.time()
        self.dim_col_imputation(self.dimension_cols)
        print("time taken for dim_col_imputation:{} seconds".format((time.time()-start_time)))

        start_time=time.time()
        self.date_col_imputation(self.datetime_cols)
        print("time taken for date_col_imputation:{} seconds".format((time.time()-start_time)))
