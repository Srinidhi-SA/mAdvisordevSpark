'''
This file contains STATIC content required by UI:
    - Data Cleansing Page
    - Feature Engineering Page

This content will be provided on an API call.
API: /api/feature_engineering_static_content/?q='data_cleaning_static'
API: /api/feature_engineering_static_content/?q='feature_engineering_static'
'''

'''
Data cleansing
1 . data_cleansing_static is for UI to fill dropdown
2 . column_format for a statndard column format for both missing_value_removal and outlier_removal
3 . At-End config for data cleansing for ML scripts to be send with configs.
'''

data_cleansing_static = {
    "top_level_options": [
        {
            'name': 'duplicate_column',
              'displayName': 'Do you want to remove duplicate attributes/columns in the dataset?',
              'selected': True,
              'slug': 'vjYloNUHxUqjPFTC9Oc8nm'
        },
        {
            'name': 'duplicate_row',
            'displayName': 'Do you want to remove duplicate observations  in the dataset?',
            'selected': True,
            'slug': '4e0mzsNOeiVG4SzRFu1mpp'
        }
    ],
    "measure": {
        "convertable_to": [
            {
                'displayName': 'Dimension',
                'name': 'dimension',
                'selected': False,
                'slug': 'rJlHUrcdiV0ZDP2euvoo1t'
            },
            {
                'displayName': 'Time Dimension',
                'name': 'time_dimension',
                'selected': False,
                'slug': 'uxfslIVAxDqKWp1CPmqhtx'
            }
        ],
        "missing_value_treatment": {
            "name": "missings_value_treatment",
            "displayName": "Missing value treatment",
            "selected": False,
            "operations": [
    {
        'columns': [],
        'displayName': 'Mean Imputation',
        'name': 'mean_imputation',
        'selected': False,
        'slug': 'MT0cf0H3rNXyaVhXHtiP43'},
    {   'columns': [],
        'displayName': 'Mode Imputation',
        'name': 'mode_imputation',
        'selected': False,
        'slug': 'mZbFlJkOkeKsneDHDqNIXE'},
    {   'columns': [],
        'displayName': 'Median Imputation',
        'name': 'median_imputation',
        'selected': False,
        'slug': 'ToO7vD2uKTyHMBjLs26dgU'},
    # {   'columns': [],
    #     'displayName': 'Remove Observations',
    #     'name': 'remove_observations',
    #     'selected': False,
    #     'slug': 'N7QJ2V82cSwfXS8ix5HPLq'},
    {   'columns': [],
        'displayName': 'None',
        'name': 'none',
        'selected': False,
        'slug': 'H3uY15p2TmHZ4KWXWfZGUq'}
            ],
        },
        "outlier_removal": {
            "name": "outlier_treatment",
            "displayName": "Outlier Treatment",
            "selected": False,
            "operations": [
        #         {   'columns': [],
        # 'displayName': 'Remove Outliers',
        # 'name': 'remove_outliers',
        # 'selected': False,
        # 'slug': 'J47WSI7DgZDxE4ROTBNahp'},
{   'columns': [],
        'displayName': 'Cap Outliers',
        'name': 'cap_outliers',
        'selected': False,
        'slug': 'J47WSI7DgZDx4ROTBNahp'},
    {   'columns': [],
        'displayName': 'Replace with Mean',
        'name': 'replace_with_mean',
        'selected': False,
        'slug': 'RMN20VRhZBrIoI3M41UF8D'},
    {   'columns': [],
        'displayName': 'Replace with Median',
        'name': 'replace_with_median',
        'selected': False,
        'slug': '2MWuRulQahdbkD66y3R0b0'},
      # {'columns': [],
      #  'displayName': 'Remove Observations',
      #  'name': 'remove_observations',
      #  'selected': False,
      #  'slug': 'N7QJ2V82cSwfXS8ix5HPLq'},
    {   'columns': [],
        'displayName': 'None',
        'name': 'none',
        'selected': False,
        'slug': 'pSUkr21TwfCzZCdbFbqIEj'},

      ]
        },
    },
    "dimension": {
        "convertable_to": [   {   'displayName': 'Measure',
        'name': 'measure',
        'selected': False,
        'slug': '4CFhdtdy3vq3Bjo6VPAY8l'},
    {   'displayName': 'Time Dimension',
        'name': 'time_dimension',
        'selected': False,
        'slug': 'f2LKc09bDRU0VVfUFAAUfu'}],
        "missing_value_treatment": {
            "name": "missings_value_treatment",
            "displayName": "Missing value treatment",
            "selected": False,
            "operations": [
    {   'columns': [],
        'displayName': 'Mode imputation',
        'name': 'mode_imputation',
        'selected': False,
        'slug': 'O97RZsAI3XXvcWWAbWXTJE'},
    # {   'columns': [],
    #     'displayName': 'Logistic regression imputation',
    #     'name': 'logistic_regression_imputation',
    #     'selected': False,
    #     'slug': 'phPtnl4Dt6Dcdy5erCINXI'},
    # {   'columns': [],
    #     'displayName': 'Discriminant analysis imputation',
    #     'name': 'discriminant_analysis_imputation',
    #     'selected': False,
    #     'slug': 'tbeVfqh4GYxoSivkKiTMoy'},
    # {   'columns': [],
    #     'displayName': 'KNN imputation',
    #     'name': 'knn_imputation',
    #     'selected': False,
    #     'slug': 'x5FU8rJgsgrJDNPsZUaQ7F'},
    # {
    #         'columns': [],
    #     'displayName': 'Remove Observations',
    #     'name': 'remove_observations',
    #     'selected': False,
    #     'slug': 'N7QJ2V82cSwfXS8ix5HPLq'
    #     },
    {   'columns': [],
        'displayName': 'None',
        'name': 'none',
        'selected': False,
        'slug': 'H3uY15p2TmHZ4KWXWfZGUq'},
    ],
        },

    },
    "time_dimension": {
        "convertable_to": [   {   'displayName': 'Measure',
        'name': 'measure',
        'selected': False,
        'slug': 'bsx3SoD7BFVdRaUhry3msx'},
    {   'displayName': 'Dimension',
        'name': 'dimension',
        'selected': False,
        'slug': '2GzOxpDE2COXhwkXoGxUev'}],
        "missing_value_treatment": {
            "name": "missings_value_treatment",
            "displayName": "Missing value treatment",
            "selected": False,
            "operations": [   {   'columns': [],
        'displayName': 'Replace with average based on time dimension '
                       '(year/month/day)',
        'name': 'replace with average based on time dimension (year/month/day)',
        'selected': False,
        'slug': 'cxVbEdsK8DpHBEmcZ5XV1a'},
    {   'columns': [],
        'displayName': 'Remove observations',
        'name': 'remove observations',
        'selected': False,
        'slug': 'IsH922G642Rv9uyYseDw0F'},
    {   'columns': [],
        'displayName': 'None',
        'name': 'none',
        'selected': False,
        'slug': 'H3uY15p2TmHZ4KWXWfZGUq'}]
        }
    }
}

