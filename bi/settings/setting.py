from __future__ import absolute_import
from .pySparkMLClassificationParams import *
from .pySparkMLRegressionParams import *
from .sklearnMLClassificationParams import *
from .sklearnMLRegressionParams import *

UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION = 11
UNIQUE_VALUES_COUNT_CUTOFF_CLASSIFICATION_DIMENSION = 20
MODEL_NAME_MAX_LENGTH = 4
CLASSIFICATION_MODEL_EVALUATION_METRIC = "accuracy"
REGRESSION_MODEL_EVALUATION_METRIC = "r2"
SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP = {
    "r2":"R-Squared",
    "RMSE":"RMSE",
    "neg_mean_absolute_error":"MAE",
    "neg_mean_squared_error":"MSE",
    "neg_mean_squared_log_error":"MSE(log)",
    "accuracy":"Accuracy",
    "precision":"Precision",
    "recall":"Recall",
    "roc_auc":"ROC-AUC"
}
PYSPARK_EVAL_METRIC_NAME_DISPLAY_MAP = {
    "r2":"r2",
    "RMSE":"rmse",
    "neg_mean_absolute_error":"mae",
    "neg_mean_squared_error":"mse",
    "neg_mean_squared_log_error":"MSE(log)",
    "accuracy":"Accuracy",
    "precision":"Precision",
    "recall":"Recall",
    "roc_auc":"ROC-AUC"
}
MAX_NUMBER_OF_MODELS_IN_SUMMARY = 10
REG_SCORE_HIGHLIGHT = False
REG_SCORE_ANOVA_KEY_FACTORS = False

CHISQUARELEVELLIMIT = 10
CHISQUARESIGNIFICANTDIMENSIONTOSHOW = 8

DTREE_TARGET_DIMENSION_MAX_LEVEL = 10
DTREE_OTHER_DIMENSION_MAX_LEVEL = 50
CONSIDERED_COLUMNS = []

DECISIONTREERKMEANSTARGETNAME = ['Low','Medium','High']
MAPEBINS = [0,5,15,25,100]  #####Need to look in the upper limit
HDFS_SECRET_KEY = "xfBmEcr_hFHGqVrTo2gMFpER3ks9x841UcvJbEQJesI="
ALGORITHMRANDOMSLUG = "f77631ce2ab24cf78c55bb6a5fce4db8"
ANOVAMAXLEVEL = 200
BLOCKSPLITTER = "|~NEWBLOCK~|"
BASEFOLDERNAME_MODELS = "mAdvisorModels"
BASEFOLDERNAME_SCORES = "mAdvisorScores"
PROBABILITY_RANGE_FOR_DONUT_CHART = {"0-10%":(0,10),"10-20%":(10,20),"20-30%":(20,30),"30-40%":(30,40),"40-50%":(40,50),"50-60%":(50,60),"60-70%":(60,70),"70-80%":(70,80),"80-90%":(80,90),"90-100%":(90,100)}

DEFAULT_VALIDATION_OBJECT = {
         "name":"trainAndtest",
         "displayName":"Train and Test",
         "value":0.8
       }

DEFAULT_NULL_VALUES = ["Null", "N/A", "NaN", "None", "na", "nan","n/a","#na","#N/A","#NA","NA",'no clue','NO CLUE','-',
                    'n a','not available','none','No Clue','!','N A','NONE','Not Available','null','NOT AVAILABLE','?']
APPS_ID_MAP = {
    '1': {
      'displayName': 'Opportunity Scoring',
      'type': 'CLASSIFICATION',
      'name': 'opportunity_scoring',
      'heading': 'Factors influencing Opportunity Score'
    },
    '2': {
      'displayName': 'Automated Prediction',
      'type': 'CLASSIFICATION',
      'name': 'automated_prediction',
      'heading': 'Feature Importance'
    },
    '3': {
      'displayName': 'Robo Advisor',
      'type': 'ROBO',
      'name': 'robo_advisor_insights',
      'heading': None
    },
    '4': {
      'displayName': 'Speech Analytics',
      'type': 'SPEECH',
      'name': 'speech_analytics',
      'heading': None
    },
    '5': {
      'displayName': 'Stock Sense',
      'type': 'STOCK_SENSE',
      'name': 'stock_sense',
      'heading': None
    },
    '6': {
      'displayName': 'Churn Prediction',
      'type': 'CLASSIFICATION',
      'name': 'churn_prediction',
      'heading': 'Factors influencing Churn'
    },
    '7': {
      'displayName': 'Re-admission Prediction',
      'type': 'CLASSIFICATION',
      'name': 're_admission_prediction',
      'heading': 'Factors influencing Re-admission'
    },
    '8': {
      'displayName': 'Physician Attrition',
      'type': 'CLASSIFICATION',
      'name': 'physician_attrition',
      'heading': 'Factors influencing Attrition'
    },
    '9': {
      'displayName': 'Credit Card Fraud',
      'type': 'CLASSIFICATION',
      'name': 'credit_card_fraud',
      'heading': 'Factors influencing Fraud'
    },
    '10': {
      'displayName': 'Claims Prediction',
      'type': 'CLASSIFICATION',
      'name': 'claims_prediction',
      'heading': 'Factors influencing Claims'
    },
  '11': {
    'displayName': 'Asset Health Prediction',
    'type': 'CLASSIFICATION',
    'name': 'asset_health_prediction',
    'heading': 'Factors influencing Asset Health'
  },
  '12': {
    'displayName': 'Employee Attrition',
    'type': 'CLASSIFICATION',
    'name': 'employee_attrition',
    'heading': 'Factors influencing Attrition'
  },
  '13': {
    'displayName': 'Automated Prediction',
    'type': 'REGRESSION',
    'name': 'regression_app',
    'heading': 'Feature Importance'
  }
}


SLUG_MODEL_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"randomforest",
            ALGORITHMRANDOMSLUG+"sprf":"sparkrandomforest",
            ALGORITHMRANDOMSLUG+"spmlpc":"sparkmlpclassifier",
            ALGORITHMRANDOMSLUG+"spxgb":"sparkxgboost",
            ALGORITHMRANDOMSLUG+"splr":"sparklogisticregression",
            ALGORITHMRANDOMSLUG+"nb":"naivebayesber",
            ALGORITHMRANDOMSLUG+"nb":"naivebayesgau",
            ALGORITHMRANDOMSLUG+"spnb":"sparknaivebayes",
            ALGORITHMRANDOMSLUG+"nb":"naive bayes",
            ALGORITHMRANDOMSLUG+"lr":"logisticregression",
            ALGORITHMRANDOMSLUG+"en":"ensemble",
            ALGORITHMRANDOMSLUG+"xgb":"xgboost",
            ALGORITHMRANDOMSLUG+"adab":"adaboost",
            ALGORITHMRANDOMSLUG+"lgbm":"LightGBM",
            ALGORITHMRANDOMSLUG+"spxgb":"sparkxgboost",
            ALGORITHMRANDOMSLUG+"svm":"svm",
            ALGORITHMRANDOMSLUG+"linr":"linearregression",
            ALGORITHMRANDOMSLUG+"gbtr":"gbtregression",
            ALGORITHMRANDOMSLUG+"dtreer":"dtreeregression",
            ALGORITHMRANDOMSLUG+"rfr":"rfregression",
            ALGORITHMRANDOMSLUG+"mlp":"Neural Network (Sklearn)",
            ALGORITHMRANDOMSLUG+"tfx":"Neural Network (TensorFlow)",
            ALGORITHMRANDOMSLUG+"nnpt":"Neural Network (PyTorch)"
            }
MODEL_SLUG_MAPPING = {
            "randomforest":ALGORITHMRANDOMSLUG+"rf",
            "sparkrandomforest":ALGORITHMRANDOMSLUG+"sprf",
            "sparkmlpclassifier":ALGORITHMRANDOMSLUG+"spmlpc",
            "sparkxgboost":ALGORITHMRANDOMSLUG+"spxgb",
            "sparklogisticregression":ALGORITHMRANDOMSLUG+"splr",
            "naivebayesber":ALGORITHMRANDOMSLUG+"nb",
            "naivebayesgau":ALGORITHMRANDOMSLUG+"nb",
            "naive bayes":ALGORITHMRANDOMSLUG+"nb",
            "naivebayesmul":ALGORITHMRANDOMSLUG+"nb",
            "sparknaivebayes":ALGORITHMRANDOMSLUG+"spnb",
            "logisticregression":ALGORITHMRANDOMSLUG+"lr",
            "ensemble":ALGORITHMRANDOMSLUG+"en",
            "xgboost":ALGORITHMRANDOMSLUG+"xgb",
            "adaboost":ALGORITHMRANDOMSLUG+"adab",
            "LightGBM":ALGORITHMRANDOMSLUG+"lgbm",
            "sparkxgboost":ALGORITHMRANDOMSLUG+"spxgb",
            "svm":ALGORITHMRANDOMSLUG+"svm",
            "linearregression":ALGORITHMRANDOMSLUG+"linr",
            "generalizedlinearregression":ALGORITHMRANDOMSLUG+"linr",
            "gbtregression":ALGORITHMRANDOMSLUG+"gbtr",
            "dtreeregression":ALGORITHMRANDOMSLUG+"dtreer",
            "rfregression":ALGORITHMRANDOMSLUG+"rfr",
            "Neural Network (Sklearn)":ALGORITHMRANDOMSLUG+"mlp",
            "Neural Network (TensorFlow)":ALGORITHMRANDOMSLUG+"tfx",
            "Neural Network (PyTorch)":ALGORITHMRANDOMSLUG+"nnpt"
                     }

SLUG_MODEL_DISPLAY_NAME_MAPPING = {
            ALGORITHMRANDOMSLUG+"rf":"Random Forest",
            ALGORITHMRANDOMSLUG+"sprf":"Spark Random Forest",
            ALGORITHMRANDOMSLUG+"spmlpc":"Spark MLP Classifier",
            ALGORITHMRANDOMSLUG+"spxgb":"Spark XGBoost",
            ALGORITHMRANDOMSLUG+"splr":"Spark Logistic Regression",
            ALGORITHMRANDOMSLUG+"nb":"Naive Bayes",
            ALGORITHMRANDOMSLUG+"spnb":"Spark Naive Bayes",
            ALGORITHMRANDOMSLUG+"lr":"Logistic Regression",
            ALGORITHMRANDOMSLUG+"en":"Ensemble",
            ALGORITHMRANDOMSLUG+"xgb":"Xgboost",
            ALGORITHMRANDOMSLUG+"adab":"Adaboost",
            ALGORITHMRANDOMSLUG+"lgbm":"LightGBM",
            ALGORITHMRANDOMSLUG+"spxgb":"Spark XGBoost",
            ALGORITHMRANDOMSLUG+"svm":"SVM",
            ALGORITHMRANDOMSLUG+"linr":"Linear Regression",
            ALGORITHMRANDOMSLUG+"gbtr":"Gradient Boosted Trees",
            ALGORITHMRANDOMSLUG+"dtreer":"Decision Tree",
            ALGORITHMRANDOMSLUG+"rfr":"Random Forest",
            ALGORITHMRANDOMSLUG+"mlp":"Neural Network (Sklearn)",
            ALGORITHMRANDOMSLUG+"tfx":"Neural Network (TensorFlow)",
            ALGORITHMRANDOMSLUG+"nnpt":"Neural Network (PyTorch)"
            }

scriptsMapping = {
    "overview" : "Descriptive analysis",
    "performance" : "Measure vs. Dimension",
    "influencer" : "Measure vs. Measure",
    "prediction" : "Predictive modeling",
    "trend" : "Trend",
    "association" : "Dimension vs. Dimension"
}
measureAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Measure vs. Dimension":3,
    "Measure vs. Measure":3,
    "Trend":1.5,
    "Predictive modeling":1.5
}
dimensionAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Dimension vs. Dimension":4,
    "Trend":2.5,
    "Predictive modeling":2.5
}



classificationTrainingInitialScriptWeight = {"initialization":{"total":10}}

regressionTrainingInitialScriptWeight = {"initialization":{"total":10}}

mlModelPredictionWeight = {
    "initialization":{"total":10,"script":5,"narratives":5},
    "Descriptive analysis":{"total":20,"script":10,"narratives":10},
    "Measure vs. Dimension":{"total":30,"script":20,"narratives":10},
    "Predictive modeling":{"total":20,"script":10,"narratives":10},
    "algoSlug":{"total":20,"script":10,"narratives":10}
}


regressionAlgoRelativeWeight = {
    ALGORITHMRANDOMSLUG+"linr"  : 1,
    ALGORITHMRANDOMSLUG+"gbtr" : 1,
    ALGORITHMRANDOMSLUG+"rfr"  : 1,
    ALGORITHMRANDOMSLUG+"dtreer" : 1,
    ALGORITHMRANDOMSLUG+"tfx" : 1,
    ALGORITHMRANDOMSLUG+"nnpt" : 1
}

classificationAlgoRelativeWeight = {
    ALGORITHMRANDOMSLUG+"rf"  : 1,
    ALGORITHMRANDOMSLUG+"sprf"  : 1,
    ALGORITHMRANDOMSLUG+"spmlpc"  : 1,
    ALGORITHMRANDOMSLUG+"spxgb"  : 1,
    ALGORITHMRANDOMSLUG+"splr"  : 1,
    ALGORITHMRANDOMSLUG+"nb"  : 1,
    ALGORITHMRANDOMSLUG+"spnb"  : 1,
    ALGORITHMRANDOMSLUG+"xgb" : 1,
    ALGORITHMRANDOMSLUG+"en" : 1,
    ALGORITHMRANDOMSLUG+"adab" : 1,
    ALGORITHMRANDOMSLUG+"lgbm" : 1,
    ALGORITHMRANDOMSLUG+"spxgb" : 1,
    ALGORITHMRANDOMSLUG+"lr"  : 1,
    ALGORITHMRANDOMSLUG+"svm" : 2,
    ALGORITHMRANDOMSLUG+"mlp" : 1,
    ALGORITHMRANDOMSLUG+"tfx" : 1,
    ALGORITHMRANDOMSLUG+"nnpt" : 1

}

metadataScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
subsettingScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}


