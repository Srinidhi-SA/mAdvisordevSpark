# -*- coding: utf-8 -*-
"""This module contains result object for DecisionTree test"""
from __future__ import print_function


from builtins import range
from builtins import object
class DecisionTreeResult(object):
    """
    Encapsulates results of DecisionTree test
    """

    def __init__(self):
        self.tree = {}

    def set_params(self, tree_result, rules, total, success, success_percent,path_dict):
        self.tree = tree_result
        try:
            self._table = {self.mappingdict[int(i)]:rules[i] for i in list(rules.keys())}
            self._total = {self.mappingdict[int(i)]:total[i] for i in list(total.keys())}
            self._success = {self.mappingdict[int(i)]:success[i] for i in list(success.keys())}
            self._success_percent = {self.mappingdict[int(i)]:success_percent[i] for i in list(success_percent.keys())}
        except:
            self._table = rules
            self._total = total
            self._success = success
            self._success_percent = success_percent

        self._path_dict=path_dict

    def set_target_map(self, target_map, target_agg, important_vars):
        self._target_map = target_map
        self._target_agg = target_agg
        print("set_target_map")
        print(target_agg)
        try:
            self._important_vars = {self.mappingdict[int(i)]:important_vars[i] for i in list(important_vars.keys())}
        except:
            self._important_vars = important_vars

    def set_freq_distribution(self, target_agg, important_vars):
        self._target_map = None
        print("set_freq_distribution")
        self._target_agg = target_agg
        print(target_agg)
        try:
            self._important_vars = {self.mappingdict[int(i)]:important_vars[i] for i in list(important_vars.keys())}
        except:
            self._important_vars = important_vars

    def get_significant_vars(self):
        return self._important_vars

    def get_target_map(self):
        return self._target_map

    def get_target_agg(self):
        return self._target_agg

    def get_target_contributions(self):
        if self._target_map==None:
            return self._target_agg
        print("get_target_contributions")
        print(dict([(self._target_map[i], self._target_agg[i]) for i in range(3)]))
        print(self._target_map)
        return dict([(self._target_map[i], self._target_agg[i]) for i in range(3)])

    def get_decision_rules(self):
        return self.tree

    def get_table(self):
        return self._table

    def get_total(self):
        return self._total

    def get_success(self):
        return self._success

    def get_success_percent(self):
        return self._success_percent

    def get_path_dict(self):
        return self._path_dict
