PT_ACTIVATION_ELU_PARAMS = [
    {
        "name": "alpha",
        "displayName": "alpha",
        "description": "the alpha value for the ELU formulation.",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Hardshrink_PARAMS = [
    {
        "name": "lambd",
        "displayName": "lambd",
        "description": "the lambda value for the Hardshrink formulation.",
        "defaultValue": 0.5,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Hardtanh_PARAMS = [
    {
        "name": "min_val",
        "displayName": "min_val",
        "description": "minimum value of the linear region range.",
        "defaultValue": -1,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_LeakyReLU_PARAMS = [
    {
        "name": "negative_slope",
        "displayName": "negative_slope",
        "description": "Controls the angle of the negative slope.",
        "defaultValue": 0.01,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_MultiheadAttention_PARAMS = [
    {
        "name": "embed_dim",
        "displayName": "embed_dim",
        "description": "total dimension of the model.",
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "bias",
        "displayName": "bias",
        "description": "",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "add_bias_kv",
        "displayName": "add_bias_kv",
        "description": "add bias to the key and value sequences at dim=0.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "add_zero_attn",
        "displayName": "add_zero_attn",
        "description": "add a new batch of zeros to the key and Value sequences at dim=1.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]
PT_ACTIVATION_PreLU_PARAMS = [
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
PT_ACTIVATION_RreLU_PARAMS = [
    {
        "name": "lower",
        "displayName": "lower",
        "description": "lower bound of the uniform distribution.",
        "defaultValue": 0.125,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_CELU_PARAMS = [
    {
        "name": "alpha",
        "displayName": "alpha",
        "description": "the alpha value for the CELU formulation.",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Softplus_PARAMS = [
    {
        "name": "beta",
        "displayName": "beta",
        "description": "the beta value for the Softplus formulation.",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Softshrink_PARAMS = [
    {
        "name": "lambd",
        "displayName": "lambd",
        "description": "the lambda value for the Softshrink formulation.",
        "defaultValue": 0.5,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Threshold_PARAMS = [
    {
        "name": "threshold",
        "displayName": "threshold",
        "description": "The value to threshold at.",
        "defaultValue": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_ACTIVATION_Softmin_PARAMS = [
    {
        "name": "dim",
        "displayName": "dim",
        "description": "A dimension along which Softmin will be computed.",
        "defaultValue": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]
PT_ACTIVATION_Softmax_PARAMS = [
    {
        "name": "dim",
        "displayName": "dim",
        "description": "A dimension along which Softmax will be computed.",
        "defaultValue": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]
PT_ACTIVATION_LogSoftmax_PARAMS = [
    {
        "name": "dim",
        "displayName": "dim",
        "description": "A dimension along which LogSoftmax will be computed.",
        "defaultValue": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]
PT_ACTIVATION_AdaptiveLogSoftmaxWithLoss_PARAMS = [
    {
        "name": "n_classes",
        "displayName": "n_classes",
        "description": "Number of classes in the dataset.",
        "defaultValue": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "head_bias",
        "displayName": "head_bias",
        "description": "If True, adds a bias term to the 'head' of the Adaptive softmax.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    }
]

PYTORCH_ACTIVATION_PARAMETERS = [
    {"name": "ELU", "selected": False, "displayName": "ELU",
     "parameters": [obj for obj in PT_ACTIVATION_ELU_PARAMS]},
    {"name": "Hardshrink", "selected": False, "displayName": "Hardshrink",
     "parameters": [obj for obj in PT_ACTIVATION_Hardshrink_PARAMS]},
    {"name": "Hardtanh", "selected": False, "displayName": "Hardtanh",
     "parameters": [obj for obj in PT_ACTIVATION_Hardtanh_PARAMS]},
    {"name": "LeakyReLU", "selected": False, "displayName": "LeakyReLU",
     "parameters": [obj for obj in PT_ACTIVATION_LeakyReLU_PARAMS]},
    {"name": "LogSigmoid", "selected": False, "displayName": "LogSigmoid", "parameters": None},
    {"name": "MultiheadAttention", "selected": False, "displayName": "MultiheadAttention",
     "parameters": [obj for obj in PT_ACTIVATION_MultiheadAttention_PARAMS]},
    {"name": "PreLU", "selected": False, "displayName": "PreLU",
     "parameters": [obj for obj in PT_ACTIVATION_PreLU_PARAMS]},
    {"name": "ReLU", "selected": False, "displayName": "ReLU", "parameters": None},
    {"name": "ReLU6", "selected": False, "displayName": "ReLU6", "parameters": None},
    {"name": "RreLU", "selected": False, "displayName": "RreLU",
     "parameters": [obj for obj in PT_ACTIVATION_RreLU_PARAMS]},
    {"name": "SELU", "selected": False, "displayName": "SELU", "parameters": None},
    {"name": "CELU", "selected": False, "displayName": "CELU",
     "parameters": [obj for obj in PT_ACTIVATION_CELU_PARAMS]},
    {"name": "GELU", "selected": False, "displayName": "GELU", "parameters": None},
    {"name": "Sigmoid", "selected": False, "displayName": "Sigmoid", "parameters": None},
    {"name": "Softplus", "selected": False, "displayName": "Softplus",
     "parameters": [obj for obj in PT_ACTIVATION_Softplus_PARAMS]},
    {"name": "Softshrink", "selected": False, "displayName": "Softshrink",
     "parameters": [obj for obj in PT_ACTIVATION_Softshrink_PARAMS]},
    {"name": "Softsign", "selected": False, "displayName": "Softsign", "parameters": None},
    {"name": "Tanh", "selected": False, "displayName": "Tanh", "parameters": None},
    {"name": "Tanhshrink", "selected": False, "displayName": "Tanhshrink", "parameters": None},
    {"name": "Threshold", "selected": False, "displayName": "Threshold",
     "parameters": [obj for obj in PT_ACTIVATION_Threshold_PARAMS]},
    {"name": "Softmin", "selected": False, "displayName": "Softmin",
     "parameters": [obj for obj in PT_ACTIVATION_Softmin_PARAMS]},
    {"name": "Softmax", "selected": False, "displayName": "Softmax",
     "parameters": [obj for obj in PT_ACTIVATION_Softmax_PARAMS]},
    {"name": "Softmax2d", "selected": False, "displayName": "Softmax2d", "parameters": None},
    {"name": "LogSoftmax", "selected": False, "displayName": "LogSoftmax",
     "parameters": [obj for obj in PT_ACTIVATION_LogSoftmax_PARAMS]},
    {"name": "AdaptiveLogSoftmaxWithLoss", "selected": False, "displayName": "AdaptiveLogSoftmaxWithLoss",
     "parameters": [obj for obj in PT_ACTIVATION_AdaptiveLogSoftmaxWithLoss_PARAMS]}
]

PT_DROPOUT_P_PARAMS = [
    {
        "name": "p",
        "displayName": "p",
        "description": "probability of an element to be dropped.",
        "defaultValue": 0.5,
        "paramType": "number",
        "uiElemType": "slider",
        "display": True,
        "valueRange": [0, 1],
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]

PYTORCH_DROPOUT_PARAMETERS = [
    {"name": "Dropout", "selected": False, "displayName": "Dropout",
     "parameters": [obj for obj in PT_DROPOUT_P_PARAMS]}
]

PT_BATCHNORMALIZATION_BatchNorm1d_PARAMS = [
    {
        "name": "num_features",
        "displayName": "num_features",
        "description": "C from an expected input of size (N,C,L) or L from input of size (N, L).",
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "a value added to the denominator for numerical stability.",
        "defaultValue": 0.00001,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "affine",
        "displayName": "affine",
        "description": "a boolean value that when set to True, this module has learnable affine parameters, initialized the same way as done for batch normalization.",
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
        "valueRange": [0, 1],
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "track_running_stats",
        "displayName": "track_running_stats",
        "description": "a boolean value that when set to True, this module tracks the running mean and variance, and when set to False, this module does not track such statistics and always uses batch statistics in both training and eval modes.",
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
        "valueRange": [0, 1],
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
]

PYTORCH_BATCHNORMALIZATION_PARAMETERS = [
    {"name": "BatchNorm1d", "selected": False, "displayName": "BatchNorm1d",
     "parameters": [obj for obj in PT_BATCHNORMALIZATION_BatchNorm1d_PARAMS]}
]

PT_BIAS_INIT_Uniform_PARAMS = [
    {
        "name": "lower_bound",
        "displayName": "lower bound",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 0.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_BIAS_INIT_Normal_PARAMS = [
    {
        "name": "mean",
        "displayName": "mean",
        "description": "Fills the input Tensor with values drawn from the normal distribution,N(mean,std^2)",
        "defaultValue": 0.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_BIAS_INIT_Constant_PARAMS = [
    {
        "name": "val",
        "displayName": "val",
        "description": "Fills the input Tensor with the value {val}",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]

PYTORCH_BIAS_INIT_PARAMETERS = [
    {"name": "Uniform", "selected": False, "displayName": "Uniform",
     "parameters": [obj for obj in PT_BIAS_INIT_Uniform_PARAMS]},
    {"name": "Normal", "selected": False, "displayName": "Normal",
     "parameters": [obj for obj in PT_BIAS_INIT_Normal_PARAMS]},
    {"name": "Constant", "selected": False, "displayName": "Constant",
     "parameters": [obj for obj in PT_BIAS_INIT_Constant_PARAMS]},
    {
        "name": "Ones",
        "displayName": "Ones",
        "description": "Input Units parameter for the hidden layer.",
        "selected": False,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]

PT_WEIGHT_INIT_xavier_uniform_PARAMS = [
    {
        "name": "gain",
        "displayName": "gain",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_WEIGHT_INIT_xavier_normal_PARAMS = [
    {
        "name": "gain",
        "displayName": "gain",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_WEIGHT_INIT_Kaiming_Normal_PARAMS = [
    {
        "name": "a",
        "displayName": "a",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 0.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
]

PT_WEIGHT_INIT_Orthogonal_PARAMS = [
    {
        "name": "gain",
        "displayName": "gain",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 1.0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_WEIGHT_INIT_Sparse_PARAMS = [
    {
        "name": "sparsity",
        "displayName": "sparsity",
        "description": "Fills the input Tensor with values drawn from the uniform distribution U(lower_bound, upper_bound)",
        "defaultValue": 0.5,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PT_WEIGHT_CONSTRAINT_TRUE_PARAMS = [
    {
        "name": "min",
        "displayName": "min",
        "description": "minimum value.",
        "defaultValue": 0.3,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

PYTORCH_WEIGHT_INIT_PARAMETERS = [
    {"name": "Uniform", "selected": False, "displayName": "Uniform",
     "parameters": [obj for obj in PT_BIAS_INIT_Uniform_PARAMS]},
    {"name": "Normal", "selected": False, "displayName": "Normal",
     "parameters": [obj for obj in PT_BIAS_INIT_Normal_PARAMS]},
    {"name": "Constant", "selected": False, "displayName": "Constant",
     "parameters": [obj for obj in PT_BIAS_INIT_Constant_PARAMS]},
    {
        "name": "Ones",
        "displayName": "Ones",
        "description": "Input Units parameter for the hidden layer.",
        "selected": False,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {"name": "Xavier_Uniform", "selected": False, "displayName": "Xavier Uniform",
     "parameters": [obj for obj in PT_WEIGHT_INIT_xavier_uniform_PARAMS]},
    {"name": "Xavier_Normal", "selected": False, "displayName": "Xavier Normal",
     "parameters": [obj for obj in PT_WEIGHT_INIT_xavier_normal_PARAMS]},
    {"name": "Kaiming_Normal", "selected": False, "displayName": "Kaiming Normal",
     "parameters": [obj for obj in PT_WEIGHT_INIT_Kaiming_Normal_PARAMS]},
    {"name": "Orthogonal", "selected": False, "displayName": "Orthogonal",
     "parameters": [obj for obj in PT_WEIGHT_INIT_Orthogonal_PARAMS]},
    {"name": "Sparse", "selected": False, "displayName": "Sparse",
     "parameters": [obj for obj in PT_WEIGHT_INIT_Sparse_PARAMS]},
    {"name": "Default", "selected": True, "displayName": "Default",
     "parameters": None},
]


PT_WEIGHT_CONSTRAINT_CONSTRAINT_PARAMS = [
    {
        "name": "constraint",
        "displayName": "constraint",
        "description": "constraint",
        "defaultValue": [
            {
                "name": "True",
                "selected": False,
                "displayName": "True",
                "parameters": [PT_WEIGHT_CONSTRAINT_TRUE_PARAMS]
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
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
]

PYTORCH_WEIGHT_CONSTRAINT_PARAMETERS = [
    {"name": "constraint", "selected": True, "displayName": "constraint",
     "parameters": [obj for obj in PT_WEIGHT_CONSTRAINT_CONSTRAINT_PARAMS]},
]

PT_BIAS_PARAMS = [
    {
        "name": "bias_init",
        "displayName": "bias_init",
        "description": "Bias initialisation parameter for the hidden layer.",
        "defaultValue": [obj for obj in PYTORCH_BIAS_INIT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
]


PYTORCH_LINEAR_PARAMETERS = [
    {
        "name": "activation",
        "displayName": "Activation",
        "description": "Activation function for the hidden layer.",
        "defaultValue": [obj for obj in PYTORCH_ACTIVATION_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "dropout",
        "displayName": "Dropout",
        "description": "During training, randomly zeroes some of the elements of the input tensor with probability p using samples from a Bernoulli distribution.",
        "defaultValue": [obj for obj in PYTORCH_DROPOUT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "batchnormalization",
        "displayName": "Batch Normalization",
        "description": "Applies Batch Normalization over a 2D or 3D input (a mini-batch of 1D inputs with optional additional channel dimension) as described in the paper.",
        "defaultValue": [obj for obj in PYTORCH_BATCHNORMALIZATION_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "bias_init",
        "displayName": "bias_init",
        "description": "Bias initialisation parameter for the hidden layer.",
        "defaultValue": [obj for obj in PYTORCH_BIAS_INIT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "weight_init",
        "displayName": "weight_init",
        "description": "Weight initialisation parameter for the hidden layer.",
        "defaultValue": [obj for obj in PYTORCH_WEIGHT_INIT_PARAMETERS],
        "paramType": "list",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
                "parameters": [PT_WEIGHT_CONSTRAINT_TRUE_PARAMS]
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
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
]

SKLEARN_ML_SUPPORTED_PT_LAYER = [
    {"name": "Linear", "selected": True, "displayName": "Linear",
     "parameters": [obj for obj in PYTORCH_LINEAR_PARAMETERS]}
]

PT_OPTIMIZER_Adadelta_PARAMETERS = [
    {
        "name": "rho",
        "displayName": "rho",
        "description": "coefficient used for computing a running average of squared gradients.",
        "defaultValue": 0.9,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.000001,
        "paramType": "number",
        "uiElemType": "textBox",
        "valueRange": [0.000001, 1],
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "lr",
        "displayName": "lr",
        "description": "coefficient that scale delta before it is applied to the parameters.",
        "defaultValue": 1.0,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_OPTIMIZER_Adagrad_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.01,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.0000000001,
        "valueRange": [0.0000000001, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
PT_OPTIMIZER_Adam_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.001,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "betas",
        "displayName": "betas",
        "description": "coefficients used for computing running averages of gradient and its square.",
        "defaultValue": [0.9, 0.999],
        "valueRange": [[0.0, 1.0], [0.0, 1.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.00000001,
        "valueRange": [0.0000000001, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "amsgrad",
        "displayName": "amsgrad",
        "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
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
    }
]
PT_OPTIMIZER_AdamW_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.001,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "betas",
        "displayName": "betas",
        "description": "coefficients used for computing running averages of gradient and its square.",
        "defaultValue": [0.9, 0.999],
        "valueRange": [[0.0, 1.0], [0.0, 1.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.00000001,
        "valueRange": [0.00000001, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0.01,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "amsgrad",
        "displayName": "amsgrad",
        "description": "whether to use the AMSGrad variant of this algorithm from the paper.",
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
    }
]
PT_OPTIMIZER_SparseAdam_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.001,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "betas",
        "displayName": "betas",
        "description": "coefficients used for computing running averages of gradient and its square.",
        "defaultValue": [0.9, 0.999],
        "valueRange": [[0.0, 1.0], [0.0, 1.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.00000001,
        "valueRange": [0.00000001, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_OPTIMIZER_Adamax_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.001,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "betas",
        "displayName": "betas",
        "description": "coefficients used for computing running averages of gradient and its square.",
        "defaultValue": [0.9, 0.999],
        "valueRange": [[0.0, 1.0], [0.0, 1.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.00000001,
        "valueRange": [0.00000001, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
PT_OPTIMIZER_ASGD_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.01,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "t0",
        "displayName": "t0",
        "description": "point at which to start averaging.",
        "defaultValue": 0.000001,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0.0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_OPTIMIZER_LBFGS_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 1,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "tolerance_grad",
        "displayName": "tolerance_grad",
        "description": " termination tolerance on first order optimality.",
        "defaultValue": 0.00001,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "tolerance_change",
        "displayName": "tolerance_change",
        "description": "termination tolerance on function value/parameter changes.",
        "defaultValue": 0.000000001,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
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
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
PT_OPTIMIZER_RMSprop_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.01,
        "valueRange": [0.0, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "term added to the denominator to improve numerical stability.",
        "defaultValue": 0.00000001,
        "valueRange": [0.00000001, 1.0],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "centered",
        "displayName": "centered",
        "description": "if True, compute the centered RMSProp, the gradient is normalized By an estimation of its variance.",
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
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]
PT_OPTIMIZER_Rprop_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.01,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "eta",
        "displayName": "eta",
        "description": "pair of (etaminus, etaplUs), that are multiplicative.",
        "defaultValue": [0.5, 1.2],
        "valueRange": [[0.0, 5.0], [0.0, 5.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "step_sizes",
        "displayName": "step_sizes",
        "description": "a pair of minimal and maximal allowed step sizes.",
        "defaultValue": [0.000001, 50],
        "valueRange": [[0.0, 5.0], [0.0, 5.0]],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    }
]
PT_OPTIMIZER_SGD_PARAMETERS = [
    {
        "name": "lr",
        "displayName": "lr",
        "description": "learning rate.",
        "defaultValue": 0.1,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "weight_decay",
        "displayName": "weight_decay",
        "description": "weight decay (L2 penalty).",
        "defaultValue": 0,
        "valueRange": [0, 0.1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
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
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "nesterov",
        "displayName": "nesterov",
        "description": "enables Nesterov momentum.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
]

SKLEARN_ML_SUPPORTED_PT_OPTIMIZER_PARAMETERS = [
    {"name": "Adadelta", "selected": False, "displayName": "Adadelta",
     "parameters": [obj for obj in PT_OPTIMIZER_Adadelta_PARAMETERS]},
    {"name": "Adagrad", "selected": False, "displayName": "Adagrad",
     "parameters": [obj for obj in PT_OPTIMIZER_Adagrad_PARAMETERS]},
    {"name": "Adam", "selected": False, "displayName": "Adam",
     "parameters": [obj for obj in PT_OPTIMIZER_Adam_PARAMETERS]},
    {"name": "AdamW", "selected": False, "displayName": "AdamW",
     "parameters": [obj for obj in PT_OPTIMIZER_AdamW_PARAMETERS]},
    {"name": "SparseAdam", "selected": False, "displayName": "SparseAdam",
     "parameters": [obj for obj in PT_OPTIMIZER_SparseAdam_PARAMETERS]},
    {"name": "Adamax", "selected": False, "displayName": "Adamax",
     "parameters": [obj for obj in PT_OPTIMIZER_Adamax_PARAMETERS]},
    {"name": "ASGD", "selected": False, "displayName": "ASGD",
     "parameters": [obj for obj in PT_OPTIMIZER_ASGD_PARAMETERS]},
    {"name": "LBFGS", "selected": False, "displayName": "LBFGS",
     "parameters": [obj for obj in PT_OPTIMIZER_LBFGS_PARAMETERS]},
    {"name": "RMSprop", "selected": False, "displayName": "RMSprop",
     "parameters": [obj for obj in PT_OPTIMIZER_RMSprop_PARAMETERS]},
    {"name": "Rprop", "selected": False, "displayName": "Rprop",
     "parameters": [obj for obj in PT_OPTIMIZER_Rprop_PARAMETERS]},
    {"name": "SGD", "selected": False, "displayName": "SGD", "parameters": [obj for obj in PT_OPTIMIZER_SGD_PARAMETERS]}
]

PT_LOSS_CrossEntropyLoss_PARAMETERS = [
    {
        "name": "weight",
        "displayName": "weight",
        "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
        "paramType": "tensor",
        "defaultValue": None,
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["tensor"],
        "allowedDataType": ["tensor"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
PT_LOSS_CTCLoss_PARAMETERS = [
    {
        "name": "blank",
        "displayName": "blank",
        "description": "blank label.",
        "defaultValue": 0,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "zero_infinity",
        "displayName": "zero_infinity",
        "description": "Whether to zero infinite losses and the associated gradients.",
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
    }
]
PT_LOSS_NLLLoss_PARAMETERS = [
    {
        "name": "weight",
        "displayName": "weight",
        "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
        "paramType": "tensor",
        "defaultValue": None,
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["tensor"],
        "allowedDataType": ["tensor"]
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
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
PT_LOSS_PoissonNLLLoss_PARAMETERS = [
    {
        "name": "log_input",
        "displayName": "log_input",
        "description": "if True the loss is computed as exp(input)-target*input.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "full",
        "displayName": "full",
        "description": "whether to compute full loss, i. e. to add the Stirling approximation term.",
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
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["bool"],
        "allowedDataType": ["bool"]
    },
    {
        "name": "eps",
        "displayName": "eps",
        "description": "small value to avoid evaluation of log(0) when log_input = False.",
        "defaultValue": 0.00000001,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
PT_LOSS_BCELoss_PARAMETERS = [
    {
        "name": "weight",
        "displayName": "weight",
        "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
        "paramType": "tensor",
        "defaultValue": None,
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["tensor"],
        "allowedDataType": ["tensor"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]
PT_LOSS_BCEWithLogitsLoss_PARAMETERS = [
    {
        "name": "weight",
        "displayName": "weight",
        "description": "a manual rescaling weight given to each class. If given, has to be a Tensor of size C.",
        "paramType": "tensor",
        "defaultValue": None,
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["tensor"],
        "allowedDataType": ["tensor"]
    },
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
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
        "expectedDataType": ["tensor"],
        "allowedDataType": ["tensor"]
    },
]
PT_LOSS_SoftMarginLoss_PARAMETERS = [
    {
        "name": "reduction",
        "displayName": "reduction",
        "description": "Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.",
        "defaultValue": "mean",
        "paramType": "list",
        "valueRange": ["none", "mean", "sum"],
        "uiElemType": "checkbox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    }
]

SKLEARN_ML_SUPPORTED_PT_LOSS_PARAMS = [
    {"name": "CrossEntropyLoss", "selected": False, "displayName": "CrossEntropyLoss",
     "parameters": [obj for obj in PT_LOSS_CrossEntropyLoss_PARAMETERS]},
    {"name": "CTCLoss", "selected": False, "displayName": "CTCLoss",
     "parameters": [obj for obj in PT_LOSS_CTCLoss_PARAMETERS]},
    {"name": "NLLLoss", "selected": False, "displayName": "NLLLoss",
     "parameters": [obj for obj in PT_LOSS_NLLLoss_PARAMETERS]},
    {"name": "PoissonNLLLoss", "selected": False, "displayName": "PoissonNLLLoss",
     "parameters": [obj for obj in PT_LOSS_PoissonNLLLoss_PARAMETERS]},
    {"name": "BCELoss", "selected": False, "displayName": "BCELoss",
     "parameters": [obj for obj in PT_LOSS_BCELoss_PARAMETERS]},
    {"name": "BCEWithLogitsLoss", "selected": False, "displayName": "BCEWithLogitsLoss",
     "parameters": [obj for obj in PT_LOSS_BCEWithLogitsLoss_PARAMETERS]},
    {"name": "SoftMarginLoss", "selected": False, "displayName": "SoftMarginLoss",
     "parameters": [obj for obj in PT_LOSS_SoftMarginLoss_PARAMETERS]}
]

SKLEARN_ML_SUPPORTED_PT_L1_REGULARIZER_PARAMETERS = [
    {
        "name": "l1_decay",
        "selected": False,
        "displayName": "l1_decay",
        "description": "l1 decay.",
        "defaultValue": 0.0,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]

    },
]

SKLEARN_ML_SUPPORTED_PT_L2_REGULARIZER_PARAMETERS = [
    {
        "name": "l2_decay",
        "selected": False,
        "displayName": "l2_decay",
        "description": "l2 dacay.",
        "defaultValue": 0.0,
        "valueRange": [0, 1],
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["float"],
        "allowedDataType": ["float"]
    },
]

SKLEARN_ML_SUPPORTED_PT_REGULARIZER_PARAMETERS = [
    {"name": "l1_regularizer", "selected": False, "displayName": "l1_regularizer",
     "parameters": [obj for obj in SKLEARN_ML_SUPPORTED_PT_L1_REGULARIZER_PARAMETERS]},
    {"name": "l2_regularizer", "selected": False, "displayName": "l2_regularizer",
     "parameters": [obj for obj in SKLEARN_ML_SUPPORTED_PT_L2_REGULARIZER_PARAMETERS]},
]

SKLEARN_ML_PYTORCH_CLASSIFICATION_PARAMS = [
    {
        "name": "layer",
        "displayName": "Layer",
        "description": "A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.",
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_PT_LAYER],
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "list",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": True,
        "expectedDataType": ["string"],
        "allowedDataType": ["string"]
    },
    {
        "name": "loss",
        "displayName": "Loss",
        "description": "The function used to evaluate the candidate solution (i.e. a set of weights).",
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_PT_LOSS_PARAMS],
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
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_PT_OPTIMIZER_PARAMETERS],
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
        "name": "regularizer",
        "displayName": "regularizer",
        "description": "Regularizer function.",
        "defaultValue": [obj for obj in SKLEARN_ML_SUPPORTED_PT_REGULARIZER_PARAMETERS],
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
        "acceptedValue": None,
        "valueRange": [0, 100],
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
        "acceptedValue": None,
        "valueRange": None,
        "paramType": "number",
        "uiElemType": "textBox",
        "display": True,
        "hyperpatameterTuningCandidate": False,
        "expectedDataType": ["int"],
        "allowedDataType": ["int"]
    }
]
