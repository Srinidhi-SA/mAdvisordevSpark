from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


def get_kernel_weights(kernel_weight_init, main_layer, input_units, output_units):
    if kernel_weight_init != None:
        layer_units_ip = input_units
        layer_units_op = output_units
        weights = main_layer.weight
        if kernel_weight_init["name"] == "Uniform":
            nn.init.uniform_(weights, a = kernel_weight_init["lower_bound"], b = kernel_weight_init["upper_bound"])
        if kernel_weight_init["name"] == "Normal":
            nn.init.normal_(weights, mean = kernel_weight_init["mean"], std = kernel_weight_init["std"])
        if kernel_weight_init["name"] == "Constant":
            nn.init.constant_(weights, val = kernel_weight_init["val"])
        if kernel_weight_init["name"] == "Ones":
            nn.init.ones_(weights)
        if kernel_weight_init["name"] == "Zeros":
            nn.init.zeros_(weights)
        if kernel_weight_init["name"] == "Eye":
            nn.init.eye_(weights)
        if kernel_weight_init["name"] == "Xavier_Uniform":
            nn.init.xavier_uniform_(weights, gain = nn.init.calculate_gain('relu'))
        if kernel_weight_init["name"] == "Xavier_Normal":
            nn.init.xavier_normal_(weights, gain = nn.init.calculate_gain('relu'))
        if kernel_weight_init["name"] == "Kaiming_Uniform":
            nn.init.kaiming_uniform_(weights, a = 0,mode = 'fan_in', nonlinearity = 'leaky_relu')
        if kernel_weight_init["name"] == "Kaiming_Normal":
            nn.init.kaiming_normal_(weights, a = 0,mode = 'fan_in',nonlinearity = 'leaky_relu')
        if kernel_weight_init["name"] == "Orthogonal":
            nn.init.orthogonal_(weights, gain = 4)
        if kernel_weight_init["name"] == "Sparse":
            nn.init.sparse_(weights, sparsity = kernel_weight_init["sparsity"], std = kernel_weight_init["std"])
        if kernel_weight_init["name"] == "Default":
            return weights
    else:
        pass


def get_kernel_bias(kernel_bias_init, main_layer, input_units, output_units):
    if kernel_bias_init != None:
        layer_units_ip = input_units
        layer_units_op = output_units
        bias = main_layer.bias
        if kernel_bias_init["name"] == "Uniform":
            nn.init.uniform_(bias, a = kernel_bias_init["lower_bound"], b = kernel_bias_init["upper_bound"])
        if kernel_bias_init["name"] == "Normal":
            nn.init.normal_(bias, mean = kernel_bias_init["mean"], std = kernel_bias_init["std"])
        if kernel_bias_init["name"] == "Constant":
            nn.init.constant_(bias, val = kernel_bias_init["val"])
        if kernel_bias_init["name"] == "Ones":
            nn.init.ones_(bias)
        if kernel_bias_init["name"] == "Zeros":
            nn.init.zeros_(bias)
        if kernel_bias_init["name"] == "Eye":
            nn.init.eye_(bias)
        if kernel_bias_init["name"] == "Default":
            return bias
        if kernel_bias_init["name"] == "Other":
            bias.data.zero_()
        # if kernel_bias_init["name"] == "Xavier_Uniform":
        #     bias.data.zero_()
        #     nn.init.xavier_uniform_(bias, gain = nn.init.calculate_gain('relu'))
        # if kernel_bias_init["name"] == "Xavier_Normal":
        #     bias.data.zero_()
        #     nn.init.xavier_normal_(bias, gain = nn.init.calculate_gain('relu'))
        # if kernel_bias_init["name"] == "Kaiming_Uniform":
        #     bias.data.zero_()
        #     nn.init.kaiming_uniform_(bias, a = 0, nonlinearity = 'leaky_relu')#mode = layer_units_ip)
        # if kernel_bias_init["name"] == "Kaiming_Normal":
        #     bias.data.zero_()
        #     nn.init.kaiming_normal_(bias, a = 0,nonlinearity = 'leaky_relu')#mode = layer_units_ip)
        # if kernel_bias_init["name"] == "Orthogonal":
        #     bias.data.zero_()
        #     nn.init.orthogonal_(bias, gain = 4)
        # if kernel_bias_init["name"] == "Sparse":
        #     bias.data.zero_()
        #     nn.init.sparse_(bias, sparsity = kernel_bias_init["sparsity"], std = kernel_bias_init["std"])
    else:
        pass

