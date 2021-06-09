from __future__ import print_function
from builtins import str
from builtins import object
import time
import re
import pandas as pd
from sklearn import metrics
from math import sqrt
try:
    from sklearn.externals import joblib
except:
    import joblib
from bi.settings import setting as GLOBALSETTINGS
from bi.common import utils as CommonUtils
from sklearn.model_selection import KFold,StratifiedKFold,StratifiedShuffleSplit
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')

import lightgbm as lgb
import numpy as np

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.mllib.evaluation import BinaryClassificationMetrics, MulticlassMetrics
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf
from pyspark.sql.types import *

class ModelSummary(object):
    """
    modelJsonOutput = {
                        "model_summary":modelResult,
                        "model_dropdown":[
                                    {"name":"Random Forest","accuracy":89,"slug":"djksjkdsjdsk12NN2156"},
                                    {"name":"Logistic Regression","accuracy":86,"slug":"djk18jjsjdsk12NN2156"},
                                    {"name":"Xgboost","accuracy":80,"slug":"djkjkd77661sk12NN2156"}
                        ],
                        "config":{
                            "target_variable":[None],
                            "targetVariableLevelcount":[],
                            "modelFeatures":{
                                "slug1":[],
                                "slug2":[],
                                "slug3":[],
                            }
                        }
                    }
    """
    def __init__(self, model_summary=None, model_dropdown=None, modelConfig=None, modelHyperparameter=None, model_management_summary=None):
        if model_summary is None:
            model_summary = {}
        if model_dropdown is None:
            model_dropdown = []
        if modelConfig is None:
            modelConfig = {}
        if model_management_summary is None:
            model_management_summary = []
        self.model_summary = model_summary
        self.model_dropdown = model_dropdown
        self.config = modelConfig
        self.model_hyperparameter_summary = modelHyperparameter
        self.modelSelectedByUser = False
        self.model_management_summary = model_management_summary

    def set_model_summary(self, data):
        self.model_summary = data

    def get_model_summary(self):
        return self.model_summary

    def set_model_dropdown(self, data):
        self.model_dropdown = data

    def get_model_dropdown(self):
        return self.model_dropdown

    def set_model_config(self, data):
        self.config = data

    def get_model_config(self):
        return self.config

    def get_model_hyperparameter_summary(self):
        return self.model_hyperparameter_summary

    def set_model_hyperparameter_summary(self, data):
        self.model_hyperparameter_summary = data
    def get_model_management_summary(self):
        return self.model_management_summary
    def set_model_management_summary(self, data):
        self.model_management_summary = data
    def get_json_data(self):
        output =  {
                "model_summary":self.model_summary,
                "model_dropdown":self.model_dropdown,
                "config":self.config,
                "model_hyperparameter":self.model_hyperparameter_summary,
                "modelSelected":self.modelSelectedByUser,
                "model_management_summary": self.model_management_summary
                }
        return output

