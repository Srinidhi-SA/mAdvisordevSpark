const default_updatedSubSetting = {
  "measureColumnFilters": [],
  "dimensionColumnFilters": [],
  "timeDimensionColumnFilters": []
}
export default function reducer(state = {
  dataList: {},
  selectedDataSet: "",
  current_page: 1,
  dataPreview: null, 
  allDataSets: {},
  allUserList:{},
  dataPreviewFlag: false,
  selectedAnalysis: [],
  selectedVariablesCount: 0,
  signalMeta: {},
  curUrl: "",
  editmodelFlag:false,
  dataUploadLoaderModal: false,
  dULoaderValue: -1,
  data_search_element: "",
  dataSetMeasures: [],
  dataSetDimensions: [],
  dataSetTimeDimensions: [],
  CopyOfMeasures: [],
  CopyOfDimension: [],
  CopyTimeDimension: [],
  measureAllChecked: true,
  measureChecked: [],
  dimensionAllChecked: true,
  dimensionChecked: [],
  dateTimeChecked: [],
  dataLoaderText: "Preparing data for loading",
  dataSetAnalysisList: {},
  dataSetPrevAnalysisList:{},
  dimensionSubLevel: [],
  updatedSubSetting: default_updatedSubSetting,
  subsettingDone: false,
  loading_message:[],
  dataLoadedText:[],
  dataTransformSettings:[],
  variableTypeListModal:false,
  selectedColSlug:"",
  data_sorton:"",
  data_sorttype:"",
  dataSetColumnRemoveValues:[],
  dataSetColumnReplaceValues:[],
  dataSetSelectAllAnalysis:false,
  isUpdate:false,
  latestDatasets:{},
  advancedAnalysisAssociation:true,
  advancedAnalysisInfluencer:true,
  advancedAnalysisPrediction:true,
  advancedAnalysisPerformance:true,
  createScoreShowVariables:false,
  dataTypeChangedTo:{},
  missingValueTreatment:{},
  outlierRemoval:{},
  featureEngineering:{},
  selectedVariables : {},
  checkedAll:true,
  checked:true,
  removeDuplicateObservations :{},
  duplicateObservations: false,
  showBinsLevelsTransformModal:false,
  selectedBinsOrLevelsTab:"Bins",
  selectedItem:{},
  selectedButton:"",
  shareItem:{},
  shareItemSlug:"",
  shareItemType:"",
  isNoOfBinsEnabled:false,
  shareModelShow:false,
  dtModelShow:false,
  dtRule: "",
  dtData: {},
  dtPath:[],
  dtName:"",
  isSpecifyIntervalsEnabled:true,
  convertUsingBin: "false",
  modelEditconfig:"",
  topLevelData:{},
  tensorValidateFlag: false,
  pytorchValidateFlag: false,
  createSigLoaderFlag: false,
  metaDataLoaderidxVal:0,
  metaDataLoaderidx:0,
  varibleSelectionBackFlag:false,
  scoreName:"",
  activeColSlug:"",
  paginationFlag:false,
  alreadyUpdated:false,
  measureColSelected:{},
  dimensionColSelected:{},
  datetimeColSelected:{},
}, action) {

  switch (action.type) {
    case "DATA_LIST":
      {
        return {
          ...state,
          dataList: action.data,
          latestDatasets:action.latestDatasets,
          current_page: action.current_page
        }
      }
      break;  
      case "CLEAR_DATA_LIST":{
        return{
          ...state,
          dataList:{}
        }
      }
      break;
      case "MODEL_EDIT_CONFIG":
      {
        return {
          ...state,
          modelEditconfig: action.doc,
          
         
        }
      }
      break;
      case "TENSOR_VALIDATE_FLAG":
          {
            return {
              ...state,
              tensorValidateFlag: action.flag,
            }
          }
          break;
          case "PYTORCH_VALIDATE_FLAG":
            {
              return {
                ...state,
                pytorchValidateFlag: action.flag,
              }
            }
            break;

    case "DATA_LIST_ERROR":
      {
        throw new Error("Unable to fetch data list!!");
      }
      break;
    case "DATA_PREVIEW":
      {
        return {
          ...state,
          dataPreview: action.dataPreview,
          dataPreviewFlag: true,
          selectedDataSet: action.slug,
          subsettingDone: false,
          dataTransformSettings:action.dataPreview.meta_data.uiMetaData.transformation_settings.existingColumns,
        }
      }
      break; 
      case "DATA_PREVIEW_ONLOAD":
      {
        return {
          ...state,
          dataPreview: action.dataPreview,
          dataPreviewFlag: false,
          selectedDataSet: action.slug,
          subsettingDone: false,
          dataTransformSettings:action.dataPreview.meta_data.uiMetaData.transformation_settings.existingColumns,
        }
      }
      break;
      case "DATA_PREVIEW_AUTOML":
      {
        return {
          ...state,
          dataPreview: action.dataPreview,
          dataPreviewFlag: true,
          selectedDataSet: action.slug,
        }
      }
      break;


    case "DATA_PREVIEW_FOR_LOADER":
      {
        return {
          ...state,
          dataPreview: action.dataPreview,
          selectedDataSet: action.slug

        }
      }
      break;

    case "DATA_PREVIEW_ERROR":
      {
        throw new Error("Fetching of Data failed!!");
      }
      break;
    case "DATA_ALL_LIST":
      {
        return {
          ...state,
          allDataSets: action.data,
        }
      }
      break;
    case "DATA_ALL_LIST_ERROR":
      {
        throw new Error("Unable to fetch data list!!");
      }
      break;
      case "USERS_ALL_LIST":
      {
        return {
          ...state,
          allUserList: action.json,
        }
      }
      break;
    case "USERS_ALL_LIST_ERROR":
      {
        throw new Error("Unable to fetch data list!!");
      }
      break;
      case "SHARE_MODAL_SHOW":
      {
        return {
          ...state,
          shareModelShow: true,
          shareItem:action.shareItem,
          shareItemSlug:action.slug,
          shareItemType:action.itemType,
        }
      }
      break;
      case "DT_MODAL_SHOW":
        {
          return {
            ...state,
            dtModelShow: true,
            dtRule: action.rule,
            dtPath: action.path,
            dtName:action.name
          }
        }
        break;
      case "SET_EDIT_MODEL":
      {
        return {
          ...state,
          editmodelFlag:action.flag
        }
      }
      break;
  
      case "SHARE_MODAL_HIDE":
      {
        return {
          ...state,
          shareModelShow: false
        }
      }
      break;
      case "DT_MODAL_HIDE":
        {
          return {
            ...state,
            dtModelShow: false
          }
        }
        break;
    case "SELECTED_ANALYSIS_TYPE":
      {
        return {
          ...state,
          selectedAnalysis: state.selectedAnalysis.concat(action.selectedAnalysis)
        }
      }
      break;
    case "UNSELECT_ANALYSIS_TYPE":
      {
        return {
          ...state,
          selectedAnalysis: state.selectedAnalysis.filter(item => action.selectedAnalysis !== item)
        }
      }
      break;


    case "SHOW_DATA_PREVIEW":
      {
        return {
          ...state,
          dataPreviewFlag: true
        }
      }
      break;
    case "HIDE_DATA_PREVIEW":
      {
        return {
          ...state,
          dataPreviewFlag: false
        }
      }
      break;

    case "STORE_SIGNAL_META":
      {
        return {
          ...state,
          signalMeta: action.signalMeta,
          curUrl: action.curUrl
        }
      }
      break;
    case "SELECTED_DATASET":
      {
        return {
          ...state,
          selectedDataSet: action.dataset
        }
      }
      break;
    case "RESET_VARIABLES":
      {
        return {
          ...state,
          dataSetMeasures: [],
          dataSetDimensions: [],
          dataSetTimeDimensions: [],
          CopyOfMeasures: [],
          CopyOfDimension: [],
          CopyTimeDimension: [],
          measureAllChecked:action.selectChk,
          dimensionAllChecked:action.selectChk,


        }
      }
      break;

    case "SHOW_DATA_PREVIEW":
      {
        return {
          ...state,
          dataPreviewFlag: true
        }
      }
      break;
    case "DATA_UPLOAD_LOADER":
      {
        return {
          ...state,
          dataUploadLoaderModal: true
        }
      }
      break;
    case "HIDE_DATA_UPLOAD_LOADER":
      {
        return {
          ...state,
          dataUploadLoaderModal: false
        }
      }
      break;
    case "DATA_UPLOAD_LOADER_VALUE":
      {
        return {
          ...state,
          dULoaderValue: action.value
        }
      }
      break;
    case "CLEAR_DATA_PREVIEW":
      {
        return {
          ...state,
          dataPreview: {},
          dataPreviewFlag: false,
          selectedDataSet: "",
          dataLoaderText:"Preparing data for loading",
          dULoaderValue: -1,
          loading_message:[]
        }
      }
      break;
    case "SEARCH_DATA":
      {
        return {
          ...state,
          data_search_element: action.search_element
        }
      }
      break;
    case "DATASET_VARIABLES":
      {
        return {
          ...state,
          dataSetMeasures: action.measures,
          dataSetDimensions: action.dimensions,
          dataSetTimeDimensions: action.timeDimensions,
          CopyOfMeasures: action.measures,
          CopyOfDimension: action.dimensions,
          CopyTimeDimension: action.timeDimensions,
          dataSetAnalysisList: action.possibleAnalysisList,
          dataSetPrevAnalysisList:action.prevAnalysisList,
          selectedVariablesCount:action.count,
          isUpdate:action.flag
        }
      }
      break;
    case "IS_VARIABLE_SELECTION_UPDATE":
    {
      return {
        ...state,
        isUpdate:action.flag
      }
    }
    break;
    case "SEARCH_MEASURE":
      {
        return {
          ...state,
          dataSetMeasures: state.CopyOfMeasures.filter((item) => item.name.toLowerCase().includes(action.name.toLowerCase()))
        }
      }
      break;
    case "SORT_MEASURE":
      {
        return {
          ...state,
          dataSetMeasures: action.measures,
          CopyOfMeasures: action.measures,
          //measureChecked: action.checkBoxList
        }
      }
      break;

    case "SORT_DIMENSION":
      {
        return {
          ...state,
          dataSetDimensions: action.dimensions,
          CopyOfDimension: action.dimensions,
         // dimensionChecked: action.checkBoxList1
        }
      }
      break;

    case "SORT_TIMEDIMENSION":
      {
        return {
          ...state,
          dataSetTimeDimensions: action.timedimensions,
          CopyTimeDimension: action.timedimensions,
         // dateTimeChecked: action.checkBoxList2
        }
      }
      break;

    case "SEARCH_DIMENSION":
      {
        return {
          ...state,
          dataSetDimensions: state.CopyOfDimension.filter((item) => item.name.toLowerCase().includes(action.name.toLowerCase()))
        }
      }
      break;

    case "SEARCH_TIMEDIMENSION":
      {
        return {
          ...state,
          dataSetTimeDimensions: state.CopyTimeDimension.filter((item) => item.name.toLowerCase().includes(action.name.toLowerCase()))
        }
      }
      break;

    case "UPADTE_VARIABLES_LIST":
    {
        return {
            ...state,
            dataSetMeasures: action.measures,
            dataSetDimensions: action.dimensions,
            dataSetTimeDimensions: action.timeDimensions,
            dimensionAllChecked: action.dimFlag,
            measureAllChecked: action.meaFlag,
            selectedVariablesCount:action.count,
            CopyOfMeasures: action.measures,
            CopyOfDimension: action.dimensions,
            CopyTimeDimension: action.timeDimensions,

        }
    }
        break;
    case "UPDATE_SELECTED_VARIABLES":
    {
        return {
            ...state,
            selectedMeasures: action.selectedMeasures,
            selectedDimensions:action.selectedDimensions,
        }
    }
    break;
    case "UPDATE_ANALYSIS_LIST":
      {
        return {
          ...state,
          dataSetAnalysisList: action.renderList,
          dataSetPrevAnalysisList:action.prevAnalysisList,
        }
      }
      break;
    case "SAVE_UPDATE_ANALYSIS_LIST":
    {
      return {
        ...state,
        dataSetPrevAnalysisList:action.savedAnalysisList,
      }
    }
    break;
    case "CANCEL_UPDATE_ANALYSIS_LIST":
    {
      return {
        ...state,
        dataSetAnalysisList:action.prevAnalysisList,
      }
    }
    break;
    case "UNSELECTED_TREND_SUB_LIST":
      {
        return {
          ...state,
          selectedTrendSub: state.selectedTrendSub.filter(item => action.selectedTrendSub !== item)
        }
      }
      break;

    case "UPDATE_SUBSETTING":
      {
        return {
          ...state,
          updatedSubSetting: action.updatedSubSetting,
          subsettingDone: true
        }
      }
      break;
    case "SUBSETTED_DATASET":
      {
        return {
          ...state,
          updatedSubSetting: {
            "measureColumnFilters": [],
            "dimensionColumnFilters": [],
            "timeDimensionColumnFilters": []
          },
          subsettingDone: false,
          selectedDataSet: action.subsetRs.slug

        }
      }
      break;
    case "DATA_UPLOAD_LOADER_MSG":
    {
      return{
        ...state,
        dataLoaderText: action.message
      }
    }
    break;
    case "CHANGE_LOADING_MSG":
    {
      return {...state,
      loading_message:action.message}
    }
    break;
    case "DATA_LOADED_TEXT":{
      return {
      ...state,
      dataLoadedText : action.text
      }
    }
    break;
    case "CLEAR_LOADING_MSG":
    {
      return{
        ...state,
        loading_message:[],
        dULoaderValue:-1,
        dataLoaderText:"Preparing data for loading"
      }
    }
    break;
    case "UPDATE_VARIABLES_TYPES_MODAL":
    {
         return{
        	 ...state,
        	 variableTypeListModal:action.flag,
         }
    }
    break;
    case "DATASET_SELECTED_COLUMN_SLUG":
    {
    	 return{
        	 ...state,
        	 selectedColSlug:action.slug,
         }
    }
    break;
    case "SORT_DATA":{
    	return{
    		...state,
    		data_sorton:action.sorton,
    		data_sorttype:action.sorttype
    	}
    }
    break;

    case "DATA_VALIDATION_PREVIEW":
    {
      return {
        ...state,
        dataPreview: action.dataPreview,
        subsettingDone: action.isSubsetting,
        dataTransformSettings:action.dataPreview.meta_data.uiMetaData.transformation_settings.existingColumns,
      }
    }
    break;
    case "DATA_VALIDATION_REMOVE_VALUES":
    {
      return {
        ...state,
        dataSetColumnRemoveValues:action.removeValues,
      }
    }
    break;
    case "DATA_VALIDATION_REPLACE_VALUES":
    {
      return {
        ...state,
        dataSetColumnReplaceValues:action.replaceValues,
      }
    }
    break;
    case "DATA_SET_SELECT_ALL_ANALYSIS":
    {
      return {
        ...state,
        dataSetSelectAllAnalysis:action.flag,
      }
    }
    break;
    case "UPDATE_VARIABLES_COUNT":
    {
      return {
        ...state,
        selectedVariablesCount:action.count,
      }
    }
    break;
    case "MAKE_ALL_TRUE_OR_FALSE":
    {
      return{
        ...state,
        measureAllChecked:action.value,
        dimensionAllChecked:action.value
      }
    }
    break;
    case "UPDATE_ANALYSIS_LIST_SELECT_ALL":
    {
      return {
        ...state,
        dataSetAnalysisList: action.renderList,
        dataSetPrevAnalysisList:action.renderList,
        dataSetSelectAllAnalysis:action.flag,
      }
    }
    break;
    case "ADVANCE_ANALYSIS_ASSOCIATION":
    {
      return {
        ...state,
        advancedAnalysisAssociation: action.disble,
      }
    }
    break;
    case "ADVANCE_ANALYSIS_PREDICTION":
    {
      return {
        ...state,
        advancedAnalysisPrediction: action.disble,
      }
    }
    break;
    case "ADVANCE_ANALYSIS_PERFORMANCE":
    {
      return {
        ...state,
        advancedAnalysisPerformance: action.disble,
      }
    }
    break;
    case "ADVANCE_ANALYSIS_INFLUENCER":
    {
      return {
        ...state,
        advancedAnalysisInfluencer: action.disble,
      }
    }
    break;
    case "RESET_SUBSETTED_DATASET":
    {
      return {
        ...state,
        updatedSubSetting: {
          "measureColumnFilters": [],
          "dimensionColumnFilters": [],
          "timeDimensionColumnFilters": []
        },
        subsettingDone: false,
        selectedDataSet: action.slug

      }
    }
    break;
    case "UPDATE_VARAIABLE_SELECTION_ARRAY":
    {
      return {
        ...state,
        dataPreview: action.newDataPreview,
        createScoreShowVariables:action.flag
      }
    }
    break;
    case "MISSING_VALUE_TREATMENT":
    {
      var curmissingValueTreatment = state.missingValueTreatment;
      curmissingValueTreatment[action.colSlug] = {
        "treatment" : action.treatment,
        "name" : action.colName,
        "type" : action.colType
      };
      return {
        ...state,
        missingValueTreatment : curmissingValueTreatment
      }

    }
    break;
    case "OUTLIER_REMOVAL":
    {
      var curOutlierRemoval = state.outlierRemoval;
      curOutlierRemoval[action.colSlug] = {
        "treatment" : action.treatment,
        "name" : action.colName,
        "type" : action.colType
      };
      return {
        ...state,
        outlierRemoval : curOutlierRemoval
      }

    }
    break;
    case "VARIABLE_SELECTED":
    {
      var allSelectedVariables = state.selectedVariables;
      allSelectedVariables[action.colSlug] = action.selecteOrNot;
      return {
        ...state,
        selectedVariables : allSelectedVariables
      }

    }
    break;
    case "CLEAR_SELECTED_VARIABLES":
      {
        return{
          ...state,
          selectedVariables : {}
        }
      }
      break;

    case "CHECKED_ALL_SELECTED":
    {
      var check = action.selecteOrNot;
      return {
        ...state,
        checkedAll : check
      }

    }
    break;
    case "DATA_CLEANSING_CHECK_UPDATE":
      {
        return {
          ...state,
          dataPreview: {
            ...state.dataPreview,
            meta_data: {
              ...state.dataPreview.meta_data,
              scriptMetaData: {
                ...state.dataPreview.meta_data.scriptMetaData,
                columnData: state.dataPreview.meta_data.scriptMetaData.columnData.map((item, index) => ({
                  ...item,
                  checked: index === Number(action.index) ? action.checkedOrNot : item.checked, 
                }))
              }
            }
          },
        };
  
      }
      break;
    case "REMOVE_DUPLICATE_OBSERVATIONS":
    {
      return {
        ...state,
        removeDuplicateObservations : action.yesOrNo,
        duplicateObservations : action.yesOrNo,
      }
    }
    break;
    case "DATACLEANSING_DATA_TYPE_CHANGE":
    {
       var newDataPreview = state.dataPreview
       newDataPreview.meta_data.uiMetaData.columnDataUI = newDataPreview.meta_data.uiMetaData.columnDataUI.map(item => {
          if(item.slug == action.colSlug){
             item.columnType = action.newDataType;
          }
          return item;
       })
       newDataPreview.meta_data.scriptMetaData.columnData = newDataPreview.meta_data.scriptMetaData.columnData.map(item => {
          if(item.slug == action.colSlug){
             item.columnType = action.newDataType;
          }
          return item;
       })
       // Clear missing value treatment
       var curMissingValueTreatment = state.missingValueTreatment
       delete(curMissingValueTreatment[action.colSlug]);
       // Clear outlier removal
       var curOutlierRemoval = state.outlierRemoval;
       delete(curOutlierRemoval[action.colSlug]);

       var curDataTypeChangedTo = state.dataTypeChangedTo;
       curDataTypeChangedTo[action.colSlug] = {
         "newColType" : action.newDataType
       };
       
       return {
          ...state,
          dataTypeChangedTo: curDataTypeChangedTo,
          dataPreview: newDataPreview,
          missingValueTreatment : curMissingValueTreatment,
          outlierRemoval : curOutlierRemoval
        }
      }
    break;

    case "SHOW_BINS_LEVELS_TRANSFORM_MODAL":{
      return{
        ...state,
        showBinsLevelsTransformModal : action.flag,
        selectedItem : action.item,
        selectedButton : action.btn
      }
    }
    break;
    case "BINS_OR_LEVELS":
    {
      return {
        ...state,
        selectedBinsOrLevelsTab: action.selectedBinsOrLevelsTab
      }
    }
    break;

    case "NUM_OF_BINS_SPECIFY_INTERVALS":
    {
      return {
        ...state,
        isNoOfBinsEnabled: action.isNoOfBinsEnabled,
        isSpecifyIntervalsEnabled: action.isSpecifyIntervalsEnabled
      }
    }
    break;

    case "FE_SAVE_TOP_LEVEL_DATA":
    {
      return {
        ...state,
        topLevelData: {"yesNoValue": action.yesNoValue, "numberOfBins" : action.numberOfBins},
        convertUsingBin: action.yesNoValue
      }
    }
    break;

    case "CLEAR_DATACLEANSING":
    {
      return{
        ...state,
        missingValueTreatment:{},
        outlierRemoval:{},
        removeDuplicateObservations :{},
        duplicateObservations : false,

      }
      
    }
    break;

    case "CLEAR_FEATUREENGINEERING":
    {
      return {
        ...state,
        featureEngineering:{},
        topLevelData:{}
      }
    }
    break;

    case "SAVE_BIN_LEVEL_TRANSFORMATION_DATA":
    {
      var curFeData = state.featureEngineering
      var curSlugData = curFeData[action.coloumnSlug];
      if(curSlugData == undefined){
        curSlugData = {}
      }
      curSlugData[action.actionType] = action.userData;
      curFeData[action.coloumnSlug] = curSlugData;
      return{
        ...state,
        featureEngineering : curFeData
      }
    }
    break;

    case "SPECIFY_INTERVALS_ENABLED":
    {
      return {
        ...state,
        isSpecifyIntervalsEnabled: action.isSpecifyIntervalsEnabled
      }
    }
    break;
    case "SET_CREATE_SIG_LOADER_FLAG":{
      return {
        ...state,
        createSigLoaderFlag : action.flag
      }
    }
    break;
    case "SET_VARIABLE_SELECTION_BACK":{
      return {
        ...state,
        varibleSelectionBackFlag : action.flag,
      }
    }
    break;
    case "SAVE_SCORE_NAME":{
      return {
        ...state,
        scoreName : action.value
      }
    }
    break;
    case "METADATA_LOADER_IDX_VAL":{
      return{
        ...state,
        metaDataLoaderidxVal : action.idxVal
      }
    }
    break;
    case "METADATA_LOADER_IDX":{
      return{
        ...state,
        metaDataLoaderidx : action.idx
      }
    }
    break;
    case "CLEAR_METADATA_LOADER_VALUES":{
      return {
        ...state,
        metaDataLoaderidxVal:0,
        metaDataLoaderidx:0,
      }
    }
    break;
    case "ACTIVE_COL_SLUG":{
      return{
        ...state,
        activeColSlug:action.slug
      }
    }
    break;
    case "PAGINATION_FLAG":{
      return{
        ...state,
        paginationFlag:action.flag
      }
    }
    break;
    case "CLEAR_SUBSET":{
      return{
        ...state,
        alreadyUpdated:false,
        measureColSelected:{},
        dimensionColSelected:{},
        datetimeColSelected:{},
        updatedSubSetting: {
          "measureColumnFilters": [],
          "dimensionColumnFilters": [],
          "timeDimensionColumnFilters": []
        },
        activeColSlug:"",
      }
    }
    break;
    case "ALREADY_UPDATED":{
      return{
        ...state,
        alreadyUpdated : action.flag
      }
    }
    break;
    case "CUR_MEASURE_COL":{
      let curMeasureCol = state.measureColSelected
      curMeasureCol[action.name] = action.value
      return{
        ...state,
        measureColSelected : curMeasureCol
      }
    }
    break;
    case "CUR_DIMENSION_COL":{
      let curDimensionCol = state.dimensionColSelected
      curDimensionCol[action.name] = action.value
      return{
        ...state,
        dimensionColSelected : curDimensionCol
      }
    }
    break;
    case "CUR_DATETIME_COL":{
      let curDatetimeCol = state.datetimeColSelected
      curDatetimeCol[action.name] = action.value
      return{
        ...state,
        datetimeColSelected : curDatetimeCol
      }
    }
    break;
    case "SEL_MEASURE_COL":{
      let cMin = state.updatedSubSetting.measureColumnFilters.filter(i=>i.colname===action.name)[0].lowerBound
      let cMax = state.updatedSubSetting.measureColumnFilters.filter(i=>i.colname===action.name)[0].upperBound
      let measure = state.measureColSelected
      measure["curMin"] = cMin
      measure["curMax"] = cMax
      return{
        ...state,
        measureColSelected : measure
      }
    }
    break;
    case "SEL_DIMENSION_COL":{
      let value = state.updatedSubSetting.dimensionColumnFilters.filter(i=>i.colname===action.name)[0].values
      let dimension = state.dimensionColSelected
      dimension["selectedDimensionList"] = value
      dimension["curDimensionList"] = value
      return{
        ...state,
        dimensionColSelected : dimension
      }
    }
    break;
    case "SEL_DATETIME_COL":{
      let lB = state.updatedSubSetting.timeDimensionColumnFilters.filter(i=>i.colname===action.name)[0].lowerBound
      let uB = state.updatedSubSetting.timeDimensionColumnFilters.filter(i=>i.colname===action.name)[0].upperBound
      let datetime = state.datetimeColSelected
      datetime["curstartDate"] = lB
      datetime["curendDate"] = uB
      return{
        ...state,
        datetimeColSelected : datetime
      }
    }
    break;

    case "SELECT_ALL_DIM_VAL":{
      let curDim = state.dimensionColSelected
      if(action.flag){
        curDim["selectedDimensionList"] = Object.keys(curDim["dimensionList"]);
      }else{
        curDim["selectedDimensionList"] = [];
      }
      return{
        ...state,
        dimensionColSelected : curDim
      }
    }
    break;
    case "SELECT_DIM_VAL":{
      let curDim = state.dimensionColSelected
      if(!action.flag){
        const index = curDim["selectedDimensionList"].indexOf(action.val);
        if(index > -1){
          curDim["selectedDimensionList"].splice(index, 1);
        }
      }else{
          curDim["selectedDimensionList"].push(action.val)
      }
      return{
        ...state,
        dimensionColSelected : curDim
      }
    }
    break;
  }
  return state
}
