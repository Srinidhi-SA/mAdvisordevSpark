from __future__ import absolute_import
from builtins import object
from bi.common.results.frequency_dimensions import FreqDimensionResult
from bi.common.utils import accepts
from .dimension_column import DimensionColumnNarrative


class DimensionNarrative(object):

    @accepts(object, (int, int), FreqDimensionResult)
    def __init__(self, num_measure_columns, df_freq_dimension_obj):
        self._df_regression_result = df_freq_dimension_obj
        self._num_measure_columns = num_measure_columns
        self._dataframe_context = context

        self.title = None
        self.summary = None
        self._base_dir = "/dimensions/"
