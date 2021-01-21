from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import zip
from past.builtins import basestring
from builtins import object
from past.utils import old_div
import json
import re
import numpy as np
import ast
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
import pyspark.sql.functions as F

from bi.algorithms import utils as MLUtils
from bi.common import utils as CommonUtils
from bi.common import dataframe as dataframe

from bi.common.datafilterer import DataFrameFilterer
from bi.common.decorators import accepts
from bi.common.results import DecisionTreeResult
from bi.settings import setting as GLOBALSETTINGS
from sklearn.datasets import *
from sklearn.tree import DecisionTreeClassifier,_tree
from sklearn.tree import export_graphviz
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from pyspark.sql.functions import col, countDistinct
import pydotplus
from io import BytesIO
import collections
import unicodedata
import math
"""
Decision Tree
"""


class DecisionTrees(object):

    # @accepts(object, DataFrame)
    def __init__(self, data_frame, df_helper, df_context, spark, meta_parser, max_depth=5, scriptWeight=None, analysisName=None):
        self._spark = spark
        self._maxDepth = max_depth
        self._metaParser = meta_parser
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._pandas_flag = df_context._pandas_flag
        self._ignoreMsg = self._dataframe_context.get_message_ignore()
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        self._measure_columns = self._dataframe_helper.get_numeric_columns()
        # if self._analysisDict:
        #     for m in self._measure_columns:
        #         if data_frame.select(F.countDistinct(m)).collect()[0][0]<self._analysisDict['Dimension vs. Dimension']['binSetting']['binCardinality']:
        #             self._measure_columns.remove(m)
        self._dimension_columns = self._dataframe_helper.get_string_columns()
        self._date_columns = self._dataframe_context.get_date_columns()
        self._uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(self._uid_col):
            self._dimension_columns = list(set(self._dimension_columns) - {self._uid_col})
        if len(self._date_columns) >0 :
            self._dimension_columns = list(set(self._dimension_columns)-set(self._date_columns))
        if not self._pandas_flag:
            self._data_frame = MLUtils.bucket_all_measures(data_frame,self._measure_columns,self._dimension_columns,pandas_flag=self._pandas_flag)
        else:
            self._data_frame = data_frame
        try:
            self._data_frame1 = self._data_frame.copy()
        except:
            self._data_frame1 = self._data_frame
        self._mapping_dict = {}
        self._new_rules = {}
        self._total = {}
        self._success = {}
        self._fail={}
        self._probability = {}
        self._alias_dict = {}
        self._important_vars = {}
        self._total_list=[]
        self._row_count=[]
        self._targetlevels=[]
        self._new_list=[]
        self._count_list=[]
        self._rule_id=0
        self._path_dict={}

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

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized The Decision Tree Script",
                "weight":0
                },
            "treegeneration":{
                "summary":"Decision Tree Generation Finished",
                "weight":10
                }
            }
        self._completionStatus += old_div(self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["initialization"]["weight"],10)
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=self._ignoreMsg)
        self._dataframe_context.update_completion_status(self._completionStatus)
        print("I AM HERE")

    def parse(self, lines, df):
        block = []
        while lines :

            if lines[0].startswith('If'):

                bl = ' '.join(lines.pop(0).split()[1:]).replace('(', '').replace(')', '')
                if "feature" in bl:
                    feature_mapping = df.columns[int(bl.split()[1]) + 1]
                    bl = "%s %s" % (feature_mapping, ' '.join(bl.split()[2:]))

                    if "{" in bl:
                        sub_mappings = json.loads(bl.split()[-1].strip().replace('{', '[').replace('}', ']'))
                        sub_mappings_string = '(' +  ','.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                        bl = "%s in %s" % (feature_mapping, sub_mappings_string)
                block.append({'name':bl, 'children':self.parse(lines, df)})
                if lines[0].startswith('Else'):
                    be = ' '.join(lines.pop(0).split()[1:]).replace('(', '').replace(')', '')
                    if "feature" in be:
                        feature_mapping = df.columns[int(be.split()[1]) + 1]
                        be = "%s %s" % (feature_mapping, ' '.join(be.split()[2:]))
                        if "{" in be:
                            sub_mappings = json.loads(be.split()[-1].strip().replace('{', '[').replace('}', ']'))
                            sub_mappings_string = '(' + ','.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                            be = "%s not in %s" % (feature_mapping, sub_mappings_string)
                    block.append({'name':be, 'children':self.parse(lines, df)})
            elif not lines[0].startswith(('If','Else')):
                block2 = lines.pop(0)
                if "feature" in block2:
                    block2 = "%s %s" % (df.columns[int(block2.split()[1])], ' '.join(block2.split()[2:]))
                if "Predict" in block2:
                    outcome = self._mapping_dict[df.columns[0]][int(float(block2.split(':')[1].strip()))]
                    block2 = "Predict: %s" % (outcome)
                block.append({'name':block2})
            else:
                break
        return block


    def parse_pandas(self, lines, df,check_list=[],n=["."]):
        block = []
        while lines :

            if lines[0].startswith('if'):

                bl = ' '.join(lines.pop(0).split()[1:]).replace(':', '').replace(')', '')
                feature_mapping = bl.split()[0]
                if "<=" or "<" in bl:
                    # sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x <= math.floor(float(bl.split()[-1]))]
                    # sub_mappings_string = '(' +  ', '.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                    # bl = "%s in %s" % (feature_mapping, sub_mappings_string)
                    bl = bl
                elif ">=" or ">" in bl:
                    # sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x >= math.ceil(float(bl.split()[-1]))]
                    # sub_mappings_string = '(' +  ', '.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                    # bl = "%s in %s" % (feature_mapping, sub_mappings_string)
                    bl = bl
                if bl not in check_list:
                    check_list.append(bl)

                else:
                    bl = str(n[0])+bl
                    n[0] =n[0]+" "
                block.append({'name':bl, 'children':self.parse_pandas(lines, df)})
                if lines[0].startswith('else'):

                    be = ' '.join(lines.pop(0).split()[3:]).replace('#', '').replace(':', '')
                    feature_mapping = be.split()[0]

                    if ">" or ">=" in be:
                        # sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x <= math.floor(float(be.split()[-1]))]
                        # sub_mappings_string = '(' + ', '.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                        # be = "%s not in %s" % (feature_mapping, sub_mappings_string)
                        be = be
                    if be not in check_list:
                        check_list.append(be)
                    else:
                        be = str(n[0]) + be
                        n[0] =n[0]+" "
                    block.append({'name':be, 'children':self.parse_pandas(lines, df)})
            elif not lines[0].startswith(('if','else')):
                block2 = lines.pop(0)
                if "return" in block2:
                    # outcome = self._mapping_dict[df.columns[0]][int(float(block2.split(' ')[1].strip()))]
                    block2 = "Predict: %s" % (str(int(float(block2.split(' ')[1].strip()))))
                block.append({'name':block2})
            else:
                break

        return block