class MLModelSummary(object):
    def __init__(self):
        self.confusionMatrix = None
        self.featureImportance = None
        self.featureList = None
        self.trainingTime = None
        self.precisionRecallStats = None
        self.modelAccuracy = None
        self.modelPrecision = None
        self.modelRecall = None
        self.targetVariable = None
        self.predictionSplit = None
        self.algorithmName = None
        self.algorithmDisplayName = None
        self.validationMethod = None
        self.hyperParamAlgoName = None
        self.modelFeatures = None
        self.levelCounts = None
        self.nTrees = None
        self.nRules = None
        self.slug = None
        self.levelMap = None
        self.modelParams = None
        self.modelEvaluationMetrics = None
        self.modelType = None  # can be "regression", or "classification"
        self.quantileSummary = None
        self.mapeStats = None
        self.sampleData = None
        self.coefficinetsArray = []
        self.interceptValue = None
        self.gain_lift_KS_data = None
        self.modelAUC = None
        self.fitIntercept = None
        self.warmStart = None
        self.trainingStatus = None
        self.jobType = None
        self.noOfIndependentVariables = None
        self.creationDate = None
        self.maximumSolver = None
        self.inverseRegularizationStrength = None
        self.convergenceTolerenceIteration = None
        self.multiClassOption = None
        self.criterion = None
        self.maxDepth = None
        self.minInstanceForSplit = None
        self.minInstanceForLeafNode = None
        self.maxLeafNodes = None
        self.impurityDecreaseCutoffForSplit = None
        self.noOfEstimators = None
        self.bootstrapSampling = None
        self.noOfJobs = None
        self.alpha = None
        self.boosterFunction = None
        self.learningRate = None
        self.minimumLossReduction = None
        self.minimumChildWeight = None
        self.subsamplingRatio = None
        self.subsampleForEachTree = None
        self.subsampleForEachSplit = None
        self.targetLevel = None
        self.priors = None
        self.varSmoothing = None
        self.datasetName = None
        self.mse = None
        self.rsquared = None
        self.mae = None
        self.rmse = None
        self.splitter = None
        self.loss_function = None
        self.normalizeValue = None
        self.copyX = None
        self.exp_var_score = None
        self.layer_info=[]
        self.optimizer=None
        self.aggregation_depth=None
        self.standardization=None
        self.threshold=None
        self.maxBins = None
        self.minInstancesPerNode = None
        self.minInfoGain = None
        self.cacheNodeIds = None
        self.checkpointInterval = None
        self.impurity = None
        self.numTrees = None
        self.featureSubsetStrategy = None
        self.subsamplingRate = None

    def set_max_bins(self,data):
        self.maxBins = data
    def get_max_bins(self):
        return self.maxBins
    def set_min_instances_per_node(self,data):
        self.minInstancesPerNode = data
    def get_min_instances_per_node(self):
        return self.minInstancesPerNode
    def set_min_info_gain(self,data):
        self.minInfoGain = data
    def get_min_info_gain(self):
        return self.minInfoGain
    def set_cacheNodeIds(self,data):
        self.cacheNodeIds = data
    def get_cacheNodeIds(self):
        return self.cacheNodeIds
    def set_checkpoint_interval(self,data):
        self.checkpointInterval = data
    def get_checkpoint_interval(self):
        return self.checkpointInterval
    def set_impurity(self,data):
        self.impurity = data
    def get_impurity(self):
        return self.impurity
    def set_num_of_trees(self,data):
        self.numTrees = data
    def get_num_of_trees(self):
        return self.numTrees
    def set_feature_subset_strategy(self,data):
        self.featureSubsetStrategy = data
    def get_feature_subset_strategy(self):
        return self.featureSubsetStrategy
    def set_subsampling_rate(self,data):
        self.subsamplingRate = data
    def get_subsampling_rate(self):
        return self.subsamplingRate
    def set_elasticNetParam(self,data):
        self.elasticNetParam=data
    def get_elasticNetParam(self):
        return self.elasticNetParam
    def set_aggregationDepth(self,data):
        self.aggregation_depth=data
    def get_aggregationDepth(self):
        return self.aggregation_depth
    def set_standardization(self,data):
        self.standardization=data
    def get_standardization(self):
        return self.standardization
    def set_threshold(self,data):
        self.threshold=data
    def get_threshold(self):
        return self.threshold
    def set_layer_info(self,data):
        self.layer_info=data
    def get_layer_info(self):
        return self.layer_info
    def set_optimizer(self,data):
        self.optimizer=data
    def get_optimizer(self):
        return self.optimizer
    def set_no_epochs(self,data):
        self.epochs=data
    def get_no_epochs(self):
        return self.epochs

    def set_epsilon(self,data):
        self.epsilon =data

    def get_epsilon(self):
        return self.epsilon

    def set_activation(self,data):
        self.activation = data

    def get_activation(self):
        return self.activation

    def set_batch_size(self,data):
        self.batch_size=data
    def get_batch_size(self):
        return self.batch_size
    def set_early_stopping(self,data):
        self.early_stopping = data
    def get_early_stopping(self):
        return self.early_stopping
    def set_beta_1(self,data):
        self.beta1= data
    def get_beta_1(self):
        return self.beta1
    def set_beta_2(self,data):
        self.beta1= data
    def get_beta_2(self):
        return self.beta1
    def set_nesterovs_momentum(self,data):
        self.nesterovs_momentum=data
    def get_nesterovs_momentum(self):
        return self.nesterovs_momentum
    def set_hidden_layer_sizes(self,data):
        self.hidden_layer_sizes=data
    def get_hidden_layer_sizes(self):
        return self.hidden_layer_sizes
    def set_power_t(self,data):
        self.power_t=data
    def get_power_t(self):
        return self.power_t
    def set_learning_rate_init(self,data):
        self.learning_rate_init=data
    def get_learning_rate_init(self):
        return self.learning_rate_init
    def set_shuffle(self,data):
        self.shuffle=data
    def get_shuffle(self):
        return self.shuffle
    def set_verbose(self,data):
        self.verbose=data
    def get_verbose(self):
        return self.verbose
    def set_random_state(self,data):
        self.random_state= data
    def get_random_state(self):
        return self.random_state
    def set_n_iter_no_change(self,data):
        self.n_iter_no_change=data
    def get_n_iter_no_change(self):
        return self.n_iter_no_change
    def set_learning_rate(self,data):
        self.learning_rate=data
    def get_learning_rate(self):
        return self.learning_rate
    def set_validation_fraction(self,data):
        self.validation_fraction= data
    def get_validation_fraction(self):
        return self.validation_fraction
    def set_momentum(self,data):
        self.momentum=data
    def get_momentum(self):
        return self.momentum

    def set_normalize_value(self,data):
        self.normalizeValue = data

    def get_normalize_value(self):
         return self.normalizeValue

    def set_copy_x(self,data):
        self.copyX = data

    def get_copy_x(self):
        return self.copyX

    def set_model_mse(self,data):
        self.mse = round(data,3)

    def get_model_mse(self):
        return self.mse

    def set_model_rsquared(self,data):
        self.rsquared = round(data,3)

    def get_model_rsquared(self):
        return self.rsquared

    def set_model_mae(self,data):
        self.mae = round(data,3)

    def get_model_mae(self):
        return self.mae

    def set_rmse(self,data):
        self.rmse = round(data,3)

    def get_rmse(self):
        return self.rmse

    def set_splitter(self,data):
        self.splitter=data

    def get_splitter(self):
        return self.splitter

    def set_loss_function(self,data):
        self.loss_function = data

    def get_loss_function(self):
        return self.loss_function

    def set_model_exp_variance_score(self,data):
        self.exp_var_score = round(data,3)

    def get_model_exp_variance_score(self):
        return self.exp_var_score

    def set_datasetName(self,data):
        self.datasetName = data
    def get_datasetName(self):
        return self.datasetName
    def set_priors(self,data):
        self.priors = data
    def get_priors(self):
        return self.priors
    def set_var_smoothing(self,data):
        self.varSmoothing = data
    def get_var_smoothing(self):
        return self.varSmoothing
    def set_model_F1_score(self,data):
        self.F1_score = round(data,3)

    def get_model_F1_score(self):
        return self.F1_score

    def set_model_log_loss(self,data):
        self.log_loss = round(data,3)

    def get_model_log_loss(self):
        return self.log_loss


    def set_AUC_score(self,data):
        self.modelAUC =  round(data,3)

    def get_AUC_score(self):
        return self.modelAUC

    def set_gain_lift_KS_data(self,data):
        self.gain_lift_KS_data = data

    def get_gain_lift_KS_data(self):
        return self.gain_lift_KS_data

    def set_fit_intercept(self,data):
        self.fitIntercept = data

    def get_fit_intercept(self):
        return self.fitIntercept

    def set_warm_start(self,data):
        self.warmStart = data

    def get_warm_start(self):
        return self.warmStart

    def set_training_status(self,data):
        self.trainingStatus = data

    def get_training_status(self):
        return self.trainingStatus

    def set_job_type(self,data):
        self.jobType = data

    def get_job_type(self):
        return self.jobType

    def set_no_of_independent_variables(self,data):
        self.noOfIndependentVariables = len(data.columns)

    def get_no_of_independent_variables(self):
        return self.noOfIndependentVariables

    def set_creation_date(self,data):
        self.creationDate = data

    def get_creation_date(self):
        return self.creationDate

    def set_maximum_solver(self,data):
        self.maximumSolver = data

    def get_maximum_solver(self):
        return self.maximumSolver

    def set_inverse_regularization_strength(self,data):
        self.inverseRegularizationStrength = data

    def get_inverse_regularization_strength(self):
        return self.inverseRegularizationStrength

    def set_convergence_tolerence_iteration(self,data):
        self.convergenceTolerenceIteration = data

    def get_convergence_tolerence_iteration(self):
        return self.convergenceTolerenceIteration

    def set_solver_used(self,data):
        self.solverUsed = data

    def get_solver_used(self):
        return self.solverUsed

    def set_multiclass_option(self,data):
        self.multiClassOption = data

    def get_multiclass_option(self):
        return self.multiClassOption
    def set_criterion(self,data):
        self.criterion = data
    def get_criterion(self):
        return self.criterion
    def set_max_depth(self,data):
        self.maxDepth = data
    def get_max_depth(self):
        return self.maxDepth
    def set_min_instance_for_split(self,data):
        self.minInstanceForSplit = data
    def get_min_instance_for_split(self):
        return self.minInstanceForSplit
    def set_min_instance_for_leaf_node(self,data):
        self.minInstanceForLeafNode = data
    def get_min_instance_for_leaf_node(self):
        return self.minInstanceForLeafNode
    def set_max_leaf_nodes(self,data):
        self.maxLeafNodes = data
    def get_max_leaf_nodes(self):
        return self.maxLeafNodes
    def set_impurity_decrease_cutoff_for_split(self,data):
        self.impurityDecreaseCutoffForSplit = data
    def get_impurity_decrease_cutoff_for_split(self):
        return self.impurityDecreaseCutoffForSplit
    def set_no_of_estimators(self,data):
        self.noOfEstimators = data
    def get_no_of_estimators(self):
        return self.noOfEstimators
    def set_bootstrap_sampling(self,data):
        self.bootstrapSampling = data
    def get_bootstrap_sampling(self):
        return self.bootstrapSampling
    def set_no_of_jobs(self,data):
        self.noOfJobs = data
    def get_no_of_jobs(self):
        return self.noOfJobs
    def set_alpha(self,data):
        self.alpha = data
    def get_alpha(self):
        return self.alpha
    def set_l1_ratio(self,data):
        self.l1Ratio = data
    def get_l1_ratio(self):
        return self.l1Ratio
    def set_booster_function(self,data):
        self.boosterFunction = data
    def get_booster_function(self):
        return self.boosterFunction
    def set_learning_rate(self,data):
        self.learningRate = data
    def get_learning_rate(self):
        return self.learningRate
    def set_minimum_loss_reduction(self,data):
        self.minimumLossReduction = data
    def get_minimum_loss_reduction(self):
        return self.minimumLossReduction
    def set_minimum_child_weight(self,data):
        self.minimumChildWeight = data
    def get_minimum_child_weight(self):
        return self.minimumChildWeight
    def set_subsampling_ratio(self,data):
        self.subsamplingRatio = data
    def get_subsampling_ratio(self):
        return self.subsamplingRatio
    def set_subsample_for_each_tree(self,data):
        self.subsampleForEachTree = data
    def get_subsample_for_each_tree(self):
        return self.subsampleForEachTree
    def set_subsample_for_each_split(self,data):
        self.subsampleForEachSplit = data
    def get_subsample_for_each_split(self):
        return self.subsampleForEachSplit

    def set_intercept(self, data):
        self.interceptValue = data

    def get_intercept(self):
        return self.interceptValue

    def set_coefficinets_array(self, data):
        self.coefficinetsArray = data

    def get_coefficinets_array(self):
        return self.coefficinetsArray

    def set_sample_data(self, data):
        self.sampleData = data

    def get_sample_data(self):
        return self.sampleData

    def set_mape_stats(self, data):
        self.mapeStats = data

    def get_mape_stats(self):
        return self.mapeStats

    def set_quantile_summary(self, data):
        self.quantileSummary = data

    def get_quantile_summary(self):
        return self.quantileSummary

    def set_model_type(self, data):
        self.modelType = data

    def get_model_type(self):
        return self.modelType

    def set_model_evaluation_metrics(self, data):
        self.modelEvaluationMetrics = data

    def get_model_evaluation_metrics(self):
        return self.modelEvaluationMetrics

    def set_model_params(self, data):
        self.modelParams = data

    def get_model_params(self):
        return self.modelParams

    def set_level_map_dict(self, data):
        self.levelMap = data

    def get_level_map_dict(self):
        return self.levelMap

    def set_confusion_matrix(self, data):
        self.confusionMatrix = data

    def set_feature_importance(self, data):
        self.featureImportance = data

    def set_feature_list(self, data):
        self.featureList = data

    def set_training_time(self, data):
        self.trainingTime = data

    def set_precision_recall_stats(self, data):
        self.precisionRecallStats = data

    def set_model_accuracy(self,data):
        self.modelAccuracy = round(data,3)

    def set_model_precision(self,data):
        self.modelPrecision = round(data,3)

    def set_model_recall(self,data):
        self.modelRecall = round(data,3)

    def set_target_variable(self, data):
        self.targetVariable = data

    def set_prediction_split(self, data):
        self.predictionSplit = data

    def set_algorithm_name(self, data):
        self.algorithmName = data

    def set_algorithm_display_name(self, data):
        self.algorithmDisplayName = data

    def set_validation_method(self, data):
        self.validationMethod = data

    def set_hyperParamAlgoName(self,data):
        self.hyperParamAlgoName = data

    def set_model_features(self, data):
        self.modelFeatures = data

    def set_level_counts(self, data):
        self.levelCounts = data

    def set_num_trees(self, data):
        self.nTrees = data

    def set_num_rules(self, data):
        self.nRules = data

    def set_target_level(self, data):
        self.targetLevel = data

    def set_slug(self, data):
        self.slug = data

    def get_hyperParamAlgoName(self):
        return self.hyperParamAlgoName

    def get_confusion_matrix(self):
        return self.confusionMatrix

    def get_feature_importance(self):
        return self.featureImportance

    def get_feature_list(self):
        return self.featureList

    def get_training_time(self):
        return self.trainingTime

    def get_precision_recall_stats(self):
        return self.precisionRecallStats

    def get_model_accuracy(self):
        return self.modelAccuracy

    def get_model_precision(self):
        return self.modelPrecision

    def get_model_recall(self):
        return self.modelRecall

    def get_target_variable(self):
        return self.targetVariable

    def get_target_level(self):
        return self.targetLevel

    def get_prediction_split(self):
        return self.predictionSplit

    def get_algorithm_name(self):
        return self.algorithmName

    def get_algorithm_display_name(self):
        return self.algorithmDisplayName

    def get_validation_method(self):
        return self.validationMethod

    def get_model_features(self):
        return self.modelFeatures

    def get_level_counts(self):
        return self.levelCounts

    def get_num_trees(self):
        return self.nTrees

    def get_num_rules(self):
        return self.nRules

    def get_slug(self):
        return self.slug


