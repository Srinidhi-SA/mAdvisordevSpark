############################      Regression      ###############################
SKLEARN_ML_LINEAR_REGRESSION_PARAMS = [
            {
                "name": "n_jobs",
                "displayName": "No Of Jobs",
                "description": "Number of CPU cores to be used when parallelizing over classes",
                "defaultValue": [
                    {
                        "name": -1,
                        "selected": True,
                        "displayName": "All"
                    },
                    {
                        "name": 1,
                        "selected": False,
                        "displayName": "1 core"
                    },
                    {
                        "name": 2,
                        "selected": False,
                        "displayName": "2 cores"
                    },
                    {
                        "name": 3,
                        "selected": False,
                        "displayName": "3 cores"
                    },
                    {
                        "name": 4,
                        "selected": False,
                        "displayName": "4 cores"
                    },
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": ["int"],
                "allowedDataType": ["int"]
            },
            {
                 "name":"fit_intercept",
                 "displayName":"Fit Intercept",
                 "description":"It specifies whether to calculate the intercept for this model. If set to False, no intercept will be used in calculations",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":False,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":False,
                         "displayName":"True"
                     }
                    ],
                 "paramType":"list",
                 "uiElemType":"checkbox",
                 "display":True,
                 "hyperpatameterTuningCandidate":True,
                 "expectedDataType": ["bool"],
                 "allowedDataType":["bool"]

             },
             {
                 "name":"normalize",
                 "displayName":"Normalize",
                 "description":"If True, the regressors X will be normalized before regression",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":False,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":False,
                         "displayName":"True"
                     }
                    ],
                 "paramType":"list",
                 "uiElemType":"checkbox",
                 "display":True,
                 "hyperpatameterTuningCandidate":True,
                 "expectedDataType": ["bool"],
                 "allowedDataType":["bool"]

             },
             {
                 "name":"copy_X",
                 "displayName":"Copy X",
                 "description":"If True, X will be copied; else, it may be overwritten",
                 "defaultValue":[
                     {
                         "name":"false",
                         "selected":False,
                         "displayName":"False"
                     },
                     {
                         "name":"true",
                         "selected":False,
                         "displayName":"True"
                     }
                    ],
                 "paramType":"list",
                 "uiElemType":"checkbox",
                 "display":True,
                 "hyperpatameterTuningCandidate":True,
                 "expectedDataType": ["bool"],
                 "allowedDataType":["bool"]

             }
]

SKLEARN_ML_GENERALIZED_LINEAR_REGRESSION_PARAMS = [

]

SKLEARN_SGD_LEARNING_RATES = [
    {"name":"invscaling","selected":True,"displayName":"Inverse Scaling"},
    {"name":"optimal","selected":False,"displayName":"Optimal"},
    {"name":"constant","selected":False,"displayName":"Constant"},
]

SKLEARN_ML_SUPPORTED_LOSS = [
    {"name":"ls","selected":True,"displayName":"Least Squares Regression"},
    {"name":"lad","selected":False,"displayName":"Least Absolute Deviation"},
    {"name":"huber","selected":False,"displayName":"Huber"},
    {"name":"quantile","selected":False,"displayName":"Quantile Regression"},
]
SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION = [
    {"name":"friedman_mse","selected":False,"displayName":"Friedman Mse"},
    {"name":"mse","selected":False,"displayName":"Mean Squared Error"},
    {"name":"mae","selected":False,"displayName":"Mean Absolute Error"},
]

SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
                {
                    "name":"n_estimators",
                    "displayName":"No. Of Estimators",
                    "description":"The number of trees in the forest",
                    "defaultValue":10,
                    "acceptedValue":None,
                    "valueRange":[10,1000],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int"],
                    "allowedDataType":["int"]
                },
                {
                    "name":"max_depth",
                    "displayName":"Max Depth Of Trees",
                    "description":"The maximum depth of the tree",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int", None],
                    "allowedDataType":["int",None]

                },

                {
                    "name":"min_samples_split",
                    "displayName":"Minimum Instances For Split",
                    "description":"The minimum number of samples required to split an internal node",
                    "defaultValue":2,
                    "acceptedValue":None,
                    "valueRange":[0,100],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int"],
                    "allowedDataType":["int", "float"]

                },
                {
                    "name":"min_samples_leaf",
                    "displayName":"Minimum Instances For Leaf Node",
                    "description":"The minimum number of samples required to be at a leaf node",
                    "defaultValue":1,
                    "acceptedValue":None,
                    "valueRange":[1,100],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int"],
                    "allowedDataType": ["int", "float"]

                },
                {
                    "name":"subsample",
                    "displayName":"Sub Sampling Rate",
                    "description":"It is the subsample ratio of the training instance",
                    "defaultValue":1.0,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["float"],
                    "allowedDataType":["float"]

                },
                {
                    "name":"max_features",
                    "displayName":"Maximum Features for Split",
                    "description":"The number of features to consider when looking for the best split",
                    "defaultValue":None,
                    "acceptedValue":None,
                    "valueRange":[0.1,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType":["float"],
                    "allowedDataType": ["float", "int","string", None]
                },
                {
                    "name":"min_impurity_decrease",
                    "displayName":"Impurity Decrease cutoff for Split",
                    "description":"A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":False,
                    "expectedDataType": ["float"],
                    "allowedDataType": ["float"]

                },
                {
                    "name":"criterion",
                    "displayName":"Measure For quality of a split",
                    "description":"The function to measure the quality of a split",
                    "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION],
                    "paramType":"list",
                    "uiElemType":"checkbox",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["string"],
                    "allowedDataType":["string"]

                }

]