# look into floor/ceil for measure columns: binned in the pandas tree?

    def tree_json(self, tree, df, pandas_flag):
        if not pandas_flag:
            data = []
            for line in tree.splitlines() :
                if line.strip():
                    line = line.strip()
                    data.append(line)
                else : break
                if not line : break
            print ("data", data)
        res = []
        if pandas_flag:
            ## TODO: parse has to be done for pandas
            res.append({'name': 'Root', 'children':self.parse_pandas(tree, df)}) #,'count':self.parse_count(data[1:],df)})
        else:
            print ("\n\n")
            print ("parse output", self.parse(data[1:], df))
            res.append({'name': 'Root', 'children':self.parse(data[1:], df)}) #,'count':self.parse_count(data[1:],df)})

        return res[0]


    @accepts(object, rule_list=list,target=str)
    def extract_rules(self, rule_list, target):
        if target not in self._important_vars:
            self._important_vars[target] = []
        if self._pandas_flag:
            DFF = DataFrameFilterer(self._data_frame, self._pandas_flag)
        else:
            DFF = DataFrameFilterer(self._data_frame1, self._pandas_flag)
        colname = self._target_dimension
        success = 0
        total = 0
        important_vars = []
        targetcols=[]
        row_count=[]
        dict_tree=[]
        data_dict={}
        for rows in DFF.get_count_result(colname):
            if rows is not None:
                data_dict[rows[0]]=rows[1]
        dict_tree.append(data_dict)


        for rule in rule_list:

            if ' <= ' in rule:
                var, limit = re.split(' <= ', rule)
                DFF.values_below(var, float(limit))
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            elif ' > ' in rule:
                var,limit = re.split(' > ',rule)
                DFF.values_above(var.lstrip('0123456789. '), float(limit))
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            elif ' not in ' in rule:
                var,levels = rule.split(' not in (')
                levels = levels.lstrip('. ')
                if self._pandas_flag:
                    levels=levels[0:-1].split(", ")
                else:
                    levels=levels[0:-1].split(",")
                if '' in levels:
                    levels.remove('')
                levels1 = [key if x==key else self._alias_dict[x] for x in levels for key in  list(self._alias_dict.keys())]
                #levels = [self._alias_dict[x] for x in levels]
                DFF.values_not_in(var,levels1,self._measure_columns)
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)


            elif ' in ' in rule:
                var,levels = rule.split(' in (')
                levels = levels.lstrip('. ')
                if self._pandas_flag:
                    levels=levels[0:-1].split(", ")
                else:
                    levels=levels[0:-1].split(",")
                if '' in levels:
                    levels.remove('')

                levels1 = [x  if x==key else self._alias_dict[x] for x in levels for key in  list(self._alias_dict.keys())]
                #levels = [self._alias_dict[x] for x in levels]
                DFF.values_in(var,levels1,self._measure_columns)
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            important_vars.append(var)
        for rows in DFF.get_aggregated_result(colname,target):
            if self._pandas_flag:
                if(rows[0]==int(target)):
                    success = rows[1]
                total = total + rows[1]
                self._total_list.append(total)
            else:
                if(rows[0]==target):
                    success = rows[1]
                total = total + rows[1]
                self._total_list.append(total)

        self._important_vars[target] = list(set(self._important_vars[target] + important_vars))
        if (total > 0):
            if target not in self._new_rules:
                self._new_rules[target] = []
                self._total[target] = []
                self._success[target] = []
                self._probability[target] = []
            self._new_rules[target].append(','.join(rule_list))
            self._total[target].append(total)
            self._success[target].append(success)
            self._probability[target].append(old_div(success*100.0,total))
            return success,total,dict_tree


    def node_name_extractor(self, tree_dict):
        new_list=[]
        if "children" in list(tree_dict.keys()) and len(tree_dict['children'])>0:
            if tree_dict['name'] not in new_list:
                new_list.append(tree_dict['name'])
                for child in tree_dict['children']:
                    if not "fruits" in list(child.keys()):
                            val=self.node_name_extractor(child)
                            if val!= None:
                                if val not in new_list:
                                    new_list.append(val)
                    else:
                        for idx,fruit in enumerate(child['fruits']):
                            if (fruit,idx) not in self._count_list:
                                self._count_list.append((fruit,idx))


        return new_list


    def path_extractor(self,dct, value, path=()):
        for key, val in list(dct.items()):
            if val == value:
                yield path + (key, )
        for key, lst in list(dct.items()):
            if isinstance(lst, list):
                for idx,item in enumerate(lst):
                    for pth in self.path_extractor(item, value, path + (key,idx )):
                        yield pth


    def path_dict_creator(self,tree_list,new_tree):
        path_list=[]
        for val in tree_list:
            for item in self.path_extractor(new_tree, value=val):
                    if val=="Root":
                        path_list.append("Root")
                    else:
                        path="Root"
                        for i in item:
                            if type(i)!=int:
                                path=path+"."+i
                            else:
                                path=path+"[{}]".format(i)
                                if path not in path_list:
                                    path_list.append(path)
                                    path_dict=dict(list(zip(tree_list,path_list)))

        return path_dict


    def generate_new_tree(self, rules, rule_list=None):
        if rule_list is None:
            rule_list = []
        rules_list=rule_list
        new_rules = {'name':rules['name']}
        if 'children' in rules:
            for rule in rules['children']:
                if rules['name']!='Root':
                    val = self.generate_new_tree(rule,rule_list=rules_list+[rules['name']])
                else:
                    val = self.generate_new_tree(rule,rule_list=rules_list)
                if val!=None:
                    if 'children' not in new_rules:
                        new_rules['children'] = []
                    new_rules['children'].append(val)
            return new_rules
        else:
            new_rules = {'name':rules['name'],'fruits':[]}
            target = rules['name'][9:]
            try:
                num_success,num_total,dict_tree = self.extract_rules(rules_list,target)
            except Exception as e:
                print("ONE RULE EXCEPTION")
                print(e)
                return(None)
            new_rules['fruits']=dict_tree
            vals=list(dict_tree[-1].values())
            extract_level = new_rules['name']
            rule_target_level =  extract_level.split(':')[-1][1:]
            new_level_dict = dict_tree[-1]
            if self._pandas_flag:
                new_rules['probability']=round(old_div(new_level_dict[int(rule_target_level)]*100.0,sum(vals)),2)
            else:
                new_rules['probability']=round(old_div(new_level_dict[rule_target_level]*100.0,sum(vals)),2)
            print(new_rules['probability'])
            if 'Predict:' in rules['name'] and num_success>0:
                return new_rules


    def flatten(self,l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    def wrap_tree(self, tree, tree_dict):
        new_tree = {}
        if "children" in list(tree.keys()) and len(tree['children'])>0:
            for item in list(tree_dict.keys()):
                if item.find(tree['name']) != -1:
                    #tree_name=tree['name'].split("(")
                    new_tree['name']= tree['name']
                    new_tree['name1'] = str(tree_dict.get(item))
                    new_tree['name1'] = new_tree['name1'].replace("u'", "'")
                    new_tree['name1'] = new_tree['name1'].replace("'", '')
            for child in tree['children']:
                val = self.wrap_tree(child,tree_dict)
                if val!= None:
                    if 'children' not in new_tree:
                        new_tree['children']=[]
                    new_tree['children'].append(val)

            if 'children' in new_tree:
                if len(new_tree['children'])>0:
                    return new_tree

        elif 'Predict: ' in tree['name'] or 'Root' in tree['name']:
            new_tree['name'] = tree['name']
            new_tree['name1']="Probability:"+str(tree['probability']) + "%"
            return new_tree

    def tree_to_code(self, tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        l=[]
        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                l.append("{}if {} <= {}:".format(indent, name, threshold))
                recurse(tree_.children_left[node], depth + 1)
                l.append("{}else:  # if {} > {}".format(indent, name, threshold))
                recurse(tree_.children_right[node], depth + 1)
            else:
                l.append("{}return {}".format(indent, np.argmax(tree_.value[node][0])))

        recurse(0, 1)
        return l

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple))
    def test_all(self, measure_columns=None, dimension_columns=None):
        measures = measure_columns
        if measure_columns is None:
            measures = self._measure_columns
        self._target_dimension = dimension_columns[0]
        dimension = self._target_dimension

        #####Look into it for Issue 947#################
        max_num_levels = GLOBALSETTINGS.DTREE_OTHER_DIMENSION_MAX_LEVEL
        # max_num_levels = min(max_num_levels, round(self._dataframe_helper.get_num_rows()**0.5))
        # all_dimensions = [dim for dim in self._dimension_columns if self._dataframe_helper.get_num_unique_values(dim) <= max_num_levels]
        all_dimensions = [dim for dim in self._dimension_columns if self._metaParser.get_num_unique_values(dim) <= max_num_levels]
        all_measures = self._measure_columns
        if self._pandas_flag:
            self._data_frame=self._data_frame[all_dimensions+all_measures]
        cat_feature_info = []
        columns_without_dimension = [x for x in all_dimensions if x != dimension]
        mapping_dict = {}
        masterMappingDict = {}
        decision_tree_result = DecisionTreeResult()
        decision_tree_result.set_freq_distribution(self._metaParser.get_unique_level_dict(self._target_dimension), self._important_vars)
        if self._pandas_flag:
            try:
                all_dimensions.remove(dimension)
            except:
                pass
            actual_cols = list(self._data_frame.columns)
            print(actual_cols)
            self._data_frame=pd.get_dummies(self._data_frame,columns=all_dimensions)
            after_dummy_cols = list(self._data_frame.columns)

            def Diff(li1, li2):
                return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))
            decision_tree_result.dummy_cols=[Diff(after_dummy_cols,Diff(actual_cols,all_dimensions)),all_dimensions]

        all_dimensions.append(dimension)#this has been done for scoring error
        if self._pandas_flag:
            self._data_frame, mapping_dict = MLUtils.add_string_index(self._data_frame, [dimension], self._pandas_flag)
        else:
            self._data_frame, mapping_dict = MLUtils.add_string_index(self._data_frame, all_dimensions, self._pandas_flag)
        if self._pandas_flag:
            print(self._data_frame.head(1))
        else:
            print(self._data_frame.show(1))
        # standard_measure_index = {0.0:'Low',1.0:'Medium',2.0:'High'}
        standard_measure_index = {0.0:'Low',1.0:'Below Average',2.0:'Average',3.0:'Above Average',4.0:'High'}
        for measure in all_measures:
            mapping_dict[measure] = standard_measure_index

        for k,v in list(mapping_dict.items()):
            temp = {}
            for k1,v1 in list(v.items()):
                self._alias_dict[v1.replace(",","")] = v1
                temp[k1] = v1.replace(",","")
            mapping_dict[k] = temp
        self._mapping_dict = mapping_dict
        if not self._pandas_flag:

            for c in columns_without_dimension:
                if self._pandas_flag:
                    cat_feature_info.append(len(self._data_frame[c].unique()))
                else:
                    cat_feature_info.append(self._data_frame.select(c).distinct().count())
            for c in all_measures:
                cat_feature_info.append(5)
            columns_without_dimension = columns_without_dimension+all_measures
            all_measures = []
            if len(cat_feature_info)>0:
                max_length = max(cat_feature_info)
            else:
                max_length=32
        else:
            decision_tree_result.mappingdict=mapping_dict[dimension]
            max_length=32
        cat_feature_info = dict(enumerate(cat_feature_info))
        if self._pandas_flag:
            dimension_classes = len(self._data_frame[dimension].unique())
        else:
            dimension_classes = self._data_frame.select(dimension).distinct().count()
        if not self._pandas_flag:
            self._data_frame = self._data_frame[[dimension] + columns_without_dimension + all_measures]
        print("="*200)
        # print self._data_frame.rdd.first()
        print("numClasses",dimension_classes)
        print("maxDepth",self._maxDepth)
        decision_tree_result._maxDepth = self._maxDepth
        print("maxBins",max_length)
        print("="*200)
        if self._pandas_flag:
            x = self._data_frame.drop(dimension,axis=1)
            y = self._data_frame[dimension]
            #tle = LabelEncoder()
            #y = tle.fit_transform(y)
            for i in x.columns:
                x[i] = x[i].fillna(x[i].mode()[0])
            model = DecisionTreeClassifier(criterion='gini', max_depth=self._maxDepth,random_state=42)
            model = model.fit(x,y)
            output_result = self.tree_to_code(model,list(x.columns))
            output_result = list(map(lambda x:x.strip(),output_result))
        else:
            data = self._data_frame.rdd.map(lambda x: LabeledPoint(x[0], x[1:]))
            (trainingData, testData) = data.randomSplit([1.0, 0.0])
            # TO DO : set maxBins at least equal to the max level of categories in dimension column
            # model = DecisionTree.trainClassifier(trainingData, numClasses=dimension_classes, categoricalFeaturesInfo=cat_feature_info, impurity='gini', maxDepth=self._maxDepth, maxBins=max_length)
            # Removed categoricalFeaturesInfo to be passed to DecisionTree to get all levels and consider all feature as continuous variables
            #But that results in wrong result in Prediction Rule eg: columns containing "yes" or "no" as its value is considered as float value(0.5) so removing categoricalFeaturesInfo={} with categoricalFeaturesInfo=cat_feature_info
            model = DecisionTree.trainClassifier(trainingData, numClasses=dimension_classes, categoricalFeaturesInfo=cat_feature_info, impurity='gini', maxDepth=self._maxDepth, maxBins=max_length)
            output_result = model.toDebugString()
        decision_tree = self.tree_json(output_result, self._data_frame, self._pandas_flag)
        self._new_tree = self.generate_new_tree(decision_tree)
        node_list = self.node_name_extractor(self._new_tree)
        node_list=list(self.flatten(node_list))
        correct_count_list=[i[0] for i in  self._count_list]
        tree_dict=dict(list(zip(node_list,correct_count_list)))
        self._new_tree = self.wrap_tree(self._new_tree,tree_dict)
        self._path_dict=self.path_dict_creator(node_list,self._new_tree)
        print("==="*40)
        decision_tree_result.set_params(self._new_tree, self._new_rules, self._total, self._success, self._probability,self._path_dict)
        self._completionStatus += old_div(self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["treegeneration"]["weight"],10)
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "treegeneration",\
                                    "info",\
                                    self._scriptStages["treegeneration"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=self._ignoreMsg)
        self._dataframe_context.update_completion_status(self._completionStatus)

        return decision_tree_result
