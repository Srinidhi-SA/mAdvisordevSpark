from __future__ import print_function
from __future__ import division
from builtins import zip
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import time
from datetime import datetime
import gc
import pandas as pd
import math
from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import regexp_extract
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import size
from pyspark.sql.functions import desc
from pyspark.sql.functions import isnan, when, count, col
from pyspark.sql.functions import unix_timestamp,to_timestamp,udf
from pyspark.sql.types import DateType

from bi.common import utils as CommonUtils
from bi.common.cardStructure import C3ChartData
from bi.common.charts import ChartJson, NormalChartData
from bi.common.decorators import accepts
from bi.settings import setting as GLOBALSETTINGS
from bi.stats.util import Stats


class MetaDataHelper(object):

    def __init__(self, df, rows):
        self.df = df
        self.rows = rows
        self._sample_data = self.set_sample_data()


    def get_binned_stat(self,df,colname,col_stat,n_split = 10):
        splits  = CommonUtils.frange(col_stat["min"],col_stat["max"],num_steps=n_split)
        splits = sorted(splits)
        splits[0] = splits[0] - 1
        splits[-1] = splits[-1] + 1
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
        splits_data = {"splits":splits,"splits_range":splits_range}
        splits = splits_data["splits"]
        double_df = df.withColumn(colname, df[colname].cast(DoubleType()))
        bucketizer = Bucketizer(inputCol=colname,outputCol="BINNED_INDEX")
        bucketizer.setSplits(splits)
        binned_df = bucketizer.transform(double_df)
        histogram_df = binned_df.groupBy("BINNED_INDEX").count().toPandas()
        str_splits_range = [" to ".join([str(x[0]),str(x[1])]) for x in splits_range]
        bin_name_dict = dict(list(zip(list(range(len(splits_range))),str_splits_range)))
        bin_name_dict[n_split] = "null"
        histogram_df["orderIndex"] = histogram_df["BINNED_INDEX"].apply(lambda x: n_split if pd.isnull(x) else x)
        histogram_df["bins"] = histogram_df["orderIndex"].apply(lambda x:bin_name_dict[int(x)])
        relevant_df = histogram_df[["bins","count","orderIndex"]]
        histogram_dict = list(relevant_df.T.to_dict().values())
        histogram_dict = sorted(histogram_dict,key=lambda x:x["orderIndex"])
        output = []
        for val in histogram_dict:
            output.append({"name":val["bins"],"value":val["count"]})
        return output

    def get_binned_stat_pandas(self, pandas_df, colname, col_stat, n_split = 10):
        splits  = CommonUtils.frange(col_stat["min"],col_stat["max"],num_steps=n_split)
        splits = sorted(splits)
        splits[0] = splits[0] - 1
        splits[-1] = splits[-1] + 1
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
        splits_data = {"splits":splits,"splits_range":splits_range}
        splits = splits_data["splits"]
        pandas_df[colname] = pandas_df[colname].astype(float)
        single_col_df =  pandas_df[[colname]]
        single_col_df["BINNED_INDEX"] = pd.cut(single_col_df[colname],splits,labels=list(range(0,len(splits)-1)))
        histogram_df = single_col_df.groupby("BINNED_INDEX").count()
        histogram_df["BINNED_INDEX"] = histogram_df.index.tolist()
        histogram_df.columns = ['count','BINNED_INDEX']
        str_splits_range = [" to ".join([str(x[0]),str(x[1])]) for x in splits_range]
        bin_name_dict = dict(list(zip(list(range(len(splits_range))),str_splits_range)))
        bin_name_dict[n_split] = "null"
        histogram_df["orderIndex"] = histogram_df["BINNED_INDEX"].apply(lambda x: n_split if pd.isnull(x) else x)
        histogram_df["bins"] = histogram_df["orderIndex"].apply(lambda x:bin_name_dict[int(x)])
        relevant_df = histogram_df[["bins","count","orderIndex"]]
        histogram_dict = list(relevant_df.T.to_dict().values())
        histogram_dict = sorted(histogram_dict,key=lambda x:x["orderIndex"])
        output = []
        for val in histogram_dict:
            output.append({"name":val["bins"],"value":val["count"]})
        return output


    def calculate_measure_column_stats_pandas(self, pandas_df, column, summary_df, total_count, binned_stat_flag, chart_data):
        df1 = pandas_df[column]
        col_stat = dict(list(zip(summary_df["summary"], summary_df[column])))
        col_summary = df1.describe()
        outlier_LR, outlier_UR = col_summary["mean"] - (3*col_summary["std"]), col_summary["mean"] + (3*col_summary["std"])
        outlier = len(df1[(df1 > outlier_UR) | (df1 < outlier_LR)])

        for k,v in list(col_stat.items()):
            if "." in str(v):
                col_stat[k] = round(float(v),2)
            elif v != "NaN":
                col_stat[k] = int(v)
            else:
                col_stat[k] = v
        col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]*100.0, (total_count))), 3) ) + "%"
        col_stat["numberOfNotNulls"] = col_stat["count"]
        col_stat["numberOfUniqueValues"] = df1.dropna().nunique()
        if col_stat["numberOfNulls"] > 0:
            col_stat["numberOfUniqueValues"]=col_stat["numberOfUniqueValues"] +1
        col_stat["Outliers"] = outlier
        if math.isnan(outlier_LR):
            col_stat["OutlierLR"] = None
        else:
            col_stat["OutlierLR"] = outlier_LR
        if math.isnan(outlier_UR):
            col_stat["OutlierUR"] = None
        else:
            col_stat["OutlierUR"] = outlier_UR

        if round((old_div(col_stat["numberOfNulls"]*100.0, (total_count))), 3) <=90:
            if col_stat["numberOfUniqueValues"] <= GLOBALSETTINGS.UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION:
                fs1 = time.time()
                levelCount = dict(df1.value_counts())
                levelCount = {str(k):v for k,v in list(levelCount.items())}
                if col_stat["numberOfNulls"] > 0:
                    levelCount[None]=col_stat["numberOfNulls"]
                col_stat["LevelCount"] = levelCount
                print("TIME FOR MEASURE LEVEL COUNT - " + column, time.time() - fs1, "Seconds")
            if binned_stat_flag:
                st = time.time()
                measure_chart_data = self.get_binned_stat_pandas(pandas_df, column, col_stat)
                print("BINNED STAT FOR - " + column, time.time() - st)
                measure_chart_data = sorted(measure_chart_data,key=lambda x:x["value"],reverse=True)
                measure_chart_obj = ChartJson(NormalChartData(measure_chart_data).get_data(),chart_type="bar")
                measure_chart_obj.set_axes({"x":"name","y":"value"})
                measure_chart_obj.set_subchart(False)
                measure_chart_obj.set_hide_xtick(True)
                measure_chart_obj.set_show_legend(False)
                chart_data = C3ChartData(data=measure_chart_obj)
            else:
                chart_data = {}
        else:
            chart_data = {}

        # print "<>"*40
        # print "COLUMN - ", column
        # print "-"*40
        # print "COL STAT - ", col_stat
        # print "-"*40
        # print "<>"*40

        return col_stat, chart_data

    def calculate_measure_column_stats_pyspark(self, pyspark_df, column, summary_df, total_count, binned_stat_flag, chart_data):
        df1 = pyspark_df.select(column)
        col_stat = dict(list(zip(summary_df["summary"], summary_df[column])))

        outlier, outlier_LR, outlier_UR = Stats.detect_outliers_z(df1, column)
        for k,v in list(col_stat.items()):
            if "." in v:
                col_stat[k] = round(float(v),2)
            elif v != "NaN":
                col_stat[k] = int(v)
            else:
                col_stat[k] = v
        col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]*100.0, (total_count))), 3)) + "%"
        col_stat["numberOfNotNulls"] = col_stat["count"]
        col_stat["numberOfUniqueValues"] = df1.select(column).distinct().count()
        col_stat["Outliers"] = outlier
        if math.isnan(outlier_LR):
            col_stat["OutlierLR"] = None
        else:
            col_stat["OutlierLR"] = outlier_LR
        if math.isnan(outlier_UR):
            col_stat["OutlierUR"] = None
        else:
            col_stat["OutlierUR"] = outlier_UR

        if round((old_div(col_stat["numberOfNulls"]*100.0, (total_count))), 3) <=90:
            if col_stat["numberOfUniqueValues"] <= GLOBALSETTINGS.UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION:
                fs1 = time.time()
                levelCount = df1.groupBy(column).count().sort(desc("count")).limit(20)
                levelCount = [row.asDict() for row in levelCount.collect()]
                l = {}
                for level in levelCount:
                    l[level[column]] = level['count']
                levelCount =  l
                col_stat["LevelCount"] = levelCount
                print("TIME FOR MEASURE LEVEL COUNT - " + column, time.time() - fs1, "Seconds")
            if binned_stat_flag:
                st = time.time()
                measure_chart_data = self.get_binned_stat(df1, column, col_stat)
                print("BINNED STAT FOR - " + column, time.time() - st, "Seconds")
                measure_chart_data = sorted(measure_chart_data,key=lambda x:x["value"],reverse=True)
                measure_chart_obj = ChartJson(NormalChartData(measure_chart_data).get_data(),chart_type="bar")
                measure_chart_obj.set_axes({"x":"name","y":"value"})
                measure_chart_obj.set_subchart(False)
                measure_chart_obj.set_hide_xtick(True)
                measure_chart_obj.set_show_legend(False)
                chart_data = C3ChartData(data=measure_chart_obj)
            else:
                chart_data = {}
        else:
            chart_data = {}

        # print "<>"*40
        # print "COLUMN - ", column
        # print "-"*40
        # print "COL STAT - ", col_stat
        # print "-"*40
        # print "<>"*40

        return col_stat, chart_data

    def calculate_measure_column_stats_per_column(self, df, pandas_df, column, summary_df, total_count, binned_stat_flag, displayNameDict, displayOrderDict, output, chart_data, pandas_flag):
        st = time.time()
        if pandas_flag:
            try:
                col_stat, chart_data = self.calculate_measure_column_stats_pandas(pandas_df, column, summary_df, total_count, binned_stat_flag, chart_data)
            except:
                col_stat, chart_data = self.calculate_measure_column_stats_pyspark(df, column, summary_df, total_count, binned_stat_flag, chart_data)
        else:
            col_stat, chart_data = self.calculate_measure_column_stats_pyspark(df, column, summary_df, total_count, binned_stat_flag, chart_data)
        output = []
        for k,v in list(col_stat.items()):
            if k not in ["numberOfNotNulls","LevelCount","OutlierLR","OutlierUR"]:
                output.append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
            else:
                output.append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
        output = sorted(output,key=lambda x:displayOrderDict[x["name"]])
        print("MEASURE STATS FOR COLUMN - "+ column, time.time() - st, "Seconds")
        return output, chart_data

    def calculate_measure_column_stats(self, df, measure_columns, **kwargs):
        i = 0
        pandas_flag = True
        if kwargs["pandas_flag"]:
            n_rows, n_cols = df.shape[0], len(df.columns)
            binned_stat_flag = True
            xtraArgs = {}
            for key in kwargs:
                xtraArgs[key] =  kwargs[key]
            if "binColumn" in xtraArgs:
                binned_stat_flag = xtraArgs["binColumn"]
            df = df[measure_columns]
            pandas_df = df.copy()
            total_count = df.shape[0]
            output = {}
            chart_data = {}
            if measure_columns:
                summary_df = df.describe()
                summary_df.drop(index=["25%", "50%", "75%"], inplace=True)
                summary_df.rename(index={'std': 'stddev'}, inplace=True)
                summary_df=summary_df.reset_index()
                summary_df.rename(columns={'index': 'summary'}, inplace=True)
            else:
                summary_df = None
        else:
            n_rows, n_cols = df.count(), len(df.columns)
            if n_rows < 100000 and n_cols < 500:
                pandas_flag = True
            else:
                pandas_flag = False
            binned_stat_flag = True
            xtraArgs = {}
            for key in kwargs:
                xtraArgs[key] =  kwargs[key]
            if "binColumn" in xtraArgs:
                binned_stat_flag = xtraArgs["binColumn"]
            df = df.select(measure_columns)
            if pandas_flag:
                pandas_df = df.toPandas()
            total_count = df.count()
            output = {}
            chart_data = {}
            ## TODO : Remove if pyspark df doesnt need this.
            if pandas_flag:
                if measure_columns:
                    ## was done cause preprocessing and feature Engineering was done on pandas to handle NA
                    summary_df = pandas_df.describe()
                    summary_df.drop(index=["25%","50%","75%"],inplace = True)
                    summary_df.rename(index={'std': 'stddev'}, inplace=True)
                    summary_df=summary_df.reset_index()
                    summary_df.rename(columns={'index': 'summary'}, inplace=True)
            else :
                if len(measure_columns) > 0:
                    summary_df = df.describe().toPandas()
                else:
                    summary_df = None
        displayNameDict = {
                            "count":"Count",
                            "mean":"Mean",
                            "stddev":"Standard Deviation",
                            "min":"Min",
                            "max":"Max",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls",
                            "LevelCount":"Unique Values",
                            "Outliers":"Outliers",
                            "OutlierLR":"OutlierLR",
                            "OutlierUR":"OutlierUR",
                            "percentOfNulls": "Percent Nulls"
                            }
        displayOrderDict = {"min":0,"max":1,"mean":2,"stddev":3,"numberOfUniqueValues":4,"numberOfNulls":5,
                            "numberOfNotNulls":7,"count":8,"LevelCount":9,"Outliers":10,"OutlierLR":11,"OutlierUR":12,
                            "percentOfNulls": 6}




        print("+"*60)
        print("NUMBER OF ROWS - ", n_rows)
        print("NUMBER OF COLUMNS - ", n_cols)
        print("MEASURE COLUMNS - ", measure_columns)
        print("+"*60)
        for column in measure_columns:
            print("COLUMN NUMBER IN MEASURE - ", i)
            i+=1
            if pandas_flag or kwargs["pandas_flag"]:
                output[column],chart_data[column] = self.calculate_measure_column_stats_per_column(df, pandas_df, column, summary_df, total_count, binned_stat_flag, displayNameDict, displayOrderDict, output, chart_data, pandas_flag)
            else:
                output[column],chart_data[column] = self.calculate_measure_column_stats_per_column(df, None, column, summary_df, total_count, binned_stat_flag, displayNameDict, displayOrderDict, output, chart_data, False)
        return output, chart_data

    def calculate_dimension_column_stats_pandas(self, pandas_df, column, summary_df, total_count, level_count_flag, chart_data):
        df1 = pandas_df[column]
        col_stat = {}
        col_stat["numberOfNulls"] = df1.isnull().sum()
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]  * 100.0, (total_count))), 3)) + "%"
        col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
        col_stat["numberOfUniqueValues"] = df1.dropna().nunique()

        if col_stat["numberOfNulls"] > 0:
            col_stat["numberOfUniqueValues"]= col_stat["numberOfUniqueValues"] +1
        if round((old_div(col_stat["numberOfNulls"] * 100.0, (total_count))), 3) <= 90:
            if level_count_flag:
                fs1 = time.time()
                levelCount = {}
                if col_stat["numberOfUniqueValues"] <= GLOBALSETTINGS.UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION_DIMENSION:
                    levelCount = dict(df1.value_counts())
                    levelCount = {str(k):v for k,v in list(levelCount.items())}
                    if col_stat["numberOfNulls"] > 0:
                        levelCount[None]=col_stat["numberOfNulls"]
                    col_stat["LevelCount"] = levelCount
                    levelCountWithoutNull = levelCount
                    if None in levelCount:
                        levelCountWithoutNull.pop(None)
                    if levelCountWithoutNull != {}:
                        col_stat["MaxLevel"] = str(max(levelCountWithoutNull,key=levelCount.get))
                        col_stat["MinLevel"] = str(min(levelCountWithoutNull,key=levelCount.get))
                    else:
                        col_stat["MaxLevel"] = None
                        col_stat["MinLevel"] = None
                else:
                    levelCount = dict(df1.value_counts())
                    levelCount = {str(k):v for k,v in list(levelCount.items())}
                    col_stat["LevelCount"] = levelCount

                print("TIME FOR LEVEL COUNT - " + column, time.time() - fs1, "Seconds")
                dimension_chart_data = [{"name":str(k),"value":v} if k != None else {"name":"null","value":v} for k,v in list(levelCount.items())]
                dimension_chart_data = sorted(dimension_chart_data,key=lambda x:x["value"],reverse=True)
                dimension_chart_obj = ChartJson(NormalChartData(dimension_chart_data).get_data(),chart_type="bar")
                dimension_chart_obj.set_axes({"x":"name","y":"value"})
                dimension_chart_obj.set_subchart(False)
                dimension_chart_obj.set_hide_xtick(True)
                dimension_chart_obj.set_show_legend(False)
                chart_data[column] = C3ChartData(data=dimension_chart_obj)
            else:
                col_stat = dict(list(zip(summary_df["summary"],summary_df[column])))
                col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
                col_stat["numberOfUniqueValues"] = None
                col_stat["MaxLevel"] = str(col_stat["max"])
                col_stat["MinLevel"] = str(col_stat["min"])
                chart_data[column] = {}
        else:
            chart_data[column] = {}
            levelCount = {}
            col_stat["LevelCount"] = levelCount

        # print "<>"*40
        # print "COLUMN - ", column
        # print "-"*40
        # print "COL STAT - ", col_stat
        # print "-"*40
        # print "<>"*40

        return col_stat, chart_data[column]

    def calculate_dimension_column_stats_pyspark(self, pyspark_df, column, summary_df, total_count, level_count_flag, chart_data):
        df1 = pyspark_df.select(column)
        st = time.time()
        col_stat = {}

        '''PYSPARK'''
        try:
            nullcnt = df1.select(count(when(isnan(column) | col(column).isNull(), column)).alias(column))
        except:
            nullcnt = df1.select(count(when(col(column).isNull(), column)).alias(column))
        col_stat["numberOfNulls"] = nullcnt.rdd.flatMap(list).first()
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]  * 100.0, (total_count))), 3)) + "%"
        col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
        col_stat["numberOfUniqueValues"] = df1.select(column).distinct().count()

        if round((old_div(col_stat["numberOfNulls"]  * 100.0, (total_count))), 3) <=90:
            if level_count_flag:
                fs1 = time.time()
                levelCount = {}

                levelCount = df1.groupBy(column).count().sort(desc("count")).limit(20)
                levelCount = [row.asDict() for row in levelCount.collect()]
                l = {}
                for level in levelCount:
                    l[level[column]] = level['count']
                levelCount =  l
                col_stat["LevelCount"] = levelCount
                levelCountBig = df1.groupBy(column).count().sort(("count"))
                col_stat["MinLevel"] = str(levelCountBig.select(column).rdd.take(1)[0][0])
                levelCountBig = df1.groupBy(column).count().sort(desc("count"))
                col_stat["MaxLevel"] = str(levelCountBig.select(column).rdd.take(1)[0][0])

                print("TIME FOR LEVEL COUNT - " + column, time.time() - fs1, "Seconds")
                dimension_chart_data = [{"name":str(k),"value":v} if k != None else {"name":"null","value":v} for k,v in list(levelCount.items())]
                dimension_chart_data = sorted(dimension_chart_data,key=lambda x:x["value"],reverse=True)
                dimension_chart_obj = ChartJson(NormalChartData(dimension_chart_data).get_data(),chart_type="bar")
                dimension_chart_obj.set_axes({"x":"name","y":"value"})
                dimension_chart_obj.set_subchart(False)
                dimension_chart_obj.set_hide_xtick(True)
                dimension_chart_obj.set_show_legend(False)
                chart_data[column] = C3ChartData(data=dimension_chart_obj)
            else:
                col_stat = dict(list(zip(summary_df["summary"],summary_df[column])))
                col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
                col_stat["numberOfUniqueValues"] = None
                col_stat["MaxLevel"] = str(col_stat["max"])
                col_stat["MinLevel"] = str(col_stat["min"])
                chart_data[column] = {}
        else:
            chart_data[column] = {}
            levelCount = {}
            col_stat["LevelCount"] = levelCount

        # print "COL STAT [LEVEL COUNT]", col_stat["LevelCount"]
        # print "-"*40
        # print "<>"*40

        return col_stat, chart_data[column]

    def calculate_dimension_column_stats_per_column(self, df, pandas_df, column, summary_df, total_count, level_count_flag, displayNameDict, displayOrderDict, output, chart_data, pandas_flag):
        st = time.time()
        if pandas_flag:
            try:
                col_stat, chart_data[column] = self.calculate_dimension_column_stats_pandas(pandas_df, column, summary_df, total_count, level_count_flag, chart_data)
            except:
                col_stat, chart_data[column] = self.calculate_dimension_column_stats_pyspark(df, column, summary_df, total_count, level_count_flag, chart_data)
        else:
            col_stat, chart_data[column] = self.calculate_dimension_column_stats_pyspark(df, column, summary_df, total_count, level_count_flag, chart_data)
        output[column] = []
        for k,v in list(col_stat.items()):
            if k not in ["LevelCount","numberOfNotNulls"]:
                output[column].append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
            else:
                output[column].append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
        output[column] = sorted(output[column],key=lambda x:displayOrderDict[x["name"]])
        print("DIMENSION STATS FOR COLUMN - "+ column, time.time() - st, "Seconds")
        return output[column], chart_data[column]

    def calculate_dimension_column_stats(self, df, dimension_columns, **kwargs):
        i = 0
        level_count_flag = True
        pandas_flag = True
        xtraArgs = {}
        for key in kwargs:
            xtraArgs[key] =  kwargs[key]
        if "levelCount" in xtraArgs:
            level_count_flag = xtraArgs["levelCount"]
        if xtraArgs["pandas_flag"]:
            df = df[dimension_columns]
            n_rows, n_cols = df.shape[0], len(df.columns)
            pandas_df = df.copy()
            total_count = df.shape[0]
            output = {}
            chart_data = {}
            if dimension_columns:
                summary_df = df.describe()
                summary_df = summary_df.reset_index()
                summary_df.rename(columns={'index': 'summary'}, inplace=True)
            else:
                summary_df = None
        else:
            df = df.select(dimension_columns)
            n_rows, n_cols = df.count(), len(df.columns)
            if n_rows < 100000 and n_cols < 500:
                pandas_flag = True
            else:
                pandas_flag = False
            if pandas_flag:
                pandas_df = df.toPandas()
            total_count = df.count()
            output = {}
            chart_data = {}
            if len(dimension_columns) > 0:
                summary_df = df.describe().toPandas()
            else:
                summary_df = None
        displayNameDict = {
                            "count":"Count",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls",
                            "MaxLevel":"Max Level",
                            "MinLevel":"Min Level",
                            "LevelCount":"LevelCount",
                            "percentOfNulls": "Percent Nulls"
                            }

        displayOrderDict = {"MinLevel": 0, "MaxLevel": 1, "numberOfUniqueValues": 2, "numberOfNulls": 3,
                            "numberOfUniqueValues": 5, "numberOfNotNulls": 6, "count": 7, "LevelCount": 8, "percentOfNulls": 4}


        print("+"*60)
        print("NUMBER OF ROWS - ", n_rows)
        print("NUMBER OF COLUMNS - ", n_cols)
        print("DIMENSION COLUMNS - ", dimension_columns)
        print("+"*60)

        for column in dimension_columns:
            print("COLUMN NUMBER IN DIMENSION - ", i)
            i+=1
            if pandas_flag or xtraArgs["pandas_flag"]:
                output[column], chart_data[column] = self.calculate_dimension_column_stats_per_column(df, pandas_df, column, summary_df, total_count, level_count_flag, displayNameDict, displayOrderDict, output, chart_data, pandas_flag)
            else:
                output[column], chart_data[column] = self.calculate_dimension_column_stats_per_column(df,None, column, summary_df, total_count, level_count_flag,displayNameDict, displayOrderDict, output, chart_data,False)

        return output, chart_data

    def calculate_time_dimension_column_stats_pandas(self, pandas_df, column, total_count, level_count_flag, chart_data,unprocessed_columns):
        df1 = pandas_df[column]
        col_stat = {}
        col_stat["numberOfNulls"] = df1.isnull().sum()
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]  * 100.0, (total_count))), 3)) + "%"
        col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
        col_stat["numberOfUniqueValues"] = df1.dropna().nunique()
        if col_stat["numberOfNulls"] > 0:
            col_stat["numberOfUniqueValues"]= col_stat["numberOfUniqueValues"] +1
        try:
            if round((old_div(col_stat["numberOfNulls"]*100.0, total_count)), 3) <= 80:
                uniqueVals = df1.dropna().unique()
                first_date = str((pd.to_datetime(min(uniqueVals))).date())
                last_date = str((pd.to_datetime(max(uniqueVals))).date())
                col_stat["firstDate"] = first_date
                col_stat["lastDate"] = last_date
                col_stat["count"] = total_count - col_stat["numberOfNulls"]
                if level_count_flag:
                    fs1 = time.time()
                    levelCount = {}
                    levelCount = dict(df1.value_counts())
                    levelCount = {str(k):v for k,v in list(levelCount.items())}
                    col_stat["LevelCount"] = levelCount
                    col_stat["MinLevel"] = first_date
                    col_stat["MaxLevel"] = last_date

                    dimension_chart_data = [{"name":k,"value":v} if k != None else {"name":"null","value":v} for k,v in list(levelCount.items())]
                    dimension_chart_data = sorted(dimension_chart_data,key=lambda x:x["value"],reverse=True)
                    dimension_chart_obj = ChartJson(NormalChartData(dimension_chart_data).get_data(),chart_type="bar")
                    dimension_chart_obj.set_axes({"x":"name","y":"value"})
                    dimension_chart_obj.set_subchart(False)
                    dimension_chart_obj.set_hide_xtick(True)
                    dimension_chart_obj.set_show_legend(False)
                    chart_data[column] = C3ChartData(data=dimension_chart_obj)

                else:
                    col_stat["firstDate"] = first_date
                    col_stat["lastDate"] = last_date
                    chart_data[column] = {}
            else:
                chart_data[column] = {}
        except:
            print("could not process column: ",column)
            unprocessed_columns.append(column)
            chart_data[column] = {}
        return col_stat, chart_data[column],unprocessed_columns

    def calculate_time_dimension_column_stats_pyspark(self, pyspark_df, column, total_count, level_count_flag, chart_data,unprocessed_columns):
        df1 = pyspark_df.select(column)
        col_stat = {}
        nullcnt = df1.select(count(when(col(column).isNull(), column)).alias(column))
        col_stat["numberOfNulls"] = nullcnt.rdd.flatMap(list).first()
        col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
        col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]*100.0, total_count)), 3)) + "%"
        col_stat["numberOfUniqueValues"] = df1.select(column).distinct().count()
        try:
            if round((old_div(col_stat["numberOfNulls"]*100.0, total_count)), 3) <=80:
                uniqueVals = df1.select(column).distinct().na.drop().limit(100).collect()
                notNullDf = df1.select(column).distinct().na.drop()
                notNullDf = notNullDf.orderBy([column],ascending=[True])
                notNullDf = notNullDf.withColumn("_id_", monotonically_increasing_id())
                id_max = notNullDf.select("_id_").rdd.max()[0]
                first_date = notNullDf.select(column).first()[0]
                first_date = pd.to_datetime(first_date).date()
                try:
                    last_date = notNullDf.where(col("_id_") == id_max).select(column).first()[0]
                    last_date = pd.to_datetime(last_date).date()
                except:
                    pandas_df = notNullDf.select(["_id_",column]).toPandas()
                    pandas_df.sort_values(by=column,ascending=True,inplace=True)
                    last_date = str(pandas_df[column].iloc[-1].date())
                col_stat["firstDate"] = first_date
                col_stat["lastDate"] = last_date
                col_stat["count"] = notNullDf.count()
                if level_count_flag:
                    fs1 = time.time()
                    levelCount = {}
                    levelCount = list(df1.groupBy(column).count().sort(desc("count")).limit(12).toPandas().set_index(column).to_dict().values())[0]
                    levelCount = {str(k):v for k,v in list(levelCount.items())}
                    col_stat["LevelCount"] = levelCount
                    col_stat["MinLevel"] = first_date
                    col_stat["MaxLevel"] = last_date

                    dimension_chart_data = [{"name":k,"value":v} if k != None else {"name":"null","value":v} for k,v in list(levelCount.items())]
                    dimension_chart_data = sorted(dimension_chart_data,key=lambda x:x["value"],reverse=True)
                    dimension_chart_obj = ChartJson(NormalChartData(dimension_chart_data).get_data(),chart_type="bar")
                    dimension_chart_obj.set_axes({"x":"name","y":"value"})
                    dimension_chart_obj.set_subchart(False)
                    dimension_chart_obj.set_hide_xtick(True)
                    dimension_chart_obj.set_show_legend(False)
                    chart_data[column] = C3ChartData(data=dimension_chart_obj)

                else:
                    col_stat["firstDate"] = first_date
                    col_stat["lastDate"] = last_date
                    chart_data[column] = {}
            else:
                chart_data[column] = {}
        except:
            print("could not process column: ",column)
            unprocessed_columns.append(column)
            chart_data[column] = {}
        return col_stat, chart_data[column],unprocessed_columns

    def calculate_time_dimension_column_stats_per_column(self, df, pandas_df, column, total_count, level_count_flag, displayNameDict, displayOrderDict, chart_data, output, pandas_flag,unprocessed_columns):
        st = time.time()
        if pandas_flag:
            try:
                col_stat, chart_data[column],unprocessed_columns = self.calculate_time_dimension_column_stats_pandas(pandas_df, column, total_count, level_count_flag, chart_data,unprocessed_columns)
            except:
                col_stat, chart_data[column],unprocessed_columns = self.calculate_time_dimension_column_stats_pyspark(df, column, total_count, level_count_flag, chart_data,unprocessed_columns)
        else:
            col_stat, chart_data[column],unprocessed_columns = self.calculate_time_dimension_column_stats_pyspark(df, column, total_count, level_count_flag, chart_data,unprocessed_columns)

        output[column] = []
        for k,v in list(col_stat.items()):
            if k not in ["LevelCount","numberOfNotNulls","MaxLevel","MinLevel"]:
                output[column].append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
            else:
                output[column].append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
        output[column] = sorted(output[column],key=lambda x:displayOrderDict[x["name"]])
        print("TIME DIMENSION STATS FOR COLUMN - "+ column, time.time() - st, "Seconds")
        return output[column], chart_data[column],unprocessed_columns

    def calculate_time_dimension_column_stats(self, df, td_columns, **kwargs):
        i = 0
        level_count_flag = True
        pandas_flag = True
        xtraArgs = {}
        for key in kwargs:
            xtraArgs[key] =  kwargs[key]
        if "level_count_flag" in xtraArgs:
            level_count_flag = xtraArgs[key]
        if xtraArgs["pandas_flag"]:
            df = df[td_columns]
            pandas_df = df.copy()
            total_count = df.shape[0]
            output = {}
            chart_data = {}
            unprocessed_columns = []
            n_rows, n_cols = df.shape[0], len(df.columns)
        else:
            df = df.select(td_columns)
            pandas_df = df.toPandas()
            total_count = df.count()
            output = {}
            chart_data = {}
            unprocessed_columns=[]
            n_rows, n_cols = df.count(), len(df.columns)
            if n_rows < 100000 and n_cols < 500:
                pandas_flag = True
            else:
                pandas_flag = False
        displayNameDict = {
                            "count":"Count",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls",
                            "MaxLevel":"Max Level",
                            "MinLevel":"Min Level",
                            "LevelCount":"LevelCount",
                            "firstDate":"Start Date",
                            "lastDate":"Last Date",
                            "percentOfNulls": "Percent Nulls"
                            }
        # TODO: FIX copy paste error numberOfUniqueValues
        displayOrderDict = {"firstDate": 0, "lastDate": 1, "MinLevel": 9, "MaxLevel": 10, "numberOfUniqueValues": 2,
                            "numberOfNulls": 3, "numberOfUniqueValues": 5, "numberOfNotNulls": 6, "count": 7, "LevelCount": 8, "percentOfNulls": 4}


        print("+"*60)
        print("TIME DIMENSION COLUMNS - ", td_columns)
        print("+"*60)
        for column in td_columns:
            print("COLUMN NUMBER IN TIME DIMENSION - ", i)
            i+=1
            output[column], chart_data[column],unprocessed_columns = self.calculate_time_dimension_column_stats_per_column(df, pandas_df, column, total_count, level_count_flag, displayNameDict, displayOrderDict, chart_data, output, pandas_flag,unprocessed_columns)
        return output, chart_data,unprocessed_columns

    # def get_datetime_suggestions(self,df,col_name):
    #     output = {}
    #     date_time_suggestions = {}
    #     formats = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["formats"]
    #     dual_checks = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["dual_checks"]
    #     row_vals = df.select(col_name).distinct().na.drop().collect()
    #     # row_vals = df.select(dims).na.drop().take(int(self.total_rows**0.5 + 1))
    #     if len(row_vals) > 0:
    #         x = row_vals[0][col_name]
    #         for format1 in formats:
    #             try:
    #                 t = datetime.strptime(x,format1)
    #                 # if (format1 in dual_checks):
    #                 #     for x1 in row_vals:
    #                 #         x = x1[dims]
    #                 #         try:
    #                 #             t = dt.datetime.strptime(x,format1)
    #                 #         except ValueError as err:
    #                 #             format1 = '%d'+format1[2]+'%m'+format1[5:]
    #                 #             break
    #                 output[col_name] = format1
    #                 break
    #             except ValueError as err:
    #                 pass
    #     return output

    def get_datetime_format(self,columnVector):
        """
        suggest candidate for datetime column.
        checks against a list of datetime formats

        Arguments:
        columnVector -- an array of strings of any size.

        Return:
        detectedFormat -- datetime format
        """
        detectedFormat = None
        # availableDateTimeFormat = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["formats"]
        # sample1 = str(columnVector[0])
        # for dt_format in availableDateTimeFormat:
        #     try:
        #         t = datetime.strptime(sample1,dt_format)
        #         detectedFormat = dt_format
        #         break
        #     except ValueError as err:
        #         pass
        formats = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["formats"]
        dual_checks = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["dual_checks"]
        if columnVector[0] == None and  len(columnVector)>1:
            x = columnVector[1]
        elif columnVector[0] != None:
            x = columnVector[0]
        else:
            return detectedFormat
        for format1 in formats:
            try:
                t = datetime.strptime(x,format1)
                if (format1 in dual_checks):
                    for x1 in columnVector:
                        if x1 != None:
                            try:
                                t = datetime.strptime(x1,format1)
                            except ValueError as err:
                                format1 = '%d'+format1[2]+'%m'+format1[5:]
                                break
                        else:
                            pass
                detectedFormat = format1
                break
            except ValueError as err:
                pass
        return detectedFormat

    def get_datetime_format_pandas(self,columnVector):
        """
        suggest candidate for datetime column.
        checks against a list of datetime formats

        Arguments:
        columnVector -- an array of strings of any size.

        Return:
        detectedFormat -- datetime format
        """
        detectedFormat = None
        # availableDateTimeFormat = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["formats"]
        # sample1 = str(columnVector[0])
        # for dt_format in availableDateTimeFormat:
        #     try:
        #         t = datetime.strptime(sample1,dt_format)
        #         detectedFormat = dt_format
        #         break
        #     except ValueError as err:
        #         pass
        formats = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["formats"]
        dual_checks = GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["dual_checks"]
        if columnVector[0] == None and  len(columnVector)>1:
            x = columnVector[1]
        elif columnVector[0] != None:
            x = columnVector[0]
        else:
            return detectedFormat
        for format1 in formats:
            try:
                t = datetime.strptime(str(x),str(format1))
                if (format1 in dual_checks):
                    for x1 in columnVector:
                        if x1 != None:
                            try:
                                t = datetime.strptime(str(x1),str(format1))
                            except ValueError as err:
                                format1 = '%d'+format1[2]+'%m'+format1[5:]
                                break
                        else:
                            pass
                detectedFormat = format1
                break
            except ValueError as err:
                pass
        return detectedFormat


    def get_ignore_column_suggestions(self,df,total_rows,column_name,dataType,colStat,max_levels=100):
        ignore = False
        reason = None
        modifiedColStat = {}
        for obj in colStat:
            modifiedColStat[obj["name"]] = obj["value"]
        colStat = modifiedColStat
        if dataType == "measure":
            if (colStat["numberOfUniqueValues"]==1):
                ignore = True
                reason = "Only one Unique Value"
            if "Duplicate" in colStat:
                if (colStat["Duplicate"] != None):
                    ignore = True
                    reason = "Column is a duplicate of "+str(colStat["Duplicate"])
            if (colStat["numberOfNulls"] > 0):
                if (colStat["numberOfUniqueValues"]==2):
                    ignore = True
                    reason = "Only one Unique Value"
            if (colStat["numberOfNulls"] == 0):
                try:
                    if (colStat["numberOfUniqueValues"] == total_rows) and (df.schema[column_name].dataType == 'IntegerType'):
                        ignore = True
                        reason = "Index column (all values are distinct)"
                except:
                    if (colStat["numberOfUniqueValues"] == total_rows) and (df[column_name].dtype in ['int32','int16','int64']):
                        ignore = True
                        reason = "Index column (all values are distinct)"

            else:
                if (colStat["numberOfNulls"] > colStat["numberOfNotNulls"]):
                    ignore = True
                    reason = "Count of Nulls More than Count of Not Nulls"
                # handling cases where some ids will be missing
                elif (colStat["numberOfNotNulls"] <= 0.01*colStat["numberOfUniqueValues"]):
                    ignore = True
                    reason = "Index Column(Most of Not Null Values are unique)"

        elif dataType == "dimension":
            if (colStat["numberOfUniqueValues"]==1):
                ignore = True
                reason = "Only one Unique Value"
            if "Duplicate" in colStat:
                if (colStat["Duplicate"] != None):
                    ignore = True
                    reason = "Column is a duplicate of "+str(colStat["Duplicate"])
            if (colStat["numberOfNulls"] == 0):
                if (colStat["numberOfUniqueValues"] == total_rows):
                    ignore = True
                    reason = "Index Column (all values are distinct)"
            else:
                if (colStat["numberOfNulls"] > colStat["numberOfNotNulls"]):
                    ignore = True
                    reason = "Count of Nulls More than Count of Not Nulls"
                elif (colStat["numberOfNotNulls"]==1):
                    ignore = True
                    reason = "Only one Not Null value"
                elif colStat["numberOfUniqueValues"] > max_levels:
                    ignore = True
                    reason = "Number of Levels are more than the defined thershold"

        elif dataType == "datetime":
            if (colStat["numberOfUniqueValues"]==1):
                ignore = True
                reason = "Only one Unique Value"
            if "Duplicate" in colStat:
                if (colStat["Duplicate"] != None):
                    ignore = True
                    reason = "Column is a duplicate of "+str(colStat["Duplicate"])
            if (colStat["numberOfNulls"] == 0):
                if (colStat["numberOfUniqueValues"] == total_rows):
                    ignore = True
                    reason = "Index Column (all values are distinct)"
            else:
                if (colStat["numberOfNulls"] > colStat["numberOfNotNulls"]):
                    ignore = True
                    reason = "Count of Nulls More than Count of Not Nulls"
                elif (colStat["numberOfNotNulls"]==1):
                    ignore = True
                    reason = "Only one Not Null value"
        return ignore,reason


    def get_utf8_suggestions(self,colStat):
        utf8 = False
        modifiedColStat = {}
        for obj in colStat:
            modifiedColStat[obj["name"]] = obj["value"]
        colStat = modifiedColStat
        levels = list(colStat["LevelCount"].keys())
        if len(levels)>0:
            for val in levels:
                if val:
                    if any([ord(char)>127 for char in str(val)]):
                        utf8 = True
                        break
        return utf8

    @accepts(object,pd.DataFrame,(tuple,list),bool)
    def format_sampledata_timestamp_columns(self,pandasDf,timestampCols,stripTimestampFlag):
        if len(timestampCols) > 0:
            for colname in timestampCols:
                pandasDf[colname] = pandasDf[colname].apply(str)
                if stripTimestampFlag == True:
                    pandasDf[colname] = pandasDf[colname].apply(lambda x:x[:10])
                else:
                    unique_timestamps = pandasDf[colname].unique()
                    if len(unique_timestamps) == 1 and unique_timestamps[0] == "00:00:00":
                        pandasDf[colname] = pandasDf[colname].apply(lambda x:x[:10])
        return pandasDf.values.tolist()

    def set_sample_data(self):
        try :
            if self.rows > 100:
                sample_data = self.df.sample(False, float(100)/self.rows, seed=420)
                return sample_data
            else:
                return self.df
        except :
            if self.rows > 100:
                sample_data = self.df.sample(replace=False, frac=float(100)/self.rows,random_state=420)
                return sample_data
            else:
                return self.df

    def get_sample_data(self):
        return self._sample_data

    def get_percentage_columns(self, dimension_columns):
        sdf = self._sample_data
        orig_count = sdf.count()
        percentage_columns = []
        for col in dimension_columns:
            df = sdf.withColumn('new_column', sdf[col].substr(-1, 1))
            df = df.select('new_column').distinct()
            if df.count()==1 and df.first()['new_column']=='%':
                # print "percentage"
                result = sdf.withColumn('percent', regexp_extract(sdf[col], '^(((\s)*?[+-]?([0-9]+(\.[0-9][0-9]?)?)(\s)*)[^%]*)',1))
                result = result.select(result.percent.cast('float'))
                not_nulls = result.select('percent').na.drop().count()
                if orig_count == not_nulls:
                    percentage_columns.append(col)
        return percentage_columns

    def get_dollar_columns(self, dimension_columns):
        sdf = self._sample_data
        orig_count = sdf.count()
        dollar_columns = []
        for col in dimension_columns:
            df = sdf.withColumn('new_column', sdf[col].substr(1, 1))
            df = df.select('new_column').distinct()
            if df.count()==1 and df.first()['new_column']=='$':
                # print "dollar_columns"
                result = sdf.withColumn('dollar', regexp_extract(sdf[col], '^([$]((\s)*?[+-]?([0-9]+(\.[0-9][0-9]?)?)(\s)*)*)',2))
                result = result.select(result.dollar.cast('float'))
                not_nulls = result.select('dollar').na.drop().count()
                if orig_count == not_nulls:
                    dollar_columns.append(col)
        return dollar_columns

    def calculate_time_dimension_column_stats_from_string(self,df,td_columns,**kwargs):
        metaHelperInstance = MetaDataHelper(df, df.count())
        level_count_flag = True
        xtraArgs = {}
        for key in kwargs:
            xtraArgs[key] =  kwargs[key]
        if "level_count_flag" in xtraArgs:
            level_count_flag = xtraArgs[key]
        df = df.select(td_columns)
        total_count = df.count()
        output = {}
        chart_data = {}
        displayNameDict = {"count":"Count",
                            "mean":"Mean",
                            "stddev":"Standard Deviation",
                            "min":"Min",
                            "max":"Max",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls",
                            "MaxLevel":"Max Level",
                            "MinLevel":"Min Level",
                            "LevelCount":"LevelCount",
                            "firstDate":"Start Date",
                            "lastDate":"Last Date",
                            "percentOfNulls": "Percent Nulls"
                            }
        # TODO: FIX copy paste error numberOfUniqueValues
        displayOrderDict = {"firstDate": 0, "lastDate": 1, "MinLevel": 13, "MaxLevel": 14, "numberOfUniqueValues": 2,
                            "numberOfNulls": 3, "numberOfUniqueValues": 5, "numberOfNotNulls": 6, "count": 7, "min": 8,
                            "max": 9, "stddev": 10, "mean": 11, "LevelCount": 12, "percentOfNulls": 4}
        unprocessed_columns = []
        for column in td_columns:
            df1 = df.select(column)
            col_stat = {}
            nullcnt = df1.select(count(when(col(column).isNull(), column)).alias(column))
            col_stat["numberOfNulls"] = nullcnt.rdd.flatMap(list).first()
            col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
            col_stat["percentOfNulls"] = str(round((old_div(col_stat["numberOfNulls"]*100.0, total_count)), 3)) + "%"
            col_stat["numberOfUniqueValues"] = df1.select(column).distinct().count()
            # try:

            uniqueVals = df1.select(column).distinct().na.drop().limit(1000).collect()
            date_format=metaHelperInstance.get_datetime_format(uniqueVals)

            notNullDf = df1.select(column).distinct().na.drop()
            func =  udf (lambda x: datetime.strptime(x, date_format), DateType())
            notNullDf = notNullDf.withColumn("timestampCol", func(col(column)))
            notNullDf = notNullDf.orderBy("timestampCol",ascending=[True])
            notNullDf = notNullDf.withColumn("_id_", monotonically_increasing_id())
            id_max=notNullDf.select("_id_").rdd.max()[0]
            first_date = notNullDf.select("timestampCol").first()[0]
            first_date = str(pd.to_datetime(first_date).date())
            try:
                print("TRY BLOCK STARTED for column ", column)
                last_date = str(notNullDf.where(col("_id_") == id_max).select("timestampCol").first()[0])
            except:
                print("ENTERING EXCEPT BLOCK for column ", column)
                pandas_df = notNullDf.select(["_id_",column]).toPandas()
                pandas_df.sort_values(by=column,ascending=True,inplace=True)
                last_date = str(pandas_df[column].iloc[-1].date())
            col_stat["firstDate"] = first_date
            col_stat["lastDate"] = last_date
            col_stat["count"] = notNullDf.count()
            if level_count_flag:
                fs1 = time.time()
                levelCount = {}
                # if col_stat["numberOfUniqueValues"] <= GLOBALSETTINGS.UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION_DIMENSION:
                #     tdLevelCount = df1.groupBy(column).count().toPandas().set_index(column).to_dict().values()[0]
                #     levelCount = {}
                #     for k,v in tdLevelCount.items():
                #         if k != None:
                #             levelCount[str(pd.to_datetime(k).date())] = v
                #         else:
                #             levelCount[k] = v
                #     col_stat["LevelCount"] = levelCount
                #     if None in levelCount.keys():
                #         col_stat["numberOfNulls"] = levelCount[None]
                #         col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
                #     else:
                #         col_stat["numberOfNulls"] = 0
                #         col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
                #
                #     col_stat["percentOfNulls"] = str(round((col_stat["numberOfNulls"]*100.0 / total_count ), 3)) + "%"
                #     levelCountWithoutNull = levelCount
                #     if None in levelCount:
                #         levelCountWithoutNull.pop(None)
                #     if levelCountWithoutNull != {}:
                #         col_stat["MaxLevel"] = max(levelCountWithoutNull,key=levelCount.get)
                #         col_stat["MinLevel"] = min(levelCountWithoutNull,key=levelCount.get)
                #     else:
                #         col_stat["MaxLevel"] = None
                #         col_stat["MinLevel"] = None
                # else:
                levelCount = list(df1.groupBy(column).count().sort(desc("count")).limit(20).toPandas().set_index(column).to_dict().values())[0]
                levelCount = {str(k):v for k,v in list(levelCount.items())}
                col_stat["LevelCount"] = levelCount
                levelCountBig = df1.groupBy(column).count().sort(("count"))
                col_stat["MinLevel"]=first_date
                col_stat["MaxLevel"]=last_date

                dimension_chart_data = [{"name":k,"value":v} if k != None else {"name":"null","value":v} for k,v in list(levelCount.items())]
                dimension_chart_data = sorted(dimension_chart_data,key=lambda x:x["value"],reverse=True)
                dimension_chart_obj = ChartJson(NormalChartData(dimension_chart_data).get_data(),chart_type="bar")
                dimension_chart_obj.set_axes({"x":"name","y":"value"})
                dimension_chart_obj.set_subchart(False)
                dimension_chart_obj.set_hide_xtick(True)
                dimension_chart_obj.set_show_legend(False)
                chart_data[column] = C3ChartData(data=dimension_chart_obj)

            else:
                col_stat["firstDate"] = first_date
                col_stat["lastDate"] = last_date
                # col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
                # col_stat["numberOfNotNulls"] = int(col_stat["count"])
                # col_stat["numberOfUniqueValues"] = None
                chart_data[column] = {}

            # except:
            #     print "could not process column: ",column
            #     unprocessed_columns.append(column)
            #     chart_data[column] = {}

            output[column] = []
            for k,v in list(col_stat.items()):
                if k not in ["LevelCount","min","max","mean","stddev","numberOfNotNulls","MaxLevel","MinLevel"]:
                    output[column].append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
                else:
                    output[column].append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
            output[column] = sorted(output[column],key=lambda x:displayOrderDict[x["name"]])
            #output[column] = output[column]
        return output,chart_data,unprocessed_columns
