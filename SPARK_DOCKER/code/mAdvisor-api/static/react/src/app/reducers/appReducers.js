
export default function reducer(state = {
        appsModelShowModal:false,
        modelList: {},
        allModelList: {},
        algoList:{},
        deploymentData:{},
        viewDeploymentFlag:false,
        allProjects: {},
        deploymentList:{},
        deployShowModal:false,
        algo_search_element:"",
        deployItem:{},
        deployData: {},
        current_page:1,
        trainValue:50,
        testValue:50,
        scoreList:{},
        appsScoreShowModal:false,
        modelSlug:"",
        modelSummary:{},
        algorithmsList:null,
        selectedAlg:"",
        scoreSummary:{},
        scoreSlug:"",
        scoreSlugShared:"",
        currentAppId:"",
        currentAppName:"",
        appsLoaderModal:false,
        appsLoaderPerValue:-1,
        appsLoaderText :"",
        appsLoadedText :["Loading..."],
        modelSummaryFlag:false,
        parameterTuningFlag:false,
        scoreSummaryFlag:false,
        modelTargetVariable:"",
        roboList:{},
        appsRoboShowModal:false,
        customerDataUpload:{},
        historialDataUpload:{},
        externalDataUpload:{},
        roboDatasetSlug:"",
        roboSummary:{},
        showRoboDataUploadPreview:false,
        customerDataset_slug :"",
        historialDataset_slug:"",
        externalDataset_slug:"",
        roboUploadTabId:"customer",
        robo_search_element:"",
        model_search_element:"",
        score_search_element:"",
        appsSelectedTabId:"model",
        audioFileUploadShowFlag:false,
        audioFileUpload:{},
        audioFileSummary:{},
        audioFileSlug :"",
        audioFileSummaryFlag:false,
        audioList:{},
        audio_search_element:"",
        robo_sorton:null,
        robo_sorttype:null,
        apps_model_sorton:null,
        apps_model_sorttype:null,
        filter_models_by_mode:"",
        apps_score_sorton:null,
        apps_score_sorttype:null,
        appsCreateStockModal:false,
        appsStockSymbolsInputs:[],
        stockAnalysisList:{},
        tensorFlowInputs:[],
        stockUploadDomainModal:false,
        stockUploadDomainFiles:[],
        stockSlug:"",
        stockAnalysisFlag:false,
        conceptList:{},
        scoreSummaryCSVData:[],
        appsList:[],
        storeAppsSearchElement:"",
        storeAppsSortByElement : "",
        storeAppsSortType:"",
        app_filtered_keywords:[],
        exportAsPMMLModal:false,
        scoreToProceed:false,
        latestScores : {},
        latestModels :{},
        latestAlgos:{},
        latestRoboInsights:{},
        latestAudioList:{},
        latestStocks:{},
        targetLevelCounts:"",
        currentAppDetails:null,
        apps_regression_modelName:"",
        apps_regression_targetType:"",
        apps_regression_levelCount:"",
        regression_algorithm_data:[],
        regression_algorithm_data_manual:[],
        regression_selectedTechnique:"crossValidation",
        regression_crossvalidationvalue:2,
        selectedModelCount:0,
        selectedAlgObj:{},
        stock_model_search_element:"",
        stock_apps_model_sorton:null,
        stock_apps_model_sorttype:null,
        unselectedModelsCount:0,
        metricSelected:{},
        pyTorchLayer:{},
        pyTorchSubParams:{},
        idLayer:[],
        layerType:"Dense",
        panels:[],
        modelLoaderidxVal:0,
        modelLoaderidx:0,
        allStockAnalysisList:{},
        chartLoaderFlag:false,
        activeAlgorithmTab:""

}, action) {

    switch (action.type) {
    case "APPS_MODEL_SHOW_POPUP":
    {
        return {
            ...state,
            appsModelShowModal:true,
        }
    }
    break;

    case "APPS_MODEL_HIDE_POPUP":
    {
        return {
            ...state,
            appsModelShowModal:false,
        }
    }
    break;
    case "MODEL_LIST":
    {
        return {
            ...state,
            modelList: action.data,
            latestModels:action.latestModels,
            current_page:action.current_page,
        }
    }
    break;

    case "MODEL_LIST_ERROR":
    {
        throw new Error("Unable to fetch model list!!");
    }
    break;
    case "MODEL_ALL_LIST":
      {
        return {
          ...state,
          allModelList: action.data,
        }
      }
      break;
    case "MODEL_ALL_LIST_ERROR":
    {
        throw new Error("Unable to fetch model list!!");
    }
    break;
    case "ALGO_LIST":
    {
        return {
            ...state,
            algoList: action.data,
            latestAlgos:action.latestAlgos,
            current_page:action.current_page,
        }
    }
    break;
    case "CLEAR_APPS_ALGO_LIST":
    {
        return {
            ...state,
            algoList:{}
        }
    }
    break;

    case "ALGO_LIST_ERROR":
    {
        throw new Error("Unable to fetch model list!!");
    }
    break;

    case "DEPLOYMENT_LIST_ERROR":
    {
        throw new Error("Unable to fetch model list!!");
    }
    break;

    case "DEPLOYMENT_LIST":
    {
        return {
            ...state,
            deploymentList: action.data,
            current_page:action.current_page,
        }
    }
    break;

    case "SAVE_DEPLOY_DATA":
    {
        var dd = action.dataToSave
        return{
            ...state,
            deployData :{
                "name":dd.name,
                "deploytrainer": action.colSlug,
                "config":{
                "dataset_details":{
                    "datasource_details":{
                        "datasetname":dd.datasetname,
                        "bucket_name":dd.s3Bucket,
                        "file_name":dd.file_name,
                        "access_key_id":dd.access_key_id,
                        "secret_key":dd.secret_key
                    },
                    "datasource_type":"S3"
                },
                "timing_details": dd.timing_details,
                "destination_s3": { "bucket": "none" }
                },
                "data":{}
            }
        }
    }
    break;

    case "CREATE_DEPLOY_SUCCESS":
    {
        return {
            ...state,
        }
    }
    break;
    case "CREATE_DEPLOY_ERROR":
    {
        throw new Error("Unable to create deployment!");
    }
    break;

    case "VIEW_DEPLOY_SUCCESS":
    {
        return {
            ...state,
            deploymentData: action.data,
            viewDeploymentFlag:true,
        }
    }
    break;

    case "VIEW_DEPLOY_ERROR":
    {
        throw new Error("Unable to fetch Deployment Details");
    }
    break;
    case "SEARCH_ALGORITHM":
    {
        return{
            ...state,
            algo_search_element:action.search_element
        }
    }

    case "DEPLOY_SHOW_MODAL":
    {
      return {
        ...state,
        deployShowModal: true,
        deployItem:action.selectedItem
      }
    }
    break;

    case "DEPLOY_HIDE_MODAL":
    {
      return {
        ...state,
        deployShowModal: false
      }
    }
    break;
    case "HIDE_VIEW_MODAL":
    {
      return {
        ...state,
        viewDeploymentFlag: false
      }
    }
    break;

    case "PROJECT_ALL_LIST":
    {
      return {
        ...state,
        allProjects: action.data,
      }
    }
    break;
    case "PROJECT_ALL_LIST_ERROR":
      {
        throw new Error("Unable to fetch project list!!");
      }
      break;

    case "UPDATE_MODEL_RANGE":
    {
        return {
            ...state,
            trainValue: action.trainValue,
            testValue:action.testValue,
        }
    }
    break;

    case "SCORE_LIST":
    {
        return {
            ...state,
            scoreList: action.data,
            latestScores:action.latestScores,
            current_page:action.current_page,
        }
    }
    break;
    case "CLEAR_SCORE_LIST":{
        return{
            ...state,
            scoreList:{}
        }
    }
    break;
    case "SCORE_LIST_ERROR":
    {
        throw new Error("Unable to fetch score list!!");
    }
    break;
    case "APPS_SCORE_SHOW_POPUP":
    {
        return {
            ...state,
            appsScoreShowModal:true,
        }
    }
    break;

    case "APPS_SCORE_HIDE_POPUP":
    {
        return {
            ...state,
            appsScoreShowModal:false,
        }
    }
    break;

    case "MODEL_SUMMARY_SUCCESS":
    {
        return {
            ...state,
            modelSummary: action.data,
            algorithmsList:action.data.data.model_dropdown,
            modelSlug:action.data.slug,
            modelTargetVariable:action.data.data.config.target_variable[0],
            unselectedModelsCount:(action.data.data.model_hyperparameter != null)?(action.data.data.model_dropdown.length - (action.data.data.model_hyperparameter.length-1)):0,
        }
    }
    break;
    case "CLEAR_MODEL_SUMMARY":
    {
        return {
            ...state,
            modelSummary: {},
            modelSlug:"",
            unselectedModelsCount:0,
        }
    }
    break;
    case "MODEL_SUMMARY_ERROR":
    {
        throw new Error("Unable to fetch model summary!!");
    }
    break;

    case "SELECTED_ALGORITHM":
    {
        return {
            ...state,
            selectedAlg:action.name,
        }
    }
    break;
    case "SCORE_SUMMARY_SUCCESS":
    {

        return {
            ...state,
            scoreSummary: action.data,
            scoreSlug:action.data.slug,
            scoreSlugShared:action.data.shared_slug,
        }
    }
    break;
    case "CLEAR_SCORE_SUMMARY":{
        return{
            ...state,
            scoreSummary: {},
            scoreSlug:"",
            scoreSlugShared:"",
        }
    }
    break;
    case "SCORE_SUMMARY_ERROR":
    {
        throw new Error("Unable to fetch score summary!!");
    }
    break;
    case "SCORE_SUMMARY_CSV_DATA":
    {
       var scoreCsvData=action.data.length!=0?action.data.csv_data:[]
        return {
            ...state,
            scoreSummaryCSVData: scoreCsvData,
        }
    }
    break;
    case "SELECTED_APP_DETAILS":
    {
        return {
            ...state,
            currentAppId: action.appId,
            currentAppName:action.appName,
            currentAppDetails:action.appDetails
        }
    }
    break;
    case "SHOW_CREATE_MODAL_LOADER":
      {
        return {
          ...state,
          appsLoaderModal: true
        }
      }
      break;
    case "OPEN_APPS_LOADER_MODAL":
    {
        return {
            ...state,
            appsLoaderPerValue:action.value,
            appsLoaderText :action.text,
        }
    }
    break;
    case "APPS_LOADED_TEXT":{
        return {
            ...state,
            appsLoadedText : action.text,
        }
    }
    break;
    case "MODEL_LOADER_IDX_VAL": {
        return {
          ...state,
          modelLoaderidxVal : action.idxVal
        }
      }
      break;
    case "MODEL_LOADER_IDX": {
      return {
        ...state,
        modelLoaderidx : action.idx
      }
    }
    break;
    case "CLEAR_MODEL_LOADER_VALUES":{
      return {
        ...state,
        modelLoaderidxVal:0,
        modelLoaderidx:0,
      }
    }
    break;
    case "HIDE_APPS_LOADER_MODAL":
    {

        return {
            ...state,
            appsLoaderModal:false,
            appsLoaderPerValue:-1,
            appsLoaderText :"",
        }
    }
    break;
    case "UPDATE_APPS_LOADER_VALUE":
    {

        return {
            ...state,
            appsLoaderPerValue:action.value,
        }
    }
    break;
    case "CREATE_MODEL_SUCCESS":
    {
        return {
            ...state,
            modelSlug:action.slug,
        }
    }
    break;
    case "CREATE_MODEL_ERROR":
    {
        throw new Error("Unable to create model!");
    }
    break;
    case "UPDATE_MODEL_FLAG":
    {
        return {
            ...state,
            modelSummaryFlag:action.flag,
        }
    }
    break;
    case "UPDATE_PARAMETER_TUNING_FLAG":
    {
        return {
            ...state,
            parameterTuningFlag:action.flag,
        }
    }
    break;
    case "CREATE_SCORE_SUCCESS":
    {
        return {
            ...state,
            scoreSlug:action.slug,
            scoreSlugShared:action.sharedSlug,
        }
    }
    break;
    case "UPDATE_SCORE_FLAG":
    {
        return {
            ...state,
            scoreSummaryFlag:action.flag,
        }
    }
    break;
    case "ROBO_LIST":
    {
        return {
            ...state,
            roboList: action.data,
            latestRoboInsights:action.latestRoboInsights,
            current_page:action.current_page,
        }
    }
    break;

    case "ROBO_LIST_ERROR":
    {
        throw new Error("Unable to fetch robo list!!");
    }
    break;
    case "APPS_ROBO_SHOW_POPUP":
    {
        return {
            ...state,
            appsRoboShowModal:true,
        }
    }
    break;

    case "APPS_ROBO_HIDE_POPUP":
    {
        return {
            ...state,
            appsRoboShowModal:false,
        }
    }
    break;
    case "CUSTOMER_DATA_UPLOAD_FILE":
    {
        return {
            ...state,
            customerDataUpload:action.files[0],
        }
    }
    break;
    case "HISTORIAL_DATA_UPLOAD_FILE":
    {
        return {
            ...state,
            historialDataUpload:action.files[0],
        }
    }
    break;

    case "EXTERNAL_DATA_UPLOAD_FILE":
    {
        return {
            ...state,
            externalDataUpload:action.files[0],
        }
    }
    break;
    case "ROBO_DATA_UPLOAD_SUCCESS":
    {
        return {
            ...state,
            roboDatasetSlug:action.slug,
        }
    }
    break;

    case "ROBO_DATA_UPLOAD_ERROR":
    {
        throw new Error("Unable to upload robo data files!!");
    }
    break;
    case "ROBO_SUMMARY_SUCCESS":
    {
        return {
            ...state,
            roboSummary: action.data,
            roboDatasetSlug:action.data.slug,
            customerDataset_slug:action.data.customer_dataset.slug,
            historialDataset_slug:action.data.historical_dataset.slug,
            externalDataset_slug:action.data.market_dataset.slug,
        }
    }
    break;
    case "ROBO_DATA_UPLOAD_PREVIEW":
    {
        return {
            ...state,
            showRoboDataUploadPreview: action.flag,
        }
    }
    break;
    case "ROBO_SUMMARY_ERROR":
    {
        throw new Error("Unable to fetch robo summary!!");
    }
    break;
    case "EMPTY_ROBO_DATA_UPLOAD_FILES":
    {
        return {
            ...state,
            historialDataUpload:{},
            customerDataUpload:{},
            externalDataUpload:{},

        }
    }
    break;
    case "UPDATE_ROBO_UPLOAD_TAB_ID":
    {
        return {
            ...state,

            roboUploadTabId:action.tabId,
        }
    }
    break;
    case "APPS_SELECTED_TAB":
    {
        return {
            ...state,
            appsSelectedTabId:action.id,
        }
    }
    break;
    case "SEARCH_ROBO":
    {
        return{
            ...state,
            robo_search_element:action.search_element
        }
    }
    break;
    case "SEARCH_MODEL":
    {
        return{
            ...state,
            model_search_element:action.search_element
        }
    }
    break;
    case "SEARCH_SCORE":
    {
        return{
            ...state,
            score_search_element:action.search_element
        }
    }
    break;
    case "CLEAR_ROBO_SUMMARY_SUCCESS":
    {
        return {
            ...state,
            roboSummary: {},
            roboDatasetSlug:"",
            customerDataset_slug:"",
            historialDataset_slug:"",
            externalDataset_slug:"",
            roboUploadTabId:"customer",
        }
    }
    break;
    case "SHOW_AUDIO_FILE_UPLOAD":
    {
        return{
            ...state,
            audioFileUploadShowFlag:true,
        }
    }
    break;
    case "HIDE_AUDIO_FILE_UPLOAD":
    {
        return{
            ...state,
            audioFileUploadShowFlag:false,
        }
    }
    break;
    case "AUDIO_UPLOAD_FILE":
    {
        return{
            ...state,
            audioFileUpload:action.files[0],
        }
    }
    break;
    case "AUDIO_UPLOAD_SUCCESS":
    {
        return{
            ...state,
            audioFileSlug:action.slug,
        }
    }
    break;
    case "AUDIO_UPLOAD_ERROR":
    {
        throw new Error("Unable to upload audio files!!");
    }
    break;
    case "AUDIO_UPLOAD_SUMMARY_SUCCESS":
    {
        return{
            ...state,
            audioFileSummary:action.data,
        }
    }
    break;
    case "AUDIO_UPLOAD_SUMMARY_ERROR":
    {
        throw new Error("Unable to get audio file preview!!");
    }
    break;
    case "CLEAR_AUDIO_UPLOAD_FILE":
    {
        return{
            ...state,
            audioFileUpload:{},
        }
    }
    break;
    case "UPDATE_AUDIO_FILE_SUMMARY_FLAG":
    {
        return{
            ...state,
            audioFileSummaryFlag:action.flag,
        }
    }
    break;

    case "AUDIO_LIST":
    {
        return {
            ...state,
            audioList: action.data,
            current_page:action.current_page,
            latestAudioList:action.latestAudioFiles,
        }
    }
    break;

    case "AUDIO_LIST_ERROR":
    {
        throw new Error("Unable to fetch audio list!!");
    }
    break;
    case "SEARCH_AUDIO_FILE":
    {
        return{
            ...state,
            audio_search_element:action.search_element
        }
    }
    break;

    case "SORT_ROBO":
    {
        return{
            ...state,
            robo_sorton:action.roboSorton,
            robo_sorttype:action.roboSorttype
        }
    }
    break;	
    case "SORT_APPS_MODEL":
    {
        return{
            ...state,
            apps_model_sorton:action.appsModelSorton,
            apps_model_sorttype:action.appsModelSorttype
        }
    }
    break;
    break;	case "FILTER_APPS_MODEL":
    {
        return{
            ...state,
            filter_models_by_mode:action.filter_by_mode,
        }
    }
    break;
    case "SORT_APPS_SCORE":
    {
        return{
            ...state,
            apps_score_sorton:action.appsScoreSorton,
            apps_score_sorttype:action.appsScoreSorttype
        }
    }
    break;

    case "CREATE_STOCK_MODAL":
    {
        return{
            ...state,
            appsCreateStockModal:action.flag

        }
    }
    break;
    case "ADD_STOCK_SYMBOLS":
    {
        return{
            ...state,
            appsStockSymbolsInputs:action.stockSymbolsArray

        }
    }
    break;
    case "EDIT_TENSORFLOW_INPUT":{
        return{
            ...state,
            tensorFlowInputs : action.editTfInput
        }
    }
    break;

    case "ADD_LAYERS":
    {
        var curTfData = state.tensorFlowInputs
        curTfData[action.id-1] =  action.tensorFlowArray;
        return{
            ...state,
            tensorFlowInputs : curTfData.filter(i=>i!=null)
        }
    }

    break;    
    case "UPDATE_LAYERS":
    { 
        var stateval =state.tensorFlowInputs
        action.tensorFlowInputs[action.name] = action.val;
        stateval[action.arrayIndxToUpdate]=action.tensorFlowInputs        
        return{
          ...state,
          tensorFlowInputs : stateval
        }
    }

    break;
    
    case "DELETE_LAYER_TENSORFLOW":
    { 
        var curTfData =state.tensorFlowInputs.filter(i=>i!=null).filter(j=>j.layerId!=action.deleteId)
        var delPanel = state.panels;
        delPanel.pop(action.deleteId)
        return{
          ...state,
          tensorFlowInputs :curTfData,
          panels : delPanel
        }
      }

    break;
    
    case "CLEAR_LAYERS":
    {
        return{
          ...state,
          tensorFlowInputs :[],
          panels : [],
          layerType:"Dense",
        }
      }

    break;

    case "CHANGE_LAYER_TYPE":{
        return{
            ...state,
            layerType:action.layerTyp,
        }
    }
    break;
    case "PANELS_TENSOR":{
        return{
            ...state,
            panels:action.newPanel
        }
    }
    break;

    case "STOCK_LIST":
    {
        return {
            ...state,
            stockAnalysisList: action.data,
            current_page:action.current_page,
            latestStocks:action.latestStocks,
        }
    }
    break;

    case "STOCK_LIST_ERROR":
    {
        throw new Error("Unable to fetch stock list!!");
    }
    break;
    case "UPLOAD_STOCK_MODAL":
    {
        return{
            ...state,
            stockUploadDomainModal:action.flag

        }
    }
    break;
    case "UPLOAD_STOCK_FILES":
    {
        return{
            ...state,
            stockUploadDomainFiles:action.files

        }
    }
    break;
    case "STOCK_CRAWL_SUCCESS":
    {
        return{
            ...state,
            stockSlug:action.slug,
        }
    }
    break;
    case "UPDATE_STOCK_ANALYSIS_FLAG":
    {
        return{
            ...state,
            stockAnalysisFlag:action.flag,
        }
    }
    break;
    case "CONCEPTSLIST":
    {
        return{
            ...state,
            conceptList:action.concepts
        }
    }
    break;

    case "UPDATE_LOADER_TEXT":
    {
        return{
            ...state,
            appsLoaderText:action.text
        }
    }
    break;
    case "APPS_LIST":
    {
        return {
            ...state,
            appsList: action.json,
            current_page:action.current_page,
        }
    }
    break;
    case "CLEAR_APPS_LIST":{
        return{
            ...state,
            appsList:[],
            current_page:1,
        }
    }
    case "APPS_LIST_ERROR":
    {
        throw new Error("Unable to fetch apps list data!!");
    }
    break;

    case "APPS_SEARCH":
    {
        return{
            ...state,
            storeAppsSearchElement:action.search_element
        }
    }
    break;
    case "APPS_SORT":
    {
        return{
            ...state,
            storeAppsSortType:action.sort_type,
            storeAppsSortByElement:action.sort_by
        }
    }
    break;
    case "UPDATE_FILTER_LIST":
    {
        return{
            ...state,
            app_filtered_keywords:action.filter_list
        }
    }
    break;

    case "EXPORT_AS_PMML_MODAL":
    {
        return{
            ...state,
            exportAsPMMLModal:action.flag
        }
    }
    break;

    case "SCORE_TO_PROCEED":
    {
        return{
            ...state,
            scoreToProceed:action.flag
        }
    }
    break;
    case "SET_TARGET_LEVEL_COUNTS":
    {
        return{
            ...state,
            targetLevelCounts:action.levelCounts
        }
    }
    break;
    case "SAVE_SELECTED_VALES_FOR_MODEL":
    {
        return{
            ...state,
            apps_regression_modelName:action.modelName,
            apps_regression_targetType:action.targetType,
            apps_regression_levelCount:action.levelCount
        }
    }
    break;
    case "SAVE_REGRESSION_ALGORITHM_DATA":
    {
        return{
            ...state,
            regression_algorithm_data:action.data.ALGORITHM_SETTING,
            regression_algorithm_data_manual:action.data.ALGORITHM_SETTING,
        }
    }
    break;
    case "ID_LAYER_ARRAY":{
        let curIdArray = state.idLayer.concat([action.newLayer])
        return{
            ...state,
            idLayer:curIdArray,
        }
    }
    break;
    case "SET_PYTORCH_LAYER":{
        var layerData = state.pyTorchLayer
        var curLayer = layerData[parseInt(action.layerNum)];
        if(curLayer === undefined){
            curLayer = {}
        }
        curLayer = action.lyrDt
        layerData[action.layerNum] = curLayer
        return {
            ...state,
            pyTorchLayer : layerData
        }
    }
    break;
    case "SET_PYTORCH_SUBPARAMS":{
        return {
            ...state,
            pyTorchSubParams : action.subParamDt
        }
    }
    break;
    case "DELETE_LAYER_PYTORCH":{
        var newPyTorchLayer = state.pyTorchLayer
        delete newPyTorchLayer[action.layerNum];
        return {
            ...state,
            pyTorchLayer : newPyTorchLayer,
            idLayer : action.newIdArray
        }
    }
    break;
    case "CLEAR_PYTORCH_VALUES":{
        return {
            ...state,
            pyTorchLayer : {},
            pyTorchSubParams : {},
            idLayer : [],
        }
    }
    break;
    case "UPDATE_REGRESSION_ALGORITHM_DATA":
    {
        return{
            ...state,
            regression_algorithm_data_manual:action.newAlgorithm,
        }
    }
    break;
    case "UPDATE_REGRESSION_TECHNIQUE":
    {
        return{
            ...state,
            regression_selectedTechnique:action.name,
        }
    }
    break;
    case "UPDATE_CROSS_VALIDATION_VALUE":
    {
        return{
            ...state,
            regression_crossvalidationvalue:action.val,
        }
    }
    break;
    case "RESET_REGRESSION_VARIABLES":
    {
        return{
            ...state,
            regression_algorithm_data:[],
            regression_algorithm_data_manual:[],
            regression_selectedTechnique:"crossValidation",
            regression_crossvalidationvalue:2,
        }
    }
    break;
    case "EDIT_REGRESSION_ALGORITHM_DATA":
    {
        return{
            ...state,
            regression_algorithm_data:action.newAlgorithm,
        }
    }
    break;
     case "SAVE_CHECKED_ALGORITHMS":
    {
        return{
            ...state,
            algorithmsList:action.selectedAlgorithms,
            selectedModelCount:action.selectedModelCount,
            modelSummary:action.modelSummary,
        }
    }
    break;
    case "SELECTED_ALGORITHM_OBJECT":
    {
        return{
            ...state,
            selectedAlgObj:action.obj,
        }
    }
    break;
     case "CLEAR_SELECT_MODEL_COUNT":
    {
        return{
            ...state,
            selectedModelCount:action.count,
        }
    }
    break;
    case "STOCK_SEARCH_MODEL":
    {
        return{
            ...state,
            stock_model_search_element:action.search_element
        }
    }
    break;
    case "STOCK_SORT_APPS_MODEL":
    {
        return{
            ...state,
            stock_apps_model_sorton:action.appsModelSorton,
            stock_apps_model_sorttype:action.appsModelSorttype
        }
    }
    break;
    case "SET_EVALUATION_METRIC":
    { 
        return{
            ...state,
            metricSelected :{
                "selected" : action.selected,
                "name" : action.name,
                "displayName" : action.displayName
            }
        }
    }
    break;
    case "ALL_STOCK_ANALYSIS_LIST":
      {
        return {
          ...state,
          allStockAnalysisList: action.data,
        }
      }
      break;
      case "ALL_STOCK_ANALYSIS_LIST_ERROR":
      {
        throw new Error("Unable to fetch stock analysis list!!");
      }
      break;
    case "SET_LOADER_FLAG":{
        return{
            ...state,
            chartLoaderFlag:action.flag
        }
    }
    break;
    case "ACTIVE_ALGORITHM_SLUG":{
        return{
            ...state,
            activeAlgorithmTab:action.slug
        }
    }
    break;
    case "CLEAR_MODEL_LIST": {
        return{
            ...state,
            modelList:{}
        }
    }
    }
    return state
}
