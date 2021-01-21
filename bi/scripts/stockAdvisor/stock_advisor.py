from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import random
import json
import urllib.request, urllib.error, urllib.parse
from collections import Counter
import operator
from collections import ChainMap
import numpy as np
import pandas as pd
from datetime import datetime
import scipy.stats as scs
from pyspark.sql import SQLContext
from statsmodels.formula.api import ols
import requests
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData, TableData, ModelSummary,PopupData,NormalCard,ParallelCoordinateData,DataBox,WordCloud
from bi.common import NormalChartData, ChartJson

class StockAdvisor(object):

    def __init__(self, spark, stockNameList,dataframe_context,result_setter):
        self._spark = spark
        self._stockNameList = stockNameList
        self._sqlContext = SQLContext(self._spark)
        self._dataAPI = dataframe_context.get_stock_data_api()
        self._hdfsBaseDir = dataframe_context.get_stock_data_path()
        self.dataFilePath = self._dataAPI+"?stockDataType={}&stockName={}"
        self._runEnv = dataframe_context.get_environement()
        self.BASE_DIR = "file:///home/marlabs/Documents/mAdvisor/Datasets/"
        self._dateFormat = "%Y%m%d"
        self._dataframe_context = dataframe_context
        self._percentage = int((80 /(((len(self._stockNameList)*2))+1)))
        self._stock_per = 0

    def read_csv(self, file_name):
        print("Reading File : ", file_name + ".csv")
        name = self.BASE_DIR + file_name + ".csv"
        df = (self._sqlContext.read
         .format("com.databricks.spark.csv")
         .option("header", "true")
         .load(name))
        return df
    def stock_status(self,value):
        self._stock_per = value + self._stock_per
        return self._stock_per
    def read_json(self, filepath):
        with open(filepath) as f:
            df = json.load(f)
            df = pd.DataFrame(df)
            return df
    def read_ankush_concepts(self,url):
        req = urllib.request.urlopen(url)
        req_data = req.read()
        return json.loads(req_data.decode('utf-8'))

    def read_ankush_json(self,url):
        req = urllib.request.urlopen(url)
        req_data = req.read()
        randNO = str(int(random.random()*10000000))
        tempFileName = "/tmp/temp{}.json".format(randNO)
        print(tempFileName)
        tf = open(tempFileName,"w")
        tf.write(req_data)
        tf.close()
        df = self._spark.read.json("file://"+tempFileName)
        return df

#    def read_hdfs_json(self,filepath):
#        print("filepath : ", filepath)
#        df = self._spark.read.json(filepath)
#        return df
    def read_hdfs_json(self,filepath):
        print("filepath : ", filepath)
        with open(filepath) as f:
            df = json.load(f)
            df = pd.DataFrame(df)
        return df

    def unpack_df(self, df):
        print("Unpacking the dataframe")
        old = df.toPandas()
        new_pd = old[['stock','source','final_url','time','title','short_desc','google_url','content']].copy()
        new = self._spark.createDataFrame(new_pd)

    def change_date_format(self,dateString):
        formattedString = str(datetime.strptime(str(dateString),self._dateFormat).date())
        return formattedString

    def get_stock_articles(self, df):
        #return df.count()
        return len(df)

    def get_stock_sources(self, df):
        #return df.select("source").distinct().count()
        return df['source'].nunique()

#    def get_stock_sentiment(self, df):
#        sentiment = 0
#        for row in df.rdd.collect():
#            sentimentLabel = row['sentiment']['document']['label']
#            if sentimentLabel in ["positive","neutral"]:
#                sentiment += row['sentiment']['document']['score']
#            else:
#                sentiment += (row['sentiment']['document']['score'])
#        return sentiment/float(df.count())
    def get_stock_sentiment(self, df):
        sentiment = np.mean([row['document']['score'] for row in df['sentiment']])
        #sentiment = np.mean([row['document']['score'] if row['document']['label'] != 'negative' else -row['document']['score'] for row in df['sentiment']])
        return sentiment


    def avg_sentiment_wrt_date(self,change, date):
        count = 0
        sentiment_sum = 0
        for tup in change:
            if tup[0] == date:
                sentiment_sum = sentiment_sum + tup[1]
                count = count + 1
        avg_sentiment = sentiment_sum / count
        return avg_sentiment

#    def get_sentiment_change(self, df):
#        change = list((x["time"], x["sentiment"]["document"]["score"]) for x in df.rdd.sortBy(lambda x : x["time"], ascending=True).collect())
#        latest_date = change[-1][0]
#        old_date = change[0][0]
#        latest_avg = self.avg_sentiment_wrt_date(change, latest_date)
#        old_avg = self.avg_sentiment_wrt_date(change, old_date)
#       #return change[len(change)-1][1] - change[0][1]
#        return latest_avg - old_avg
    def get_sentiment_change(self, average_sentiment_per_date):
        dates = list(average_sentiment_per_date.keys())
        dates.sort()
        return average_sentiment_per_date[dates[-1]] - average_sentiment_per_date[dates[0]]

    def get_number_articles_per_source(self, df):
        #output = dict(df.groupby('source').count().rdd.collect())
        # print "*"*50
        # print output
        # print "*"*50
        #return output
        output = dict(df['source'].value_counts())
        return output

#    def get_average_sentiment_per_source(self, df, number_articles_per_source):
#        return_dict = {}
#        for item in number_articles_per_source.items():
#            temp = df.filter(df.source == item[0])
#            avg_sum = 0
#            for inner_row in temp.select("sentiment").collect():
#                avg_sum = avg_sum + inner_row["sentiment"]["document"]["score"]
#            avg_sent = round(avg_sum/item[1],2)
#            return_dict.update({item[0]:avg_sent})
#        #for item in list(number_articles_per_source.keys()):
#            #return_dict[item] = list(df.filter(df.source == item).groupBy(df.sentiment.document.score).avg().collect()[0].asDict().values())[0]
#        return return_dict
    def get_average_sentiment_per_source(self, df, number_articles_per_source):
        return_dict = {}
        for source in number_articles_per_source.keys():
            return_dict[source] = np.mean([item['document']['score'] for item in list(df[df.source == source].groupby('source')['sentiment'])[0][1]])
        return return_dict

