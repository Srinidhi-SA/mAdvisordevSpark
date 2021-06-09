#filepath for this file is /mAdvisor-Code/mAdvisor-MLScripts/bi/common/scriptStages.py
# add to master file the below two lines at (line 86)[just after reading config]
    # messages = scriptStages.messages_list(config, jobConfig, jobType, jobName)
    # messages_for_API = messages.send_messages()

from builtins import str
from builtins import range
from builtins import object
class messages_list(object):
    """ Contains messages to send to API """


    def __init__(self, config, jobConfig, jobType, jobName):
        self._config = config
        self._jobConfig = jobConfig
        self._jobType = jobType
        self._jobName = jobName
        self._targetColumn = "Target Column"


        self._training_messages = {
        "Logistic Regression": ("Initialized The Logistic Regression Scripts", "Logistic Regression Model Training Started", "Logistic Regression Model Training Finished"),
        "Random Forest": ("Initialized The Random Forest Scripts", "Random Forest Model Training Started", "Random Forest Model Training Finished"),
        "Ensemble": ("Initialized The Ensemble Scripts", "Ensemble Model Training Started", "Ensemble Model Training Finished"),
        "XGBoost": ("Initialized The Xgboost Scripts", "Xgboost Model Training Started", "Xgboost Model Training Finished"),
        "Adaboost": ("Initialized The AdaBoost Scripts", "AdaBoost Model Training Started", "AdaBoost Model Training Finished"),
        "LightGBM": ("Initialized The LightGBM Scripts", "LightGBM Model Training Started", "LightGBM Model Training Finished"),
        "naive bayes": ("Initialized The Naive Bayes Scripts", "Naive Bayes Model Training Started", "Naive Bayes Model Training Finished"),
        "SVM": ("Initialized the SVM Scripts", "SVM Model Training Started", "SVM Model Training Finished"),
        "Neural Network (Sklearn)": ("Initialized The Neural Network (Sklearn) Scripts", "Neural Network (Sklearn) Model Training Started", "Neural Network (Sklearn) Model Training Finished"),
        "Linear Regression": ("Initialized The Linear Regression Scripts", "Linear Regression Model Training Started", "Linear Regression Model Training Finished"),
        "Gradient Boosted Tree Regression": ("Initialized The Gradient Boosted Tree Regression Scripts","Gradient Boosted Tree Regression Model Training Started", "Gradient Boosted Tree Regression Model Training Finished"),
        "Decision Tree Regression": ("Initialized The Decision Tree Regression Scripts", "Decision Tree Regression Model Training Started", "Decision Tree Regression Model Training Finished"),
        "Random Forest Regression": ("Initialized The Random Forest Regression Scripts", "Random Forest Regression Model Training Started", "Random Forest Regression Model Training Finished"),
        "Neural Network (TensorFlow)": ("Initialized The Neural Network (TensorFlow) Regression Scripts", "Neural Network Model Training Started", "Neural Network (TensorFlow) Neural Network (Sklearn) Model Training Finished"),
        "Neural Network (PyTorch)": ("Initialized The Neural Network (PyTorch)  Scripts", "Neural Network (PyTorch)  Training Started", "Neural Network (PyTorch)  Training Finished")
        }

        self._score_messages = {
        "LightGBM": ("Initialized The LightGBM Scripts", "LightGBM Model Prediction Finished"),
        "Logistic Regression": ("Initialized The Logistic Regression Scripts", "Logistic Regression Model Prediction Finished"),
        "Random Forest": ("Initialized The Random Forest Scripts", "Random Forest Model Prediction Finished"),
        "Ensemble": ("Initialized The Ensemble Scripts", "Ensemble Model Prediction Finished"),
        "XGBoost": ("Initialized The Xgboost Scripts", "XGBoost Model Prediction Finished"),
        "Adaboost": ("Initialized The Adaboost Scripts", "AdaBoost Model Prediction Finished"),
        "Naive Bayes": ("Initialized The Naive Bayes Scripts", "Naive Bayes Model Prediction Finished"),
        "SVM": ("Initialized the SVM Scripts", "SVM Model Training Started", "SVM Model Training Finished"),
        "Neural Network (Sklearn)": ("Initialized The Neural Network (Sklearn) Scripts", "Neural Network (Sklearn) Model Prediction Finished"),
        "Linear Regression": ("Initialized The Linear Regression Scripts", "Linear Regression Model Prediction Started", "Linear Regression Model Prediction Finished;"),
        "GBT Regression": ("Initialized The Gradient Boosted Tree Regression Scripts","Gradient Boosted Tree Regression Model Prediction Started", "Gradient Boosted Tree Regression Model Prediction Finished"),
        "DTREE Regression": ("Initialized The Decision Tree Regression Scripts", "Decision Tree Regression Model Prediction Started", "Decision Tree Regression Model Prediction Finished"),
        "RF Regression": ("Initialized The Random Forest Regression Scripts", "Random Forest Regression Model Prediction Started", "Random Forest Regression Model Prediction Finished"),
        "Neural Network (TensorFlow)": ("Initialized The Neural Network (TensorFlow) Neural Network Scripts", "Neural Network (TensorFlow) Neural Network  Model Prediction Finished"),
        "dtree Regression": ("Initialized The Decision Tree Regression Scripts", "Decision Tree Regression Model Prediction Started", "Decision Tree Regression Model Prediction Finished"),
        "Neural Network (PyTorch)": ("Initialized The Neural Network (PyTorch)  Scripts", "Neural Network (PyTorch)  Prediction Finished")
        }

        self._metaData_messages = ('Preparing Data For Loading', 'Initializing The Loading Process', 'Uploading Data', 'Creating Metadata For The Dataset', 'Sampling The Dataframe', 'Calculated Stats For Measure Columns', 'Calculated Stats For Time Dimension Columns', 'Calculated Stats For Dimension Columns', 'Validating Metadata Information', 'Ignore And Date Suggestions', 'Your Data Is Uploaded', 'Job Finished')

        self._story_messages_measure = {"Overview1": ['Analyzing Target Variable', 'Choosing Statistical And Machine Learning Techniques For Analysis', 'Initialized The Descriptive Stats Scripts', 'Descriptive Stats Calculated', 'Started The Descriptive Stats Narratives', 'Narratives For Descriptive Stats Finished'],
        "Overview2": ['Validating Analysis Results', 'Creating Visualizations', 'Creating Narratives', 'Your Signal Is Ready', 'Job Finished'],
        "Trend": ['Analyzing Trend For Something', 'Started The Descriptive Stats Narratives', 'Narratives For Descriptive Stats Finished'],
        "Performance": [ 'Evaluating Variables For Performance Analysis', 'Initialized The Anova Scripts', 'Anova Calculated', 'Started The Anova Narratives', 'Analyzing Key Drivers', 'Narratives For Anova Finished'],
        "Influencer": ['Finding Factors That Influence Target Variable', 'Started The Regression Script', 'Regression Coefficients Calculated', 'Started The Regression Narratives', 'Analyzing Key Influencers', 'Narratives For Regression Finished'],
        "Prediction": [ 'Creating Prediction Model For target', 'Started The Decision Tree Regression Script', 'Decision Tree Regression Learning Finished', 'Started The Decision Tree Regression Narratives', 'Generating Prediction Rules', 'Narratives For Decision Tree Regression Finished']}

        self._story_messages_dimension = {"Overview1": ['Analyzing Target Variable', 'Choosing Statistical And Machine Learning Techniques For Analysis', 'Initialized the Frequency Scripts', 'Running Groupby Operations', 'Frequency Stats Calculated', 'Initialized The Frequency Narratives', 'Summary Generation Finished'],
        "Overview2": ['Validating Analysis Results', 'Creating Visualizations', 'Creating Narratives', 'Your Signal Is Ready', 'Job Finished'],
        "Trend": ['Analyzing Trend For target', 'Initialized The Frequency Narratives', 'Summary Generation Finished', 'Frequency Stats Narratives Done'],
        "Association": ['Evaluating Variables For Statistical Association', 'Initialized the Chisquare Scripts', 'Chisquare Stats Calculated', 'Initialized the Frequency Narratives', 'Analyzing key drivers', 'Summary Generation Finished', 'Frequency Stats Narratives Done'],
        "Prediction": ['Creating Prediction Model For target', 'Initialized The Decision Tree Script', 'Decision Tree Generation Finished', 'Started The Decision Tree Narratives', 'Generating Prediction Rules', 'Narratives For Decision Tree Finished']}

    def send_messages(self):
        output_messages = []

        if self._jobType == 'training':
            output_messages.append('Loading The Dataset')
            if self._config['FEATURE_SETTINGS']['DATA_CLEANSING']['selected'] == True or self._config['FEATURE_SETTINGS']['FEATURE_ENGINEERING']['selected']  == True:
                output_messages.append('Performing Required Data Preprocessing And Feature Transformation Tasks')
            output_messages.append('Dataset Loading Completed')
            for modeltype in self._config['ALGORITHM_SETTING']:
                if modeltype['selected'] == True:
                    for i in self._training_messages[modeltype['algorithmName']]:
                        output_messages.append(i)
            output_messages.append('Evaluating And Comparing Performance Of All Predictive Models')
            output_messages.append('mAdvisor Has Successfully Completed Building Machine Learning Models')

        if self._jobType == 'prediction':
            output_messages.append('Loading The Dataset')
            if self._config['FEATURE_SETTINGS']['DATA_CLEANSING']['selected'] == True or self._config['FEATURE_SETTINGS']['FEATURE_ENGINEERING']['selected']  == True:
                output_messages.append('Performing Required Data Preprocessing And Feature Transformation Tasks')
            output_messages.append('Dataset Loading Completed')
            for i in self._score_messages[self._config['FILE_SETTINGS']['selectedModel'][0]['name']]:
                output_messages.append(i)
            score_ending_messages = ['Initialized The Decision Tree Script', 'Decision Tree Generation Finished', 'Started The Decision Tree Narratives', 'Generating Prediction Rules', 'Narratives For Decision Tree Finished', 'mAdvisor Has Successfully Completed Building Machine Learning Models']
            for i in score_ending_messages:
                output_messages.append(i)

        if self._jobType == 'metaData':
            for i in self._metaData_messages:
                output_messages.append(i)

