from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pyspark.sql.types import StringType, DoubleType, TimestampType
import numpy as np
import pandas as pd
import time
class DataValidation:
    def __init__(self,data_frame,target,problem_type,pandas_flag):
        self.data_frame = data_frame
        self._pandas_flag = pandas_flag
        na_values = ["NO CLUE", "no clue", "No Clue", "na", "NA", "N/A", "n/a", "n a", "N A", "not available",
                     "Not Available", "NOT AVAILABLE", "?", "!", "NONE", "None", "none", "null", "-"]
        if self._pandas_flag:
            self.data_frame = self.data_frame.replace(to_replace =na_values, value = np.nan)
        #else:
         #   self.data_frame = self.data_frame.replace(na_values,'null')
        data = self.data_frame
        if self._pandas_flag:
            data = data.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = []
        self.dimension_cols = []
        self.datetime_cols = [] #Check it
        if self._pandas_flag:
            self.datetime_cols.extend(data.select_dtypes(include=['datetime']).columns)
        else:
            self.datetime_cols=[f.name for f in data.schema.fields if isinstance(f.dataType, TimestampType)]
        self.data_change_dict = {} #Keeps track of changes done on the dataset

    def find_dataType(self,column):
        Dict = {
            "column_name": column,
            "re_column_name": column,
            "data_type": False,
            "re_name": False,
            "special_char": False,
            "dropped_column_flag": False
        }
        if self._pandas_flag:
            if self.data_frame[column].dtype!= np.object:
                Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
                if column != self.target:
                    self.numeric_cols.append(column)

            else:
                Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
                if column != self.target and column not in self.datetime_cols:
                    self.dimension_cols.append(column)
        else:
            if (self.data_frame.select(column).dtypes[0][1] == 'int') | (self.data_frame.select(column).dtypes[0][1] == 'double'):
                Dict["data_type"] = "{}".format(self.data_frame.select(column).dtypes[0][1])
                if column != self.target:
                    self.numeric_cols.append(column)

            else:
                Dict["data_type"] = "{}".format(self.data_frame.select(column).dtypes[0][1])
                if column != self.target and column not in self.datetime_cols:
                    self.dimension_cols.append(column)



        #     try:
        #         self.data_frame[column] = pd.to_datetime(self.data_frame[column], errors='ignore')
        #         Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
        #         if column != self.target:
        #             self.datetime_cols.append(column)
        #     except:
        #         Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
        #         if column != self.target:
        #             self.dimension_cols.append(column)

        return Dict

    def target_fitness_check(self):
        """Checks if target is fit for the type of analysis"""
        # '''replace nan values with nan_class '''
        if self._pandas_flag:
            try:
                if self.problem_type.lower() == "classification":
                # self.data_frame[self.target].fillna("nan_class", inplace=True)
                    self.data_frame.dropna(axis=0, inplace=True, subset=[self.target])
                    target_val = self.data_frame[self.target]
                else:
                    self.data_frame[self.target].fillna(self.data_frame[self.target].mean(), inplace=True)
                    target_val = self.data_frame[self.target]
            except:
                flag = True
                return flag
            if self.problem_type.lower() == "classification":
                if (target_val.nunique()) > 30 or (target_val.nunique()) <= 1:
                    flag = False
                else:
                    flag = True
            else:
                if target_val.nunique() < 10:
                    flag = False
                else:
                    flag = True
        else:
            try:
                if self.problem_type.lower() == "classification":
                    self.data_frame = self.data_frame.dropna(subset=(self.target))
                    target_val = self.data_frame.select(self.target)
                else:
                    mean_value = self.data_frame.agg(avg(self.target)).first()[0]
                    self.data_frame = self.data_frame.fillna({self.target: mean_value})
                    target_val = self.data_frame.select(self.target)
            except:
                flag = True
                return flag
            if self.problem_type.lower() == "classification":
                if (target_val.distinct().count()) > 30 or (target_val.distinct().count()) <= 1:
                    flag = False
                else:
                    flag = True
            else:
                if target_val.distinct().count() < 10:
                    flag = False
                else:
                    flag = True
        return flag


    def data_validation_run(self):
        start_time=time.time()
        self.data_change_dict['Column_settings'] = [self.find_dataType(i) for i in self.data_frame.columns]
        print("time taken for find_dataType:{} seconds".format((time.time()-start_time)))

        start_time=time.time()
        target_fitness_flag = self.target_fitness_check()
        self.data_change_dict['target_fitness_check']=target_fitness_flag
        print("time taken for target_fitness_check:{} seconds".format((time.time()-start_time)))
