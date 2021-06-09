import React from "react";
import {API,STATIC_URL} from "../helpers/env";
import {CSLOADERPERVALUE,LOADERMAXPERVALUE,DEFAULTINTERVAL,PERPAGE,SUCCESS,FAILED,getUserDetailsOrRestart,DIMENSION,
    MEASURE,SET_VARIABLE,SET_POLARITY,DYNAMICLOADERINTERVAL,UNIQUE_IDENTIFIER,handleJobProcessing,statusMessages} from "../helpers/helper";
import store from "../store";
import {closeCsLoaderModal, updateCsLoaderValue, updateCsLoaderMsg} from "./createSignalActions";
import renderHTML from 'react-render-html';
import Dialog from 'react-bootstrap-dialog'
import {showLoading, hideLoading} from 'react-redux-loading-bar'
import {updateStoreVariables,updateSelectAllAnlysis,hideDataPreview,updateTargetAnalysisList,getTotalVariablesSelected, paginationFlag} from './dataActions';

var createSignalInterval = null;
var refreshSignalInterval = null;

function getHeader(token) {
  return {'Authorization': token, 'Content-Type': 'application/json'};
}
export function checkIfTrendIsSelected() {
  var totalAnalysisList = store.getState().datasets.dataSetAnalysisList;
  var analysisList = [];
  var trendIsChecked = false;
  if (store.getState().signals.getVarType == MEASURE) {
    analysisList = totalAnalysisList.measures.analysis;
  } else {
    analysisList = totalAnalysisList.dimensions.analysis;
  }

  for (var i = 0; i < analysisList.length; i++) {
    if (analysisList[i].name == "trend") {
      if (analysisList[i].status) {
        trendIsChecked = true;
      }
      break;
    }
  }
  return trendIsChecked;

}

export function checkIfDateTimeIsSelected(){
    var dataSetTimeDimensions = store.getState().datasets.dataSetTimeDimensions;
    var flag = dataSetTimeDimensions.find(function(element) {
        return element.selected  == true;
      });
    return flag;
}

export function createSignal(metaData) {
  return (dispatch) => {
    dispatch(hideDataPreview())
    return fetchCreateSignal(metaData,dispatch).then(([response, json]) => {
      if (response.status === 200) {
        dispatch(fetchCreateSignalSuccess(json, dispatch))
      } else {
        dispatch(fetchCreateSignalError(json))
        dispatch(closeCsLoaderModal())
        dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
      }
    }).catch(function(error) {
      bootbox.alert("Connection lost. Please try again later.")
      dispatch(closeCsLoaderModal())
      dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
      clearInterval(createSignalInterval);
    });
  }

}

function fetchCreateSignal(metaData) {
 return fetch(API + '/api/signals/', {
    method: 'POST',
    headers: getHeader(getUserDetailsOrRestart.get().userToken),
    body: JSON.stringify(metaData)
  }).then(response => Promise.all([response, response.json()]));
}

export function checkAnalysisIsChecked(){
    var isChecked = false;
     $("#analysisList").find("input:checkbox").each(function(){
         if(this.checked){
             isChecked = true;
             return false;
         }
     });
     return isChecked;
 }