column_format = {
                    "name": "quantity",
                    "datatype": "measure",
                    "slug": "",
                    "mvt_value": 0,
                    "ol_lower_range": 0,
                    "ol_upper_range": 0,
                    "ol_lower_value": 0,
                    "ol_upper_value": 0
                }

overall_settings_data_cleasing_ui_ml_mapping = {
    'remove_duplicate_observations': 'duplicate_row',
    'remove_duplicate_attributes': 'duplicate_column'
}

data_cleansing_final_config_format = {
      "name": "data_cleansing",
      "displayName": "Data Cleansing",
      "selected": False,
      "slug": "",
      "overall_settings": [
        {
            'name': 'duplicate_column',
              'displayName': 'Do you want to remove duplicate attributes/columns in the dataset?',
              'selected': False,
              'slug': 'vjYloNUHxUqjPFTC9Oc8nm'
        },
        {
            'name': 'duplicate_row',
            'displayName': 'Do you want to remove duplicate observations  in the dataset?',
            'selected': False,
            'slug': '4e0mzsNOeiVG4SzRFu1mpp'
        }
        ],
      "columns_wise_settings": {
        "missing_value_treatment": {
          "name": "missing_value_treatment",
          "displayName": "Missing value treatment",
          "selected": True,
          "operations": [
  {
    'columns': [

    ],
    'displayName': 'Mean Imputation',
    'name': 'mean_imputation',
    'selected': False,
    'slug': 'MT0cf0H3rNXyaVhXHtiP43'
  },
  {
    'columns': [

    ],
    'displayName': 'Mode Imputation',
    'name': 'mode_imputation',
    'selected': False,
    'slug': 'mZbFlJkOkeKsneDHDqNIXE'
  },
  {
    'columns': [

    ],
    'displayName': 'Median Imputation',
    'name': 'median_imputation',
    'selected': False,
    'slug': 'ToO7vD2uKTyHMBjLs26dgU'
  },
  {
    'columns': [

    ],
    'displayName': 'Backward Filling',
    'name': 'backward_filling',
    'selected': False,
    'slug': 'cFruIkyFXLbarvFeObC1Rx'
  },
  {
    'columns': [

    ],
    'displayName': 'Forward Filling',
    'name': 'forward_filling',
    'selected': False,
    'slug': 'zu5VKiX2n5MqEP0jge9TSJ'
  },
  {
    'columns': [

    ],
    'displayName': 'Regression Imputation',
    'name': 'regression_imputation',
    'selected': False,
    'slug': 'cpDLZigzHSekw7y90kioQn'
  },
  {
    'columns': [

    ],
    'displayName': 'Stocastic Imputation',
    'name': 'stocastic_imputation',
    'selected': False,
    'slug': 'Tm4E16v15xUF7BZznuYpOs'
  },
  # {
  #   'columns': [
  #
  #   ],
  #   'displayName': 'Remove Observations',
  #   'name': 'remove_observations',
  #   'selected': False,
  #   'slug': 'N7QJ2V82cSwfXS8ix5HPLq'
  # },
  {
    'columns': [

    ],
    'displayName': 'Logistic regression imputation',
    'name': 'logistic_regression_imputation',
    'selected': False,
    'slug': 'phPtnl4Dt6Dcdy5erCINXI'
  },
  {
    'columns': [

    ],
    'displayName': 'Discriminant analysis imputation',
    'name': 'discriminant_analysis_imputation',
    'selected': False,
    'slug': 'tbeVfqh4GYxoSivkKiTMoy'
  },
  {
    'columns': [

    ],
    'displayName': 'KNN imputation',
    'name': 'knn_imputation',
    'selected': False,
    'slug': 'x5FU8rJgsgrJDNPsZUaQ7F'
  },
  {
    'columns': [

    ],
    'displayName': 'None',
    'name': 'none',
    'selected': False,
    'slug': 'ggususBEm6Uhj7zDMKGUrN'
  }
]
        },
        "outlier_removal": {
          "name": "outlier_treatment",
          "displayName": "Outlier treatment",
          "selected": True,
          "operations": [
        #       {   'columns': [],
        # 'displayName': 'Remove Outliers',
        # 'name': 'remove_outliers',
        # 'selected': False,
        # 'slug': 'J47WSI7DgZDxE4ROTBNahp'},
{   'columns': [],
        'displayName': 'Cap Outliers',
        'name': 'cap_outliers',
        'selected': False,
        'slug': 'J47WSI7DgZDx4ROTBNahp'},
    {   'columns': [],
        'displayName': 'Replace with Mean',
        'name': 'replace_with_mean',
        'selected': False,
        'slug': 'RMN20VRhZBrIoI3M41UF8D'},
    {   'columns': [],
        'displayName': 'Replace with Median',
        'name': 'replace_with_median',
        'selected': False,
        'slug': '2MWuRulQahdbkD66y3R0b0'},
    ]
        }
      }
    }


