############################      Regression      ###############################
AUTOML_SKLEARN_ML_LINEAR_REGRESSION_PARAMS = [
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

AUTOML_SKLEARN_ML_SUPPORTED_LOSS = [
    {"name":"ls","selected":True,"displayName":"Least Squares Regression"},
    {"name":"lad","selected":False,"displayName":"Least Absolute Deviation"},
    {"name":"huber","selected":False,"displayName":"Huber"},
    {"name":"quantile","selected":False,"displayName":"Quantile Regression"},
]

AUTOML_SKLEARN_ML_GBT_REGRESSION_PARAMS = [
        {
            "name":"loss",
            "displayName":"Loss Function",
            "description":"It is the loss function to be optimized",
            "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in AUTOML_SKLEARN_ML_SUPPORTED_LOSS],
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

AUTOML_SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION = [
    {"name":"friedman_mse","selected":True,"displayName":"Friedman Mse"},
    {"name":"mse","selected":True,"displayName":"Mean Squared Error"},
    {"name":"mae","selected":True,"displayName":"Mean Absolute Error"},
]

AUTOML_SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS = [
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
                    "name":"criterion",
                    "displayName":"Measure For quality of a split",
                    "description":"The function to measure the quality of a split",
                    "defaultValue":[{"name":obj["name"],"selected":obj["selected"],"displayName":obj["displayName"]} for obj in AUTOML_SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_REGRESSION],
                    "paramType":"list",
                    "uiElemType":"checkbox",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["string"],
                    "allowedDataType":["string"]

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
                    "name":"max_leaf_nodes",
                    "displayName":"Maximum Number of Leaf Nodes",
                    "description":"The maximum of number of leaf nodes",
                    "defaultValue":None,
                    "acceptedValue":None,
                    "valueRange":[],
                    "paramType":"number",
                    "uiElemType":"textBox",
                    "display":True,
                    "hyperpatameterTuningCandidate":False,
                    "expectedDataType": ["int", None],
                    "allowedDataType": ["int",None]
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
                 "name":"random_state",
                 "displayName":"Random Seed",
                 "description":"The seed of the pseudo random number generator to use when shuffling the data",
                 "defaultValue":None,
                 "acceptedValue":None,
                 "valueRange":[1,100],
                 "paramType":"number",
                 "uiElemType":"textBox",
                 "display":True,
                 "hyperpatameterTuningCandidate":False,
                 "expectedDataType": ["int", None],
                 "allowedDataType": ["int", None]

                }
]


AUTOML_SKLEARN_ML_RF_REGRESSION_PARAMS = AUTOML_SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
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
    }
]

AUTOML_SKLEARN_ML_DTREE_REGRESSION_PARAMS = AUTOML_SKLEARN_ML_TREE_BASED_REGRESSION_COMMON_PARAMS + [
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

]

###########################   CLASSIFICATION Config  ####################################
AUTOML_SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION = [
    {"name":"ovr","selected":False,"displayName":"One Vs Rest"},
    {"name":"multinomial","selected":False,"displayName":"Multinomial"}
]
AUTOML_SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION = [
    {"name":"newton-cg","selected":False,"displayName":"newton-cg","penalty":"l2"},
    {"name":"lbfgs","selected":False,"displayName":"lbfgs","penalty":"l2"},
    {"name":"sag","selected":False,"displayName":"sag","penalty":"l2"},
    # {"name":"liblinear","selected":False,"displayName":"liblinear","penalty":"l1"},
    {"name":"saga","selected":False,"displayName":"saga","penalty":"l1"},

]
AUTOML_SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION = [
    {"name":"gini","selected":False,"displayName":"Gini Impurity"},
    {"name":"entropy","selected":False,"displayName":"Entropy"},
]

