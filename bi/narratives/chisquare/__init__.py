from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
from builtins import object
import json
import math
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection
from sklearn.ensemble import RandomForestClassifier
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from bi.common import ChartJson
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData
from bi.common import utils as CommonUtils
from bi.narratives import utils as NarrativesUtils
from bi.settings import setting as GLOBALSETTINGS
from .chisquare import ChiSquareAnalysis
from bi.transformations import Binner
from pyspark.ml.classification import DecisionTreeClassifier as pysparkDecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator, VectorAssembler
from pyspark.ml import Pipeline
import pandas as pd
from pyspark.sql import SQLContext
from pyspark.sql.types import *

class ChiSquareNarratives(object):
    #@accepts(object, int, DFChiSquareResult ,ContextSetter)
    def __init__(self, df_helper, df_chisquare_result, spark, df_context, data_frame, story_narrative,result_setter,scriptWeight=None, analysisName=None):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_context = df_context
        self._pandas_flag = df_context._pandas_flag
        self._dataframe_helper = df_helper
        self._storyOnScoredData = self._dataframe_context.get_story_on_scored_data()
        self._measure_columns = df_helper.get_numeric_columns()
        self._df_chisquare = df_chisquare_result
        self._df_chisquare_result = df_chisquare_result.get_result()
        self.narratives = {}
        self._appid = df_context.get_app_id()
        self._chiSquareNode = NarrativesTree()
        self._chiSquareNode.set_name("Key Drivers")
        self._blockSplitter = GLOBALSETTINGS.BLOCKSPLITTER
        self._noOfSigDimsToShow = GLOBALSETTINGS.CHISQUARESIGNIFICANTDIMENSIONTOSHOW
        self._base_dir = "/chisquare/"
        self._spark = spark

        ############################DataFrame Measure to Dimesion Column#####################

        if self._pandas_flag:
            pandas_df = self._data_frame.copy(deep=True)
        else:
            pandas_df = self._data_frame.toPandas()
        target_dimension = list(self._df_chisquare_result.keys())

        bin_data = {}
        for col in self._measure_columns:
            if self._df_chisquare.get_chisquare_result(target_dimension[0],col):
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension[0],col)
                bin_data[col] = chisquare_result.get_contingency_table().get_column_two_levels()

        for bin_col in list(bin_data.keys()):
            for split in bin_data[bin_col]:
                val = split.split('to')
                # pandas_df[bin_col][(float(pandas_df[bin_col])>=float(val[0].replace(',',''))) & (float(pandas_df[bin_col])<float(val[1].replace(',','')))] =  split
                row_value = list(pandas_df[bin_col])
                temp = []
                for  row_value_  in row_value:
                    if not isinstance(row_value_, str)  and  \
                      (float(row_value_) >= float(val[0].replace(',','')))   and   \
                      (float(row_value_) <  float(val[1].replace(',',''))):
                      temp.append(split)
                    else: temp.append(row_value_)
                pandas_df[bin_col] = temp
        if self._pandas_flag:
            pass
            # self._data_frame = pandas_df
        else:
            fields = [StructField(field_name, StringType(), True) for field_name in pandas_df.columns]
            schema = StructType(fields)

            SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
            self._data_frame = SQLctx.createDataFrame(pandas_df,schema)

        # print self._data_frame
        ############################DataFrame Measure to Dimesion Column#####################

        if self._appid != None:
            if self._appid == "1":
                self._base_dir += "appid1/"
            elif self._appid == "2":
                self._base_dir += "appid2/"

        self._completionStatus = self._dataframe_context.get_completion_status()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName

        self._messageURL = self._dataframe_context.get_message_url()
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        if self._analysisDict != {}:
            self._nColsToUse = self._analysisDict[self._analysisName]["noOfColumnsToUse"]
        else:
            self._nColsToUse = None

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Frequency Narratives",
                "weight":0
                },
            "summarygeneration":{
                "summary":"Summary Generation Finished",
                "weight":4
                },
            "completion":{
                "summary":"Frequency Stats Narratives Done",
                "weight":0
                },
            }
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"initialization","info",display=False,weightKey="narratives")
        self.new_effect_size,self.signi_dict = self.feat_imp_threshold(target_dimension)
        self._generate_narratives()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"summarygeneration","info",display=False,weightKey="narratives")

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"completion","info",display=False,weightKey="narratives")
    def feat_imp_threshold(self,target_dimension,dummy_Cols = True,label_encoding= False):
        if self._pandas_flag:
            if is_numeric_dtype(self._data_frame[target_dimension[0]]):
                self.app_type = 'regression'
            elif is_string_dtype(self._data_frame[target_dimension[0]]):
                self.app_type = 'classification'
        else:
            if self._data_frame.select(target_dimension[0]).dtypes[0][1] == 'string':
                self.app_type = 'classification'
            elif self._data_frame.select(target_dimension[0]).dtypes[0][1] in ['int','double']:
                self.app_type = 'regression'
        try:
            DataValidation_obj = DataValidation(self._data_frame, target_dimension[0], self.app_type, self._pandas_flag)
            DataValidation_obj.data_validation_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "datavalidation", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(DataValidation_obj.data_frame, DataValidation_obj.target, DataValidation_obj.data_change_dict, DataValidation_obj.numeric_cols, DataValidation_obj.dimension_cols, DataValidation_obj.datetime_cols,DataValidation_obj.problem_type,self._pandas_flag)
            DataPreprocessingAutoML_obj.data_preprocessing_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "dataPreprocessing", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        preprocess_df = DataPreprocessingAutoML_obj.data_frame
        FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(DataPreprocessingAutoML_obj.data_frame, DataPreprocessingAutoML_obj.target, DataPreprocessingAutoML_obj.data_change_dict, DataPreprocessingAutoML_obj.numeric_cols, DataPreprocessingAutoML_obj.dimension_cols, DataPreprocessingAutoML_obj.datetime_cols, DataPreprocessingAutoML_obj.problem_type,self._pandas_flag)
        if FeatureEngineeringAutoML_obj.datetime_cols != 0:
            FeatureEngineeringAutoML_obj.date_column_split(FeatureEngineeringAutoML_obj.datetime_cols)
        if dummy_Cols:
            if self._pandas_flag:
                FeatureEngineeringAutoML_obj.sk_one_hot_encoding(FeatureEngineeringAutoML_obj.dimension_cols)
                clean_df = FeatureEngineeringAutoML_obj.data_frame
            else:
                FeatureEngineeringAutoML_obj.pyspark_one_hot_encoding(FeatureEngineeringAutoML_obj.dimension_cols)
                clean_df = FeatureEngineeringAutoML_obj.data_frame
        if label_encoding:
            if self._pandas_flag:
                for column_name in FeatureEngineeringAutoML_obj.dimension_cols:
                    preprocess_df[column_name + '_label_encoded'] = LabelEncoder().fit_transform(preprocess_df[column_name])
                    preprocess_df = preprocess_df.drop(column_name,1)
                clean_df = preprocess_df
            else:
                FeatureEngineeringAutoML_obj.pyspark_label_encoding(FeatureEngineeringAutoML_obj.dimension_cols)
                clean_df = FeatureEngineeringAutoML_obj.data_frame
        if self._pandas_flag:
            ind_var = clean_df.drop(target_dimension[0],1)
            target = clean_df[target_dimension[0]]
            dtree = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=42)
            dtree.fit(ind_var, target)
            feat_imp_dict = {}
            for feature, importance in zip(list(ind_var.columns), dtree.feature_importances_):
                feat_imp_dict[feature] = round(importance,2)
        else:
            num_var = [col[0] for col in clean_df.dtypes if ((col[1]=='int') | (col[1]=='double')) & (col[0]!=target_dimension[0])]
            num_var = [col for col in num_var if not col.endswith('indexed')]
            labels_count = [len(clean_df.select(col).distinct().collect()) for col in num_var]
            labels_count.sort()
            max_count =  labels_count[-1]
            label_indexes = StringIndexer(inputCol = target_dimension[0] , outputCol = 'label', handleInvalid = 'keep')
            assembler = VectorAssembler(inputCols = num_var , outputCol = "features")
            model = pysparkDecisionTreeClassifier(labelCol="label",featuresCol="features",seed = 8464,impurity='gini',maxDepth=5,maxBins = max_count+2)
            pipe = Pipeline(stages =[assembler, label_indexes, model])
            mod_fit = pipe.fit(clean_df)
            df2 = mod_fit.transform(clean_df)
            list_extract = []
            for i in df2.schema["features"].metadata["ml_attr"]["attrs"]:
                list_extract = list_extract + df2.schema["features"].metadata["ml_attr"]["attrs"][i]
            varlist = pd.DataFrame(list_extract)
            varlist['score'] = varlist['idx'].apply(lambda x: mod_fit.stages[-1].featureImportances[x])
            feat_imp_dict = pd.Series(varlist.score.values,index=varlist.name).to_dict()
        feat_imp_ori_dict = {}
        actual_cols = list(self._data_frame.columns)
        actual_cols.remove(target_dimension[0])
        for col in actual_cols:
            fea_imp_ori_list = []
            for col_imp in feat_imp_dict:
                temp = col_imp.split(col,-1)
                if len(temp)==2:
                    fea_imp_ori_list.append(feat_imp_dict[col_imp])
            feat_imp_ori_dict.update({col:sum(fea_imp_ori_list)})
        sort_dict = dict(sorted(feat_imp_ori_dict.items(), key=lambda x: x[1],reverse = True))
        if self._pandas_flag:
            cat_var = [key for key in dict(self._data_frame.dtypes) if dict(self._data_frame.dtypes)[key] in ['object']]
        else:
            cat_var = [col[0] for col in self._data_frame.dtypes if col[1]=='string']
        cat_var.remove(target_dimension[0])
        si_var_dict = {key:value for key,value in sort_dict.items() if key in cat_var}
        threshold = 0
        si_var_thresh = {}
        for key,value in si_var_dict.items():
            threshold = threshold + value
            if threshold < 0.8:
                si_var_thresh[key] = value
        return feat_imp_dict,si_var_thresh


    def _generate_narratives(self):
        """
        generate main card narrative and remaining cards are generated by calling ChiSquareAnalysis class for each of analyzed dimensions
        """
        for target_dimension in list(self._df_chisquare_result.keys()):
            target_chisquare_result = self._df_chisquare_result[target_dimension]
            analysed_variables = list(target_chisquare_result.keys())  ## List of all analyzed var.
            # List of significant var out of analyzed var.
            # significant_variables = [dim for dim in list(target_chisquare_result.keys()) if target_chisquare_result[dim].get_pvalue()<=0.05]
            effect_size_dict = self.new_effect_size
            significant_variables = list(self.signi_dict.keys())
            effect_sizes = list(self.signi_dict.values())
            significant_variables = [y for (x,y) in sorted(zip(effect_sizes,significant_variables) ,reverse=True) if round(float(x),2)>0]
            #insignificant_variables = [i for i in self._df_chisquare_result[target_dimension] if i['pv']>0.05]

            num_analysed_variables = len(analysed_variables)
            num_significant_variables = len(significant_variables)
            self.narratives['main_card']= {}
            self.narratives['main_card']['heading'] = 'Relationship between '+target_dimension+' and other factors'
            self.narratives['main_card']['paragraphs'] = {}
            data_dict = {
                          'num_variables' : num_analysed_variables,
                          'num_significant_variables' : num_significant_variables,
                          'significant_variables' : significant_variables,
                          'target' : target_dimension,
                          'analysed_dimensions': analysed_variables,
                          'blockSplitter':self._blockSplitter
            } # for both para 1 and para 2
            paragraph={}
            paragraph['header'] = ''

            paragraph['content'] = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            self.narratives['main_card']['paragraphs']=[paragraph]
            self.narratives['cards'] = []
            chart = {'header':'Strength of association between '+target_dimension+' and other dimensions'}
            chart['data'] = effect_size_dict
            chart['label_text']={'x':'Dimensions',
                                'y':'Feature Importance'}

            chart_data = []
            chartDataValues = []
            for k,v in list(effect_size_dict.items()):
                "rounding the chart data for keydrivers tab"
                if round(float(v),2) > 0:
                    chart_data.append({"Attribute":k,"Effect_Size":round(float(v),2)})
                    chartDataValues.append(round(float(v),2))
            chart_data = sorted(chart_data,key=lambda x:x["Effect_Size"],reverse=True)
            chart_json = ChartJson()
            chart_json.set_data(chart_data)
            chart_json.set_chart_type("bar")
            # chart_json.set_label_text({'x':'Dimensions','y':'Effect Size (Cramers-V)'})
            chart_json.set_label_text({'x':'  ','y':'Feature Importance'})
            chart_json.set_axis_rotation(True)
            chart_json.set_axes({"x":"Attribute","y":"Feature Importance"})
            chart_json.set_yaxis_number_format(".2f")
            # chart_json.set_yaxis_number_format(NarrativesUtils.select_y_axis_format(chartDataValues))
            self.narratives['main_card']['chart']=chart


            main_card = NormalCard()
            header = "<h3>Key Factors that drive "+target_dimension+"</h3>"
            main_card_data = [HtmlData(data=header)]
            main_card_narrative = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            main_card_narrative = NarrativesUtils.block_splitter(main_card_narrative,self._blockSplitter)
            main_card_data += main_card_narrative
            # st_info = ["Test : Chi Square", "Threshold for p-value : 0.05", "Effect Size : Cramer's V"]
            # print "chartdata",chart_data
            if len(chart_data) > 0:
                statistical_info_array=[
                    ("Test Type","Chi-Square"),
                    ("Effect Size","Cramer's V"),
                    ("Max Effect Size",chart_data[0]["Attribute"]),
                    ("Min Effect Size",chart_data[-1]["Attribute"]),
                    ]
                statistical_inferenc = ""
                if len(chart_data) == 1:
                    statistical_inference = "{} is the only variable that have significant association with the {} (Target) having an \
                     Effect size of {}".format(chart_data[0]["Attribute"],self._dataframe_context.get_result_column(),round(chart_data[0]["Effect_Size"],4))
                elif len(chart_data) == 2:
                    statistical_inference = "There are two variables ({} and {}) that have significant association with the {} (Target) and the \
                     Effect size ranges are {} and {} respectively".format(chart_data[0]["Attribute"],chart_data[1]["Attribute"],self._dataframe_context.get_result_column(),round(chart_data[0]["Effect_Size"],4),round(chart_data[1]["Effect_Size"],4))
                else:
                    statistical_inference = "There are {} variables that have significant association with the {} (Target) and the \
                     Effect size ranges from {} to {}".format(len(chart_data),self._dataframe_context.get_result_column(),round(chart_data[0]["Effect_Size"],4),round(chart_data[-1]["Effect_Size"],4))
                if statistical_inference != "":
                    statistical_info_array.append(("Inference",statistical_inference))
                statistical_info_array = NarrativesUtils.statistical_info_array_formatter(statistical_info_array)
            else:
                statistical_info_array = []
            main_card_data.append(C3ChartData(data=chart_json,info=statistical_info_array))
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Key Influencers")

            if self._storyOnScoredData != True:
                self._chiSquareNode.add_a_card(main_card)
                self._result_setter.add_a_score_chi_card(main_card)

            print("target_dimension",target_dimension)
            if self._appid=='2' and num_significant_variables>5:
                significant_variables = significant_variables[:5]
            else:
                if self._nColsToUse != None:
                    significant_variables = significant_variables[:self._nColsToUse]
                    nColsToUse_temp =  self._nColsToUse
                else:
                    nColsToUse_temp =  self._noOfSigDimsToShow

            CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"custom","info",display=True,customMsg="Analyzing key drivers",weightKey="narratives")
            for analysed_dimension in significant_variables[:nColsToUse_temp]:
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                if self._appid=='2':
                    print("APPID 2 is used")
                    card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns, self._base_dir,None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))

                elif self._appid=='1':
                    print("APPID 1 is used")
                    card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))
                else:
                    target_dimension_card = ChiSquareAnalysis(self._dataframe_context,self._dataframe_helper,chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    self.narratives['cards'].append(target_dimension_card)
                    self._chiSquareNode.add_a_node(target_dimension_card.get_dimension_node())
        self._story_narrative.add_a_node(self._chiSquareNode)
        self._result_setter.set_chisquare_node(self._chiSquareNode)