export function triggerSignalAnalysis(signalData,percentage,message){
    return (dispatch) => {
        dispatch(updateCsLoaderValue(percentage));
        dispatch(updateCsLoaderMsg(message));
        fetchCreateSignalSuccess(signalData,dispatch);
        dispatch(assignSignalData(signalData));
    }
}
export function fetchCreateSignalSuccess(signalData, dispatch) {
  let msg = store.getState().signals.loaderText
  let loaderVal = store.getState().signals.createSignalLoaderValue
  if (signalData.hasOwnProperty("proceed_for_loading") && !signalData.proceed_for_loading) {
    msg = "Your signal will be created in background...";
    dispatch(updateCsLoaderMsg(msg));
    setTimeout(function() {
      dispatch(closeCsLoaderModal())
      dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
    }, DYNAMICLOADERINTERVAL);

  } else {
    createSignalInterval = setInterval(function() {
      let loading_message = store.getState().signals.loading_message
      dispatch(getSignalAnalysis(getUserDetailsOrRestart.get().userToken, signalData.slug));
      if (store.getState().signals.createSignalLoaderValue < LOADERMAXPERVALUE) {
        if (loading_message && loading_message.length > 0) {
          loaderVal = loading_message[loading_message.length - 1].globalCompletionPercentage
        }
        if(loaderVal!=-1 && store.getState().signals.sigLoaderidxVal!=0){
          dispatch(updateSignalIndex(store.getState().signals.sigLoaderidxVal))
        }
        dispatch(updateSignalIndexValue(loading_message.length));
        dispatch(updateCsLoaderValue(loaderVal));
      } else {
        dispatch(clearSignalLoaderValues())
        dispatch(clearLoadingMsg())
      }

    }, DEFAULTINTERVAL);
  }

  return {type: "CREATE_SUCCESS", signalData}
}
function updateSignalIndexValue(idxVal) {
  return {
    type: "SIGNAL_LOADER_IDX_VAL",idxVal
  }  
}
function updateSignalIndex(idx) {
  return {
    type: "SIGNAL_LOADER_IDX",idx
  }  
}
export function clearSignalLoaderValues() {
  return {
    type: "CLEAR_SIGNAL_LOADER_VALUES"
  }
}
export function clearCreateSignalInterval() {
  clearInterval(createSignalInterval);
}
export function assignSignalData(signalData) {
  return {type: "CREATE_SUCCESS", signalData}
}

function fetchCreateSignalError(json) {
  return {type: "CREATE_ERROR", json}
}

export function getList(token, pageNo) {
  return (dispatch) => {
    return fetchPosts(token, pageNo,dispatch).then(([response, json]) => {
      if (response.status === 200) {
        dispatch(hideLoading())
        dispatch(paginationFlag(false))
        dispatch(fetchPostsSuccess(json))
      } else {
        dispatch(fetchPostsError(json))
        dispatch(hideLoading())
      }
    })
  }
}

function fetchPosts(token, pageNo) {
  let search_element = store.getState().signals.signal_search_element;
  let signal_sorton = store.getState().signals.signal_sorton;
  let signal_sorttype = store.getState().signals.signal_sorttype;
  if (signal_sorttype == 'asc')
    signal_sorttype = ""
  else if (signal_sorttype == 'desc')
    signal_sorttype = "-"
      return fetch(API + '/api/signals/?name=' + search_element + '&sorted_by=' + signal_sorton + '&ordering=' + signal_sorttype + '&page_number=' + pageNo + '&page_size=' + PERPAGE + '', {
        method: 'get',
        headers: getHeader(token)
      }).then(response => Promise.all([response, response.json()]));
}

export function refreshSignals() {
  return (dispatch) => {
    if(refreshSignalInterval != null)
    clearInterval(refreshSignalInterval);
    refreshSignalInterval = setInterval(function() {
      var pageNo = window.location.href.split("=").pop();
      if (isNaN(pageNo))
        pageNo = 1;
      let signalLst = store.getState().signals.signalList.data
      if(window.location.pathname == "/signals" && signalLst!=undefined && signalLst.filter(i=> (i.status!="SUCCESS" && i.status!="FAILED" && i.completed_percentage!=100) ).length != 0 )  
        dispatch(getList(getUserDetailsOrRestart.get().userToken, parseInt(pageNo)));
      }
    , DEFAULTINTERVAL);
  }
}
function fetchPostsSuccess(signalList) {
  var current_page = signalList.current_page;
  var latestSignals = signalList.top_3;
  return {type: "SIGNAL_LIST", signalList,latestSignals, current_page}
}

function fetchPostsError(json) {
  return {type: "SIGNAL_LIST_ERROR", json}
}

export function getSignalAnalysis(token, errandId) {
  return (dispatch) => {
    return fetchPosts_analysis(token, errandId).then(([response, json]) => {
      if (response.status === 200){
        if(json.message != "failed")
        dispatch(fetchPostsSuccess_analysis(json, errandId, dispatch))
        else
        window.history.back();
      } else {
        dispatch(fetchPostsError_analysis(json));
        dispatch(closeCsLoaderModal())
        dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
      }
    })
  }
}

