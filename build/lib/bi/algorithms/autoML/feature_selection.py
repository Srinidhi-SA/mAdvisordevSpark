import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import ExtraTreesRegressor
from scipy import stats
from sklearn.preprocessing import LabelEncoder
#pysaprk importances
from pyspark.sql.functions import *
from pyspark.ml.classification import  RandomForestClassifier
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator, VectorAssembler
from pyspark.ml import Pipeline
from bi.stats.util import Stats
from bi.algorithms import utils as MLUtils
import pyspark.sql.functions as F
from past.utils import old_div
import math

class FeatureSelection():

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type,pandas_flag):
        self.data_frame = data_frame
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict['SelectedColsTree'] = []
        self.data_change_dict['SelectedColsLinear'] = []
        self._pandas_flag =  pandas_flag

    #def extractFeature_colname(self, featureImp, dataset, featuresCol):
    #    list_extract = []
    #    for i in dataset.schema[featuresCol].metadata["ml_attr"]["attrs"]:
    #        list_extract = list_extract + dataset.schema[featuresCol].metadata["ml_attr"]["attrs"][i]
    #    varlist = pd.DataFrame(list_extract)
    #    varlist['score'] = varlist['idx'].apply(lambda x: featureImp[x])
    #    varlist = varlist[varlist.score>0].sort_values('score', ascending = False)
    #    return (varlist.name.tolist())

    def feature_imp_pyspark(self):
        num_var = [i[0] for i in self.data_frame.dtypes if ((i[1]=='int') | (i[1]=='double')) & (i[0]!=self.target)]
        num_var = [col for col in num_var if not col.endswith('indexed')]
        # labels_count = [len(self.data_frame.select(col).distinct().collect()) for col in num_var]
        labels_count = [len(self.data_frame.agg((F.collect_set(col).alias(col))).first().asDict()[col]) for col in num_var]
        labels_count.sort()
        max_count =  labels_count[-1]
        #one_hot = [col for col in self.data_frame.columns if col.endswith('_indexed_encoded')]
        #num_var.extend(one_hot)
        label_indexes = StringIndexer(inputCol = self.target , outputCol = 'label', handleInvalid = 'keep')
        assembler = VectorAssembler(inputCols = num_var , outputCol = "features")
        if self.problem_type == 'REGRESSION':
            model = RandomForestRegressor(labelCol="label", \
                                     featuresCol="features", seed = 8464,\
                                     numTrees=10, cacheNodeIds = True,\
                                     subsamplingRate = 0.7)
        else:
            model = RandomForestClassifier(labelCol="label", \
                                     featuresCol="features", seed = 8464,\
                                     numTrees=10, cacheNodeIds = True,\
                                     subsamplingRate = 0.7,maxBins = max_count+2)
        pipe = Pipeline(stages =[assembler, label_indexes, model])

        mod_fit = pipe.fit(self.data_frame)
        df2 = mod_fit.transform(self.data_frame)
        cols = MLUtils.ExtractFeatureImp(mod_fit.stages[-1].featureImportances, df2, "features")
        cols_considered = cols.loc[cols['score'] > 0]
        cols_considered = list(cols_considered['name'])
        #tree_fs = list(set(cols_considered) & set(self.data_frame.columns))
        #tree_fs.extend(list(set([encoded for encoded in one_hot for column in cols_considered if column.startswith(encoded)])))
        self.data_change_dict['SelectedColsTree'] = cols_considered
        if self.target not in cols_considered:
            cols_considered.append(self.target)
        return cols_considered

    def feat_importance_tree(self):
        if self.problem_type  =='REGRESSION':
            model = ExtraTreesRegressor()
        else:
            model = ExtraTreesClassifier()
        X_train = self.data_frame.drop(self.target, axis=1)
        X_train = X_train[X_train._get_numeric_data().columns]
        Y_train = self.data_frame[self.target]
        # print (list(training_set))
        model.fit(X_train, Y_train)
        feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
        number_of_cols_to_consider = int(len(X_train.columns)*0.7)
        # print (feat_importances.nlargest(number_of_cols_to_consider))
        cols_considered = []
        for i, v in feat_importances.items():
            if v > 0:
                if i not in cols_considered:
                    cols_considered.append(i)
        self.data_change_dict['SelectedColsTree'] = cols_considered
        cols_considered.append(self.target)
        return cols_considered

    def feat_importance_linear(self):
        linear_list=[]
        if self._pandas_flag:
            le=LabelEncoder()
            X_train = self.data_frame.drop(self.target, axis=1)
            if self.problem_type !='REGRESSION':
                try:
                    Y_train=le.fit_transform(self.data_frame[self.target])
                except:
                    Y_train = le.fit_transform(self.data_frame[self.target].astype(str))
            else:
                Y_train = self.data_frame[self.target]
            X_train = X_train[X_train._get_numeric_data().columns]

            for c in list(X_train.columns):
                pearson_coef, p_value = stats.pearsonr(X_train[c],Y_train)
                if p_value < 0.05 :
                    linear_list.append(c)
        else:
            if self.problem_type !='REGRESSION':
                indexer = StringIndexer(inputCol=self.target, outputCol="label")
                indexed = indexer.fit(self.data_frame).transform(self.data_frame)
                X_train = indexed.drop('label')
                num_var = [i[0] for i in X_train.dtypes if ((i[1]=='int') | (i[1]=='double'))]
                num_of_samples = indexed.select(num_var[0]).count()
                for column_one in num_var:
                    corr = indexed.corr(column_one, 'label')
                    # num_of_samples = indexed.select(column_one).count()
                    df = num_of_samples - 2
                    std_error = math.sqrt(old_div((1 - math.pow(corr, 2)), df))
                    t_value = old_div(corr, std_error)
                    p_value = Stats.t_distribution_critical_value(t_value, df=df)
                    if p_value < 0.05 :
                        linear_list.append(column_one)
            else:
                X_train = self.data_frame.drop(self.target)
                num_var = [i[0] for i in X_train.dtypes if ((i[1]=='int') | (i[1]=='double'))]
                for column_one in num_var:
                    corr = self.data_frame.corr(column_one, self.target)
                    num_of_samples = self.data_frame.select(column_one).count()
                    df = num_of_samples - 2
                    std_error = math.sqrt(old_div((1 - math.pow(corr, 2)), df))
                    t_value = old_div(corr, std_error)
                    p_value = Stats.t_distribution_critical_value(t_value, df=df)
                    if p_value < 0.05 :
                        linear_list.append(column_one)
        self.data_change_dict['SelectedColsLinear'] = linear_list
        linear_list.append(self.target)
        return linear_list
