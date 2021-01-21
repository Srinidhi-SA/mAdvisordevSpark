from bi.algorithms.autoML.Feature_Engineering import FeatureEngineeringAutoMl

from bi.algorithms.autoML.ScoringDataPreprocessing import ScorePreprocessing

# from bi.algorithms.autoML_score.Data_Preprocessing import Data_Preprocessing

from bi.algorithms.autoML.Feature_Selection import Utils

import chardet

import pandas as pd

import ast

import re


class Scoring(object):

    def __init__(self, path, data_dict):

        self.path = path

        # self.data_dict = ast.literal_eval(data_dict)
        self.data_dict = data_dict

        # path = self.path
        #
        # obj =  Data_Validation(path,target =self.target,method = self.app_type)
        # obj.run()

    # def find_encoding(self):
    #
    #     ## TO DO : Not be used , check and remove
    #
    #     r_file = open(self.path, 'rb').read()
    #
    #     result = chardet.detect(r_file)
    #
    #     charencode = result['encoding']
    #
    #     return charencode

    # def read_df(self):
    #
    #     na_values = ["NO CLUE","no clue", "No Clue","na","NA","N/A", "n/a","n a","N A", "not available",
    #          "Not Available", "NOT AVAILABLE","?","!","NONE","None","none","null","-"]
    #
    #     df = pd.read_csv(self.path,error_bad_lines=False,
    #                               sep=",",na_values=na_values)
    #     return df

    def validation(self, data, data_dict):

        for idx in range(len(data_dict["Column_settings"])):

            re_column = data_dict["Column_settings"][idx]['re_column_name']

            # column = data_dict["Column_settings"][idx]['column_name']
            try:
                column = data_dict["Column_settings"][idx]['column_name']
            except:
                column = re.sub('\W+', '_', data_dict["Column_settings"][idx]['column_name'])
            # print (column)
            ## TO DO : why all columns are being renamed , check re_name =True then do all this.

            if data_dict['target'] != re_column:

                if not data_dict["Column_settings"][idx]['droped_column']:

                    data.rename(columns={column: re_column}, inplace=True)

                else:

                    data.drop([column], axis=1, inplace=True)

                if data_dict["Column_settings"][idx]['data_type'] == 'datetime64[ns]':
                    data[re_column] = pd.to_datetime(data[re_column],
                                                     infer_datetime_format=True)  # data[re_column].astype['datetime64[ns]']

        return data

    # def null_handling(self,df):
    #
    #     ## TO DO : Not being used , check and remove.
    #
    #     cls=Data_Preprocessing(self.data_dict,df)
    #
    #     measureCol,dim = [],[]
    #
    #     for i in df.columns:
    #
    #         if df[i].dtypes != "object" and df[i].dtypes != "datetime64[ns]":
    #
    #             measureCol.append(i)
    #
    #         else :
    #
    #             dim.append(i)
    #
    #     outlier_columns,capped_cols=cls.handle_outliers(measureCol)
    #
    #     measureColImpu = [i for i in measureCol if cls.dataframe[i].isna().sum()>0 ]
    #
    #     dimColImpu = [i for i in dim if cls.dataframe[i].isna().sum()>0 ]
    #
    #     mean_impute_cols,median_impute_cols = cls.measure_col_imputation(measureColImpu,outlier_columns)
    #
    #     cls.dim_col_imputation(dimColImpu)
    #
    #     return cls.dataframe

    def score_feature_eng(self, df, data_dict):
        fe_obj = FeatureEngineeringAutoMl(df, data_dict)

        if len(data_dict['created_feature']) > 0:

            fe_obj.test_main(data_dict['normalize_column'], data_dict['train_final_cols'])
            return fe_obj.original_df, fe_obj.only_created_df, fe_obj.date_time_columns
        else:
            original_cols = data_dict['original_cols']
            original_cols.remove(data_dict['target'])
            original_df = df[original_cols]
            self.original_df = original_df
            self.only_created_df = None
            date_time_columns_df = pd.DataFrame()
            self.date_time_columns = date_time_columns_df
            return self.original_df, self.only_created_df, self.date_time_columns

    def scoring_feature_selection(self, Dataframe, data_dict):

        print("linear features: ", data_dict['linear_features'])
        print("tree features: ", data_dict['tree_features'])

        linear_dataframe = Dataframe[data_dict['linear_features']]

        tree_dataframe = Dataframe[data_dict['tree_features']]

        utils_obj = Utils()

        """ Label encoding transform"""

        if data_dict['labelencoder']['tree']:
            tree_dataframe = utils_obj.label_en(tree_dataframe, data_dict['labelencoder']['tree'])

        if data_dict['labelencoder']['linear']:
            linear_dataframe = utils_obj.label_en(linear_dataframe, data_dict['labelencoder']['linear'])

        """ Dummy transform"""

        if data_dict['dummy']['tree']:

            for col in data_dict['dummy']['tree']:
                tree_dataframe = utils_obj.one_hot_encoder(tree_dataframe, col)

        if data_dict['dummy']['linear']:

            for col in data_dict['dummy']['linear']:
                linear_dataframe = utils_obj.one_hot_encoder(linear_dataframe, col)

        return linear_dataframe, tree_dataframe

    def validate(self, Dataframe, data_dict, linear_dataframe, tree_dataframe):

        if data_dict['dummified_columns']['linear']:

            for i in data_dict['dummified_columns']['linear']:

                labels = list(Dataframe[i].value_counts().index)

                labels.sort()

                labels.pop(0)

                if len(labels) < len(data_dict['dummified_columns']['linear'][i]):

                    missing_labels = set(data_dict['dummified_columns']['linear'][i]) - set(labels)

                    for j in missing_labels:
                        linear_dataframe[j] = 0

                elif len(labels) > len(data_dict['dummified_columns']['linear'][i]):

                    excess_labels = set(data_dict['dummified_columns']['linear'][i]) - set(labels)

                    for k in excess_labels:
                        linear_dataframe.drop(k, inplace=True)

        if data_dict['dummified_columns']['tree']:

            for i in data_dict['dummified_columns']['tree']:

                labels = list(Dataframe[i].value_counts().index)

                labels.sort()

                labels.pop(0)

                if len(labels) < len(data_dict['dummified_columns']['tree'][i]):

                    missing_labels = set(data_dict['dummified_columns']['tree'][i]) - set(labels)

                    for j in missing_labels:
                        tree_dataframe[j] = 0

                elif len(labels) > len(data_dict['dummified_columns']['tree'][i]):

                    excess_labels = set(data_dict['dummified_columns']['tree'][i]) - set(labels)

                    for k in excess_labels:
                        tree_dataframe.drop(k, inplace=True)

        return linear_dataframe, tree_dataframe

    def scoring_data_distribution(self, data, data_dict):
        print(len(data.columns))
        l = data[data_dict['linear_features']]
        t = data[data_dict['tree_features']]
        return l, t

    def run(self):

        """pass_1 """

        """DataValidation"""

        # data = self.read_df()
        data = self.path

        data = self.validation(data, self.data_dict)
        print(data.shape)

        """preprocessing"""

        score_preprocessing_obj = ScorePreprocessing(self.data_dict)

        data = score_preprocessing_obj.preprocessing(data, self.data_dict)
        print(data.shape)

        """FeatureEngineering"""
        original_df, created_df, date_col = self.score_feature_eng(data, self.data_dict)
        try:
            print(original_df.columns, created_df.columns)
        except:
            print("No created columns")
        cols = list(set(original_df) - set(date_col))
        original_df = original_df[cols]

        try:
            result = pd.concat([original_df, created_df], axis=1)
        except:
            result = original_df.merge(created_df, left_on=original_df.index, right_on=created_df.index, copy=False)

        print('result: ', result.shape)

        """Feature_selection"""
        linear_df, tree_df = self.scoring_feature_selection(result, self.data_dict)
        ## TO DO: the working of validate function below , could be removed.
        linear_df, tree_df = self.validate(data, self.data_dict, linear_df, tree_df)
        linear_df_cols = [re.sub('\W+', '_', col) for col in linear_df.columns]
        linear_df.columns = linear_df_cols
        tree_df_cols = [re.sub('\W+', '_', col) for col in tree_df.columns]
        tree_df.columns = tree_df_cols
        return linear_df, tree_df

# directory = 'D:/mAdvisor/AutoML/SCORING+TRAINING/OneClick_AutoML (copy)/soccer_train/'
# path = directory + 'test.csv'
#
# import pickle
#
# pickle_in = open(directory+"dict4.pickle","rb")
#
# data_dict = pickle.load(pickle_in)
#
#
# obj = Scoring(path,data_dict)
#
# l,t = obj.run()
# l.to_csv(directory+'linear_score.csv')
# t.to_csv(directory+'tree_score.csv')
#
#
# from Scoring import *
# obj = Scoring(path,data_dict)
#
# linear,tree =  obj.run()