#    def get_average_sentiment_per_date(self, df):
#        return_dict = {}
#        for item in dict(df.groupby('time').count().rdd.collect()):
#            temp = df.filter(df.time == item)
#            avg_sum = 0
#            count = 0
#            for inner_row in temp.select("sentiment").collect():
#                avg_sum = avg_sum + inner_row["sentiment"]["document"]["score"]
#                count = count+1
#            avg_sent = round(avg_sum / count, 2)
#            return_dict.update({item: avg_sent})
#            #return_dict[item] = list(df.filter(df.time == item).groupBy(df.sentiment.document.score).avg().collect()[0].asDict().values())[0]
#        return return_dict
    def get_average_sentiment_per_date(self, df):
        return_dict = {}
        df.sort_values(by='time', inplace=True)
        df.reset_index(drop=True, inplace=True)
        for time in df['time'].unique():
            return_dict[time] = np.mean(
                [item['document']['score'] for item in list(df[df.time == time].groupby('time')['sentiment'])[0][1]])
        return return_dict

#    def get_top_keywords(self, df):
#        return dict((x['text'], x['relevance']) for x in df.select('keywords').rdd.flatMap(lambda x: x).flatMap(lambda x: x).sortBy(lambda x: x['relevance'], ascending=False).collect())
    def get_top_keywords(self, df):
        inter = dict(ChainMap(*df['keywords'].apply(lambda x: {keyword['text']: keyword['relevance'] for keyword in x})))
        return {k: v for k, v in sorted(inter.items(), key=lambda item: item[1], reverse=True)}

#    def get_top_events(self, df):
#        positive_articles = list((x['title'], x['sentiment']['document']['score']) for x in df.rdd.sortBy(lambda x: x['sentiment']['document']['score'], ascending=False).filter(lambda x : x['sentiment']['document']['score'] > 0).collect())
#        negative_articles = list((x['title'], x['sentiment']['document']['score']) for x in df.rdd.sortBy(lambda x: x['sentiment']['document']['score'], ascending=False).filter(lambda x : x['sentiment']['document']['score'] < 0).collect())
#        return (positive_articles, negative_articles)
    def get_top_events(self, df):
        inter_positive = {row['title']: row['sentiment']['document']['score'] for index, row in
                          df[['title', 'sentiment']].iterrows()}
        positive_articles = {k: v for k, v in sorted(inter_positive.items(), key=lambda item: item[1], reverse=True)}

        inter_negative = {row['title']: row['sentiment']['document']['score'] for index, row in
                          df[['title', 'sentiment']].iterrows()}
        negative_articles = {k: v for k, v in sorted(inter_negative.items(), key=lambda item: item[1], reverse=False)}
        return (positive_articles, negative_articles)

#    def get_stock_change(self, df_historic):
#        df_historic = df_historic.toPandas()
#        df_historic= df_historic.sort_values(by='date')
#        df_historic["close"] = df_historic["close"].astype("float32")
#        df_historic["close_pct_change"] = df_historic["close"].pct_change()
#        df_historic = df_historic.fillna(0)
#        max_increase_close = max(df_historic["close_pct_change"])
#        max_decrease_close = min(df_historic["close_pct_change"])
#        max_values = [max_decrease_close,max_increase_close]
#        start_price = float(df_historic['close'][0])
#        end_price = float(df_historic['close'][df_historic.shape[0]-1])
#        #sorted_list = df_historic.rdd.sortBy(lambda x: x['date'], ascending=True).collect()
#        #start_price = float(sorted_list[0]['close'])
#        #end_price = float(sorted_list[-1]['close'])
#        #print(start_price,end_price)
#        #return (end_price-start_price, old_div(((end_price-start_price)*100.0),start_price) )
#        return (max_values,end_price-start_price, old_div(((end_price - start_price) * 100.0), start_price))
    def get_stock_change(self, df_historic):
        df_historic['close'].dropna(inplace=True)
        df_historic.sort_values(by='date', inplace=True)
        df_historic.reset_index(drop=True, inplace=True)
        df_historic['close'] = pd.to_numeric(df_historic['close'])
        df_historic['close_change'] = df_historic['close'].diff()
        df_historic['close_percent_change'] = df_historic['close'].pct_change()
        start_price = df_historic['close'][0]
        end_price = df_historic['close'].iloc[-1]
        max_increase_close = round(df_historic['close_percent_change'].max() * 100, 2)
        max_decrease_close = round(df_historic['close_percent_change'].min() * 100, 2)
        max_values = [max_decrease_close, max_increase_close]
        return (max_values,end_price-start_price, old_div(((end_price - start_price) * 100.0), start_price))


    def get_stock_start_end_value(self, df_historic):
        df_historic.sort_values(by='date', inplace=True)
        df_historic.reset_index(drop=True, inplace=True)
        start_price = pd.to_numeric(df_historic['close'][0])
        end_price = pd.to_numeric(df_historic['close'].iloc[-1])
        return (start_price,end_price)
#    def get_stock_start_end_value(self, df_historic):
#        sorted_list = df_historic.rdd.sortBy(lambda x: x['date'], ascending=True).collect()
#        start_price = float(sorted_list[0]['close'])
#        end_price = float(sorted_list[-1]['close'])
#        return (start_price,end_price)

    def get_capitalized_name(self,word):
        capWord = ""
        for letter in word:
            capWord += letter.capitalize()
        return capWord

    def identify_concepts(self, df):
        # temp_fun = udf( lambda x: self.get_concepts_for_item(x), ArrayType)
        # new_df = df.withColumn("concepts", temp_fun(col("keywords")))
        # new_df.printSchema()
        return df

