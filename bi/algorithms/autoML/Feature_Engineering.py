import numpy as np
import pandas as pd
# import featuretools as ft
# import featuretools.variable_types as vtypes
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import random
import gc
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import sklearn
from sklearn.preprocessing import PolynomialFeatures, PowerTransformer
import scipy.stats as ss
import time

# from itertools import combinations
import warnings

warnings.filterwarnings('ignore')
# import holidays


# import statsmodels.api as sm
# from   statsmodels.formula.api import ols
# from statsmodels.api import add_constant
# from   statsmodels.stats.anova import anova_lm
# import scipy.stats as stats
# import pickle
# from datetime import date
# import datetime as dt
# import holidays

from pandas.api.types import is_datetime64_any_dtype as is_datetime


class FeatureEngineeringAutoMl:

    def __init__(self, Dataframe, data_dict):

        self.data_dict2 = data_dict
        self.Dataframe = Dataframe
        self.norm_col = ''
        self.target = ''
        self.date_time_columns = pd.DataFrame()
        self.combained_df = pd.DataFrame()  # combined data
        self.original_df = pd.DataFrame()  # original data
        self.only_created_df = pd.DataFrame()  # fe created data
        self.columns_list = []
        self.one_click = {'created_feature': [],
                          #                         'original_cols':[],
                          'splitted_columns': [],
                          'created_ud_date_column': [],
                          'normalize_column': [],
                          'train_final_cols': [],
                          'removed_null_cols': [],
                          'removed_unique_cols': [],
                          #                         'log1p':[],
                          #                         'exp':[],
                          #                         'minmax':[],
                          #                         'standard_scalar':[],
                          #                         'new_scaled_colums':[],
                          #                         'new_transformed_columns':[],
                          'removed_duplicate_columns': [],
                          'removed_constant_columns': []
                          }

    def set_dataframe(self, data):
        """set dataframe"""

        self.Dataframe = data

    def set_target(self, target):
        """set target info"""
        self.target = target

    ##Split columns containing seperator
    # need data_dict from prevoius module
    def split_columns(self):
        """Splitting columns having seperator"""
        data_dict = self.data_dict2
        created_split_columns = []
        data = self.Dataframe

        """Moved below code to data preprocessing as we want to capture only original columns and not others that were created during feature engineering
#         orginal_columns=data.columns.to_list()
#         self.one_click['original_cols'] = orginal_columns
#         print("Original Columns:  ",orginal_columns)
"""

        for idx in range(0, len(data_dict['Column_settings'])):
            if data_dict['Column_settings'][idx]['SepSymbols']['value']:
                col = data_dict['Column_settings'][idx]['re_column_name']
                sep = data_dict['Column_settings'][idx]['SepSymbols']['Symbol']
                new_col_first = col + "_first"
                new_col_second = col + "_second"
                data[new_col_first] = None
                data[new_col_second] = None

                ## why two loops if it can be done in one TO:DO
                for idx in data.index.to_list():
                    if sep != '':
                        data.loc[idx, [new_col_first]] = data[col].str.strip().str.split(sep, n=1)[idx][0]
                    else:
                        data.loc[idx, [new_col_first]] = data[col].str.strip().str.split()[idx][0]
                try:
                    for idx in data.index.to_list():
                        if sep != '':
                            data.loc[idx, [new_col_second]] = data[col].str.strip().str.split(sep, n=1)[idx][1]
                        else:
                            data.loc[idx, [new_col_second]] = data[col].str.strip().str.split()[idx][1]
                except:
                    for idx in data.index.to_list():
                        temp = list(data.loc[idx, [col]].str.strip().str.split('_', n=1))[0]
                        if len(temp) == 2:
                            data.loc[idx, [new_col_second]] = temp[1]
                        else:
                            data.loc[idx, [new_col_second]] = list(data.loc[idx, [new_col_first]].str.strip() + '_ab')[
                                0]

                created_split_columns.append(new_col_first)
                created_split_columns.append(new_col_second)
        self.set_dataframe(data)

        created_split_columns = [{'name': x, 'dtype': str(data[x].dtype), 'splitted': True, 'created': True} for x in
                                 created_split_columns]
        self.one_click['splitted_columns'] = created_split_columns

        self.one_click['created_feature'].extend(created_split_columns)

        return data

    ##adding new date column features

    def date_column_split(self):
        """Splitting date column"""
        data = self.Dataframe
        data = data.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)

        orginal_columns = data.columns.to_list()

        date_time_columns = data.select_dtypes(include=['datetime'])
        self.date_time_columns = date_time_columns
        for col_name in self.date_time_columns.columns:
            column = str(col_name)
            data[column + '_day'] = data[column].dt.day
            data[column + '_month'] = data[column].dt.month
            data[column + '_year'] = data[column].dt.year
            data[column + '_quarter'] = data[column].dt.quarter
            data[column + '_semester'] = np.where(data[column + '_quarter'].isin([1, 2]), 1, 2)
            data[column + '_day_of_the_week'] = data[column].dt.dayofweek
            data[column + '_time'] = data[column].dt.time
            data[column + '_day_of_the_year'] = data[column].dt.dayofyear
            data[column + '_week_of_the_year'] = data[column].dt.weekofyear

        new_cols = list(set(data.columns.to_list()) - set(orginal_columns))
        date_extracted_cols = [{'name': x, 'dtype': str(data[x].dtype), 'created': True} for x in new_cols]
        self.one_click['created_ud_date_column'] = date_extracted_cols
        self.one_click['created_feature'].extend(date_extracted_cols)
        self.set_dataframe(data)
        return data

    # def select_norm_col(self,target):
    #
    #     """Selecting column for normalize the data"""
    #
    #     df= self.Dataframe
    #
    #     shape =df.shape
    #     df = df.apply(lambda col: pd.to_datetime(col, errors='ignore')
    #           if col.dtypes == object
    #           else col,
    #           axis=0)###finding datetime column and change dtype
    #     df_train =df.drop(target,axis=1)
    #     y_train=df[target]
    #     self.set_target(target)
    #     asso_dic,corrltd={},{}
    #     norm_num_col,norm_cat_col='',''
    #     cat_list = df_train.select_dtypes(include='object').columns.to_list()
    #     num_list = df_train.select_dtypes(exclude=['object','datetime']).columns.to_list()
    #     date_time_columns= df_train.select_dtypes(include=['datetime'])
    #     self.date_time_columns=date_time_columns
    #     if y_train.dtype =='object':
    #         for cols in df_train.select_dtypes(include='object').columns:
    #             crosstab = pd.crosstab(df_train[cols], y_train)
    #             chi_sq_Stat, p_value, deg_freedom, exp_freq = stats.chi2_contingency(crosstab)
    #             if(p_value <= 0.05):
    #                 chi2 = stats.chi2_contingency(crosstab)[0]
    #                 n = crosstab.sum().sum()
    #                 phi2 = chi2/n
    #                 r,k = crosstab.shape
    #                 phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    #                 rcorr = r-((r-1)**2)/(n-1)
    #                 kcorr = k-((k-1)**2)/(n-1)
    #                 association = np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
    #                 asso_dic[association]= cols
    #     else:
    #         for  col in num_list:
    #             val,pval = stats.pearsonr(df_train[col],y_train)
    #             if abs(val)>0.5:
    #                 corrltd[val]=col
    #     if len(asso_dic)>0:
    #         norm_cat_col = asso_dic[max(asso_dic)]
    #     else:
    #         if len(cat_list)>0:
    #             norm_cat_col =random.choice(cat_list)
    #     if len(corrltd)  >0:
    #         norm_num_col = corrltd[max(corrltd)]
    #     else:
    #         if len(num_list)>0:
    #             norm_num_col =random.choice(num_list)
    #     if len(norm_num_col)>0:
    #         pass
    #     norm_col = [col for col in [norm_cat_col,norm_num_col] if len(col)>0]
    #     self.norm_col =random.choice(norm_col)
    #     self.one_click['normalize_column'] =self.norm_col
    #     self.one_click['y_train'] =y_train
    #     self.set_dataframe(df_train)
    #     return df_train,self.norm_col

    def feature_transformation(self, data, target, col_list):
        data_dict = {}
        pt_list = []
        lt_list = []
        bin_list = []
        dec_list = []
        # pt = PowerTransformer()
        # temp=np.array(np.zeros(len(data)))
        # temp=temp.reshape(1,-1)
        # pt.fit(temp)
        # print("time taken for fitting",end-start)
        for i in col_list:
            if (str(data[i].dtype).startswith('int')) | (str(data[i].dtype).startswith('float')):
                if (data[i].std() > data[i].mean() / 2) & (data[i].nunique() > 20):
                    print(i, data[i].nunique(), data[i].nunique() / data[i].count())
                    start = time.time()
                    # temp=np.array(data[i])
                    # temp=temp.reshape(1,-1)
                    # if  any(data[i]<=0):
                    #     data[i+'_pt']=self.power_transform(data[i],pt,temp)
                    #     pt_list.append(i)
                    #     self.one_click['power_transform']=pt_list
                    #     self.one_click['created_feature'].append({'name':i+'_pt','dtype':str(data[i].dtype),'created':True})
                    # else:
                    data[i + '_lt'] = data[i].apply(lambda x: np.log(x) if x > 0 else np.log(x + abs(min(data[i]) + 1)))
                    end = time.time()
                    print(i + '_lt', end - start)
                    lt_list.append(i)
                    self.one_click['log_transform'] = lt_list
                    self.one_click['created_feature'].append(
                        {'name': i + '_lt', 'dtype': str(data[i].dtype), 'created': True})


                elif data[i].nunique() > 0.5 * data[i].count():
                    print(i + '_bins')
                    start = time.time()
                    data[i + '_bins'] = self.bin_columns(data[i])
                    end = time.time()
                    print(i + '_bins', end - start)
                    bin_list.append(i)
                    self.one_click['created_feature'].append(
                        {'name': i + '_bins', 'dtype': str(data[i].dtype), 'created': True})
                    self.one_click['bin_columns'] = bin_list

            else:
                if data[i].nunique() > 0.1 * data[i].count():
                    print(i + '_decomposed')
                    a = time.time()
                    data[i + '_decomposed'] = self.categorical_decomposition(data[i])
                    print(i + '_decomposed', time.time() - a)
                    self.one_click['created_feature'].append(
                        {'name': i + '_decomposed', 'dtype': str(data[i].dtype), 'created': True})
                    dec_list.append(i)
                    self.one_click['categorical_decomposition'] = dec_list

        return data

    def power_transform(self, data, pt, temp):
        try:
            new_list = pt.transform(np.float32(temp))
            data = new_list[0]
        except:
            new_list = pt.transform(np.float64(temp))
            data = new_list[0]
        return data

    def bin_columns(self, data):
        max_val = round(data.max(), 2)
        min_val = round(data.min(), 2)
        print(min_val, max_val)
        mean_val = round(data.mean(), 2)
        std_val = round(data.std(), 2)
        data = pd.cut(data, bins=[min_val, mean_val, mean_val + std_val, max_val],
                      labels=["[{}-{}]".format(min_val, round(mean_val, 2)),
                              "[{}-{}]".format(round(mean_val, 2), round(mean_val + std_val)),
                              "[{}-{}]".format(round(mean_val + std_val), max_val)], right=True, include_lowest=True)
        return data

    def bin_columns_for_crammers(self, data):
        max_val = data.max()
        min_val = data.min()
        mean_val = data.mean()
        std_val = round(data.std(), 2)
        data = pd.cut(data, bins=[min_val, mean_val, max_val], labels=["[{}-{}]".format(min_val, round(mean_val, 2)),
                                                                       "[{}-{}]".format(round(mean_val, 2), max_val)],
                      right=True, include_lowest=True, duplicates='drop')
        return data

    def categorical_decomposition(self, data):
        val_count_dict = dict(data.value_counts() / data.count())
        for key in val_count_dict:
            if val_count_dict[key] == min(val_count_dict.values()):
                data = data.replace(to_replace=key, value="Others")
        return data

    # def feature_combiner_classification(self,data,target,col_list):
    #     """The following function multiples 2 columns based on the correlation between one another and the target """
    #
    #     data_dict={'added':[],'multiplied_encoded_both':[],'multiplied_series_both':[],'multiplied_encoded1_series2':[],'multiplied_encoded2_series1':[]}
    #     self.one_click['feature_combiner_classification']={}
    #     name ='_and_'
    #     le= sklearn.preprocessing.LabelEncoder()
    #     """ This loop removes the columns which have a correlation value more than the specified threshold"""
    #     for i in col_list:
    #         if data[i].dtype==object:
    #             if (self.cramers_corrected_stat(data[i],data[target]) >0.1) :
    #                 col_list.remove(i)
    #         else:
    #             labels1=self.bin_columns_for_crammers(data[i])
    #             if (self.cramers_corrected_stat(labels1,data[target]) >0.1):
    #                  col_list.remove(i)
    #     for i in col_list:
    #         for j in col_list[1:]:
    #             if not j+name+i in list(data.columns):
    #                 if (data[target].dtype==object) | (data[target].nunique()<=3) :
    #                     if ((data[i].dtype==object) )  & ((data[j].dtype==object)):
    #                             """combining columns which are objects """
    #                             if (self.cramers_corrected_stat(data[i],data[j]) <0.5) :
    #                                     combined_list1=[]
    #                                     combined_list1.append(i)
    #                                     combined_list1.append(j)
    #                                     labels1=data[i]
    #                                     labels2=data[j]
    #                                     le.fit(labels1)
    #                                     labels1 = le.transform(labels1)
    #                                     le.fit(labels2)
    #                                     labels2 = le.transform(labels2)
    #                                     data[i+name+j]=labels1*labels2
    #                                     self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                     data_dict['added'].append(combined_list1)
    #                                     self.one_click['feature_combiner_classification']=data_dict
    #
    #                     #"""combining columns where one is categorical and other is numerical.Categorical Columns are label encoded"""
    #                     elif (((str(data[i].dtype).startswith('int'))| (str(data[i].dtype).startswith('float')) & (data[i].nunique()>0.1*data[i].count())) & (data[j].dtype==object)) | ((data[i].dtype==object) & ((str(data[j].dtype).startswith('int'))| (str(data[j].dtype).startswith('float')) & (data[j].nunique()>0.1*data[i].count()))):
    #                                 if data[i].dtype==object:
    #                                          labels1=self.bin_columns_for_crammers(data[j])
    #                                          if (self.cramers_corrected_stat(data[i],labels1) <0.5):
    #                                             combined_list2=[]
    #                                             combined_list2.append(i)
    #                                             combined_list2.append(j)
    #                                             labels2=data[i]
    #                                             try:
    #                                                 le.fit(labels1)
    #                                                 labels1 = le.transform(labels1)
    #                                             except:
    #                                                 labels1 = labels1
    #                                             try:
    #                                                 le.fit(labels2)
    #                                                 labels2 = le.transform(labels2)
    #                                             except:
    #                                                 labels2=labels2
    #                                             try:
    #                                                 try:
    #                                                         data[i+name+j]=labels1*labels2
    #                                                         data_dict['multiplied_encoded_both'].append(combined_list2)
    #                                                         self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                         self.columns_list.append(combined_list2)
    #                                                         self.one_click['feature_combiner_classification']=data_dict
    #                                                 except:
    #                                                         data[i+name+j]=data[i]*data[j]
    #                                                         data_dict['multiplied_series_both'].append(combined_list2)
    #                                                         self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                         self.columns_list.append(combined_list2)
    #                                                         self.one_click['feature_combiner_classification']=data_dict
    #                                             except:
    #                                                 try:
    #                                                         data[i+name+j]=data[j]*labels2
    #                                                         data_dict['multiplied_encoded1_series2'].append(combined_list2)
    #                                                         self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                         self.columns_list.append(combined_list2)
    #                                                         self.one_click['feature_combiner_classification']=data_dict
    #                                                 except:
    #                                                         data[i+name+j]=labels1*data[i]
    #                                                         data_dict['multiplied_encoded2_series1'].append(combined_list2)
    #                                                         self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                         self.columns_list.append(combined_list2)
    #                                                         self.one_click['feature_combiner_classification']=data_dict
    #                                 elif data[j].dtype==object:
    #                                          labels1=self.bin_columns_for_crammers(data[i])
    #                                          if (self.cramers_corrected_stat(data[j],labels1) <0.5):
    #                                                 combined_list3=[]
    #                                                 combined_list3.append(i)
    #                                                 combined_list3.append(j)
    #                                                 labels2=data[j]
    #                                                 try:
    #                                                     le.fit(labels1)
    #                                                     labels1 = le.transform(labels1)
    #                                                 except:
    #                                                     labels1=labels1
    #                                                 try:
    #                                                     le.fit(labels2)
    #                                                     labels2 = le.transform(labels2)
    #                                                 except:
    #                                                     labels2 = labels2
    #                                                 try:
    #                                                     try:
    #                                                             data[i+name+j]=data[i]*labels2
    #                                                             data_dict['multiplied_encoded2_series1'].append(combined_list3)
    #                                                             self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                             self.columns_list.append(combined_list3)
    #                                                             self.one_click['feature_combiner_classification']=data_dict
    #                                                     except:
    #                                                              data[i+name+j]=labels1*data[j]
    #                                                              data_dict['multiplied_encoded1_series2'].append(combined_list3)
    #                                                              self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                              self.columns_list.append(combined_list3)
    #                                                              self.one_click['feature_combiner_classification']=data_dict
    #                                                 except:
    #                                                     try:
    #                                                             data[i+name+j]=labels1*labels2
    #                                                             data_dict['multiplied_encoded_both'].append(combined_list3)
    #                                                             self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                             self.columns_list.append(combined_list3)
    #                                                             self.one_click['feature_combiner_classification']=data_dict
    #                                                     except:
    #                                                             data[i+name+j]=data[i]*data[j]
    #                                                             data_dict['multiplied_series_both'].append(combined_list3)
    #                                                             self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                                             self.columns_list.append(combined_list3)
    #                                                             self.one_click['feature_combiner_classification']=data_dict
    #
    #
    #                 #"""combining columns where both are measures"""
    #                 elif (str(data[i].dtype).startswith(int))|(str(data[i].dtype).startswith(float)) & (str(data[j].dtype).startswith(int))|(str(data[j].dtype).startswith(float)):
    #                             if (data[i].nunique()>0.01*len(data[i])) & (data[j].nunique()>0.01*len(data[j])):
    #                                 if (-0.5<(data[i].corr(data[j]))<0.5) :
    #                                     combined_list4=[]
    #                                     combined_list4.append(i)
    #                                     combined_list4.append(j)
    #                                     column=data[i]*data[j]
    #                                     self.one_click['created_feature'].append({'name':i+name+j,'dtype':str(data[i+name+j].dtype),'created':True})
    #                                     data_dict['multiplied_series_both'].append(combined_list4)
    #                                     #columns_list.append(combined_list4)
    #                                     self.one_click['feature_combiner_classification']=data_dict
    #     return data

    # def feature_combiner_regression(self,data,target,col_list):
    #     for i in col_list:
    #         for j in col_list[1:]:
    #             if (data[target].dtype!=object) | (data[target].nunique()>=3) :
    #                 if ((data[i].dtype==object) | (data[i].nunique()<=5))  & ((data[j].dtype==object)|(data[j].nunique()<=5)):
    #                     if not j+i in list(data.columns):
    #                         if (self.cramers_corrected_stat(data[i],data[j]) <0.5) & (self.cramers_corrected_stat(data[i],data[target]) <0.5) & (self.cramers_corrected_stat(data[j],data[target]) <0.5):
    #                             combined_list1=[]
    #                             combined_list1.append(i)
    #                             combined_list1.append(j)
    #                             labels1=data[i]
    #                             labels2=data[j]
    #                             le= sklearn.preprocessing.LabelEncoder()
    #                             le.fit(labels1)
    #                             labels1 = le.transform(labels1)
    #                             le.fit(labels2)
    #                             labels2 = le.transform(labels2)
    #                             data[i+j]=labels1+labels2
    #                             self.columns_list.append(combined_list1)
    #                             self.one_click['feature_combiner_regression']=self.columns_list
    #                 elif ((str(data[i].dtype).startswith('int'))|(str(data[i].dtype).startswith('float')) & (data[j].dtype==object)) | ((data[i].dtype==object) & ((str(data[j].dtype).startswith('int'))|(str(data[j].dtype).startswith('float')))):
    #                         if not j+i in list(data.columns):
    #                             if data[i].dtype==object:
    #                                      labels1=self.bin_columns_for_crammers(data[j])
    #                                      if (self.cramers_corrected_stat(data[i],labels1) <0.5) & (self.cramers_corrected_stat(data[i],data[target]) <0.5) & (self.cramers_corrected_stat(labels1,data[target]) <0.5):
    #                                             combined_list2=[]
    #                                             combined_list2.append(i)
    #                                             combined_list2.append(j)
    #                                             labels2=data[i]
    #                                             le= sklearn.preprocessing.LabelEncoder()
    #                                             try:
    #                                                 le.fit(labels1)
    #                                                 labels1 = le.transform(labels1)
    #                                             except:
    #                                                 labels1 = labels1
    #                                             try:
    #                                                 le.fit(labels2)
    #                                                 labels2 = le.transform(labels2)
    #                                             except:
    #                                                 labels2=labels2
    #                                             try:
    #                                                 data[i+j]=labels1*labels2
    #                                             except:
    #                                                 try:
    #                                                      data[i+j]=data[j]*labels2
    #                                                 except:
    #                                                      data[i+j]=labels1*data[i]
    #                                             self.columns_list.append(combined_list2)
    #                                             self.one_click['feature_combiner_regression']=self.columns_list
    #                             elif data[j].dtype==object:
    #                                      labels1=self.bin_columns_for_crammers(data[i])
    #                                      if (self.cramers_corrected_stat(data[j],labels1) <0.5) & (self.cramers_corrected_stat(data[j],data[target]) <0.5) & (self.cramers_corrected_stat(labels1,data[target]) <0.5):
    #                                             combined_list3=[]
    #                                             combined_list3.append(i)
    #                                             combined_list3.append(j)
    #                                             labels2=data[j]
    #                                             le= sklearn.preprocessing.LabelEncoder()
    #                                             try:
    #                                                 le.fit(labels1)
    #                                                 labels1 = le.transform(labels1)
    #                                             except:
    #                                                 labels1=labels1
    #                                             try:
    #                                                 le.fit(labels2)
    #                                                 labels2 = le.transform(labels2)
    #                                             except:
    #                                                 labels2 = labels2
    #                                             try:
    #                                                 data[i+j]=labels1*labels2
    #                                             except:
    #                                                 try:
    #                                                      data[i+j]=labels1*data[j]
    #                                                 except:
    #                                                      data[i+j]=data[i]*labels2
    #                                             self.columns_list.append(combined_list3)
    #                                             self.one_click['feature_combiner_regression']=self.columns_list
    #                 else:
    #                     if not j+i in list(data.columns):
    #                         if (-0.5<(data[i].corr(data[j]))<0.5) & (-0.5<(data[i].corr(data[target]))<0.5) & (-0.5<(data[j].corr(data[target]))<0.5):
    #                                 combined_list4=[]
    #                                 combined_list4.append(i)
    #                                 combined_list4.append(j)
    #                                 data[i+j]=data[i]*data[j]
    #                                 self.columns_list.append(combined_list4)
    #     return data

    # def feature_combiner_classification_score(self,data,data_dict):
    #     le= sklearn.preprocessing.LabelEncoder()
    #     name='_and_'
    #     if 'multiplied_encoded_both' in data_dict['feature_combiner_classification'].keys():
    #         if len(data_dict['feature_combiner_classification']['multiplied_encoded_both'])>0:
    #             for vals in data_dict['feature_combiner_classification']['multiplied_encoded_both']:
    #                 labels1=data[vals[0]]
    #                 le.fit(labels1)
    #                 labels1=le.transform(labels1)
    #                 labels2=data[vals[1]]
    #                 le.fit(labels2)
    #                 labels2=le.transform(labels2)
    #                 data[vals[0]+name+vals[1]]=labels1*labels2
    #     if 'multiplied_encoded1_series2' in data_dict['feature_combiner_classification'].keys():
    #         if len(data_dict['feature_combiner_classification']['multiplied_encoded1_series2'])>0:
    #             for vals in data_dict['feature_combiner_classification']['multiplied_encoded1_series2']:
    #                 labels1=data[vals[0]]
    #                 le.fit(labels1)
    #                 labels1=le.transform(labels1)
    #                 data[vals[0]+name+vals[1]]=labels1*data[vals[1]]
    #     if 'multiplied_encoded2_series1' in data_dict['feature_combiner_classification'].keys():
    #         if len(data_dict['feature_combiner_classification']['multiplied_encoded2_series1'])>0:
    #             for vals in data_dict['feature_combiner_classification']['multiplied_encoded2_series1']:
    #                 labels1=data[vals[1]]
    #                 le.fit(labels1)
    #                 labels1=le.transform(labels1)
    #                 data[vals[0]+name+vals[1]]=labels1*data[vals[0]]
    #     if 'multiplied_series_both' in data_dict['feature_combiner_classification'].keys():
    #         if len(data_dict['feature_combiner_classification']['multiplied_series_both'])>0:
    #             for vals in data_dict['feature_combiner_classification']['multiplied_series_both']:
    #                 data[vals[0]+name+vals[1]]=data[vals[0]]*data[vals[1]]
    #     if 'added' in data_dict['feature_combiner_classification'].keys():
    #         if len(data_dict['feature_combiner_classification']['added'])>0:
    #             for vals in data_dict['feature_combiner_classification']['added']:
    #                 labels1=data[vals[0]]
    #                 labels2=data[vals[1]]
    #                 le.fit(labels1)
    #                 labels1=le.transform(labels1)
    #                 le.fit(labels2)
    #                 labels2=le.transform(labels2)
    #                 data[vals[0]+name+vals[1]]=labels1+labels2
    #     return data

    def feature_transformation_score(self, data, data_dict):
        if 'log_transform' in data_dict.keys():
            for i in data_dict['log_transform']:
                data[i + '_lt'] = data[i].apply(lambda x: np.log(x) if x > 0 else np.log(x + abs(min(data[i]) + 1)))
        if 'power_transform' in data_dict.keys():
            for i in data_dict['power_transform']:
                data[i + '_pt'] = self.power_transform(data[i])
        if 'bin_columns' in data_dict.keys():
            for i in data_dict['bin_columns']:
                data[i + '_bins'] = self.bin_columns(data[i])
        if 'categorical_decomposition' in data_dict.keys():
            for i in data_dict['categorical_decomposition']:
                data[i + '_decomposed'] = self.categorical_decomposition(data[i])
        return data

    # def cramers_corrected_stat(self,x,y):
    #
    #     """ calculate Cramers V statistic for categorial-categorial association.
    #         uses correction from Bergsma and Wicher,
    #         Journal of the Korean Statistical Society 42 (2013): 323-328
    #     """
    #     result=-1
    #     if len(x.value_counts())==1 :
    #         print("First variable is constant")
    #     elif len(y.value_counts())==1:
    #         print("Second variable is constant")
    #     else:
    #         conf_matrix=pd.crosstab(x, y)
    #
    #         if conf_matrix.shape[0]==2:
    #             correct=False
    #         else:
    #             correct=True
    #
    #         chi2 = ss.chi2_contingency(conf_matrix, correction=correct)[0]
    #
    #         n = sum(conf_matrix.sum())
    #         phi2 = chi2/n
    #         r,k = conf_matrix.shape
    #         phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    #         rcorr = r - ((r-1)**2)/(n-1)
    #         kcorr = k - ((k-1)**2)/(n-1)
    #         result=np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))
    #     return round(result,6)

    # def feature_creation(self,norm_col):
    #
    #     """Feature creation
    #
    #     return
    #
    #     ------
    #     dataframe
    #
    #
    #     """
    #
    #     es = ft.EntitySet(id = 'Entity_Set_Id')
    #     self.Dataframe['Unique_Id']=self.Dataframe.index
    #      # adding a dataframe
    #     es.entity_from_dataframe(entity_id = 'Entity_Df_Id', dataframe = self.Dataframe,index='Unique_Id')
    #     # to establish the relation between the dataframes
    #     es = es.normalize_entity(base_entity_id='Entity_Df_Id', new_entity_id='New_Entity_Df_Id', index=norm_col)
    #     feature_matrix, feature_names = ft.dfs(entityset=es,
    #                                            target_entity = 'Entity_Df_Id',
    #                                            max_depth = 2,
    #                                            n_jobs = -1)
    #     orginal_col = self.Dataframe.columns.to_list()
    #
    #     feature_tool_variables=list(set(feature_matrix.columns)-(set(self.Dataframe.columns)))
    #     created_list =[{'name':x,'dtype':str(feature_matrix[x].dtype),'created':True} for x in feature_tool_variables ]
    #     self.one_click['created_feature'].extend(created_list)
    #
    #     if len(self.date_time_columns)>0:
    #         feature_matrix[self.date_time_columns.columns]=self.date_time_columns
    #     self.set_dataframe(feature_matrix)
    #     return feature_matrix

    def remove_null_density(self, data):

        """Removing columns containing more than 50% null values

        Returns
        ------

        Dataframe

        """
        orginal_cols = data.columns.to_list()
        cols_to_keep = data.columns[data.isnull().mean() < 0.5].to_list()  # removing columns with many null values
        cols_to_keep = list(set(cols_to_keep + self.data_dict2['original_cols']))
        print("self.data_dict2['original_cols']  ", self.data_dict2['original_cols'])
        cols_to_keep.remove(self.target)
        removed_cols = list(set(orginal_cols) - set(cols_to_keep))
        removed_cols = [{'name': x, 'dtype': str(data[x].dtype), 'removed': True} for x in removed_cols]
        data = data[cols_to_keep]
        self.one_click['removed_null_cols'] = removed_cols
        return data

    def remove_unique_values(self, data):

        """Removing columns with high cardinality

        Returns
        ------

        Dataframe


        """
        orginal_cols = data.columns.to_list()
        cols_to_keep = data.iloc[:, (data.nunique() / len(data) < .9).values].columns.to_list()
        cols_to_keep = list(set(cols_to_keep + self.data_dict2['original_cols']))
        print("self.data_dict2['original_cols']  ", self.data_dict2['original_cols'])
        cols_to_keep.remove(self.target)
        clean_data = data[cols_to_keep]
        removed_cols = list(set(orginal_cols) - set(cols_to_keep))
        removed_cols = [{'name': x, 'dtype': str(data[x].dtype), 'removed': True} for x in removed_cols]
        self.one_click['removed_unique_cols'] = removed_cols
        return clean_data

    def remove_single_value(self, data):
        """removing columns containing only single value"

        return
        -------
        data frame.

        """
        single_col = []
        for cols in data:
            if data[cols].nunique() == 1:
                single_col.append(cols)
        constant_column = [{'name': x, 'dtype': str(data[x].dtype), 'drop_column': True} for x in single_col]
        self.one_click['removed_constant_columns'] = constant_column
        df = data.drop(single_col, axis=1)
        return df

    def remove_duplicate(self, data):

        """Removing duplicate features

        return
        -------
        data frame.


        """
        null_columns = data.columns[data.isnull().any()]
        data[null_columns].isnull().sum()
        duplicate_columns = 0
        dup_list = []
        data.dropna(axis=1, inplace=True)
        for x in range(data.shape[1]):
            col = data.iloc[:, x]
            for y in range(x + 1, data.shape[1]):
                other_col = data.iloc[:, y]
                try:
                    test_col = (other_col == col)
                    if all(x == True for x in test_col):  # col.equals(other_col):
                        dup_list.append(other_col.name)
                        duplicate_columns += 1
                except:
                    print("Errored! ", type(other_col), "hgh", type(col), "hhhhhhhhhhhhhhhhhhhhhhhhhh", other_col.name,
                          col.name)

        duplicate_column = [{'name': x, 'dtype': str(data[x].dtype), 'drop_column': True} for x in dup_list]
        self.one_click['removed_duplicate_columns'] = duplicate_column
        data.drop(dup_list, axis=1, inplace=True)
        return data

    # def transformations(self,data):
    #
    #     """ Transformation
    #
    #        return
    #     ------
    #     data frame.
    #
    #     """
    #
    #     logp_col =[]
    #     exp_col=[]
    #     skewness=dict(data.skew(axis=0,skipna=True))
    #     for k,v in skewness.items():
    #         if v>1:
    #
    #             data[k+'_logp']=(np.log1p(data[k]-min(data[k])))
    #             if data[k+'_logp'].median() in [np.inf, -np.inf]:
    #                 replace_value=np.nan
    #             else:
    #                 replace_value =data[k+'_logp'].median()
    #             data[k+'_logp']=data[k+'_logp'].replace([np.inf, -np.inf],replace_value)
    #             logp_col.append(k)
    #         elif v<-1:
    #             data[k+'_exp']=np.log1p(np.exp(data[k]))
    #             if data[k+'_exp'].median() in [np.inf, -np.inf]:
    #                 replace_value=np.nan
    #             else:
    #                 replace_value=data[k+'_exp'].median()
    #             data[k+'_exp']=data[k+'_exp'].replace([np.inf, -np.inf,np.nan],replace_value)
    #             exp_col.append(k)
    #     after_logp_col=[col for col in data.columns if col.endswith('logp')==True]
    #     after_exp_col=[col for col in data.columns if col.endswith('exp')==True]
    #     all_transformed= after_logp_col+after_exp_col
    #     transformed_list =[{'name':x,'dtype':str(data[x].dtype),'created':True,'transformed':True} for x in all_transformed ]
    #     self.one_click['new_transformed_columns']=transformed_list
    #     self.one_click['exp']=exp_col
    #     self.one_click['log1p']=logp_col
    #
    #     return data

    def scaling(self, data):

        """Scaling data

        Return

        -------

        Dataframe

        """

        min_max = []
        std_scalar = []
        for col in data.select_dtypes(exclude='object').columns:
            if (data[[col]].kurt() < 2).any():
                normalize = MinMaxScaler()
                data[col + '_minmax'] = normalize.fit_transform(data[[col]])
                min_max.append(col)
            else:
                sc = StandardScaler()
                data[col + '_std_scaled'] = sc.fit_transform(data[[col]])
                std_scalar.append(col)
        self.one_click['minmax'] = min_max
        self.one_click['standard_scalar'] = std_scalar

        after_mimmax_col = [col for col in data.columns if col.endswith('minmax') == True]
        after_stdscaled_col = [col for col in data.columns if col.endswith('std_scaled') == True]
        all_scaled = after_mimmax_col + after_stdscaled_col
        scaled_list = [{'name': x, 'dtype': str(data[x].dtype), 'created': True, 'scaled': True} for x in all_scaled]
        self.one_click['new_scaled_colums'] = scaled_list

        return data

    def fe_main(self):

        """Feature creation for train data flow """
        # self.target = self.data_dict2["target_analysis"]['target_analysis']['target']
        self.target = self.data_dict2['target']

        cols_to_keep = self.Dataframe.iloc[:,
                       (self.Dataframe.nunique() / len(self.Dataframe) < .9).values].columns.to_list()

        cols_to_keep=[cols for cols in cols_to_keep if not is_datetime(self.Dataframe[cols])]
        try:
            cols_to_keep.remove(self.target)
        except:
            pass
        #features = self.feature_creation(self.norm_col)
        import time
        start = time.time()
        data1 = self.feature_transformation(self.Dataframe, self.target, cols_to_keep)
        end = time.time()
        print("Time taken for feature transformation", end - start)
        # if (self.data_dict2["app_type"].lower() == "classification"):
        #        start = time.time()
        #        data2=self.feature_combiner_classification(self.Dataframe,self.target,cols_to_keep)
        #        end = time.time()
        #        print("Time taken for feature combiner classification",end - start)
        # else:
        #        data2=self.feature_combiner_regression(self.Dataframe,self.target,cols_to_keep)
        data1['index'] = data1.index
        # data2['index'] = data2.index
        # self.Dataframe = data1.merge(data2)
        self.Dataframe = data1
        self.Dataframe.drop(['index'], axis=1, inplace=True)
        self.split_columns()

        # self.select_norm_col(self.target)
        self.set_target(self.target)
        self.one_click['y_train'] = self.Dataframe[self.target]
        self.date_column_split()

        features = self.Dataframe

        rem_uniq = self.remove_unique_values(features)
        rem_null_density = self.remove_null_density(rem_uniq)

        clean_df = self.remove_single_value(rem_null_density)  # removing single value
        clean_df = self.remove_duplicate(clean_df)  # removing duplicate
        self.one_click['train_final_cols'] = clean_df.columns.to_list()
        clean_df[self.target] = self.one_click['y_train']
        featue_col_list = [x['name'] for x in self.one_click['created_feature']]

        new_created = [x for x in featue_col_list if x in self.one_click['train_final_cols']]

        original_cols = self.data_dict2['original_cols']

        original_cols = [x for x in original_cols if x in self.one_click['train_final_cols']]

        only_created_df = clean_df[new_created + [self.target]]

        original_df = clean_df[original_cols]
        original_df[self.target] = self.one_click['y_train']

        del self.one_click['y_train']
        self.combained_df = clean_df
        self.original_df = original_df
        self.only_created_df = only_created_df

        self.data_dict2.update(self.one_click)

    # def test_transformations(self,data,log_col=[],exp_col=[]):
    #
    #     """Test data transformation"""
    #
    #     for cols in log_col:
    #         data[cols+'_logp']=(np.log1p(data[cols]-min(data[cols])))
    #         if data[cols+'_logp'].median() in [np.inf, -np.inf]:
    #                 replace_value=np.nan
    #         else:
    #             replace_value =data[cols+'_logp'].median()
    #         data[cols+'_logp']=data[cols+'_logp'].replace([np.inf, -np.inf,np.nan],replace_value)
    #     for cols in exp_col:
    #             data[cols+'_exp']=np.log1p(np.exp(data[cols]))
    #             if data[cols+'_exp'].median() in [np.inf, -np.inf]:
    #                 replace_value=np.nan
    #             else:
    #                 replace_value=data[cols+'_exp'].median()
    #             data[cols+'_exp']=data[cols+'_exp'].replace([np.inf, -np.inf,np.nan],replace_value)
    #     return data

    def test_scaling(self, data, minmax, sds):
        """Test data Scaling"""
        for col in minmax:
            normalize = MinMaxScaler()
            data[col + '_minmax'] = normalize.fit_transform(data[[col]])
        for col in sds:
            sc = StandardScaler()
            data[col + '_std_scaled'] = sc.fit_transform(data[[col]])
        return data

    def test_main(self, normal, final_col=[]):
        """test data flow"""
        self.split_columns()
        self.date_column_split()
        cols_to_keep = self.Dataframe.iloc[:,
                       (self.Dataframe.nunique() / len(self.Dataframe) < .9).values].columns.to_list()
        cols_to_keep = [cols for cols in cols_to_keep if not is_datetime(self.Dataframe[cols])]
        print(len(self.Dataframe.columns), "self.Dataframe.columns")
        data1 = self.feature_transformation_score(self.Dataframe, self.data_dict2.copy())
        print(len(data1.columns), "length after transformation columns")
        # if (self.data_dict2["app_type"].lower() == "classification"):
        #        data2=self.feature_combiner_classification_score(self.Dataframe,self.data_dict2.copy())
        #        print(len(data2.columns),"length after combination columns")
        # else:
        #        data2=self.feature_combiner_regression_score(self.Dataframe,self.one_click)

        self.Dataframe = data1

        test_data = self.Dataframe  # [final_col]
        featue_col_list = [x['name'] for x in self.data_dict2['created_feature']]
        new_created = [x for x in featue_col_list if x in final_col]
        original_cols = self.data_dict2['original_cols']
        original_cols = [x for x in original_cols if x in final_col]
        only_created_df = test_data[new_created]

        original_df = test_data[original_cols]

        self.combained_df = test_data
        self.original_df = original_df
        self.only_created_df = only_created_df
