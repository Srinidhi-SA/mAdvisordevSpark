from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import zip
from builtins import str
from builtins import range
from past.builtins import basestring
from past.utils import old_div
import json
from hashlib import md5
import time
import traceback
import uuid
import math
from re import sub
import re

import matplotlib
import numpy as np
import pandas as pd
import requests

import os

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import size, zeros, where
from scipy import linspace
# from matplotlib.pyplot import hist

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col
import pyspark.sql.functions as F

from .decorators import accepts
from math import log10, floor

from bi.settings import setting as GLOBALSETTINGS


# def possible_analysis():
#     stringCols =

def round_sig(x, sig=3):
    if isinstance(x,str):
        return x
    else:
        try:
            if abs(x)>=1:
                x = round(x,sig)
            else:
                x = round(x, sig-int(floor(log10(abs(x))))-1)
        except:
            pass
    return x

def generate_signature(json_obj,secretKey=None):
    """
    json_obj = json obj with {"key1":"DSDDD","key2":"DASDAA","signature":None}
    secretKey = "secret key"
    """
    existing_key = json_obj["key1"]+"|"+json_obj["key2"]+"|"+secretKey
    newhash = md5.new()
    newhash.update(existing_key)
    value = newhash.hexdigest()
    return value

def get_existing_metadata(dataframe_context):
    baseUrl = dataframe_context.get_metadata_url()
    slugs = dataframe_context.get_metadata_slugs()
    jsonToken = {"key1":uuid.uuid4().hex,"key2":uuid.uuid4().hex,"signature":None,"generated_at":time.time()}
    secretKey = GLOBALSETTINGS.HDFS_SECRET_KEY
    try:
        sigString = generate_signature(jsonToken,secretKey)
        jsonToken["signature"] = sigString
        url = "{}{}/?key1={}&key2={}&signature={}&generated_at={}".format(baseUrl,slugs[0],jsonToken["key1"],jsonToken["key2"],jsonToken["signature"],jsonToken["generated_at"])
        # print "url",url
        metaObj = requests.get(url)
        output = metaObj.json()
        if "Message" in output:
            return None
        else:
            return output
    except:
        return None

@accepts((int, int, float), (int, int, float), num_steps=int)
def frange(start, stop, num_steps=10):
    """
    Create num_step equal sized ranges form start to stop, useful in histogram generation
    :param start:
    :param stop:
    :param num_steps:
    :return:
    """
    step_size = start+1
    if start == stop:
        start=start - 0.8
        stop = stop + 0.8
    step_size = 1.0 * (stop-start) / num_steps
    rounding_digits = 0
    if step_size >= 1:
        step_size = int(math.ceil(step_size))
    else:
        rounding_digits = 1
        while num_steps >= (step_size * math.pow(10, rounding_digits)):
            rounding_digits += 1
        step_size = round(step_size, rounding_digits)

    rounded_start = math.floor(1.0 * start / step_size) * step_size
    rounded_stop = math.ceil(1.0 * (stop+old_div(step_size,num_steps)) / step_size) * step_size
    i = rounded_start
    result = []
    while i < rounded_stop:
        result.append(round(i, rounding_digits))
        i += step_size
    if result[-1] < rounded_stop:
        result.append(round(rounded_stop, rounding_digits))
    result = list(set(result))
    result.sort()
    return result


@accepts(app_name=basestring,hive_environment=bool)
def get_spark_session(app_name='Demo App',hive_environment=True):
    if hive_environment:
        return SparkSession.builder.appName(app_name).config(conf=SparkConf()).enableHiveSupport().getOrCreate()
    else:
        # os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /home/keshav/pysparkExternalJars/jpmml-sparkml-executable-1.5.0.jar,' \
        # ' ~/pysparkExternalJars/xgboost4j-0.72.jar, ~/pysparkExternalJars/xgboost4j-spark-0.72.jar pyspark-shell'
        return SparkSession.builder.appName(app_name) \
                        .getOrCreate()

                        # .config("spark.executor.extraClassPath", '/home/keshav/pysparkExternalJars/jpmml-sparkml-executable-1.5.0.jar') \
                        # .config("spark.driver.extraClassPath", '/home/keshav/pysparkExternalJars/xgboost4j-0.72.jar') \
                        # .config("spark.driver.extraClassPath", '/home/keshav/pysparkExternalJars/xgboost4j-spark-0.72.jar') \
                        # .config("spark.executor.extraClassPath", '/home/keshav/pysparkExternalJars/xgboost4j-0.72.jar') \
                        # .config("spark.executor.extraClassPath", '/home/keshav/pysparkExternalJars/xgboost4j-spark-0.72.jar') \
                        # .config("spark.driver.extraClassPath", '/home/keshav/pysparkExternalJars/jpmml-sparkml-executable-1.5.0.jar') \
                        # .config("spark.executor.extraClassPath", '/home/keshav/pysparkExternalJars/jpmml-sparkml-executable-1.5.0.jar') \