#    def load_concepts_from_json(self):
#        concepts = {}
#        for item in self._spark.read.json(self.BASE_DIR + "concepts.json").rdd.collect():
#            cur_dict = item.asDict()
#            for k in cur_dict:
#                concepts[k] = cur_dict[k]
#        return concepts

    def load_concepts_from_json(self,filepath):
        with open(filepath) as f:
            concepts = json.load(f)
        return concepts

    def get_concepts_for_item(self, item):
        cur_keywords = [item["text"].lower() for item in item["keywords"]]
        cur_concepts = []
        # print set(keywords)
        for key in self.concepts:
            if set(self.concepts[key]).intersection(set(cur_keywords)):
                cur_concepts.append(key)
        return cur_concepts

    def initialize_overall_dict(self):
        data_dict_overall = {}
        data_dict_overall["number_articles"] = 0
        data_dict_overall["number_sources"] = 0
        data_dict_overall["avg_sentiment_score"] = 0
        data_dict_overall["stock_value_change"] = 0
        data_dict_overall["stock_percent_change"] = 0
        data_dict_overall["max_value_change"] = {}
        data_dict_overall["min_value_change"] = {}
        data_dict_overall["max_sentiment_change"] = {}
        data_dict_overall["number_articles_by_stock"] = {}
        data_dict_overall["number_articles_per_source"] = {}
        data_dict_overall["stocks_by_sentiment"] = {}
        data_dict_overall["top_keywords"] = {}
        data_dict_overall["nArticlesAndSentimentsPerConcept"] = {}

        return data_dict_overall

    def identify_concepts_python(self,df):
        df["concepts"] = df["keywords"].apply(self.get_sub_concepts_for_item_python)
        return df

    # def get_sub_concepts_for_item_python(self, item):
    #     cur_keywords = [k["text"].lower() for k in item]
    #     cur_sentiments = [k["sentiment"]["score"] if True in [k["sentiment"]["label"] == "positive",k["sentiment"]["label"] == "neutral"]  else -k["sentiment"]["score"] for k in item]
    #     sentimentsDict = dict(list(zip(cur_keywords,cur_sentiments)))
    #     cur_concepts = {"conceptList":[],"conceptKeywordDict":{},"conceptAvgSentimentDict":{}}
    #     for key in self.concepts:
    #         keywordIntersection = list(set(self.concepts[key]).intersection(set(cur_keywords)))
    #         if len(keywordIntersection) > 0:
    #             cur_concepts["conceptList"].append(key)
    #             cur_concepts["conceptKeywordDict"][key] = keywordIntersection
    #             cur_concepts["conceptAvgSentimentDict"][key] = np.mean(np.array([sentimentsDict[x]  for x in keywordIntersection]))
    #     return cur_concepts

    def get_sub_concepts_for_item_python(self, item):
        cur_concepts = {"conceptList": [], "conceptKeywordDict": {}, "conceptAvgSentimentDict": {}}
        for dic in item:
            if dic['concept'] != None:
                if dic['concept'] not in cur_concepts["conceptList"]:
                    cur_concepts["conceptList"].append(dic['concept'])
                if dic['concept'] not in cur_concepts["conceptKeywordDict"]:
                    cur_concepts["conceptKeywordDict"][dic['concept']] = []
                    cur_concepts["conceptKeywordDict"][dic['concept']].append({dic['text']: dic['sentiment']['score']})
                else:
                    cur_concepts["conceptKeywordDict"][dic['concept']].append({dic['text']: dic['sentiment']['score']})
                if dic['concept'] not in cur_concepts["conceptAvgSentimentDict"]:
                    cur_concepts["conceptAvgSentimentDict"][dic['concept']] = []
                    cur_concepts["conceptAvgSentimentDict"][dic['concept']].append(dic['sentiment']['score'])
                else:
                    cur_concepts["conceptAvgSentimentDict"][dic['concept']].append(dic['sentiment']['score'])

        for key in cur_concepts['conceptAvgSentimentDict'].keys():
            cur_concepts['conceptAvgSentimentDict'][key] = np.mean(cur_concepts['conceptAvgSentimentDict'][key])
        return cur_concepts

    def get_number_articles_and_sentiments_per_concept(self,pandasDf):
        conceptNames = list(self.concepts.keys())
        valArray = []
        for val in conceptNames:
            valArray.append({"recordNumber":[],"articlesCount":0,"posArticles":0,"negArticles":0,"totalSentiment":0})
        conceptNameDict = dict(list(zip(conceptNames,valArray)))
        conceptCountArray = []
        sentimentArray = []
        for index, dfRow in pandasDf.iterrows():
            conceptNameDict = self.update_article_count_and_sentiment_score(conceptNameDict,dfRow,index)
            rowConceptArray = [1 if x in dfRow["concepts"]["conceptList"] else 0 for x in list(self.concepts.keys())]
            rowConceptArray.append(np.sum(np.array(rowConceptArray)))
            conceptCountArray.append(rowConceptArray)
            sentimentArray.append([dfRow["concepts"]["conceptAvgSentimentDict"][x] if x in dfRow["concepts"]["conceptAvgSentimentDict"] else 0 for x in list(self.concepts.keys())])
        outputDict = {}
        for key,value in list(conceptNameDict.items()):
            if value["articlesCount"] > 0:
                value["avgSentiment"] = round(float(value["totalSentiment"])/value["articlesCount"],2)
                outputDict[key] = value
            else:
                value["avgSentiment"] = 0
                outputDict[key] = value
        conceptCounterDf = pd.DataFrame(np.array(conceptCountArray),columns=[x+"_count" for x in list(self.concepts.keys())]+["totalCount"])
        sentimentCounterDf = pd.DataFrame(np.array(sentimentArray),columns=[x+"_sentiment" for x in list(self.concepts.keys())])
        self.pandasDf = pd.concat([pandasDf,conceptCounterDf,sentimentCounterDf], axis=1)
        #self.pandasDf["overallSentiment"] = self.pandasDf["sentiment"].apply(lambda x:x["document"]["score"] if x["document"]["label"] == "positive" else -x["document"]["score"])
        self.pandasDf["overallSentiment"] = self.pandasDf["sentiment"].apply(lambda x: x["document"]["score"])
        # print "*"*50
        # print "*"*50
        # print self.pandasDf[["overallSentiment","source"]].head(3)
        # print "*"*50
        return outputDict

    def get_number_articles_per_concept(self,stockConceptsData):
        """
        aggregate results of get_number_articles_and_sentiments_per_concept method
        """
        outputDict = dict(list(zip(list(self.concepts.keys()),[0]*len(list(self.concepts.keys())))))
        for stock,conceptDict in list(stockConceptsData.items()):
            for k,v in list(conceptDict.items()):
                outputDict[k] += v["articlesCount"]
        concepts = list(set([x.split("__")[0] for x in list(outputDict.keys())]))
        newDict = dict(list(zip(concepts,[0]*len(concepts))))
        for k,v in list(outputDict.items()):
            newDict[k.split("__")[0]] += v
        return newDict


    def update_article_count_and_sentiment_score(self,counterDict,dfRow,index):
        for concept in dfRow["concepts"]["conceptList"]:
            counterDict[concept]["articlesCount"] += 1
            counterDict[concept]["recordNumber"].append(index)
            absSentimentScore = dfRow["sentiment"]["document"]["score"]
            label = dfRow["sentiment"]["document"]["label"]
            sentimentScore = absSentimentScore if label == "positive" else -absSentimentScore
            counterDict[concept]["totalSentiment"] += dfRow['concepts']['conceptAvgSentimentDict'][concept]
            if (True if dfRow['sentiment']['document']['score']>0 else False):
                counterDict[concept]["posArticles"] += 1
            else:
                counterDict[concept]["negArticles"] += 1
        return counterDict

    def check_an_article_is_positive_or_not(self,keyWordArray):
        nPositive = []
        nNegative = []
        [nPositive.append(1) if obj["sentiment"]["label"] == "positive" else nNegative.append(1) for obj in keyWordArray]
        return True if sum(nPositive) > sum(nNegative) else False

    def create_chi_square_df(self,pandasDf,stockPriceData):
        conceptList = list(self.concepts.keys())
        conceptsData = pandasDf[["time"]+[x+"_count" for x in list(self.concepts.keys())]]
        # conceptCountDict = {}
        # for val in conceptList:
        #     conceptCountDict[val] = []
        # map(lambda x: self.get_chisquare_concept_columns(conceptCountDict,x),conceptsData["concepts"])
        # conceptCountDf = pd.DataFrame(conceptCountDict,index=conceptsData.index)
        # conceptsDF = pd.concat([conceptsData["time"], conceptCountDf], axis=1).groupby("time").sum().reset_index()
        conceptsDF = conceptsData.groupby("time").sum().reset_index()
        conceptsDF.index = conceptsDF["time"]
        stockDf = stockPriceData[["date","dayPriceDiff"]]
        stockDf.index = stockDf["date"]
        chiSquareDf = pd.concat([conceptsDF, stockDf], axis=1, join='inner')
        # print chiSquareDf.columns
        chiSquareDf.drop(['time','date'], axis=1, inplace=True)
        # print chiSquareDf.columns
        return chiSquareDf

    def get_chisquare_concept_columns(self,conceptCountDict,dfRow):
        for concept in list(conceptCountDict.keys()):
            if concept in dfRow["conceptList"]:
                conceptCountDict[concept].append(1)
            else:
                conceptCountDict[concept].append(0)

    def get_splits(self,pandasDf,colname,n_split):
        splits  = CommonUtils.frange(min(pandasDf[colname])-1,max(pandasDf[colname])+1,num_steps=n_split)
        splits = sorted(splits)
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
        splits_data = {"splits":splits,"splits_range":splits_range}
        return splits_data

    def cramers_stat(self,confusion_matrix):
        n = confusion_matrix.sum().sum()
        chi2 = scs.chi2_contingency(confusion_matrix)[0]
        return np.sqrt(old_div(chi2, (n*(min(confusion_matrix.shape)-1))))

    def calculate_chiSquare(self,df,targetCol):
        cramerStat = {}
        colsToIterate = [x for x in df.columns if x != targetCol]
        targetColSplits = self.get_splits(df,targetCol,3)["splits"]
        targetColGroupNames = ["grp"+str(idx) for idx in range(1,len(targetColSplits))]
        df["targetColBins"] = pd.cut(df[targetCol], targetColSplits, labels=targetColGroupNames)
        for col in colsToIterate:
            colSplits = self.get_splits(df,col,3)["splits"]
            colGroupNames = ["grp"+str(idx) for idx in range(1,len(colSplits))]
            df[col+"_bin_"] = pd.cut(df[col], colSplits, labels=colGroupNames)
            confusionMatrix = pd.crosstab(df["targetColBins"], df[col+"_bin_"])
            # Dropping rows and columns with zero sum
            confusionMatrix = confusionMatrix.loc[(confusionMatrix.sum(axis=1) != 0), (confusionMatrix.sum(axis=0) != 0)]
            cramerStat[col] = self.cramers_stat(confusionMatrix)
        return cramerStat

    def run_regression(self,df,targetCol):
        # print "~"*100
        colMaps = ["c"+str(idx) if x != targetCol else x for idx,x in enumerate(df.columns)]
        # print colMaps
        reverseMap = dict(list(zip(colMaps,df.columns)))
        # print reverseMap
        df.columns = colMaps
        reg_model = ols("{} ~ ".format(targetCol) +"+".join(list(set(df.columns) - {targetCol})), data=df).fit()
        # summarize our model
        model_summary = reg_model.summary()
        modelParams = reg_model.params
        modelParamsDf = pd.DataFrame({'id':modelParams.index, 'value':modelParams.values})
        # print modelParamsDf
        coeffDict = modelParamsDf.set_index('id').to_dict()["value"]
        reverseMappedCoef = {}
        for k,v in list(coeffDict.items()):
            if k != "Intercept":
                try:
                    reverseMappedCoef[reverseMap[k]] = coeffDict[k]
                except:
                    pass
            else:
                reverseMappedCoef[k] = coeffDict[k]
        # print reverseMappedCoef
        # print model_summary
        return reverseMappedCoef

    def get_number_articles_and_sentiments_per_source(self,pandasDf):
        pandasDf["articlesCount"] = 1
        grouped = pandasDf.groupby("source", as_index=False).agg({"overallSentiment":np.mean,"articlesCount":np.sum})
        grouped.columns = ["source","avgSentiment","articles"]
        output = list(grouped.T.to_dict().values())
        output = sorted(output,key=lambda x:x["articles"],reverse=True)
        return output

    #def get_datewise_stock_value_and_sentiment(self,pandasDf,stockPriceData):
        #relevantDf = pandasDf[["time","overallSentiment"]]
        #relevantDf.columns = ["date","overallSentiment"]
        #merged = pd.merge(relevantDf,stockPriceData[["close","date"]],on="date",how="inner")
        #merged["date"] = merged["date"].apply(self.change_date_format)
        #output = list(merged.T.to_dict().values())
        #output = sorted(output,key = lambda x:datetime.strptime(x["date"],"%Y-%m-%d"))
        #return output