def get_kernel_weight_constraint(kernel_weight_constraint,main_layer):
    if(kernel_weight_constraint["constraint"] == True):
        weights = main_layer.weight
        new_weights = weights.clamp(kernel_weight_constraint["min"],kernel_weight_constraint["max"])
        main_layer.weight = torch.nn.Parameter(new_weights)

def get_layers_for_network_module(nnpt_params, task_type, first_layer_units):
    layers = []
    nnpt_params["hidden_layer_info"] =  {int(key): val for key, val in nnpt_params['hidden_layer_info'].items()}

    layers_list = sorted(tuple(nnpt_params["hidden_layer_info"]))

    print("="*45)
    print(nnpt_params)
    print("n_layers - ", len(layers_list))
    print("task_type - ", task_type)
    print("layers_tuple - ", layers_list)

    if task_type == "CLASSIFICATION":
        for val in layers_list:
            print(val)
            layer_dict = nnpt_params["hidden_layer_info"][val]
            layer_name = layer_dict["layer"]
            if val == 1:
                layer_units_ip = first_layer_units
            else:
                layer_units_ip = layer_dict["units_ip"]

            kernel_weight_init = layer_dict["weight_init"]
            kernel_bias_init = layer_dict["bias_init"]
            kernel_weight_constraint = layer_dict["weight_constraint"]
            layer_units_op = layer_dict["units_op"]
            #layer_bias = layer_dict["bias"]
            layer_activation = layer_dict["activation"]
            layer_batchnormalization = layer_dict["batchnormalization"]
            layer_dropout = layer_dict["dropout"]

            print("~"*50)
            print("Layer ID - ", val)
            print("Layer Name - ", layer_name)
            print("~"*50)

            if layer_name == "Linear":
                main_layer = nn.Linear(in_features = layer_units_ip, out_features = layer_units_op)
                get_kernel_weights(kernel_weight_init, main_layer,layer_units_ip,layer_units_op)
                get_kernel_bias(kernel_bias_init, main_layer,layer_units_ip,layer_units_op)
                get_kernel_weight_constraint(kernel_weight_constraint,main_layer)
                layers.append(main_layer)
                if layer_activation != None:
                    if layer_activation["name"] == "ELU":
                        activation = nn.ELU(alpha = layer_activation["alpha"], inplace = False)
                        layers.append(activation)
                    if layer_activation["name"] == "Hardshrink":
                        activation = nn.Hardshrink(lambd = layer_activation["lambd"])
                        layers.append(activation)
                    if layer_activation["name"] == "Hardtanh":
                        activation = nn.Hardtanh(min_val = layer_activation["min_val"], max_val = layer_activation["max_val"], inplace = False)
                        layers.append(activation)
                    if layer_activation["name"] == "LeakyReLU":
                        activation = nn.LeakyReLU(negative_slope = layer_activation["negative_slope"], inplace = False)
                        layers.append(activation)
                    if layer_activation["name"] == "LogSigmoid":
                        activation = nn.LogSigmoid()
                        layers.append(activation)
                    if layer_activation["name"] == "MultiheadAttention":
                        activation = nn.MultiheadAttention(
                        embed_dim = layer_activation["embed_dim"],
                        num_heads = layer_activation["num_heads"],
                        dropout = layer_activation["dropout"],
                        bias = layer_activation["bias"],
                        add_bias_kv = layer_activation["add_bias_kv"],
                        add_zero_attn = layer_activation["add_zero_attn"],
                        kdim = layer_activation["kdim"],
                        vdim = layer_activation["vdim"]
                        )
                        layers.append(activation)
                    if layer_activation["name"] == "PreLU":
                        activation = nn.PreLU(num_parameters = layer_activation["num_parameters"], init = layer_activation["init"])
                        layers.append(activation)
                    if layer_activation["name"] == "ReLU":
                        activation = nn.ReLU()
                        layers.append(activation)
                    if layer_activation["name"] == "ReLU6":
                        activation = nn.ReLU6()
                        layers.append(activation)
                    if layer_activation["name"] == "RreLU":
                        activation = nn.RreLU(lower = layer_activation["lower"], upper = layer_activation["upper"], inplace = False)
                        layers.append(activation)
                    if layer_activation["name"] == "SELU":
                        activation = nn.SELU()
                        layers.append(activation)
                    if layer_activation["name"] == "CELU":
                        activation = nn.CELU(alpha = layer_activation["alpha"], inplace = False)
                        layers.append(activation)
                    if layer_activation["name"] == "GELU":
                        activation = nn.GELU()
                        layers.append(activation)
                    if layer_activation["name"] == "Sigmoid":
                        activation = nn.Sigmoid()
                        layers.append(activation)
                    if layer_activation["name"] == "Softplus":
                        activation = nn.Softplus(beta = layer_activation["beta"], threshold = layer_activation["threshold"])
                        layers.append(activation)
                    if layer_activation["name"] == "Softshrink":
                        activation = nn.Softshrink(lambd = layer_activation["lambd"])
                        layers.append(activation)
                    if layer_activation["name"] == "Softsign":
                        activation = nn.Softsign()
                        layers.append(activation)
                    if layer_activation["name"] == "Tanh":
                        activation = nn.Tanh()
                        layers.append(activation)
                    if layer_activation["name"] == "Tanhshrink":
                        activation = nn.Tanhshrink()
                        layers.append(activation)
                    if layer_activation["name"] == "Threshold":
                        activation = nn.Threshold(threshold = layer_activation["threshold"], value = layer_activation["value"])
                        layers.append(activation)
                    if layer_activation["name"] == "Softmin":
                        activation = nn.Softmin(dim = layer_activation["dim"])
                        layers.append(activation)
                    if layer_activation["name"] == "Softmax":
                        activation = nn.Softmax(dim = layer_activation["dim"])
                        layers.append(activation)
                    if layer_activation["name"] == "Softmax2d":
                        activation = nn.Softmax2d()
                        layers.append(activation)
                    if layer_activation["name"] == "LogSoftmax":
                        activation = nn.LogSoftmax(dim = layer_activation["dim"])
                        layers.append(activation)
                    if layer_activation["name"] == "AdaptiveLogSoftmaxWithLoss":
                        activation = nn.AdaptiveLogSoftmaxWithLoss(n_classes = layer_activation["n_classes"], cutoffs = layer_activation["cutoffs"], div_value = layer_activation["div_value"], head_bias = layer_activation["head_bias"])
                        layers.append(activation)
                else:
                    pass

                if layer_batchnormalization != None:
                    if layer_batchnormalization["name"] == "BatchNorm1d":
                        batch_normalization = nn.BatchNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "BatchNorm2d":
                        batch_normalization = nn.BatchNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "BatchNorm3d":
                        batch_normalization = nn.BatchNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "SyncBatchNorm":
                        batch_normalization = nn.SyncBatchNorm(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"], process_group = layer_batchnormalization["process_group"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "InstanceNorm1d":
                        batch_normalization = nn.InstanceNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "InstanceNorm2d":
                        batch_normalization = nn.InstanceNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "InstanceNorm3d":
                        batch_normalization = nn.InstanceNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "GroupNorm":
                        batch_normalization = nn.GroupNorm(num_groups = layer_batchnormalization["num_groups"], num_channels = layer_batchnormalization["num_channels"], eps = layer_batchnormalization["eps"], affine = layer_batchnormalization["affine"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "LayerNorm":
                        batch_normalization = nn.LayerNorm(normalized_shape = layer_batchnormalization["normalized_shape"], eps = layer_batchnormalization["eps"], elementwise_affine = layer_batchnormalization["elementwise_affine"])
                        layers.append(batch_normalization)
                    if layer_batchnormalization["name"] == "LocalResponseNorm":
                        batch_normalization = nn.LocalResponseNorm(size = layer_batchnormalization["size"], alpha = layer_batchnormalization["alpha"], beta = layer_batchnormalization["beta"], k = layer_batchnormalization["k"])
                        layers.append(batch_normalization)
                else:
                    pass

                if layer_dropout != None:
                    if layer_dropout["name"] == "Dropout":
                        dropout = nn.Dropout(p = layer_dropout["p"], inplace = False)
                        layers.append(dropout)
                    if layer_dropout["name"] == "Dropout2d":
                        dropout = nn.Dropout2d(p = layer_dropout["p"], inplace = False)
                        layers.append(dropout)
                    if layer_dropout["name"] == "Dropout3d":
                        dropout = nn.Dropout3d(p = layer_dropout["p"], inplace = False)
                        layers.append(dropout)
                    if layer_dropout["name"] == "AlphaDropout":
                        dropout = nn.AlphaDropout(p = layer_dropout["p"], inplace = False)
                        layers.append(dropout)
                else:
                    pass

        print("~"*50)
        print("FINAL LAYERS FOR NETWORK - ", layers)
        print("~"*50)

    if task_type == "REGRESSION":
        for val in layers_list:
            layer_dict = nnpt_params["hidden_layer_info"][val]
            layer_name = layer_dict["layer"]
            if val == 1:
                layer_units_ip = first_layer_units
            else:
                layer_units_ip = layer_dict["units_ip"]
            layer_units_op = layer_dict["units_op"]
            layer_bias = layer_dict["bias"]
            layer_activation = layer_dict["activation"]
            layer_batchnormalization = layer_dict["batchnormalization"]
            layer_dropout = layer_dict["dropout"]

            print("~"*50)
            print("Layer ID - ", val)
            print("Layer Name - ", layer_name)
            print("~"*50)

            if layer_name == "Linear":
                main_layer = nn.Linear(in_features = layer_units_ip, out_features = layer_units_op, bias = layer_bias)
                layers.append(main_layer)
                if layer_activation != None:
                    if layer_activation["name"] == "ELU":
                        activation = nn.ELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "Hardshrink":
                        activation = nn.Hardshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Hardtanh":
                        activation = nn.Hardtanh(min_val = layer_activation["min_val"], max_val = layer_activation["max_val"], inplace = False)
                    if layer_activation["name"] == "LeakyReLU":
                        activation = nn.LeakyReLU(negative_slope = layer_activation["negative_slope"], inplace = False)
                    if layer_activation["name"] == "LogSigmoid":
                        activation = nn.LogSigmoid()
                    if layer_activation["name"] == "MultiheadAttention":
                        activation = nn.MultiheadAttention(
                        embed_dim = layer_activation["embed_dim"],
                        num_heads = layer_activation["num_heads"],
                        dropout = layer_activation["dropout"],
                        bias = layer_activation["bias"],
                        add_bias_kv = layer_activation["add_bias_kv"],
                        add_zero_attn = layer_activation["add_zero_attn"],
                        kdim = layer_activation["kdim"],
                        vdim = layer_activation["vdim"]
                        )
                    if layer_activation["name"] == "PreLU":
                        activation = nn.PreLU(num_parameters = layer_activation["num_parameters"], init = layer_activation["init"])
                    if layer_activation["name"] == "ReLU":
                        activation = nn.ReLU()
                    if layer_activation["name"] == "ReLU6":
                        activation = nn.ReLU6()
                    if layer_activation["name"] == "RreLU":
                        activation = nn.RreLU(lower = layer_activation["lower"], upper = layer_activation["upper"], inplace = False)
                    if layer_activation["name"] == "SELU":
                        activation = nn.SELU()
                    if layer_activation["name"] == "CELU":
                        activation = nn.CELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "GELU":
                        activation = nn.GELU()
                    if layer_activation["name"] == "Sigmoid":
                        activation = nn.Sigmoid()
                    if layer_activation["name"] == "Softplus":
                        activation = nn.Softplus(beta = layer_activation["beta"], threshold = layer_activation["threshold"])
                    if layer_activation["name"] == "Softshrink":
                        activation = nn.Softshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Softsign":
                        activation = nn.Softsign()
                    if layer_activation["name"] == "Tanh":
                        activation = nn.Tanh()
                    if layer_activation["name"] == "Tanhshrink":
                        activation = nn.Tanhshrink()
                    if layer_activation["name"] == "Threshold":
                        activation = nn.Threshold(threshold = layer_activation["threshold"], value = layer_activation["value"])
                    if layer_activation["name"] == "Softmin":
                        activation = nn.Softmin(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax":
                        activation = nn.Softmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax2d":
                        activation = nn.Softmax2d()
                    if layer_activation["name"] == "LogSoftmax":
                        activation = nn.LogSoftmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "AdaptiveLogSoftmaxWithLoss":
                        activation = nn.AdaptiveLogSoftmaxWithLoss(n_classes = layer_activation["n_classes"], cutoffs = layer_activation["cutoffs"], div_value = layer_activation["div_value"], head_bias = layer_activation["head_bias"])

                    layers.append(activation)
                else:
                    pass

                if layer_batchnormalization != None:
                    if layer_batchnormalization["name"] == "BatchNorm1d":
                        batch_normalization = nn.BatchNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm2d":
                        batch_normalization = nn.BatchNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm3d":
                        batch_normalization = nn.BatchNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "SyncBatchNorm":
                        batch_normalization = nn.SyncBatchNorm(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"], process_group = layer_batchnormalization["process_group"])
                    if layer_batchnormalization["name"] == "InstanceNorm1d":
                        batch_normalization = nn.InstanceNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm2d":
                        batch_normalization = nn.InstanceNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm3d":
                        batch_normalization = nn.InstanceNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "GroupNorm":
                        batch_normalization = nn.GroupNorm(num_groups = layer_batchnormalization["num_groups"], num_channels = layer_batchnormalization["num_channels"], eps = layer_batchnormalization["eps"], affine = layer_batchnormalization["affine"])
                    if layer_batchnormalization["name"] == "LayerNorm":
                        batch_normalization = nn.LayerNorm(normalized_shape = layer_batchnormalization["normalized_shape"], eps = layer_batchnormalization["eps"], elementwise_affine = layer_batchnormalization["elementwise_affine"])
                    if layer_batchnormalization["name"] == "LocalResponseNorm":
                        batch_normalization = nn.LocalResponseNorm(size = layer_batchnormalization["size"], alpha = layer_batchnormalization["alpha"], beta = layer_batchnormalization["beta"], k = layer_batchnormalization["k"])

                    layers.append(batch_normalization)
                else:
                    pass

                if layer_dropout != None:
                    if layer_dropout["name"] == "Dropout":
                        dropout = nn.Dropout(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout2d":
                        dropout = nn.Dropout2d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout3d":
                        dropout = nn.Dropout3d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "AlphaDropout":
                        dropout = nn.AlphaDropout(p = layer_dropout["p"], inplace = False)

                    layers.append(dropout)
                else:
                    pass

    return layers

def get_other_pytorch_params(nnpt_params, task_type, network_params):
    loss_criterion_dict = nnpt_params["loss"]
    loss_name = loss_criterion_dict["loss"]
    optimizer_dict = nnpt_params["optimizer"]
    #optimizer_name = optimizer_dict["optimizer"]
    regularizer = nnpt_params["regularizer"]
    batch_size = nnpt_params["batch_size"]
    number_of_epochs = nnpt_params["number_of_epochs"]

    loss_criterion = get_loss_criterion(loss_name, loss_criterion_dict)
    #optimizer = get_optimizer(optimizer_name, optimizer_dict, network_params)
    other_params_dict = {}
    other_params_dict["loss_name"] = loss_criterion_dict["loss"]
    other_params_dict["number_of_epochs"] = number_of_epochs
    other_params_dict["batch_size"] = batch_size
    other_params_dict["loss_criterion"] = loss_criterion
    other_params_dict["optimizer"] = optimizer_dict
    other_params_dict["regularizer"] = regularizer
    other_params_dict["reduction"] = nnpt_params["loss"]["reduction"]

    if "weight" in loss_criterion_dict:
        other_params_dict["loss_weight"] = nnpt_params["loss"]["weight"]

    return other_params_dict

def get_loss_criterion(loss_name, loss_criterion_dict):
    if loss_name == "CrossEntropyLoss":
        loss_criterion = nn.CrossEntropyLoss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "L1Loss":
        loss_criterion = nn.L1Loss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "MSELoss":
        loss_criterion = nn.MSELoss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "CTCLoss":
        loss_criterion = nn.CTCLoss(reduction = loss_criterion_dict["reduction"], blank = loss_criterion_dict["blank"], zero_infinity = loss_criterion_dict["zero_infinity"])
    if loss_name == "NLLLoss":
        loss_criterion = nn.NLLLoss(reduction = loss_criterion_dict["reduction"], weight = None)
    if loss_name == "PoissonNLLLoss":
        loss_criterion = nn.PoissonNLLLoss(reduction = loss_criterion_dict["reduction"], log_input = loss_criterion_dict["log_input"], full = loss_criterion_dict["full"], eps = loss_criterion_dict["eps"])
    if loss_name == "KLDivLoss":
        loss_criterion = nn.KLDivLoss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "BCELoss":
        loss_criterion = nn.BCELoss(reduction = loss_criterion_dict["reduction"], weight = None)
    if loss_name == "BCEWithLogitsLoss":
        loss_criterion = nn.BCEWithLogitsLoss(reduction = loss_criterion_dict["reduction"], weight = None , pos_weight = None)
    if loss_name == "SoftMarginLoss":
        loss_criterion = nn.SoftMarginLoss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "None":
        pass
    return loss_criterion


def get_optimizer(optimizer_name, optimizer_dict, network_params):
    if optimizer_name == "Adadelta":
        optimizer = optim.Adadelta(network_params, weight_decay = optimizer_dict["weight_decay"], rho = optimizer_dict["rho"], eps = optimizer_dict["eps"], lr = optimizer_dict["lr"])
    if optimizer_name == "Adagrad":
        optimizer = optim.Adagrad(network_params, weight_decay = optimizer_dict["weight_decay"], lr_decay = optimizer_dict["lr_decay"], eps = optimizer_dict["eps"], lr = optimizer_dict["lr"])
    if optimizer_name == "Adam":
        optimizer = optim.Adam(network_params, weight_decay = optimizer_dict["weight_decay"], betas = eval(optimizer_dict["betas"]), eps = optimizer_dict["eps"], lr = optimizer_dict["lr"], amsgrad = optimizer_dict["amsgrad"])
    if optimizer_name == "AdamW":
        optimizer = optim.AdamW(network_params, weight_decay = optimizer_dict["weight_decay"], betas = eval(optimizer_dict["betas"]), eps = optimizer_dict["eps"], lr = optimizer_dict["lr"], amsgrad = optimizer_dict["amsgrad"])
    if optimizer_name == "SparseAdam":
        optimizer = optim.SparseAdam(network_params, betas = eval(optimizer_dict["betas"]), eps = optimizer_dict["eps"], lr = optimizer_dict["lr"])
    if optimizer_name == "Adamax":
        optimizer = optim.Adamax(network_params, betas = eval(optimizer_dict["betas"]), eps = optimizer_dict["eps"], lr = optimizer_dict["lr"], weight_decay = optimizer_dict["weight_decay"])
    if optimizer_name == "ASGD":
        optimizer = optim.ASGD(network_params, lr = optimizer_dict["lr"], lambd = optimizer_dict["lambd"], alpha = optimizer_dict["alpha"], t0 = optimizer_dict["t0"], weight_decay = optimizer_dict["weight_decay"])
    if optimizer_name == "LBFGS":
        optimizer = optim.LBFGS(network_params, lr = optimizer_dict["lr"], max_iter = optimizer_dict["max_iter"], max_eval = optimizer_dict["max_eval"], tolerance_grad = optimizer_dict["tolerance_grad"], tolerance_change = optimizer_dict["tolerance_change"], history_size = optimizer_dict["history_size"], line_search_fn = optimizer_dict["line_search_fn"])
    if optimizer_name == "RMSprop":
        optimizer = optim.RMSprop(network_params, weight_decay = optimizer_dict["weight_decay"], lr = optimizer_dict["lr"], momentum = optimizer_dict["momentum"], alpha = optimizer_dict["alpha"], eps = optimizer_dict["eps"], centered = optimizer_dict["centered"])
    if optimizer_name == "Rprop":
        optimizer = optim.Rprop(network_params, lr = optimizer_dict["lr"], eta = optimizer_dict["eta"], step_sizes = optimizer_dict["step_sizes"])
    if optimizer_name == "SGD":
        optimizer = optim.SGD(network_params, weight_decay = optimizer_dict["weight_decay"], momentum = optimizer_dict["momentum"], dampening = optimizer_dict["dampening"], lr = optimizer_dict["lr"], nesterov = optimizer_dict["nesterov"])
    if optimizer_name == None:
        optimizer = None

    return optimizer


def get_tensored_data(x_train, y_train, x_test, y_test):
    x_train = np.stack([x_train[col].values for col in x_train.columns], 1)
    x_train_tensored = torch.tensor(x_train, dtype=torch.float)

    # y_train = np.stack([y_train[col].values for col in y_train.columns], 1)
    y_train_tensored = torch.tensor(y_train, dtype=torch.float)

    x_test = np.stack([x_test[col].values for col in x_test.columns], 1)
    x_test_tensored = torch.tensor(x_test, dtype=torch.float)

    # y_test = np.stack([y_test[col].values for col in y_test.columns], 1)
    try:
        y_test_tensored = torch.tensor(y_test, dtype=torch.float)
    except:
        y_test_tensored = torch.tensor(y_test.values, dtype=torch.float)

    return x_train_tensored, y_train_tensored, x_test_tensored, y_test_tensored

def get_nnptc_params_dict(levels,columns,rows):
    large = False
    if columns > 35 :
        large = True
        nnptc_params = {
            "hidden_layer_info": {
              "1": {
                "weight_constraint": {
                  "constraint": "None"
                },
                "units_op": 16,
                "units_ip": 32,
                "activation": {
                  "name": "ReLU"
                },
                "bias_init": {
                  "name": "Uniform",
                  "lower_bound": 0,
                  "upper_bound": 1
                },
                "weight_init": {
                  "name": "Kaiming_Normal",
                  "mode": "fan_in",
                  "nonlinearity": "leaky_relu",
                  "a": 0
                },
                "layer": "Linear",
                "dropout": {
                  "name": "Dropout",
                  "p": 0.5
                },
                "batchnormalization": {
                  "name": "None"
                }
              },
              "2": {
                "weight_constraint": {
                  "constraint": "None"
                },
                "units_op": 8,
                "units_ip": 16,
                "activation": {
                  "name": "ReLU"
                },
                "bias_init": {
                  "name": "Uniform",
                  "lower_bound": 0,
                  "upper_bound": 1
                },
                "weight_init": {
                  "name": "Kaiming_Normal",
                  "mode": "fan_in",
                  "nonlinearity": "leaky_relu",
                  "a": 0
                },
                "layer": "Linear",
                "dropout": {
                  "name": "Dropout",
                  "p": 0.5
                },
                "batchnormalization": {
                  "name": "None"
                }
              },
              "3": {
                "weight_constraint": {
                  "constraint": "None"
                },
                "units_op": 2,
                "units_ip": 8,
                "activation": {
                  "name": "Sigmoid"
                },
                "bias_init": {
                  "name": "Uniform",
                  "lower_bound": 0,
                  "upper_bound": 1
                },
                "weight_init": {
                  "name": "Kaiming_Normal",
                  "mode": "fan_in",
                  "nonlinearity": "leaky_relu",
                  "a": 0
                },
                "layer": "Linear",
                "dropout": {
                  "name": "None",
                  "p": "None"
                },
                "batchnormalization": {
                  "name": "None"
                }
              }
            },
            "number_of_epochs": 50,
            "loss": {
              "ignore_index": None,
              "loss": "CrossEntropyLoss",
              "weight": None,
              "reduction": "mean"
            },
            "optimizer": {
              "lr": 0.001,
              "weight_decay": 0,
              "betas": "(0.9,0.999)",
              "amsgrad": "False",
              "optimizer": "Adam",
              "eps": 1e-08
            },
            "regularizer": {
              "regularizer": "l2_regularizer",
              "l2_decay": 0
            },
            "batch_size": 32
          }
    else:
        nnptc_params = {
            "hidden_layer_info": {
              "1": {
                "weight_constraint": {
                  "constraint": "None"
                },
                "units_op": 8,
                "units_ip": 16,
                "activation": {
                  "name": "ReLU"
                },
                "bias_init": {
                  "name": "Normal",
                  "std": 1,
                  "mean": 0
                },
                "weight_init": {
                  "name": "Kaiming_Normal",
                  "mode": "fan_in",
                  "nonlinearity": "leaky_relu",
                  "a": 0
                },
                "layer": "Linear",
                "dropout": {
                  "name": "Dropout",
                  "p": 0.2
                },
                "batchnormalization": {
                  "name": "None"
                }
              },
              "2": {
                "weight_constraint": {
                  "constraint": "None"
                },
                "units_op": 2,
                "units_ip": 8,
                "activation": {
                  "name": "Sigmoid"
                },
                "bias_init": {
                  "name": "Uniform",
                  "lower_bound": 0,
                  "upper_bound": 1
                },
                "weight_init": {
                  "name": "Uniform",
                  "lower_bound": 0,
                  "upper_bound": 1
                },
                "layer": "Linear",
                "dropout": {
                  "name": "None",
                  "p": "None"
                },
                "batchnormalization": {
                  "name": "None"
                }
              }
            },
            "number_of_epochs": 50,
            "loss": {
              "ignore_index": None,
              "loss": "CrossEntropyLoss",
              "weight": None,
              "reduction": "mean"
            },
            "optimizer": {
              "lr": 0.001,
              "weight_decay": 0,
              "betas": "(0.9,0.999)",
              "amsgrad": "False",
              "optimizer": "Adam",
              "eps": 1e-08
            },
            "regularizer": {
              "regularizer": "l2_regularizer",
              "l2_decay": 0
            },
            "batch_size": 32
          }
    if not large:
        if rows > 10000:
            nnptc_params["batch_size"] = 64
            nnptc_params["number_of_epochs"] = 250
        if columns < nnptc_params["hidden_layer_info"]["1"]["units_op"]:
            nnptc_params["hidden_layer_info"]["1"]["units_op"] = 4
            nnptc_params["hidden_layer_info"]["2"]["units_ip"] = 4
        nnptc_params["hidden_layer_info"]["2"]["units_op"] = len(levels)
    else:
        if rows > 10000:
            nnptc_params["batch_size"] = 64
            nnptc_params["number_of_epochs"] = 100
        nnptc_params["hidden_layer_info"]["3"]["units_op"] = len(levels)
    if len(levels) > 2:
        if not large:
            nnptc_params["hidden_layer_info"]["2"]["activation"]["name"] = "Softmax"
            nnptc_params["hidden_layer_info"]["2"]["activation"]["dim"] = None
        else:
            nnptc_params["hidden_layer_info"]["3"]["activation"]["name"] = "Softmax"
            nnptc_params["hidden_layer_info"]["3"]["activation"]["dim"] = None
    else:
        if not large:
            nnptc_params["hidden_layer_info"]["2"]["activation"]["name"] = "Sigmoid"
        else:
            nnptc_params["hidden_layer_info"]["3"]["activation"]["name"] = "Sigmoid"
    return nnptc_params