export function getAlgoAnalysis(token, errandId) {
  return (dispatch) => {
    return fetchAlgos_analysis(token, errandId).then(([response, json]) => {
      if (response.status === 200) {
        dispatch(fetchAlgosSuccess_analysis(json, errandId, dispatch))
      } else {
        dispatch(fetchAlgosError_analysis(json));
      }
    })
  }
}

function fetchAlgos_analysis(token, errandId) {
  return fetch(
  API + '/api/trainalgomapping/' + errandId + "/" ,{
    method: 'get',
    headers: {
      'Authorization': token,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => Promise.all([response, response.json()])).catch(function(error) {
      bootbox.alert(statusMessages("error","Something went wrong. Please try again later.","small_mascot"))
  });

}


function fetchPosts_analysis(token, errandId) {
  return fetch(API + '/api/signals/' + errandId + "/", {
    method: 'get',
    headers: {
      'Authorization': token,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => Promise.all([response, response.json()])).catch(function() {
      bootbox.alert(statusMessages("error","Something went wrong. Please try again later.","small_mascot"))
  });

}

function fetchPostsSuccess_analysis(signalAnalysis, errandId, dispatch) {
  if(signalAnalysis.status == SUCCESS && (signalAnalysis.data.listOfCards === undefined && signalAnalysis.data.listOfNodes === undefined)){
    bootbox.dialog({
            message:"Unable to fetch signal summary, try creating again.",
            buttons: {
                'confirm': {
                    label: 'Ok',
                    callback:function(){
                        window.location.pathname = "/signals"
                    }
                },
            },
          });
  }else if(signalAnalysis.status == SUCCESS) {
    if(store.getState().signals.createSignalLoaderModal && signalAnalysis.message!=null && signalAnalysis.message.length>0){
      document.getElementsByClassName("sigProgress")[0].innerHTML = (document.getElementsByClassName("sigProgress")[0].innerText === "In Progress")?"<h2 class="+"text-white"+">"+"100%"+"</h2>":"100%"
      $("#loadingMsgs")[0].innerHTML = "Step " + (signalAnalysis.message.length-3) + ": " + signalAnalysis.message[signalAnalysis.message.length-3].shortExplanation;
      $("#loadingMsgs1")[0].innerHTML ="Step " + (signalAnalysis.message.length-2) + ": " + signalAnalysis.message[signalAnalysis.message.length-2].shortExplanation;
      $("#loadingMsgs2")[0].innerHTML ="Step " + (signalAnalysis.message.length-1) + ": " + signalAnalysis.message[signalAnalysis.message.length-1].shortExplanation;
      $("#loadingMsgs1")[0].className = "modal-steps"
      $("#loadingMsgs2")[0].className = "modal-steps active"
    }
   setTimeout(()=>{
      clearInterval(createSignalInterval);
      dispatch(closeCsLoaderModal())
      dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
      dispatch(clearSignalLoaderValues())
      dispatch(clearLoadingMsg());
      dispatch(updateSignalAnalysis(signalAnalysis, errandId))
    },2000) 
  } 
  else if (signalAnalysis.status == FAILED || signalAnalysis.status == false) {
    bootbox.alert(statusMessages("error","The signal could not be created. Please check the dataset and try again.","small_mascot"))
    clearInterval(createSignalInterval);
    dispatch(closeCsLoaderModal())
    dispatch(updateCsLoaderValue(CSLOADERPERVALUE))
    dispatch(clearLoadingMsg())
  } else if (signalAnalysis.status == "INPROGRESS") {
    dispatch(dispatchSignalLoadingMsg(signalAnalysis));
  }
  if(signalAnalysis.status == SUCCESS && store.getState().signals.createSignalLoaderModal){
   return { type: "SIGNAL_ANALYSIS_ONLOAD"}
  }
  else{
   return {type: "SIGNAL_ANALYSIS", signalAnalysis, errandId}
  }
}

function updateSignalAnalysis(signalAnalysis,errandId){
  return {type: "SIGNAL_ANALYSIS", signalAnalysis, errandId}
}

function fetchAlgosSuccess_analysis(algoAnalysis, errandId) {
  return {type: "ALGO_ANALYSIS", algoAnalysis, errandId}
}

function fetchAlgosError_analysis(json) {
  return {type: "ALGO_ANALYSIS_ERROR", json}
}

function fetchPostsError_analysis(json) {
  return {type: "SIGNAL_ANALYSIS_ERROR", json}
}
export function setPossibleAnalysisList(varType,varText,varSlug) {
    if (varType == MEASURE) {
        $(".treatAsCategorical").removeClass("hidden")
        var isVarTypeChanged = checkIfDataTypeChanges(varSlug);
        if (isVarTypeChanged) {
            varType = DIMENSION;
            $(".treatAsCategorical").find('input[type=checkbox]').prop("checked", true);
        } else {
            $(".treatAsCategorical").find('input[type=checkbox]').prop("checked", false);
        }
    } else {
        $(".treatAsCategorical").find('input[type=checkbox]').prop("checked", false);
        $(".treatAsCategorical").addClass("hidden")
    }
    return {type: "SET_POSSIBLE_LIST", varType, varText, varSlug};
}

export function updateAdvanceSettings(event){
   var variableSelection = store.getState().datasets.dataPreview.meta_data.uiMetaData.varibaleSelectionArray;
   var selOption = event.target.childNodes[event.target.selectedIndex];
   var varType = selOption.getAttribute("data-dataType");
   var varText = selOption.text;
   var varSlug = selOption.getAttribute("name");
    return (dispatch) => {
        return triggerAdvanceSettingsAPI(variableSelection).then(([response, json]) =>{
            if(response.status === 200){
                dispatch(updateTargetAnalysisList(json));
                dispatch(setPossibleAnalysisList(varType,varText,varSlug));
                dispatch(updateSelectAllAnlysis(false));
            }
        })
    }
}

function triggerAdvanceSettingsAPI(variableSelection){
    return fetch(API+'/api/datasets/'+store.getState().datasets.selectedDataSet+'/advanced_settings_modification/',{
        method: 'put',
        body:JSON.stringify({
            variableSelection
        }),
        headers: getHeader(getUserDetailsOrRestart.get().userToken)
    }).then( response => Promise.all([response, response.json()]));
}

function updateTargetVariable(slug,array){
    for(var i=0;i<array.length;i++){
    if(array[i].slug == slug){
        array[i].targetColumn = !array[i].targetColumn;
        array[i].targetColSetVarAs = null;
         break;
    }
}
    return array;
}

function handleSelectAllFlag(array){
    var selectAllFlag = true;
    for(var i=0;i<array.length;i++){
       if(array[i].selected == false && array[i].targetColumn == false){
            selectAllFlag = false;
            return selectAllFlag;
        }
    }
    return selectAllFlag;
}
export function clearMeasureSearchIfTargetIsSelected(name){
    $("#measureSearch").val("");
    return {
        type: "SEARCH_MEASURE",
        name,
    }
}
export function clearDimensionSearchIfTargetIsSelected(name){
    $("#dimensionSearch").val("");
    return {
        type: "SEARCH_DIMENSION",
        name,
    }
}
export function hideTargetVariable(event,jobType){
    return (dispatch) => {
    var selOption = event.target.childNodes[event.target.selectedIndex];
    var colData = store.getState().datasets.dataPreview.meta_data.scriptMetaData.columnData;
    var varText = selOption.text;
    var varType = colData.filter(i=>i.name==varText)[0].actualColumnType;
    var varSlug = selOption.getAttribute("name");
    var prevVarSlug = store.getState().signals.selVarSlug;

    dispatch(clearMeasureSearchIfTargetIsSelected(""))
    dispatch(clearDimensionSearchIfTargetIsSelected(""))

    var dataSetMeasures = store.getState().datasets.dataSetMeasures.slice();
    var dataSetDimensions = store.getState().datasets.dataSetDimensions.slice();
    var dataSetTimeDimensions = store.getState().datasets.dataSetTimeDimensions.slice();
    var dimFlag =  store.getState().datasets.dimensionAllChecked;
    var meaFlag = store.getState().datasets.measureAllChecked;
    var count = store.getState().datasets.selectedVariablesCount;
    if(varType == "measure"){
        dataSetMeasures = updateTargetVariable(varSlug,dataSetMeasures);
        dataSetDimensions = updateTargetVariable(varSlug,dataSetDimensions);
        $("#measureSearch").val("");
    }else if(varType == "dimension"){
        dataSetDimensions = updateTargetVariable(varSlug,dataSetDimensions);
        dataSetMeasures = updateTargetVariable(varSlug,dataSetMeasures);
        $("#dimensionSearch").val("");
    }
    if(prevVarSlug != null){
        dataSetDimensions = updateTargetVariable(prevVarSlug,dataSetDimensions)
        dataSetMeasures = updateTargetVariable(prevVarSlug,dataSetMeasures)
    }

    dimFlag = handleSelectAllFlag(dataSetDimensions);
    meaFlag = handleSelectAllFlag(dataSetMeasures);

    dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
    count = getTotalVariablesSelected();
    dispatch(updateVariablesCount(count));
    if(jobType == "signals"){
        dispatch(updateAdvanceSettings(event));
    }

    }

}
export function updateVariablesCount(count){
    return {type: "UPDATE_VARIABLES_COUNT", count}
}
function checkIfDataTypeChanges(varSlug) {
  var transformSettings = store.getState().datasets.dataTransformSettings;
  var isVarTypeChanged = false
  for (var i = 0; i < transformSettings.length; i++) {
    if (transformSettings[i].slug == varSlug) {
      for (var j = 0; j < transformSettings[i].columnSetting.length; j++) {
        if (transformSettings[i].columnSetting[j].actionName == SET_VARIABLE) {
          for (var k = 0; k < transformSettings[i].columnSetting[j].listOfActions.length; k++) {
            if (transformSettings[i].columnSetting[j].listOfActions[k].name != "general_numeric") {
              if (transformSettings[i].columnSetting[j].listOfActions[k].status) {
                isVarTypeChanged = true;
                break;
              }
            }
          }
        }
      }
      break;
    }
  }
  return isVarTypeChanged;
}
function updateSetVarAs(colSlug){
    return (dispatch) => {
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var dataSetTimeDimensions = store.getState().datasets.CopyTimeDimension.slice();
        var dimFlag =  store.getState().datasets.dimensionAllChecked;
        var meaFlag = store.getState().datasets.measureAllChecked;
        var count = store.getState().datasets.selectedVariablesCount;
        for(var i=0;i<dataSetMeasures.length;i++){
            if(dataSetMeasures[i].slug == colSlug){
                if(dataSetMeasures[i].targetColSetVarAs == null){
                    dataSetMeasures[i].targetColSetVarAs = "percentage";
                    dataSetMeasures[i].columnType = "dimension";
                    break;
                }
                else{
                    dataSetMeasures[i].targetColSetVarAs = null;
                    break;
                }

            }
        }
        dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
    }
}
export function updateCategoricalVariables(colSlug) {
  return (dispatch) => {
        dispatch(updateSetVarAs(colSlug));

  }
}

export function changeSelectedVariableType(colSlug, colName, evt) {
  var varType = "dimension";
  var varText = colName;
  var varSlug = colSlug;
  if (evt.target.checked) {
    varType = "dimension";
    return {type: "SET_POSSIBLE_LIST", varType, varText, varSlug}
  } else {
    varType = "measure";
    return {type: "SET_POSSIBLE_LIST", varType, varText, varSlug}
  }

}
export function saveSignalName(sigName) {
  return {type: "SET_SIGNAL_NAME", sigName}
}

export function createcustomAnalysisDetails() {
  var transformSettings = store.getState().datasets.dataTransformSettings;
  var customAnalysisDetails = []
  var polarity = []
  var columnSettings = {}
  var uidColumn = {}
  for (var i = 0; i < transformSettings.length; i++) {
    for (var j = 0; j < transformSettings[i].columnSetting.length; j++) {
      if (transformSettings[i].columnSetting[j].actionName == SET_VARIABLE) {
        for (var k = 0; k < transformSettings[i].columnSetting[j].listOfActions.length; k++) {
          if (transformSettings[i].columnSetting[j].listOfActions[k].name != "general_numeric") {
            if (transformSettings[i].columnSetting[j].listOfActions[k].status) {
              customAnalysisDetails.push({"colName": transformSettings[i].name, "colSlug": transformSettings[i].slug, "treatAs": transformSettings[i].columnSetting[j].listOfActions[k].name})
            }
          }
        }
      } else if (transformSettings[i].columnSetting[j].actionName == SET_POLARITY) {
        for (var k = 0; k < transformSettings[i].columnSetting[j].listOfActions.length; k++) {
          if (transformSettings[i].columnSetting[j].listOfActions[k].status) {
            polarity.push({"colName": transformSettings[i].name, "colSlug": transformSettings[i].slug, "polarity": transformSettings[i].columnSetting[j].listOfActions[k].name})
          }

        }
      } else if (transformSettings[i].columnSetting[j].actionName == UNIQUE_IDENTIFIER) {
        uidColumn.colSlug = transformSettings[i].slug;
        uidColumn.colName = transformSettings[i].name;
      }
    }
  }
  return columnSettings = {
    "customAnalysisDetails": customAnalysisDetails,
    "polarity": polarity,
    "uidColumn": uidColumn
  };
}
export function showPredictions(predictionSelected) {
  return {type: "SEL_PREDICTION", predictionSelected}
}
export function showDepthPredictions(predictionSelected,dropDownName) {
  return {type: "SEL_DEPTH_PREDICTION", predictionSelected,dropDownName}
}
export function emptySignalAnalysis() {
  return {type: "SIGNAL_ANALYSIS_EMPTY"}
}

export function emptyAlgoAnalysis() {
  return {type: "ALGO_ANALYSIS_EMPTY"}
}

export function showDialogBox(slug,dialog,dispatch,evt){
    var labelTxt = evt.target.text;
	Dialog.setOptions({
		  defaultOkLabel: 'Yes',
		  defaultCancelLabel: 'No',
		})
	var body_msg=renderHTML(statusMessages("warning","Are you sure you want to delete this Signal?","small_mascot"))
	dialog.show({
		  title: 'Delete Signal',
		  body: body_msg,
		  actions: [
		    Dialog.CancelAction(),
		    Dialog.OKAction(() => {
		        if(labelTxt.indexOf("Stop") != -1)dispatch(handleJobProcessing(slug));
		        else deleteSignal(slug,dialog,dispatch)
		    })
		  ],
		  bsSize: 'medium',
		  onHide: (dialogBox) => {
		    dialogBox.hide()
		  }
		});
}
export function handleDelete(slug,dialog,evt) {
	return (dispatch) => {
		showDialogBox(slug,dialog,dispatch,evt)
	}
}
function deleteSignal(slug, dialog, dispatch) {
  dispatch(showLoading());
  Dialog.resetOptions();
  return deleteSignalAPI(slug).then(([response, json]) => {
    if (response.status === 200) {
      dispatch(getList(getUserDetailsOrRestart.get().userToken, store.getState().signals.signalList.current_page));
      dispatch(hideLoading());
    } else {
      bootbox.alert(statusMessages("error","The card could not be deleted. Please try again later.","without_mascot"))
      dispatch(hideLoading());
    }
  })
}
function deleteSignalAPI(slug) {
  return fetch(API + '/api/signals/' + slug + '/', {
    method: 'put',
    headers: getHeader(getUserDetailsOrRestart.get().userToken),
    body: JSON.stringify({deleted: true})
  }).then(response => Promise.all([response, response.json()]));

}
export function storeSearchElement(search_element) {
  return {type: "SEARCH_SIGNAL", search_element}
}
export function storeSortElements(sorton, sorttype) {

  return {type: "SORT_SIGNAL", sorton, sorttype}
}

export function getAllSignalList() {
  return (dispatch) => {
    return fetchAllSignalList(getUserDetailsOrRestart.get().userToken).then(([response, json]) =>{
        if(response.status === 200){
            dispatch(fetchAllSignalSuccess(json))
        }else{
          dispatch(fetchAllSignalError(json))
        }
    })
  }
}
function fetchAllSignalList(token) {
  return fetch(API + '/api/signals/get_all_signals/', {
      method: 'get',
      headers: getHeader(token)
  }).then( response => Promise.all([response, response.json()]));
}

export function fetchAllSignalSuccess(doc){
  var data = ""
  if(doc.allSignalList[0]!= undefined){
      data = doc.allSignalList;
  }
  return {
      type: "ALL_SIGNAL_LIST",
      data,
  }
}
function fetchAllSignalError(json) {
  return {
      type: "ALL_SIGNAL_LIST_ERROR",
      json
  }
}

export function handleRename(slug, dialog, name) {
  return (dispatch) => {
    showRenameDialogBox(slug, dialog, dispatch, name)
  }
}
function showRenameDialogBox(slug, dialog, dispatch, name) {
  const customBody = (
  	<div className="row">
			<div className="col-md-4">
				<img src={STATIC_URL + "assets/images/alert_thinking.gif"} class="img-responsive" />
			</div>
			<div className="col-md-8">
			<div className="form-group">
			<label for="fl1" className="control-label">Enter a new name</label>
			<input className="form-control" id="idRenameSignal" type="text" defaultValue={name}/>
      <div className="text-danger" id="ErrorMsg"></div>
			</div>
			</div>
		</div>

  )

  dialog.show({
    title: 'Rename Signal',
    body: customBody,
    actions: [
      Dialog.CancelAction(), 
      Dialog.OKAction(() => {
        let letters = /^[0-9a-zA-Z\-_\s]+$/;
        var allSignalList=store.getState().signals.allSignalList;
        if($("#idRenameSignal").val()==""){
              document.getElementById("ErrorMsg").innerHTML = "Please enter a name to proceed..";
              showRenameDialogBox(slug, dialog, dispatch, name)
        }
        else if (!letters.test($("#idRenameSignal").val())){
              document.getElementById("ErrorMsg").innerHTML = "Please enter name in a correct format. It should not contain special characters @,#,$,%,!,&.";
              showRenameDialogBox(slug, dialog, dispatch, name)
        }
       else if(Object.values(allSignalList).map(i=>i.name.toLowerCase()).includes($("#idRenameSignal").val().toLowerCase())){
              document.getElementById("ErrorMsg").innerHTML = "Signal with same name already exists.";
              showRenameDialogBox(slug, dialog, dispatch, name)
        }else{
          renameSignal(slug, dialog, $("#idRenameSignal").val(), dispatch)
        }
      })
    ],
    bsSize: 'medium',
    onHide: (dialogBox) => {
      dialogBox.hide()
    }
  });
}

function renameSignal(slug, dialog, newName, dispatch) {
  dispatch(showLoading());
  Dialog.resetOptions();
  return renameSignalAPI(slug, newName).then(([response, json]) => {
    if (response.status === 200) {
      dispatch(getList(getUserDetailsOrRestart.get().userToken, store.getState().datasets.current_page));
      dispatch(hideLoading());
    } else {
      dialog.showAlert("Renaming unsuccessful. Please try again later.");
      dispatch(hideLoading());
    }
  })
}
function renameSignalAPI(slug, newName) {
  return fetch(API + '/api/signals/' + slug + '/', {
    method: 'put',
    headers: getHeader(getUserDetailsOrRestart.get().userToken),
    body: JSON.stringify({name: newName})
  }).then(response => Promise.all([response, response.json()]));

}
export function advanceSettingsModal(flag) {
  return {type: "ADVANCE_SETTINGS_MODAL", flag}
}

function dispatchSignalLoadingMsg(signalAnalysis) {
  let message = signalAnalysis.message
  return {type: "CHANGE_LOADING_MSG", message}
}
export function clearLoadingMsg() {
  return {type: "CLEAR_LOADING_MSG"}
}
export function pickToggleValue(id,flag){
  return {type: "TOGGLE_VALUES", id,flag}
}
export function clearToggleValue(){
  return {type: "CLEAR_TOGGLE_VALUES"}
}
export function handleDecisionTreeTable(evt) {
  var probability = "";
  var probabilityCond = true;
  var noDataFlag = true;
  var selPred = ""
  //triggered when probability block is clicked to select and unselect
  if (evt) {
    selectProbabilityBlock(evt);
  }
  if ($(".pred_disp_block").find(".selected").length > 0)
    probability = $(".pred_disp_block").find(".selected")[0].innerText.toLowerCase();

  $(".popupDecisionTreeTable").find("tr").each(function() {
    if (this.rowIndex != 0) {
      if (probability)
        probabilityCond = probability.indexOf(this.cells[4].innerText.toLowerCase()) != -1;
        selPred = (this.parentElement.parentElement.className.includes("DepthOfTree"))?
          store.getState().signals.selectedDepthPrediction[this.parentElement.parentElement.classList[3]]
          :store.getState().signals.selectedPrediction;
      if((this.cells[2].innerText.toLowerCase().trim() === selPred.toLowerCase().trim()) && probabilityCond) {
        $(this).removeClass("hidden");
        noDataFlag = false;
      } else {
        $(this).addClass("hidden");
      }
    }
  })
  if (noDataFlag) {
    $(".popupDecisionTreeTable").addClass("hidden");
  } else {
    $(".popupDecisionTreeTable").removeClass("hidden");
  }
}
export function handleTopPredictions() {
  var noDataFlag = true;
  var selPred = ""
  $(".topPredictions").find("tr").each(function() {
    selPred = (this.parentElement.parentElement.className.includes("DepthOfTree"))?
      store.getState().signals.selectedDepthPrediction[this.parentElement.parentElement.classList[3]]
      : store.getState().signals.selectedPrediction
    if (this.rowIndex != 0) {
      if (this.cells[2].innerText.toLowerCase().trim() == selPred.toLowerCase().trim()) {
        $(this).removeClass("hidden");
        noDataFlag = false;
      } else {
        $(this).addClass("hidden");
      }

    }
  })
  if (noDataFlag) {
    $(".topPredictions").addClass("hidden");
  } else {
    $(".topPredictions").removeClass("hidden");
  }
}
export function selectProbabilityBlock(evt) {
  $(".pred_disp_block").each(function() {
    if (!$(this).find("a").hasClass("selected")) {
      if ($(this).find("a")[0].innerText.toLowerCase().indexOf(evt.target.innerText.toLowerCase()) != -1) {
        $(this).find("a").addClass("selected");
      } else {
        $(this).find("a").removeClass("selected");
      }
    } else {
      $(this).find("a").removeClass("selected");
    }

  })

}
export function showZoomChart(flag, classId) {
  return {type: "ZOOM_CHART", flag, classId}
}

export function showChartData(flag, classId) {
  return {type: "CHART_DATA", flag, classId}
}

export function updateselectedL1(selectedL1){
  return{
    type:"SELECTED_L1",
    selectedL1
  }
}
export function resetSelectedTargetVariable(){
    var varType = null;
    var varText = null;
    var varSlug = null;
    return {type: "SET_POSSIBLE_LIST", varType, varText, varSlug}
}
export function clearSignalAnalysisBeforeLogout(){
  return {
    type:"CLEAR_SIGNAL_ANALYSIS_BEFORE_LOGOUT"
  }
}
export function fromVariableSelectionPage(flag){
  return {
      type: "FROM_VARIABLE_SELECTION_PAGE",flag
  }
}
export function clearSignalList(){
  return {
      type: "CLEAR_SIGNAL_LIST"
  }
}
export function setmmLoaderFlag(flag){
  return {
    type: "SET_MM_LOADER",flag
  }
}