class MLModelMetaData(object):
    """
    This module contains Meta Data for a corresponding ML Model
    """

    def __init__(self):
        self.algorithmName = None
        self.modelType = None  # ensemble or single model
        self.trainingTime = None
        self.packageUsed = None
        self.packageVersion = None


class ParamsGrid(object):
    """

    """
class PySparkGridSearchResult(object):
    def __init__(self, estimator=None, paramGrid=None, appType=None,
                 modelFilepath=None, levels=None, evaluationMetricDict=None,
                 trainingData=None, validationData=None, numFolds=None, targetLevel=None,
                 labelMapping=None, inverseLabelMapping=None, df=None, categorical_columns=None,
                 numerical_columns=None):
        self.estimator = estimator
        self.paramGrid = paramGrid
        self.appType = appType
        self.levels = levels
        self.evaluationMetricDict = evaluationMetricDict
        self.modelFilepath = modelFilepath
        self.trainingData = trainingData
        self.validationData = validationData
        self.numFolds = numFolds
        self.targetLevel = targetLevel
        self.labelMapping = labelMapping
        self.inverseLabelMapping = inverseLabelMapping
        self.df = df
        self.categorical_columns = categorical_columns
        self.numerical_columns = numerical_columns
        self.ignoreList = ["Model Id", "Precision", "Recall", "ROC-AUC", "RMSE", "MAE", "MSE", "R-Squared", "Slug",
                           "Selected", "Run Time(Secs)", "comparisonMetricUsed", "algorithmName", "alwaysSelected"]
        self.hideFromTable = ["Selected", "alwaysSelected", "Slug", "comparisonMetricUsed", "algorithmName"]
        self.metricColName = "comparisonMetricUsed"
        self.keepColumns = ["Model Id"]
        self.bestModel = None
        self.bestPrediction = None

    def get_ignore_list(self):
        return self.ignoreList

    def get_hide_columns(self):
        return self.hideFromTable

    def get_comparison_metric_colname(self):
        return self.metricColName

    def get_keep_columns(self):
        return self.keepColumns

    def train_and_save_classification_models(self):
        tableOutput = []
        evaluationMetric = self.evaluationMetricDict["name"]
        evaluationMetricVal = -1
        for idx, params in enumerate(self.paramGrid):
            st = time.time()
            crossval = CrossValidator(estimator=self.estimator,
                                      estimatorParamMaps=[params],
                                      evaluator=BinaryClassificationEvaluator() if self.levels == 2 else MulticlassClassificationEvaluator(),
                                      numFolds=3 if self.numFolds is None else self.numFolds)  # use 3+ folds in practice

            modelName = "M" + "0" * (GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH - len(str(idx + 1))) + str(idx + 1)
            cvrf = crossval.fit(self.trainingData)

            prediction = cvrf.transform(self.validationData)
            predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
            metrics = MulticlassMetrics(predsAndLabels)

            trainingTime = time.time() - st
            precision = metrics.precision()
            recall = metrics.recall()
            accuracy = metrics.accuracy
            roc_auc = 'NA'
            if self.levels == 2:
                bin_metrics = BinaryClassificationMetrics(predsAndLabels)
                roc_auc = bin_metrics.areaUnderROC
                precision = metrics.precision(self.inverseLabelMapping[self.targetLevel])
                recall = metrics.recall(self.inverseLabelMapping[self.targetLevel])

            # finding out the best model
            metrics = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'roc_auc': roc_auc}
            if metrics[evaluationMetric] > evaluationMetricVal:
                self.bestModel = cvrf.bestModel
                self.bestPrediction = prediction
                evaluationMetricVal = metrics[evaluationMetric]

            # Save model
            slug = self.modelFilepath.split("/")[-1]
            algoName = GLOBALSETTINGS.SLUG_MODEL_DISPLAY_NAME_MAPPING[slug]
            cvrf.bestModel.save(self.modelFilepath + "/" + modelName)

            # Create table output row
            row = {"Model Id": modelName, "Slug": slug, "Selected": "False", "alwaysSelected": "False",
                   "Run Time(Secs)": CommonUtils.round_sig(time.time() - st), "comparisonMetricUsed": None,
                   "algorithmName": algoName}

            # Algorithm evaluation metrics
            algoEvaluationMetrics = {}
            algoEvaluationMetrics["Accuracy"] = accuracy
            row["comparisonMetricUsed"] = self.evaluationMetricDict["displayName"]
            algoEvaluationMetrics["Precision"] = precision
            algoEvaluationMetrics["Recall"] = recall
            algoEvaluationMetrics["ROC-AUC"] = roc_auc

            algoEvaluationMetrics = {k: CommonUtils.round_sig(v) for k, v in algoEvaluationMetrics.items()}
            row.update(algoEvaluationMetrics)
            paramsObj = dict(
                [(k.name, str(v)) if (v == None) | (v in [True, False]) else (k.name, v) for k, v in params.items()])
            row.update(paramsObj)
            tableOutput.append(row)
            if (self.levels > 2) & (self.evaluationMetricDict["name"] == "roc_auc"):
                defaultComparisonMetric = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[
                    GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC]
                tableOutput = sorted(tableOutput, key=lambda x: float(x[defaultComparisonMetric]), reverse=True)
            else:
                tableOutput = sorted(tableOutput, key=lambda x: float(x[tableOutput[0]["comparisonMetricUsed"]]),
                                     reverse=True)
        self.keepColumns += ["Accuracy", "Precision", "Recall", "ROC-AUC"]
        self.keepColumns += [k.name for k in params.keys()]
        self.keepColumns.append("Selected")
        bestMod = tableOutput[0]
        bestMod["Selected"] = "True"
        bestMod["alwaysSelected"] = "True"
        tableOutput[0] = bestMod
        return tableOutput

    def getBestModel(self):
        return self.bestModel

    def getBestPrediction(self):
        return self.bestPrediction