SKLEARN_ML_GBT_REGRESSION_PARAMS = [
        {
            "name":"learning_rate",
            "displayName":"Learning Rate",
            "description":"It shrinks the contribution of each tree by learning_rate",
            "defaultValue":0.1,
            "acceptedValue":None,
            "valueRange":[0.1,1.0],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["float"],
            "allowedDataType": ["float"]
        },
        {
            "name":"loss",
            "displayName":"Loss Function",
            "description":"It is the loss function to be optimized",
            "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_LOSS],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["string"],
            "allowedDataType": ["string"]

        },
        {
            "name":"alpha",
            "displayName":"Alpha-Quantile",
            "description":"The alpha-quantile of the huber loss function and the quantile loss function",
            "defaultValue":0.9,
            "acceptedValue":None,
            "valueRange":[0.1,1.0],
            "paramType":"number",
            "uiElemType":"slider",
            "display":False,
            "dependentOnDict":{"loss":["huber","quantile"]},
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["float"],
            "allowedDataType": ["float"]

        },
        {
            "name":"warm_start",
            "displayName":"Warm Start",
            "description":"When set to True, reuse the solution of the previous call to fit as initialization",
            "defaultValue":[
             {
                 "name":"false",
                 "selected":True,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":False,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["bool"],
            "allowedDataType": ["bool"]

        },
        {
            "name": "loss",
            "displayName": "Loss Function",
            "description": "It is the loss function to be optimized",
            "defaultValue": [{"name": obj["name"], "selected": obj["selected"], "displayName": obj["displayName"]} for obj
                             in SKLEARN_ML_SUPPORTED_LOSS],
            "paramType": "list",
            "uiElemType": "checkbox",
            "display": True,
            "hyperpatameterTuningCandidate": True,
            "expectedDataType": ["string"],
            "allowedDataType": ["string"]

        },

]

SKLEARN_ML_RF_REGRESSION_PARAMS = SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
    {
        "name":"bootstrap",
        "displayName":"Bootstrap Sampling",
        "description":"It defines whether bootstrap samples are used when building trees",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":False,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":True,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["bool"],
            "allowedDataType": ["bool"]

    },
    {
        "name":"oob_score",
        "displayName":"use out-of-bag samples",
        "description":"It defines whether to use out-of-bag samples to estimate the R^2 on unseen data",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":False,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":True,
                 "displayName":"True"
             }
            ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":False,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
                "name": "n_jobs",
                "displayName": "No Of Jobs",
                "description": "Number of CPU cores to be used when parallelizing over classes",
                "defaultValue": [
                    {
                        "name": -1,
                        "selected": True,
                        "displayName": "All"
                    },
                    {
                        "name": 1,
                        "selected": False,
                        "displayName": "1 core"
                    },
                    {
                        "name": 2,
                        "selected": False,
                        "displayName": "2 cores"
                    },
                    {
                        "name": 3,
                        "selected": False,
                        "displayName": "3 cores"
                    },
                    {
                        "name": 4,
                        "selected": False,
                        "displayName": "4 cores"
                    },
                ],
                "paramType": "list",
                "uiElemType": "checkbox",
                "display": True,
                "hyperpatameterTuningCandidate": False,
                "expectedDataType": ["int"],
                "allowedDataType": ["int"]
    },
    {
        "name":"warm_start",
        "displayName":"Warm Start",
        "description":"When set to True, reuse the solution of the previous call to fit as initialization",
        "defaultValue":[
             {
                 "name":"false",
                 "selected":True,
                 "displayName":"False"
             },
             {
                 "name":"true",
                 "selected":False,
                 "displayName":"True"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
]

SKLEARN_ML_DTREE_REGRESSION_PARAMS = SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
        {
            "name":"splitter",
            "displayName":"Node Split Strategy",
            "description":"The strategy used to choose the split at each node",
            "defaultValue":[
             {
                 "name":"best",
                 "selected":True,
                 "displayName":"Best split"
             },
             {
                 "name":"random",
                 "selected":False,
                 "displayName":"Best random split"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["string"],
            "allowedDataType": ["string"]
        },
        {
            "name": "max_leaf_nodes",
            "displayName": "Maximum Number of Leaf Nodes",
            "description": "The maximum of number of leaf nodes",
            "defaultValue": None,
            "acceptedValue": None,
            "valueRange": [],
            "paramType": "number",
            "uiElemType": "textBox",
            "display": True,
            "hyperpatameterTuningCandidate": False,
            "expectedDataType": ["int", None],
            "allowedDataType": ["int", None]
        },
        {
            "name": "random_state",
            "displayName": "Random Seed",
            "description": "The seed of the pseudo random number generator to use when shuffling the data",
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

TENSORFLOW_ACTIVATION_PARAMETERS = [
    {"name": "deserialize", "selected": True, "displayName": "deserialize"},
    {"name": "elu", "selected": False, "displayName": "elu"},
    {"name": "exponential", "selected": False, "displayName": "exponential"},
    {"name":"get","selected":False,"displayName":"get"},
    {"name": "hard_sigmoid", "selected": False, "displayName": "hard_sigmoid"},
    {"name":"Linear","selected":False,"displayName":"Linear"},
    {"name":"relu","selected":False,"displayName":"relu"},
    {"name":"selu","selected":False,"displayName":"selu"},
    {"name":"serialize","selected":False,"displayName":"serialize"},
    {"name":"sigmoid","selected":False,"displayName":"sigmoid"},
    {"name":"softmax","selected":False,"displayName":"softmax"},
    {"name":"softplus","selected":False,"displayName":"softplus"},
    {"name":"softsign","selected":False,"displayName":"softsign"},
    {"name":"tanh","selected":False,"displayName":"tanh"},
]
TENSORFLOW_COMMON_INITIALIZER_PARAMETERS = [
    {"name": "Zeros", "selected": True, "displayName": "Zeros"},
    {"name": "Ones", "selected": False, "displayName": "Ones"},
    {"name": "Constant", "selected": False, "displayName": "Constant"},
    {"name": "RandomNormal", "selected": False, "displayName": "RandomNormal"},
    {"name": "RandomUniform", "selected": False, "displayName": "RandomUniform"},
    {"name": "TruncatedNormal", "selected": False, "displayName": "TruncatedNormal"},
    {"name": "VarianceScaling", "selected": False, "displayName": "VarianceScaling"},
    {"name": "Orthogonal", "selected": False, "displayName": "Orthogonal"},
    {"name": "Identity", "selected": False, "displayName": "Identity"},
    {"name": "lecun_uniform", "selected": False, "displayName": "lecun_uniform"},
    {"name": "glorot_normal", "selected": False, "displayName": "glorot_normal"},
    {"name": "glorot_uniform", "selected": False, "displayName": "glorot_uniform"},
    {"name": "he_normal", "selected": False, "displayName": "he_normal"},
    {"name": "lecun_normal", "selected": False, "displayName": "lecun_normal"},
    {"name": "he_uniform", "selected": False, "displayName": "he_uniform"},

]
TENSORFLOW_COMMON_REGULARIZER_PARAMETERS = [
    {"name": "l1", "selected": True, "displayName": "l1"},
    {"name": "l2", "selected": False, "displayName": "l2"},
    {"name": "l1_l2", "selected": False, "displayName": "l1_l2"},
]
TENSORFLOW_COMMON_CONSTRAINT_PARAMETERS = [
    {"name": "MaxNorm", "selected": True, "displayName": "MaxNorm"},
    {"name": "NonNeg", "selected": False, "displayName": "NonNeg"},
    {"name": "UnitNorm", "selected": False, "displayName": "UnitNorm"},
    {"name": "MinMaxNorm", "selected": False, "displayName": "MinMaxNorm"},
]
TENSORFLOW_LAMBDA_FUNCTIONS = [
    {"name": "2*X", "selected": True, "displayName": "2*X"},
]
SKLEARN_ML_SUPPORTED_TF_LOSS_PARAMETERS = [
    {"name": "mean_squared_error", "selected": True, "displayName": "mean_squared_error"},
    {"name": "mean_absolute_error", "selected": False, "displayName": "mean_absolute_error"},
    {"name": "mean_absolute_percentage_error", "selected": False, "displayName": "mean_absolute_percentage_error"},
    {"name": "mean_squared_logarithmic_error", "selected": False, "displayName": "mean_squared_logarithmic_error"},
    {"name": "cosine_proximity", "selected": False, "displayName": "cosine_proximity"},
]
SKLEARN_ML_SUPPORTED_TF_OPTIMIZER_PARAMETERS = [
    {"name": "SGD", "selected": True, "displayName": "SGD"},
    {"name": "RMSprop", "selected": False, "displayName": "RMSprop"},
    {"name": "Adagrad", "selected": False, "displayName": "Adagrad"},
    {"name": "Adadelta", "selected": False, "displayName": "Adadelta"},
    {"name": "Adam", "selected": False, "displayName": "Adam"},
    {"name": "Adamax", "selected": False, "displayName": "Adamax"},
    {"name": "Nadam", "selected": False, "displayName": "Nadam"},
]
TF_REGRESSION_METRICS = [
    {"name": "CosineSimilarity", "selected": False, "displayName": "CosineSimilarity"},
    {"name": "mae", "selected": False, "displayName": "mae"},
    {"name": "mape", "selected": False, "displayName": "mape"},
    {"name": "mean", "selected": False, "displayName": "mean"},
    {"name": "mean_absolute_error", "selected": False, "displayName": "mean_absolute_error"},
    {"name": "mean_absolute_percentage_error", "selected": False, "displayName": "mean_absolute_percentage_error"},
    {"name": "mean_squared_error", "selected": True, "displayName": "mean_squared_error"},
    {"name": "mean_squared_logarithmic_error", "selected": False, "displayName": "mean_squared_logarithmic_error"},
]
TENSORFLOW_DENSE_PARAMETERS = [
    {
        "name": "activation",
        "displayName": "Activation",
        "description": "Activation function for the hidden layer.",
        # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
        "defaultValue": [obj for obj in TENSORFLOW_ACTIVATION_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "units",
        "displayName": "Units",
        "description": "Dimensionality of the output space.",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.1, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "use_bias",
        "displayName": "use_bias",
        "description": "Whether the layer uses a bias vector.",
        "defaultValue": [
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
            },
            {
                "name": "true",
                "selected": False,
                "displayName": "True"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "kernel_initializer",
        "displayName": "kernel_initializer",
        "description": "Initializer for the kernel weights matrix.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_INITIALIZER_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "bias_initializer",
        "displayName": "bias_initializer",
        "description": "Initializer for the bias vector.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_INITIALIZER_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "kernel_regularizer",
        "displayName": "kernel_regularizer",
        "description": "Regularizer function applied to the kernel weights matrix.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_REGULARIZER_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "bias_regularizer",
        "displayName": "bias_regularizer",
        "description": "Regularizer function applied to the bias vector.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_REGULARIZER_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "activity_regularizer",
        "displayName": "activity_regularizer",
        "description": "Regularizer function applied to the output of the layer.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_REGULARIZER_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "kernel_constraint",
        "displayName": "kernel_constraint",
        "description": "Constraint function applied to the kernel weights matrix.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_CONSTRAINT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "bias_constraint",
        "displayName": "bias_constraint",
        "description": "Constraint function applied to the bias vector.",
        "defaultValue": [obj for obj in TENSORFLOW_COMMON_CONSTRAINT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]
TENSORFLOW_DROPOUT_PARAMETERS = [
    {
        "name": "rate",
        "displayName": "Rate",
        "description": "Fraction of the input units to drop.",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
TENSORFLOW_LAMBDA_PARAMETERS = [
    {
        "name": "lambda",
        "displayName": "Lambda",
        "description": "Wraps arbitrary expression as a Layer object..",
        "defaultValue": [obj for obj in TENSORFLOW_LAMBDA_FUNCTIONS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]
SKLEARN_ML_SUPPORTED_TF_LAYER = [
    {"name": "Dense", "selected": True, "displayName": "Dense","parameters":[obj for obj in TENSORFLOW_DENSE_PARAMETERS]},
    {"name": "Dropout", "selected": False, "displayName": "Dropout","parameters":[obj for obj in TENSORFLOW_DROPOUT_PARAMETERS]},
    {"name": "Lambda", "selected": False, "displayName": "Lambda","parameters":[obj for obj in TENSORFLOW_LAMBDA_PARAMETERS]}
]
SKLEARN_ML_TENSORFLOW_REGRESSION_PARAMS = [
    {
        "name": "layer",
        "displayName": "Layer",
        "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
        "defaultValue":[obj for obj in SKLEARN_ML_SUPPORTED_TF_LAYER],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "loss",
        "displayName": "Loss",
        "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
        "defaultValue":[obj for obj in SKLEARN_ML_SUPPORTED_TF_LOSS_PARAMETERS],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "optimizer",
        "displayName": "Optimizer",
        "description": "Method used to minimize the loss function.",
        "defaultValue":[obj for obj in SKLEARN_ML_SUPPORTED_TF_OPTIMIZER_PARAMETERS],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "batch_size",
        "displayName": "Batch Size",
        "description": "The number of training examples in one Forward/Backward Pass.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [0.0, 100.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "number_of_epochs",
        "displayName": "Number of Epochs",
        "description": "An epoch refers to one cycle through the full training data-set.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [0.0, 10000.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "metrics",
        "displayName": "Metrics",
        "description": "List of metrics to be evaluated by the model during training And testing.",
        "defaultValue":[obj for obj in TF_REGRESSION_METRICS],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]
