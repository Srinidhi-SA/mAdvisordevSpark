from __future__ import print_function
from builtins import str
from builtins import zip
from builtins import range
from past.builtins import basestring
from builtins import object
import math
from itertools import chain
from scipy.stats import chi2_contingency
from pyspark.ml.feature import Bucketizer
from pyspark.mllib.linalg import Matrices
from pyspark.mllib.stat import Statistics
from pyspark.sql.types import DoubleType, IntegerType
import pyspark.sql.functions as F

from bi.common import BIException
from bi.common import utils as CommonUtils
from bi.common.decorators import accepts
from bi.common.results import ChiSquareResult
from bi.common.results import DFChiSquareResult
from bi.common.results.chisquare import ContingencyTable
import numpy as np
import pandas as pd

"""
Chi Square Test
"""

class ChiSquare(object):
    GRAND_MEAN_COLUMN_NAME = '__grand_mean'
    MEAN_COLUMN_NAME = '__mean'
    COUNT_COLUMN_NAME = '__count'
    SUM_OF_SQUARES = '__sum_of_squares'

    def __init__(self, data_frame, df_helper, df_context,meta_parser,scriptWeight=None, analysisName=None):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._pandas_flag = df_context._pandas_flag
        self._metaParser = meta_parser
        self._measure_columns = self._dataframe_helper.get_numeric_columns()
        self._dimension_columns = self._dataframe_helper.get_string_columns()
        self._timestamp_columns = self._dataframe_helper.get_timestamp_columns()
        self._date_columns = self._dataframe_context.get_date_columns()
        self._uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(self._uid_col):
            self._dimension_columns = list(set(self._dimension_columns) - {self._uid_col})
        if len(self._date_columns) >0 :
            self._dimension_columns = list(set(self._dimension_columns)-set(self._date_columns))

        self._completionStatus = self._dataframe_context.get_completion_status()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        self._messageURL = self._dataframe_context.get_message_url()
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Chisquare Scripts",
                "weight":1
                },
            "chisquareStats":{
                "summary":"Running Chisquare For Relevant Dimension Columns",
                "weight":2
                },
            "completion":{
                "summary":"Chisquare Stats Calculated",
                "weight":2
                },
            }

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"initialization","info",display=False,weightKey="script")

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple), max_num_levels=int)
    def test_all(self, measure_columns=None, dimension_columns=None, max_num_levels=40):
        # CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"chisquareStats","info",display=False,weightKey="script")
        targetDimension = dimension_columns[0]
        all_dimensions = self._dimension_columns
        all_dimensions = [x for x in all_dimensions if x != targetDimension]
        # if self._analysisDict != {}:
        #     nColsToUse = self._analysisDict[self._analysisName]["noOfColumnsToUse"]
        # else:
        #     nColsToUse = None
        # if nColsToUse != None:
        #     all_dimensions = all_dimensions[:nColsToUse]
        all_measures = self._measure_columns
        df_chisquare_result = DFChiSquareResult()
        # print "df_chisquare_result"*50
        # print df_chisquare_result
        for d in all_dimensions:
            try:
                chisquare_result = self.test_dimension(targetDimension, d)
                df_chisquare_result.add_chisquare_result(targetDimension, d, chisquare_result)
            except Exception as e:
                print(repr(e), d)
                continue
        for m in all_measures:
            try:
                if self._pandas_flag :
                    if len(self._data_frame[m].unique())>self._analysisDict['Dimension vs. Dimension']['binSetting']['binCardinality']:
                        chisquare_result = self.test_measures(targetDimension, m)
                        df_chisquare_result.add_chisquare_result(targetDimension, m, chisquare_result)
                else:
                    if self._data_frame.select(F.countDistinct(m)).collect()[0][0]>self._analysisDict['Dimension vs. Dimension']['binSetting']['binCardinality']:
                        chisquare_result = self.test_measures(targetDimension, m)
                        df_chisquare_result.add_chisquare_result(targetDimension, m, chisquare_result)
            except Exception as e:
                print(str(e), m)
                continue

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"completion","info",display=False,weightKey="script")
        return df_chisquare_result

    @accepts(object, basestring, basestring)
    def test_dimension(self, targetDimension, testDimension):
        if not targetDimension in self._dataframe_helper.get_string_columns():
            raise BIException.non_string_column(testDimension)
        chisquare_result = ChiSquareResult()
        if self._pandas_flag:
            pivot_table = pd.crosstab([self._data_frame[targetDimension]], self._data_frame[testDimension])
            try:
                data_matrix = np.array(pivot_table.as_matrix(columns=None)).astype(np.int)
            except:
                data_matrix = np.array(pivot_table.values).astype(np.int)
        else:
            pivot_table = self._data_frame.stat.crosstab("{}".format(targetDimension), testDimension)
            # rdd = pivot_table.rdd.flatMap(lambda x: x).filter(lambda x: str(x).isdigit()).collect()
            rdd = list(chain(*list(zip(*pivot_table.drop(pivot_table.columns[0]).collect()))))
            data_matrix = Matrices.dense(pivot_table.count(), len(pivot_table.columns) - 1, rdd)
            data_matrix = data_matrix.toArray().tolist()
        result = chi2_contingency(data_matrix)
        chisquare_result.set_params(result)
        freq_table = self._get_contingency_table_of_freq(pivot_table, need_sorting = True)
        freq_table.set_tables()
        chisquare_result.set_table_result(freq_table)
        # Cramers V Calculation
        stat_value = result[0]
        n = freq_table.get_total()
        t = min(len(freq_table.column_one_values), len(freq_table.column_two_values))
        v_value = math.sqrt(float(stat_value) / (n * float(t)))
        chisquare_result.set_v_value(v_value)
        self._dataframe_helper.add_chisquare_significant_dimension(testDimension,v_value)
        return chisquare_result

    @accepts(object, basestring, basestring)
    def test_measures(self, targetDimension, testMeasure):
        chisquare_result = ChiSquareResult()
        if self._pandas_flag:
            if self._data_frame[testMeasure].dtypes == 'int64':
                measureSummaryDict = dict(self._data_frame[testMeasure].describe())
                if float(measureSummaryDict["count"]) > 10:
                    maxval = int(measureSummaryDict["max"])
                    minval = int(measureSummaryDict["min"])
                    step = (maxval - minval) / 5.0
                    splits = [round(math.floor(minval)), round(minval + step), round(minval + (step * 2)),
                              round(minval + (step * 3)), round(minval + (step * 4)), round(math.ceil(maxval))]
                    splits = list(set(splits))
                    splits.sort()
                    self._data_frame['bucketedColumn'] = pd.cut(self._data_frame[testMeasure], bins=splits,labels=list(range(len(splits)-1)), retbins=True, right=False)[0]
                    self._data_frame = self._data_frame.dropna()
                    pivot_table = pd.crosstab([self._data_frame[targetDimension]], self._data_frame['bucketedColumn'])
                else:
                    pivot_table = pd.crosstab([self._data_frame[targetDimension]], self._data_frame[testMeasure])

            else:
                df = self._data_frame
                if [df[testMeasure].dtypes == 'float64']:
                    measureSummaryDict = dict(df[testMeasure].describe())
                    if float(measureSummaryDict["count"]) > 10:
                        maxval = float(measureSummaryDict["max"])
                        minval = float(measureSummaryDict["min"])
                        step = (maxval - minval) / 5.0
                        splits = [math.floor(minval), minval + step, minval + (step * 2), minval + (step * 3),
                                  minval + (step * 4), math.ceil(maxval)]
                        df['bucketedColumn'] = pd.cut(df[testMeasure], bins=splits, labels=list(range(len(splits)-1)), retbins=True, right=False)[0]
                        df = df.dropna()
                        pivot_table = pd.crosstab([df[targetDimension]], df['bucketedColumn'])
                    else:
                        pivot_table = pd.crosstab([df[targetDimension]], df[testMeasure])
        else:
            dtype = self._data_frame.schema[testMeasure].dataType
            if dtype is IntegerType():
                # df = self._data_frame.withColumn(testMeasure, self._data_frame[testMeasure].cast(DoubleType()))
                measureSummaryDict = dict(self._data_frame.describe([testMeasure]).toPandas().values)
                if float(measureSummaryDict["count"]) > 10:
                    maxval = int(measureSummaryDict["max"])
                    minval = int(measureSummaryDict["min"])
                    step = (maxval - minval) / 5.0
                    splits = [round(math.floor(minval)), round(minval + step), round(minval + (step * 2)), round(minval + (step * 3)), round(minval + (step * 4)), round(math.ceil(maxval))]
                    splits = list(set(splits))
                    splits.sort()
                    bucketizer = Bucketizer(splits=splits, inputCol=testMeasure, outputCol="bucketedColumn")
                    # bucketedData = bucketizer.transform(df)
                    bucketedData = bucketizer.transform(self._data_frame.na.drop(subset=testMeasure))
                    pivot_table = bucketedData.stat.crosstab("{}".format(targetDimension), 'bucketedColumn')
                    keshav = pivot_table.toPandas()
                else:
                    pivot_table = self._data_frame.stat.crosstab("{}".format(targetDimension), testMeasure)
            else:
                df = self._data_frame.withColumn(testMeasure, self._data_frame[testMeasure].cast(DoubleType()))
                measureSummaryDict = dict(df.describe([testMeasure]).toPandas().values)
                if float(measureSummaryDict["count"]) > 10:
                    maxval = float(measureSummaryDict["max"])
                    minval = float(measureSummaryDict["min"])
                    step = (maxval - minval) / 5.0
                    splits = [math.floor(minval), minval + step, minval + (step * 2), minval + (step * 3),
                              minval + (step * 4), math.ceil(maxval)]
                    bucketizer = Bucketizer(splits=splits, inputCol=testMeasure, outputCol="bucketedColumn")
                    # bucketedData = bucketizer.transform(df)
                    bucketedData = bucketizer.transform(df.na.drop(subset=testMeasure))
                    pivot_table = bucketedData.stat.crosstab("{}".format(targetDimension), 'bucketedColumn')
                else:
                    pivot_table = df.stat.crosstab("{}".format(targetDimension), testMeasure)
        if self._pandas_flag:
            try:
                data_matrix = np.array(pivot_table.as_matrix(columns=None)).astype(np.int)
            except:
                data_matrix = np.array(pivot_table.values).astype(np.int)
        else:
            rdd = list(chain(*list(zip(*pivot_table.drop(pivot_table.columns[0]).collect()))))
            data_matrix = Matrices.dense(pivot_table.count(), len(pivot_table.columns)-1, rdd)
            data_matrix = data_matrix.toArray().tolist()
        result = chi2_contingency(data_matrix)
        chisquare_result.set_params(result)
        freq_table = self._get_contingency_table_of_freq(pivot_table)
        freq_table.update_col2_names(splits)
        freq_table.set_tables()
        chisquare_result.set_table_result(freq_table)
        # Cramers V Calculation
        stat_value = result[0]
        n = freq_table.get_total()
        t = min(len(freq_table.column_one_values), len(freq_table.column_two_values))

        v_value = math.sqrt(float(stat_value) / (n * float(t)))
        chisquare_result.set_v_value(v_value)
        chisquare_result.set_split_values([float(x) for x in splits])
        # chisquare_result.set_buckeddata(bucketedData)
        return chisquare_result


    def _get_contingency_table_of_freq(self, pivot_table, need_sorting=False):
        """

        :param pivot_table:
                column_names[1:] correspond to unique values of column two
                values in first column correspond to unique values of column one
        :return:
        """
        if self._pandas_flag:
            column_one_values = list(pivot_table.index)
            column_two_values = list(pivot_table.columns)

        else:
            column_one_values = []
            column_two_values = pivot_table.columns[1:]
            rows = pivot_table.collect()
            # first column value in every row is a unique column one value used to build contingency table
            for row in rows:
                column_one_values.append(row[0])
        contigency_table = ContingencyTable(column_one_values, column_two_values)
        if need_sorting:
            contigency_table.update_col2_order()
        if self._pandas_flag:
            for j in range(len(pivot_table.index)):
                try:
                    contigency_table.add_row(pivot_table.index[j], list((pivot_table.ix[j][0:]).astype('float')))
                except:
                    contigency_table.add_row(pivot_table.index[j], list((pivot_table.iloc[j][0:]).astype('float')))
        else:
            for row in rows:
                column_one_val = row[0]
                contigency_table.add_row(column_one_val, [float(value) for value in row[1:]])
        return contigency_table

    def _get_contigency_table_of_percentages(self, pivot_table):
        contigency_table = self._get_contingency_table_of_freq(pivot_table)
        total = contigency_table.get_total()
        for row_index in range(0, len(contigency_table.table)):
            for column_index in range(0, len(contigency_table.table[row_index])):
                cell_value = contigency_table.table[row_index][column_index]
                cell_value_percentage = 100.0 * cell_value / total
                contigency_table.table[row_index][column_index] = cell_value_percentage

        return contigency_table

    def _get_contigency_table_of_percentages_rounded(self, pivot_table):
        contigency_table = self._get_contingency_table_of_freq(pivot_table)
        total = contigency_table.get_total()
        for row_index in range(0, len(contigency_table.table)):
            for column_index in range(0, len(contigency_table.table[row_index])):
                cell_value = contigency_table.table[row_index][column_index]
                cell_value_percentage = 100.0 * cell_value / total
                contigency_table.table[row_index][column_index] = round(cell_value_percentage,2)

        return contigency_table

    def _get_contigency_table_of_percentages_rounded_by_target(self, pivot_table):
        contigency_table = self._get_contingency_table_of_freq(pivot_table)
        total = []
        for row_index in range(0, len(contigency_table.table)):
            total.append(sum(contigency_table.table[row_index]))
        for row_index in range(0, len(contigency_table.table)):
            for column_index in range(0, len(contigency_table.table[row_index])):
                cell_value = contigency_table.table[row_index][column_index]
                cell_value_percentage = 100.0 * cell_value / total[row_index]
                contigency_table.table[row_index][column_index] = round(cell_value_percentage,2)
        return contigency_table