class PySparkTrainTestResult(object):
    def __init__(self, estimator=None, paramGrid=None, appType=None,
                 modelFilepath=None, levels=None, evaluationMetricDict=None,
                 trainingData=None, validationData=None, train_test_ratio=None, targetLevel=None,
                 labelMapping=None, inverseLabelMapping=None, df=None):
        self.estimator = estimator
        self.paramGrid = paramGrid
        self.levels = levels
        self.evaluationMetricDict = evaluationMetricDict
        self.modelFilepath = modelFilepath
        self.trainingData = trainingData
        self.validationData = validationData
        self.train_test_ratio = train_test_ratio
        self.targetLevel = targetLevel
        self.labelMapping = labelMapping
        self.inverseLabelMapping = inverseLabelMapping
        self.df = df
        self.ignoreList = ["Model Id", "Precision", "Recall", "ROC-AUC", "RMSE", "MAE", "MSE", "R-Squared", "Slug",
                           "Selected", "Run Time(Secs)", "comparisonMetricUsed", "algorithmName", "alwaysSelected"]
        self.hideFromTable = ["Selected", "alwaysSelected", "Slug", "comparisonMetricUsed", "algorithmName"]
        self.metricColName = "comparisonMetricUsed"
        self.keepColumns = ["Model Id"]
        self.bestModel = None
        self.bestPrediction = None

    def get_ignore_list(self):
        return self.ignoreList

    def get_hide_columns(self):
        return self.hideFromTable

    def get_comparison_metric_colname(self):
        return self.metricColName

    def get_keep_columns(self):
        return self.keepColumns

    def train_and_save_classification_models(self):
        tableOutput = []
        evaluationMetric = self.evaluationMetricDict["name"]
        evaluationMetricVal = -1
        for idx, params in enumerate(self.paramGrid):
            st = time.time()
            tvs = TrainValidationSplit(estimator=self.estimator,
                                       estimatorParamMaps=[params],
                                       evaluator=BinaryClassificationEvaluator() if self.levels == 2 else MulticlassClassificationEvaluator(),
                                       trainRatio=self.train_test_ratio)

            modelName = "M" + "0" * (GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH - len(str(idx + 1))) + str(idx + 1)
            cvrf = tvs.fit(self.trainingData)

            prediction = cvrf.transform(self.validationData)
            predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
            metrics = MulticlassMetrics(predsAndLabels)

            trainingTime = time.time() - st
            precision = metrics.precision()
            recall = metrics.recall()
            accuracy = metrics.accuracy
            roc_auc = 'NA'
            if self.levels == 2:
                bin_metrics = BinaryClassificationMetrics(predsAndLabels)
                roc_auc = bin_metrics.areaUnderROC
                precision = metrics.precision(self.inverseLabelMapping[self.targetLevel])
                recall = metrics.recall(self.inverseLabelMapping[self.targetLevel])

            # finding out the best model
            metrics = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'roc_auc': roc_auc}
            if metrics[evaluationMetric] > evaluationMetricVal:
                self.bestModel = cvrf.bestModel
                self.bestPrediction = prediction
                evaluationMetricVal = metrics[evaluationMetric]

            # Save model
            slug = self.modelFilepath.split("/")[-1]
            algoName = GLOBALSETTINGS.SLUG_MODEL_DISPLAY_NAME_MAPPING[slug]
            cvrf.bestModel.save(self.modelFilepath + "/" + modelName)

            # Create table output row
            row = {"Model Id": modelName, "Slug": slug, "Selected": "False", "alwaysSelected": "False",
                   "Run Time(Secs)": CommonUtils.round_sig(time.time() - st), "comparisonMetricUsed": None,
                   "algorithmName": algoName}

            # Algorithm evaluation metrics
            algoEvaluationMetrics = {}
            algoEvaluationMetrics["Accuracy"] = accuracy
            row["comparisonMetricUsed"] = self.evaluationMetricDict["displayName"]
            algoEvaluationMetrics["Precision"] = precision
            algoEvaluationMetrics["Recall"] = recall
            algoEvaluationMetrics["ROC-AUC"] = roc_auc

            algoEvaluationMetrics = {k: CommonUtils.round_sig(v) for k, v in algoEvaluationMetrics.items()}
            row.update(algoEvaluationMetrics)
            paramsObj = dict(
                [(k.name, str(v)) if (v == None) | (v in [True, False]) else (k.name, v) for k, v in params.items()])
            row.update(paramsObj)
            tableOutput.append(row)
            if (self.levels > 2) & (self.evaluationMetricDict["name"] == "roc_auc"):
                defaultComparisonMetric = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[
                    GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC]
                tableOutput = sorted(tableOutput, key=lambda x: float(x[defaultComparisonMetric]), reverse=True)
            else:
                tableOutput = sorted(tableOutput, key=lambda x: float(x[tableOutput[0]["comparisonMetricUsed"]]),
                                     reverse=True)
        self.keepColumns += ["Accuracy", "Precision", "Recall", "ROC-AUC"]
        self.keepColumns += [k.name for k in params.keys()]
        self.keepColumns.append("Selected")
        bestMod = tableOutput[0]
        bestMod["Selected"] = "True"
        bestMod["alwaysSelected"] = "True"
        tableOutput[0] = bestMod
        return tableOutput

    def getBestModel(self):
        return self.bestModel

    def getBestPrediction(self):
        return self.bestPrediction