SUPPORTED_DATETIME_FORMATS = {
            "formats": (
                    '%m/%d/%Y %H:%M', '%d/%m/%Y %H:%M', '%m/%d/%y %H:%M', '%d/%m/%y %H:%M',
                    '%d-%m-%Y %H:%M', '%m-%d-%Y %H:%M',  '%m-%d-%y %H:%M', '%d-%m-%y %H:%M',
                    '%b/%d/%Y %H:%M', '%d/%b/%Y %H:%M', '%b/%d/%y %H:%M', '%d/%b/%y %H:%M',
                    '%b-%d-%Y %H:%M', '%d-%b-%Y %H:%M', '%b-%d-%y %H:%M', '%d-%b-%y %H:%M',
                    '%B/%d/%Y %H:%M', '%d/%B/%Y %H:%M', '%B/%d/%y %H:%M', '%d/%B/%y %H:%M',
                    '%B-%d-%Y %H:%M', '%d-%B-%Y %H:%M', '%B-%d-%y %H:%M', '%d-%B-%y %H:%M',
                    '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%Y-%b-%d %H:%M', '%Y-%B-%d %H:%M',

                    '%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%m/%d/%y %H:%M:%S', '%d/%m/%y %H:%M:%S',
                    '%d-%m-%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S', '%m-%d-%y %H:%M:%S', '%d-%m-%y %H:%M:%S',
                    '%b/%d/%Y %H:%M:%S', '%d/%b/%Y %H:%M:%S', '%b/%d/%y %H:%M:%S', '%d/%b/%y %H:%M:%S',
                    '%b-%d-%Y %H:%M:%S', '%d-%b-%Y %H:%M:%S', '%b-%d-%y %H:%M:%S', '%d-%b-%y %H:%M:%S',
                    '%B/%d/%Y %H:%M:%S', '%d/%B/%Y %H:%M:%S', '%B/%d/%y %H:%M:%S', '%d/%B/%y %H:%M:%S',
                    '%B-%d-%Y %H:%M:%S', '%d-%B-%Y %H:%M:%S', '%B-%d-%y %H:%M:%S', '%d-%B-%y %H:%M:%S',
                    '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%b-%d %H:%M:%S', '%Y-%B-%d %H:%M:%S',

                    '%m/%d/%YT%H:%M:%S.%f', '%d/%m/%YT%H:%M:%S.%f', '%m/%d/%yT%H:%M:%S.%f', '%d/%m/%yT%H:%M:%S.%f',
                    '%d-%m-%YT%H:%M:%S.%f', '%m-%d-%YT%H:%M:%S.%f', '%m-%d-%yT%H:%M:%S.%f', '%d-%m-%yT%H:%M:%S.%f',
                    '%b/%d/%YT%H:%M:%S.%f', '%d/%b/%YT%H:%M:%S.%f', '%b/%d/%yT%H:%M:%S.%f', '%d/%b/%yT%H:%M:%S.%f',
                    '%b-%d-%YT%H:%M:%S.%f', '%d-%b-%YT%H:%M:%S.%f', '%b-%d-%yT%H:%M:%S.%f', '%d-%b-%yT%H:%M:%S.%f',
                    '%B/%d/%YT%H:%M:%S.%f', '%d/%B/%YT%H:%M:%S.%f', '%B/%d/%yT%H:%M:%S.%f', '%d/%B/%yT%H:%M:%S.%f',
                    '%B-%d-%YT%H:%M:%S.%f', '%d-%B-%YT%H:%M:%S.%f', '%B-%d-%yT%H:%M:%S.%f', '%d-%B-%yT%H:%M:%S.%f',
                    '%Y-%m-%dT%H:%M:%S.%f', '%Y/%m/%dT%H:%M:%S.%f', '%Y-%b-%dT%H:%M:%S.%f', '%Y-%B-%dT%H:%M:%S.%f',

                    '%m-%d-%Y %r', '%d-%m-%Y %r', '%m-%d-%Y %R',
                    '%d-%m-%Y %R', '%m-%d-%y %r', '%d-%m-%y %r', '%m-%d-%y %R',
                    '%d-%m-%y %R', '%b-%d-%Y %r', '%d-%b-%Y %r', '%Y-%b-%d %r', '%b-%d-%Y %R',
                    '%d-%b-%Y %R', '%b-%d-%y %r', '%d-%b-%y %r', '%b-%d-%y %R', '%d-%b-%y %R',
                    '%B-%d-%Y %r', '%d-%B-%Y %r', '%B-%d-%Y %R', '%d-%B-%y %R',
                    '%d-%B-%Y %R', '%B-%d-%y %r', '%d-%B-%y %r', '%B-%d-%y %R',
                    '%y-%m-%d %R', '%y-%m-%d %r', '%Y-%m-%d %r', '%Y-%B-%d %r',
                    '%d %B %Y', '%d %B %y', '%d %b %y', '%d %b %Y',
                    '%m/%d/%Y', '%d/%m/%Y', '%m/%d/%y', '%d/%m/%y',
                    '%m-%d-%Y', '%d-%m-%Y', '%m-%d-%y', '%d-%m-%y',
                    '%b/%d/%Y', '%d/%b/%Y', '%b/%d/%y', '%d/%b/%y',
                    '%b-%d-%Y', '%d-%b-%Y', '%b-%d-%y', '%d-%b-%y',
                    '%B/%d/%Y', '%d/%B/%Y', '%B/%d/%y', '%d/%B/%y',
                    '%B-%d-%Y', '%d-%B-%Y', '%B-%d-%y', '%d-%B-%y',
                    '%Y-%m-%d', '%Y/%m/%d', '%Y-%b-%d', '%Y-%B-%d',
                    '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%m/%d/%Y',
                    '%d %B, %Y', '%d %B, %y', '%d %b, %Y', '%d %b, %y',
                    '%m/%d/%y', '%b %Y', '%B %y', '%m/%y', '%m/%Y',
                    '%B%Y', '%b %d,%Y', '%m.%d.%Y', '%m.%d.%y', '%b/%y',
                    '%m - %d - %Y', '%m - %d - %y', '%B %d, %y', '%b %d, %y',
                    '%d-%B', '%d-%b', '%b,%y', '%B,%y', '%b,%Y', '%B,%Y',
                    '%b %Y', '%b %y', '%B %Y', '%B %y', '%b-%y', '%b/%Y', '%b-%Y'),
             "dual_checks": (
                    '%m/%d/%Y %H:%M', '%m/%d/%y %H:%M', '%m-%d-%Y %H:%M', '%m-%d-%y %H:%M',
                    '%m-%d-%Y %r', '%m-%d-%Y %R', '%m-%d-%y %r','%m-%d-%y %R',
                    '%m/%d/%Y %r', '%m/%d/%Y %R', '%m/%d/%y %r', '%m/%d/%y %R',
                    '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
                    '%m.%d.%Y', '%m.%d.%y', '%m - %d - %Y','%m - %d - %y'),
            "pyspark_formats": (
          'MM/dd/yy', 'dd/MM/yy','MM-dd-yy', 'dd-MM-yy','MM/dd/yyyy HH:mm', 'dd/MM/yyyy HH:mm', 'MM/dd/yy HH:mm', 'dd/MM/yy HH:mm',
          'MM-dd-yyyy HH:mm', 'dd-MM-yyyy HH:mm', 'MM-dd-yy HH:mm', 'dd-MM-yy HH:mm',
          'MMM/dd/yyyy HH:mm', 'dd/MMM/yyyy HH:mm', 'MMM/dd/yy HH:mm', 'dd/MMM/yy HH:mm',
          'MMM-dd-yyyy HH:mm', 'dd-MMM-yyyy HH:mm', 'MMM-dd-yy HH:mm', 'dd-MMM-yy HH:mm',
          'MMMM/dd/yyyy HH:mm', 'dd/MMMM/yyyy HH:mm', 'MMMM/dd/yy HH:mm', 'dd/MMMM/yy HH:mm',
          'MMMM-dd-yyyy HH:mm', 'dd-MMMM-yyyy HH:mm', 'MMMM-dd-yy HH:mm', 'dd-MMMM-yy HH:mm',
          'yyyy-MM-dd HH:mm', 'yyyy/MM/dd HH:mm', 'yyyy-MMM-dd HH:mm', 'yyyy-MMMM-dd HH:mm',
          'dd MMMM yyyy', 'dd MMMM yy', 'dd MMM yy', 'dd MMM yyyy',
          'MM/dd/yyyy', 'dd/MM/yyyy',
          'MM-dd-yyyy', 'dd-MM-yyyy',
          'MMM/dd/yyyy', 'dd/MMM/yyyy', 'MMM/dd/yy', 'dd/MMM/yy',
          'MMM-dd-yyyy', 'dd-MMM-yyyy', 'MMM-dd-yy', 'dd-MMM-yy',
          'MMMM/dd/yyyy', 'dd/MMMM/yyyy', 'MMMM/dd/yy', 'dd/MMMM/yy',
          'MMMM-dd-yyyy', 'dd-MMMM-yyyy', 'MMMM-dd-yy', 'dd-MMMM-yy',
          'yyyy-MM-dd', 'yyyy/MM/dd', 'yyyy-MMM-dd', 'yyyy-MMMM-dd',
          'MMM dd, yyyy', 'MMMM dd, yyyy', 'MMMM dd yyyy', 'MM/dd/yyyy',
          'dd MMMM, yyyy', 'dd MMMM, yy', 'dd MMM, yyyy', 'dd MMM, yy',
          'MM/dd/yy', 'MMM yyyy', 'MMMM yy', 'MM/yy', 'MM/yyyy',
          'MMMMyyyy', 'MMM dd,yyyy', 'MM.dd.yyyy', 'MM.dd.yy', 'MMM/yy',
          'MM - dd - yyyy', 'MM - dd - yy', 'MMMM dd, yy', 'MMM dd, yy',
          'dd-MMMM', 'dd-MMM', 'MMM,yy', 'MMMM,yy', 'MMM,yyyy', 'MMMM,yyyy',
          'MMM yyyy', 'MMM yy', 'MMMM yyyy', 'MMMM yy', 'MMM-yy', 'MMM/yyyy', 'MMM-yyyy', 'dd-mm-yyyy')
                    }
