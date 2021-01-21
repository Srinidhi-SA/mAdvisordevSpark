PYSPARK_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION = [
    {"name": "gini", "selected": True, "displayName": "Gini Impurity"},
    {"name": "entropy", "selected": False, "displayName": "Entropy"}
]

PYSPARK_ML_SUPPORTED_SPLIT_MODEL_TYPE_CLASSIFICATION = [
    {"name": "multinomial", "selected": True, "displayName": "multinomial"}
]

PYSPARK_ML_SUPPORTED_SPLIT_FAMILY_CLASSIFICATION = [
    {"name": "auto", "selected": True, "displayName": "auto"},
    {"name": "binomial", "selected": False, "displayName": "binomial"},
    {"name": "multinomial", "selected": False, "displayName": "multinomial"}
]

PYSPARK_ML_SUPPORTED_SOLVER_CLASSIFICATION = [
    {"name": "newton-cg", "selected": True, "displayName": "newton-cg", "penalty": "l2"},
    {"name": "lbfgs", "selected": False, "displayName": "lbfgs", "penalty": "l2"},
    {"name": "sag", "selected": False, "displayName": "sag", "penalty": "l2"},
    {"name": "liblinear", "selected": False, "displayName": "liblinear", "penalty": "l1"},
    {"name": "saga", "selected": False, "displayName": "saga", "penalty": "l1"}
]

PYSPARK_ML_SUPPORTED_MULTICLASS_OPTION = [
    {"name": "ovr", "selected": False, "displayName": "One Vs Rest"},
    {"name": "multinomial", "selected": False, "displayName": "Multinomial"}
]

# Algorithm Params
PYSPARK_ML_LOGISTIC_REGRESSION_PARAMS = [
    {
        "name": "maxIter",
        "displayName": "Maximum Solver Iterations",
        "className": "maxIter",
        "description": "Max number of iterations.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [10, 1000],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "regParam",
        "displayName": "Regularisation parameter",
        "className": "regParam",
        "description": "Regularisation parameter.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.00001, 0.5],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "elasticNetParam",
        "displayName": "elasticNetParam",
        "className": "elasticNetParam",
        "description": "Elastic Net mixing parameter in the given range.",
        "defaultValue": 0.0,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "aggregationDepth",
        "className": "aggregationDepth",
        "displayName": "aggregationDepth",
        "description": "Depth for tree aggregation",
        "defaultValue": 2,
        "acceptedValue": None,
        "valueRange": [2, 10],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "standardization",
        "displayName": "standardization",
        "description": "Whether to standardize the training features before fitting the model.",
        "defaultValue": [
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
            },
            {
                "name": "true",
                "selected": True,
                "displayName": "True"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "fitIntercept",
        "displayName": "fitIntercept",
        "description": "Fit an intercept terms.",
        "defaultValue": [
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
            },
            {
                "name": "true",
                "selected": True,
                "displayName": "True"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "tol",
        "className": "tol",
        "displayName": "tol",
        "description": "Convergence tolerance for iterative algorithms",
        "defaultValue": 0.000001,
        "acceptedValue": None,
        "valueRange": [0, 1000],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float", "int"],
        "allowedDataType": ["float", "int"]
    },
    {
        "name": "family",
        "className": "family",
        "displayName": "family",
        "description": "The name of family which is a description of the label distribution to be used in the model.",
        "defaultValue": [obj for obj in PYSPARK_ML_SUPPORTED_SPLIT_FAMILY_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "threshold",
        "displayName": "threshold",
        "className": "threshold",
        "description": "In binary classification prediction",
        "defaultValue": 0.5,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]

PYSPARK_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Max Depth",
        "description": "Max number of levels in each decision tree.",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]
    },
    {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Min number of data points placed in a node before the node is split.",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]

PYSPARK_ML_RF_CLASSIFICATION_PARAMS = PYSPARK_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
    {
        "name": "numTrees",
        "displayName": "No of Estimators",
        "description": "Number of trees in the forest.",
        "defaultValue": 10,
        "acceptedValue": None,
        "valueRange": [10, 1000],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [obj for obj in PYSPARK_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "maxBins",
        "displayName": "No of Bins",
        "description": "Number of bins used when discretizing continuous features.",
        "defaultValue": 3,
        "acceptedValue": None,
        "valueRange": [3, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "seed",
        "className": "seed",
        "displayName": "Random Seed",
        "description": "Random seed for bootstrapping and choosing feature subsets.",
        "defaultValue": None,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]
    }
]

PYSPARK_ML_DECISIONTREE_CLASSIFICATION_PARAMS = [
    {
        "name": "maxDepth",
        "displayName": "Max Depth",
        "description": "Maximum depth of the tree.",
        "defaultValue": 5,
        "acceptedValue": None,
        "valueRange": [2, 20],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", None],
        "allowedDataType": ["int", None]
    },
    {
        "name": "impurity",
        "displayName": "Criterion",
        "description": "Criterion used for information gain calculation.",
        "defaultValue": [obj for obj in PYSPARK_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "maxBins",
        "displayName": "maxBins",
        "description": "Maximum number of bins used for discretizing continuous features and for choosing how to split on features at each node.",
        "defaultValue": 32,
        "acceptedValue": None,
        "valueRange": [40, 300],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInstancesPerNode",
        "displayName": "Minimum instance for split",
        "description": "Minimum number of instances each child must have after split",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "minInfoGain",
        "className": "minInfoGain",
        "displayName": "minInfoGain",
        "description": "Minimum information gain for a split to be considered at a tree node.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]

PYSPARK_ML_NAIVE_BAYES_CLASSIFICATION_PARAMS = [
    {
        "name": "smoothing",
        "className": "smoothing",
        "displayName": "Alpha",
        "description": "Smoothing parameter",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "modelType",
        "className": "modelType",
        "displayName": "Model Type",
        "description": "The model type which is a string.",
        "defaultValue": [obj for obj in PYSPARK_ML_SUPPORTED_SPLIT_MODEL_TYPE_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