bin_conf = {
    'column_name': "",
    'type_of_binning': [
        {
            "name": "equal_sized_bin",
            "display name": "Equal sized bin"
        },
        {
            "name": "custom_bins",
            "display name": "Custom bins"
        },
    ],
    'number_of_bins': 2,
    'specify_interval': [],
    'new_column_name': ""
}

level_conf = {
    "column_name": "",
    "drop_down_values": [],
    "type": ""
}

replace_values_where_quantity = {
    "name": "replace_values_where_quantity",
    "displayName": "Replace values where quantity is",
    "range": {
        "lower": {
            'value': None,
            'default_value': 1
        },
        "upper": {
            "value": None,
            "deafult_value": 2
        }
    },
    "valid_range": {
        "lower": None,
        "upper": None
    },
    "replace_with" : [
        {
            "name": "mean",
            "displayName": "Mean",
            "value": None
        },
        {
            "name": "median",
            "displayName": "Median",
            "value": None
        },
    ]
}

sum_operation = {
    'name': 'sum_operations',
    "displayName": 'Add specific value',
    "value": 1,
    "default_value": 1,
    "status": True
}

subtract_operation = {
    'name': 'subtract_operations',
    "displayName": 'Subtract specific value',
    "value": 1,
    "default_value": 1,
    "status": True
}