def clean(x):
    from re import sub
    # \g<1> is whatever matches the the first (...)
    #x = sub( r'(\d+)[kK]', r'\g<1>000', x )
    x = sub('[^0-9.a-zA-z/-]','',x)
    return x

def get_updated_colnames(df):
    num_rows = len(df.index)
    final_column_names = []
    changed_cols = []
    for col in df.columns:
        if not df[col].dtype==object:
            final_column_names.append(col)
            continue
        temp = []
        try:
            temp = [x for x in df.dropna(subset=[col])[col]]
            initial_length = len(temp)
            if (initial_length<old_div(num_rows,2)):
                raise ValueError('None Vals')
            temp1 = [float(clean(x)) for x in temp]
            final_length = len(temp1)
            if initial_length == final_length:
                changed_cols.append(col)
                try:
                    pre=int(temp[0][0])
                except:
                    col = col + '||pre:' + temp[0][0]
                try:
                    post=int(temp[0][-1])
                except:
                    col = col + '||post:' + temp[0][-1]

        except ValueError:
            # print "e1"
            pass
        else:
            pass
            # print "e2"
        final_column_names.append(col)
    return {'f':final_column_names, 'c':changed_cols}

def tryconvert(x):
    """
    for converting string cols to floats
    """
    if x==None:
        return None
    try:
        x =float(sub('[^0-9.a-zA-z:/-]','',x))
        return x
    except:
        pass
    return None

def as_dict(obj):
    """
    Converts an object hierarchy into a dictionary object
    Ref: http://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return {k: as_dict(v) for (k, v) in list(obj.items())}
    elif hasattr(obj, "_ast"):
        return as_dict(obj._ast())
    elif hasattr(obj, '__iter__')and not isinstance(obj, str):
        return [as_dict(v) for v in obj]
    elif hasattr(obj, '__dict__'):
        return dict([(key, as_dict(value))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
    else:
        return obj

def recursiveRemoveNoneNodes(tree):
    if isinstance(tree, dict) and "children" not in list(tree.keys()):
        return tree
    elif isinstance(tree, dict) and "children" in list(tree.keys()):
        # if len(tree["children"]) != 0:
        if tree["children"] != [None]:
            for idx,stree in enumerate(tree["children"]):
                if stree != None:
                    tree["children"][idx] = (recursiveRemoveNoneNodes(stree))
            return tree
        else:
            tree.pop("children")
            return tree

def write_to_file(filepath,obj):
    if filepath.startswith("file"):
        filepath = filepath[7:]
    f = open(filepath, 'w')
    f.write(obj)
    f.close()

def get_level_count_dict(df,categorical_columns,separator,output_type="string",dataType="pandas"):
    count_dict = {}
    out = []
    for col in categorical_columns:
        if dataType == "spark":
            count_dict[col] = len(df.select(col).distinct().collect())
            # count_dict[col] = df.agg((F.countDistinct(col).alias(col))).first().asDict()[col]
        else:
            count_dict[col] = len(df[col].unique())
        out.append(col)
        out.append(str(count_dict[col]))
    if output_type == "string":
        return separator.join(out)
    else:
        return count_dict

def send_message_API(monitor_api, task, message, complete, progress):
    url = monitor_api
    message_dict = {'task': task, 'message': message, 'complete': complete, 'progress': progress}
    #r = requests.post(url, data=json.dumps(message_dict))
    #print json.loads(r.content)['message'] + " for ", task +'\n'

def temp_convertor(x):
    try:
        return x.__dict__
    except Exception as e:
        return "{}".format(x)

# def convert_python_object_to_json(object):
#     try:
#         return json.dumps(object, default=temp_convertor)
#     except:
#         return json.dumps(stringify_keys(object.__dict__), default=temp_convertor)

def convert_python_object_to_json(object):
    try:
        return json.dumps(object, default=temp_convertor)
    except:
        try:
            return json.dumps(stringify_keys(object.__dict__), default=temp_convertor)
        except:
            return json.dumps(stringify_keys(object.__dict__), default=temp_convertor)

def stringify_keys(d):
    """Convert a dict's keys to strings if they are not."""
    for key in d.keys():

        # check inner dict
        if isinstance(d[key], dict):
            value = stringify_keys(d[key])
        else:
            value = d[key]

        # convert nonstring to string if needed
        if not isinstance(key, str):
            try:
                d[str(key)] = value
            except Exception:
                try:
                    d[repr(key)] = value
                except Exception:
                    raise

            # delete old key
            del d[key]
    return d
