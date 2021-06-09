############################    Classification    ###############################
SKLEARN_ML_SUPPORTED_PENALTY_CLASSIFICATION = [
    {"name": "gini", "selected": False, "displayName": "Gini Impurity"},
    {"name": "entropy", "selected": False, "displayName": "Entropy"},
]
SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION = [
    {"name": "ovr", "selected": False, "displayName": "One Vs Rest"},
    {"name": "multinomial", "selected": False, "displayName": "Multinomial"}
]
SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION = [
    {"name": "newton-cg", "selected": True, "displayName": "newton-cg", "penalty": "l2"},
    {"name": "lbfgs", "selected": False, "displayName": "lbfgs", "penalty": "l2"},
    {"name": "sag", "selected": False, "displayName": "sag", "penalty": "l2"},
    {"name": "liblinear", "selected": False, "displayName": "liblinear", "penalty": "l1"},
    {"name": "saga", "selected": False, "displayName": "saga", "penalty": "l1"},

]
SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION = [
    {"name": "gini", "selected": True, "displayName": "Gini Impurity"},
    {"name": "entropy", "selected": False, "displayName": "Entropy"},
]

SKLEARN_ML_SUPPORTED_MAX_FEATURES = [
    {"name": "auto", "selected": False, "displayName": "sqrt(n_features)"},
    {"name": "sqrt", "selected": False, "displayName": "sqrt(n_features)"},
    {"name": "log2", "selected": False, "displayName": "log2(n_features)"},
    {"name": None, "selected": False, "displayName": "n_features"}
]

##### NEURAL NETWORK PARAMETERS    ####

SKLEARN_ML_SUPPORTED_ACTIVATION_CLASSIFICATION = [
    {"name": "relu", "selected": True, "displayName": "relu"},
    {"name": "identity", "selected": False, "displayName": "identity"},
    {"name": "logistic", "selected": False, "displayName": "logistic"},
    {"name": "tanh", "selected": False, "displayName": "tanh"},
]

SKLEARN_ML_SUPPORTED_NNSOLVER_CLASSIFICATION = [
    {"name": "adam", "selected": True, "displayName": "adam"},
    {"name": "lbfgs", "selected": False, "displayName": "lbfgs"},
    {"name": "sgd", "selected": False, "displayName": "sgd"},
]

SKLEARN_ML_SUPPORTED_LEARNING_RATE_CLASSIFICATION = [
    {"name": "constant", "selected": True, "displayName": "constant"},
    {"name": "invscaling", "selected": False, "displayName": "invscaling"},
    {"name": "adaptive", "selected": False, "displayName": "adaptive"},

]

SKLEARN_ML_SUPPORTED_BATCH_SIZE_CLASSIFICATION = [
    {"name": "auto", "selected": True, "displayName": "auto"},
    {"name": 8, "selected": False, "displayName": "8"},
    {"name": 16, "selected": False, "displayName": "16"},
    {"name": 32, "selected": False, "displayName": "32"},
    {"name": 64, "selected": False, "displayName": "64"},
    {"name": 128, "selected": False, "displayName": "128"},
]

#########################################################

SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS = [
    {
        "name": "max_depth",
        "displayName": "Max Depth",
        "description": "The maximum depth of the tree",
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
        "name": "min_samples_split",
        "displayName": "Minimum Instances For Split",
        "description": "The minimum number of samples required to split an internal node",
        "defaultValue": 2,
        "acceptedValue": None,
        "valueRange": [0, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int", "float"]
    },
    {
        "name": "min_samples_leaf",
        "displayName": "Minimum Instances For Leaf Node",
        "description": "The minimum number of samples required to be at a leaf node",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int", "float"]
    },
    {
        "name": "min_impurity_decrease",
        "displayName": "Impurity Decrease cutoff for Split",
        "description": "A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
        "defaultValue": 0.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

SKLEARN_ML_DTREE_CLASSIFICATION_PARAMS = SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
    {
        "name": "max_features",
        "displayName": "Maximum Features for Split",
        "description": "The number of features to consider when looking for the best split",
        "defaultValue": [
            obj if obj["name"] != None else {"name": obj["name"], "selected": True, "displayName": obj["displayName"]}
            for obj in SKLEARN_ML_SUPPORTED_MAX_FEATURES],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "splitter",
        "displayName": "Node Split Strategy",
        "description": "The strategy used to choose the split at each node",
        "defaultValue": [
            {
                "name": "best",
                "selected": True,
                "displayName": "Best split"
            },
            {
                "name": "random",
                "selected": False,
                "displayName": "Best random split"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["string"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "presort",
        "displayName": "Pre Sort",
        "description": "Presort the data to speed up the finding of best splits in fitting",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "display": False,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },

]

SKLEANR_ML_RF_CLASSIFICATION_PARAMS = SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
    {
        "name": "n_estimators",
        "displayName": "No of Estimators",
        "description": "The number of trees in the forest",
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
        "name": "n_jobs",
        "displayName": "No Of Jobs",
        "className": "n_jobs_rf",
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
        "name": "criterion",
        "displayName": "Criterion",
        "description": "The function to measure the quality of a split",
        # "defaultValue":[obj if obj["name"] != "gini" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "oob_score",
        "displayName": "use out-of-bag samples",
        "description": "It defines whether to use out-of-bag samples to estimate the R^2 on unseen data",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "bootstrap",
        "displayName": "Bootstrap Sampling",
        "description": "It defines whether bootstrap samples are used when building trees",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "warm_start",
        "className": "warm_start_rf",
        "displayName": "Warm Start",
        "description": "When set to True, reuse the solution of the previous call to fit as initialization",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "display": False,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "class_weight",
        "className": "class_weight_rf",
        "displayName": "Class Weight",
        "description": "Weights associated with classes of the target column",
        "defaultValue": [
            {
                "name": "None",
                "selected": False,
                "displayName": "None"
            },
            {
                "name": "balanced",
                "selected": False,
                "displayName": "balanced"
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
        "name": "max_leaf_nodes",
        "displayName": "Max Leaf Nodes",
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
        "className": "random_state_rf",
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
    },
    {
        "uiElemType": "checkbox",
        "display": True,
        "paramType": "list",
        "description": "The number of features to consider when looking for the best split",
        "defaultValue": [
            {
                "selected": True,
                "name": "auto",
                "displayName": "auto"
            },
            {
                "selected": False,
                "name": "sqrt",
                "displayName": "sqrt"
            },
            {
                "selected": False,
                "name": "log2",
                "displayName": "log2"
            }
        ],
        "displayName": "Max Features",
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
            "bool"
        ],
        "name": "max_features",
        "className": "max_features_rf",
        "allowedDataType": [
            "bool"
        ]
    },
    {
        "uiElemType": "slider",
        "paramType": "number",
        "description": "The minimum weighted fraction of the sum total of weights(of all the input samples) required to be at a leaf node",
        "defaultValue": 0.0,
        "displayName": "Minimum Weight Fraction Leaf",
        "hyperpatameterTuningCandidate": True,
        "name": "min_weight_fraction_leaf",
        "valueRange": [
            0,
            0.5
        ],
        "display": True,
        "acceptedValue": None,
        "expectedDataType": [
            "float"
        ],
        "allowedDataType": [
            "float"
        ]
    },
    {
        "uiElemType": "slider",
        "paramType": "number",
        "description": "Threshold for early stopping in tree growth",
        "defaultValue": 0.0,
        "displayName": "Minimum Impurity Split",
        "hyperpatameterTuningCandidate": True,
        "name": "min_impurity_split",
        "valueRange": [
            0,
            1
        ],
        "display": True,
        "acceptedValue": None,
        "expectedDataType": [
            "float"
        ],
        "allowedDataType": [
            "float"
        ]
    },
    {
        "uiElemType": "slider",
        "paramType": "number",
        "description": "Determines what fraction of the original dataset is given to any individual tree",
        "defaultValue": 1,
        "displayName": "Maximum Samples",
        "hyperpatameterTuningCandidate": True,
        "name": "max_samples",
        "valueRange": [
            1,
            100
        ],
        "display": True,
        "acceptedValue": None,
        "expectedDataType": [
            "int"
        ],
        "allowedDataType": [
            "int"
        ]
    }
]

SKLEARN_ML_LOGISTIC_REGRESSION_PARAMS = [
    {
        "name": "max_iter",
        "displayName": "Maximum Solver Iterations",
        "className": "max_iter_lr",
        "description": "Maximum number of iterations to be attempted for solver operations",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [10, 400],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "tol",
        "displayName": "Convergence tolerance of iterations(e^-n)",
        "className": "tol_lr",
        "description": "Tolerance for the stopping criteria",
        "defaultValue": 4,
        "acceptedValue": None,
        "valueRange": [3, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]

    },
    {
        "name": "n_jobs",
        "displayName": "No Of Jobs",
        "className": "n_jobs_lr",
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
        "name": "fit_intercept",
        "displayName": "Fit Intercept",
        "description": "Specifies if a constant(a.k.a bias or intercept) should be added to the decision function",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "penalty",
        "displayName": "Penalty Option",
        "className": "penalty_lr",
        "description": "Regularization options for classification",
        "defaultValue": [
            {
                "selected": False,
                "name": "l1",
                "displayName": "l1"
            },
            {
                "selected": True,
                "name": "l2",
                "displayName": "l2"
            },
            {
                "selected": False,
                "name": "elasticnet",
                "displayName": "elasticnet"
            },
            {
                "selected": False,
                "name": "none",
                "displayName": "none"
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
        "name": "l1_ratio",
        "displayName": "L1 Ratio",
        "className": "l1_ratio_lr",
        "description": "Comparison of the sparsity (percentage of zero coefficients) of solutions when L1, "
                       "L2 and Elastic-Net penalty are used for different values of C",
        "defaultValue": 0,
        "acceptedValue": None,
        "valueRange": [
            0,
            1
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
            "int",
            "float"
        ],
        "allowedDataType": [
            "int",
            "float"
        ]
    },
    {
        "name": "multi_class",
        "displayName": "Multiclass Option",
        "description": "Nature of multiclass modeling options for classification",
        "defaultValue": [
            obj if obj["name"] != "ovr" else {"name": obj["name"], "selected": True, "displayName": obj["displayName"]}
            for obj in SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "solver",
        "displayName": "Solver Used",
        "className": "solver_lr",
        "description": "Algorithm to use in the Optimization",
        "defaultValue": [
            {
                "name": "newton-cg",
                "selected": False,
                "displayName": "newton-cg"
            },
            {
                "name": "lbfgs",
                "selected": True,
                "displayName": "lbfgs"
            },
            {
                "name": "sag",
                "selected": False,
                "displayName": "sag"
            },
            {
                "name": "liblinear",
                "selected": False,
                "displayName": "liblinear"
            },
            {
                "name": "saga",
                "selected": False,
                "displayName": "saga"
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
        "name": "warm_start",
        "displayName": "Warm Start",
        "description": "It reuses the solution of the previous call to fit as initialization",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "name": "class_weight",
        "className": "class_weight_lr",
        "displayName": "Class Weight",
        "description": "Weights associated with classes of the target column",
        "defaultValue": [
            {
                "name": "None",
                "selected": False,
                "displayName": "None"
            },
            {
                "name": "balanced",
                "selected": False,
                "displayName": "balanced"
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
        "name": "random_state",
        "className": "random_state_lr",
        "displayName": "Random Seed",
        "description": "The seed of the pseudo random number generator to use when shuffling the data",
        "defaultValue": None,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "C",
        "displayName": "Inverse of regularization strength",
        "description": "It refers to the inverse of regularization strength",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.1, 20.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float", "int"],
        "allowedDataType": ["float"]
    },

]

SKLEARN_ML_NEURAL_NETWORK_PARAMS = [
    {
        "name": "max_iter",
        "displayName": "Maximum Solver Iterations",
        "className": "max_iter_nn",
        "description": "Maximum number of iterations to be attempted for solver operations",
        "defaultValue": 200,
        "acceptedValue": None,
        "valueRange": [10, 400],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "tol",
        "displayName": "Convergence tolerance of iterations(e^-n)",
        "className": "tol_nn",
        "description": "Tolerance for the stopping criteria",
        "defaultValue": 4,
        "neural": True,
        "acceptedValue": None,
        "valueRange": [3, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]

    },
    {
        "name": "epsilon",
        "displayName": "Epsilon",
        "description": "Value for numerical stability in adam.",
        "defaultValue": 8,
        "acceptedValue": None,
        "valueRange": [3, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "n_iter_no_change",
        "displayName": "No of Iteration",
        "description": "Maximum number of epochs to not meet tol improvement.",
        "defaultValue": 10,
        "acceptedValue": None,
        "valueRange": [3, 10],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "solver",
        "displayName": "Solver Used",
        "className": "solver_nn",
        "description": "The solver for weight optimization.",
        # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_NNSOLVER_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "activation",
        "className": "activation_nn",
        "displayName": "Activation",
        "description": "Activation function for the hidden layer.",
        # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_ACTIVATION_CLASSIFICATION],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "shuffle",
        "displayName": "Shuffle",
        "description": "Whether to shuffle samples in each iteration.",
        "defaultValue": [
            {
                "name": "true",
                "selected": True,
                "displayName": "True"
            },
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "learning_rate",
        "className": "learning_rate_nn",
        "displayName": "Learning Rate",
        "description": "Learning rate schedule for weight updates.",
        # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_LEARNING_RATE_CLASSIFICATION],
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
        "description": "Size of minibatches for stochastic optimizers.",
        # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj  in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_BATCH_SIZE_CLASSIFICATION],
        "acceptedValue": None,
        "valueRange": [],
        "paramType": "list",
        "uiElemType": "checkBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int", "string"],
        "allowedDataType": ["int", "string"]
    },
    {
        "name": "nesterovs_momentum",
        "displayName": "Nesterovs momentum",
        "description": "Whether to use Nesterovs momentum.",
        "defaultValue": [
            {
                "name": "true",
                "selected": False,
                "displayName": "True"
            },
            {
                "name": "false",
                "selected": False,
                "displayName": "False"
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
        "name": "early_stopping",
        "displayName": "Early Stop",
        "description": "Whether to use early stopping to terminate training when validation score is not improving.",
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
        "name": "warm_start",
        "className": "warm_start_nn",
        "displayName": "Warm Start",
        "description": "It reuses the solution of the previous call to fit as initialization",
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
        "name": "verbose",
        "displayName": "Verbose",
        "description": "Whether to print progress messages to stdout.",
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
        "display": False,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "hidden_layer_sizes",
        "displayName": "Hidden Layer Size",
        "description": "Number of neurons in the ith hidden layer.",
        "defaultValue": 100,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["tuple"],
        "allowedDataType": ["int", "string"]
    },
    {
        "name": "learning_rate_init",
        "displayName": "Learning Rate Initialize",
        "description": "Controls the step-size in updating the weights.",
        "defaultValue": 0.001,
        "acceptedValue": None,
        "valueRange": [0.0001, 20.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["double"],
        "allowedDataType": ["double"]
    },
    {
        "name": "alpha",
        "className": "alpha_nn",
        "displayName": "Alpha",
        "description": "L2 penalty (regularization term) parameter.",
        "defaultValue": 0.0001,
        "acceptedValue": None,
        "valueRange": [0, 5],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["int", "float"]
    },
    # {
    # "name":"batch_size",
    # "displayName":"Batch Size",
    # "description": "Size of minibatches for stochastic optimizers.",
    # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
    # "defaultValue":"auto",
    # "acceptedValue":None,
    # "valueRange":[],
    # "paramType":"number",
    # "uiElemType":"textbox",
    # "display":True,
    # "hyperpatameterTuningCandidate":True,
    # "expectedDataType": ["int"],
    # "allowedDataType":["int"]
    # },
    {
        "name": "power_t",
        "displayName": "Power T",
        "description": "The exponent for inverse scaling learning rate.",
        "defaultValue": 0.5,
        "acceptedValue": None,
        "valueRange": [0.1, 20.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "random_state",
        "displayName": "Random Seed",
        "description": "The seed of the pseudo random number generator to use when shuffling the data",
        "defaultValue": 42,
        "acceptedValue": None,
        "valueRange": [1, 100],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": False,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "momentum",
        "displayName": "Momentum",
        "description": "Momentum for gradient descent update.",
        "defaultValue": 0.9,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "validation_fraction",
        "displayName": "Validation Fraction",
        "description": "The proportion of training data to set aside as validation set for early stopping.",
        "defaultValue": 0.1,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "beta_1 ",
        "displayName": "Beta 1",
        "description": "Exponential decay rate for estimates of first moment vector in adam.",
        "defaultValue": 0.9,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "beta_2 ",
        "displayName": "Beta 2",
        "description": "Exponential decay rate for estimates of second moment vector in adam.",
        "defaultValue": 0.999,
        "acceptedValue": None,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }

]

SKLEARN_ML_SUPPORTED_XGB_BOOSTER = [
    {"name": "gbtree", "selected": True, "displayName": "gbtree"},
    {"name": "dart", "selected": False, "displayName": "dart"},
    {"name": "gblinear", "selected": False, "displayName": "gblinear"},
]

SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS = [
    {"name": "auto", "selected": True, "displayName": "auto"},
    {"name": "exact", "selected": False, "displayName": "exact"},
    {"name": "approx", "selected": False, "displayName": "approx"},
    {"name": "hist", "selected": False, "displayName": "hist"},
    {"name": "gpu_exact", "selected": False, "displayName": "gpu_exact"},
    {"name": "gpu_hist", "selected": False, "displayName": "gpu_hist"},

]

SKLEARN_ML_XGBOOST_CLASSIFICATION_PARAMS = [
    {
        "name": "eta",
        "className": "eta_xg",
        "displayName": "Learning Rate",
        "description": "It is the step size shrinkage used to prevent Overfitting",
        "defaultValue": 0.3,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "gamma",
        "displayName": "Minimum Loss Reduction",
        "description": "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
        "defaultValue": 0,
        "acceptedValue": None,
        "valueRange": [0, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "max_depth",
        "displayName": "Maximum Depth",
        "description": "The maximum depth of a tree",
        "defaultValue": 6,
        "acceptedValue": None,
        "valueRange": [0, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "min_child_weight",
        "displayName": "Minimum Child Weight",
        "description": "The Minimum sum of Instance weight needed in a child node",
        "defaultValue": 1,
        "acceptedValue": None,
        "valueRange": [0, 100],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "subsample",
        "displayName": "Subsampling Ratio",
        "description": "It is the subsample ratio of the training instance",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.1, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "colsample_bytree",
        "displayName": "subsample ratio of columns for each tree",
        "description": "It is the subsample ratio of columns when constructing each tree",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.1, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "colsample_bylevel",
        "displayName": "subsample ratio of columns for each split",
        "description": "Subsample ratio of columns for each split in each level",
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
        "name": "booster",
        "displayName": "Booster Function",
        "description": "The booster function to be used",
        # "defaultValue":[obj if obj["name"] != "gbtree" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_BOOSTER],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_XGB_BOOSTER],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "tree_method",
        "displayName": "Tree Construction Algorithm",
        "description": "The Tree construction algorithm used in XGBoost",
        # "defaultValue":[obj if obj["name"] != "auto" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS],
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "process_type",
        "displayName": "Process Type",
        "description": "Boosting process to run",
        "defaultValue": [{"name": "default", "selected": True, "displayName": "Create New Trees"},
                         {"name": "update", "selected": True, "displayName": "Update Trees"}
                         ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "silent",
        "displayName": "Print Messages on Console",
        "description": "Runtime Message Printing",
        "defaultValue": [{"name": 0, "selected": False, "displayName": "True"},
                         {"name": 1, "selected": True, "displayName": "False"}],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": False,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "predictor",
        "displayName": "Type of Predictor Algorithm",
        "description": "The type of predictor algorithm to use",
        "defaultValue": [
            {"name": "cpu_predictor", "selected": True, "displayName": "Multicore CPU prediction algorithm"},
            {"name": "gpu_predictor", "selected": True, "displayName": "Prediction using GPU"}
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": False,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "class_weight",
        "className": "class_weight_xg",
        "displayName": "Class Weight",
        "description": "Weights associated with classes of the target column",
        "defaultValue": [
            {
                "name": "None",
                "selected": False,
                "displayName": "None"
            },
            {
                "name": "balanced",
                "selected": False,
                "displayName": "balanced"
            }
        ],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    }
]

SKLEARN_ML_NAIVE_BAYES_PARAMS = [
    {
        "name": "alpha",
        "className": "alpha_nb",
        "displayName": "Alpha",
        "description": "Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).",
        "defaultValue": 1.0,
        "acceptedValue": None,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
TENSORFLOW_ACTIVATION_PARAMETERS = [
    # {"name": "deserialize", "selected": True, "displayName": "deserialize"},
    {"name": "elu", "selected": False, "displayName": "elu"},
    {"name": "exponential", "selected": False, "displayName": "exponential"},
    # {"name":"get","selected":False,"displayName":"get"},
    {"name": "hard_sigmoid", "selected": False, "displayName": "hard_sigmoid"},
    {"name": "linear", "selected": False, "displayName": "Linear"},
    {"name": "relu", "selected": False, "displayName": "relu"},
    {"name": "selu", "selected": False, "displayName": "selu"},
    # {"name":"serialize","selected":False,"displayName":"serialize"},
    {"name": "sigmoid", "selected": False, "displayName": "sigmoid"},
    {"name": "softmax", "selected": False, "displayName": "softmax"},
    {"name": "softplus", "selected": False, "displayName": "softplus"},
    {"name": "softsign", "selected": False, "displayName": "softsign"},
    {"name": "tanh", "selected": False, "displayName": "tanh"},
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
    {"name": "Addition", "selected": True, "displayName": "Addition"},
    {"name": "Subtraction", "selected": True, "displayName": "Subtraction"},
    {"name": "Multiplication", "selected": True, "displayName": "Multiplication"},
    {"name": "Division", "selected": True, "displayName": "Division"},
]
SKLEARN_ML_SUPPORTED_TF_LOSS_PARAMETERS = [
    {"name": "sparse_categorical_crossentropy", "selected": True, "displayName": "sparse_categorical_crossentropy"},
    {"name": "squared_hinge", "selected": False, "displayName": "squared_hinge"},
    {"name": "hinge", "selected": False, "displayName": "hinge"},
    {"name": "categorical_hinge", "selected": False, "displayName": "categorical_hinge"},
    {"name": "categorical_crossentropy", "selected": False, "displayName": "categorical_crossentropy"},
    {"name": "binary_crossentropy", "selected": False, "displayName": "binary_crossentropy"},
    {"name": "kullback_leibler_divergence", "selected": False, "displayName": "kullback_leibler_divergence"},
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
TF_CLASSIFICATION_METRICS = [
    {"name": "sparse_categorical_crossentropy", "selected": True, "displayName": "sparse_categorical_crossentropy"},
    {"name": "binary_crossentropy", "selected": False, "displayName": "binary_crossentropy"},
    {"name": "categorical_accuracy", "selected": False, "displayName": "categorical_accuracy"},
    {"name": "categorical_crossentropy", "selected": False, "displayName": "categorical_crossentropy"},
    {"name": "FalseNegatives", "selected": False, "displayName": "FalseNegatives"},
    {"name": "FalsePositives", "selected": False, "displayName": "FalsePositives"},
    {"name": "sparse_categorical_accuracy", "selected": False, "displayName": "sparse_categorical_accuracy"},
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
        "displayName": "Use Bias",
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
        "name": "batch_normalization",
        "displayName": "Batch Normalization",
        "description": "It is used to normalize the input layer by adjusting and scaling the activations.",
        "defaultValue": [
            {
                "name": "false",
                "selected": True,
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
        "displayName": "Kernel Initializer",
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
        "displayName": "Bias Initializer",
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
        "displayName": "Kernel Regularizer",
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
        "displayName": "Bias Regularizer",
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
        "displayName": "Activity Regularizer",
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
        "displayName": "Kernel Constraint",
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
        "displayName": "Bias Constraint",
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
        "uiElemType": "textbox",
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
        "acceptedValue": None,
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
        "defaultValue": None,
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": [],
        "allowedDataType": []
    },
]
SKLEARN_ML_SUPPORTED_TF_LAYER = [
    {"name": "Dense", "selected": True, "displayName": "Dense",
     "parameters": [obj for obj in TENSORFLOW_DENSE_PARAMETERS]},
    {"name": "Dropout", "selected": False, "displayName": "Dropout",
     "parameters": [obj for obj in TENSORFLOW_DROPOUT_PARAMETERS]},
    # {"name": "Lambda", "selected": False, "displayName": "Lambda","parameters":[obj for obj in TENSORFLOW_LAMBDA_PARAMETERS]}
]

SKLEARN_ML_TENSORFLOW_CLASSIFICATION_PARAMS = [
    {
        "name": "layer",
        "displayName": "Layer",
        "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_TF_LAYER],
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
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_TF_LOSS_PARAMETERS],
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
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_TF_OPTIMIZER_PARAMETERS],
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
        "defaultValue": 0,
        "acceptedValue": 100,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
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
        "acceptedValue": 100,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "metrics",
        "displayName": "Metrics",
        "description": "List of metrics to be evaluated by the model during training And testing.",
        "defaultValue": [obj for obj in TF_CLASSIFICATION_METRICS],
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
        "name": "learning_rate",
        "displayName": "Learning Rate",
        "description": "It is the step size shrinkage used to prevent Overfitting",
        "defaultValue": 0.3,
        "acceptedValue": None,
        "valueRange": [
            0,
            1
        ],
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": [
            "int",
            "float"
        ],
        "allowedDataType": [
            "int",
            "float"
        ]
    },
]