multiply_operation = {
    'name': 'multiply_operations',
    "displayName": 'Multiply specific value',
    "value": 1,
    "default_value": 1,
    "status": True
}

division_operation = {
    'name': 'division_operation',
    "displayName": 'Division specific value',
    "value": 1,
    "default_value": 1,
    "status": True
}

perform_standardization = [
    {
        'name': 'min-max scaling',
        'displayName': 'Min Max Scaling'
    },

]

transform_variable_using = [
    {
        'name': 'log-transformtion',
        'displayName': 'Log transformation'
    },
]

convert_values_into_columns = [
    {
        'name': 'one_hot_encoding',
        'displayName': 'One Hot Encoding',
        'status': True
    }
]

is_date_weekend = {
    'name': 'is_date_weekend',
    'displayName': 'Is date a weekend?',
    'status': True
}

extarct_time_based_feature = [
    {
        'name': 'day_of_week',
        'displayName': 'Day of week',
    },
    {
        'name': 'part_of_month',
        'displayName': 'Part of Month'
    }
]

time_since_specific_date = {
    'name': 'time_since_specific_date',
    'displayName': 'Time since specific date',
    'status': True,
    'default_value': None,
    'value': None
}

transform_column = [
    {

    }
]

transform_dropdown_measure = [
    {
        "name": "Replace_value",
        "displayName": "",

    }
]


transform_dropdown_dimension = [

]

