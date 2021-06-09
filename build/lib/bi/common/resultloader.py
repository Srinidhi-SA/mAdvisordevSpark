from __future__ import print_function
from builtins import object
from bi.common import utils as CommonUtils
import json

class ResultSetter(object):
    """
    Provides helper method to store all the different result and narratives.
    """

    def __init__(self, df_context):
        self.executiveSummaryDataDict = {}
        self.trend_subsection_name = None
        self.trend_subsection_data = None
        self.trend_subsection_complete = False
        self.model_summary = {}
        self.businessImpactNode = None
        self.distributionNode = None
        self.chisquareNode = None
        self.trendNode = None
        self.decisionTreeNode = {}
        self.score_dtree = {}
        self.regressionNode = None
        self.anovaNode = None
        self.headNode = None
        self.sparkMultilayerPerceptronModelSummary = None
        self.randomForestModelSummary = None
        self.sparkRandomForestModelSummary = None
        self.naiveBayesModelSummary = None
        self.df_context=df_context
        self.ensembleModelSummary=None
        self.xgboostModelSummary = None
        self.nnModelSummary = None
        self.tfModelSummary = None
        self.sparknaiveBayesModelSummary = None
        self.xgboostModelSummary = None
        self.sparkxgboostModelSummary = None
        self.logisticRegressionModelSummary = None
        self.sparklogisticRegressionModelSummary = None
        self.svmModelSummary = None
        self.nnptcModelSummary = None
        self.lgbmModelSummary=None
        self.adaboostModelSummary=None
        self.linearRegressionModelSummary = None
        self.generalizedLinearRegressionModelSummary = None
        self.gbtRegressionModelSummary = None
        self.dtreeRegressionModelSummary = None
        self.rfRegressionModelSummary = None
        self.tfRegressionModelSummary = None
        self.nnptrModelSummary = None
        self.sparkMultilayerPerceptronManagementSummary = None
        self.randomForestManagementSummary = None
        self.sparkRandomForestManagementSummary = None
        self.naiveBayesManagementSummary = None
        self.sparknaiveBayesManagementSummary = None
        self.xgboostManagementSummary = None
        self.sparkxgboostManagementSummary = None
        self.logisticRegressionManagementSummary = None
        self.sparklogisticRegressionManagementSummary = None
        self.svmManagementSummary = None

        self.mlpccards = []

        self.rfcards = []
        self.nbcards = []
        self.lrcards = []
        self.svmcards = []
        self.encards=[]
        self.xgbcards = []
        self.nncards = []
        self.tfcards = []
        self.nnptccards = []
        self.lgbmcards=[]
        self.adabcards=[]

        self.linrcards = []
        self.glinrcards = []
        self.gbtrcards = []
        self.rfrcards = []
        self.tfregcards = []
        self.nnptrcards = []
        self.dtreercards = []


        self.scorefreqcard = []
        self.scorechicards = []
        self.scoredtreecards = []

        self.rfnodes = []
        self.nnnodes = []
        self.tfnodes = []
        self.nbnodes = []
        self.ennodes = []
        self.xgbnodes = []
        self.lrnodes = []
        self.nnptcnodes = []
        self.lgbmnodes=[]
        self.adabnodes=[]

        self.stockAdvisorNode = None
        self.uidTable = None
        self.pmmlObjects = {}
        self.anovaCardsRegScore = []
        self.kpiCardScore = None
        self.hyperParameterResultDict = {}
        self.parallelCooridnateMetaData = {}
        self.hideTableColumns = []
        self.coeffCardScore = None
        self.anovaNarrativeOnScoredData = {}
        self.anovaChartOnScoredData = {}

        self.dtreenodes = []
        self.tfregnodes =[]
        self.gbtnodes = []
        self.lregnodes = []
        self.rfgnodes = []
        self.nnptrnodes = []

        self.rffailcard =[]
        self.lrfailcard = []
        self.nnfailcard = []
        self.tffailcard= []
        self.enfailcard=[]
        self.xgbfailcard = []
        self.nnptcfailcard = []
        self.nbfailcard = []

        self.dtrfailcard = []
        self.gbtfailcard = []
        self.tfregfailcard = []
        self.nnptrfailcard = []
        self.lgbmfailcard =[]
        self.adabfailcard=[]
    def set_dtr_fail_card(self,data):
        self.dtrfailcard=data
    def get_dtr_fail_card(self):
        return self.dtrfailcard
    def set_tfreg_fail_card(self,data):
        self.tfregfailcard=data
    def get_tfreg_fail_card(self):
        return self.tfregfailcard
    def set_gbt_fail_card(self,data):
        self.gbtfailcard=data
    def get_gbt_fail_card(self):
        return self.gbtfailcard
    def set_nnptr_fail_card(self,data):
        self.nnptrfailcard=data
    def get_nnptr_fail_card(self):
        return self.nnptrfailcard

    def set_lr_fail_card(self,data):
        self.lrfailcard=data
    def get_lr_fail_card(self):
        return self.lrfailcard
    def set_nn_fail_card(self,data):
        self.nnfailcard=data
    def get_nn_fail_card(self):
        return self.nnfailcard
    def set_nnptc_fail_card(self,data):
        self.nnptcfailcard=data
    def get_nnptc_fail_card(self):
        return self.nnptcfailcard
    def set_tf_fail_card(self,data):
        self.tffailcard=data
    def get_tf_fail_card(self):
        return self.tffailcard
    def set_en_fail_card(self,data):
        self.enfailcard=data
    def get_en_fail_card(self):
        return self.enfailcard

    def set_xgb_fail_card(self,data):
        self.xgbfailcard=data
    def get_xgb_fail_card(self):
        return self.xgbfailcard
    def set_nb_fail_card(self,data):
        self.nbfailcard=data
    def get_nb_fail_card(self):
        return self.nbfailcard
    def set_rf_fail_card(self,data):
        self.rffailcard=data
    def get_rf_fail_card(self):
        return self.rffailcard

    def set_lgbm_fail_card(self,data):
        self.lgbmfailcard=data
    def get_lgbm_fail_card(self):
        return self.lgbmfailcard

    def set_adab_fail_card(self,data):
        self.adabfailcard=data
    def get_adab_fail_card(self):
        return self.adabfailcard

    def set_dtree_nodes(self,data):
        self.dtreenodes = data
    def set_tfreg_nodes(self,data):
        self.tfregnodes = data
    def set_gbt_nodes(self,data):
        self.gbtnodes = data
    def set_lreg_nodes(self,data):
        self.lregnodes = data
    def set_rfreg_nodes(self,data):
        self.rfgnodes = data
    def set_nnptr_nodes(self,data):
        self.nnptrnodes = data

    def get_all_rfreg_regression_nodes(self):
        return self.rfgnodes
    def get_all_lreg_regression_nodes(self):
        return self.lregnodes
    def get_all_gbt_regression_nodes(self):
        return self.gbtnodes
    def get_all_dtree_regression_nodes(self):
        return self.dtreenodes
    def get_all_tfreg_regression_nodes(self):
        return self.tfregnodes
    def get_all_nnptr_regression_nodes(self):
        return self.nnptrnodes

    def set_rf_nodes(self,data):
        self.rfnodes = data
    def set_nn_nodes(self,data):
        self.nnnodes = data
    def set_tf_nodes(self,data):
        self.tfnodes = data
    def set_lr_nodes(self,data):
        self.lrnodes = data
    def set_nb_nodes(self,data):
        self.nbnodes = data
    def set_en_nodes(self,data):
        self.ennodes = data
    def set_xgb_nodes(self,data):
        self.xgbnodes = data
    def set_nnptc_nodes(self,data):
        self.nnptcnodes = data
    def set_lgbm_nodes(self,data):
        self.lgbmnodes = data
    def set_adab_nodes(self,data):
        self.adabnodes = data

    def get_all_rf_classification_nodes(self):
        return self.rfnodes
    def get_all_nn_classification_nodes(self):
        return self.nnnodes
    def get_all_tf_classification_nodes(self):
        return self.tfnodes
    def get_all_lr_classification_nodes(self):
        return self.lrnodes
    def get_all_xgb_classification_nodes(self):
        return self.xgbnodes
    def get_all_en_classification_nodes(self):
        return self.ennodes
    def get_all_lgbm_classification_nodes(self):
        return self.lgbmnodes
    def get_all_adab_classification_nodes(self):
        return self.adabnodes
    def get_all_nb_classification_nodes(self):
        return self.nbnodes
    def get_all_nnptc_classification_nodes(self):
        return self.nnptcnodes

    def set_anova_narrative_on_scored_data(self,dataDict):
        self.anovaNarrativeOnScoredData.update(dataDict)

    def set_anova_chart_on_scored_data(self,dataDict):
        self.anovaChartOnScoredData.update(dataDict)

    def get_anova_narratives_scored_data(self):
        return self.anovaNarrativeOnScoredData

    def get_anova_charts_scored_data(self):
        return self.anovaChartOnScoredData

    def set_metadata_parallel_coordinates(self,slug,data):
        self.parallelCooridnateMetaData[slug] = data

    def get_metadata_parallel_coordinates(self,slug):
        return self.parallelCooridnateMetaData[slug]

    def set_hyper_parameter_results(self,slug,data):
        self.hyperParameterResultDict[slug] = data
    def get_hyper_parameter_results(self,slug):
        return self.hyperParameterResultDict[slug]
    def update_pmml_object(self,data):
        self.pmmlObjects.update(data)
    def get_pmml_object(self):
        return self.pmmlObjects

    def get_score_cards(self):
        return self.scoredtreecards
    def set_score_dtree_cards(self,data,decisionTree):
        try:
            data[0]['decisionTree']=decisionTree
        except:
            pass
        self.scoredtreecards = data

        #self.scoredtreecards.append(decisionTree)
    # def set_score_dtree_cards_classifier(self,data,decisionTree,maxdepth):
    #     try:
    #         data[0]['decisionTree']=decisionTree
    #     except:
    #         pass
    #     self.score_dtree['maxdepth'+str(maxdepth)] = data
    #     if maxdepth == 5:
    #         dtree = []
    #         dtree.append(self.score_dtree)
    #         self.scoredtreecards = dtree
    def set_score_freq_card(self,data):
        self.scorefreqcard  = data
    def get_score_freq_card(self):
        return self.scorefreqcard
    def set_score_chi_cards(self,data):
        self.scorechicards = data
    def add_a_score_chi_card(self,data):
        self.scorechicards.append(data)
    def get_score_chi_cards(self):
        return self.scorechicards

    def set_lr_cards(self,data):
        self.lrcards = data
    def set_rf_cards(self,data):
        self.rfcards = data
    def set_nb_cards(self,data):
        self.nbcards = data
    def set_linr_cards(self,data):
        self.linrcards = data
    def set_glinr_cards(self,data):
        self.glinrcards = data
    def set_tfreg_cards(self,data):
        self.tfregcards = data
    def set_nnptr_cards(self,data):
        self.nnptrcards = data
    def set_gbtr_cards(self,data):
        self.gbtrcards = data
    def set_rfr_cards(self,data):
        self.rfrcards = data
    def set_dtreer_cards(self,data):
        self.dtreercards = data
    def set_en_cards(self,data):
        self.encards = data
    def set_xgb_cards(self,data):
        self.xgbcards = data
    def set_svm_cards(self,data):
        self.svmcards = data
    def set_nn_cards(self,data):
        self.nncards = data
    def set_tf_cards(self,data):
        self.tfcards = data
    def set_nnptc_cards(self,data):
        self.nnptccards = data
    def set_lgbm_cards(self,data):
        self.lgbmcards = data
    def set_adab_cards(self,data):
        self.adabcards = data
    def set_mlpc_cards(self,data):
        self.mlpccards = data

    def get_all_classification_cards(self):
        map_dict={'Naive Bayes':self.nbcards, 'Logistic Regression':self.lrcards, 'Neural Network (Sklearn)':self.nncards,'Ensemble':self.encards,'XGBoost':self.xgbcards,'LightGBM':self.lgbmcards,'Adaboost':self.adabcards, 'Random Forest':self.rfcards,'Neural Network (TensorFlow)':self.tfcards, "Neural Network (PyTorch)":self.nnptccards}
        all_cards=[]
        for i in self.model_order:
            all_cards=all_cards+map_dict[i]
        return all_cards

    def get_all_regression_cards(self):
        print(self.model_order)
        map_dict={'Linear Regression':self.linrcards, 'Gradient Boosted Tree Regression':self.gbtrcards, 'Decision Tree Regression':self.dtreercards, 'Random Forest Regression':self.rfrcards,'Neural Network (TensorFlow)':self.tfregcards, "Neural Network (PyTorch)":self.nnptrcards}
        all_cards=[]
        for i in self.model_order:
            all_cards=all_cards+map_dict[i]
        return all_cards
        #return self.linrcards+self.gbtrcards+self.dtreercards+self.rfrcards+self.glinrcards
    def set_tf_model_summary(self,data):
        self.tfModelSummary = data
    def set_nn_model_summary(self,data):
        self.nnModelSummary = data
    def set_random_forest_model_summary(self,data):
        self.randomForestModelSummary = data
    def set_spark_multilayer_perceptron_model_summary(self,data):
        self.sparkMultilayerPerceptronModelSummary = data
    def set_spark_random_forest_model_summary(self, data):
        self.sparkRandomForestModelSummary = data
    def set_spark_logistic_regression_model_summary(self, data):
        self.sparkLogisticRegressionModelSummary = data

    def set_naive_bayes_model_summary(self,data):
        self.naiveBayesModelSummary = data
    def set_spark_naive_bayes_model_summary(self,data):
        self.sparknaiveBayesModelSummary = data
    def set_xgboost_model_summary(self,data):
        self.xgboostModelSummary = data
    def set_spark_xgboost_model_summary(self,data):
        self.sparkxgboostModelSummary = data
    def set_logistic_regression_model_summary(self,data):
        self.logisticRegressionModelSummary = data
    def set_spark_logistic_regression_model_summary(self,data):
        self.sparklogisticRegressionModelSummary = data
    def set_spark_multilayer_perceptron_model_summary(self, data):
        self.sparkMultilayerPerceptronModelSummary = data
    def set_svm_model_summary(self,data):
        self.svmModelSummary = data
    def set_nnptc_model_summary(self,data):
        self.nnptcModelSummary = data
    def set_lgbm_model_summary(self,data):
        self.lgbmModelSummary =data
    def set_adaboost_model_summary(self,data):
        self.adaboostModelSummary =data
    def set_ensemble_model_summary(self,data):
        self.ensembleModelSummary =data
    def set_linear_regression_model_summary(self,data):
        self.linearRegressionModelSummary = data
    def set_generalized_linear_regression_model_summary(self,data):
        self.generalizedLinearRegressionModelSummary = data
    def set_gbt_regression_model_summart(self,data):
        self.gbtRegressionModelSummary = data
    def set_dtree_regression_model_summart(self,data):
        self.dtreeRegressionModelSummary = data
    def set_tfreg_regression_model_summart(self,data):
        self.tfRegressionModelSummary = data
    def set_rf_regression_model_summart(self,data):
        self.rfRegressionModelSummary = data
    def set_nnptr_regression_model_summary(self,data):
        self.nnptrModelSummary = data

    def get_random_forest_model_summary(self):
        return self.randomForestModelSummary
    def get_spark_logistic_regression_model_summary(self):
        return self.sparkLogisticRegressionModelSummary
    def get_spark_multilayer_perceptron_model_summary(self):
        return self.sparkMultilayerPerceptronModelSummary
    def get_spark_random_forest_model_summary(self):
        return self.sparkRandomForestModelSummary
    def get_naive_bayes_model_summary(self):
        return self.naiveBayesModelSummary
    def get_spark_naive_bayes_model_summary(self):
        return self.sparknaiveBayesModelSummary
    def get_xgboost_model_summary(self):
        return self.xgboostModelSummary
    def get_spark_xgboost_model_summary(self):
        return self.sparkxgboostModelSummary
    def get_logistic_regression_model_summary(self):
        return self.logisticRegressionModelSummary
    def get_spark_logistic_regression_model_summary(self):
        return self.sparklogisticRegressionModelSummary
    def get_spark_multilayer_perceptron_model_summary(self):
        return self.sparkMultilayerPerceptronModelSummary
    def get_svm_model_summary(self):
        return self.svmModelSummary
    def get_nn_model_summary(self):
        return self.nnModelSummary
    def get_tf_model_summary(self):
        return self.tfModelSummary
    def get_nnptc_model_summary(self):
        return self.nnptcModelSummary
    def get_lgbm_model_summary(self):
        return self.lgbmModelSummary
    def get_adaboost_model_summary(self):
        return self.adaboostModelSummary
    def get_ensemble_model_summary(self):
        return self.ensembleModelSummary

    def get_linear_regression_model_summary(self):
        return self.linearRegressionModelSummary
    def get_gbt_regression_model_summart(self):
        return self.gbtRegressionModelSummary
    def get_dtree_regression_model_summart(self):
        return self.dtreeRegressionModelSummary
    def get_rf_regression_model_summart(self):
        return self.rfRegressionModelSummary
    def get_generalized_linear_regression_model_summary(self):
        return self.generalizedLinearRegressionModelSummary
    def get_tfreg_regression_model_summart(self):
        return self.tfRegressionModelSummary
    def get_nnptr_regression_model_summary(self):
        return self.nnptrModelSummary

    def get_all_regression_model_summary(self):
        allRegressionModelSummary = [self.linearRegressionModelSummary,self.gbtRegressionModelSummary,self.dtreeRegressionModelSummary,self.rfRegressionModelSummary,self.generalizedLinearRegressionModelSummary,self.tfRegressionModelSummary,self.nnptrModelSummary]
        allRegressionModelSummary = [x for x in allRegressionModelSummary if x != None]
        return allRegressionModelSummary

    def set_head_node(self,node):
        self.headNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_trend_node(self,node):
        self.trendNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_chisquare_node(self,node):
        self.chisquareNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_distribution_node(self,node):
        self.distributionNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_decision_tree_node(self,node,decision_tree):
        self.decisionTreeNode = json.loads(CommonUtils.convert_python_object_to_json(node))
        self.decisionTreeNode['decisionTree']=decision_tree
    def set_decision_tree_node_classifier(self,node,decision_tree,maxdepth):
        self.decisionTreeNode["name"] = "Prediction"
        self.decisionTreeNode["slug"] = "prediction_maxdepth"
        self.decisionTreeNode['Depth Of Tree '+str(maxdepth)] = json.loads(CommonUtils.convert_python_object_to_json(node))
        self.decisionTreeNode['Depth Of Tree '+str(maxdepth)]['decisionTree'] = decision_tree
        self.decisionTreeNode['Depth Of Tree '+str(maxdepth)]["name"] = 'Depth Of Tree '+str(maxdepth)
        self.decisionTreeNode['Depth Of Tree '+str(maxdepth)]["slug"] = 'slug_maxdepth'+str(maxdepth)
    def set_anova_node(self,node):
        self.anovaNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_regression_node(self,node):
        self.regressionNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_business_impact_node(self,node):
        self.businessImpactNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def get_head_node(self):
        return self.headNode
    def get_trend_node(self):
        return self.trendNode
    def get_chisquare_node(self):
        return self.chisquareNode
    def get_distribution_node(self):
        return self.distributionNode
    def get_decision_tree_node(self):
        return self.decisionTreeNode
    def get_anova_node(self):
        return self.anovaNode
    def get_regression_node(self):
        return self.regressionNode
    def get_business_impact_node(self):
        return self.businessImpactNode

    def update_executive_summary_data(self,data_dict):
        if data_dict != None:
            self.executiveSummaryDataDict.update(data_dict)

    def get_executive_summary_data(self):
        return self.executiveSummaryDataDict

    def set_trend_section_name(self,name):
        self.trend_subsection_name = name

    def set_trend_section_completion_status(self,status):
        self.trend_subsection_complete = status

    def set_model_summary(self,data):
        """data will be a key value dictionary
        {"model_name":"model_summary"}
        """
        self.model_summary.update(data)

    def get_trend_section_name(self):
        return self.trend_subsection_name

    def set_trend_section_data(self,dataDict):
        self.trend_subsection_data = dataDict

    def get_trend_section_data(self):
        return self.trend_subsection_data

    def get_trend_section_completion_status(self):
        return self.trend_subsection_complete

    def get_model_summary(self):
        return self.model_summary

    def set_unique_identifier_table(self,data):
        self.uidTable = data

    def get_unique_identifier_table(self):
        return self.uidTable

    def get_kpi_card_regression_score(self):
        return self.kpiCardScore

    def set_kpi_card_regression_score(self,kpiCardScore):
        self.kpiCardScore = kpiCardScore

    def get_anova_cards_regression_score(self):
        return self.anovaCardsRegScore

    def set_anova_cards_regression_score(self,data):
        self.anovaCardsRegScore.append(data)

    def get_coeff_card_regression_score(self):
        return self.coeffCardScore

    def set_coeff_card_regression_score(self,coeffCardScore):
        self.coeffCardScore = coeffCardScore

    def set_random_forest_management_summary(self, data):
        self.randomForestManagementSummary = data

    def get_random_forest_management_summary(self):
        return self.randomForestManagementSummary

    def set_xgboost_management_summary(self, data):
        self.xgboostManagementSummary = data

    def get_xgboost_management_summary(self):
        return self.xgboostManagementSummary

    def set_logistic_regression_management_summary(self, data):
        self.logisticRegressionManagementSummary = data

    def get_logistic_regression_management_summary(self):
        return self.logisticRegressionManagementSummary

    def set_naive_bayes_management_summary(self, data):
        self.naiveBayesManagementSummary = data

    def get_naive_bayes_management_summary(self):
        return self.naiveBayesManagementSummary

    def set_svm_management_summary(self, data):
        self.svmManagementSummary = data

    def get_svm_management_summary(self):
        return self.svmManagementSummary

    def set_spark_random_forest_management_summary(self, data):
        self.sparkRandomForestManagementSummary = data

    def get_spark_random_forest_management_summary(self):
        return self.sparkRandomForestManagementSummary

    def set_spark_naive_bayes_management_summary(self, data):
        self.sparknaiveBayesManagementSummary = data

    def get_spark_naive_bayes_management_summary(self):
        return self.sparknaiveBayesManagementSummary

    def set_spark_logistic_regression_management_summary(self, data):
        self.sparklogisticRegressionManagementSummary = data

    def get_spark_logistic_regression_management_summary(self):
        return self.sparklogisticRegressionManagementSummary

    def set_spark_multilayer_perceptron_management_summary(self, data):
        self.sparkMultilayerPerceptronManagementSummary = data

    def get_spark_multilayer_perceptron_management_summary(self):
        return self.sparkMultilayerPerceptronManagementSummary

    def set_spark_xgboost_management_summary(self, data):
        self.sparkxgboostManagementSummary = data

    def get_spark_xgboost_management_summary(self):
        return self.sparkxgboostManagementSummary