class SklearnGridSearchResult(object):
    def __init__(self,resultDict = {},estimator=None,x_train=None,x_test=None,y_train=None,y_test=None,appType=None,modelFilepath = None,levels=None,posLabel=None,evaluationMetricDict=None):
        self.resultDict = resultDict
        self.estimator = estimator
        self.appType = appType
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.posLabel = posLabel
        self.levels = levels
        self.evaluationMetricDict = evaluationMetricDict
        self.modelFilepath = modelFilepath
        if self.resultDict != {}:
            self.resultDf = pd.DataFrame(self.resultDict)
        else:
            self.resultDf = None
        self.ignoreList = ["Model Id","Precision","Recall","ROC-AUC","RMSE","MAE","MSE","R-Squared","Slug","Selected","Run Time(Secs)","comparisonMetricUsed","algorithmName","alwaysSelected","explained_variance_score"]
        self.hideFromTable = ["Selected","alwaysSelected","Slug","comparisonMetricUsed","algorithmName","explained_variance_score"]
        self.metricColName = "comparisonMetricUsed"
        self.keepColumns = ["Model Id"]
        self.bestModel = None
        self.bestParam = None

    def get_ignore_list(self):
        return self.ignoreList

    def get_hide_columns(self):
        return self.hideFromTable

    def get_comparison_metric_colname(self):
        return self.metricColName

    def get_keep_columns(self):
        return self.keepColumns

    def train_and_save_models(self):
        tableOutput = []
        evaluationMetric = self.evaluationMetricDict["name"].capitalize()
        if evaluationMetric == "Roc_auc":
            evaluationMetric = "ROC-AUC"
        if evaluationMetric == "R2":
            evaluationMetric = "R-Squared"
        if evaluationMetric == "Neg_mean_absolute_error":
            evaluationMetric = "MAE"
        if evaluationMetric == "Neg_mean_squared_error":
            evaluationMetric = "MSE"
        if  evaluationMetric == "Rmse":
            evaluationMetric = "RMSE"

        if evaluationMetric in ["MSE","RMSE","MAE"]:
            initial = True
        else:
            evalMetricVal = -1
        for idx,paramsObj in enumerate(self.resultDf["params"]):
            st = time.time()
            estimator = self.estimator.set_params(**paramsObj)
            estimator.fit(self.x_train, self.y_train)
            estimator.feature_names = list(self.x_train.columns.values)
            y_score = estimator.predict(self.x_test)
            train_score = estimator.predict(self.x_train)
            try:
                y_prob = estimator.predict_proba(self.x_test)
            except:
                y_prob = [0]*len(y_score)
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-len(str(idx+1)))+str(idx+1)

            print("#"*100)
            print("Feature Importance ",modelName)
            # try:
            #     print(estimator.feature_importances_)
            # except:
            #     print("Feature Importance Not Defined")

            print("#"*100)
            slug = self.modelFilepath.split("/")[-1]
            algoName = GLOBALSETTINGS.SLUG_MODEL_DISPLAY_NAME_MAPPING[slug]
            joblib.dump(estimator, self.modelFilepath + "/" + modelName + ".pkl")
            row = {"Model Id": modelName, "Slug": slug, "Selected": "False", "alwaysSelected": "False",
                   "Run Time(Secs)": CommonUtils.round_sig(time.time() - st), "comparisonMetricUsed": None,
                   "algorithmName": algoName}
            # row = {"Model Id":modelName,"Slug":slug,"Selected":"False","Run Time(Secs)":str(CommonUtils.round_sig(time.time()-st))}
            algoEvaluationMetrics = {}
            if self.appType == "REGRESSION":
                algoEvaluationMetrics["R-Squared"] = metrics.r2_score(self.y_test, y_score)
                overfit_check = metrics.r2_score(self.y_train, train_score)
                algoEvaluationMetrics["MSE"] = metrics.mean_squared_error(self.y_test, y_score)
                algoEvaluationMetrics["MAE"] = metrics.mean_absolute_error(self.y_test, y_score)
                algoEvaluationMetrics["RMSE"] = sqrt(algoEvaluationMetrics["MSE"])
                row["comparisonMetricUsed"] = self.evaluationMetricDict["displayName"]
            elif self.appType == "CLASSIFICATION":
                algoEvaluationMetrics["Accuracy"] = metrics.accuracy_score(self.y_test,y_score)
                overfit_check =  metrics.accuracy_score(self.y_train, train_score)
                row["comparisonMetricUsed"] = self.evaluationMetricDict["displayName"]
                if len(self.levels) <= 2:
                    algoEvaluationMetrics["Precision"] = metrics.precision_score(self.y_test, y_score,
                                                                                 pos_label=self.posLabel,
                                                                                 average="binary")
                    algoEvaluationMetrics["Recall"] = metrics.recall_score(self.y_test, y_score,
                                                                           pos_label=self.posLabel, average="binary")
                    algoEvaluationMetrics["ROC-AUC"] = metrics.roc_auc_score(self.y_test, y_score)
                elif len(self.levels) > 2:
                    algoEvaluationMetrics["Precision"] = metrics.precision_score(self.y_test,y_score,pos_label=self.posLabel,average="macro")
                    algoEvaluationMetrics["Recall"] = metrics.recall_score(self.y_test,y_score,pos_label=self.posLabel,average="macro")

                    algoEvaluationMetrics["ROC-AUC"] = self.getMultiClassAucRoc(y_prob,y_score)

            if evaluationMetric in ["MAE","MSE","RMSE"]:
                if initial:
                    evalMetricVal = algoEvaluationMetrics[evaluationMetric]
                    self.bestModel = estimator
                    self.bestParam = paramsObj
                    initial = False
                else:
                    if algoEvaluationMetrics[evaluationMetric] < evalMetricVal:
                        if 0.15 > (overfit_check-algoEvaluationMetrics["R-Squared"]):
                            self.bestModel = estimator
                            self.bestParam = paramsObj
                            evalMetricVal = algoEvaluationMetrics[evaluationMetric]
            else:
                if algoEvaluationMetrics[evaluationMetric] > evalMetricVal and self.appType == "CLASSIFICATION":
                    if evalMetricVal== -1:
                        print("updated initial params")
                        self.bestModel = estimator
                        self.bestParam = paramsObj
                        evalMetricVal = algoEvaluationMetrics[evaluationMetric]
                    elif 15 > (int(overfit_check)-int(algoEvaluationMetrics["Accuracy"])):
                        print("updated best params")
                        self.bestModel = estimator
                        self.bestParam = paramsObj
                        evalMetricVal = algoEvaluationMetrics[evaluationMetric]
                elif algoEvaluationMetrics[evaluationMetric] > evalMetricVal and self.appType == "REGRESSION":
                    if evalMetricVal== -1:
                        self.bestModel = estimator
                        self.bestParam = paramsObj
                        evalMetricVal = algoEvaluationMetrics[evaluationMetric]
                    elif 0.15 > (overfit_check-algoEvaluationMetrics["R-Squared"]):
                        self.bestModel = estimator
                        self.bestParam = paramsObj
                        evalMetricVal = algoEvaluationMetrics[evaluationMetric]

            algoEvaluationMetrics = {k:CommonUtils.round_sig(v) for k,v in list(algoEvaluationMetrics.items())}
            # algoEvaluationMetrics = {k:str(CommonUtils.round_sig(v)) for k,v in algoEvaluationMetrics.items()}
            row.update(algoEvaluationMetrics)
            paramsObj = dict([(k,str(v)) if (v == None) | (v in [True,False]) else (k,v) for k,v in list(paramsObj.items())])
            row.update(paramsObj)
            tableOutput.append(row)
        #joblib.dump(estimator,self.modelFilepath+"/"+modelName+".pkl")
        if self.appType == "REGRESSION":
            if self.evaluationMetricDict["name"] == "r2":
                tableOutput = sorted(tableOutput, key=lambda x: float(x[tableOutput[0]["comparisonMetricUsed"]]),
                                     reverse=True)
            else:
                tableOutput = sorted(tableOutput, key=lambda x: float(x[tableOutput[0]["comparisonMetricUsed"]]),
                                     reverse=False)

        elif self.appType == "CLASSIFICATION":
            if (len(self.levels) > 2) & (self.evaluationMetricDict["name"] == "roc_auc"):
                defaultComparisonMetric = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[
                    GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC]
                tableOutput = sorted(tableOutput, key=lambda x: float(x[defaultComparisonMetric]), reverse=True)
            else:
                tableOutput = sorted(tableOutput, key=lambda x: float(x[tableOutput[0]["comparisonMetricUsed"]]),
                                     reverse=True)
        if self.appType == "REGRESSION":
            self.keepColumns += ["RMSE", "MAE", "MSE", "R-Squared"]
        elif self.appType == "CLASSIFICATION":
            self.keepColumns += ["Accuracy","Precision","Recall","ROC-AUC"]
        self.keepColumns += list(paramsObj.keys())
        self.keepColumns.append("Selected")
        bestMod = tableOutput[0]
        bestMod["Selected"] = "True"
        bestMod["alwaysSelected"] = "True"
        tableOutput[0] = bestMod
        return tableOutput

    def getBestModel(self):
        return self.bestModel

    def getBestParam(self):
        return self.bestParam

    def getMultiClassAucRoc(self,y_prob,y_score):
        positive_label_probs = []
        for val in y_prob:
            positive_label_probs.append(val[self.posLabel])

        y_test_roc_multi = []
        for val in self.y_test:
            if val != self.posLabel:
                val = self.posLabel + 1
                y_test_roc_multi.append(val)
            else:
                y_test_roc_multi.append(val)

        y_score_roc_multi = []
        for val in y_score:
            if val != self.posLabel:
                val = self.posLabel + 1
                y_score_roc_multi.append(val)
            else:
                y_score_roc_multi.append(val)

        roc_auc = metrics.roc_auc_score(y_test_roc_multi, y_score_roc_multi)
        return roc_auc