algorithm_settings_pyspark =[
  {
    "algorithmName": "Logistic Regression",
    "selected": True,
    "parameters": [
      {
        "name": "maxIter",
        "displayName": "Maximum Solver Iterations",
        "className": "maxIter",
        "description": "Max number of iterations.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [
          10,
          1000
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "regParam",
        "displayName": "Regularisation parameter",
        "className": "regParam",
        "description": "Regularisation parameter.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [
          1e-05,
          0.5
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "float"
        ],
        "allowedDataType": [
          "float"
        ]
      },
      {
        "name": "elasticNetParam",
        "displayName": "elasticNetParam",
        "className": "elasticNetParam",
        "description": "Elastic Net mixing parameter in the given range.",
        "defaultValue": 0.0,
        "valueRange": [
          0,
          1
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": False,
        "expectedDataType": [
          "float"
        ],
        "allowedDataType": [
          "float"
        ]
      },
      {
        "name": "aggregationDepth",
        "className": "aggregationDepth",
        "displayName": "aggregationDepth",
        "description": "Depth for tree aggregation",
        "defaultValue": 2,
        "acceptedValue": None,
        "valueRange": [
          2,
          10
        ],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperparameterTuningCandidate": False,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "standardization",
        "displayName": "standardization",
        "description": "Whether to standardize the training features before fitting the model.",
        "defaultValue": True,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "fitIntercept",
        "displayName": "fitIntercept",
        "description": "Fit an intercept terms.",
        "defaultValue": True,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "tol",
        "className": "tol",
        "displayName": "tol",
        "description": "Convergence tolerance for iterative algorithms",
        "defaultValue": 1e-06,
        "acceptedValue": None,
        "valueRange": [
          0.0001,
          1000
        ],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "float",
          "int"
        ],
        "allowedDataType": [
          "float",
          "int"
        ]
      },
      {
        "name": "family",
        "className": "family",
        "displayName": "family",
        "description": "The name of family which is a description of the label distribution to be used in the model.",
        "defaultValue": [
          {
            "name": "auto",
            "selected": True,
            "displayName": "auto"
          },
          {
            "name": "binomial",
            "selected": False,
            "displayName": "binomial"
          },
          {
            "name": "multinomial",
            "selected": False,
            "displayName": "multinomial"
          }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "threshold",
        "displayName": "threshold",
        "className": "threshold",
        "description": "In binary classification prediction",
        "defaultValue": 0.5,
        "valueRange": [
          0,
          1
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": False,
        "expectedDataType": [
          "float"
        ],
        "allowedDataType": [
          "float"
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8lr",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "A statistical method to predict the likely outcome of any qualitative attribute. It is invariably used for predicting binary outcomes (such as Yes or No)."
  },
  {
    "algorithmName": "Random Forest",
    "selected": True,
    "parameters": [
      {
        "name": "maxDepth",
        "displayName": "Max Depth",
        "description": "Max number of levels in each decision tree.",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [
          2,
          20
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int",
          None
        ],
        "allowedDataType": [
          "int",
          None
        ]
      },
      {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Min number of data points placed in a node before the node is split.",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [
          1,
          100
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "numTrees",
        "displayName": "No of Estimators",
        "description": "Number of trees in the forest.",
        "defaultValue": 10,
        "acceptedValue": None,
        "valueRange": [
          10,
          1000
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [
          {
            "name": "gini",
            "selected": True,
            "displayName": "Gini Impurity"
          },
          {
            "name": "entropy",
            "selected": False,
            "displayName": "Entropy"
          }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "maxBins",
        "displayName": "No of Bins",
        "description": "Number of bins used when discretizing continuous features.",
        "defaultValue": 3,
        "acceptedValue": None,
        "valueRange": [
          3,
          100
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "seed",
        "className": "seed",
        "displayName": "Random Seed",
        "description": "Random seed for bootstrapping and choosing feature subsets.",
        "defaultValue": None,
        "acceptedValue": None,
        "valueRange": [
          1,
          100
        ],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperparameterTuningCandidate": False,
        "expectedDataType": [
          "int",
          None
        ],
        "allowedDataType": [
          "int",
          None
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8rf",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "A meta estimator that uses averaging predictive power of a number of decision tree\n                    classification models. This is very effective in predicting the likelihood in multi-class\n                    classifications and also to control overfitting."
  },
  {
    "algorithmName": "XGBoost",
    "selected": True,
    "parameters": [
      {
        "name": "maxDepth",
        "displayName": "Max Depth",
        "description": "Maximum depth of the tree.",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [
          2,
          20
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int",
          None
        ],
        "allowedDataType": [
          "int",
          None
        ]
      },
      {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [
          {
            "name": "gini",
            "selected": True,
            "displayName": "Gini Impurity"
          },
          {
            "name": "entropy",
            "selected": False,
            "displayName": "Entropy"
          }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "maxBins",
        "displayName": "maxBins",
        "description": "Maximum number of bins used for discretizing continuous features and for choosing how to split on features at each node.",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [
          40,
          300
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Minimum number of instances each child must have after split",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [
          1,
          100
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "minInfoGain",
        "className": "minInfoGain",
        "displayName": "minInfoGain",
        "description": "Minimum information gain for a split to be considered at a tree node.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [

        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "float"
        ],
        "allowedDataType": [
          "float"
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8xgb",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "A machine learning technique that produces an ensemble of multiple decision tree\n                    models to predict categorical variables. It is highly preferred to leverage\n                    computational power to build scalable and accurate models."
  },
  {
    "algorithmName": "naive bayes",
    "selected": True,
    "parameters": [
      {
        "name": "smoothing",
        "className": "smoothing",
        "displayName": "Alpha",
        "description": "Smoothing parameter",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [
          0.0,
          1.0
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "float"
        ],
        "allowedDataType": [
          "float"
        ]
      },
      {
        "name": "modelType",
        "className": "modelType",
        "displayName": "Model Type",
        "description": "The model type which is a string.",
        "defaultValue": [
          {
            "name": "multinomial",
            "selected": True,
            "displayName": "multinomial"
          },
          {
            "name": "bernoulli",
            "selected": False,
            "displayName": "bernoulli"
          }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperparameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8nb",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "The multinomial Naive Bayes classifier is suitable for classification with discrete\n                    features (e.g., word counts for text classification).\n                    The multinomial distribution normally requires integer feature counts.\n                    However, in practice, fractional counts such as tf-idf may also work."
  },
  {
    "algorithmName": "Neural Network (TensorFlow)",
    "selected": True,
    "parameters": [
      {
        "name": "layer",
        "displayName": "Layer",
        "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
        "defaultValue": [
          {
            "name": "Dense",
            "selected": True,
            "displayName": "Dense",
            "parameters": [
              {
                "name": "activation",
                "displayName": "Activation",
                "description": "Activation function for the hidden layer.",
                "defaultValue": [
                  {
                    "name": "elu",
                    "selected": False,
                    "displayName": "elu"
                  },
                  {
                    "name": "exponential",
                    "selected": False,
                    "displayName": "exponential"
                  },
                  {
                    "name": "hard_sigmoid",
                    "selected": False,
                    "displayName": "hard_sigmoid"
                  },
                  {
                    "name": "linear",
                    "selected": False,
                    "displayName": "Linear"
                  },
                  {
                    "name": "relu",
                    "selected": False,
                    "displayName": "relu"
                  },
                  {
                    "name": "selu",
                    "selected": False,
                    "displayName": "selu"
                  },
                  {
                    "name": "sigmoid",
                    "selected": False,
                    "displayName": "sigmoid"
                  },
                  {
                    "name": "softmax",
                    "selected": False,
                    "displayName": "softmax"
                  },
                  {
                    "name": "softplus",
                    "selected": False,
                    "displayName": "softplus"
                  },
                  {
                    "name": "softsign",
                    "selected": False,
                    "displayName": "softsign"
                  },
                  {
                    "name": "tanh",
                    "selected": False,
                    "displayName": "tanh"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "units",
                "displayName": "Units",
                "description": "Dimensionality of the output space.",
                "defaultValue": 1.0,
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "use_bias",
                "displayName": "Use Bias",
                "description": "Whether the layer uses a bias vector.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": False,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "batch_normalization",
                "displayName": "Batch Normalization",
                "description": "It is used to normalize the input layer by adjusting and scaling the activations.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": True,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "kernel_initializer",
                "displayName": "Kernel Initializer",
                "description": "Initializer for the kernel weights matrix.",
                "defaultValue": [
                  {
                    "name": "Zeros",
                    "selected": True,
                    "displayName": "Zeros"
                  },
                  {
                    "name": "Ones",
                    "selected": False,
                    "displayName": "Ones"
                  },
                  {
                    "name": "Constant",
                    "selected": False,
                    "displayName": "Constant"
                  },
                  {
                    "name": "RandomNormal",
                    "selected": False,
                    "displayName": "RandomNormal"
                  },
                  {
                    "name": "RandomUniform",
                    "selected": False,
                    "displayName": "RandomUniform"
                  },
                  {
                    "name": "TruncatedNormal",
                    "selected": False,
                    "displayName": "TruncatedNormal"
                  },
                  {
                    "name": "VarianceScaling",
                    "selected": False,
                    "displayName": "VarianceScaling"
                  },
                  {
                    "name": "Orthogonal",
                    "selected": False,
                    "displayName": "Orthogonal"
                  },
                  {
                    "name": "Identity",
                    "selected": False,
                    "displayName": "Identity"
                  },
                  {
                    "name": "lecun_uniform",
                    "selected": False,
                    "displayName": "lecun_uniform"
                  },
                  {
                    "name": "glorot_normal",
                    "selected": False,
                    "displayName": "glorot_normal"
                  },
                  {
                    "name": "glorot_uniform",
                    "selected": False,
                    "displayName": "glorot_uniform"
                  },
                  {
                    "name": "he_normal",
                    "selected": False,
                    "displayName": "he_normal"
                  },
                  {
                    "name": "lecun_normal",
                    "selected": False,
                    "displayName": "lecun_normal"
                  },
                  {
                    "name": "he_uniform",
                    "selected": False,
                    "displayName": "he_uniform"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "bias_initializer",
                "displayName": "Bias Initializer",
                "description": "Initializer for the bias vector.",
                "defaultValue": [
                  {
                    "name": "Zeros",
                    "selected": True,
                    "displayName": "Zeros"
                  },
                  {
                    "name": "Ones",
                    "selected": False,
                    "displayName": "Ones"
                  },
                  {
                    "name": "Constant",
                    "selected": False,
                    "displayName": "Constant"
                  },
                  {
                    "name": "RandomNormal",
                    "selected": False,
                    "displayName": "RandomNormal"
                  },
                  {
                    "name": "RandomUniform",
                    "selected": False,
                    "displayName": "RandomUniform"
                  },
                  {
                    "name": "TruncatedNormal",
                    "selected": False,
                    "displayName": "TruncatedNormal"
                  },
                  {
                    "name": "VarianceScaling",
                    "selected": False,
                    "displayName": "VarianceScaling"
                  },
                  {
                    "name": "Orthogonal",
                    "selected": False,
                    "displayName": "Orthogonal"
                  },
                  {
                    "name": "Identity",
                    "selected": False,
                    "displayName": "Identity"
                  },
                  {
                    "name": "lecun_uniform",
                    "selected": False,
                    "displayName": "lecun_uniform"
                  },
                  {
                    "name": "glorot_normal",
                    "selected": False,
                    "displayName": "glorot_normal"
                  },
                  {
                    "name": "glorot_uniform",
                    "selected": False,
                    "displayName": "glorot_uniform"
                  },
                  {
                    "name": "he_normal",
                    "selected": False,
                    "displayName": "he_normal"
                  },
                  {
                    "name": "lecun_normal",
                    "selected": False,
                    "displayName": "lecun_normal"
                  },
                  {
                    "name": "he_uniform",
                    "selected": False,
                    "displayName": "he_uniform"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "kernel_regularizer",
                "displayName": "Kernel Regularizer",
                "description": "Regularizer function applied to the kernel weights matrix.",
                "defaultValue": [
                  {
                    "name": "l1",
                    "selected": True,
                    "displayName": "l1"
                  },
                  {
                    "name": "l2",
                    "selected": False,
                    "displayName": "l2"
                  },
                  {
                    "name": "l1_l2",
                    "selected": False,
                    "displayName": "l1_l2"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "bias_regularizer",
                "displayName": "Bias Regularizer",
                "description": "Regularizer function applied to the bias vector.",
                "defaultValue": [
                  {
                    "name": "l1",
                    "selected": True,
                    "displayName": "l1"
                  },
                  {
                    "name": "l2",
                    "selected": False,
                    "displayName": "l2"
                  },
                  {
                    "name": "l1_l2",
                    "selected": False,
                    "displayName": "l1_l2"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "activity_regularizer",
                "displayName": "Activity Regularizer",
                "description": "Regularizer function applied to the output of the layer.",
                "defaultValue": [
                  {
                    "name": "l1",
                    "selected": True,
                    "displayName": "l1"
                  },
                  {
                    "name": "l2",
                    "selected": False,
                    "displayName": "l2"
                  },
                  {
                    "name": "l1_l2",
                    "selected": False,
                    "displayName": "l1_l2"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "kernel_constraint",
                "displayName": "Kernel Constraint",
                "description": "Constraint function applied to the kernel weights matrix.",
                "defaultValue": [
                  {
                    "name": "MaxNorm",
                    "selected": True,
                    "displayName": "MaxNorm"
                  },
                  {
                    "name": "NonNeg",
                    "selected": False,
                    "displayName": "NonNeg"
                  },
                  {
                    "name": "UnitNorm",
                    "selected": False,
                    "displayName": "UnitNorm"
                  },
                  {
                    "name": "MinMaxNorm",
                    "selected": False,
                    "displayName": "MinMaxNorm"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "bias_constraint",
                "displayName": "Bias Constraint",
                "description": "Constraint function applied to the bias vector.",
                "defaultValue": [
                  {
                    "name": "MaxNorm",
                    "selected": True,
                    "displayName": "MaxNorm"
                  },
                  {
                    "name": "NonNeg",
                    "selected": False,
                    "displayName": "NonNeg"
                  },
                  {
                    "name": "UnitNorm",
                    "selected": False,
                    "displayName": "UnitNorm"
                  },
                  {
                    "name": "MinMaxNorm",
                    "selected": False,
                    "displayName": "MinMaxNorm"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "Dropout",
            "selected": False,
            "displayName": "Dropout",
            "parameters": [
              {
                "name": "rate",
                "displayName": "Rate",
                "description": "Fraction of the input units to drop.",
                "defaultValue": 0.0,
                "acceptedValue": None,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textbox",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "loss",
        "displayName": "Loss",
        "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
        "defaultValue": [
          {
            "name": "sparse_categorical_crossentropy",
            "selected": True,
            "displayName": "sparse_categorical_crossentropy"
          },
          {
            "name": "squared_hinge",
            "selected": False,
            "displayName": "squared_hinge"
          },
          {
            "name": "hinge",
            "selected": False,
            "displayName": "hinge"
          },
          {
            "name": "categorical_hinge",
            "selected": False,
            "displayName": "categorical_hinge"
          },
          {
            "name": "categorical_crossentropy",
            "selected": False,
            "displayName": "categorical_crossentropy"
          },
          {
            "name": "binary_crossentropy",
            "selected": False,
            "displayName": "binary_crossentropy"
          },
          {
            "name": "kullback_leibler_divergence",
            "selected": False,
            "displayName": "kullback_leibler_divergence"
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "optimizer",
        "displayName": "Optimizer",
        "description": "Method used to minimize the loss function.",
        "defaultValue": [
          {
            "name": "SGD",
            "selected": True,
            "displayName": "SGD"
          },
          {
            "name": "RMSprop",
            "selected": False,
            "displayName": "RMSprop"
          },
          {
            "name": "Adagrad",
            "selected": False,
            "displayName": "Adagrad"
          },
          {
            "name": "Adadelta",
            "selected": False,
            "displayName": "Adadelta"
          },
          {
            "name": "Adam",
            "selected": False,
            "displayName": "Adam"
          },
          {
            "name": "Adamax",
            "selected": False,
            "displayName": "Adamax"
          },
          {
            "name": "Nadam",
            "selected": False,
            "displayName": "Nadam"
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "batch_size",
        "displayName": "Batch Size",
        "description": "The number of training examples in one Forward/Backward Pass.",
        "defaultValue": 0,
        "acceptedValue": 100,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "number_of_epochs",
        "displayName": "Number of Epochs",
        "description": "An epoch refers to one cycle through the full training data-set.",
        "defaultValue": 100,
        "acceptedValue": 100,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "metrics",
        "displayName": "Metrics",
        "description": "List of metrics to be evaluated by the model during training And testing.",
        "defaultValue": [
          {
            "name": "sparse_categorical_crossentropy",
            "selected": True,
            "displayName": "sparse_categorical_crossentropy"
          },
          {
            "name": "binary_crossentropy",
            "selected": False,
            "displayName": "binary_crossentropy"
          },
          {
            "name": "categorical_accuracy",
            "selected": False,
            "displayName": "categorical_accuracy"
          },
          {
            "name": "categorical_crossentropy",
            "selected": False,
            "displayName": "categorical_crossentropy"
          },
          {
            "name": "FalseNegatives",
            "selected": False,
            "displayName": "FalseNegatives"
          },
          {
            "name": "FalsePositives",
            "selected": False,
            "displayName": "FalsePositives"
          },
          {
            "name": "sparse_categorical_accuracy",
            "selected": False,
            "displayName": "sparse_categorical_accuracy"
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8tfx",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "An end-to-end open source platform for machine learning. TensorFlow is a rich system for managing all aspects of a machine learning system."
  },
  {
    "algorithmName": "Neural Network (PyTorch)",
    "selected": True,
    "parameters": [
      {
        "name": "layer",
        "displayName": "Layer",
        "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
        "defaultValue": [
          {
            "name": "Linear",
            "selected": True,
            "displayName": "Linear",
            "parameters": [
              {
                "name": "activation",
                "displayName": "Activation",
                "description": "Activation function for the hidden layer.",
                "defaultValue": [
                  {
                    "name": "ELU",
                    "selected": False,
                    "displayName": "ELU",
                    "parameters": [
                      {
                        "name": "alpha",
                        "displayName": "alpha",
                        "description": "the alpha value for the ELU formulation.",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Hardshrink",
                    "selected": False,
                    "displayName": "Hardshrink",
                    "parameters": [
                      {
                        "name": "lambd",
                        "displayName": "lambd",
                        "description": "the lambda value for the Hardshrink formulation.",
                        "defaultValue": 0.5,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Hardtanh",
                    "selected": False,
                    "displayName": "Hardtanh",
                    "parameters": [
                      {
                        "name": "min_val",
                        "displayName": "min_val",
                        "description": "minimum value of the linear region range.",
                        "defaultValue": -1,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "max_val",
                        "displayName": "max_val",
                        "description": "maximum value of the linear region range.",
                        "defaultValue": 1,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "LeakyReLU",
                    "selected": False,
                    "displayName": "LeakyReLU",
                    "parameters": [
                      {
                        "name": "negative_slope",
                        "displayName": "negative_slope",
                        "description": "Controls the angle of the negative slope.",
                        "defaultValue": 0.01,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "LogSigmoid",
                    "selected": False,
                    "displayName": "LogSigmoid",
                    "parameters": None
                  },
                  {
                    "name": "MultiheadAttention",
                    "selected": False,
                    "displayName": "MultiheadAttention",
                    "parameters": [
                      {
                        "name": "embed_dim",
                        "displayName": "embed_dim",
                        "description": "total dimension of the model.",
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "num_heads",
                        "displayName": "num_heads",
                        "description": "parallel attention heads.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "dropout",
                        "displayName": "dropout",
                        "description": "a Dropout layer on attn_output_weights.",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "bias",
                        "displayName": "bias",
                        "description": "",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": False,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      },
                      {
                        "name": "add_bias_kv",
                        "displayName": "add_bias_kv",
                        "description": "add bias to the key and value sequences at dim=0.",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": False,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      },
                      {
                        "name": "add_zero_attn",
                        "displayName": "add_zero_attn",
                        "description": "add a new batch of zeros to the key and Value sequences at dim=1.",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": False,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      },
                      {
                        "name": "kdim",
                        "displayName": "kdim",
                        "description": "total number of features in key.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "vdim",
                        "displayName": "vdim",
                        "description": "",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "PreLU",
                    "selected": False,
                    "displayName": "PreLU",
                    "parameters": [
                      {
                        "name": "num_parameters",
                        "displayName": "num_parameters",
                        "description": "number of alpha to learn.",
                        "defaultValue": [
                          {
                            "name": "1",
                            "selected": True,
                            "displayName": "1"
                          },
                          {
                            "name": "no of channels",
                            "selected": False,
                            "displayName": "No of Channels"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "string"
                        ],
                        "allowedDataType": [
                          "string"
                        ]
                      },
                      {
                        "name": "init",
                        "displayName": "init",
                        "description": "the initial value of alpha.",
                        "defaultValue": 0.25,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "ReLU",
                    "selected": False,
                    "displayName": "ReLU",
                    "parameters": None
                  },
                  {
                    "name": "ReLU6",
                    "selected": False,
                    "displayName": "ReLU6",
                    "parameters": None
                  },
                  {
                    "name": "RreLU",
                    "selected": False,
                    "displayName": "RreLU",
                    "parameters": [
                      {
                        "name": "lower",
                        "displayName": "lower",
                        "description": "lower bound of the uniform distribution.",
                        "defaultValue": 0.125,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "upper",
                        "displayName": "upper",
                        "description": "upper bound of the uniform distribution.",
                        "defaultValue": 0.33,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "SELU",
                    "selected": False,
                    "displayName": "SELU",
                    "parameters": None
                  },
                  {
                    "name": "CELU",
                    "selected": False,
                    "displayName": "CELU",
                    "parameters": [
                      {
                        "name": "alpha",
                        "displayName": "alpha",
                        "description": "the alpha value for the CELU formulation.",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "GELU",
                    "selected": False,
                    "displayName": "GELU",
                    "parameters": None
                  },
                  {
                    "name": "Sigmoid",
                    "selected": False,
                    "displayName": "Sigmoid",
                    "parameters": None
                  },
                  {
                    "name": "Softplus",
                    "selected": False,
                    "displayName": "Softplus",
                    "parameters": [
                      {
                        "name": "beta",
                        "displayName": "beta",
                        "description": "the beta value for the Softplus formulation.",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "threshold",
                        "displayName": "threshold",
                        "description": "values above this revert to a linear function.",
                        "defaultValue": 20,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Softshrink",
                    "selected": False,
                    "displayName": "Softshrink",
                    "parameters": [
                      {
                        "name": "lambd",
                        "displayName": "lambd",
                        "description": "the lambda value for the Softshrink formulation.",
                        "defaultValue": 0.5,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Softsign",
                    "selected": False,
                    "displayName": "Softsign",
                    "parameters": None
                  },
                  {
                    "name": "Tanh",
                    "selected": False,
                    "displayName": "Tanh",
                    "parameters": None
                  },
                  {
                    "name": "Tanhshrink",
                    "selected": False,
                    "displayName": "Tanhshrink",
                    "parameters": None
                  },
                  {
                    "name": "Threshold",
                    "selected": False,
                    "displayName": "Threshold",
                    "parameters": [
                      {
                        "name": "threshold",
                        "displayName": "threshold",
                        "description": "The value to threshold at.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "value",
                        "displayName": "value",
                        "description": "The value to replace with.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Softmin",
                    "selected": False,
                    "displayName": "Softmin",
                    "parameters": [
                      {
                        "name": "dim",
                        "displayName": "dim",
                        "description": "A dimension along which Softmin will be computed.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Softmax",
                    "selected": False,
                    "displayName": "Softmax",
                    "parameters": [
                      {
                        "name": "dim",
                        "displayName": "dim",
                        "description": "A dimension along which Softmax will be computed.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Softmax2d",
                    "selected": False,
                    "displayName": "Softmax2d",
                    "parameters": None
                  },
                  {
                    "name": "LogSoftmax",
                    "selected": False,
                    "displayName": "LogSoftmax",
                    "parameters": [
                      {
                        "name": "dim",
                        "displayName": "dim",
                        "description": "A dimension along which LogSoftmax will be computed.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "AdaptiveLogSoftmaxWithLoss",
                    "selected": False,
                    "displayName": "AdaptiveLogSoftmaxWithLoss",
                    "parameters": [
                      {
                        "name": "n_classes",
                        "displayName": "n_classes",
                        "description": "Number of classes in the dataset.",
                        "defaultValue": None,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "cutoffs",
                        "displayName": "cutoffs",
                        "description": "Cutoffs used to assign targets to their buckets.",
                        "defaultValue": None,
                        "paramType": "list",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "div_value",
                        "displayName": "div_value",
                        "description": "value used as an exponent to compute sizes of the clusters.",
                        "defaultValue": 4.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "head_bias",
                        "displayName": "head_bias",
                        "description": "If True, adds a bias term to the 'head' of the Adaptive softmax.",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": False,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      }
                    ]
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "dropout",
                "displayName": "Dropout",
                "description": "During training, randomly zeroes some of the elements of the input tensor with probability p using samples from a Bernoulli distribution.",
                "defaultValue": [
                  {
                    "name": "Dropout",
                    "selected": False,
                    "displayName": "Dropout",
                    "parameters": [
                      {
                        "name": "p",
                        "displayName": "p",
                        "description": "probability of an element to be dropped.",
                        "defaultValue": 0.5,
                        "paramType": "number",
                        "uiElemType": "slider",
                        "display": True,
                        "valueRange": [
                          0,
                          1
                        ],
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "batchnormalization",
                "displayName": "Batch Normalization",
                "description": "Applies Batch Normalization over a 2D or 3D input (a mini-batch of 1D inputs with optional additional channel dimension) as described in the paper.",
                "defaultValue": [
                  {
                    "name": "BatchNorm1d",
                    "selected": False,
                    "displayName": "BatchNorm1d",
                    "parameters": [
                      {
                        "name": "num_features",
                        "displayName": "num_features",
                        "description": "C from an expected input of size (N,C,L) or L from input of size (N, L).",
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "int"
                        ],
                        "allowedDataType": [
                          "int"
                        ]
                      },
                      {
                        "name": "eps",
                        "displayName": "eps",
                        "description": "a value added to the denominator for numerical stability.",
                        "defaultValue": 1e-05,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "momentum",
                        "displayName": "momentum",
                        "description": "the value used for the running_mean and running_var computation.",
                        "defaultValue": 0.1,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "affine",
                        "displayName": "affine",
                        "description": "a boolean value that when set to True, this module has learnable affine parameters, initialized the same way as done for batch normalization.",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": True,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "valueRange": [
                          0,
                          1
                        ],
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      },
                      {
                        "name": "track_running_stats",
                        "displayName": "track_running_stats",
                        "description": "a boolean value that when set to True, this module tracks the running mean and variance, and when set to False, this module does not track such statistics and always uses batch statistics in both training and eval modes.",
                        "defaultValue": [
                          {
                            "name": "False",
                            "selected": False,
                            "displayName": "False"
                          },
                          {
                            "name": "True",
                            "selected": True,
                            "displayName": "True"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "valueRange": [
                          0,
                          1
                        ],
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "bool"
                        ],
                        "allowedDataType": [
                          "bool"
                        ]
                      }
                    ]
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "units_ip",
                "displayName": "Input Units",
                "description": "Input Units parameter for the hidden layer.",
                "defaultValue": None,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "units_op",
                "displayName": "Output Units",
                "description": "Output Units parameter for the hidden layer.",
                "defaultValue": None,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "bias_init",
                "displayName": "bias_init",
                "description": "Bias initialisation parameter for the hidden layer.",
                "defaultValue": [
                  {
                    "name": "Uniform",
                    "selected": False,
                    "displayName": "Uniform",
                    "parameters": [
                      {
                        "name": "lower_bound",
                        "displayName": "lower bound",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "upper_bound",
                        "displayName": "upper bound",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Normal",
                    "selected": False,
                    "displayName": "Normal",
                    "parameters": [
                      {
                        "name": "mean",
                        "displayName": "mean",
                        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "std",
                        "displayName": "std",
                        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Constant",
                    "selected": False,
                    "displayName": "Constant",
                    "parameters": [
                      {
                        "name": "val",
                        "displayName": "val",
                        "description": "Fills the input Tensor with the value {val}",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Ones",
                    "displayName": "Ones",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Zeros",
                    "displayName": "Zeros",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Eyes",
                    "displayName": "Eyes",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Default",
                    "displayName": "Default",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Other",
                    "displayName": "Other",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": True,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "weight_init",
                "displayName": "weight_init",
                "description": "Weight initialisation parameter for the hidden layer.",
                "defaultValue": [
                  {
                    "name": "Uniform",
                    "selected": False,
                    "displayName": "Uniform",
                    "parameters": [
                      {
                        "name": "lower_bound",
                        "displayName": "lower bound",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "upper_bound",
                        "displayName": "upper bound",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Normal",
                    "selected": False,
                    "displayName": "Normal",
                    "parameters": [
                      {
                        "name": "mean",
                        "displayName": "mean",
                        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "std",
                        "displayName": "std",
                        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Constant",
                    "selected": False,
                    "displayName": "Constant",
                    "parameters": [
                      {
                        "name": "val",
                        "displayName": "val",
                        "description": "Fills the input Tensor with the value {val}",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Ones",
                    "displayName": "Ones",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Zeros",
                    "displayName": "Zeros",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Eyes",
                    "displayName": "Eyes",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Dirac",
                    "displayName": "Dirac",
                    "description": "Input Units parameter for the hidden layer.",
                    "selected": False,
                    "paramType": "number",
                    "uiElemType": "textBox",
                    "display": True,
                    "hyperpatameterTuningCandidate": True,
                    "expectedDataType": [
                      "string"
                    ],
                    "allowedDataType": [
                      "string"
                    ]
                  },
                  {
                    "name": "Xavier_Uniform",
                    "selected": False,
                    "displayName": "Xavier Uniform",
                    "parameters": [
                      {
                        "name": "gain",
                        "displayName": "gain",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Xavier_Normal",
                    "selected": False,
                    "displayName": "Xavier Normal",
                    "parameters": [
                      {
                        "name": "gain",
                        "displayName": "gain",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Kaiming_Normal",
                    "selected": False,
                    "displayName": "Kaiming Normal",
                    "parameters": [
                      {
                        "name": "a",
                        "displayName": "a",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 0.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "mode",
                        "displayName": "mode",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": [
                          {
                            "name": "fan_in",
                            "selected": True,
                            "displayName": "fan_in"
                          },
                          {
                            "name": "fan_out",
                            "selected": False,
                            "displayName": "fan_out"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "string"
                        ],
                        "allowedDataType": [
                          "string"
                        ]
                      },
                      {
                        "name": "nonlinearity",
                        "displayName": "nonlinearity",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": [
                          {
                            "name": "leaky_relu",
                            "selected": True,
                            "displayName": "leaky_relu"
                          },
                          {
                            "name": "relu",
                            "selected": False,
                            "displayName": "relu"
                          }
                        ],
                        "paramType": "list",
                        "uiElemType": "checkbox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "string"
                        ],
                        "allowedDataType": [
                          "string"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Orthogonal",
                    "selected": False,
                    "displayName": "Orthogonal",
                    "parameters": [
                      {
                        "name": "gain",
                        "displayName": "gain",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 1.0,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Sparse",
                    "selected": False,
                    "displayName": "Sparse",
                    "parameters": [
                      {
                        "name": "sparsity",
                        "displayName": "sparsity",
                        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                        "defaultValue": 0.5,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      },
                      {
                        "name": "std",
                        "displayName": "std",
                        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                        "defaultValue": 0.01,
                        "paramType": "number",
                        "uiElemType": "textBox",
                        "display": True,
                        "hyperpatameterTuningCandidate": True,
                        "expectedDataType": [
                          "float"
                        ],
                        "allowedDataType": [
                          "float"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "Default",
                    "selected": True,
                    "displayName": "Default",
                    "parameters": None
                  }
                ],
                "paramType": "list",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "weight_constraint",
                "displayName": "weight constraint",
                "description": "clipping the Weights.",
                "defaultValue": [
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True",
                    "parameters": [
                      [
                        {
                          "name": "min",
                          "displayName": "min",
                          "description": "minimum value.",
                          "defaultValue": 0.3,
                          "paramType": "number",
                          "uiElemType": "textBox",
                          "display": True,
                          "hyperpatameterTuningCandidate": True,
                          "expectedDataType": [
                            "float"
                          ],
                          "allowedDataType": [
                            "float"
                          ]
                        },
                        {
                          "name": "max",
                          "displayName": "max",
                          "description": "maximum value.",
                          "defaultValue": 0.7,
                          "paramType": "number",
                          "uiElemType": "textBox",
                          "display": True,
                          "hyperpatameterTuningCandidate": True,
                          "expectedDataType": [
                            "float"
                          ],
                          "allowedDataType": [
                            "float"
                          ]
                        }
                      ]
                    ]
                  },
                  {
                    "name": "False",
                    "selected": True,
                    "displayName": "False"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              }
            ]
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "loss",
        "displayName": "Loss",
        "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
        "defaultValue": [
          {
            "name": "CrossEntropyLoss",
            "selected": False,
            "displayName": "CrossEntropyLoss",
            "parameters": [
              {
                "name": "weight",
                "displayName": "weight",
                "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                "paramType": "tensor",
                "defaultValue": None,
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "tensor"
                ],
                "allowedDataType": [
                  "tensor"
                ]
              },
              {
                "name": "ignore_index",
                "displayName": "ignore_index",
                "description": "Specifies a target value that is ignored and does not contribute to the input gradient.",
                "defaultValue": None,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "CTCLoss",
            "selected": False,
            "displayName": "CTCLoss",
            "parameters": [
              {
                "name": "blank",
                "displayName": "blank",
                "description": "blank label.",
                "defaultValue": 0,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "zero_infinity",
                "displayName": "zero_infinity",
                "description": "Whether to zero infinite losses and the associated gradients.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": True,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              }
            ]
          },
          {
            "name": "NLLLoss",
            "selected": False,
            "displayName": "NLLLoss",
            "parameters": [
              {
                "name": "weight",
                "displayName": "weight",
                "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                "paramType": "tensor",
                "defaultValue": None,
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "tensor"
                ],
                "allowedDataType": [
                  "tensor"
                ]
              },
              {
                "name": "ignore_index",
                "displayName": "ignore_index",
                "description": "Specifies a target value that is ignored and does not contribute to the input gradient.",
                "defaultValue": None,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "PoissonNLLLoss",
            "selected": False,
            "displayName": "PoissonNLLLoss",
            "parameters": [
              {
                "name": "log_input",
                "displayName": "log_input",
                "description": "if True the loss is computed as exp(input)-target*input.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": False,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "full",
                "displayName": "full",
                "description": "whether to compute full loss, i. e. to add the Stirling approximation term.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": False,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "small value to avoid evaluation of log(0) when log_input = False.",
                "defaultValue": 1e-08,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "BCELoss",
            "selected": False,
            "displayName": "BCELoss",
            "parameters": [
              {
                "name": "weight",
                "displayName": "weight",
                "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                "paramType": "tensor",
                "defaultValue": None,
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "tensor"
                ],
                "allowedDataType": [
                  "tensor"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "BCEWithLogitsLoss",
            "selected": False,
            "displayName": "BCEWithLogitsLoss",
            "parameters": [
              {
                "name": "weight",
                "displayName": "weight",
                "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                "paramType": "tensor",
                "defaultValue": None,
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "tensor"
                ],
                "allowedDataType": [
                  "tensor"
                ]
              },
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "name": "pos_weight",
                "displayName": "pos_weight",
                "description": "a weight of positive examples. Must be a vector with length equal to the number of classes.",
                "defaultValue": "mean",
                "paramType": "tensor",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "tensor"
                ],
                "allowedDataType": [
                  "tensor"
                ]
              }
            ]
          },
          {
            "name": "SoftMarginLoss",
            "selected": False,
            "displayName": "SoftMarginLoss",
            "parameters": [
              {
                "name": "reduction",
                "displayName": "reduction",
                "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                "defaultValue": "mean",
                "paramType": "list",
                "valueRange": [
                  "none",
                  "mean",
                  "sum"
                ],
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "optimizer",
        "displayName": "Optimizer",
        "description": "Method used to minimize the loss function.",
        "defaultValue": [
          {
            "name": "Adadelta",
            "selected": False,
            "displayName": "Adadelta",
            "parameters": [
              {
                "name": "rho",
                "displayName": "rho",
                "description": "coefficient used for computing a running average of squared gradients.",
                "defaultValue": 0.9,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-06,
                "paramType": "number",
                "uiElemType": "textBox",
                "valueRange": [
                  1e-06,
                  1
                ],
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "lr",
                "displayName": "lr",
                "description": "coefficient that scale delta before it is applied to the parameters.",
                "defaultValue": 1.0,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "Adagrad",
            "selected": False,
            "displayName": "Adagrad",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.01,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "lr_decay",
                "displayName": "lr_decay",
                "description": " learning rate decay.",
                "defaultValue": 0,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-10,
                "valueRange": [
                  1e-10,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "Adam",
            "selected": False,
            "displayName": "Adam",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.001,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "betas",
                "displayName": "betas",
                "description": "coefficients used for computing running averages of gradient and its square.",
                "defaultValue": [
                  0.9,
                  0.999
                ],
                "valueRange": [
                  [
                    0.0,
                    1.0
                  ],
                  [
                    0.0,
                    1.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-08,
                "valueRange": [
                  1e-10,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "amsgrad",
                "displayName": "amsgrad",
                "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": True,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              }
            ]
          },
          {
            "name": "AdamW",
            "selected": False,
            "displayName": "AdamW",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.001,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "betas",
                "displayName": "betas",
                "description": "coefficients used for computing running averages of gradient and its square.",
                "defaultValue": [
                  0.9,
                  0.999
                ],
                "valueRange": [
                  [
                    0.0,
                    1.0
                  ],
                  [
                    0.0,
                    1.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-08,
                "valueRange": [
                  1e-08,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0.01,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "amsgrad",
                "displayName": "amsgrad",
                "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": True,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              }
            ]
          },
          {
            "name": "SparseAdam",
            "selected": False,
            "displayName": "SparseAdam",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.001,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "betas",
                "displayName": "betas",
                "description": "coefficients used for computing running averages of gradient and its square.",
                "defaultValue": [
                  0.9,
                  0.999
                ],
                "valueRange": [
                  [
                    0.0,
                    1.0
                  ],
                  [
                    0.0,
                    1.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-08,
                "valueRange": [
                  1e-08,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "Adamax",
            "selected": False,
            "displayName": "Adamax",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.001,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "betas",
                "displayName": "betas",
                "description": "coefficients used for computing running averages of gradient and its square.",
                "defaultValue": [
                  0.9,
                  0.999
                ],
                "valueRange": [
                  [
                    0.0,
                    1.0
                  ],
                  [
                    0.0,
                    1.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-08,
                "valueRange": [
                  1e-08,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "ASGD",
            "selected": False,
            "displayName": "ASGD",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.01,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "lambd",
                "displayName": "lambd",
                "description": "decay term.",
                "defaultValue": 0.0001,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "alpha",
                "displayName": "alpha",
                "description": "power for eta update.",
                "defaultValue": 0.75,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "t0",
                "displayName": "t0",
                "description": "point at which to start averaging.",
                "defaultValue": 1e-06,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0.0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "LBFGS",
            "selected": False,
            "displayName": "LBFGS",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 1,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "max_iter",
                "displayName": "max_iter",
                "description": "maximal number of iterations per optimization step.",
                "defaultValue": 20,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "max_eval",
                "displayName": "max_eval",
                "description": "maximal number of function evaluations per optimization step.",
                "defaultValue": 25,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "tolerance_grad",
                "displayName": "tolerance_grad",
                "description": " termination tolerance on first order optimality.",
                "defaultValue": 1e-05,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "tolerance_change",
                "displayName": "tolerance_change",
                "description": "termination tolerance on function value/parameter changes.",
                "defaultValue": 1e-09,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "history_size",
                "displayName": "history_size",
                "description": "update history size.",
                "defaultValue": 100,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "int"
                ],
                "allowedDataType": [
                  "int"
                ]
              },
              {
                "name": "line_search_fn",
                "displayName": "line_search_fn",
                "description": "either 'strong_wolfe' or None.",
                "defaultValue": [
                  {
                    "name": "None",
                    "selected": True,
                    "displayName": "None"
                  },
                  {
                    "name": "strong_wolfe",
                    "selected": False,
                    "displayName": "strong_wolfe"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "string"
                ],
                "allowedDataType": [
                  "string"
                ]
              }
            ]
          },
          {
            "name": "RMSprop",
            "selected": False,
            "displayName": "RMSprop",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.01,
                "valueRange": [
                  0.0,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "momentum",
                "displayName": "momentum",
                "description": "momentum factor.",
                "defaultValue": 0,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "alpha",
                "displayName": "alpha",
                "description": "smoothing constant.",
                "defaultValue": 0.99,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eps",
                "displayName": "eps",
                "description": "term added to the denominator to improve numerical stability.",
                "defaultValue": 1e-08,
                "valueRange": [
                  1e-08,
                  1.0
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "centered",
                "displayName": "centered",
                "description": "if True, compute the centered RMSProp, the gradient is normalized By an estimation of its variance.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": False,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": True,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "Rprop",
            "selected": False,
            "displayName": "Rprop",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.01,
                "valueRange": [
                  0,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "eta",
                "displayName": "eta",
                "description": "pair of (etaminus, etaplUs), that are multiplicative.",
                "defaultValue": [
                  0.5,
                  1.2
                ],
                "valueRange": [
                  [
                    0.0,
                    5.0
                  ],
                  [
                    0.0,
                    5.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "step_sizes",
                "displayName": "step_sizes",
                "description": "a pair of minimal and maximal allowed step sizes.",
                "defaultValue": [
                  1e-06,
                  50
                ],
                "valueRange": [
                  [
                    0.0,
                    5.0
                  ],
                  [
                    0.0,
                    5.0
                  ]
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "SGD",
            "selected": False,
            "displayName": "SGD",
            "parameters": [
              {
                "name": "lr",
                "displayName": "lr",
                "description": "learning rate.",
                "defaultValue": 0.1,
                "valueRange": [
                  0,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "momentum",
                "displayName": "momentum",
                "description": "momentum factor.",
                "defaultValue": 0,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "weight_decay",
                "displayName": "weight_decay",
                "description": "weight decay (L2 penalty).",
                "defaultValue": 0,
                "valueRange": [
                  0,
                  0.1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "dampening",
                "displayName": "dampening",
                "description": "dampening for momentum.",
                "defaultValue": 0,
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              },
              {
                "name": "nesterov",
                "displayName": "nesterov",
                "description": "enables Nesterov momentum.",
                "defaultValue": [
                  {
                    "name": "False",
                    "selected": False,
                    "displayName": "False"
                  },
                  {
                    "name": "True",
                    "selected": False,
                    "displayName": "True"
                  }
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "bool"
                ],
                "allowedDataType": [
                  "bool"
                ]
              }
            ]
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "regularizer",
        "displayName": "regularizer",
        "description": "Regularizer function.",
        "defaultValue": [
          {
            "name": "l1_regularizer",
            "selected": False,
            "displayName": "l1_regularizer",
            "parameters": [
              {
                "name": "l1_decay",
                "selected": False,
                "displayName": "l1_decay",
                "description": "l1 decay.",
                "defaultValue": 0.0,
                "valueRange": [
                  0,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          },
          {
            "name": "l2_regularizer",
            "selected": False,
            "displayName": "l2_regularizer",
            "parameters": [
              {
                "name": "l2_decay",
                "selected": False,
                "displayName": "l2_decay",
                "description": "l2 dacay.",
                "defaultValue": 0.0,
                "valueRange": [
                  0,
                  1
                ],
                "paramType": "number",
                "uiElemType": "textBox",
                "display": True,
                "hyperpatameterTuningCandidate": True,
                "expectedDataType": [
                  "float"
                ],
                "allowedDataType": [
                  "float"
                ]
              }
            ]
          }
        ],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
          "string"
        ],
        "allowedDataType": [
          "string"
        ]
      },
      {
        "name": "batch_size",
        "displayName": "Batch Size",
        "description": "The number of training examples in one Forward/Backward Pass.",
        "defaultValue": 0,
        "acceptedValue": None,
        "valueRange": [
          0,
          100
        ],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      },
      {
        "name": "number_of_epochs",
        "displayName": "Number of Epochs",
        "description": "An epoch refers to one cycle through the full training data-set.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": [
          "int"
        ],
        "allowedDataType": [
          "int"
        ]
      }
    ],
    "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8nnpt",
    "hyperParameterSetting": [
      {
        "name": "gridsearchcv",
        "params": [
          {
            "name": "evaluationMetric",
            "displayName": "Metric Used for Optimization",
            "defaultValue": [
              {
                "name": "accuracy",
                "selected": True,
                "displayName": "Accuracy"
              }
            ],
            "paramType": "list",
            "uiElemType": "dropDown",
            "display": False,
            "expectedDataType": [
              None,
              "string"
            ]
          },
          {
            "name": "kFold",
            "displayName": "No Of Folds to Use",
            "defaultValue": 3,
            "acceptedValue": None,
            "valueRange": [
              2,
              20
            ],
            "paramType": "number",
            "uiElemType": "slider",
            "display": True,
            "expectedDataType": [
              None,
              "int"
            ]
          }
        ],
        "displayName": "Grid Search",
        "selected": False
      },
      {
        "name": "none",
        "params": None,
        "displayName": "None",
        "selected": True
      }
    ],
    "description": "A python based library built to provide flexibility as a deep learning development platform. It is an open source machine learning library based on the Torch library, used for applications such as computer vision and natural language processing."
  }
]
algorithm_settings_pandas = [
      {
        "algorithmName": "Logistic Regression",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8lr",
        "description": "A statistical method to predict the likely outcome of any qualitative attribute. It is invariably used for predicting binary outcomes (such as Yes or No).",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_iter",
            "valueRange": [
              10,
              400
            ],
            "description": "Maximum number of iterations to be attempted for solver operations",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 100,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Solver Iterations",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": -1,
                "displayName": "All",
                "selected": True
              },
              {
                "name": 1,
                "displayName": "1 core",
                "selected": False
              },
              {
                "name": 2,
                "displayName": "2 cores",
                "selected": False
              },
              {
                "name": 3,
                "displayName": "3 cores",
                "selected": False
              },
              {
                "name": 4,
                "displayName": "4 cores",
                "selected": False
              }
            ],
            "displayName": "No Of Jobs",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "n_jobs",
            "allowedDataType": [
              "int"
            ],
            "description": "Number of CPU cores to be used when parallelizing over classes",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "tol",
            "valueRange": [
              3,
              10
            ],
            "description": "Tolerance for the stopping criteria",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 4,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Convergence tolerance of iterations(e^-n)",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Fit Intercept",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "fit_intercept",
            "allowedDataType": [
              "bool"
            ],
            "description": "Specifies if a constant(a.k.a bias or intercept) should be added to the decision function",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "newton-cg",
                "displayName": "newton-cg",
                "selected": True,
                "penalty": "l2"
              },
              {
                "name": "lbfgs",
                "displayName": "lbfgs",
                "selected": False,
                "penalty": "l2"
              },
              {
                "name": "sag",
                "displayName": "sag",
                "selected": False,
                "penalty": "l2"
              },
              {
                "name": "saga",
                "displayName": "saga",
                "selected": False,
                "penalty": "l1"
              }
            ],
            "displayName": "Solver Used",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "solver",
            "allowedDataType": [
              "string"
            ],
            "description": "Algorithm to use in the Optimization",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "ovr",
                "displayName": "One Vs Rest",
                "selected": True
              },
              {
                "name": "multinomial",
                "displayName": "Multinomial",
                "selected": False
              }
            ],
            "displayName": "Multiclass Option",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "multi_class",
            "allowedDataType": [
              "string"
            ],
            "description": "Nature of multiclass modeling options for classification",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Warm Start",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "warm_start",
            "allowedDataType": [
              "bool"
            ],
            "description": "It reuses the solution of the previous call to fit as initialization",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "random_state",
            "valueRange": [
              1,
              100
            ],
            "description": "The seed of the pseudo random number generator to use when shuffling the data",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": None,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Random Seed",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "C",
            "valueRange": [
              0.1,
              20
            ],
            "description": "It refers to the inverse of regularization strength",
            "expectedDataType": [
              "float",
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Inverse of regularization strength",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "None",
                "displayName": "None",
                "selected": False
              },
              {
                "name": "balanced",
                "displayName": "balanced",
                "selected": False
              }
            ],
            "displayName": "Class Weight",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "class_weight",
            "allowedDataType": [
              "bool"
            ],
            "description": "Weights associated with classes of the target column",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "Random Forest",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8rf",
        "description": "A meta estimator that uses averaging predictive power of a number of decision tree\n            classification models. This is very effective in predicting the likelihood in multi-class\n            classifications and also to control overfitting.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_depth",
            "valueRange": [
              2,
              20
            ],
            "description": "The maximum depth of the tree",
            "expectedDataType": [
              "int",
              None
            ],
            "defaultValue": 5,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Max Depth",
            "allowedDataType": [
              "int",
              None
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_samples_split",
            "valueRange": [
              0,
              100
            ],
            "description": "The minimum number of samples required to split an internal node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 2,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Instances For Split",
            "allowedDataType": [
              "int",
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_samples_leaf",
            "valueRange": [
              1,
              100
            ],
            "description": "The minimum number of samples required to be at a leaf node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Instances For Leaf Node",
            "allowedDataType": [
              "int",
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_impurity_decrease",
            "valueRange": [
              0,
              1
            ],
            "description": "A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Impurity Decrease cutoff for Split",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "n_estimators",
            "valueRange": [
              10,
              1000
            ],
            "description": "The number of trees in the forest",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 10,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "No of Estimators",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": -1,
                "displayName": "All",
                "selected": True
              },
              {
                "name": 1,
                "displayName": "1 core",
                "selected": False
              },
              {
                "name": 2,
                "displayName": "2 cores",
                "selected": False
              },
              {
                "name": 3,
                "displayName": "3 cores",
                "selected": False
              },
              {
                "name": 4,
                "displayName": "4 cores",
                "selected": False
              }
            ],
            "displayName": "No Of Jobs",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "n_jobs",
            "allowedDataType": [
              "int"
            ],
            "description": "Number of CPU cores to be used when parallelizing over classes",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "gini",
                "displayName": "Gini Impurity",
                "selected": True
              },
              {
                "name": "entropy",
                "displayName": "Entropy",
                "selected": False
              }
            ],
            "displayName": "Criterion",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "criterion",
            "allowedDataType": [
              "string"
            ],
            "description": "The function to measure the quality of a split",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_leaf_nodes",
            "valueRange": [],
            "description": "The maximum of number of leaf nodes",
            "expectedDataType": [
              "int",
              None
            ],
            "defaultValue": None,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Max Leaf Nodes",
            "allowedDataType": [
              "int",
              None
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "random_state",
            "valueRange": [
              1,
              100
            ],
            "description": "The seed of the pseudo random number generator to use when shuffling the data",
            "expectedDataType": [
              "int",
              None
            ],
            "defaultValue": None,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Random Seed",
            "allowedDataType": [
              "int",
              None
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": False
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Bootstrap Sampling",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "bootstrap",
            "allowedDataType": [
              "bool"
            ],
            "description": "It defines whether bootstrap samples are used when building trees",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "use out-of-bag samples",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "oob_score",
            "allowedDataType": [
              "bool"
            ],
            "description": "It defines whether to use out-of-bag samples to estimate the R^2 on unseen data",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Warm Start",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "warm_start",
            "allowedDataType": [
              "bool"
            ],
            "description": "When set to True, reuse the solution of the previous call to fit as initialization",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "None",
                "displayName": "None",
                "selected": False
              },
              {
                "name": "balanced",
                "displayName": "balanced",
                "selected": False
              }
            ],
            "displayName": "Class Weight",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "class_weight",
            "allowedDataType": [
              "bool"
            ],
            "description": "Weights associated with classes of the target column",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "XGBoost",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8xgb",
        "description": "A machine learning technique that produces an ensemble of multiple decision tree\n            models to predict categorical variables. It is highly preferred to leverage\n            computational power to build scalable and accurate models.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "eta",
            "valueRange": [
              0,
              1
            ],
            "description": "It is the step size shrinkage used to prevent Overfitting",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.3,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Learning Rate",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "gamma",
            "valueRange": [
              0,
              100
            ],
            "description": "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Loss Reduction",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_depth",
            "valueRange": [
              0,
              100
            ],
            "description": "The maximum depth of a tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 6,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Depth",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_child_weight",
            "valueRange": [
              0,
              100
            ],
            "description": "The Minimum sum of Instance weight needed in a child node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Minimum Child Weight",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "subsample",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of the training instance",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Subsampling Ratio",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bytree",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of columns when constructing each tree",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "subsample ratio of columns for each tree",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bylevel",
            "valueRange": [
              0.1,
              1
            ],
            "description": "Subsample ratio of columns for each split in each level",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "subsample ratio of columns for each split",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "gbtree",
                "displayName": "gbtree",
                "selected": True
              },
              {
                "name": "dart",
                "displayName": "dart",
                "selected": True
              },
              {
                "name": "gblinear",
                "displayName": "gblinear",
                "selected": True
              }
            ],
            "displayName": "Booster Function",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "booster",
            "allowedDataType": [
              "string"
            ],
            "description": "The booster function to be used",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "auto",
                "displayName": "auto",
                "selected": True
              },
              {
                "name": "exact",
                "displayName": "exact",
                "selected": True
              },
              {
                "name": "approx",
                "displayName": "approx",
                "selected": True
              },
              {
                "name": "hist",
                "displayName": "hist",
                "selected": True
              },
              {
                "name": "gpu_exact",
                "displayName": "gpu_exact",
                "selected": True
              },
              {
                "name": "gpu_hist",
                "displayName": "gpu_hist",
                "selected": True
              }
            ],
            "displayName": "Tree Construction Algorithm",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "tree_method",
            "allowedDataType": [
              "string"
            ],
            "description": "The Tree construction algorithm used in XGBoost",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "default",
                "displayName": "Create New Trees",
                "selected": True
              },
              {
                "name": "update",
                "displayName": "Update Trees",
                "selected": True
              }
            ],
            "displayName": "Process Type",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "process_type",
            "allowedDataType": [
              "string"
            ],
            "description": "Boosting process to run",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": 0,
                "displayName": "True",
                "selected": False
              },
              {
                "name": 1,
                "displayName": "False",
                "selected": True
              }
            ],
            "displayName": "Print Messages on Console",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "silent",
            "allowedDataType": [
              "int"
            ],
            "description": "Runtime Message Printing",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "cpu_predictor",
                "displayName": "Multicore CPU prediction algorithm",
                "selected": True
              },
              {
                "name": "gpu_predictor",
                "displayName": "Prediction using GPU",
                "selected": True
              }
            ],
            "displayName": "Type of Predictor Algorithm",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "predictor",
            "allowedDataType": [
              "string"
            ],
            "description": "The type of predictor algorithm to use",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "naive bayes",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8nb",
        "description": "The multinomial Naive Bayes classifier is suitable for classification with discrete\n            features (e.g., word counts for text classification).\n            The multinomial distribution normally requires integer feature counts.\n            However, in practice, fractional counts such as tf-idf may also work.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "alpha",
            "valueRange": [
              0,
              1
            ],
            "description": "Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Alpha",
            "allowedDataType": [
              "float"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "Neural Network (Sklearn)",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8mlp",
        "description": "This model optimizes the log-loss function using LBFGS or stochastic gradient descent.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "className": "max_iter_nn",
            "name": "max_iter",
            "valueRange": [
              10,
              400
            ],
            "description": "Maximum number of iterations to be attempted for solver operations",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 200,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Solver Iterations",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "className": "tol_nn",
            "name": "tol",
            "valueRange": [
              3,
              10
            ],
            "description": "Tolerance for the stopping criteria",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 4,
            "uiElemType": "slider",
            "neural": True,
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Convergence tolerance of iterations(e^-n)",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "epsilon",
            "valueRange": [
              3,
              10
            ],
            "description": "Value for numerical stability in adam.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 8,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Epsilon",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "n_iter_no_change",
            "valueRange": [
              3,
              10
            ],
            "description": "Maximum number of epochs to not meet tol improvement.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 10,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "No of Iteration",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "adam",
                "displayName": "adam",
                "selected": True
              },
              {
                "name": "lbfgs",
                "displayName": "lbfgs",
                "selected": False
              },
              {
                "name": "sgd",
                "displayName": "sgd",
                "selected": False
              }
            ],
            "displayName": "Solver Used",
            "display": True,
            "paramType": "list",
            "className": "solver_nn",
            "hyperpatameterTuningCandidate": True,
            "name": "solver",
            "allowedDataType": [
              "string"
            ],
            "description": "The solver for weight optimization.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "relu",
                "displayName": "relu",
                "selected": True
              },
              {
                "name": "identity",
                "displayName": "identity",
                "selected": False
              },
              {
                "name": "logistic",
                "displayName": "logistic",
                "selected": False
              },
              {
                "name": "tanh",
                "displayName": "tanh",
                "selected": False
              }
            ],
            "displayName": "Activation",
            "display": True,
            "paramType": "list",
            "className": "activation_nn",
            "hyperpatameterTuningCandidate": True,
            "name": "activation",
            "allowedDataType": [
              "string"
            ],
            "description": "Activation function for the hidden layer.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "True",
                "displayName": "True",
                "selected": True
              },
              {
                "name": "False",
                "displayName": "False",
                "selected": False
              }
            ],
            "displayName": "Shuffle",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "shuffle",
            "allowedDataType": [
              "bool"
            ],
            "description": "Whether to shuffle samples in each iteration.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "constant",
                "displayName": "constant",
                "selected": True
              },
              {
                "name": "invscaling",
                "displayName": "invscaling",
                "selected": False
              },
              {
                "name": "adaptive",
                "displayName": "adaptive",
                "selected": False
              }
            ],
            "displayName": "Learning Rate",
            "display": True,
            "paramType": "list",
            "className": "learning_rate_nn",
            "hyperpatameterTuningCandidate": True,
            "name": "learning_rate",
            "allowedDataType": [
              "string"
            ],
            "description": "Learning rate schedule for weight updates.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "batch_size",
            "valueRange": [],
            "description": "Size of minibatches for stochastic optimizers.",
            "expectedDataType": [
              "int",
              "string"
            ],
            "defaultValue": [
              {
                "name": "auto",
                "displayName": "auto",
                "selected": True
              },
              {
                "name": 8,
                "displayName": "8",
                "selected": False
              },
              {
                "name": 16,
                "displayName": "16",
                "selected": False
              },
              {
                "name": 32,
                "displayName": "32",
                "selected": False
              },
              {
                "name": 64,
                "displayName": "64",
                "selected": False
              },
              {
                "name": 128,
                "displayName": "128",
                "selected": False
              }
            ],
            "uiElemType": "checkBox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Batch Size",
            "allowedDataType": [
              "int",
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "True",
                "displayName": "True",
                "selected": True
              },
              {
                "name": "False",
                "displayName": "False",
                "selected": False
              }
            ],
            "displayName": "Nesterovs momentum",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "nesterovs_momentum",
            "allowedDataType": [
              "bool"
            ],
            "description": "Whether to use Nesterovs momentum.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Early Stop",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "early_stopping",
            "allowedDataType": [
              "bool"
            ],
            "description": "Whether to use early stopping to terminate training when validation score is not improving.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Warm Start",
            "display": True,
            "paramType": "list",
            "className": "warm_start_nn",
            "hyperpatameterTuningCandidate": False,
            "name": "warm_start",
            "allowedDataType": [
              "bool"
            ],
            "description": "It reuses the solution of the previous call to fit as initialization",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "False",
                "displayName": "False",
                "selected": True
              },
              {
                "name": "True",
                "displayName": "True",
                "selected": False
              }
            ],
            "displayName": "Verbose",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "verbose",
            "allowedDataType": [
              "bool"
            ],
            "description": "Whether to print progress messages to stdout.",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "bool"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "hidden_layer_sizes",
            "valueRange": [
              1,
              100
            ],
            "description": "Number of neurons in the ith hidden layer.",
            "expectedDataType": [
              "tuple"
            ],
            "defaultValue": 100,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Hidden Layer Size",
            "allowedDataType": [
              "int",
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "learning_rate_init",
            "valueRange": [
              0.0001,
              20
            ],
            "description": "Controls the step-size in updating the weights.",
            "expectedDataType": [
              "double"
            ],
            "defaultValue": 0.001,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Learning Rate Initialize",
            "allowedDataType": [
              "double"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "className": "alpha_nn",
            "name": "alpha",
            "valueRange": [
              0,
              5
            ],
            "description": "L2 penalty (regularization term) parameter.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.0001,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Alpha",
            "allowedDataType": [
              "int",
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "power_t",
            "valueRange": [
              0.1,
              20
            ],
            "description": "The exponent for inverse scaling learning rate.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.5,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Power T",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": False,
            "acceptedValue": None,
            "name": "random_state",
            "valueRange": [
              1,
              100
            ],
            "description": "The seed of the pseudo random number generator to use when shuffling the data",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 42,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Random Seed",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "momentum",
            "valueRange": [
              0,
              1
            ],
            "description": "Momentum for gradient descent update.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.9,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Momentum",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "validation_fraction",
            "valueRange": [
              0,
              1
            ],
            "description": "The proportion of training data to set aside as validation set for early stopping.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.1,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Validation Fraction",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "beta_1 ",
            "valueRange": [
              0,
              1
            ],
            "description": "Exponential decay rate for estimates of first moment vector in adam.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.9,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Beta 1",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "beta_2 ",
            "valueRange": [
              0,
              1
            ],
            "description": "Exponential decay rate for estimates of second moment vector in adam.",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.999,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Beta 2",
            "allowedDataType": [
              "float"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "Neural Network (TensorFlow)",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8tfx",
        "description": "An end-to-end open source platform for machine learning. TensorFlow is a rich system for managing all aspects of a machine learning system.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "layer",
            "valueRange": None,
            "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "Dense",
                "displayName": "Dense",
                "parameters": [
                  {
                    "defaultValue": [
                      {
                        "name": "elu",
                        "displayName": "elu",
                        "selected": False
                      },
                      {
                        "name": "exponential",
                        "displayName": "exponential",
                        "selected": False
                      },
                      {
                        "name": "hard_sigmoid",
                        "displayName": "hard_sigmoid",
                        "selected": False
                      },
                      {
                        "name": "linear",
                        "displayName": "Linear",
                        "selected": False
                      },
                      {
                        "name": "relu",
                        "displayName": "relu",
                        "selected": False
                      },
                      {
                        "name": "selu",
                        "displayName": "selu",
                        "selected": False
                      },
                      {
                        "name": "sigmoid",
                        "displayName": "sigmoid",
                        "selected": False
                      },
                      {
                        "name": "softmax",
                        "displayName": "softmax",
                        "selected": False
                      },
                      {
                        "name": "softplus",
                        "displayName": "softplus",
                        "selected": False
                      },
                      {
                        "name": "softsign",
                        "displayName": "softsign",
                        "selected": False
                      },
                      {
                        "name": "tanh",
                        "displayName": "tanh",
                        "selected": False
                      }
                    ],
                    "displayName": "Activation",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "activation",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Activation function for the hidden layer.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "display": True,
                    "acceptedValue": None,
                    "name": "units",
                    "valueRange": [
                      0.1,
                      1
                    ],
                    "description": "Dimensionality of the output space.",
                    "expectedDataType": [
                      "float"
                    ],
                    "defaultValue": 1,
                    "uiElemType": "slider",
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": False,
                    "displayName": "Units",
                    "allowedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": False
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "Use Bias",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": False,
                    "name": "use_bias",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "Whether the layer uses a bias vector.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": True
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "Batch Normalization",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": False,
                    "name": "batch_normalization",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "It is used to normalize the input layer by adjusting and scaling the activations.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "Zeros",
                        "displayName": "Zeros",
                        "selected": True
                      },
                      {
                        "name": "Ones",
                        "displayName": "Ones",
                        "selected": False
                      },
                      {
                        "name": "Constant",
                        "displayName": "Constant",
                        "selected": False
                      },
                      {
                        "name": "RandomNormal",
                        "displayName": "RandomNormal",
                        "selected": False
                      },
                      {
                        "name": "RandomUniform",
                        "displayName": "RandomUniform",
                        "selected": False
                      },
                      {
                        "name": "TruncatedNormal",
                        "displayName": "TruncatedNormal",
                        "selected": False
                      },
                      {
                        "name": "VarianceScaling",
                        "displayName": "VarianceScaling",
                        "selected": False
                      },
                      {
                        "name": "Orthogonal",
                        "displayName": "Orthogonal",
                        "selected": False
                      },
                      {
                        "name": "Identity",
                        "displayName": "Identity",
                        "selected": False
                      },
                      {
                        "name": "lecun_uniform",
                        "displayName": "lecun_uniform",
                        "selected": False
                      },
                      {
                        "name": "glorot_normal",
                        "displayName": "glorot_normal",
                        "selected": False
                      },
                      {
                        "name": "glorot_uniform",
                        "displayName": "glorot_uniform",
                        "selected": False
                      },
                      {
                        "name": "he_normal",
                        "displayName": "he_normal",
                        "selected": False
                      },
                      {
                        "name": "lecun_normal",
                        "displayName": "lecun_normal",
                        "selected": False
                      },
                      {
                        "name": "he_uniform",
                        "displayName": "he_uniform",
                        "selected": False
                      }
                    ],
                    "displayName": "Kernel Initializer",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "kernel_initializer",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Initializer for the kernel weights matrix.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "Zeros",
                        "displayName": "Zeros",
                        "selected": True
                      },
                      {
                        "name": "Ones",
                        "displayName": "Ones",
                        "selected": False
                      },
                      {
                        "name": "Constant",
                        "displayName": "Constant",
                        "selected": False
                      },
                      {
                        "name": "RandomNormal",
                        "displayName": "RandomNormal",
                        "selected": False
                      },
                      {
                        "name": "RandomUniform",
                        "displayName": "RandomUniform",
                        "selected": False
                      },
                      {
                        "name": "TruncatedNormal",
                        "displayName": "TruncatedNormal",
                        "selected": False
                      },
                      {
                        "name": "VarianceScaling",
                        "displayName": "VarianceScaling",
                        "selected": False
                      },
                      {
                        "name": "Orthogonal",
                        "displayName": "Orthogonal",
                        "selected": False
                      },
                      {
                        "name": "Identity",
                        "displayName": "Identity",
                        "selected": False
                      },
                      {
                        "name": "lecun_uniform",
                        "displayName": "lecun_uniform",
                        "selected": False
                      },
                      {
                        "name": "glorot_normal",
                        "displayName": "glorot_normal",
                        "selected": False
                      },
                      {
                        "name": "glorot_uniform",
                        "displayName": "glorot_uniform",
                        "selected": False
                      },
                      {
                        "name": "he_normal",
                        "displayName": "he_normal",
                        "selected": False
                      },
                      {
                        "name": "lecun_normal",
                        "displayName": "lecun_normal",
                        "selected": False
                      },
                      {
                        "name": "he_uniform",
                        "displayName": "he_uniform",
                        "selected": False
                      }
                    ],
                    "displayName": "Bias Initializer",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "bias_initializer",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Initializer for the bias vector.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "l1",
                        "displayName": "l1",
                        "selected": True
                      },
                      {
                        "name": "l2",
                        "displayName": "l2",
                        "selected": False
                      },
                      {
                        "name": "l1_l2",
                        "displayName": "l1_l2",
                        "selected": False
                      }
                    ],
                    "displayName": "Kernel Regularizer",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "kernel_regularizer",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Regularizer function applied to the kernel weights matrix.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "l1",
                        "displayName": "l1",
                        "selected": True
                      },
                      {
                        "name": "l2",
                        "displayName": "l2",
                        "selected": False
                      },
                      {
                        "name": "l1_l2",
                        "displayName": "l1_l2",
                        "selected": False
                      }
                    ],
                    "displayName": "Bias Regularizer",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "bias_regularizer",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Regularizer function applied to the bias vector.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "l1",
                        "displayName": "l1",
                        "selected": True
                      },
                      {
                        "name": "l2",
                        "displayName": "l2",
                        "selected": False
                      },
                      {
                        "name": "l1_l2",
                        "displayName": "l1_l2",
                        "selected": False
                      }
                    ],
                    "displayName": "Activity Regularizer",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "activity_regularizer",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Regularizer function applied to the output of the layer.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "MaxNorm",
                        "displayName": "MaxNorm",
                        "selected": True
                      },
                      {
                        "name": "NonNeg",
                        "displayName": "NonNeg",
                        "selected": False
                      },
                      {
                        "name": "UnitNorm",
                        "displayName": "UnitNorm",
                        "selected": False
                      },
                      {
                        "name": "MinMaxNorm",
                        "displayName": "MinMaxNorm",
                        "selected": False
                      }
                    ],
                    "displayName": "Kernel Constraint",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "kernel_constraint",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Constraint function applied to the kernel weights matrix.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "MaxNorm",
                        "displayName": "MaxNorm",
                        "selected": True
                      },
                      {
                        "name": "NonNeg",
                        "displayName": "NonNeg",
                        "selected": False
                      },
                      {
                        "name": "UnitNorm",
                        "displayName": "UnitNorm",
                        "selected": False
                      },
                      {
                        "name": "MinMaxNorm",
                        "displayName": "MinMaxNorm",
                        "selected": False
                      }
                    ],
                    "displayName": "Bias Constraint",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "bias_constraint",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Constraint function applied to the bias vector.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": True
              },
              {
                "name": "Dropout",
                "displayName": "Dropout",
                "parameters": [
                  {
                    "display": True,
                    "acceptedValue": None,
                    "name": "rate",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "Fraction of the input units to drop.",
                    "expectedDataType": [
                      "float"
                    ],
                    "defaultValue": 0,
                    "uiElemType": "textbox",
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": False,
                    "displayName": "Rate",
                    "allowedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Layer",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "loss",
            "valueRange": None,
            "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "sparse_categorical_crossentropy",
                "displayName": "sparse_categorical_crossentropy",
                "selected": True
              },
              {
                "name": "squared_hinge",
                "displayName": "squared_hinge",
                "selected": False
              },
              {
                "name": "hinge",
                "displayName": "hinge",
                "selected": False
              },
              {
                "name": "categorical_hinge",
                "displayName": "categorical_hinge",
                "selected": False
              },
              {
                "name": "categorical_crossentropy",
                "displayName": "categorical_crossentropy",
                "selected": False
              },
              {
                "name": "binary_crossentropy",
                "displayName": "binary_crossentropy",
                "selected": False
              },
              {
                "name": "kullback_leibler_divergence",
                "displayName": "kullback_leibler_divergence",
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Loss",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "optimizer",
            "valueRange": None,
            "description": "Method used to minimize the loss function.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "SGD",
                "displayName": "SGD",
                "selected": True
              },
              {
                "name": "RMSprop",
                "displayName": "RMSprop",
                "selected": False
              },
              {
                "name": "Adagrad",
                "displayName": "Adagrad",
                "selected": False
              },
              {
                "name": "Adadelta",
                "displayName": "Adadelta",
                "selected": False
              },
              {
                "name": "Adam",
                "displayName": "Adam",
                "selected": False
              },
              {
                "name": "Adamax",
                "displayName": "Adamax",
                "selected": False
              },
              {
                "name": "Nadam",
                "displayName": "Nadam",
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Optimizer",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": 100,
            "name": "batch_size",
            "valueRange": None,
            "description": "The number of training examples in one Forward/Backward Pass.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 0,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Batch Size",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": 100,
            "name": "number_of_epochs",
            "valueRange": None,
            "description": "An epoch refers to one cycle through the full training data-set.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 100,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Number of Epochs",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "metrics",
            "valueRange": None,
            "description": "List of metrics to be evaluated by the model during training And testing.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "sparse_categorical_crossentropy",
                "displayName": "sparse_categorical_crossentropy",
                "selected": True
              },
              {
                "name": "binary_crossentropy",
                "displayName": "binary_crossentropy",
                "selected": False
              },
              {
                "name": "categorical_accuracy",
                "displayName": "categorical_accuracy",
                "selected": False
              },
              {
                "name": "categorical_crossentropy",
                "displayName": "categorical_crossentropy",
                "selected": False
              },
              {
                "name": "FalseNegatives",
                "displayName": "FalseNegatives",
                "selected": False
              },
              {
                "name": "FalsePositives",
                "displayName": "FalsePositives",
                "selected": False
              },
              {
                "name": "sparse_categorical_accuracy",
                "displayName": "sparse_categorical_accuracy",
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Metrics",
            "allowedDataType": [
              "string"
            ]
          }
        ],
        "selected": True,
        "tensorflow_params": {
          "hidden_layer_info": {}
        }
      },
      {
        "algorithmName": "Neural Network (PyTorch)",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8nnpt",
        "description": "A python based library built to provide flexibility as a deep learning development platform. It is an open source machine learning library based on the Torch library, used for applications such as computer vision and natural language processing.",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "layer",
            "valueRange": None,
            "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "Linear",
                "displayName": "Linear",
                "parameters": [
                  {
                    "defaultValue": [
                      {
                        "name": "ELU",
                        "displayName": "ELU",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "alpha",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "alpha",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the alpha value for the ELU formulation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Hardshrink",
                        "displayName": "Hardshrink",
                        "parameters": [
                          {
                            "defaultValue": 0.5,
                            "displayName": "lambd",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "lambd",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the lambda value for the Hardshrink formulation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Hardtanh",
                        "displayName": "Hardtanh",
                        "parameters": [
                          {
                            "defaultValue": -1,
                            "displayName": "min_val",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "min_val",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "minimum value of the linear region range.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 1,
                            "displayName": "max_val",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "max_val",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "maximum value of the linear region range.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "LeakyReLU",
                        "displayName": "LeakyReLU",
                        "parameters": [
                          {
                            "defaultValue": 0.01,
                            "displayName": "negative_slope",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "negative_slope",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Controls the angle of the negative slope.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "LogSigmoid",
                        "displayName": "LogSigmoid",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "MultiheadAttention",
                        "displayName": "MultiheadAttention",
                        "parameters": [
                          {
                            "displayName": "embed_dim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "embed_dim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "total dimension of the model.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": None,
                            "displayName": "num_heads",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "num_heads",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "parallel attention heads.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": 0,
                            "displayName": "dropout",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "dropout",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "a Dropout layer on attn_output_weights.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": False
                              }
                            ],
                            "displayName": "bias",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "bias",
                            "allowedDataType": [
                              "bool"
                            ],
                            "description": "",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": False
                              }
                            ],
                            "displayName": "add_bias_kv",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "add_bias_kv",
                            "allowedDataType": [
                              "bool"
                            ],
                            "description": "add bias to the key and value sequences at dim=0.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": False
                              }
                            ],
                            "displayName": "add_zero_attn",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "add_zero_attn",
                            "allowedDataType": [
                              "bool"
                            ],
                            "description": "add a new batch of zeros to the key and Value sequences at dim=1.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          },
                          {
                            "defaultValue": None,
                            "displayName": "kdim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "kdim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "total number of features in key.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": None,
                            "displayName": "vdim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "vdim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "PreLU",
                        "displayName": "PreLU",
                        "parameters": [
                          {
                            "defaultValue": [
                              {
                                "name": "1",
                                "displayName": "1",
                                "selected": True
                              },
                              {
                                "name": "no of channels",
                                "displayName": "No of Channels",
                                "selected": False
                              }
                            ],
                            "displayName": "num_parameters",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "num_parameters",
                            "allowedDataType": [
                              "string"
                            ],
                            "description": "number of alpha to learn.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "string"
                            ]
                          },
                          {
                            "defaultValue": 0.25,
                            "displayName": "init",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "init",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the initial value of alpha.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "ReLU",
                        "displayName": "ReLU",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "ReLU6",
                        "displayName": "ReLU6",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "RreLU",
                        "displayName": "RreLU",
                        "parameters": [
                          {
                            "defaultValue": 0.125,
                            "displayName": "lower",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "lower",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "lower bound of the uniform distribution.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 0.33,
                            "displayName": "upper",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "upper",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "upper bound of the uniform distribution.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "SELU",
                        "displayName": "SELU",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "CELU",
                        "displayName": "CELU",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "alpha",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "alpha",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the alpha value for the CELU formulation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "GELU",
                        "displayName": "GELU",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "Sigmoid",
                        "displayName": "Sigmoid",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "Softplus",
                        "displayName": "Softplus",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "beta",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "beta",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the beta value for the Softplus formulation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 20,
                            "displayName": "threshold",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "threshold",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "values above this revert to a linear function.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Softshrink",
                        "displayName": "Softshrink",
                        "parameters": [
                          {
                            "defaultValue": 0.5,
                            "displayName": "lambd",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "lambd",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the lambda value for the Softshrink formulation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Softsign",
                        "displayName": "Softsign",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "Tanh",
                        "displayName": "Tanh",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "Tanhshrink",
                        "displayName": "Tanhshrink",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "Threshold",
                        "displayName": "Threshold",
                        "parameters": [
                          {
                            "defaultValue": None,
                            "displayName": "threshold",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "threshold",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "The value to threshold at.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": None,
                            "displayName": "value",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "value",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "The value to replace with.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Softmin",
                        "displayName": "Softmin",
                        "parameters": [
                          {
                            "defaultValue": None,
                            "displayName": "dim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "dim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "A dimension along which Softmin will be computed.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Softmax",
                        "displayName": "Softmax",
                        "parameters": [
                          {
                            "defaultValue": None,
                            "displayName": "dim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "dim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "A dimension along which Softmax will be computed.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Softmax2d",
                        "displayName": "Softmax2d",
                        "parameters": None,
                        "selected": False
                      },
                      {
                        "name": "LogSoftmax",
                        "displayName": "LogSoftmax",
                        "parameters": [
                          {
                            "defaultValue": None,
                            "displayName": "dim",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "dim",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "A dimension along which LogSoftmax will be computed.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "AdaptiveLogSoftmaxWithLoss",
                        "displayName": "AdaptiveLogSoftmaxWithLoss",
                        "parameters": [
                          {
                            "defaultValue": None,
                            "displayName": "n_classes",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "n_classes",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "Number of classes in the dataset.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": None,
                            "displayName": "cutoffs",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "cutoffs",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "Cutoffs used to assign targets to their buckets.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": 4,
                            "displayName": "div_value",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "div_value",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "value used as an exponent to compute sizes of the clusters.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": False
                              }
                            ],
                            "displayName": "head_bias",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "head_bias",
                            "allowedDataType": [
                              "bool"
                            ],
                            "description": "If True, adds a bias term to the 'head' of the Adaptive softmax.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          }
                        ],
                        "selected": False
                      }
                    ],
                    "displayName": "Activation",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "activation",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Activation function for the hidden layer.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "Dropout",
                        "displayName": "Dropout",
                        "parameters": [
                          {
                            "defaultValue": 0.5,
                            "displayName": "p",
                            "display": True,
                            "paramType": "number",
                            "allowedDataType": [
                              "float"
                            ],
                            "hyperpatameterTuningCandidate": True,
                            "name": "p",
                            "valueRange": [
                              0,
                              1
                            ],
                            "description": "probability of an element to be dropped.",
                            "uiElemType": "slider",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      }
                    ],
                    "displayName": "Dropout",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "dropout",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "During training, randomly zeroes some of the elements of the input tensor with probability p using samples from a Bernoulli distribution.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "BatchNorm1d",
                        "displayName": "BatchNorm1d",
                        "parameters": [
                          {
                            "displayName": "num_features",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "num_features",
                            "allowedDataType": [
                              "int"
                            ],
                            "description": "C from an expected input of size (N,C,L) or L from input of size (N, L).",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "int"
                            ]
                          },
                          {
                            "defaultValue": 0.00001,
                            "displayName": "eps",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "eps",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "a value added to the denominator for numerical stability.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 0.1,
                            "displayName": "momentum",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "momentum",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "the value used for the running_mean and running_var computation.",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": True
                              }
                            ],
                            "displayName": "affine",
                            "display": True,
                            "paramType": "list",
                            "allowedDataType": [
                              "bool"
                            ],
                            "hyperpatameterTuningCandidate": True,
                            "name": "affine",
                            "valueRange": [
                              0,
                              1
                            ],
                            "description": "a boolean value that when set to True, this module has learnable affine parameters, initialized the same way as done for batch normalization.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "False",
                                "displayName": "False",
                                "selected": False
                              },
                              {
                                "name": "True",
                                "displayName": "True",
                                "selected": True
                              }
                            ],
                            "displayName": "track_running_stats",
                            "display": True,
                            "paramType": "list",
                            "allowedDataType": [
                              "bool"
                            ],
                            "hyperpatameterTuningCandidate": True,
                            "name": "track_running_stats",
                            "valueRange": [
                              0,
                              1
                            ],
                            "description": "a boolean value that when set to True, this module tracks the running mean and variance, and when set to False, this module does not track such statistics and always uses batch statistics in both training and eval modes.",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "bool"
                            ]
                          }
                        ],
                        "selected": False
                      }
                    ],
                    "displayName": "Batch Normalization",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "batchnormalization",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "Applies Batch Normalization over a 2D or 3D input (a mini-batch of 1D inputs with optional additional channel dimension) as described in the paper.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": None,
                    "displayName": "Input Units",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "units_ip",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "Input Units parameter for the hidden layer.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": None,
                    "displayName": "Output Units",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "units_op",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "Output Units parameter for the hidden layer.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "Uniform",
                        "displayName": "Uniform",
                        "parameters": [
                          {
                            "defaultValue": 0,
                            "displayName": "lower bound",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "lower_bound",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 1,
                            "displayName": "upper bound",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "upper_bound",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Normal",
                        "displayName": "Normal",
                        "parameters": [
                          {
                            "defaultValue": 0,
                            "displayName": "mean",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "mean",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 1,
                            "displayName": "std",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "std",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Constant",
                        "displayName": "Constant",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "val",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "val",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with the value {val}",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "displayName": "Ones",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Ones",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Zeros",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Zeros",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Eyes",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Eyes",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Default",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Default",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Other",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Other",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": True,
                        "expectedDataType": [
                          "string"
                        ]
                      }
                    ],
                    "displayName": "bias_init",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "bias_init",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "Bias initialisation parameter for the hidden layer.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "Uniform",
                        "displayName": "Uniform",
                        "parameters": [
                          {
                            "defaultValue": 0,
                            "displayName": "lower bound",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "lower_bound",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 1,
                            "displayName": "upper bound",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "upper_bound",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Normal",
                        "displayName": "Normal",
                        "parameters": [
                          {
                            "defaultValue": 0,
                            "displayName": "mean",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "mean",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 1,
                            "displayName": "std",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "std",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Constant",
                        "displayName": "Constant",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "val",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "val",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with the value {val}",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "displayName": "Ones",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Ones",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Zeros",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Zeros",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Eyes",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Eyes",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "displayName": "Dirac",
                        "display": True,
                        "paramType": "number",
                        "hyperpatameterTuningCandidate": True,
                        "name": "Dirac",
                        "allowedDataType": [
                          "string"
                        ],
                        "description": "Input Units parameter for the hidden layer.",
                        "uiElemType": "textBox",
                        "selected": False,
                        "expectedDataType": [
                          "string"
                        ]
                      },
                      {
                        "name": "Xavier_Uniform",
                        "displayName": "Xavier Uniform",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "gain",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "gain",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Xavier_Normal",
                        "displayName": "Xavier Normal",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "gain",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "gain",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Kaiming_Normal",
                        "displayName": "Kaiming Normal",
                        "parameters": [
                          {
                            "defaultValue": 0,
                            "displayName": "a",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "a",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "fan_in",
                                "displayName": "fan_in",
                                "selected": True
                              },
                              {
                                "name": "fan_out",
                                "displayName": "fan_out",
                                "selected": False
                              }
                            ],
                            "displayName": "mode",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "mode",
                            "allowedDataType": [
                              "string"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "string"
                            ]
                          },
                          {
                            "defaultValue": [
                              {
                                "name": "leaky_relu",
                                "displayName": "leaky_relu",
                                "selected": True
                              },
                              {
                                "name": "relu",
                                "displayName": "relu",
                                "selected": False
                              }
                            ],
                            "displayName": "nonlinearity",
                            "display": True,
                            "paramType": "list",
                            "hyperpatameterTuningCandidate": True,
                            "name": "nonlinearity",
                            "allowedDataType": [
                              "string"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "checkbox",
                            "expectedDataType": [
                              "string"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Orthogonal",
                        "displayName": "Orthogonal",
                        "parameters": [
                          {
                            "defaultValue": 1,
                            "displayName": "gain",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "gain",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Sparse",
                        "displayName": "Sparse",
                        "parameters": [
                          {
                            "defaultValue": 0.5,
                            "displayName": "sparsity",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "sparsity",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          },
                          {
                            "defaultValue": 0.01,
                            "displayName": "std",
                            "display": True,
                            "paramType": "number",
                            "hyperpatameterTuningCandidate": True,
                            "name": "std",
                            "allowedDataType": [
                              "float"
                            ],
                            "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
                            "uiElemType": "textBox",
                            "expectedDataType": [
                              "float"
                            ]
                          }
                        ],
                        "selected": False
                      },
                      {
                        "name": "Default",
                        "displayName": "Default",
                        "parameters": None,
                        "selected": True
                      }
                    ],
                    "displayName": "weight_init",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_init",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "Weight initialisation parameter for the hidden layer.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "True",
                        "displayName": "True",
                        "parameters": [
                          [
                            {
                              "defaultValue": 0.3,
                              "displayName": "min",
                              "display": True,
                              "paramType": "number",
                              "hyperpatameterTuningCandidate": True,
                              "name": "min",
                              "allowedDataType": [
                                "float"
                              ],
                              "description": "minimum value.",
                              "uiElemType": "textBox",
                              "expectedDataType": [
                                "float"
                              ]
                            },
                            {
                              "defaultValue": 0.7,
                              "displayName": "max",
                              "display": True,
                              "paramType": "number",
                              "hyperpatameterTuningCandidate": True,
                              "name": "max",
                              "allowedDataType": [
                                "float"
                              ],
                              "description": "maximum value.",
                              "uiElemType": "textBox",
                              "expectedDataType": [
                                "float"
                              ]
                            }
                          ]
                        ],
                        "selected": False
                      },
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": True
                      }
                    ],
                    "displayName": "weight constraint",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_constraint",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "clipping the Weights.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  }
                ],
                "selected": True
              }
            ],
            "uiElemType": "textBox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Layer",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "loss",
            "valueRange": None,
            "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "CrossEntropyLoss",
                "displayName": "CrossEntropyLoss",
                "parameters": [
                  {
                    "defaultValue": None,
                    "displayName": "weight",
                    "display": True,
                    "paramType": "tensor",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight",
                    "allowedDataType": [
                      "tensor"
                    ],
                    "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "tensor"
                    ]
                  },
                  {
                    "defaultValue": None,
                    "displayName": "ignore_index",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "ignore_index",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "Specifies a target value that is ignored and does not contribute to the input gradient.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "CTCLoss",
                "displayName": "CTCLoss",
                "parameters": [
                  {
                    "defaultValue": 0,
                    "displayName": "blank",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "blank",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "blank label.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": True
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "zero_infinity",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "zero_infinity",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "Whether to zero infinite losses and the associated gradients.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "NLLLoss",
                "displayName": "NLLLoss",
                "parameters": [
                  {
                    "defaultValue": None,
                    "displayName": "weight",
                    "display": True,
                    "paramType": "tensor",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight",
                    "allowedDataType": [
                      "tensor"
                    ],
                    "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "tensor"
                    ]
                  },
                  {
                    "defaultValue": None,
                    "displayName": "ignore_index",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "ignore_index",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "Specifies a target value that is ignored and does not contribute to the input gradient.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "PoissonNLLLoss",
                "displayName": "PoissonNLLLoss",
                "parameters": [
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": False
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "log_input",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "log_input",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "if True the loss is computed as exp(input)-target*input.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": False
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "full",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "full",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "whether to compute full loss, i. e. to add the Stirling approximation term.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "small value to avoid evaluation of log(0) when log_input = False.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "BCELoss",
                "displayName": "BCELoss",
                "parameters": [
                  {
                    "defaultValue": None,
                    "displayName": "weight",
                    "display": True,
                    "paramType": "tensor",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight",
                    "allowedDataType": [
                      "tensor"
                    ],
                    "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "tensor"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "BCEWithLogitsLoss",
                "displayName": "BCEWithLogitsLoss",
                "parameters": [
                  {
                    "defaultValue": None,
                    "displayName": "weight",
                    "display": True,
                    "paramType": "tensor",
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight",
                    "allowedDataType": [
                      "tensor"
                    ],
                    "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "tensor"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  },
                  {
                    "defaultValue": "mean",
                    "displayName": "pos_weight",
                    "display": True,
                    "paramType": "tensor",
                    "hyperpatameterTuningCandidate": True,
                    "name": "pos_weight",
                    "allowedDataType": [
                      "tensor"
                    ],
                    "description": "a weight of positive examples. Must be a vector with length equal to the number of classes.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "tensor"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "SoftMarginLoss",
                "displayName": "SoftMarginLoss",
                "parameters": [
                  {
                    "defaultValue": "mean",
                    "displayName": "reduction",
                    "display": True,
                    "paramType": "list",
                    "allowedDataType": [
                      "string"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "reduction",
                    "valueRange": [
                      "none",
                      "mean",
                      "sum"
                    ],
                    "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Loss",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "optimizer",
            "valueRange": None,
            "description": "Method used to minimize the loss function.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "Adadelta",
                "displayName": "Adadelta",
                "parameters": [
                  {
                    "defaultValue": 0.9,
                    "displayName": "rho",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "rho",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "coefficient used for computing a running average of squared gradients.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.000001,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      0.000001,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "coefficient that scale delta before it is applied to the parameters.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "Adagrad",
                "displayName": "Adagrad",
                "parameters": [
                  {
                    "defaultValue": 0.01,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "lr_decay",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr_decay",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": " learning rate decay.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-10,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-10,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "Adam",
                "displayName": "Adam",
                "parameters": [
                  {
                    "defaultValue": 0.001,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.9,
                      0.999
                    ],
                    "displayName": "betas",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "betas",
                    "valueRange": [
                      [
                        0,
                        1
                      ],
                      [
                        0,
                        1
                      ]
                    ],
                    "description": "coefficients used for computing running averages of gradient and its square.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-10,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": True
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "amsgrad",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "amsgrad",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "AdamW",
                "displayName": "AdamW",
                "parameters": [
                  {
                    "defaultValue": 0.001,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.9,
                      0.999
                    ],
                    "displayName": "betas",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "betas",
                    "valueRange": [
                      [
                        0,
                        1
                      ],
                      [
                        0,
                        1
                      ]
                    ],
                    "description": "coefficients used for computing running averages of gradient and its square.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-8,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.01,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": True
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "amsgrad",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "amsgrad",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "SparseAdam",
                "displayName": "SparseAdam",
                "parameters": [
                  {
                    "defaultValue": 0.001,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.9,
                      0.999
                    ],
                    "displayName": "betas",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "betas",
                    "valueRange": [
                      [
                        0,
                        1
                      ],
                      [
                        0,
                        1
                      ]
                    ],
                    "description": "coefficients used for computing running averages of gradient and its square.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-8,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "Adamax",
                "displayName": "Adamax",
                "parameters": [
                  {
                    "defaultValue": 0.001,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.9,
                      0.999
                    ],
                    "displayName": "betas",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "betas",
                    "valueRange": [
                      [
                        0,
                        1
                      ],
                      [
                        0,
                        1
                      ]
                    ],
                    "description": "coefficients used for computing running averages of gradient and its square.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-8,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "ASGD",
                "displayName": "ASGD",
                "parameters": [
                  {
                    "defaultValue": 0.01,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.0001,
                    "displayName": "lambd",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "lambd",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "decay term.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.75,
                    "displayName": "alpha",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "alpha",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "power for eta update.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.000001,
                    "displayName": "t0",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "t0",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "point at which to start averaging.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "LBFGS",
                "displayName": "LBFGS",
                "parameters": [
                  {
                    "defaultValue": 1,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 20,
                    "displayName": "max_iter",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "max_iter",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "maximal number of iterations per optimization step.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": 25,
                    "displayName": "max_eval",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "max_eval",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "maximal number of function evaluations per optimization step.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": 0.00001,
                    "displayName": "tolerance_grad",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "tolerance_grad",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": " termination tolerance on first order optimality.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-9,
                    "displayName": "tolerance_change",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "tolerance_change",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "termination tolerance on function value/parameter changes.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 100,
                    "displayName": "history_size",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "history_size",
                    "allowedDataType": [
                      "int"
                    ],
                    "description": "update history size.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "int"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "None",
                        "displayName": "None",
                        "selected": True
                      },
                      {
                        "name": "strong_wolfe",
                        "displayName": "strong_wolfe",
                        "selected": False
                      }
                    ],
                    "displayName": "line_search_fn",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "line_search_fn",
                    "allowedDataType": [
                      "string"
                    ],
                    "description": "either 'strong_wolfe' or None.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "string"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "RMSprop",
                "displayName": "RMSprop",
                "parameters": [
                  {
                    "defaultValue": 0.01,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "momentum",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "momentum",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "momentum factor.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0.99,
                    "displayName": "alpha",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "alpha",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "smoothing constant.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 1e-8,
                    "displayName": "eps",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eps",
                    "valueRange": [
                      1e-8,
                      1
                    ],
                    "description": "term added to the denominator to improve numerical stability.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": False
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": True
                      }
                    ],
                    "displayName": "centered",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "centered",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "if True, compute the centered RMSProp, the gradient is normalized By an estimation of its variance.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "Rprop",
                "displayName": "Rprop",
                "parameters": [
                  {
                    "defaultValue": 0.01,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.5,
                      1.2
                    ],
                    "displayName": "eta",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "eta",
                    "valueRange": [
                      [
                        0,
                        5
                      ],
                      [
                        0,
                        5
                      ]
                    ],
                    "description": "pair of (etaminus, etaplUs), that are multiplicative.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      0.000001,
                      50
                    ],
                    "displayName": "step_sizes",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "step_sizes",
                    "valueRange": [
                      [
                        0,
                        5
                      ],
                      [
                        0,
                        5
                      ]
                    ],
                    "description": "a pair of minimal and maximal allowed step sizes.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  }
                ],
                "selected": False
              },
              {
                "name": "SGD",
                "displayName": "SGD",
                "parameters": [
                  {
                    "defaultValue": 0.1,
                    "displayName": "lr",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "lr",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "learning rate.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "momentum",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "momentum",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "momentum factor.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "weight_decay",
                    "display": True,
                    "paramType": "number",
                    "allowedDataType": [
                      "float"
                    ],
                    "hyperpatameterTuningCandidate": True,
                    "name": "weight_decay",
                    "valueRange": [
                      0,
                      0.1
                    ],
                    "description": "weight decay (L2 penalty).",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": 0,
                    "displayName": "dampening",
                    "display": True,
                    "paramType": "number",
                    "hyperpatameterTuningCandidate": True,
                    "name": "dampening",
                    "allowedDataType": [
                      "float"
                    ],
                    "description": "dampening for momentum.",
                    "uiElemType": "textBox",
                    "expectedDataType": [
                      "float"
                    ]
                  },
                  {
                    "defaultValue": [
                      {
                        "name": "False",
                        "displayName": "False",
                        "selected": False
                      },
                      {
                        "name": "True",
                        "displayName": "True",
                        "selected": False
                      }
                    ],
                    "displayName": "nesterov",
                    "display": True,
                    "paramType": "list",
                    "hyperpatameterTuningCandidate": True,
                    "name": "nesterov",
                    "allowedDataType": [
                      "bool"
                    ],
                    "description": "enables Nesterov momentum.",
                    "uiElemType": "checkbox",
                    "expectedDataType": [
                      "bool"
                    ]
                  }
                ],
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Optimizer",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "regularizer",
            "valueRange": None,
            "description": "Regularizer function.",
            "expectedDataType": [
              "string"
            ],
            "defaultValue": [
              {
                "name": "l1_regularizer",
                "displayName": "l1_regularizer",
                "parameters": [
                  {
                    "display": True,
                    "paramType": "number",
                    "name": "l1_decay",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "l1 decay.",
                    "expectedDataType": [
                      "float"
                    ],
                    "defaultValue": 0,
                    "uiElemType": "textBox",
                    "hyperpatameterTuningCandidate": True,
                    "displayName": "l1_decay",
                    "allowedDataType": [
                      "float"
                    ],
                    "selected": False
                  }
                ],
                "selected": False
              },
              {
                "name": "l2_regularizer",
                "displayName": "l2_regularizer",
                "parameters": [
                  {
                    "display": True,
                    "paramType": "number",
                    "name": "l2_decay",
                    "valueRange": [
                      0,
                      1
                    ],
                    "description": "l2 dacay.",
                    "expectedDataType": [
                      "float"
                    ],
                    "defaultValue": 0,
                    "uiElemType": "textBox",
                    "hyperpatameterTuningCandidate": True,
                    "displayName": "l2_decay",
                    "allowedDataType": [
                      "float"
                    ],
                    "selected": False
                  }
                ],
                "selected": False
              }
            ],
            "uiElemType": "checkbox",
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "displayName": "regularizer",
            "allowedDataType": [
              "string"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "batch_size",
            "valueRange": [
              0,
              100
            ],
            "description": "The number of training examples in one Forward/Backward Pass.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 0,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Batch Size",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "number_of_epochs",
            "valueRange": None,
            "description": "An epoch refers to one cycle through the full training data-set.",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 100,
            "uiElemType": "textBox",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Number of Epochs",
            "allowedDataType": [
              "int"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "LightGBM",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8lgbm",
        "description": "For LightGBM Algorithm",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "eta",
            "valueRange": [
              0,
              1
            ],
            "description": "It is the step size shrinkage used to prevent Overfitting",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.3,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Learning Rate",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "gamma",
            "valueRange": [
              0,
              100
            ],
            "description": "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Loss Reduction",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_depth",
            "valueRange": [
              0,
              100
            ],
            "description": "The maximum depth of a tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 6,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Depth",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_child_weight",
            "valueRange": [
              0,
              100
            ],
            "description": "The Minimum sum of Instance weight needed in a child node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Minimum Child Weight",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "subsample",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of the training instance",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Subsampling Ratio",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bytree",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of columns when constructing each tree",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "subsample ratio of columns for each tree",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bylevel",
            "valueRange": [
              0.1,
              1
            ],
            "description": "Subsample ratio of columns for each split in each level",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "subsample ratio of columns for each split",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "gbtree",
                "displayName": "gbtree",
                "selected": True
              },
              {
                "name": "dart",
                "displayName": "dart",
                "selected": True
              },
              {
                "name": "gblinear",
                "displayName": "gblinear",
                "selected": True
              }
            ],
            "displayName": "Booster Function",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "booster",
            "allowedDataType": [
              "string"
            ],
            "description": "The booster function to be used",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "auto",
                "displayName": "auto",
                "selected": True
              },
              {
                "name": "exact",
                "displayName": "exact",
                "selected": True
              },
              {
                "name": "approx",
                "displayName": "approx",
                "selected": True
              },
              {
                "name": "hist",
                "displayName": "hist",
                "selected": True
              },
              {
                "name": "gpu_exact",
                "displayName": "gpu_exact",
                "selected": True
              },
              {
                "name": "gpu_hist",
                "displayName": "gpu_hist",
                "selected": True
              }
            ],
            "displayName": "Tree Construction Algorithm",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "tree_method",
            "allowedDataType": [
              "string"
            ],
            "description": "The Tree construction algorithm used in XGBoost",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "default",
                "displayName": "Create New Trees",
                "selected": True
              },
              {
                "name": "update",
                "displayName": "Update Trees",
                "selected": True
              }
            ],
            "displayName": "Process Type",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "process_type",
            "allowedDataType": [
              "string"
            ],
            "description": "Boosting process to run",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": 0,
                "displayName": "True",
                "selected": False
              },
              {
                "name": 1,
                "displayName": "False",
                "selected": True
              }
            ],
            "displayName": "Print Messages on Console",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "silent",
            "allowedDataType": [
              "int"
            ],
            "description": "Runtime Message Printing",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "cpu_predictor",
                "displayName": "Multicore CPU prediction algorithm",
                "selected": True
              },
              {
                "name": "gpu_predictor",
                "displayName": "Prediction using GPU",
                "selected": True
              }
            ],
            "displayName": "Type of Predictor Algorithm",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "predictor",
            "allowedDataType": [
              "string"
            ],
            "description": "The type of predictor algorithm to use",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "Ensemble",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8en",
        "description": "For Ensemble Algorithm",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "eta",
            "valueRange": [
              0,
              1
            ],
            "description": "It is the step size shrinkage used to prevent Overfitting",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.3,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Learning Rate",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "gamma",
            "valueRange": [
              0,
              100
            ],
            "description": "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Loss Reduction",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_depth",
            "valueRange": [
              0,
              100
            ],
            "description": "The maximum depth of a tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 6,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Depth",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_child_weight",
            "valueRange": [
              0,
              100
            ],
            "description": "The Minimum sum of Instance weight needed in a child node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Minimum Child Weight",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "subsample",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of the training instance",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Subsampling Ratio",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bytree",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of columns when constructing each tree",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "subsample ratio of columns for each tree",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bylevel",
            "valueRange": [
              0.1,
              1
            ],
            "description": "Subsample ratio of columns for each split in each level",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "subsample ratio of columns for each split",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "gbtree",
                "displayName": "gbtree",
                "selected": True
              },
              {
                "name": "dart",
                "displayName": "dart",
                "selected": True
              },
              {
                "name": "gblinear",
                "displayName": "gblinear",
                "selected": True
              }
            ],
            "displayName": "Booster Function",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "booster",
            "allowedDataType": [
              "string"
            ],
            "description": "The booster function to be used",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "auto",
                "displayName": "auto",
                "selected": True
              },
              {
                "name": "exact",
                "displayName": "exact",
                "selected": True
              },
              {
                "name": "approx",
                "displayName": "approx",
                "selected": True
              },
              {
                "name": "hist",
                "displayName": "hist",
                "selected": True
              },
              {
                "name": "gpu_exact",
                "displayName": "gpu_exact",
                "selected": True
              },
              {
                "name": "gpu_hist",
                "displayName": "gpu_hist",
                "selected": True
              }
            ],
            "displayName": "Tree Construction Algorithm",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "tree_method",
            "allowedDataType": [
              "string"
            ],
            "description": "The Tree construction algorithm used in XGBoost",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "default",
                "displayName": "Create New Trees",
                "selected": True
              },
              {
                "name": "update",
                "displayName": "Update Trees",
                "selected": True
              }
            ],
            "displayName": "Process Type",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "process_type",
            "allowedDataType": [
              "string"
            ],
            "description": "Boosting process to run",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": 0,
                "displayName": "True",
                "selected": False
              },
              {
                "name": 1,
                "displayName": "False",
                "selected": True
              }
            ],
            "displayName": "Print Messages on Console",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "silent",
            "allowedDataType": [
              "int"
            ],
            "description": "Runtime Message Printing",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "cpu_predictor",
                "displayName": "Multicore CPU prediction algorithm",
                "selected": True
              },
              {
                "name": "gpu_predictor",
                "displayName": "Prediction using GPU",
                "selected": True
              }
            ],
            "displayName": "Type of Predictor Algorithm",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "predictor",
            "allowedDataType": [
              "string"
            ],
            "description": "The type of predictor algorithm to use",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          }
        ],
        "selected": True
      },
      {
        "algorithmName": "Adaboost",
        "hyperParameterSetting": [
          {
            "name": "gridsearchcv",
            "params": [
              {
                "defaultValue": [
                  None
                ],
                "name": "evaluationMetric",
                "display": False,
                "paramType": "list",
                "displayName": "Metric Used for Optimization",
                "uiElemType": "dropDown",
                "expectedDataType": [
                  None,
                  "string"
                ]
              },
              {
                "defaultValue": 3,
                "name": "kFold",
                "display": True,
                "acceptedValue": None,
                "displayName": "No Of Folds to Use",
                "valueRange": [
                  2,
                  20
                ],
                "paramType": "number",
                "uiElemType": "slider",
                "expectedDataType": [
                  None,
                  "int"
                ]
              }
            ],
            "selected": False,
            "displayName": "Grid Search"
          },
          {
            "name": "none",
            "params": None,
            "selected": True,
            "displayName": "None"
          }
        ],
        "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8adab",
        "description": "For Adaboost Algorithm",
        "parameters": [
          {
            "display": True,
            "acceptedValue": None,
            "name": "eta",
            "valueRange": [
              0,
              1
            ],
            "description": "It is the step size shrinkage used to prevent Overfitting",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 0.3,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Learning Rate",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "gamma",
            "valueRange": [
              0,
              100
            ],
            "description": "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Minimum Loss Reduction",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "max_depth",
            "valueRange": [
              0,
              100
            ],
            "description": "The maximum depth of a tree",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 6,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Maximum Depth",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "min_child_weight",
            "valueRange": [
              0,
              100
            ],
            "description": "The Minimum sum of Instance weight needed in a child node",
            "expectedDataType": [
              "int"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "Minimum Child Weight",
            "allowedDataType": [
              "int"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "subsample",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of the training instance",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "Subsampling Ratio",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bytree",
            "valueRange": [
              0.1,
              1
            ],
            "description": "It is the subsample ratio of columns when constructing each tree",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": True,
            "displayName": "subsample ratio of columns for each tree",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "display": True,
            "acceptedValue": None,
            "name": "colsample_bylevel",
            "valueRange": [
              0.1,
              1
            ],
            "description": "Subsample ratio of columns for each split in each level",
            "expectedDataType": [
              "float"
            ],
            "defaultValue": 1,
            "uiElemType": "slider",
            "paramType": "number",
            "hyperpatameterTuningCandidate": False,
            "displayName": "subsample ratio of columns for each split",
            "allowedDataType": [
              "float"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "gbtree",
                "displayName": "gbtree",
                "selected": True
              },
              {
                "name": "dart",
                "displayName": "dart",
                "selected": True
              },
              {
                "name": "gblinear",
                "displayName": "gblinear",
                "selected": True
              }
            ],
            "displayName": "Booster Function",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "booster",
            "allowedDataType": [
              "string"
            ],
            "description": "The booster function to be used",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "auto",
                "displayName": "auto",
                "selected": True
              },
              {
                "name": "exact",
                "displayName": "exact",
                "selected": True
              },
              {
                "name": "approx",
                "displayName": "approx",
                "selected": True
              },
              {
                "name": "hist",
                "displayName": "hist",
                "selected": True
              },
              {
                "name": "gpu_exact",
                "displayName": "gpu_exact",
                "selected": True
              },
              {
                "name": "gpu_hist",
                "displayName": "gpu_hist",
                "selected": True
              }
            ],
            "displayName": "Tree Construction Algorithm",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": True,
            "name": "tree_method",
            "allowedDataType": [
              "string"
            ],
            "description": "The Tree construction algorithm used in XGBoost",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "default",
                "displayName": "Create New Trees",
                "selected": True
              },
              {
                "name": "update",
                "displayName": "Update Trees",
                "selected": True
              }
            ],
            "displayName": "Process Type",
            "display": True,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "process_type",
            "allowedDataType": [
              "string"
            ],
            "description": "Boosting process to run",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          },
          {
            "defaultValue": [
              {
                "name": 0,
                "displayName": "True",
                "selected": False
              },
              {
                "name": 1,
                "displayName": "False",
                "selected": True
              }
            ],
            "displayName": "Print Messages on Console",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "silent",
            "allowedDataType": [
              "int"
            ],
            "description": "Runtime Message Printing",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "int"
            ]
          },
          {
            "defaultValue": [
              {
                "name": "cpu_predictor",
                "displayName": "Multicore CPU prediction algorithm",
                "selected": True
              },
              {
                "name": "gpu_predictor",
                "displayName": "Prediction using GPU",
                "selected": True
              }
            ],
            "displayName": "Type of Predictor Algorithm",
            "display": False,
            "paramType": "list",
            "hyperpatameterTuningCandidate": False,
            "name": "predictor",
            "allowedDataType": [
              "string"
            ],
            "description": "The type of predictor algorithm to use",
            "uiElemType": "checkbox",
            "expectedDataType": [
              "string"
            ]
          }
        ],
        "selected": True
      }
    ]
