from __future__ import print_function
from builtins import filter
from builtins import zip
from builtins import map
from builtins import str
from builtins import object
import time
import uuid
import gc
from bi.common import ColumnType
from bi.common import MetaDataHelper
from bi.common import utils as CommonUtils
from bi.common.results import DfMetaData, MetaData, ColumnData, ColumnHeader
from bi.settings import setting as GLOBALSETTINGS
import pandas as pd
from pyspark.sql.functions import coalesce, to_date
from pyspark.sql.functions import date_format, lit


class MetaDataScriptPandas(object):
    '''
    Gives metaData information about the data
    '''
    def __init__(self, data_frame, dataframe_context):
        self._dataframe_context = dataframe_context
        self._completionStatus = self._dataframe_context.get_completion_status()
        self._start_time = time.time()
        self._analysisName = "metadata"
        self._messageURL = self._dataframe_context.get_message_url()
        self._ignoreMsgFlag = self._dataframe_context.get_metadata_ignore_msg_flag()
        if dataframe_context.get_job_type()== "training" or dataframe_context.get_job_type()== "prediction" :
            self._scriptStages = {
                "schema":{
                    "summary":"Preparing The Data For Model Creation",
                    "weight":2
                    },
                "sampling":{
                    "summary":"Sampling The Dataframe",
                    "weight":2
                    },
                "measurestats":{
                    "summary":"Calculated Stats For Measure Columns",
                    "weight":2
                    },
                "dimensionstats":{
                    "summary":"Calculating Stats For Dimension Columns",
                    "weight":2
                    },
                "timedimensionstats":{
                    "summary":"Calculating Stats For Time Dimension Columns",
                    "weight":2
                    },
                "suggestions":{
                    "summary":"Ignore And Date Suggestions",
                    "weight":2
                    },
                }
        if dataframe_context.get_job_type()== "story":
            self._scriptStages = {
                "schema":{
                    "summary":"Loaded The Data and Schema Is Run",
                    "weight":1
                    },
                "sampling":{
                    "summary":"Sampling The Dataframe",
                    "weight":1
                    },
                "measurestats":{
                    "summary":"Calculated Stats For Measure Columns",
                    "weight":2
                    },
                "dimensionstats":{
                    "summary":"Calculated Stats For Dimension Columns",
                    "weight":2
                    },
                "timedimensionstats":{
                    "summary":"Calculated Stats For Time Dimension Columns",
                    "weight":2
                    },
                "suggestions":{
                    "summary":"Ignore And Date Suggestions",
                    "weight":1
                    },
                }
        else:
            self._scriptStages = {
                "schema":{
                    "summary":"Loaded The Data and Schema Is Run",
                    "weight":12
                    },
                "sampling":{
                    "summary":"Sampling The Dataframe",
                    "weight":5
                    },
                "measurestats":{
                    "summary":"Calculated Stats For Measure Columns",
                    "weight":5
                    },
                "dimensionstats":{
                    "summary":"Calculated Stats For Dimension Columns",
                    "weight":5
                    },
                "timedimensionstats":{
                    "summary":"Calculated Stats For Time Dimension Columns",
                    "weight":5
                    },
                "suggestions":{
                    "summary":"Ignore And Date Suggestions",
                    "weight":5
                    },
                }
        self._binned_stat_flag = True
        self._level_count_flag = True
        self._stripTimestamp = True
        self._data_frame = data_frame
        self._total_columns = self._data_frame.shape[0]
        self._total_rows = self._data_frame.shape[1]
        self._max_levels = min(200, round(self._total_rows**0.5))
        self._percentage_columns = []
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        self._numeric_columns = self._data_frame.select_dtypes(include=numerics).columns.tolist()
        self._string_columns = self._data_frame.select_dtypes(include=object).columns.tolist()
        for column in self._string_columns:
            try:
                print(column)
                self._data_frame[column] = pd.to_datetime(self._data_frame[column], infer_datetime_format=True)
            except:
                pass
        self._timestamp_columns = self._data_frame.select_dtypes(include='datetime64').columns.tolist()
        print(self._timestamp_columns)
        self._string_columns = list(set(self._string_columns)-set(self._timestamp_columns))
        self._boolean_columns = self._data_frame.select_dtypes(include=bool).columns.tolist()
        self._dataSize = {"nRows":self._total_rows,"nCols":self._total_columns,"nBooleans":None,"nMeasures":None,"nDimensions":None,"nTimeDimensions":None,"dimensionLevelCountDict":{},"totalLevels":None}
        self.actual_col_datatype_update=[]
        self.update_column_type_dict()
        time_taken_schema = time.time()-self._start_time
        print("schema rendering takes",time_taken_schema)


    def update_column_type_dict(self):
        self._column_type_dict = dict(\
                                        list(zip(self._numeric_columns,[{"actual":"measure","abstract":"measure"}]*len(self._numeric_columns)))+\
                                        list(zip(self._string_columns,[{"actual":"dimension","abstract":"dimension"}]*len(self._string_columns)))+\
                                        list(zip(self._timestamp_columns,[{"actual":"datetime","abstract":"datetime"}]*len(self._timestamp_columns)))+\
                                        list(zip(self._boolean_columns,[{"actual":"boolean","abstract":"dimension"}]*len(self._boolean_columns)))\
                                     )
        self._dataSize["nMeasures"] = len(self._numeric_columns)
        self._dataSize["nDimensions"] = len(self._string_columns)
        self._dataSize["nTimeDimensions"] = len(self._timestamp_columns)
        self._dataSize["nBooleans"] = len(self._boolean_columns)

        print(self._dataSize)

    def to_date_(self,col, formats=GLOBALSETTINGS.SUPPORTED_DATETIME_FORMATS["pyspark_formats"]):
        # Spark 2.2 or later syntax, for < 2.2 use unix_timestamp and cast
        pass

    def run(self):
        pass

    def checkDuplicateCols_pandas(self,col1,col2,flag=False):
        pass

    def checkDupColName(self,statsDict):
        flipped = {}
        if len(set(list(map(str,list(statsDict.values()))))) < len(list(statsDict.keys())):
            for key, value in list(statsDict.items()):
                if str(value) not in flipped:
                    flipped[str(value)] = [key]
                else:
                    flipped[str(value)].append(key)
            def check_length(value):
                if len(value)>1:
                    return True
                else:
                    return False
            dupCols=list(filter(check_length, list(flipped.values())))
            return dupCols
        else :
            return []