class SkleanrKFoldResult(object):
    """
    sampling can be ["kfold","stratifiedKfold","stratifiedShuffleSplit"]
    by default its kfold
    """
    def __init__(self,numFold=3,estimator=None,x_train=None,x_test=None,y_train=None,y_test=None,appType=None,levels=None,posLabel=None,sampling="stratifiedKfold",evaluationMetricDict=None):
        self.estimator = estimator
        self.appType = appType
        self.x_train = x_train
        self.y_train = y_train
        self.posLabel = posLabel
        self.levels = levels
        self.evaluationMetricDict = evaluationMetricDict
        self.kFoldOutput = []
        if self.appType == "CLASSIFICATION":
            self.sampling = sampling
        else:
            self.sampling = "kfold"
        if self.sampling == "stratifiedKfold":
            self.kfObject = StratifiedKFold(n_splits=numFold, random_state=None, shuffle=False)
            self.kfObjectSplit = self.kfObject.split(self.x_train, self.y_train)
        elif self.sampling == "kfold":
            self.kfObject = KFold(n_splits=numFold, random_state=None, shuffle=False)
            self.kfObjectSplit = self.kfObject.split(self.x_train)
        elif self.sampling == "stratifiedShuffleSplit":
            self.kfObject = StratifiedShuffleSplit(n_splits=numFold, test_size=0.5, random_state=0)
            self.kfObjectSplit = self.kfObject.split(self.x_train, self.y_train)

    def train_and_save_result(self):
        evaluationMetric = self.evaluationMetricDict["name"]
        for train_index, test_index in self.kfObject.split(self.x_train,self.y_train):
            x_train_fold, x_test_fold = self.x_train.iloc[train_index, :], self.x_train.iloc[test_index, :]
            y_train_fold, y_test_fold = self.y_train.iloc[train_index], self.y_train.iloc[test_index]
            x_train_fold.columns = [re.sub("[[]|[]]|[<]", "", col) for col in x_train_fold.columns.values]
            self.estimator.fit(x_train_fold, y_train_fold)
            self.estimator.feature_names = list(x_train_fold.columns.values)
            if self.appType == "CLASSIFICATION":
                try:
                    # y_score_fold = self.estimator.best_estimator_.predict(x_test_fold)
                    y_score_fold, y_prob, threshold = self.set_fold_accuracy(self.estimator.best_estimator_,
                                                                             x_test_fold, y_test_fold, self.levels)
                except:
                    # y_score_fold = self.estimator.predict(x_test_fold)
                    y_score_fold, y_prob, threshold = self.set_fold_accuracy(self.estimator, x_test_fold, y_test_fold,
                                                                             self.levels)
            else:
                y_prob = None
                threshold = False
                try:
                    y_score_fold = self.estimator.best_estimator_.predict(x_test_fold)
                except:
                    y_score_fold = self.estimator.predict(x_test_fold)
            metricsFold = {}
            y_test = []
            y_score = []
            y_proba = []
            thresholds = []
            y_test.append(y_test_fold)
            y_score.append(y_score_fold)
            y_proba.append(y_prob)
            thresholds.append(threshold)
            if self.appType == "CLASSIFICATION":
                metricsFold["accuracy"] = metrics.accuracy_score(y_test_fold, y_score_fold)
                if len(self.levels) <= 2:
                    metricsFold["precision"] = metrics.precision_score(y_test_fold, y_score_fold,
                                                                       pos_label=self.posLabel, average="binary")
                    metricsFold["recall"] = metrics.recall_score(y_test_fold, y_score_fold, pos_label=self.posLabel,
                                                                 average="binary")
                    fpr, tpr, _ = metrics.roc_curve(y_test_fold, y_prob[:, self.posLabel], pos_label=self.posLabel)
                    roc_auc_score = metrics.auc(fpr, tpr)
                    metricsFold["roc_auc"] = roc_auc_score
                elif len(self.levels) > 2:
                    metricsFold["precision"] = metrics.precision_score(y_test_fold, y_score_fold,
                                                                       pos_label=self.posLabel, average="macro")
                    metricsFold["recall"] = metrics.recall_score(y_test_fold, y_score_fold, pos_label=self.posLabel,
                                                                 average="macro")
                    metricsFold["roc_auc"] = "NA"
            elif self.appType == "REGRESSION":
                metricsFold["r2"] = metrics.r2_score(y_test_fold, y_score_fold)
                metricsFold["neg_mean_squared_error"] = metrics.mean_squared_error(y_test_fold, y_score_fold)
                metricsFold["neg_mean_absolute_error"] = metrics.mean_absolute_error(y_test_fold, y_score_fold)
                try:
                    metricsFold["neg_mean_squared_log_error"] = metrics.mean_squared_log_error(y_test_fold,
                                                                                               y_score_fold)
                except:
                    metricsFold["neg_mean_squared_log_error"] = "NA"
                metricsFold["RMSE"] = sqrt(metricsFold["neg_mean_squared_error"])
            # try:
            # self.kFoldOutput.append((self.estimator.best_estimator_,metricsFold))
            # except:
            self.kFoldOutput.append((self.estimator, metricsFold, y_test, y_score, y_proba, thresholds))
        if self.appType == "CLASSIFICATION":
            self.kFoldOutput = sorted(self.kFoldOutput, key=lambda x: x[1][self.evaluationMetricDict["name"]],
                                      reverse=True)
        elif self.appType == "REGRESSION":
            if self.evaluationMetricDict["name"] == "r2":
                self.kFoldOutput = sorted(self.kFoldOutput, key=lambda x: x[1][self.evaluationMetricDict["name"]],
                                          reverse=True)
            else:
                self.kFoldOutput = sorted(self.kFoldOutput, key=lambda x: x[1][self.evaluationMetricDict["name"]],
                                          reverse=False)

    def get_kfold_result(self):
        return self.kFoldOutput

    def get_best_estimator(self):
        return self.kFoldOutput[0][0]

    def set_fold_accuracy(self, estimator, x_test_fold, y_test_fold, levels):
        threshold = False
        if len(levels) == 1:
            y_score = estimator.predict(x_test_fold)
        elif len(levels) == 2:
            y_proba = estimator.predict_proba(x_test_fold)[:, 1]
            fpr, tpr, threshold = metrics.roc_curve(y_test_fold, y_proba)
            thresh_point = np.argmax(tpr - fpr)
            y_score = [1 if x >= threshold[thresh_point] else 0 for x in y_proba]
            threshold = threshold[thresh_point]
        else:
            y_score = estimator.predict(x_test_fold)
        try:
            y_prob = estimator.predict_proba(x_test_fold)
        except:
            y_prob = [0] * len(y_score)
        return y_score, y_prob, threshold

    def get_ytest(self):
        return self.kFoldOutput[0][2]

    def get_yscore(self):
        return self.kFoldOutput[0][3]

    def get_yprob(self):
        return self.kFoldOutput[0][4]

    def get_threshold(self):
        return self.kFoldOutput[0][5]
