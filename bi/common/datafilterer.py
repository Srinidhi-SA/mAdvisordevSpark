from __future__ import absolute_import
from builtins import map
from builtins import object
from pyspark.ml.feature import Bucketizer
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType

from .utils import accepts


#import bi.common.dataframe
revmap_dict = {'Low':0.0,'Below Average':1.0,'Average':2.0,'Above Average':3.0,'High':4.0}
class DataFrameFilterer(object):
    @accepts(object,dataframe=DataFrame,pandas_flag=bool)
    def __init__(self, dataframe, pandas_flag):
        self._data_frame = dataframe
        self._pandas_flag = pandas_flag

    def bucketize(self, splits, target_col):
        self._bucket_name = 'bucket_'+target_col
        if self._pandas_flag:
            ''' TO DO: this method is not being used anywhere '''
            pass
        else:
            bucketizer = Bucketizer(inputCol=target_col,
                                    outputCol=self._bucket_name)
            splits.sort()
            bucketizer.setSplits(splits)
            column_data_types = {field.name: field.dataType for field in self._data_frame.schema.fields}
            if column_data_types[target_col] != DoubleType:
                self._data_frame = self._data_frame.select(*[col(target_col).cast('double').alias(target_col) if column==target_col else column for column in self._data_frame.columns])
            self._data_frame = bucketizer.transform(self._data_frame)
        return self._bucket_name

    def values_between(self,colname,start_value, end_value, greater_than_equal = 0, less_than_equal=1):
        if self._pandas_flag:
            if (greater_than_equal == 0) and (less_than_equal==1):
                self._data_frame = self._data_frame[(self._data_frame[colname] > start_value) & (self._data_frame[colname] <= end_value)]
            elif (greater_than_equal == 0) and (less_than_equal==0):
                self._data_frame = self._data_frame[(self._data_frame[colname] > start_value) & (self._data_frame[colname] < end_value)]
            elif (greater_than_equal == 1) and (less_than_equal==1):
                self._data_frame = self._data_frame[(self._data_frame[colname] >= start_value) & (self._data_frame[colname] <= end_value)]
            elif (greater_than_equal == 1) and (less_than_equal==0):
                self._data_frame = self._data_frame[(self._data_frame[colname] >= start_value) & (self._data_frame[colname] < end_value)]
        else:
            if (greater_than_equal == 0) and (less_than_equal==1):
                self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) <= end_value)
            elif (greater_than_equal == 0) and (less_than_equal==0):
                self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) < end_value)
            elif (greater_than_equal == 1) and (less_than_equal==1):
                self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) <= end_value)
            elif (greater_than_equal == 1) and (less_than_equal==0):
                self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) < end_value)

    def dates_between(self,colname,start_value, end_value, greater_than_equal = 1, less_than_equal=1):
        colname = colname.lstrip('0123456789. ')
        if self._pandas_flag:
            # needs to be a pandas datetime64 type to filter by dates
            if (greater_than_equal == 0) and (less_than_equal==1):
                self._data_frame = self._data_frame[(self._data_frame[colname] > start_value) & (self._data_frame[colname] <= end_value)]
            elif (greater_than_equal == 0) and (less_than_equal==0):
                self._data_frame = self._data_frame[(self._data_frame[colname] > start_value) & (self._data_frame[colname] < end_value)]
            elif (greater_than_equal == 1) and (less_than_equal==1):
                self._data_frame = self._data_frame[(self._data_frame[colname] >= start_value) & (self._data_frame[colname] <= end_value)]
            elif (greater_than_equal == 1) and (less_than_equal==0):
                self._data_frame = self._data_frame[(self._data_frame[colname] >= start_value) & (self._data_frame[colname] < end_value)]
        else:
            # needs to be a pyspark timestamp type to filter by dates
            if (greater_than_equal == 0) and (less_than_equal==1):
                self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) <= end_value)
            elif (greater_than_equal == 0) and (less_than_equal==0):
                self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) < end_value)
            elif (greater_than_equal == 1) and (less_than_equal==1):
                self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) <= end_value)
            elif (greater_than_equal == 1) and (less_than_equal==0):
                self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) < end_value)

    def values_above(self,colname, start_value, greater_than_equal=0):
        colname = colname.lstrip('0123456789. ')
        if self._pandas_flag:
            if greater_than_equal == 0:
                self._data_frame = self._data_frame[(self._data_frame[colname]  > start_value)]
            elif greater_than_equal == 1:
                self._data_frame = self._data_frame[(self._data_frame[colname]  >= start_value)]
        else:
            if greater_than_equal == 0:
                self._data_frame = self._data_frame.filter(col(colname) > start_value)
            elif greater_than_equal == 1:
                self._data_frame = self._data_frame.filter(col(colname) >= start_value)

    def values_below(self, colname, end_value, less_than_equal=1):
        colname = colname.lstrip('0123456789. ')
        if self._pandas_flag:
            if less_than_equal==0:
                self._data_frame = self._data_frame[(self._data_frame[colname] < end_value)]
            elif less_than_equal==1:
                self._data_frame = self._data_frame[(self._data_frame[colname] <= end_value)]
        else:
            if less_than_equal==0:
                self._data_frame = self._data_frame.filter(col(colname) < end_value)
            elif less_than_equal==1:
                self._data_frame = self._data_frame.filter(col(colname) <= end_value)

    def values_in(self, colname, values,measure_columns):
        colname = colname.lstrip('0123456789. ')
        if type(values) == str:
            values = values[1:-1]
            values = values.split(',')
        if colname in measure_columns:
            values=list(map(revmap_dict.get,values))
        if self._pandas_flag:
            self._data_frame = self._data_frame[self._data_frame[colname].isin(values)]
        else:
            self._data_frame = self._data_frame.where(col(colname).isin(values))

    def values_not_in(self, colname, values,measure_columns):
        colname = colname.lstrip('0123456789. ')
        if type(values) == str:
            values = values[1:-1]
            values = values.split(',')
        if colname in measure_columns:
            values=list(map(revmap_dict.get,values))
        if self._pandas_flag:
            self._data_frame = self._data_frame[self._data_frame[colname].isin(values)==False]
        else:
            self._data_frame = self._data_frame.where(col(colname).isin(values)==False)

    def get_aggregated_result(self, colname, target):
        if self._pandas_flag:
            return self._data_frame.groupby([colname])[colname].agg(['count']).reset_index(inplace=False).values
        else:
            return self._data_frame.select(colname).groupBy(colname).agg({'*': 'count'}).collect()

    def get_count_result(self,target):
        if self._pandas_flag:
            return self._data_frame.groupby([target])[target].agg(['count']).reset_index(inplace=False).values
        else:
            return self._data_frame.groupBy(target).count().collect()

    def get_filtered_data_frame(self):
        return self._data_frame
