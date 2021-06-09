export default function reducer(state = {
  signalList: {},
  allSignalList:{},
  signalAnalysis:{},
  signalAnalysisViewed:"",
  algoAnalysis:{},
  mmLoaderFlag:true,
  selectedAlgo:{},
  selectedSignal:{},
  newSignalShowModal:false,
  signalData:null,
  createSignalLoaderModal:false,
  createSignalLoaderValue:-1,
  current_page:1,
  urlPrefix:"/signals",
  signal_search_element:"",
  signal_sorton:null,
  signal_sorttype:null,
  loaderText:"Submitting for analysis",
  signalLoadedText:[],
  advanceSettingsModal:false,
  getVarType:null,
  getVarText:null,
  selVarSlug:null,
  setSigName:"",
  loading_message:[],
  viewChartFlag:false,
  chartClassId :"",
  viewChartDataFlag:false,
  chartDataClassId :"",
  selectedL1: "",
  latestSignals:{},
  toggleValues:{},
  fromVariableSelectionPage:false,
  sigLoaderidxVal:0,
  sigLoaderidx:0,
  selectedDepthPrediction:[],
}, action) {

  switch (action.type) {
    case "SIGNAL_LIST":
      {
        return {
          ...state,
          signalList: action.signalList,
          latestSignals:action.latestSignals,
          current_page: action.current_page
        }
      }
      break;
    case "CLEAR_SIGNAL_LIST":{
      return{
        ...state,
        signalList:{}
      }
    }
    case "SIGNAL_LIST_ERROR":
      {
        throw new Error("Unable to fetch signal list!!");
      }
      break;

    case "SIGNAL_ANALYSIS":
      {
        return {
          ...state,
          signalAnalysis: action.signalAnalysis.data,
          signalAnalysisViewed:action.signalAnalysis.viewed,
          selectedSignal: action.errandId,
          urlPrefix:"/signals",
          signalLoadedText:action.signalAnalysis.initial_messages,
        }
      }
      break;

      case "SIGNAL_ANALYSIS_ONLOAD":
      {
        return {
          ...state,
          signalAnalysis:"",
        }
      }
      break;
      case "ALGO_LIST_ERROR":
      {
        throw new Error("Unable to fetch algo list!!");
      }
      break;

      case "ALGO_ANALYSIS":
      {
        return {
          ...state,
          algoAnalysis: action.algoAnalysis,
          selectedAlgo: action.errandId,
          // urlPrefix: action.urlPrefix,
        }
      }
      break;
      case "SET_MM_LOADER":{
        return{
          ...state,
          mmLoaderFlag : action.flag
        }
      }
  

      case "ALGO_ANALYSIS_ERROR":
      {
        throw new Error("Unable to fetch algo list!!");
      }
      break; 


    case "SIGNAL_ANALYSIS_ERROR":
      {
        throw new Error("Unable to fetch signal list!!");
      }
      break;
    case "CREATE_SIGNAL_SHOW_MODAL":
      {
        return {
          ...state,
          newSignalShowModal: true
        }
      }
      break;

    case "CREATE_SIGNAL_HIDE_MODAL":
      {
        return {
          ...state,
          newSignalShowModal: false
        }
      }
      break;
    case "SIGNAL_LOADER_IDX_VAL": {
        return {
          ...state,
          sigLoaderidxVal : action.idxVal
        }
      }
      break;
    case "SIGNAL_LOADER_IDX": {
      return {
        ...state,
        sigLoaderidx : action.idx
      }
    }
    break;
    case "CLEAR_SIGNAL_LOADER_VALUES":{
      return {
        ...state,
        sigLoaderidxVal:0,
        sigLoaderidx:0,
      }
    }
    break;
    case "CREATE_SUCCESS":
      {
        return {
          ...state,
          signalData: action.signalData,
          loading_message:[],
          signalLoadedText:[]
        }
      }
      break;
    case "CREATE_ERROR":
      {
        throw new Error("Create Signal Failed!!");
      }
      break;
    case "SET_POSSIBLE_LIST":
      {
        return {
          ...state,
          getVarType: action.varType,
		  getVarText: action.varText,
		  selVarSlug:action.varSlug,
        }
      }
      break;
    case "SET_SIGNAL_NAME":{
      return{
        ...state,
        setSigName: action.sigName
      }
    }
    break;
    case "SEL_PREDICTION":
      {
        return {
          ...state,
          selectedPrediction: action.predictionSelected
        }
      }
      break;
      case "SEL_DEPTH_PREDICTION":{
        let curSelectedDepthPrediction = state.selectedDepthPrediction;
        curSelectedDepthPrediction[action.dropDownName] = action.predictionSelected
        return{
          ...state,
          selectedDepthPrediction : curSelectedDepthPrediction
        }
      }
      break;
    case "HIDE_CREATE_SIGNAL_LOADER":
      {
        return {
          ...state,
          createSignalLoaderModal: false
        }
      }
      break;
    case "SHOW_CREATE_SIGNAL_LOADER":
      {
        return {
          ...state,
          createSignalLoaderModal: true
        }
      }
      break;
    case "CREATE_SIGNAL_LOADER_VALUE":
      {
        return {
          ...state,
          createSignalLoaderValue: action.value
        }
      }
      break;
    case "SIGNAL_ANALYSIS_EMPTY":
      {
        return {
          ...state,
          signalAnalysis: {}
        }
      }
      break;

      case "ALGO_ANALYSIS_EMPTY":
      {
        return {
          ...state,
          algoAnalysis: {}
        }
      }
      break;

    case "ROBO_DATA_ANALYSIS":
      {
        return {
          ...state,
          signalAnalysis: action.roboData.data,
          urlPrefix: action.urlPrefix,
          selectedSignal: action.roboSlug
        }
      }
      break;
    case "SEARCH_SIGNAL":
    {
      return{
        ...state,
        signal_search_element:action.search_element
      }
    }
    break;

	case "SORT_SIGNAL":
	{
      return{
        ...state,
        signal_sorton:action.sorton,
		signal_sorttype:action.sorttype
      }
    }
    break;
	case "ADVANCE_SETTINGS_MODAL":
	{
		return{
			...state,
			advanceSettingsModal:action.flag
		}

	}
    break;
    case "CHANGE_LOADING_MSG":
    {
      return {...state,
      loading_message:action.message}
    }
    break;
    case "CLEAR_LOADING_MSG":
    {
      return{
        ...state,
        loading_message:[],
        createSignalLoaderValue:-1,
        loaderText:"Analyzing Target Variable"
      }
    }
    break;
    case "TOGGLE_VALUES":
      {
        var allToggleValues = state.toggleValues;
        allToggleValues[action.id] = action.flag;
        return {
          ...state,
          toggleValues : allToggleValues
        }      
      }
      break;
      case "CLEAR_TOGGLE_VALUES":
      {
        return {
          ...state,
          toggleValues : {}
        }      
      }
      break;
    case "CREATE_SIGNAL_LOADER_MSG":
      {
        return {
          ...state,
          loaderText: action.message
        }
      }
      break;
    case "ZOOM_CHART":
    {
        return {
            ...state,
            viewChartFlag: action.flag,
            chartClassId:action.classId,
          }
    }
    break;
  case "CHART_DATA":
  {
      return {
          ...state,
          viewChartDataFlag: action.flag,
          chartDataClassId:action.classId,
        }
  }
  break;
  case "SELECTED_L1":
  {
    return{
      ...state,
      selectedL1:action.selectedL1
    }
  }
  break;
  case "CLEAR_SIGNAL_ANALYSIS_BEFORE_LOGOUT":
  {
    return{
      ...state,
      signalAnalysis:{}
    }
  }
  break;
  case "FROM_VARIABLE_SELECTION_PAGE":{
    return{
      ...state,
      fromVariableSelectionPage:action.flag
    }
  }break;
  case "ALL_SIGNAL_LIST":
      {
        return {
          ...state,
          allSignalList: action.data,
        }
      }
      break;
      case "ALL_SIGNAL_LIST_ERROR":
      {
        throw new Error("Unable to fetch signal list!!");
      }
  }
  return state
}