#        if self._jobType == 'stockAdvisor':
#            stocks = self._config["STOCK_SETTINGS"]["stockSymbolList"]
#            for stock in stocks:
#                output_messages.append("Analyzing " + str.upper(stock) + " Data")
#            for stock in stocks:
#                output_messages.append("Applying Regression on  " + str.upper(stock) + " Data")
#            output_messages.extend(["Calculating Stock Price Trend"])

        if self._jobType == 'story':
            storyType = ''
            targetColumn = ''
            for columns in self._config['COLUMN_SETTINGS']['variableSelection']:
                if columns['targetColumn'] == True:
                    targetColumn = columns['name']
                    if columns['columnType'] == "dimension":
                        storyType = "dimension"
                    elif columns['columnType'] == "measure":
                        storyType = "measure"

            if storyType == "measure":
                for i in self._story_messages_measure["Overview1"]:
                    output_messages.append(i)
            elif storyType == "dimension":
                for i in self._story_messages_dimension["Overview1"]:
                    output_messages.append(i)

            for task in self._config['ADVANCED_SETTINGS']['analysis']:
                if task['status'] == True:
                    if task['displayName'] == "Overview":
                        pass
                    else:
                        if storyType == "measure":
                            self._story_messages_measure["Trend"][0] = 'Analyzing Trend For ' + str(targetColumn)
                            self._story_messages_measure["Prediction"][0] = 'Creating Prediction Model For ' + str(targetColumn)
                            for i in self._story_messages_measure[task['displayName']]:
                                output_messages.append(i)
                        elif storyType == "dimension":
                            self._story_messages_dimension["Trend"][0] = 'Analyzing Trend For ' + str(targetColumn)
                            self._story_messages_dimension["Prediction"][0] = 'Creating Prediction Model For ' + str(targetColumn)
                            for i in self._story_messages_dimension[task['displayName']]:
                                output_messages.append(i)

            if storyType == "measure":
                for i in self._story_messages_measure["Overview2"]:
                    output_messages.append(i)
            elif storyType == "dimension":
                for i in self._story_messages_dimension["Overview2"]:
                    output_messages.append(i)


        output_dictionary ={i:output_messages[i] for i in range(len(output_messages))}
        return output_dictionary
#comment above two and uncomment below two line if output is required in a list format. The print statement is to be used if required
        # print output_messages
        # return output_messages