AUTOML_SKLEARN_ML_LOGISTIC_REGRESSION_PARAMS = [
        {
            "name":"max_iter",
            "displayName":"Maximum Solver Iterations",
            "description": "Maximum number of iterations to be attempted for solver operations",
            "defaultValue":100,
            "acceptedValue":None,
            "valueRange":[10,400],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["int"],
            "allowedDataType":["int"]
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
            "name":"tol",
            "displayName":"Convergence tolerance of iterations(e^-n)",
           "description": "Tolerance for the stopping criteria",
            "defaultValue":4,
            "acceptedValue":None,
            "valueRange":[3,10],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["int"],
            "allowedDataType":["int"]

        },
        {
            "name":"fit_intercept",
            "displayName":"Fit Intercept",
            "description":"Specifies if a constant(a.k.a bias or intercept) should be added to the decision function",
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
            "name":"solver",
            "displayName":"Solver Used",
            "description": "Algorithm to use in the Optimization",
            # "defaultValue":[obj if obj["name"] != "lbfgs" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
            "defaultValue":[obj for obj in AUTOML_SKLEARN_ML_SUPPORTED_SOLVER_CLASSIFICATION],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["string"],
            "allowedDataType":["string"]
        },
        {
            "name":"multi_class",
            "displayName":"Multiclass Option",
            "description": "Nature of multiclass modeling options for classification",
            "defaultValue":[obj if obj["name"] != "ovr" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in AUTOML_SKLEARN_ML_SUPPORTED_MULTICLASS_OPTION],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["string"],
            "allowedDataType":["string"]
        },
        {
            "name":"warm_start",
            "displayName":"Warm Start",
            "description": "It reuses the solution of the previous call to fit as initialization",
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
            "allowedDataType":["bool"]
        },
         {
             "name":"random_state",
             "displayName":"Random Seed",
            "description": "The seed of the pseudo random number generator to use when shuffling the data",
             "defaultValue":None,
             "acceptedValue":None,
             "valueRange":[1,100],
             "paramType":"number",
             "uiElemType":"textBox",
             "display":True,
             "hyperpatameterTuningCandidate":False,
             "expectedDataType": ["int"],
             "allowedDataType":["int"]
         },
         {
             "name":"C",
             "displayName":"Inverse of regularization strength",
            "description": "It refers to the inverse of regularization strength",
             "defaultValue":1.0,
             "acceptedValue":None,
             "valueRange":[0.1,20.0],
             "paramType":"number",
             "uiElemType":"textBox",
             "display":True,
             "hyperpatameterTuningCandidate":True,
             "expectedDataType": ["float","int"],
             "allowedDataType":["float"]
         },
         {
             "name":"class_weight",
             "displayName":"Class Weight",
             "description": "Weights associated with classes of the target column",
             "defaultValue":[
              {
                  "name":"None",
                  "selected":False,
                  "displayName":"None"
              },
              {
                  "name":"balanced",
                  "selected":False,
                  "displayName":"balanced"
              }
             ],
             "paramType":"list",
             "uiElemType":"checkbox",
             "display":True,
             "hyperpatameterTuningCandidate":False,
             "expectedDataType": ["bool"],
             "allowedDataType":["bool"]
         }
]

AUTOML_SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS = [
               {
                    "name":"max_depth",
                    "displayName":"Max Depth",
                    "description":"The maximum depth of the tree",
                    "defaultValue":5,
                    "acceptedValue":None,
                    "valueRange":[2,20],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["int",None],
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
                    "name":"min_impurity_decrease",
                    "displayName":"Impurity Decrease cutoff for Split",
                    "description":"A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
                    "defaultValue":0.0,
                    "acceptedValue":None,
                    "valueRange":[0.0,1.0],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True,
                    "hyperpatameterTuningCandidate":True,
                    "expectedDataType": ["float"],
                    "allowedDataType": ["float"]
                },
]

AUTOML_SKLEANR_ML_RF_CLASSIFICATION_PARAMS = AUTOML_SKLEARN_ML_TREE_BASED_CLASSIFICATION_COMMON_PARAMS + [
        {
            "name":"n_estimators",
            "displayName":"No of Estimators",
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
            "name":"criterion",
            "displayName":"Criterion",
            "description":"The function to measure the quality of a split",
            # "defaultValue":[obj if obj["name"] != "gini" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
            "defaultValue":[obj for obj in AUTOML_SKLEARN_ML_SUPPORTED_SPLIT_CRITERION_CLASSIFICATION],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType":["string"],
            "allowedDataType":["string"]
        },
        {
            "name":"max_leaf_nodes",
            "displayName":"Max Leaf Nodes",
            "description":"The maximum of number of leaf nodes",
            "defaultValue":None,
            "acceptedValue":None,
            "valueRange":[],
            "paramType":"number",
            "uiElemType":"textBox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["int", None],
            "allowedDataType": ["int",None]
        },
        {
         "name":"random_state",
         "displayName":"Random Seed",
         "description":"The seed of the pseudo random number generator to use when shuffling the data",
         "defaultValue":None,
         "acceptedValue":None,
         "valueRange":[1,100],
         "paramType":"number",
         "uiElemType":"textBox",
         "display":True,
         "hyperpatameterTuningCandidate":False,
         "expectedDataType": ["int", None],
         "allowedDataType": ["int", None]
        },
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
                 "selected":False,
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
            "display":False,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["bool"],
            "allowedDataType": ["bool"]
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
            "display":False,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["bool"],
            "allowedDataType": ["bool"]
        },
        {
            "name":"class_weight",
            "displayName":"Class Weight",
            "description": "Weights associated with classes of the target column",
            "defaultValue":[
             {
                 "name":"None",
                 "selected":False,
                 "displayName":"None"
             },
             {
                 "name":"balanced",
                 "selected":False,
                 "displayName":"balanced"
             }
            ],
            "paramType":"list",
            "uiElemType":"checkbox",
            "display":True,
            "hyperpatameterTuningCandidate":False,
            "expectedDataType": ["bool"],
            "allowedDataType":["bool"]
        }
]