def byteify(input):
    if isinstance(input, dict):
        return dict([(byteify(key), byteify(value)) for key, value in input.items()])
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input


def create_progress_message_object(analysisName,stageName,messageType,shortExplanation,stageCompletionPercentage,globalCompletionPercentage,display=True):
    """
    messageType = ["info","failure"]
    """
    timestamp = time.time()
    progressMessage = {
        "analysisName" : analysisName,
        "stageName" : stageName,
        "messageType" : messageType,
        "shortExplanation" : shortExplanation,
        "stageCompletionTimestamp" : timestamp,
        "gmtDateTime":time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)),
        "globalCompletionPercentage" : min(globalCompletionPercentage,100),
        "stageCompletionPercentage" : stageCompletionPercentage,
        "display":display
    }
    # print "completionStatus for the Job:- ",globalCompletionPercentage,"timestamp:- ",progressMessage["stageCompletionTimestamp"]
    return progressMessage

def save_result_json(url,jsonData):
    url += "set_result"
    print("result url",url)
    res = requests.put(url=url,data=jsonData)
    return res

def save_progress_message(url,jsonData,ignore=False,emptyBin=False):
    print("="*100)
    print({
        "stageName": jsonData["stageName"],
        "globalCompletionPercentage": jsonData["globalCompletionPercentage"],
        "shortExplanation": jsonData["shortExplanation"],
        "analysisName": jsonData["analysisName"],
        "gmtDateTime":jsonData["gmtDateTime"]
        })
    print("="*100)

    if jsonData["globalCompletionPercentage"] > 100:
        print("Red Alert ( percentage more than 100)"*5)
    if emptyBin == True:
        url += "?emptyBin=True"
    # print "message url",url
    if ignore == False:
        res = requests.put(url=url,data=json.dumps(jsonData))
        return res
    else:
        return True

def create_update_and_save_progress_message(dataframeContext,scriptWeightDict,scriptStages,analysisName,stageName,messageType,display=True,emptyBin=False,customMsg=None,weightKey="script"):
    if dataframeContext.get_dont_send_message() == False:
        completionStatus = dataframeContext.get_completion_status()
        print("incoming completionStatus",completionStatus)
        completionStatus = min(completionStatus,100)
        messageURL = dataframeContext.get_message_url()
        if customMsg == None:
            if dataframeContext.get_job_type() == 'training' or dataframeContext.get_job_type() == 'prediction':
                completionStatus += scriptStages[stageName]["weight"]
            else:
                completionStatus += old_div(scriptWeightDict[analysisName][weightKey]*scriptStages[stageName]["weight"],10)
            progressMessage = create_progress_message_object(analysisName,\
                                        stageName,\
                                        messageType,\
                                        scriptStages[stageName]["summary"],\
                                        completionStatus,\
                                        completionStatus,\
                                        display=display)
        else:
            progressMessage = create_progress_message_object(analysisName,stageName,messageType,customMsg,completionStatus,completionStatus,display=display)
        runningEnv = dataframeContext.get_environement()
        if runningEnv == "debugMode":
            save_progress_message(messageURL,progressMessage,ignore=True,emptyBin=emptyBin)
        else:
            save_progress_message(messageURL,progressMessage,ignore=False,emptyBin=emptyBin)
        dataframeContext.update_completion_status(completionStatus)
        print("Outgoing Completion Status - ", completionStatus)


def save_pmml_models(url,jsonData,ignore=False):
    if ignore == False:
        res = requests.put(url=url,data=json.dumps(jsonData))
        return res
    else:
        return True


def keyWithMaxVal(dictObj):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(dictObj.values())
     k=list(dictObj.keys())
     return k[v.index(max(v))]

def print_errors_and_store_traceback(loggerDict,scriptName,error):
    print(error)
    exception = {"exception":error,"traceback":traceback.format_exc()}
    loggerDict[scriptName] = exception
    print("#####ERROR#####"*5)
    print(error)
    print("#####ERROR#####"*5)
    print("{} Script Failed".format(scriptName))
    print(loggerDict[scriptName])