feture_engineering_static = {
    'top_level_option': [
        {
          "name": "binning_all_measures",
          "displayName": "Bin all Measures",
          "selected": True,
          "number_of_bins": 10,
          "slug": "",
          "display": True,
        }
    ],
    'measure': {
        "level_creation_settings":{
            "name": "creating_new_bins_or_levels",
            "displayName": "Create Bins Or Levels",
            "selected": True,
            "display": True,
            "operations": [
                # {
                #     "name": "none",
                #     "displayName": "None",
                #     "selected": True,
                #     "columns": [],
                #     "display": True,
                #     "columns_structure": {
                #
                #     }
                # },
                {
                    "name": "create_equal_sized_bins",
                    "displayName": "Create Equal Sized Bins",
                    "selected": True,
                    "columns":[],
                    "display": True,
                    "column_structure": {
                          "name": "quantity",
                          "modified_column_name": "Binned_quantity",
                          "datatype": "measure",
                          "number_of_bins": 10
                        }
                },
                {
                    "name": "create_custom_bins",
                    "displayName": "Create Custom Bins",
                    "selected": True,
                    "columns":[],
                    "display": True,
                    "columns_structure": {
                      "name": "age",
                      "name_after_binning": "Custom_Binned_age",
                      "datatype": "measure",
                      "list_of_intervals": [10,20,30,40]
                    }
                }
          ],
        },
        "transformation_settings": {
            "name": "Transformation_Settings",
            "displayName": "Transform Variables",
            "selected": True,
            "display": True,
            "operations": [
                {
                    "name": "Replace_Values_With",
                    "displayName": "Replace Values With",
                    "selected": True,
                    "columns":[],
                    "display": True,
                    "column_structure": {
                         "name": "Salary",
                         "user_given_new_name": "Salary_new",
                         "datatype": "measure",
                         "replace_by": "mean",
                         "replace_values_in_range": ["lower_val", "upper_val"]
                    }
                },
                {
                    "name": "add_value_to",
                    "displayName": "Add Specific value",
                    "selected": True,
                    "columns":[],
                    "display": True,
                    "column_structure": {
                         "name": "age",
                         "user_given_new_name": "age_added",
                         "datatype": "measure",
                         "value_to_be_added": 5
                    }
                },
                {
                    "name": "subtract_value_from",
                    "displayName": "Subtract Specific value",
                    "selected": True,
                    "columns":[],
                    "display": True,
                    "column_structure": {
                        "name": "height",
                        "user_given_new_name": "height_subtracted",
                        "datatype": "measure",
                        "value_to_be_subtracted": 10
                        }
                },
                {
                    "name": "multiply_by_value",
                    "displayName": "Multiply by Specific value",
                    "selected": True,
                    "columns": [],
                    "display": True,
                    "column_structure": {
                        "name": "bonus_pay",
                        "user_given_new_name": "bonus_pay_multiplied",
                        "datatype": "measure",
                        "value_to_be_multiplied": 10
                    }
                },
                {
                    "name": "divide_by_value",
                    "displayName": "Divide by Specific value",
                    "selected": True,
                    "columns": [],
                    "display": True,
                    "column_structure": {
                     "name": "tax",
                     "user_given_new_name": "tax_divided",
                     "datatype": "measure",
                     "value_to_be_divided": 10
                    }
                },
                {
                    "name": "perform_standardization",
                    "displayName": "Perform Standardization",
                    "selected": True,
                    "columns": [],
                    "display": True,
                    "column_structure": {
                      "name": "Marks_Scored",
                      "user_given_new_name": "Marks_Scored_Standardized",
                      "datatype": "measure",
                      "standardization_type": "Min-Max Scaling"
                    }
                },
                {
                  "name": "variable_transformation",
                  "displayName": "Variable Transformation",
                  "selected": True,
                    "display": True,
                  "columns":[],
                    "column_structure": {
                      "name": "years_of_experience",
                      "user_given_new_name": "years_of_experience_Transformed",
                      "datatype": "measure",
                      "transformation_type": "log-transform"
                    }
                },
                {
                  "name": "encoding_dimensions",
                  "displayName": "Perform Encoding",
                  "selected": True,
                  "columns": [],
                    "display": False,
                    "column_structure":
                    {
                      "name": "country",
                      "new_column_prefix": "Encoded_",
                      "datatype": "dimension",
                      "Encoding_type": "One-hot Encoding"
                    }
                },
                {
                  "name": "return_character_count",
                  "displayName": "return Character Count",
                  "selected": True,
                  "columns": [],
                    "display": False,
                    "column_structure":
                    {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_count",
                      "datatype": "dimension"
                    }
                },
                {
                  "name": "is_custom_string_in",
                  "displayName": "Is custom string in",
                  "selected": True,
                  "columns": [],
                    "display": False,
                    "column_structure": {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_check",
                      "datatype": "dimension",
                      "User_given_character": "Delhi"
                    }
                },
                {
                  "name": "is_date_weekend",
                  "displayName": "Is Date Weekend",
                  "selected": True,
                    "display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates1",
                      "user_given_new_name": "is_weekend_dates1",
                      "datatype": "datetime"
                    }
                },
                {
                  "name": "extract_time_feature",
                  "displayName": "Extract Time Feature",
                  "selected": True,
                    "display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates2",
                      "user_given_new_name": "is_weekend_dates2",
                      "datatype": "datetime",
                      "time_feature_to_extract": "month"
                    }
                },
                {
                  "name": "time_since",
                  "displayName": "Time Since Some Event",
                  "selected": True,
                    "display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates3",
                      "user_given_new_name": "time_since_dates3",
                      "datatype": "datetime",
                      "time_since": "21/05/2016"
                    }
                }
            ]
        }
    },
    'dimension': {
        "level_creation_settings":{
            "name": "creating_new_bins_or_levels",
            "displayName": "Create Bins Or Levels",
            "selected": True,
            "display": True,
            "operations": [
                {
                    "name": "create_equal_sized_bins",
                    "displayName": "Create Equal Sized Bins",
                    "selected": True,
                    "columns":[],"display": False,
                    "column_structure": {
                          "name": "quantity",
                          "modified_column_name": "Binned_quantity",
                          "datatype": "measure",
                          "number_of_bins": 10
                        }
                },
                {
                    "name": "create_custom_bins",
                    "displayName": "Create Custom Bins",
                    "selected": True,"display": False,
                    "columns":[],
                    "columns_structure": {
                      "name": "age",
                      "name_after_binning": "Custom_Binned_age",
                      "datatype": "measure",
                      "list_of_intervals": [10,20,30,40]
                    }
                },
                {
                    "name": "create_new_levels",
                    "displayName": "Create Levels",
                    "selected": True,"display": True,
                    "columns": [],
                    "columns_structure": {
                        "name": "States",
                        "name_after_binning": "States_Levels",
                        "datatype": "dimension",
                        "mapping_dict": {}
                    }

                },
                {
                    "name": "create_new_datetime_levels",
                    "displayName": "Create Datetime Levels",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                        "name": "Date_of_Birth",
                        "name_after_binning": "Date_of_Birth_Levels",
                        "datatype": "datetime",
                        "mapping_dict": {}
                    }
                }
          ],
        },
        "transformation_settings": {
            "name": "transformation_settings",
            "displayName": "Transform Variables",
            "selected": True,"display": True,
            "operations": [
                {
                    "name": "replace_values_with",
                    "displayName": "Replace Values With",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                         "name": "Salary",
                         "user_given_new_name": "Salary_new",
                         "datatype": "measure",
                         "replace_by": "mean",
                         "replace_values_in_range": ["lower_val", "upper_val"]
                    }
                },
                {
                    "name": "add_value_to",
                    "displayName": "Add Specific value",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                         "name": "age",
                         "user_given_new_name": "age_added",
                         "datatype": "measure",
                         "value_to_be_added": 5
                    }
                },
                {
                    "name": "subtract_value_from",
                    "displayName": "Subtract Specific value",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                        "name": "height",
                        "user_given_new_name": "height_subtracted",
                        "datatype": "measure",
                        "value_to_be_subtracted": 10
                        }
                },
                {
                    "name": "multiply_by_value",
                    "displayName": "Multiply by Specific value",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                        "name": "bonus_pay",
                        "user_given_new_name": "bonus_pay_multiplied",
                        "datatype": "measure",
                        "value_to_be_multiplied": 10
                    }
                },
                {
                    "name": "divide_by_value",
                    "displayName": "Divide by Specific value",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                     "name": "tax",
                     "user_given_new_name": "tax_divided",
                     "datatype": "measure",
                     "value_to_be_divided": 10
                    }
                },
                {
                    "name": "perform_standardization",
                    "displayName": "Perform Standardization",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                      "name": "Marks_Scored",
                      "user_given_new_name": "Marks_Scored_Standardized",
                      "datatype": "measure",
                      "standardization_type": "Min-Max Scaling"
                    }
                },
                {
                  "name": "variable_transformation",
                  "displayName": "Variable Transformation",
                  "selected": True,"display": False,
                  "columns":[],
                    "column_structure": {
                      "name": "years_of_experience",
                      "user_given_new_name": "years_of_experience_Transformed",
                      "datatype": "measure",
                      "transformation_type": "log-transform"
                    }
                },
                {
                  "name": "encoding_dimensions",
                  "displayName": "Perform Encoding",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "country",
                      "new_column_prefix": "Encoded_",
                      "datatype": "dimension",
                      "Encoding_type": "One-hot Encoding"
                    }
                },
                {
                  "name": "return_character_count",
                  "displayName": "return Character Count",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_count",
                      "datatype": "dimension"
                    }
                },
                {
                  "name": "is_custom_string_in",
                  "displayName": "Is custom string in",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure": {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_check",
                      "datatype": "dimension",
                      "User_given_character": "Delhi"
                    }
                },
                {
                  "name": "is_date_weekend",
                  "displayName": "Is Date Weekend",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates1",
                      "user_given_new_name": "is_weekend_dates1",
                      "datatype": "datetime"
                    }
                },
                {
                  "name": "extract_time_feature",
                  "displayName": "Extract Time Feature",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates2",
                      "user_given_new_name": "is_weekend_dates2",
                      "datatype": "datetime",
                      "time_feature_to_extract": "month"
                    }
                },
                {
                  "name": "time_since",
                  "displayName": "Time Since Some Event",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates3",
                      "user_given_new_name": "time_since_dates3",
                      "datatype": "datetime",
                      "time_since": "21/05/2016"
                    }
                }
            ]
        }
    },
    'time_dimension': {
        "level_creation_settings":{
            "name": "creating_new_bins_or_levels",
            "displayName": "Create Bins Or Levels",
            "selected": True,"display": True,
            "operations": [
                {
                    "name": "create_equal_sized_bins",
                    "displayName": "Create Equal Sized Bins",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                          "name": "quantity",
                          "modified_column_name": "Binned_quantity",
                          "datatype": "measure",
                          "number_of_bins": 10
                        }
                },
                {
                    "name": "create_custom_bins",
                    "displayName": "Create Custom Bins",
                    "selected": True,"display": False,
                    "columns":[],
                    "columns_structure": {
                      "name": "age",
                      "name_after_binning": "Custom_Binned_age",
                      "datatype": "measure",
                      "list_of_intervals": [10,20,30,40]
                    }
                },
                {
                    "name": "create_new_levels",
                    "displayName": "Create Levels",
                    "selected": True,"display": False,
                    "columns": [],
                    "columns_structure": {
                        "name": "States",
                        "name_after_binning": "States_Levels",
                        "datatype": "dimension",
                        "mapping_dict": {}
                    }

                },
                {
                    "name": "create_new_datetime_levels",
                    "displayName": "Create Datetime Levels",
                    "selected": True,"display": True,
                    "columns": [],
                    "column_structure": {
                        "name": "Date_of_Birth",
                        "name_after_binning": "Date_of_Birth_Levels",
                        "datatype": "datetime",
                        "mapping_dict": {}
                    }
                }
          ],
        },
        "transformation_settings": {
            "name": "transformation_settings",
            "displayName": "Transform Variables",
            "selected": True,"display": True,
            "operations": [
                {
                    "name": "replace_values_with",
                    "displayName": "Replace Values With",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                         "name": "Salary",
                         "user_given_new_name": "Salary_new",
                         "datatype": "measure",
                         "replace_by": "mean",
                         "replace_values_in_range": ["lower_val", "upper_val"]
                    }
                },
                {
                    "name": "add_value_to",
                    "displayName": "Add Specific value",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                         "name": "age",
                         "user_given_new_name": "age_added",
                         "datatype": "measure",
                         "value_to_be_added": 5
                    }
                },
                {
                    "name": "subtract_value_from",
                    "displayName": "Subtract Specific value",
                    "selected": True,"display": False,
                    "columns":[],
                    "column_structure": {
                        "name": "height",
                        "user_given_new_name": "height_subtracted",
                        "datatype": "measure",
                        "value_to_be_subtracted": 10
                        }
                },
                {
                    "name": "multiply_by_value",
                    "displayName": "Multiply by Specific value",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                        "name": "bonus_pay",
                        "user_given_new_name": "bonus_pay_multiplied",
                        "datatype": "measure",
                        "value_to_be_multiplied": 10
                    }
                },
                {
                    "name": "divide_by_value",
                    "displayName": "Divide by Specific value",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                     "name": "tax",
                     "user_given_new_name": "tax_divided",
                     "datatype": "measure",
                     "value_to_be_divided": 10
                    }
                },
                {
                    "name": "perform_standardization",
                    "displayName": "Perform Standardization",
                    "selected": True,"display": False,
                    "columns": [],
                    "column_structure": {
                      "name": "Marks_Scored",
                      "user_given_new_name": "Marks_Scored_Standardized",
                      "datatype": "measure",
                      "standardization_type": "Min-Max Scaling"
                    }
                },
                {
                  "name": "variable_transformation",
                  "displayName": "Variable Transformation",
                  "selected": True,"display": False,
                  "columns":[],
                    "column_structure": {
                      "name": "years_of_experience",
                      "user_given_new_name": "years_of_experience_Transformed",
                      "datatype": "measure",
                      "transformation_type": "log-transform"
                    }
                },
                {
                  "name": "encoding_dimensions",
                  "displayName": "Perform Encoding",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "country",
                      "new_column_prefix": "Encoded_",
                      "datatype": "dimension",
                      "Encoding_type": "One-hot Encoding"
                    }
                },
                {
                  "name": "return_character_count",
                  "displayName": "return Character Count",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_count",
                      "datatype": "dimension"
                    }
                },
                {
                  "name": "is_custom_string_in",
                  "displayName": "Is custom string in",
                  "selected": True,"display": False,
                  "columns": [],
                    "column_structure": {
                      "name": "Cities",
                      "user_given_new_name": "Cities_char_check",
                      "datatype": "dimension",
                      "User_given_character": "Delhi"
                    }
                },
                {
                  "name": "is_date_weekend",
                  "displayName": "Is Date Weekend",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates1",
                      "user_given_new_name": "is_weekend_dates1",
                      "datatype": "datetime"
                    }
                },
                {
                  "name": "extract_time_feature",
                  "displayName": "Extract Time Feature",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates2",
                      "user_given_new_name": "is_weekend_dates2",
                      "datatype": "datetime",
                      "time_feature_to_extract": "month"
                    }
                },
                {
                  "name": "time_since",
                  "displayName": "Time Since Some Event",
                  "selected": True,"display": True,
                  "columns": [],
                    "column_structure":
                    {
                      "name": "dates3",
                      "user_given_new_name": "time_since_dates3",
                      "datatype": "datetime",
                      "time_since": "21/05/2016"
                    }
                }
            ]
        }
    }
}