AUTOML_SKLEARN_ML_SUPPORTED_XGB_BOOSTER = [
    {"name":"gbtree","selected":True,"displayName":"gbtree"},
    {"name":"dart","selected":True,"displayName":"dart"},
    {"name":"gblinear","selected":True,"displayName":"gblinear"},
]

AUTOML_SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS = [
    {"name":"auto","selected":True,"displayName":"auto"},
    {"name":"exact","selected":True,"displayName":"exact"},
    {"name":"approx","selected":True,"displayName":"approx"},
    {"name":"hist","selected":True,"displayName":"hist"},
    {"name":"gpu_exact","selected":True,"displayName":"gpu_exact"},
    {"name":"gpu_hist","selected":True,"displayName":"gpu_hist"},

]

AUTOML_SKLEARN_ML_XGBOOST_CLASSIFICATION_PARAMS = [
    {
        "name":"eta",
        "displayName":"Learning Rate",
        "description" : "It is the step size shrinkage used to prevent Overfitting",
        "defaultValue":0.3,
        "acceptedValue":None,
        "valueRange":[0.0,1.0],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["float"],
        "allowedDataType":["float"]
    },
    {
        "name":"gamma",
        "displayName":"Minimum Loss Reduction",
        "description" : "It is the minimum loss reduction required to make a further partition on a leaf node of the tree",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["int"],
        "allowedDataType":["int"]
    },
    {
        "name":"max_depth",
        "displayName":"Maximum Depth",
        "description" : "The maximum depth of a tree",
        "defaultValue":6,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["int"],
        "allowedDataType":["int"]
    },
    {
        "name":"min_child_weight",
        "displayName":"Minimum Child Weight",
        "description":"The Minimum sum of Instance weight needed in a child node",
        "defaultValue":1,
        "acceptedValue":None,
        "valueRange":[0,100],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["int"],
        "allowedDataType":["int"]
    },
    {
        "name":"subsample",
        "displayName":"Subsampling Ratio",
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
        "name":"colsample_bytree",
        "displayName":"subsample ratio of columns for each tree",
        "description":"It is the subsample ratio of columns when constructing each tree",
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
        "name":"colsample_bylevel",
        "displayName":"subsample ratio of columns for each split",
        "description":"Subsample ratio of columns for each split in each level",
        "defaultValue":1.0,
        "acceptedValue":None,
        "valueRange":[0.1,1.0],
        "paramType":"number",
        "uiElemType":"slider",
        "display":True,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["float"],
        "allowedDataType":["float"]
    },
    {
        "name":"booster",
        "displayName" : "Booster Function",
        "description" : "The booster function to be used",
        # "defaultValue":[obj if obj["name"] != "gbtree" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_BOOSTER],
        "defaultValue":[obj for obj in AUTOML_SKLEARN_ML_SUPPORTED_XGB_BOOSTER],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["string"],
        "allowedDataType":["string"]
    },
    {
        "name":"tree_method",
        "displayName":"Tree Construction Algorithm",
        "description":"The Tree construction algorithm used in XGBoost",
        # "defaultValue":[obj if obj["name"] != "auto" else {"name":obj["name"],"selected":True,"displayName":obj["displayName"]} for obj in SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS],
        "defaultValue":[obj for obj in AUTOML_SKLEARN_ML_SUPPORTED_XGB_TREE_ALGORITHMS],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name":"process_type",
        "displayName":"Process Type",
        "description":"Boosting process to run",
        "defaultValue":[{"name":"default","selected":True,"displayName":"Create New Trees"},
                {"name":"update","selected":True,"displayName":"Update Trees"}
            ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":True,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name":"silent",
        "displayName":"Print Messages on Console",
        "description" : "Runtime Message Printing",
        "defaultValue":[{"name":0,"selected":False,"displayName":"True"},{"name":1,"selected":True,"displayName":"False"}],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":False,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["int"],
        "allowedDataType":["int"]
    },
    {
        "name":"predictor",
        "displayName":"Type of Predictor Algorithm",
        "description":"The type of predictor algorithm to use",
        "defaultValue":[{"name":"cpu_predictor","selected":True,"displayName":"Multicore CPU prediction algorithm"},
                {"name":"gpu_predictor","selected":True,"displayName":"Prediction using GPU"}
            ],
        "paramType":"list",
        "uiElemType":"checkbox",
        "display":False,
        "hyperpatameterTuningCandidate":False,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]

AUTOML_SKLEARN_ML_NAIVE_BAYES_PARAMS = [
         {
            "name":"alpha",
            "displayName":"Alpha",
            "description" : "Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).",
            "defaultValue":1.0,
            "acceptedValue":None,
            "valueRange":[0.0,1.0],
            "paramType":"number",
            "uiElemType":"slider",
            "display":True,
            "hyperpatameterTuningCandidate":True,
            "expectedDataType": ["float"],
            "allowedDataType":["float"]
        },
    ]