def save_error_messages(url,errorKey,error,ignore=False):
    if errorKey != None:
        url = url+errorKey+"/"
    if url != None:
        if errorKey != "jobRuntime":
            tracebackData = str(traceback.format_exc())
            errordict = {"error":str(error).split("\n"),"traceback":tracebackData.split("\n")}
        else:
            errordict = error
        if ignore == False:
            res = requests.put(url=url,data=json.dumps(errordict))
            return res
        else:
            return True


def get_duration_string(datarange):
    yr = str(datarange//365)
    mon = str((datarange%365)//30)
    if mon == "12":
        yr = str(int(yr)+1)
        mon = None
    if mon != None:
        durationString = yr+" years and "+mon+" months"
    else:
        durationString = yr+" years"
    return durationString

def get_splits(minVal,maxVal,n_split):
    # splits  = frange(minVal,maxVal,num_steps=n_split)
    diff = (maxVal - minVal)*1.0
    splits = [minVal,minVal+diff*0.2,minVal+diff*0.4,minVal+diff*0.6,minVal+diff*0.8,maxVal]
    splits = sorted(splits)
    splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
    splits_data = {"splits":splits,"splits_range":splits_range}
    str_splits_range = [" to ".join([str(round_sig(x[0],sig=2)),str(round_sig(x[1],sig=2))]) for x in splits_range]
    splits_data["bin_mapping"] = dict(list(zip(list(range(len(splits_range))),str_splits_range)))
    return splits_data

def return_optimum_bins(x):
	sd = np.std(x)
	mean = np.mean(x)

	final_list = [i for i in x if (i > mean - 3 * sd)]
	final_list = [i for i in final_list if (i < mean + 3 * sd)]

	x= pd.Series(final_list)

	#--------------Optimizing bins ---------------#

	x_max = max(x)
	x_min = min(x)

	N_MIN = 2   					# Minimum number of bins (integer)
	N_MAX = 30						# Maximum number of bins (integer)
	N = list(range(N_MIN,N_MAX)) 			#of Bins
	N = np.array(N)
	D = old_div((x_max-x_min),N)    			#Bin size vector
	C = zeros(shape=(size(D),1))

	# Computation of the cost function

	for i in range(size(N)):
		edges = linspace(x_min,x_max,N[i]+1)  # Bin edges
		ki = plt.hist(x,edges) 				  # Count # of events in bins
		ki = list(ki[0])
		k = np.mean(ki) 					  # Mean of event count
		v = old_div(sum((ki-k)**2),N[i]) 			  # Variance of event count
		C[i] = old_div((2*k-v),((D[i])**2.))        	  # The cost Function

	# Optimal Bin Size Selection

	cmin = min(C)
	idx  = where(C==cmin)
	idx = int(idx[0])
	optD = D[idx]

	# plt.clf()
	# plt.close()

	edges = linspace(x_min,x_max,N[idx]+1)

	return edges

def convert_percentage_columns(df, percentage_columns):
    for column in percentage_columns:
        df = df.withColumn(column, regexp_extract(df[column], '^(((\s)*?[+-]?([0-9]+(\.[0-9][0-9]?)?)(\s)*)[^%]*)',1))
        df = df.withColumn(column, col(column).cast('double'))
    return df

def convert_dollar_columns(df, dollar_columns):
    for column in dollar_columns:
        df = df.withColumn(column, regexp_extract(df[column], '^([$]((\s)*?[+-]?([0-9]+(\.[0-9][0-9]?)?)(\s)*)*)',2))
        df = df.withColumn(column, col(column).cast('double'))
    return df

def select_y_axis_format(dataArray):
    if len(dataArray)>0:
        minval = min(dataArray)
        if minval >= 0.01:
            return ".2f"
        elif minval < 0.01:
            return ".4f"
    else:
        return ".2f"

def humanize_time(time_in_secs):
    '''
    Takes time in seconds (67856) and converts to 12 hours 13 minutes
    '''
    time_in_secs = int(round(time_in_secs))
    hours = old_div(time_in_secs,3600)
    minutes = old_div((time_in_secs - (hours*3600)),60)
    if time_in_secs < 60:
        return "{} Seconds".format(time_in_secs)
    return "{} Hrs {} Mins".format(hours, minutes)

def get_dataset_name(filepath):
    filelist = filepath.split('/')
    filename = filelist[-1]
    return filename



if __name__ == '__main__':
    x = frange(0.01,0.02,5)
