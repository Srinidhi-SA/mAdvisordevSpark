from __future__ import print_function
from __future__ import division
from builtins import object
from past.utils import old_div
import time

from pyspark.ml.feature import QuantileDiscretizer
from pyspark.sql import functions as FN

from bi.common import BIException
from bi.common.results import FivePointSummary


class Quantizer(object):
    QUANTIZATION_OUTPUT_COLUMN = '__quant'
    QUANTIZATION_RELATIVE_ERROR = 0.0001
    APPROX_ERROR = 0.10
    QUARTILE_PERCENTAGES = [0.25,0.5,0.75]

    @staticmethod
    def quantize(data_frame, measure_column, dataframe_helper):
        if not dataframe_helper.is_numeric_column(measure_column):
            raise BIException.non_numeric_column(measure_column)

        quantile_discretizer = QuantileDiscretizer(numBuckets=4, inputCol=measure_column,
                                                   outputCol=Quantizer.QUANTIZATION_OUTPUT_COLUMN,
                                                   relativeError=Quantizer.QUANTIZATION_RELATIVE_ERROR)
        bucketizer = quantile_discretizer.fit(data_frame)
        # splits have these values [-Inf, Q1, Median, Q3, Inf]
        splits = bucketizer.getSplits()
        if len(splits) < 5:
            q1 = splits[1]
            median = splits[1]
            q3 = splits[1]
            iqr = (q3 - q1)
            left_hinge = (q1 - 1.5 * iqr)
            right_hinge = (q3 + 1.5 * iqr)
        else:
            q1 = splits[1]
            median = splits[2]
            q3 = splits[3]
            iqr = (q3 - q1)
            left_hinge = (q1 - 1.5 * iqr)
            right_hinge = (q3 + 1.5 * iqr)

        mean = data_frame.select(FN.mean(measure_column)).collect()[0][0]
        column = FN.column(measure_column)
        num_left_outliers = data_frame.filter(column < left_hinge).count()
        num_right_outliers = data_frame.filter(column > right_hinge).count()
        # q1_freq = data_frame.filter(column < q1).count()
        # q2_freq = data_frame.filter(column >= q1).filter(column < median).count()
        # q3_freq = data_frame.filter(column >= median).filter(column < q3).count()
        # q4_freq = data_frame.filter(column >= q3).count()
        q1_stats = data_frame.filter(column < q1).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q2_stats = data_frame.filter(column >= q1).filter(column < median).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q3_stats = data_frame.filter(column >= median).filter(column < q3).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q4_stats = data_frame.filter(column >= q3).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()

        q1_freq = q1_stats[0]['count']
        q2_freq = q2_stats[0]['count']
        q3_freq = q3_stats[0]['count']
        q4_freq = q4_stats[0]['count']

        quartile_sums = {}
        quartile_sums['q1'] = q1_stats[0]['sum']
        quartile_sums['q2'] = q2_stats[0]['sum']
        quartile_sums['q3'] = q3_stats[0]['sum']
        quartile_sums['q4'] = q4_stats[0]['sum']

        quartile_means = {}
        quartile_means['q1'] = old_div(q1_stats[0]['sum'],q1_stats[0]['count'])
        quartile_means['q2'] = old_div(q2_stats[0]['sum'],q2_stats[0]['count'])
        quartile_means['q3'] = old_div(q3_stats[0]['sum'],q3_stats[0]['count'])
        quartile_means['q4'] = old_div(q4_stats[0]['sum'],q4_stats[0]['count'])

        FPS = FivePointSummary(left_hinge_value=left_hinge, q1_value=q1, median=median, q3_value=q3,
                                right_hinge_value=right_hinge, num_left_outliers=num_left_outliers,
                                num_right_outliers=num_right_outliers, q1_freq=q1_freq, q2_freq=q2_freq,
                                q3_freq=q3_freq, q4_freq=q4_freq)
        FPS.set_means(quartile_means)
        FPS.set_sums(quartile_sums)

        return FPS
    @staticmethod
    def approxQuantize(data_frame, measure_column, dataframe_helper):
        if not dataframe_helper.is_numeric_column(measure_column):
            raise BIException.non_numeric_column(measure_column)
        st = time.time()
        data_frame = data_frame.select(measure_column)
        splits = data_frame.approxQuantile(measure_column,Quantizer.QUARTILE_PERCENTAGES, Quantizer.APPROX_ERROR)
        print(splits)
        print("bucketizer",time.time()-st)
        q1 = splits[0]
        median = splits[1]
        q3 = splits[2]
        iqr = (q3 - q1)
        left_hinge = (q1 - 1.5 * iqr)
        right_hinge = (q3 + 1.5 * iqr)
        # print q1,median,q3,iqr,left_hinge,right_hinge

        mean = data_frame.select(FN.mean(measure_column)).collect()[0][0]
        column = FN.column(measure_column)
        num_left_outliers = data_frame.filter(column < left_hinge).count()
        num_right_outliers = data_frame.filter(column > right_hinge).count()

        q1_stats = data_frame.filter(column < q1).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q2_stats = data_frame.filter(column >= q1).filter(column < median).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q3_stats = data_frame.filter(column >= median).filter(column < q3).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()
        q4_stats = data_frame.filter(column >= q3).agg(FN.sum(column).alias('sum'), FN.count(column).alias('count')).collect()

        q1_freq = q1_stats[0]['count']
        q2_freq = q2_stats[0]['count']
        q3_freq = q3_stats[0]['count']
        q4_freq = q4_stats[0]['count']

        quartile_sums = {}
        quartile_sums['q1'] = q1_stats[0]['sum'] if q1_stats[0]['sum'] != None else 0
        quartile_sums['q2'] = q2_stats[0]['sum'] if q2_stats[0]['sum'] != None else 0 ##### Geeta:changed q1_stats[0]['sum'] to q2_stats[0]['sum']
        quartile_sums['q3'] = q3_stats[0]['sum'] if q3_stats[0]['sum'] != None else 0
        quartile_sums['q4'] = q4_stats[0]['sum'] if q4_stats[0]['sum'] != None else 0

        quartile_means = {}
        quartile_means['q1'] = old_div(quartile_sums['q1'],q1_stats[0]['count']) if q1_stats[0]['count'] != 0 else None
        quartile_means['q2'] = old_div(quartile_sums['q2'],q2_stats[0]['count']) if q2_stats[0]['count'] != 0 else None
        quartile_means['q3'] = old_div(quartile_sums['q3'],q3_stats[0]['count']) if q3_stats[0]['count'] != 0 else None ##### Geeta:changed q2_stats[0]['count'] to q3_stats[0]['count']
        quartile_means['q4'] = old_div(quartile_sums['q4'],q4_stats[0]['count']) if q4_stats[0]['count'] != 0 else None ##### Geeta:changed q2_stats[0]['count'] to q4_stats[0]['count']

        FPS = FivePointSummary(left_hinge_value=left_hinge, q1_value=q1, median=median, q3_value=q3,
                                right_hinge_value=right_hinge, num_left_outliers=num_left_outliers,
                                num_right_outliers=num_right_outliers, q1_freq=q1_freq, q2_freq=q2_freq,
                                q3_freq=q3_freq, q4_freq=q4_freq)
        FPS.set_means(quartile_means)
        FPS.set_sums(quartile_sums)

        return FPS

    @staticmethod
    def approxQuantize_pandas(data_frame, measure_column, dataframe_helper):
        if not dataframe_helper.is_numeric_column(measure_column):
           raise BIException.non_numeric_column(measure_column)
        data_frame = data_frame[measure_column]
        q1 = data_frame.describe()[4]
        median = data_frame.describe()[5]
        q3 = data_frame.describe()[6]
        iqr = (q3 - q1)
        left_hinge = (q1 - 1.5 * iqr)
        right_hinge = (q3 + 1.5 * iqr)
        num_left_outliers = data_frame[data_frame < left_hinge].count().item()
        num_right_outliers = data_frame[data_frame > right_hinge].count().item()
        q1_freq = data_frame[data_frame < q1].count().item()
        q2_freq = data_frame[(data_frame >= q1) & (data_frame < median)].count().item()
        q3_freq = data_frame[(data_frame >= median) & (data_frame < q3)].count().item()
        q4_freq = data_frame[data_frame >= q3].count().item()

        quartile_sums = {}
        quartile_sums['q1'] = data_frame[data_frame < q1].sum().item()
        quartile_sums['q2'] = data_frame[(data_frame >= q1) & (data_frame < median)].sum().item()
        quartile_sums['q3'] = data_frame[(data_frame >= median) & (data_frame < q3)].sum().item()
        quartile_sums['q4'] = data_frame[data_frame >= q3].sum().item()

        quartile_means = {}
        quartile_means['q1'] = data_frame[data_frame < q1].mean()
        quartile_means['q2'] = data_frame[(data_frame >= q1) & (data_frame < median)].mean()
        quartile_means['q3'] = data_frame[(data_frame >= median) & (data_frame < q3)].mean()
        quartile_means['q4'] = data_frame[data_frame >= q3].mean()

        FPS = FivePointSummary(left_hinge_value=left_hinge, q1_value=q1, median=median, q3_value=q3,
                                right_hinge_value=right_hinge, num_left_outliers=num_left_outliers,
                                num_right_outliers=num_right_outliers, q1_freq=q1_freq, q2_freq=q2_freq,
                                q3_freq=q3_freq, q4_freq=q4_freq)
        FPS.set_means(quartile_means)
        FPS.set_sums(quartile_sums)

        return FPS