feature_engineering_ml_settings = {
      "name": "feature_engineering",
      "displayName": "Feature Engineering",
      "selected": False,
      "slug": "",
      "overall_settings": [
        {
          "name": "binning_all_measures",
          "displayName": "Bin all Measures",
          "selected": False,
          "number_of_bins": 10,
          "slug": "",
        }],
      "column_wise_settings": {
        "level_creation_settings": {
          "name": "creating_new_bins_or_levels",
          "displayName": "Create Bins Or Levels",
          "selected": False,
          "operations": [
            {
              "name": "create_equal_sized_bins",
              "displayName": "Create Equal Sized Bins",
              "selected": False,
              "columns":[]

            },
            {
              "name": "create_custom_bins",
              "displayName": "Create Custom Bins",
               "selected": False,
              "columns":[]
            },
            {
              "name": "create_new_levels",
              "displayName": "Create Levels",
               "selected": False,
              "columns":[]

            },
            {
              "name": "create_new_datetime_levels",
              "displayName": "Create Datetime Levels",
             "selected": False,
              "columns":[]
            }]
        },
        "transformation_settings": {
          "name": "transformation_settings",
          "displayName": "Transform Variables",
          "selected": False,
          "operations": [
            {
              "name": "replace_values_with",
              "displayName": "Replace Values With",
              "selected": False,
              "columns":[]
            },
            {
              "name": "add_value_to",
              "displayName": "Add Specific value",
              "selected": False,
              "columns":[]

            },
            {
              "name": "subtract_value_from",
              "displayName": "Subtract Specific value",
              "selected": False,
              "columns":[]
            },
            {
              "name": "multiply_by_value",
              "displayName": "Multiply by Specific value",
              "selected": False,
              "columns":[]
            },
            {
              "name": "divide_by_value",
              "displayName": "Divide by Specific value",
              "selected": False,
              "columns":[]
            },
            {
              "name": "perform_standardization",
              "displayName": "Perform Standardization",
              "selected": False,
              "columns":[]
            },
            {
              "name": "variable_transformation",
              "displayName": "Variable Transformation",
              "selected": False,
              "columns":[]
            },
            {
              "name": "encoding_dimensions",
              "displayName": "Perform Encoding",
              "selected": False,
              "columns":[]
            },
            {
              "name": "return_character_count",
              "displayName": "return Character Count",
              "selected": False,
              "columns":[]
            },
            {
              "name": "is_custom_string_in",
              "displayName": "Is custom string in",
              "selected": False,
              "columns":[]
            },
            {
              "name": "is_date_weekend",
              "displayName": "Is Date Weekend",
              "selected": False,
              "columns":[]
            },
            {
              "name": "extract_time_feature",
              "displayName": "Extract Time Feature",
              "selected": False,
              "columns":[]
            },
            {
              "name": "time_since",
              "displayName": "Time Since Some Event",
              "selected": False,
              "columns":[]
            }
            ]
        }
      }
    }
