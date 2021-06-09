import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import OneHotEncoder
from pyspark.sql.functions import *
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator, VectorAssembler
from pyspark.sql.types import FloatType,IntegerType
import time as time
import numpy as np
import pyspark.sql.functions as F

class FeatureEngineeringAutoML():

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type,pandas_flag):
        self.data_frame = data_frame
        self.target = target
        self._pandas_flag = pandas_flag
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict['date_column_split'] = []
        self.data_change_dict['one_hot_encoded'] = []
        self.data_change_dict['label_encoded'] = []

    def date_column_split(self,col_list):
        """Splitting date column"""
        if self._pandas_flag:
            self.data_frame = self.data_frame.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)
            for col_name in col_list:
                column = str(col_name)
                self.data_frame[column + '_day'] = self.data_frame[column].dt.day
                self.data_frame[column + '_month'] = self.data_frame[column].dt.month
                self.data_frame[column + '_year'] = self.data_frame[column].dt.year
                self.data_frame[column + '_quarter'] = self.data_frame[column].dt.quarter
                self.data_frame[column + '_semester'] = np.where(self.data_frame[column + '_quarter'].isin([1, 2]), 1, 2)
                self.data_frame[column + '_day_of_the_week'] = self.data_frame[column].dt.dayofweek
                self.data_frame[column + '_time'] = self.data_frame[column].dt.time
                self.data_frame[column + '_day_of_the_year'] = self.data_frame[column].dt.dayofyear
                self.data_frame[column + '_week_of_the_year'] = self.data_frame[column].dt.weekofyear
                self.data_change_dict['date_column_split'].append(column)
        else:
            for col_name in col_list:
                column = str(col_name)
                self.data_frame = self.data_frame.withColumn(column +'_day',dayofmonth(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_frame = self.data_frame.withColumn(column +'_month',month(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_frame = self.data_frame.withColumn(column +'_years',year(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_frame = self.data_frame.withColumn(column +'_quarter',quarter(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_frame = self.data_frame.withColumn(column +'_semester',when(self.data_frame[column +'_quarter'].isin([1,2]), 1).otherwise(2))
                self.data_frame = self.data_frame.withColumn(column +'_dayofweek',dayofweek(column))
                self.data_frame = self.data_frame.withColumn(column +'_dayofyear',dayofyear(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_frame = self.data_frame.withColumn(column +'_weekofyear',weekofyear(to_timestamp(column, 'dd/MM/yyyy')))
                self.data_change_dict['date_column_split'].append(column)

    def one_hot_encoding(self, col_list):
        for col in col_list:
            dummy = enc.fit_transform(col)
            self.data_frame = pd.concat([self.data_frame,dummy], axis = 1)
            self.data_change_dict['one_hot_encoded'].append(col)
        #print(self.data_frame)
    def sk_one_hot_encoding(self,col_list):
        oh_enc = OneHotEncoder(sparse=False)
        new_df  = oh_enc.fit_transform(self.data_frame[col_list])
        uniq_vals = self.data_frame[col_list].apply(lambda x: x.value_counts()).unstack()
        uniq_vals = uniq_vals[~uniq_vals.isnull()]
        enc_cols = list(uniq_vals.index.map('{0[0]}_{0[1]}'.format))
        encoded_df=pd.DataFrame(new_df,columns=enc_cols,index=self.data_frame.index,dtype='int64')
        encoded_df.columns = [re.sub('\W+', '_', col.strip()) for col in encoded_df.columns]
        self.data_frame=self.data_frame[self.data_frame.columns.difference(col_list)]
        self.data_frame.reset_index(drop=True, inplace=True)
        encoded_df.reset_index(drop=True, inplace=True)
        self.data_frame = pd.concat([self.data_frame,encoded_df], axis = 1)
        self.data_change_dict['one_hot_encoded'] = col_list
        #print(self.data_frame)
    def pyspark_one_hot_encoding(self,col_list):
        for col in col_list:
            ss = StringIndexer(inputCol=col,outputCol=col+"_indexed")
            ss_fit = ss.fit(self.data_frame)
            self.data_frame = ss_fit.transform(self.data_frame)
            oe = OneHotEncoderEstimator(inputCols=[col+"_indexed"],outputCols=[col+"_indexed_encoded"])
            oe_fit = oe.fit(self.data_frame)
            self.data_frame = oe_fit.transform(self.data_frame)
            ith = udf(lambda v, i: float(v[i]), FloatType())
            for sidx, oe_col in zip([ss_fit], oe.getOutputCols()):
                for ii, val in list(enumerate(sidx.labels))[:-1]:
                    self.data_frame = self.data_frame.withColumn(sidx.getInputCol() + '_' + val, ith(oe_col, lit(ii)).astype(IntegerType()))
        self.data_frame = self.data_frame.drop(*col_list)
        cols = [re.sub('\W+','_', col.strip()) for col in self.data_frame.columns]
        self.data_frame = self.data_frame.toDF(*cols)
        self.data_change_dict['one_hot_encoded'] = col_list
    def cat_en_rule(self,cat_col):
        labels_count = [[len(self.data_frame.select(col).distinct().collect())-1,col] for col in cat_col]
        # labels_count = [[len(self.data_frame.agg((F.collect_set(col).alias(col))).first().asDict()[col])-1,col] for col in cat_col]
        labels_count.sort()
        dum_col = []
        n,p = self.data_frame.count(),len(self.data_frame.dtypes)
        for i in range(len(labels_count)):
            p = p + labels_count[i][0]
            if(int(np.sqrt(n)))>=p:
                dum_col.append(labels_count[i][1])
        label_col =  list(set(cat_col)-set(dum_col))
        return dum_col,label_col

    def pyspark_label_encoding(self,label_col):
        for col in label_col:
            ss = StringIndexer(inputCol=col,outputCol=col+"_labeled")
            ss_fit = ss.fit(self.data_frame)
            self.data_frame = ss_fit.transform(self.data_frame)
        self.data_frame = self.data_frame.drop(*label_col)
        self.data_change_dict['label_encoded'] = label_col



    def feature_engineering_run(self):
        start_time=time.time()
        self.date_column_split(self.datetime_cols)
        print("time taken for date column split:{} seconds".format((time.time()-start_time)))
        if not self._pandas_flag:
            #def translate(mapping):
            #    def translate_(col):
            #        return mapping.get(col)
            #   return udf(translate_, FloatType())
            #for column in self.dimension_cols:
            #    map_vals = self.data_frame.cube(column).count()
            #    map_dict = list(map(lambda row: row.asDict(), map_vals.collect()))
            #    if len(map_dict)<100:
            #        mapping = {feature[column]:feature['count']/self.data_frame.count() for feature in map_dict}
            #        self.data_frame = self.data_frame.withColumn("value_created", translate(mapping)(column))
            #        self.data_frame = self.data_frame.withColumn(column,when(self.data_frame.value_created >0.01 ,self.data_frame[column]).otherwise('other'))
            #        self.data_frame = self.data_frame.drop('value_created')
            #dum_col,label_col = self.cat_en_rule(self.dimension_cols)
            #if len(dum_col)>0:
            #    self.pyspark_one_hot_encoding(dum_col)
            #if len(label_col)>0:
            label_time=time.time()
            self.pyspark_label_encoding(self.dimension_cols)
            print("time taken for label encoding:{} seconds".format((time.time()-label_time)))
        else:
            self.data_frame = self.data_frame.apply(lambda x: x.mask(x.map(x.value_counts()/x.count())<0.01, 'other') if x.name in self.dimension_cols else x)
            self.sk_one_hot_encoding(self.dimension_cols)
