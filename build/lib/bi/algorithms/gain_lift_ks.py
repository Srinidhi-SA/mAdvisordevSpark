from __future__ import division
from builtins import object
from past.utils import old_div
from pyspark.sql.functions import udf, when, row_number
from pyspark.sql.types import FloatType
from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.sql.functions import udf,desc,monotonically_increasing_id
from pyspark.ml.feature import QuantileDiscretizer
import pandas as pd
import numpy as np


class GainLiftKS(object):
    def __init__(self, df, proba_column, predicted_column, target_col,posLabel, spark):
        self._df = df
        self._spark = spark
        self._target_column = target_col
        self._proba_column = proba_column
        self._predicted_column = predicted_column
        self._posLabel = posLabel

    def Run(self):
        def Lift(cum_resp,decil_no):
            return (cum_resp/float(decil_no+1))
        self._df=self._df.orderBy(self._proba_column,ascending=False)
        self._df = self._df.withColumn("id", monotonically_increasing_id())
        # w = Window.orderBy(desc(self._proba_column))
        # self._df = self._df.withColumn('id',row_number().over(w))
        discretizer = QuantileDiscretizer(numBuckets=10, inputCol="id", outputCol="deciles")
        self._df = discretizer.fit(self._df).transform(self._df)
        Rank=self._df.groupby('deciles').agg(F.count(self._df[self._proba_column]).alias('cnt'), F.count(when(self._df[self._target_column] == int(self._posLabel), True)).alias('cnt_resp'))
        Rank=Rank.withColumn('cnt_non_resp',Rank['cnt']-Rank['cnt_resp'])
        Rank=Rank.orderBy('deciles',ascending=True)
        cumsum_window = (Window.orderBy(Rank['deciles']).rangeBetween(Window.unboundedPreceding, Window.currentRow))
        Rank=Rank.withColumn("cum_resp",F.sum('cnt_resp').over(cumsum_window))
        Rank=Rank.withColumn("cum_non_resp",F.sum('cnt_non_resp').over(cumsum_window))
        Rank=Rank.withColumn("% Responders(Cumulative)",F.round(old_div(Rank["cum_resp"]*100,Rank.select(F.sum('cnt_resp')).collect()[0][0]),2))
        Rank=Rank.withColumn("% Non-Responders(Cumulative)",F.round(old_div(Rank["cum_non_resp"]*100,Rank.select(F.sum('cnt_non_resp')).collect()[0][0]),2))
        Rank=Rank.withColumn("cum_population",F.sum("cnt").over(cumsum_window))
        Rank=Rank.withColumn("pop_pct_per_decile",F.round(old_div(Rank["cnt"]*100,Rank.select(F.sum('cnt')).collect()[0][0])))
        Rank=Rank.withColumn("% Population(Cumulative)",F.round(F.sum('pop_pct_per_decile').over(cumsum_window)))
        Rank=Rank.withColumn("KS",F.round(Rank["% Responders(Cumulative)"] - Rank["% Non-Responders(Cumulative)"],2))
        Rank=Rank.withColumn("Lift at Decile",F.round(old_div(Rank["cnt_resp"]*Rank["pop_pct_per_decile"]*100,Rank.select(F.sum('cnt_resp')).collect()[0][0]),2))
        Rank = Rank.withColumn("id", monotonically_increasing_id())
        Lift_udf=udf(lambda x,y:Lift(x,y),FloatType())
        Rank=Rank.withColumn("Total_Lift",F.round(Lift_udf("cum_resp","id"),2))
        Rank=Rank.drop('id')
        return(Rank)

    def Rank_Ordering(self):
        self._df = self._df.sort_values(self._proba_column, ascending=False)
        self._df["id"] = self._df.index
        self._df['deciles'] = pd.qcut(self._df['id'], 10, labels=np.arange(0.0, 10.0, 1))
        x = self._df
        y = self._proba_column
        Target = self._target_column
        Rank = self._df.groupby('deciles').apply(lambda x: pd.Series([np.size(x[y]), np.sum(x[Target] == int(self._posLabel))],
        index=(["cnt", "cnt_resp"]))).reset_index()
        Rank["cnt_non_resp"] = Rank["cnt"] - Rank["cnt_resp"]
        Rank["cum_resp"] = Rank["cnt_resp"].cumsum()
        Rank["cum_non_resp"] = Rank["cnt_non_resp"].cumsum()
        Rank["% Responders(Cumulative)"] = round(Rank["cum_resp"] * 100 / np.sum(Rank["cnt_resp"]), 2)
        Rank["% Non-Responders(Cumulative)"] = round(Rank["cum_non_resp"] * 100 / np.sum(Rank["cnt_non_resp"]), 2)
        Rank["cum_population"] = Rank["cnt"].cumsum()
        Rank["pop_pct_per_decile"] = round(Rank["cnt"] * 100 / np.sum(Rank["cnt"]), 2)
        Rank["% Population(Cumulative)"] = round(Rank["pop_pct_per_decile"].cumsum(), 2)
        Rank["KS"] = round(Rank["% Responders(Cumulative)"] - Rank["% Non-Responders(Cumulative)"], 2)
        Rank["Lift at Decile"] = round(Rank["cnt_resp"] * Rank["pop_pct_per_decile"] * 100 / np.sum(Rank["cnt_resp"]),2)
        Rank["id"] = Rank.index
        Rank["Total_Lift"] = round(Rank["cum_resp"] / (Rank["id"] + 1), 2)
        Rank = Rank.drop(columns="id")
        return Rank