#    def get_datewise_stock_value_and_sentiment(self,pandasDf, stockPriceData):
#        relevantDf = pandasDf.groupby("date").agg({"overallSentiment": 'mean'}).reset_index(drop=False)
#        relevantDf.columns = ['date', 'overallSentiment']
#        merged = pd.merge(relevantDf, stockPriceData[["close", "date"]], on="date", how="inner")
#        merged['date'] = merged.date.astype(str).apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:8])
#        output = list(merged.T.to_dict().values())
#        output = sorted(output, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
#        return output

    def sentiment_score_compute(self,pandasDf1):
        score = []
        for index, datarow in pandasDf1.iterrows():
            score.append(datarow['sentiment']['document']['score'])
        return score
    def get_datewise_stock_value_and_sentiment(self,pandasDf, stockPriceData):
        pandasDf['pre_date'] = pandasDf.date.astype(str).apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:8])
        #pandasDf.sort_values(by='pre_date', inplace=True)
        date_list = list(sorted(dict.fromkeys(pandasDf.pre_date)))
        senti_dict = {}
        pandasDf1 = pandasDf[(pandasDf.pre_date == date_list[0])]
        senti_dict.update({date_list[0]: np.mean(self.sentiment_score_compute(pandasDf1))})
        for i in range(len(date_list) - 1):
            pandasDf1 = pandasDf[(pandasDf.pre_date >= date_list[i]) & (pandasDf.pre_date <= date_list[i + 1])]
            senti_dict.update({date_list[i + 1]: np.mean(self.sentiment_score_compute(pandasDf1))})
        relevantDf = pd.DataFrame(senti_dict.items(), columns=['date', 'overallSentiment'])

        stockPriceData['close'] = stockPriceData['close'].apply(lambda x: float(x))
        stockPriceData['date1'] = stockPriceData.date.astype(str).apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:8])

        merged = pd.merge(relevantDf, stockPriceData[["close", "date1"]], left_on="date", right_on='date1', how="inner")
        output = list(merged.T.to_dict().values())
        output = sorted(output, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        print(output)
        return output
    def apply_counter(self,keyWordArray):
        output = [x["text"] for x in keyWordArray]
        countDict = dict(Counter(output))
        return countDict

    def get_top_entities(self,pandasDf):
        pandasDf["entitiesCount"] = pandasDf["keywords"].apply(self.apply_counter)
        finalCountDict = {}
        for index, dfRow in pandasDf.iterrows():
            finalCountDict = Counter(finalCountDict)+Counter(dfRow["entitiesCount"])
        finalCount = sorted(list(dict(finalCountDict).items()),key=lambda x:x[1],reverse=True)
        return [{"text":x[0],"value":x[1]} for x in finalCount][:50]

    def get_key_days_and_impactful_articles(self,pandasDf,stockPriceData):
        relevantDf1 = stockPriceData[["date","closePerChange"]]
        relevantDf1.columns = ["time","closePerChange"]
        relevantDf2 = pandasDf[["time","source","title","overallSentiment"]]
        merged = pd.merge(relevantDf2,relevantDf1,on="time",how="inner")
        merged = merged.sort_values(by=['closePerChange'],ascending=False)
        topIncrease = merged.iloc[0:2] #top2
        # print topIncrease.shape
        merged = merged.sort_values(by=['closePerChange'],ascending=True)
        topDecrease = merged.iloc[0:2] #top2
        # print topDecrease.shape
        outDf = pd.concat([topIncrease,topDecrease])
        outDf["time"] = outDf["time"].apply(self.change_date_format)
        # print outDf.shape
        output = [["Date","% increase/ Decrease stock Price","Source","Title","Sentiment"]]
        for idx,dfRow in outDf.iterrows():
            row = [dfRow["time"],str(CommonUtils.round_sig(dfRow["closePerChange"],sig=2))+"%",dfRow["source"],dfRow["title"],CommonUtils.round_sig(dfRow["overallSentiment"],sig=2)]
            output.append(row)
        return output

    def get_top_articles(self,pandasDf):
        relevantDf = pandasDf[["time","source","title","overallSentiment"]]
        relevantDf["sentimentPerChange"] = relevantDf["overallSentiment"].pct_change()
        relevantDf = relevantDf.fillna(0)
        relevantDf['sentimentPerChange'].replace([np.inf, -np.inf], 100, inplace=True)

        relevantDf = relevantDf.sort_values(by=['overallSentiment'],ascending=False)
        topIncrease = relevantDf.iloc[0:3] #top3
        relevantDf = relevantDf.sort_values(by=['overallSentiment'],ascending=True)
        topDecrease = relevantDf.iloc[0:3] #top3
        outDf = pd.concat([topIncrease,topDecrease])
        outDf["time"] = outDf["time"].apply(self.change_date_format)
        output = [["Date","Source","Title","Sentiment","% increase/ Decrease"]]
        for idx,dfRow in outDf.iterrows():
            row = [dfRow["time"],dfRow["source"],dfRow["title"],CommonUtils.round_sig(dfRow["overallSentiment"],sig=2),str(CommonUtils.round_sig(dfRow["sentimentPerChange"],sig=2))+"%"]
            output.append(row)
        return output

    def get_average_sentiment_per_concept(self, nArticlesAndSentimentsPerConcept):
        concept_list = (set([obj.split("__")[0] for obj in list(nArticlesAndSentimentsPerConcept.keys())]))
        sentimentDict = dict(list(zip(concept_list,[0]*len(concept_list))))
        for each_concept in nArticlesAndSentimentsPerConcept:
            for each_item in concept_list:
                if each_concept.split("__")[0]==each_item:
                    sentimentDict[each_item] += nArticlesAndSentimentsPerConcept[each_concept]['avgSentiment']
        return sentimentDict

    def get_recommendation_data(self, stock_symbol, avg_sentiment_score , nArticlesAndSentimentsPerConcept, start_end_values, stock_percent_change):
        stock_symbol = self.get_capitalized_name(stock_symbol)
        avg_sentiment_score = round(avg_sentiment_score,2)
        stock_percent_change = round(stock_percent_change,2)
        sentiment_by_concept = self.get_average_sentiment_per_concept(nArticlesAndSentimentsPerConcept)
        concept_name = max(iter(sentiment_by_concept.items()), key=operator.itemgetter(1))[0]
        if avg_sentiment_score >= 0:
            score_polarity = "positive"
        else:
            score_polarity = "negative"

        if start_end_values[1]-start_end_values[0] > 0:
            stock_grown_dropped = "grown"
            percentage_growth_drop = "growth"
        else:
            stock_grown_dropped = "dropped"
            percentage_growth_drop = "drop"

        if stock_percent_change >= 1:
            outlook = "good"
            recom = "add"
        elif stock_percent_change<1 and stock_percent_change>=0:
            outlook = "moderate"
            recom = "hold"
        else:
            outlook = "below par"
            recom = "trim"
        # recommendations_data = []
        # recommendations_data.append("<li>Based on the news articles analysed, <b>{}</b> has a <b>{}</b> score of <b>{}</b>, which is strongly driven by events in <b>{}</b>.</li>".format(stock_symbol, score_polarity, avg_sentiment_score, concept_name))
        # recommendations_data.append("<li>The stock price has {} from {} to {}, showing a <b>{}</b> of <b>{}%</b></li>.".format(stock_grown_dropped, start_end_values[0], start_end_values[1], percentage_growth_drop, stock_percent_change))
        # recommendations_data.append("<li>The interim outlook for this stock is <b>{}</b> and hence the recommendation is <b>{}</b>.</li>".format(outlook, recom))
        recommendations_data = "<li>Based on the news articles analysed, <b>{}</b> has a <b>{}</b> score of <b>{}</b>, which is strongly driven by events in <b>{}</b>.</li><li>The stock price has {} from {} to {}, showing a <b>{}</b> of <b>{}%</b>.</li><li>The interim outlook for this stock is <b>{}</b> and hence the recommendation is <b>{}</b>.</li>".format(stock_symbol, score_polarity, avg_sentiment_score, concept_name, stock_grown_dropped, start_end_values[0], start_end_values[1], percentage_growth_drop, stock_percent_change, outlook, recom)
        return recommendations_data

    def Run(self):
        print("In stockAdvisor")
        messageURL = self._dataframe_context.get_message_url()
        ignoreMsg = self._dataframe_context.get_message_ignore()
        data_dict_stocks = {}
        data_dict_overall = self.initialize_overall_dict()
        if self._runEnv == "debugMode":
            conceptFilepath = self.BASE_DIR + "concepts.json"
            self.concepts = self.load_concepts_from_json(conceptFilepath)
        else:
            import requests
            api = requests.get(self.dataFilePath.format("concepts",""))
            self.concepts = api.json()
        masterDfDict = {}
        stockDict = {}
        stockPriceTrendDict = {}
        working_stock_list = []
        for stock_symbol in self._stockNameList:
            print("Analyzing data for Stock: " +stock_symbol)
            try:
                #-------------- Read Operations ----------------
                weights = self.stock_status(self._percentage)
                progressMessage = CommonUtils.create_progress_message_object(analysisName="stockAdvisor",
                                                                             stageName="custom",
                                                                             messageType="info",
                                                                             shortExplanation="Analyzing " + str.upper(stock_symbol) + " Data",
                                                                             stageCompletionPercentage=weights,
                                                                             globalCompletionPercentage=weights,
                                                                             display=True)
                #CommonUtils.save_progress_message(messageURL, progressMessage, ignore=ignoreMsg)
                stockDict[stock_symbol] = {}
                if self._runEnv == "debugMode":
                    df = self.read_json(self.BASE_DIR+stock_symbol+".json")
                    df_historic = self.read_json(self.BASE_DIR+stock_symbol+"_historic.json")
                else:
                    # df = self.read_ankush_json(self.dataFilePath.format("bluemix",stock_symbol))
                    # df_historic = self.read_ankush_json(self.dataFilePath.format("historical",stock_symbol))
                    df = pd.read_json(self.dataFilePath.format("bluemix",stock_symbol))
                    df_historic = pd.read_json(self.dataFilePath.format("historical",stock_symbol))
                #stockPriceData = df_historic.select(["date","close","open"]).toPandas()
                stockPriceData = df_historic[["date", "close", "open"]]
                stockPriceData["close"] = stockPriceData["close"].apply(float)
                stockPriceData["open"] = stockPriceData["open"].apply(float)
                stockPriceData["dayPriceDiff"] = stockPriceData["close"] - stockPriceData["open"]
                stockPriceData["closePerChange"] = stockPriceData["close"].pct_change()
                stockPriceData = stockPriceData.fillna(0)

                #df = df.filter(df.sentiment. isNotNull())
                #df1 =df.toPandas()
                #df1=df1[df1['sentiment'].notnull()]
                df = df[df['sentiment'].notnull()]
                df.reset_index(drop=True, inplace=True)
                df1 = df
                self.pandasDf = self.identify_concepts_python(df1)



                # overall Distribution of articles and sentiments by concecpts
                # needs final presentation
                nArticlesAndSentimentsPerConcept = self.get_number_articles_and_sentiments_per_concept(self.pandasDf)
                nArticlesAndSentimentsPerSource = self.get_number_articles_and_sentiments_per_source(self.pandasDf)
                # print nArticlesAndSentimentsPerSource
                data_dict_overall["nArticlesAndSentimentsPerConcept"][stock_symbol] = nArticlesAndSentimentsPerConcept
                stockDict[stock_symbol]["articlesAndSentimentsPerConcept"] = nArticlesAndSentimentsPerConcept
                stockDict[stock_symbol]["articlesAndSentimentsPerSource"] = nArticlesAndSentimentsPerSource
                stockPriceAndSentimentTrend = self.get_datewise_stock_value_and_sentiment(self.pandasDf,stockPriceData)
                stockDict[stock_symbol]["stockPriceAndSentimentTrend"] = stockPriceAndSentimentTrend
                stockDict[stock_symbol]["topEntities"] = self.get_top_entities(self.pandasDf)
                stockDict[stock_symbol]["keyDays"] = self.get_key_days_and_impactful_articles(self.pandasDf,stockPriceData)
                stockDict[stock_symbol]["keyArticles"] = self.get_top_articles(self.pandasDf)

                regDf = self.pandasDf[["time"]+[x+"_count" for x in list(self.concepts.keys())]]
                #regDf = self.pandasDf[["time", "overallSentiment", "totalCount"] + [x + "_sentiment" for x in list(self.concepts.keys())]]
                regDfcolumns = regDf.columns.tolist()
                regDfcolumns.remove('time')
                regDfgrouped = regDf.groupby('time').sum().reset_index()
                regDfgrouped["date"] = regDfgrouped["time"]
                #regDfgrouped.index = regDfgrouped["time"]
                stockDf  = stockPriceData[["close","date"]]
                #stockDf.index = stockDf["date"]
                #priceTrendDict = stockDf.to_dict()["close"]
                #tockPriceTrendDict[stock_symbol] = priceTrendDict
                regDfFinal =  pd.merge(regDfgrouped, stockDf, on='date')
                stockDf.index = stockDf["date"]
                priceTrendDict = stockDf.to_dict()["close"]
                stockPriceTrendDict[stock_symbol] = priceTrendDict
                # print regDfgrouped.columns
                # print stockDf.columns
                #regDfFinal =  pd.concat([regDfgrouped, stockDf], axis=1, join='inner')
                regDfFinal.drop(["date"],axis = 1,inplace=True)
                regDfFinal.columns = ["time"]+regDfcolumns+["close"+"_"+stock_symbol]
                masterDfDict[stock_symbol] = regDfFinal

                # self.chiSquarePandasDf = self.create_chi_square_df(self.pandasDf,stockPriceData)
                # self.chiSquareDf = self._sqlContext.createDataFrame(self.chiSquarePandasDf)
                # self.chiSquareDict = self.calculate_chiSquare(self.chiSquarePandasDf,"dayPriceDiff")

                #-------------- Start Calculations ----------------
                number_articles = self.get_stock_articles(df)
                stockDict[stock_symbol]["numArticles"] = number_articles
                data_dict_overall["number_articles"] += number_articles
                data_dict_overall["number_articles_by_stock"][stock_symbol] = number_articles  #used for bar plot



                number_sources = self.get_stock_sources(df)
                stockDict[stock_symbol]["numSources"] = number_sources
                data_dict_overall["number_sources"] += number_sources

                avg_sentiment_score = self.get_stock_sentiment(df)
                stockDict[stock_symbol]["avgSentimetScore"] = avg_sentiment_score
                data_dict_overall["avg_sentiment_score"] += avg_sentiment_score
                data_dict_overall["stocks_by_sentiment"][stock_symbol] = avg_sentiment_score #used for bar plot

                #sentiment_change = self.get_sentiment_change(df)
                average_sentiment_per_date = self.get_average_sentiment_per_date(df)
                sentiment_change = self.get_sentiment_change(average_sentiment_per_date)
                stockDict[stock_symbol]["changeInSentiment"] = sentiment_change
                data_dict_overall["max_sentiment_change"][stock_symbol]=sentiment_change  #verify: this is start to end sentiment change
                # print "sentiment_change : ", sentiment_change

                (max_values,stock_value_change, stock_percent_change) = self.get_stock_change(df_historic)
                stockDict[stock_symbol]["stockValueChange"] = stock_value_change
                stockDict[stock_symbol]["stockValuePercentChange"] = stock_percent_change
                data_dict_overall["stock_value_change"] += stock_value_change
                data_dict_overall["stock_percent_change"] += stock_percent_change
                #data_dict_overall["max_value_change"][stock_symbol]=stock_value_change
                data_dict_overall["max_value_change"][stock_symbol] = max_values[-1]
                data_dict_overall["min_value_change"][stock_symbol] = max_values[0]
                # print "stock_value_change : ", stock_value_change
                # print "stock_percent_change : ", stock_percent_change

                number_articles_per_source = self.get_number_articles_per_source(df)
                stockDict[stock_symbol]["articlesPerSource"] = number_articles_per_source
                # print "number_articles_per_source : ", number_articles_per_source
                # data_dict_overall["number_articles_per_source"][stock_symbol]=number_articles_per_source
                data_dict_overall["number_articles_per_source"]= dict(Counter(number_articles_per_source) + Counter(data_dict_overall["number_articles_per_source"]))
                average_sentiment_per_source = self.get_average_sentiment_per_source(df, number_articles_per_source)
                # print "average_sentiment_per_source : ", average_sentiment_per_source


                # # number_articles_per_concept = self.get_number_articles_per_concept(unpacked_df)
                # # average_sentiment_per_concept = self.get_average_sentiment_per_concept(unpacked_df)
                #

                top_keywords = self.get_top_keywords(df)
                # print "top_keywords : ", top_keywords
                data_dict_overall["top_keywords"] = dict(Counter(top_keywords) + Counter(data_dict_overall["top_keywords"]))

                # average_stock_per_date = self.get_average_stock_per_date(unpacked_df)

                average_sentiment_per_date = self.get_average_sentiment_per_date(df)
                # print "average_sentiment_per_date : ", average_sentiment_per_date

                (top_events_positive, top_events_negative) = self.get_top_events(df)

                start_end_values = self.get_stock_start_end_value(df_historic)
                try:
                    stockDict[stock_symbol]['recommendations'] = self.get_recommendation_data(stock_symbol, avg_sentiment_score, nArticlesAndSentimentsPerConcept, start_end_values, stock_percent_change)
                except Exception as e:
                    print("Exception in getting recommendation : ", str(e))

                working_stock_list.append(stock_symbol)
            except Exception as e:
                stockDict.pop(stock_symbol, None)
                print("Analysis for stock failed : ", stock_symbol, " with error : ", str(e))
        self._stockNameList = working_stock_list
        working_stock_list = []
        for current_stock in self._stockNameList:
            try:
                weights = self.stock_status(self._percentage)
                progressMessage = CommonUtils.create_progress_message_object(analysisName="stockAdvisor",
                                                                             stageName="custom",
                                                                             messageType="info",
                                                                             shortExplanation="Applying Regression on  " + str.upper(current_stock) + " Data",
                                                                             stageCompletionPercentage=weights,
                                                                             globalCompletionPercentage=weights,
                                                                             display=True)
                #CommonUtils.save_progress_message(messageURL, progressMessage, ignore=ignoreMsg)
                regressionDf = masterDfDict[current_stock]
                regressionDf.set_index('time', inplace=True)
                remaining_stocks = list(set(self._stockNameList) - {current_stock})
                # if len(remaining_stocks) > 0:
                #     for other_stock in remaining_stocks:
                #         colsToConsider = ["time","overallSentiment","close"]
                #         otherStockDf = masterDfDict[other_stock][colsToConsider]
                #         otherStockDf.columns = [x+"_"+other_stock for x in colsToConsider]
                #         otherStockDf.index = otherStockDf["time"+"_"+other_stock]
                #         regressionDf = pd.concat([regressionDf,otherStockDf], axis=1, join='inner')
                #         regressionDf.drop(["time","time"+"_"+other_stock],axis=1,inplace=True)
                # print regressionDf.columns
                # print "-"*100
                # Run linear regression on the regressionDf dataframe
                regressionCoeff = self.run_regression(regressionDf,"close"+"_"+current_stock)
                if 'Intercept' in regressionCoeff: del regressionCoeff['Intercept']
                regCoeffArray = sorted([{"key":k,"value":v} for k,v in list(regressionCoeff.items())],key=lambda x:abs(x["value"]),reverse=True)
                stockDict[current_stock]["regCoefficient"] = regCoeffArray
                # print current_stock , " : regCoeffArray : ", regCoeffArray
                working_stock_list.append(current_stock)
            except Exception as e:
                stockDict.pop(current_stock, None)
                print("Failed for : ", current_stock, " with error : ", str(e))
        weights = self.stock_status(self._percentage)
        progressMessage = CommonUtils.create_progress_message_object(analysisName="stockAdvisor",
                                                                     stageName="custom",
                                                                     messageType="info",
                                                                     shortExplanation="Calculating Stock Price Trend",
                                                                     stageCompletionPercentage=weights,
                                                                     globalCompletionPercentage=weights,
                                                                     display=True)
        #CommonUtils.save_progress_message(messageURL, progressMessage, ignore=ignoreMsg)
        # print "#"*100
        self._stockNameList = working_stock_list
        number_stocks = len(self._stockNameList)
        if number_stocks == 0:
            return {}

        stockPriceTrendArray = []
        dateList = list(stockPriceTrendDict[self._stockNameList[0]].keys())
        stockPriceTrendArray = list(stockPriceTrendDict[self._stockNameList[0]].items())
        capNameList = [self.get_capitalized_name(x) for x in self._stockNameList]
        capNameDict = dict(list(zip(self._stockNameList,capNameList)))
        stockPriceTrendArray = [{"date":obj[0],capNameList[0]:CommonUtils.round_sig(obj[1],sig=2)} for obj in stockPriceTrendArray]

        for obj in stockPriceTrendArray:
            for stockName in self._stockNameList[1:]:
                stock_price_dates = list(stockPriceTrendDict[stockName].keys())
                if obj["date"] not in stock_price_dates:
                    if len(stock_price_dates) > 0 :
                        stockPriceTrendDict[stockName][obj["date"]] = old_div(sum([stockPriceTrendDict[stockName][key] for key in stock_price_dates]),len(stock_price_dates))
                    else:
                        stockPriceTrendDict[stockName][obj["date"]] = 0.0
                obj.update({capNameDict[stockName]:CommonUtils.round_sig(stockPriceTrendDict[stockName][obj["date"]],sig=2)})
        stockPriceTrendArrayFormatted = []
        for obj in stockPriceTrendArray:
            formattedDateKey = str(datetime.strptime(str(obj["date"]),self._dateFormat).date())
            obj.update({"date":formattedDateKey})
            stockPriceTrendArrayFormatted.append(obj)
        stockPriceTrendArrayFormatted = sorted(stockPriceTrendArrayFormatted,key=lambda x:datetime.strptime(str(x["date"]),"%Y-%m-%d"),reverse=False)
        data_dict_overall["price_trend"] = stockPriceTrendArrayFormatted

        data_dict_overall["avg_sentiment_score"] = old_div(data_dict_overall["avg_sentiment_score"],number_stocks)
        data_dict_overall["stock_value_change"] = old_div(data_dict_overall["stock_value_change"],number_stocks)
        data_dict_overall["stock_percent_change"] = old_div(data_dict_overall["stock_percent_change"],number_stocks)

        data_dict_overall["number_articles_by_concept"] = self.get_number_articles_per_concept(data_dict_overall["nArticlesAndSentimentsPerConcept"])

        key, value = max(iter(data_dict_overall["max_value_change"].items()), key = lambda p: p[1])
        data_dict_overall["max_value_change_overall"] = (self.get_capitalized_name(key),round(value,4))
        key, value = min(iter(data_dict_overall["min_value_change"].items()), key = lambda p: p[1])
        data_dict_overall["min_value_change_overall"] = (self.get_capitalized_name(key),round(value,4))

        key,value = max(iter(data_dict_overall["max_sentiment_change"].items()), key = lambda p: p[1])
        data_dict_overall["max_sentiment_change_overall"] = (self.get_capitalized_name(key),value)

        # print data_dict_overall
        finalResult = NarrativesTree()
        overviewNode = NarrativesTree()
        stockNode = NarrativesTree()
        overviewNode.set_name("Overview")
        stockNode.set_name("Single Stock Analysis")
        overviewCard = MLUtils.stock_sense_overview_card(data_dict_overall)
        overviewNode.add_a_card(overviewCard)
        finalResult.add_a_node(overviewNode)
        individualStockNodes = MLUtils.stock_sense_individual_stock_cards(stockDict)
        stockNode.add_nodes(individualStockNodes)
        finalResult.add_a_node(stockNode)

        return finalResult
