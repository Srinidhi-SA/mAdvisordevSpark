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
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from sklearn.tree import  DecisionTreeRegressor,_tree
from bi.common.datafilterer import DataFrameFilterer
from bi.common.decorators import accepts
from bi.common.results import DecisionTreeResult

from bi.algorithms import utils as MLUtils
from bi.common import utils as CommonUtils
from bi.algorithms import KmeansClustering
from bi.settings import setting as GLOBALSETTINGS

from bi.common import DataLoader
from bi.common import DataFrameHelper
import collections
import math
"""
Decision Tree
"""


class DecisionTreeRegression(object):

    #@accepts(object, DataFrame)
    def __init__(self, data_frame, df_context, df_helper, spark, meta_parser,scriptWeight=None, analysisName=None):
        self._spark = spark
        self._metaParser = meta_parser
        self._data_frame = data_frame
        self._data_frame1 = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._pandas_flag = df_context._pandas_flag
        self._measure_columns = self._dataframe_helper.get_numeric_columns()
        self._dimension_columns = self._dataframe_helper.get_string_columns()
        self._date_columns = self._dataframe_context.get_date_columns()
        self._uid_col = self._dataframe_context.get_uid_column()
        if self._metaParser.check_column_isin_ignored_suggestion(self._uid_col):
            self._dimension_columns = list(set(self._dimension_columns) - {self._uid_col})
        if len(self._date_columns) >0 :
            self._dimension_columns = list(set(self._dimension_columns)-set(self._date_columns))
        self._mapping_dict = {}
        self._new_rules = {}
        self._total = {}
        self._success = {}
        self._probability = {}
        self._alias_dict = {}
        self._important_vars = {}
        self._numCluster = None
        self._count_list=[]

        self._data_frame = self._dataframe_helper.fill_missing_values(self._data_frame)
        self._data_frame1 = self._dataframe_helper.fill_missing_values(self._data_frame1)

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._messageURL = self._dataframe_context.get_message_url()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_measure_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight
        self._scriptStages = {
            "dtreeTrainingStart":{
                "summary":"Started The Decision Tree Regression Script",
                "weight":0
                },
            "dtreeTrainingEnd":{
                "summary":"Decision Tree Regression Learning Finished",
                "weight":10
                },
            }

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"dtreeTrainingStart","info",weightKey="script")



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
                    # print "block2",block2
                    # print self._mapping_dict[df.columns[0]]
                    # print [int(float(block2.split(':')[1].strip()))]
                    outcome = self._mapping_dict[df.columns[0]][int(float(block2.split(':')[1].strip()))]
                    block2 = "Predict: %s" % (outcome)
                block.append({'name':block2})
            else:
                break
        return block

    def parse_pandas(self, lines, df):
        block = []
        while lines :

            if lines[0].startswith('if'):

                bl = ' '.join(lines.pop(0).split()[1:]).replace(':', '').replace(')', '')
                feature_mapping = bl.split()[0]
                try:
                    if "<=" or "<" in bl:
                        sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x <= math.floor(float(bl.split()[-1]))]
                        sub_mappings_string = '(' +  ','.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                        bl = "%s in %s" % (feature_mapping, sub_mappings_string)

                    elif ">=" or ">" in bl:
                        sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x >= math.ceil(float(bl.split()[-1]))]
                        sub_mappings_string = '(' +  ','.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                        bl = "%s in %s" % (feature_mapping, sub_mappings_string)
                except:
                    pass
                block.append({'name':bl, 'children':self.parse_pandas(lines, df)})
                if lines[0].startswith('else'):

                    be = ' '.join(lines.pop(0).split()[3:]).replace('#', '').replace(':', '')
                    feature_mapping = be.split()[0]

                    try:
                        if ">" or ">=" in be:
                            sub_mappings = [x for x in list(self._mapping_dict[feature_mapping].keys()) if x <= math.floor(float(be.split()[-1]))]
                            sub_mappings_string = '(' + ','.join(list(self._mapping_dict[feature_mapping][int(x)] for x in sub_mappings)) + ')'
                            be = "%s not in %s" % (feature_mapping, sub_mappings_string)
                    except:
                        pass
                    block.append({'name':be, 'children':self.parse_pandas(lines, df)})
            elif not lines[0].startswith(('if','else')):
                block2 = lines.pop(0)
                if "return" in block2:
                    outcome = self._mapping_dict[df.columns[0]][int(float(block2.split(' ')[1].replace(']', '').replace('[', '').strip()))]
                    block2 = "Predict: %s" % (outcome)
                block.append({'name':block2})
            else:
                break

        return block


    def tree_json(self, tree, df, pandas_flag):
        if not pandas_flag:
            data = []
            for line in tree.splitlines():
                if line.strip():
                    line = line.strip()
                    data.append(line)
                else:
                    break
                if not line:
                    break
        res = []
        if pandas_flag:
            ## TODO: parse has to be done for pandas
            res.append({'name': 'Root', 'children':self.parse_pandas(tree, df)})  # ,'count':self.parse_count(data[1:],df)})
        else:
            # print("\n\n")
            # print("parse output", self.parse(data[1:], df))
            res.append(
                {'name': 'Root', 'children': self.parse(data[1:], df)})  # ,'count':self.parse_count(data[1:],df)})
        # print(res[0]["children"])
        return res[0]

    @accepts(object, rule_list=list,target=str)
    def extract_rules(self, rule_list, target):
        if target not in self._important_vars:
            self._important_vars[target] = []
        target = self._reverse_map[target]
        DFF = DataFrameFilterer(self._data_frame1, self._pandas_flag)
        colname = self._target_dimension
        success = 0
        total = 0
        important_vars = []
        targetcols = []
        row_count = []
        dict_tree=[]
        data_dict={}
        for rows in DFF.get_count_result(colname):
            if rows is not None:
                data_dict[rows[0]]=rows[1]
        dict_tree.append(data_dict)
        for rule in rule_list:
            if ' <= ' in rule:
                var,limit = re.split(' <= ',rule)
                DFF.values_below(var,float(limit))
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            elif ' > ' in rule:
                var,limit = re.split(' > ',rule)
                DFF.values_above(var,float(limit))
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            elif ' not in ' in rule:
                var, levels = re.split(' not in ', rule)
                levels = levels[1:-1].split(",")
                #levels = [self._alias_dict[x] for x in levels]
                levels1 = [key if x==key else self._alias_dict[x] for x in levels for key in  list(self._alias_dict.keys())]
                DFF.values_not_in(var,levels1,self._measure_columns)
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            elif ' in ' in rule:
                var, levels = re.split(' in ', rule)
                levels = levels[1:-1].split(",")
                #levels = [self._alias_dict[x] for x in levels]
                levels1 = [key if x==key else self._alias_dict[x] for x in levels for key in  list(self._alias_dict.keys())]
                DFF.values_in(var,levels1,self._measure_columns)
                data_dict={}
                for rows in DFF.get_count_result(colname):
                    if rows is not None:
                        data_dict[rows[0]]=rows[1]
                dict_tree.append(data_dict)
            important_vars.append(var)
        for rows in DFF.get_aggregated_result(colname,target):
            if(rows[0]==target):
                success = rows[1]
            total = total + rows[1]
        target = self._mapping_dict[self._target_dimension][target]
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
            num_success,num_total,dict_tree = self.extract_rules(rules_list,target)
            new_rules['fruits'] = dict_tree
            vals = list(dict_tree[-1].values())
            new_rules['probability'] = round(old_div(max(vals) * 100.0, sum(vals)), 2)
            if 'Predict:' in rules['name'] and num_success > 0:
                return new_rules

    def node_name_extractor(self,tree_dict):
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

    def wrap_tree(self, tree,tree_dict):
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
                l.append("{}return {}".format(indent, tree_.value[node][0]))

        recurse(0, 1)
        return l

    def flatten(self,l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    def transform_data_frames(self):
        self._data_frame, self._mapping_dict = MLUtils.add_string_index(self._data_frame, self._dimension_columns, self._pandas_flag)
        # self._data_frame, clusters = MLUtils.cluster_by_column(self._data_frame, self._target_dimension)
        # self._data_frame1, self._aggr_data = MLUtils.cluster_by_column(self._data_frame1, self._target_dimension, get_aggregation=True)
        # self._data_frame, clusters = MLUtils.bin_column(self._data_frame, self._target_dimension)
        self._data_frame, clusters, splitRanges = MLUtils.bin_column(self._data_frame, self._target_dimension, pandas_flag=self._pandas_flag)

        self._data_frame1, self._aggr_data = MLUtils.bin_column(self._data_frame1, self._target_dimension, get_aggregation=True, pandas_flag=self._pandas_flag)
        self._cluster_order = [x[1] for x in sorted(zip(clusters,[0,1,2]))]
        displayArray = list(zip(GLOBALSETTINGS.DECISIONTREERKMEANSTARGETNAME,splitRanges))
        displayArray = [x[0]+" : "+x[1] for x in displayArray]
        self._mapping_dict[self._target_dimension] = dict(list(zip(self._cluster_order,displayArray)))
        self._reverse_map = {}
        for k,v in self._mapping_dict[self._target_dimension].items():
            self._reverse_map[v] = k
        self.set_alias_dict()


    # def transform_data_frames(self):
    #     self._data_frame, self._mapping_dict = MLUtils.add_string_index(self._data_frame, self._dimension_columns)
    #     kmeans_obj = KmeansClustering(self._data_frame, self._dataframe_helper, self._dataframe_context, self._metaParser, self._spark)
    #     kmeans_obj.kmeans_pipeline([self._target_dimension],cluster_count=3)
    #     kmeans_result = {"stats":kmeans_obj.get_kmeans_result(),"data":kmeans_obj.get_prediction_data()}
    #     self._aggr_data = kmeans_obj.get_aggregated_summary(self._target_dimension)
    #     print "kmeans_result",kmeans_result
    #     clusterCenters = sorted([x[0] for x in kmeans_result["stats"]["centers"]])
    #     self._numCluster = len(clusterCenters)
    #     print dict(zip(range(len(clusterCenters)),GLOBALSETTINGS.DECISIONTREERKMEANSTARGETNAME))
    #     self._mapping_dict[self._target_dimension] = dict(zip(range(len(clusterCenters)),GLOBALSETTINGS.DECISIONTREERKMEANSTARGETNAME))
    #     self._reverse_map = {}
    #     for k,v in self._mapping_dict[self._target_dimension].iteritems():
    #         self._reverse_map[v] = k
    #     predictedDf = kmeans_obj.get_prediction_data()
    #     print "predictedDf"*3
    #     print predictedDf.show(3)
    #     self._data_frame = predictedDf.select([x for x in self._data_frame.columns if x != self._target_dimension]+["prediction"])
    #     self._data_frame = self._data_frame.withColumnRenamed("prediction",self._target_dimension)
    #     self.set_alias_dict()

    def set_alias_dict(self):
        mapping_dict = self._mapping_dict
        for k,v in list(mapping_dict.items()):
            temp = {}
            for k1,v1 in list(v.items()):
                self._alias_dict[v1.replace(",","")] = v1
                temp[k1] = v1.replace(",","")
            mapping_dict[k] = temp
        self._mapping_dict = mapping_dict

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple))
    def test_all(self, measure_columns=None, dimension_columns=None):
        if dimension_columns is None:
            dimensions = self._dimension_columns
        self._target_dimension = measure_columns[0]
        dimension = self._target_dimension
        max_num_levels = GLOBALSETTINGS.DTREE_OTHER_DIMENSION_MAX_LEVEL
        max_num_levels = min(max_num_levels, round(self._dataframe_helper.get_num_rows()**0.5))
        # all_dimensions = [dim for dim in self._dimension_columns if self._dataframe_helper.get_num_unique_values(dim) <= max_num_levels]
        all_dimensions = [dim for dim in self._dimension_columns if self._metaParser.get_num_unique_values(dim) <= max_num_levels]
        all_measures = [x for x in self._measure_columns if x!=self._target_dimension]
        self.transform_data_frames()
        decision_tree_result = DecisionTreeResult()
        cat_feature_info = [len(self._mapping_dict[c]) for c in all_dimensions]
        if len(cat_feature_info)>0:
            max_length = max(cat_feature_info)
        else:
            max_length=32
        cat_feature_info = dict(enumerate(cat_feature_info))
        # print cat_feature_info
        if self._pandas_flag:
            dimension_classes = self._data_frame[dimension].nunique()
            self._data_frame = self._data_frame[[dimension] + all_dimensions + all_measures]
            x = self._data_frame.drop(dimension, axis=1)
            y = self._data_frame[dimension]
            for i in x.columns:
                x[i] = x[i].fillna(x[i].mode()[0])
            model = DecisionTreeRegressor(max_depth=6)
            model = model.fit(x, y)
            output_result = self.tree_to_code(model, list(x.columns))
            output_result = list(map(lambda x: x.strip(), output_result))
            print(output_result, "output_result")
        else:
            dimension_classes = self._data_frame.select(dimension).distinct().count()
            self._data_frame = self._data_frame[[dimension] + all_dimensions + all_measures]
            data = self._data_frame.rdd.map(lambda x: LabeledPoint(x[0], x[1:]))
            (trainingData, testData) = data.randomSplit([1.0, 0.0])
            # TO DO : set maxBins at least equal to the max level of categories in dimension column
            model = DecisionTree.trainClassifier(trainingData, numClasses=dimension_classes,categoricalFeaturesInfo=cat_feature_info, impurity='gini', maxDepth=6,maxBins=max_length)
            output_result = model.toDebugString()
        decision_tree = self.tree_json(output_result, self._data_frame, self._pandas_flag)
        self._new_tree = self.generate_new_tree(decision_tree)
        node_list = self.node_name_extractor(self._new_tree)
        node_list=list(self.flatten(node_list))
        correct_count_list=[i[0] for i in  self._count_list]
        tree_dict=dict(list(zip(node_list,correct_count_list)))
        #self._new_tree = self.generate_new_tree_total(decision_tree)
        self._new_tree = self.wrap_tree(self._new_tree,tree_dict)
        self._path_dict=self.path_dict_creator(node_list,self._new_tree)
        # self._new_tree = utils.recursiveRemoveNullNodes(self._new_tree)
        # decision_tree_result.set_params(self._new_tree, self._new_rules, self._total, self._success, self._probability)
        decision_tree_result.set_params(self._new_tree, self._new_rules, self._total, self._success, self._probability,self._path_dict)
        decision_tree_result.set_target_map(self._mapping_dict[self._target_dimension], self._aggr_data, self._important_vars)

        # self._completionStatus += self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["dtreeTrainingStart"]["weight"]/10
        # progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
        #                             "dtreeTrainingEnd",\
        #                             "info",\
        #                             self._scriptStages["dtreeTrainingEnd"]["summary"],\
        #                             self._completionStatus,\
        #                             self._completionStatus)
        # CommonUtils.save_progress_message(self._messageURL,progressMessage)
        # self._dataframe_context.update_completion_status(self._completionStatus)
        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._analysisName,"dtreeTrainingEnd","info",weightKey="script")

        # print decision_tree_result
        return decision_tree_result
