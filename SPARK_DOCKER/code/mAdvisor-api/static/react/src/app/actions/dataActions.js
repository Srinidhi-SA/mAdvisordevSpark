import React from "react";
import {API,STATIC_URL} from "../helpers/env";
import {PERPAGE,DULOADERPERVALUE,DEFAULTINTERVAL,SUCCESS,FAILED,getUserDetailsOrRestart,DEFAULTANALYSISVARIABLES,statusMessages} from "../helpers/helper";
import store from "../store";
import {dataUploadLoaderValue,clearLoadingMsg} from "./dataUploadActions";
import {closeAppsLoaderValue,getAppsStockList,openAppsLoaderValue,saveSelectedValuesForModel} from "./appActions";
import {resetSelectedTargetVariable,updateVariablesCount} from "./signalActions";
import renderHTML from 'react-render-html';
import Dialog from 'react-bootstrap-dialog';
import { showLoading, hideLoading } from 'react-redux-loading-bar';
import {RENAME,DELETE,REPLACE,DATA_TYPE,REMOVE,CURRENTVALUE,NEWVALUE,SET_VARIABLE,UNIQUE_IDENTIFIER,SET_POLARITY,handleJobProcessing,IGNORE_SUGGESTION} from "../helpers/helper";
import {notify} from 'react-notify-toast';

var refreshDatasetsInterval = null;

function getHeader(token){
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    };
}

export function refreshDatasets(){
    return (dispatch) => {
        if(refreshDatasetsInterval != null)
            clearInterval(refreshDatasetsInterval);
        refreshDatasetsInterval = setInterval(function() {
            var pageNo = window.location.href.split("=").pop();
            if(isNaN(pageNo)) pageNo = 1;
            let dataLst = store.getState().datasets.dataList.data
            if(window.location.pathname == "/data" && dataLst!=undefined && dataLst.filter(i=> (i.status!="SUCCESS" && i.status!="FAILED" && i.completed_percentage!=100) ).length != 0 ){
                dispatch(getDataList(parseInt(pageNo)));
            }
        },DEFAULTINTERVAL);
    }
}
export function getDataList(pageNo) {
	return (dispatch) => {
		return fetchDataList(pageNo,getUserDetailsOrRestart.get().userToken,dispatch).then(([response, json]) =>{
			if(response.status === 200){
                dispatch(hideLoading())
                dispatch(paginationFlag(false))
				dispatch(fetchDataSuccess(json))
			}else{
				dispatch(fetchDataError(json))
				dispatch(hideLoading())
			}
		})
	}
}

function fetchDataList(pageNo,token) {
	let search_element = store.getState().datasets.data_search_element;
	let data_sorton =  store.getState().datasets.data_sorton;
    let data_sorttype = store.getState().datasets.data_sorttype;
	if(data_sorttype=='asc')
		data_sorttype = ""
    else if(data_sorttype=='desc')
        data_sorttype="-"
    return fetch(API+'/api/datasets/?name='+search_element+'&sorted_by='+data_sorton+'&ordering='+data_sorttype+'&page_number='+pageNo+'&page_size='+PERPAGE+'',{
        method: 'get',
        headers: getHeader(token)
    }).then( response => Promise.all([response, response.json()]));
}

function fetchDataError(json) {
	return {
		type: "DATA_LIST_ERROR",
		json
	}
}
export function fetchDataSuccess(doc){
	var data = doc;
	var current_page =  doc.current_page
	var latestDatasets = doc.top_3;
	return {
		type: "DATA_LIST",
		data,latestDatasets,
		current_page,
	}
}

export function fetchModelEdit(slug) {
	return (dispatch) => {
		return fetchModelEditAPI(slug).then(([response, json]) =>{
			if(response.status === 200){
				dispatch(fetchModelEditAPISuccess(json))
			}
			else{
			bootbox.alert("something went wrong")
			}
		})
	}
}

export function fetchModelEditAPISuccess(doc){
	return {
        type: "MODEL_EDIT_CONFIG",
        doc
	}
}
export function fetchModelEditAPI(slug) {
	return fetch(API+'/api/trainer/'+slug+'/edit/',{
		method: 'get',
		headers: getHeader(getUserDetailsOrRestart.get().userToken)
	}).then( response => Promise.all([response, response.json()]));
}
export function getStockDataSetPreview(slug,interval) {
	return (dispatch) => {
		return fetchStockDataPreview(slug).then(([response, json]) =>{
			if(response.status === 200){
				dispatch(fetchDataPreviewSuccess(json,interval,dispatch))
                dispatch(setDataLoadedText(''));           
			}
			else{
				dispatch(hideDULoaderPopup());
				dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
				dispatch(fetchDataPreviewError(json))
			}
		})
	}
}
function fetchStockDataPreview(slug) {
	return fetch(API+'/api/stockdataset/'+slug+'/',{
		method: 'get',
		headers: getHeader(getUserDetailsOrRestart.get().userToken)
	}).then( response => Promise.all([response, response.json()]));
}
export function getDataSetPreview(slug,interval) {
    return (dispatch) => {
        return fetchDataPreview(slug,dispatch,interval).then(([response, json]) =>{
            if(response.status === 200){
                if(json.message && json.message == "failed"){
                    let myColor = { background: '#00998c', text: "#FFFFFF" };
                    notify.show("You are not authorized to view this content.", "custom", 2000,myColor);
                    setTimeout(function() {
                    window.location.pathname="/signals";
                    },2000);
                }else if(json.status==="SUCCESS" && (Object.keys(json.meta_data.scriptMetaData).length === 0 || json.meta_data.uiMetaData === null || json.meta_data.uiMetaData.columnDataUI===undefined)){
                    bootbox.dialog({
                        message:"Sorry, Unable to fetch data preview",
                        buttons: {
                            'confirm': {
                                label: 'Ok',
                                callback:function(){
                                    window.location.pathname = "/data";
                                }
                            },
                        },
                    });
                }
                else{
                dispatch(setCreateSignalLoaderFlag(false))
                dispatch(fetchDataPreviewSuccess(json,interval,dispatch))
                }
            }
            else{
                dispatch(hideDULoaderPopup());
                dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
                dispatch(fetchDataPreviewError(json))
            }
        });
    }
}


function fetchDataPreview(slug,dispatch,interval) {
    return fetch(API+'/api/datasets/'+slug+'/',{
        method: 'get',
        headers: getHeader(getUserDetailsOrRestart.get().userToken)
    }).then( response => Promise.all([response, response.json()])).catch(function(){

        dispatch(hideDULoaderPopup());
        clearInterval(interval);
        let msg=statusMessages("error","Unable to connect to server. Check your connection please try again.","small_mascot")
        bootbox.alert(msg)
    });
}
function fetchDataPreviewSuccess(dataPreview,interval,dispatch) {
    if(window.location.pathname != "/apps-stock-advisor/"){
        dataPreview.meta_data.scriptMetaData!=undefined && dataPreview.meta_data.scriptMetaData.columnData != undefined && dataPreview.meta_data.scriptMetaData.columnData.forEach(column => {
            column.checked = true;
        });
    }
    var slug = dataPreview.slug;
    var dataset = slug;
    if(window.location.pathname.includes("apps-stock-advisor-analyze") )
     var getStatus = dataPreview.meta_data_status;
    else
    var getStatus = dataPreview.status;
    if(getStatus == SUCCESS && store.getState().apps.appsLoaderModal==true && window.location.pathname.includes("stock")){
        var node = document.createElement("I");
        dispatch(openAppsLoaderValue(100, ''))
        document.getElementById("loadingMsgs").appendChild(node).classList.add('tickmark');
        var x = document.getElementById("loadingMsgs");
		x.innerHTML = 'Completed Succesfully';
    }
    if(getStatus == SUCCESS){
        if(store.getState().datasets.dataUploadLoaderModal && dataPreview.initial_messages!=null && Object.keys(dataPreview.initial_messages).length != 0){
            document.getElementsByClassName("dataPercent")[0].innerHTML = (document.getElementsByClassName("dataPercent")[0].innerText === "In Progress")?"<h2 class="+"text-white"+">"+"100%"+"</h2>":"100%"
            $("#loadingMsgs")[0].innerHTML = "Step " + (dataPreview.message.length-3) + ": " + dataPreview.message[dataPreview.message.length-3].shortExplanation;
            $("#loadingMsgs1")[0].innerHTML ="Step " + (dataPreview.message.length-2) + ": " + dataPreview.message[dataPreview.message.length-2].shortExplanation;
            $("#loadingMsgs2")[0].innerHTML ="Step " + (dataPreview.message.length-1) + ": " + dataPreview.message[dataPreview.message.length-1].shortExplanation;
            $("#loadingMsgs1")[0].className = "modal-steps"
            $("#loadingMsgs2")[0].className = "modal-steps active"
        }
        clearInterval(interval);
        if(interval != undefined){
            setTimeout(() => {
                dispatch(dispatchDataPreview(dataPreview,slug));
                dispatch(hideDULoaderPopup());
                dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
                dispatch(closeAppsLoaderValue());
                dispatch(clearLoadingMsg())
                dispatch(setDataLoadedText(''));
                dispatch(clearMetaDataLoaderValues())
                 }, 2000);
            
        } else{
            dispatch(dispatchDataPreview(dataPreview,slug));
        }
        if(store.getState().datasets.dataUploadLoaderModal||store.getState().apps.appsLoaderModal){
            return { type: "DATA_PREVIEW_ONLOAD", dataPreview,slug,}
        }else{
            return {
                type: "DATA_PREVIEW",
                dataPreview,
                slug,
            }
        }
    }else if(getStatus == FAILED){
        clearInterval(interval);
        dispatch(hideDULoaderPopup());
        bootbox.alert("The uploaded file does not contain data in readable format. Please check the source file.", function() {
            window.history.go(-2);
          });
        dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
        dispatch(clearLoadingMsg())
        dispatch(closeAppsLoaderValue());
        return {
            type: "DATA_PREVIEW_FOR_LOADER",
            dataPreview,
            slug,
        }
    }else if(getStatus == "INPROGRESS"){
        if(window.location.pathname.includes("/apps-stock-advisor")){
            dispatch(getAppsStockList(1));
        }else{
            dispatch(dispatchDataPreviewLoadingMsg(dataPreview));
            dispatch(getDataList(1))
        }
        if(Object.keys(dataPreview.initial_messages).length != 0){
            dispatch(setDataLoadedText(dataPreview.initial_messages));
            if(dataPreview.message[0].globalCompletionPercentage!=undefined && dataPreview.message[0].globalCompletionPercentage !=-1 && store.getState().datasets.metaDataLoaderidxVal!=0){
                dispatch(updateMetaDataIndex(store.getState().datasets.metaDataLoaderidxVal))
            }
            dispatch(updateMetaDataIndexValue(dataPreview.message.length));
        }
        if (dataPreview.message && dataPreview.message !== null && dataPreview.message.length > 0) {
            var msgLength=dataPreview.message.length-1
            dispatch(openAppsLoaderValue(dataPreview.message[msgLength].stageCompletionPercentage, dataPreview.message[msgLength].shortExplanation));
        }
        return {
            type: "SELECTED_DATASET",
            dataset,
        }
    }
}
function updateMetaDataIndexValue(idxVal) {
    return {
      type: "METADATA_LOADER_IDX_VAL",idxVal
    }  
  }
function updateMetaDataIndex(idx) {
    return {
        type: "METADATA_LOADER_IDX",idx
    }  
}
export function clearMetaDataLoaderValues() {
    return {
        type: "CLEAR_METADATA_LOADER_VALUES"
    }
}
function dispatchDataPreview(dataPreview,slug){
    return {
        type: "DATA_PREVIEW",
        dataPreview,
        slug,
    }
}
export function dispatchDataPreviewAutoML(dataPreview,slug){
    return {
        type: "DATA_PREVIEW_AUTOML",
        dataPreview,
        slug,
    }
}
export function setDataLoadedText(text){
    return {
        type: "DATA_LOADED_TEXT",
        text
    }
  }

function dispatchDataPreviewLoadingMsg(dataPreview){
    let message = dataPreview.message
    return {
        type: "CHANGE_LOADING_MSG",
        message
    }
}
function fetchDataPreviewError(json) {
    return {
        type: "DATA_PREVIEW_ERROR",
        json
    }
}
//Fetch userList start 
export function getAllUsersList() {
    return (dispatch) => {
        return fetchAllUsersList(getUserDetailsOrRestart.get().userToken).then(([response, json]) =>{
            if(response.status === 200){
                dispatch(fetchAllUsersSuccess(json))
            }
            else{
                dispatch(fetchAllUsersError(json))
            }
        })
    }
}
function fetchAllUsersList(token) {
    return fetch(API+'/api/users/get_all_users/',{
        method: 'get',
        headers: getHeader(token)
    }).then( response => Promise.all([response, response.json()]));
}
function fetchAllUsersError(json) {
    return {
        type: "USERS_ALL_LIST_ERROR",
        json
    }
}
export function fetchAllUsersSuccess(json){
    return {
        type: "USERS_ALL_LIST",
        json,
    }
}

export function setEditModelValues(flag) {
    return {
      type: "SET_EDIT_MODEL",
      flag
      
    }
  }
  export function openShareModalAction(shareItem,slug,itemType) {
    return {
      type: "SHARE_MODAL_SHOW",
      shareItem,
      slug,
      itemType
    }
  }
  export function openDTModalAction(rule,path,name) {
    return {
      type: "DT_MODAL_SHOW",
      rule,
      path,
      name
    }
  }

  export function closeShareModalAction() {
     return {
       type: "SHARE_MODAL_HIDE",
     }
  }
  export function closeDtModalAction() {
    return {
      type: "DT_MODAL_HIDE",
    }
 }
export function getAllDataList() {
    return (dispatch) => {
        return fetchAllDataList(getUserDetailsOrRestart.get().userToken).then(([response, json]) =>{
            if(response.status === 200){
                dispatch(fetchAllDataSuccess(json))
            }
            else{
                dispatch(fetchAllDataError(json))
            }
        })
    }
}


function fetchAllDataList(token) {
    return fetch(API+'/api/datasets/all/',{
        method: 'get',
        headers: getHeader(token)
    }).then( response => Promise.all([response, response.json()]));
}

function fetchAllDataError(json) {
    return {
        type: "DATA_ALL_LIST_ERROR",
        json
    }
}
export function fetchAllDataSuccess(doc){
    var data = ""
    if(doc.data[0] != undefined){
        data = doc;
    }
    return {
        type: "DATA_ALL_LIST",
        data,
    }
}

export function handleShareItem(userIds,slug,shareItemType,shareItemName){
    return shareItemApi(userIds,slug,shareItemType).then(([response, json]) =>{
        if(response.status === 200 && json.status=="true"){
            bootbox.alert(`${ shareItemType} "${shareItemName}" is shared successfully with ${json.sharedTo}.`)
        }
        else{
            bootbox.alert(`${ shareItemType} "${shareItemName}" sharing failed. Please try again later.`)
        }
    })
}

function shareItemApi(userIds,slug,shareItemType) {
     return fetch(API+'/api/'+shareItemType+'/'+slug+'/share/?shared_id='+userIds,{
        method: 'get',
        headers: getHeader(getUserDetailsOrRestart.get().userToken)
     }).then( response => Promise.all([response, response.json()]));
}


export function saveAdvanceSettings(){
    var savedAnalysisList = jQuery.extend(true, {}, store.getState().datasets.dataSetAnalysisList);
    return {
        type: "SAVE_UPDATE_ANALYSIS_LIST",
        savedAnalysisList,
    }
}
export function cancelAdvanceSettings(){
    var prevAnalysisList = jQuery.extend(true, {}, store.getState().datasets.dataSetPrevAnalysisList);
    return {
        type: "CANCEL_UPDATE_ANALYSIS_LIST",
        prevAnalysisList
    }
}

export function checkAllAnalysisSelected(){
    return (dispatch) => {
        var totalAnalysisList = store.getState().datasets.dataSetAnalysisList;
        var analysisList = [];
        var flag = false;
        if(store.getState().signals.getVarType == "measure"){
            analysisList = totalAnalysisList.measures.analysis;
        }else{
            analysisList = totalAnalysisList.dimensions.analysis;
        }
        for(var i=0;i<analysisList.length;i++){
            if(analysisList[i].status){
                flag = true;
            }else{
                flag = false;
                break;
            }
        }
        dispatch(updateSelectAllAnlysis(flag));
    }
}
export function selectedAnalysisList(evt,noOfColumnsToUse){
    var totalAnalysisList = store.getState().datasets.dataSetAnalysisList;
    var prevAnalysisList = jQuery.extend(true, {}, store.getState().datasets.dataSetPrevAnalysisList);
    var analysisList = [];
    var renderList = {};
    var trendSettings = [];
    if(store.getState().signals.getVarType == "measure"){
        analysisList = totalAnalysisList.measures.analysis;
    }else{
        analysisList = totalAnalysisList.dimensions.analysis;
        trendSettings = totalAnalysisList.dimensions.trendSettings;
    }
    //For updating count,specific measure in trend
    if(noOfColumnsToUse == "trend" ){
        if(evt.type == "select-one"){
            for(var i in trendSettings){
                let name = trendSettings[i].name.toLowerCase();
                if(name.indexOf("specific measure") != -1)
                    trendSettings[i].selectedMeasure = $("#specific-trend-measure").val();
            }
        }
        else{
            for(var i=0;i<analysisList.length;i++){
                if(analysisList[i].name == "trend"){
                    analysisList[i].status = evt.checked;
                    break;
                }
            }
            for(var i in trendSettings){
                let name = trendSettings[i].name.toLowerCase();
                if(name == evt.value){
                    trendSettings[i].status = evt.checked;
                    if(name.indexOf("specific measure") != -1)
                        trendSettings[i].selectedMeasure = $("#specific-trend-measure").val();
                }else{
                    trendSettings[i].status = false;
                    if(name.indexOf("specific measure") != -1)
                        trendSettings[i].selectedMeasure = null
                }
            }
        }
    }//For updating low,medium,high values
    else if(noOfColumnsToUse == "noOfColumnsToUse" ){
        if(evt.type == "radio"){
            for(var i=0;i<analysisList.length;i++){
                if(analysisList[i].name == evt.name){
                    analysisList[i].status = true;
                    for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                        if(analysisList[i].noOfColumnsToUse[j].name == evt.value){
                            analysisList[i].noOfColumnsToUse[j].status = true;
                        }else{
                            analysisList[i].noOfColumnsToUse[j].status = false;
                        }
                    }
                    break;
                }
            }
        }else{
            //for updating custom input value
            for(var i=0;i<analysisList.length;i++){
                if(analysisList[i].name == evt.name){
                    for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                        if(analysisList[i].noOfColumnsToUse[j].name == "custom"){
                            analysisList[i].noOfColumnsToUse[j].value = $("#"+evt.id).val();
                        }
                    }
                    break;
                }
            }
        }
    }
    //For updating Bin values in Association
    else if(noOfColumnsToUse == "association" ){
        for(var i=0;i<analysisList.length;i++){
            if(analysisList[i].name == evt.name){
                if(evt.value)
                    analysisList[i].status = true;
                else
                    analysisList[i].status = false;
                for(var j=0;j<analysisList[i].binSetting.length;j++){
                    if(evt.id == j){
                        analysisList[i].binSetting[j].value = parseInt(evt.value);                                
                    }
                }
                break;
            }
        }

    }
    //For top level analysis update like trend,prediction,association
    else {
        if(evt.target.className == "possibleAnalysis"){
            for(var i=0;i<analysisList.length;i++){
                if(analysisList[i].name == evt.target.value){
                        analysisList[i].status = evt.target.checked;                 
                    if(analysisList[i].noOfColumnsToUse != null){
                        if(!evt.target.checked){
                            for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                                if(analysisList[i].noOfColumnsToUse[j].name == "custom"){
                                    analysisList[i].noOfColumnsToUse[j].status = evt.target.checked;
                                    analysisList[i].noOfColumnsToUse[j].value = null;
                                }else{
                                    analysisList[i].noOfColumnsToUse[j].status = evt.target.checked;
                                }
                            }
                        }else{
                            //when main analysis is checked , low parameter should be checked as default
                            for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                                if(analysisList[i].noOfColumnsToUse[j].name == DEFAULTANALYSISVARIABLES){
                                    analysisList[i].noOfColumnsToUse[j].status = evt.target.checked;
                                }
                            }
                        }
                    }
                    break;
                }
            }
        }

        //For updating trend count and specific measure when trend is unchecked
        if(evt.target.value.indexOf("trend") != -1){
            if(store.getState().signals.getVarType != "measure"){
                if(!evt.target.checked){
                    for(var i in trendSettings){
                        trendSettings[i].status = evt.target.checked;
                    }
                }else{
                    //when trend is selected , count should be selected as default
                    for(var i in trendSettings){
                        let name = trendSettings[i].name.toLowerCase();
                        if(name.indexOf("count") != -1)
                            trendSettings[i].status = evt.target.checked;
                    }
                }
            }
        }

    }

    if(store.getState().signals.getVarType == "measure"){
        totalAnalysisList.measures.analysis = analysisList
    }else{
        totalAnalysisList.dimensions.analysis = analysisList
        totalAnalysisList.dimensions.trendSettings = trendSettings;
    }
    renderList.measures = totalAnalysisList.measures;
    renderList.dimensions = totalAnalysisList.dimensions;
    return {
        type: "UPDATE_ANALYSIS_LIST",
        renderList,
        prevAnalysisList
    }
}

export function selectAllAnalysisList(flag){
    var totalAnalysisList = store.getState().datasets.dataSetAnalysisList;
    var prevAnalysisList = store.getState().datasets.dataSetAnalysisList;
    var analysisList = [];
    var renderList = {};
    var trendSettings = [];
    if(store.getState().signals.getVarType == "measure"){
        analysisList = totalAnalysisList.measures.analysis.slice();
    }else{
        analysisList = totalAnalysisList.dimensions.analysis.slice();
        trendSettings = totalAnalysisList.dimensions.trendSettings;
    }
    for(var i=0;i<analysisList.length;i++){
        if((store.getState().datasets.CopyTimeDimension.filter(i=>(i.selected==true)).length == 0) && analysisList[i].name == "trend")
            analysisList[i].status = false;
        else
            analysisList[i].status = flag;
        if(analysisList[i].noOfColumnsToUse != null){
            for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                //when select all is unchecked
                if(!flag){
                    if(analysisList[i].noOfColumnsToUse[j].name == "custom"){
                        analysisList[i].noOfColumnsToUse[j].status = flag;
                        analysisList[i].noOfColumnsToUse[j].value = null;
                    }else{
                        analysisList[i].noOfColumnsToUse[j].status = flag;
                    }
                }else{
                    if(analysisList[i].noOfColumnsToUse[j].name == DEFAULTANALYSISVARIABLES){
                        analysisList[i].noOfColumnsToUse[j].status = flag;
                    }else{
                        analysisList[i].noOfColumnsToUse[j].status = false;
                    }
                }

            }
        }
    }


    if(store.getState().signals.getVarType != "measure"){
        for(var i in trendSettings){
            if(!flag){
                trendSettings[i].status = flag;
            }else{
                let name = trendSettings[i].name.toLowerCase();
                if(name.indexOf("count") != -1)
                    trendSettings[i].status = flag;
            }
        }
    }


    if(store.getState().signals.getVarType == "measure"){
        totalAnalysisList.measures.analysis = analysisList
    }else{
        totalAnalysisList.dimensions.analysis = analysisList;
        totalAnalysisList.dimensions.trendSettings = trendSettings;
    }
    renderList.measures = totalAnalysisList.measures;
    renderList.dimensions = totalAnalysisList.dimensions;
    return {
        type: "UPDATE_ANALYSIS_LIST",
        renderList,
        prevAnalysisList
    }
}

function updateList(slug,array){
    for(var i=0;i<array.length;i++){
        if(array[i].slug == slug){
            array[i].selected = !array[i].selected;
            break;
        }
    }
    return array;
}
function updateTimeDimList(slug,array,evt){
    for(var i=0;i<array.length;i++){
    if(array[i].slug == slug){
        array[i].selected = evt.target.checked;
    }else{
        array[i].selected = !evt.target.checked;
    }
}
return array;
}

function defaultTimeDimList(slug,array){
    for(var i=0;i<array.length;i++){
        if(array[i].slug == slug){
            array[i].selected = true;
        }
    }
    return array;
}
function getIsAllSelected(array){
    var isAllSelected = true;

    for(var i=0;i<array.length;i++){
        isAllSelected = array[i].selected || array[i].targetColumn;
        if(!isAllSelected)break;
    }

    return isAllSelected;
}

export function updateStoreVariables(measures,dimensions,timeDimensions,dimFlag,meaFlag,count) {
    return (dispatch) => {
        dispatch(updateVariables(measures,dimensions,timeDimensions,dimFlag,meaFlag,count));
        dispatch(applyFilterOnVaraibles());
    }
}

export function updateVariables(measures,dimensions,timeDimensions,dimFlag,meaFlag,count) {
    return {
        type: "UPADTE_VARIABLES_LIST",
        measures,
        dimensions,
        timeDimensions,
        dimFlag,
        meaFlag,
        count
    }
}

function applyFilterOnVaraibles(){
    return (dispatch) => {
        var evt = {};
        evt.target = {}
        if($("#measureSearch").val() != ""){
            evt.target.value = $("#measureSearch").val();
            evt.target.name = "measure"
                dispatch(handleDVSearch(evt));
        }
        if($("#dimensionSearch").val() != ""){
            evt.target.value = $("#dimensionSearch").val();
            evt.target.name = "dimension"
                dispatch(handleDVSearch(evt));
        }

        if($("#datetimeSearch").val() != ""){
            evt.target.value = $("#datetimeSearch").val();
            evt.target.name = "datetime"
                dispatch(handleDVSearch(evt));
        }
    }
}
export function setDefaultTimeDimensionVariable(item){
    return (dispatch) => {
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var dataSetTimeDimensions = store.getState().datasets.CopyTimeDimension.slice();
        var dimFlag =  store.getState().datasets.dimensionAllChecked;
        var meaFlag = store.getState().datasets.measureAllChecked;
        var count = store.getState().datasets.selectedVariablesCount;
        if(item.columnType == "datetime"){
            dataSetTimeDimensions  = defaultTimeDimList(item.slug,dataSetTimeDimensions);
        }
        dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
        count = getTotalVariablesSelected();
        dispatch(updateVariablesCount(count));
    }
}
export function updateSelectedVariablesFromEdit(){
    return(dispatch) =>{
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var dataSetTimeDimensions = store.getState().datasets.CopyTimeDimension.slice();
        
        var dimFlag =  store.getState().datasets.dimensionAllChecked;
        var meaFlag = store.getState().datasets.measureAllChecked;
        var count = store.getState().datasets.selectedVariablesCount;
        
        dimFlag = getIsAllSelected(dataSetDimensions);
        meaFlag = getIsAllSelected(dataSetMeasures);
        count = getTotalVariablesSelected();
        dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
        dispatch(updateVariablesCount(count));
    }

}
export function updateSelectedVariables(evt){
    return (dispatch) => {
        var varSlug = evt.target.id;
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var dataSetTimeDimensions = store.getState().datasets.CopyTimeDimension.slice();

        var dimFlag =  store.getState().datasets.dimensionAllChecked;
        var meaFlag = store.getState().datasets.measureAllChecked;
        var count = store.getState().datasets.selectedVariablesCount;

        if(evt.target.className == "measure"){
            if(evt.target.name != ""){
                dataSetDimensions  = updateList(varSlug,dataSetDimensions);
                dimFlag = getIsAllSelected(dataSetDimensions);
            }
            else{
                dataSetMeasures =  updateList(varSlug,dataSetMeasures);
                meaFlag = getIsAllSelected(dataSetMeasures);
            }
        }else if(evt.target.className == "dimension"){
            dataSetDimensions  = updateList(varSlug,dataSetDimensions);
            dimFlag = getIsAllSelected(dataSetDimensions);
        }
        else if(evt.target.className == "timeDimension"){
                dataSetTimeDimensions  = updateTimeDimList(varSlug,dataSetTimeDimensions,evt);
        }

        dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
        count = getTotalVariablesSelected();
        dispatch(updateVariablesCount(count));
        if(evt.target.baseURI.includes("/createScore") && store.getState().apps.currentAppDetails != null && store.getState().apps.currentAppDetails.app_type == "REGRESSION"){           
        }
        if(evt.target.baseURI.includes("/createSignal"))
        dispatch(uncheckHideAnalysisList());
    }

}

export function updateSelectedVariablesAction(value){
    return {
        type: "CLEAR_SELECTED_VARIABLES",
        value
      }
  }

export function showDataPreview() {
    return {
        type: "SHOW_DATA_PREVIEW",
    }
}

export function hideDataPreview() {
    return {
        type: "HIDE_DATA_PREVIEW",
    }
}

export function storeSignalMeta(signalMeta,curUrl) {
    return {
        type: "STORE_SIGNAL_META",
        signalMeta,
        curUrl
    }
}

export function updateDatasetName(dataset){
    return {
        type: "SELECTED_DATASET",
        dataset,
    }
}
export function resetSelectedVariables(flag){
    if(flag == undefined)
    var selectChk = true;
    else
    var selectChk = flag;
    return {
        type: "RESET_VARIABLES",selectChk
    }
}

export function openDULoaderPopup(){
    return {
        type: "DATA_UPLOAD_LOADER",
    }
}


export function hideDULoaderPopup(){
    return {
        type: "HIDE_DATA_UPLOAD_LOADER",
    }
}
export function showDialogBox(slug,dialog,dispatch,evt){
    var labelTxt = (evt.target.text).trim();
    Dialog.setOptions({
        defaultOkLabel: 'Yes',
        defaultCancelLabel: 'No',
    })
    if(labelTxt == "Stop")
        var body_msg=renderHTML(statusMessages("warning","Are you sure you want to stop uploading the selected data set?","small_mascot"))
    else
	    var body_msg=renderHTML(statusMessages("warning","Are you sure you want to delete the selected data set?","small_mascot"))
    dialog.show({
        title: 'Delete Dataset',
        body: body_msg,
        actions: [
                  Dialog.CancelAction(),
                  Dialog.OKAction(() => {
                      if(labelTxt.indexOf("Stop") != -1)dispatch(handleJobProcessing(slug));
                      else deleteDataset(slug,dialog,dispatch)
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
function deleteDataset(slug,dialog,dispatch){
    dispatch(showLoading());
    Dialog.resetOptions();
    return deleteDatasetAPI(slug).then(([response, json]) =>{
        if(response.status === 200){
            dispatch(getDataList(store.getState().datasets.current_page));
            dispatch(hideLoading());
        }
        else{
            dispatch(hideLoading());
            dialog.showAlert("Something went wrong. Please try again later.");
        }
    })
}
function deleteDatasetAPI(slug){
    return fetch(API+'/api/datasets/'+slug+'/',{
        method: 'put',
        headers: getHeader(getUserDetailsOrRestart.get().userToken),
        body:JSON.stringify({
            deleted:true,
        }),
    }).then( response => Promise.all([response, response.json()]));
}

export function handleRename(slug,dialog,name,allDataList,dataList){
    return (dispatch) => {
        showRenameDialogBox(slug,dialog,dispatch,name,allDataList,dataList)
    }
}
function showRenameDialogBox(slug,dialog,dispatch,name,allDataList,dataList){
    const customBody = (
			<div className="row">
			<div className="col-md-4">
				<img src={STATIC_URL + "assets/images/alert_thinking.gif"} class="img-responsive" />
			</div>
			<div className="col-md-8">
            <div className="form-group">
            <label for="fl1" className="control-label">Enter a new  Name</label>
            <input className="form-control"  id="idRenameDataset" type="text" defaultValue={name}/>
            <div className="text-danger" id="ErrorMsg"></div>
            </div>
			</div>
		</div>
    )

    dialog.show({
        title: 'Rename Dataset',
        body: customBody,
        actions: [
                  Dialog.CancelAction(),
                  Dialog.OKAction(() => {
                    let letters = /^[0-9a-zA-Z\-_\s]+$/;
                    var datalist=store.getState().datasets.dataList.data;
                    var alldataSets=store.getState().datasets.allDataSets.data;
                    if($("#idRenameDataset").val()==""){
                        document.getElementById("ErrorMsg").innerHTML = "Please enter a name to proceed..";
                        showRenameDialogBox(slug, dialog, dispatch, name)
                  }
                  else if (!letters.test($("#idRenameDataset").val())){
                    document.getElementById("ErrorMsg").innerHTML = "Please enter name in a correct format. It should not contain special characters @,#,$,%,!,&.";
                    showRenameDialogBox(slug, dialog, dispatch, name)
                   }
                     else if(datalist!="" && datalist.map(dataset=>dataset.name.toLowerCase()).includes($("#idRenameDataset").val().toLowerCase())){
                        document.getElementById("ErrorMsg").innerHTML = "Dataset with same name already exists.";
                        showRenameDialogBox(slug,dialog,dispatch,name)                      
                      }
                      else if(alldataSets!=undefined && alldataSets.map(dataset=>dataset.name.toLowerCase()).includes($("#idRenameDataset").val().toLowerCase())){
                        document.getElementById("ErrorMsg").innerHTML = "Dataset with same name already exists.";
                        showRenameDialogBox(slug,dialog,dispatch,name)  
                      }
                      else{
                      renameDataset(slug,dialog,$("#idRenameDataset").val(),dispatch)
                      }
                  })
                  ],
                  bsSize: 'medium',
                  onHide: (dialogBox) => {
                      dialogBox.hide()
                  }
    });
}

function renameDataset(slug,dialog,newName,dispatch){
    dispatch(showLoading());
    Dialog.resetOptions();
    return renameDatasetAPI(slug,newName).then(([response, json]) =>{
        if(response.status === 200){
            dispatch(getDataList(store.getState().datasets.current_page));
            dispatch(hideLoading());
        }
        else{
            dialog.showAlert("Renaming unsuccessful. Please try again later.");
            dispatch(hideLoading());
        }
    })
}
function renameDatasetAPI(slug,newName){
    return fetch(API+'/api/datasets/'+slug+'/',{
        method: 'put',
        headers: getHeader(getUserDetailsOrRestart.get().userToken),
        body:JSON.stringify({
            name:newName,
        }),
    }).then( response => Promise.all([response, response.json()]));
}

export function storeDataSearchElement(search_element){
    return {
        type: "SEARCH_DATA",
        search_element
    }
}


export function storeDataSortElements(sorton,sorttype){
    return {
        type: "SORT_DATA",
        sorton,
        sorttype
    }
}

export function getTotalVariablesSelected(){
   var dataPrev =  store.getState().datasets.dataPreview;
   if(dataPrev){
       var varaiblesList = store.getState().datasets.dataPreview.meta_data.uiMetaData.varibaleSelectionArray;
       var totalCount = 0;
       for(var i=0;i<varaiblesList.length;i++){
           if(varaiblesList[i].selected == true && varaiblesList[i].targetColumn == false){
               totalCount = totalCount+1;
           }
       }
       return totalCount;
   }
}
export function updateDatasetVariables(measures,dimensions,timeDimensions,possibleAnalysisList,flag){
    let prevAnalysisList = jQuery.extend(true, {}, possibleAnalysisList);
    var count = getTotalVariablesSelected();
    return {
        type: "DATASET_VARIABLES",
        measures,
        dimensions,
        timeDimensions,
        possibleAnalysisList,
        prevAnalysisList,
        count,
        flag
    }
}

export function updateTargetAnalysisList(renderList){
    let prevAnalysisList = jQuery.extend(true, {}, renderList);
    return {
        type: "UPDATE_ANALYSIS_LIST",
        renderList,
        prevAnalysisList,
    }
}

export function handleDVSearch(evt){
    var name = evt.target.value;
    switch (  evt.target.name ) {
    case "measure":
        return {
        type: "SEARCH_MEASURE",
        name,
    }
        break;
    case "dimension":
        return {
        type: "SEARCH_DIMENSION",
        name,
    }
        break;
    case "datetime":
        return {
        type: "SEARCH_TIMEDIMENSION",
        name,
    }
        break;
    }
}

export function handelSort(variableType,sortOrder){
    switch ( variableType ) {

    case "measure":
        let measures = store.getState().datasets.dataSetMeasures.slice().sort(function(a,b) { return (a.name.toLowerCase() < b.name.toLowerCase()) ? -1 : 1;});
        if(sortOrder == "DESC" )
            measures = store.getState().datasets.dataSetMeasures.slice().sort(function(a,b) { return (a.name.toLowerCase() > b.name.toLowerCase()) ? -1 : 1;});
        let checkBoxList = handleCheckboxes(measures,"measure")
        return {
            type: "SORT_MEASURE",
            measures,
            checkBoxList
        }
        break;
    case "dimension":
        let dimensions = store.getState().datasets.dataSetDimensions.slice().sort(function(a,b) { return (a.name.toLowerCase() < b.name.toLowerCase()) ? -1 : 1;});
        if(sortOrder == "DESC" )
            dimensions = store.getState().datasets.dataSetDimensions.slice().sort(function(a,b) { return (a.name.toLowerCase() > b.name.toLowerCase()) ? -1 : 1;});
        let checkBoxList1 = handleCheckboxes(dimensions,"dimension")
        return {
            type: "SORT_DIMENSION",
            dimensions,
            checkBoxList1
        }
        break;
    case "datetime":
        let timedimensions = store.getState().datasets.dataSetTimeDimensions.slice().sort(function(a,b) { return (a.name.toLowerCase() < b.name.toLowerCase()) ? -1 : 1;});
        if(sortOrder == "DESC" )
            timedimensions = store.getState().datasets.dataSetTimeDimensions.slice().sort(function(a,b) { return (a.name.toLowerCase() > b.name.toLowerCase()) ? -1 : 1;});
        let checkBoxList2 = handleCheckboxes(timedimensions,"datetime")
        return {
            type: "SORT_TIMEDIMENSION",
            timedimensions,
            checkBoxList2,
        }
        break;
    }
}
function handleCheckboxes(list,listType){
    var checkBoxList = [];
    var targetArray = store.getState().datasets.selectedDimensions;
    if(listType == "measure"){
        targetArray = store.getState().datasets.selectedMeasures;
    }else  if(listType == "dimension"){
        targetArray = store.getState().datasets.selectedDimensions;
    }else  if(listType == "datetime"){
        targetArray = [];
        targetArray[0] = store.getState().datasets.selectedTimeDimensions;
    }
    for(var i=0;i<list.length;i++){
        if($.inArray(list[i],targetArray) != -1){
            checkBoxList.push(true);
        }else 	checkBoxList.push(false);
    }
    return checkBoxList;
}
function updateSelectedKey(array,IsSelected){
    for(var i=0;i<array.length;i++){
        array[i].selected = IsSelected;
    }
    return array;
}
export function handleSelectAll(evt){
    return (dispatch) => {
        var varType = evt.target.id;
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var dataSetTimeDimensions = store.getState().datasets.CopyTimeDimension.slice();
        var dimFlag =  store.getState().datasets.dimensionAllChecked;
        var meaFlag = store.getState().datasets.measureAllChecked;
        var count = store.getState().datasets.selectedVariablesCount;
        if(varType == "measure"){
            dataSetMeasures  = updateSelectedKey(dataSetMeasures,evt.target.checked);
            meaFlag = evt.target.checked;
        }else if(varType == "dimension"){
            dataSetDimensions  = updateSelectedKey(dataSetDimensions,evt.target.checked);
            dimFlag = evt.target.checked
        }

        dispatch(updateStoreVariables(dataSetMeasures,dataSetDimensions,dataSetTimeDimensions,dimFlag,meaFlag,count));
        count = getTotalVariablesSelected();
        dispatch(updateVariablesCount(count));
        if(evt.target.baseURI.includes("/createScore") && store.getState().apps.currentAppDetails != null && store.getState().apps.currentAppDetails.app_type == "REGRESSION"){
            if(evt.target.checked == false)
            {
                $('.measure[type="checkbox"]').each(function() {
                    $(this).prop('disabled', false);
                });
                $('.dimension[type="checkbox"]').each(function() {
                    $(this).prop('disabled', false);
                });
            }            
        }
        if(evt.target.baseURI.includes("/createSignal"))
        dispatch(uncheckHideAnalysisList());
    }
}

export function updateSubSetting(updatedSubSetting){
    return {
        type: "UPDATE_SUBSETTING",
        updatedSubSetting
    }
}

//Rename Metadata column
export function renameMetaDataColumn(dialog,colName,colSlug,dispatch,actionName){
    let headers = store.getState().datasets.dataPreview.meta_data.uiMetaData.headersUI;
    const customBody = (
		<div className="row">
			<div className="col-md-4">
				<img src={STATIC_URL + "assets/images/alert_thinking.gif"} class="img-responsive" />
			</div>
			<div className="col-md-8">
            <div className="form-group">
            <label for="fl1" className="control-label">Enter a new Name</label>
            <input className="form-control"  name="idRenameMetaCloumn" id="idRenameMetaCloumn" type="text" defaultValue={colName}/>
            </div>
			</div>
		</div>
    )

    dialog.show({
        title: 'Rename Column',
        body: customBody,
        actions: [
                    Dialog.CancelAction(),
                    Dialog.OKAction(() => {
                    var newColName = ($("#idRenameMetaCloumn").val()).toUpperCase();
                    let colNames = headers.map(e => (e.name).toUpperCase());

                    if(colNames.includes(newColName)){
                        bootbox.alert(statusMessages("warning","There is another column with same name.","small_mascot"));
                    }
                    else if($("#idRenameMetaCloumn").val().trim()=="")
                    {
                        bootbox.alert(statusMessages("warning","Please enter the valid column name.","small_mascot"));
                    }
                    else{
                        updateColumnName(dispatch,colSlug,$("#idRenameMetaCloumn").val());
                        updateColumnStatus(dispatch,colSlug,$("#idRenameMetaCloumn").val(),actionName);
                    }
                  })
                  ],
                  bsSize: 'medium',
                  onHide: (dialogBox) => {
                      dialogBox.hide()
                  }
    });
}
function updateColumnName(dispatch,colSlug,newColName){
    var metaData = store.getState().datasets.dataPreview;
    var slug = store.getState().datasets.selectedDataSet;
    var colData = metaData.meta_data.uiMetaData.columnDataUI;
    for(var i=0;i<colData.length;i++){
        if(colData[i].slug == colSlug){
            colData[i].name = newColName;
            break;
        }
    }
    metaData.meta_data.uiMetaData.columnDataUI = colData;
}
export function handleColumnClick(dialog,actionName,colSlug,colName,subActionName,colStatus){
    return (dispatch) => {
        if(actionName == RENAME){
            renameMetaDataColumn(dialog,colName,colSlug,dispatch,actionName)
        }else if(actionName == DELETE){
            deleteMetaDataColumn(dialog,colName,colSlug,dispatch,actionName,colStatus);
        }else if(actionName == REPLACE){
            dispatch(updateVLPopup(true));
            dispatch(addComponents(colSlug));
        }else if(actionName == UNIQUE_IDENTIFIER){
            if(!colStatus){
				let prevUniqueid = statusMessages("warning","Are you sure you want to make this column as unique identifier?","small_mascot");
                bootbox.confirm(prevUniqueid,
                        function(result){
                    if(result){
                        $(".cst_table").find("thead").find("."+colSlug).first().find("a").addClass("text-primary");
                        updateUniqueIdentifierColumn(dispatch,actionName,colSlug,colStatus);
                    }
                });
            }else{
                updateUniqueIdentifierColumn(dispatch,actionName,colSlug,colStatus);
                $(".cst_table").find("thead").find("."+colSlug).first().find("a").removeClass("text-primary");
            }

        }else {
            updateColumnStatus(dispatch,colSlug,colName,actionName,subActionName);
        }
    }
}

function deleteMetaDataColumn(dialog,colName,colSlug,dispatch,actionName,colStatus){
    var nonDeletedColumns = 0;
    let dataPrev = store.getState().datasets.dataPreview.meta_data;
    $.each(dataPrev.uiMetaData.metaDataUI,function(key,val){
        if(val.name == "noOfColumns"){
            nonDeletedColumns = val.value;
            return false;
        }
    });
    if(nonDeletedColumns <= 2 && colStatus != true){
        let errormsg = statusMessages("warning", "Cannot delete any more columns", "small_mascot");
        bootbox.alert(errormsg)
        return;
    }
	var body_msg=statusMessages("warning","Are you sure, you want to delete the selected column?","small_mascot");
    if(colStatus == true){
        body_msg = statusMessages("warning","Are you sure, you want to undelete the selected column?","small_mascot");
    }
    bootbox.confirm({
      title:"Delete Column",
      message:body_msg,
      //size:"small",
      buttons: {
      'cancel': {
          label: 'No'
      },
      'confirm': {
          label: 'Yes'
      }
  },
      callback:function(result){
        if(result){
            $(".cst_table").find("thead").find("."+colSlug).first().addClass("dataPreviewUpdateCol");
            $(".cst_table").find("tbody").find("tr").find("."+colSlug).addClass("dataPreviewUpdateCol");
            updateColumnStatus(dispatch,colSlug,colName,actionName)
        }
    }});
}
export function updateVLPopup(flag){
    return{
        type: "UPDATE_VARIABLES_TYPES_MODAL",
        flag
    }
}
export function updateColumnStatus(dispatch,colSlug,colName,actionName,subActionName){
    dispatch(showLoading());
    var isSubsetting = false;
    var transformSettings = store.getState().datasets.dataTransformSettings.slice();
    var slug = store.getState().datasets.selectedDataSet;
    for(var i =0;i<transformSettings.length;i++){
        if(transformSettings[i].slug == colSlug){
            for(var j=0;j<transformSettings[i].columnSetting.length;j++){
                if(transformSettings[i].columnSetting[j].actionName == actionName){

                    if(actionName == RENAME){
                        transformSettings[i].columnSetting[j].newName = colName;
                        transformSettings[i].columnSetting[j].status=true;
                        break;
                    }else if(actionName == DELETE){
                        if(transformSettings[i].columnSetting[j].status){
                            transformSettings[i].columnSetting[j].status = false;
                            $(".cst_table").find("thead").find("."+colSlug).first().removeClass("dataPreviewUpdateCol");
                            $(".cst_table").find("tbody").find("tr").find("."+colSlug).removeClass("dataPreviewUpdateCol");
                        }
                        else transformSettings[i].columnSetting[j].status = true;
                        break;
                    }else if(actionName == IGNORE_SUGGESTION){
                        if(transformSettings[i].columnSetting[j].status){
                            transformSettings[i].columnSetting[j].status = false;
                        }
                        else transformSettings[i].columnSetting[j].status = true;
                        break;
                    }else if(actionName == REPLACE){
                        transformSettings[i].columnSetting[j].status=true;
                        var removeValues =  store.getState().datasets.dataSetColumnRemoveValues.slice();
                        var replaceValues =  store.getState().datasets.dataSetColumnReplaceValues.slice();
                        replaceValues = replaceValues.concat(removeValues);
                        transformSettings[i].columnSetting[j].replacementValues = replaceValues;
                    }else{
                        transformSettings[i].columnSetting[j].status=true;
                        if(transformSettings[i].columnSetting[j].hasOwnProperty("listOfActions")){
                            for(var k=0;k<transformSettings[i].columnSetting[j].listOfActions.length;k++){
                                if(transformSettings[i].columnSetting[j].listOfActions[k].name == subActionName){
                                    transformSettings[i].columnSetting[j].listOfActions[k].status = true;
                                }else{
                                    transformSettings[i].columnSetting[j].listOfActions[k].status = false;
                                }
                            }
                            break;
                        }

                    }


                }
            }//end of for columnsettings
            break;
        }
    }
    if(actionName != SET_VARIABLE && actionName != UNIQUE_IDENTIFIER && actionName != SET_POLARITY && actionName != IGNORE_SUGGESTION && actionName !=DATA_TYPE){
        isSubsetting = true;
    }else{
        //Enable subsetting when any one of the column is deleted,renamed, removed
        if(store.getState().datasets.subsettingDone == false) {
            isSubsetting = false;
        }else{
            isSubsetting = true;
        }
    }
    dispatch(handleColumnActions(transformSettings,slug,isSubsetting))
    dispatch(updateVLPopup(false));
}

function updateUniqueIdentifierColumn(dispatch,actionName,colSlug,isChecked){
    dispatch(showLoading());
    var slug = store.getState().datasets.selectedDataSet;
    var transformSettings = store.getState().datasets.dataTransformSettings.slice();
    for(var i =0;i<transformSettings.length;i++){
        for(var j=0;j<transformSettings[i].columnSetting.length;j++){
            if(transformSettings[i].columnSetting[j].actionName == actionName){
                if(transformSettings[i].slug == colSlug){
                    transformSettings[i].columnSetting[j].status = !isChecked;
                }
                else {
                    if(transformSettings[i].columnSetting[j].status){
                        $(".cst_table").find("thead").find("."+transformSettings[i].slug).first().find("a").removeClass("text-primary")
                        transformSettings[i].columnSetting[j].status = false;
                    }
                }
            } else if(transformSettings[i].columnSetting[j].actionName == IGNORE_SUGGESTION){
                if(transformSettings[i].slug == colSlug){
                    transformSettings[i].columnSetting[j].status = false;
                }
            }
        }
    }
    dispatch(handleColumnActions(transformSettings,slug,false))
}

export function replaceValuesErrorAction(errMsg){
    bootbox.alert(statusMessages("error",errMsg,"small_mascot"));
}
export function handleSaveEditValues(colSlug){
    return (dispatch) => {
        updateColumnStatus(dispatch,colSlug,"",REPLACE,"");
    }
}

export function updateColSlug(slug){
    return{
        type: "DATASET_SELECTED_COLUMN_SLUG",
        slug
    }
}

export function handleColumnActions(transformSettings,slug,isSubsetting) {
    return (dispatch) => {
        return fetchModifiedMetaData(transformSettings,slug).then(([response, json]) =>{
            if(response.status === 200){ 
                dispatch(saveSelectedValuesForModel(store.getState().apps.apps_regression_modelName, "", ""))
                dispatch(makeAllVariablesTrueOrFalse(true));
                dispatch((resetSelectedTargetVariable()))
                dispatch(fetchDataValidationSuccess(json,isSubsetting));
                dispatch(hideLoading());
                dispatch(vaiableSelectionUpdate(true));
            }
            else{

                dispatch(fetchDataPreviewError(json));
                dispatch(vaiableSelectionUpdate(false));
                dispatch(hideLoading());
                let msg=statusMessages("error","Something went wrong. Please try again later.","small_mascot")
                bootbox.alert(msg)            }
        }).catch(function(){
            dispatch(hideLoading());
            dispatch(vaiableSelectionUpdate(false));
            let msg=statusMessages("error","Something went wrong. Please try again later.","small_mascot")
            bootbox.alert(msg)
        });
    }
}

export function vaiableSelectionUpdate(flag){
    return {type: "IS_VARIABLE_SELECTION_UPDATE", flag}
}
function fetchModifiedMetaData(transformSettings,slug) {
    var tran_settings = {};
    var uiMetaDataPrev = store.getState().datasets.dataPreview.meta_data.uiMetaData;
    tran_settings.existingColumns = transformSettings;
    return fetch(API+'/api/datasets/'+slug+'/meta_data_modifications/',{
        method: 'put',
        headers: getHeader(getUserDetailsOrRestart.get().userToken),
        body:JSON.stringify({
            config:tran_settings,
            uiMetaData:uiMetaDataPrev,
        }),
    }).then( response => Promise.all([response, response.json()]));
}

export function fetchDataValidationSuccess(uiMetaData,isSubsetting){
    var prevDataPreview = store.getState().datasets.dataPreview;
    prevDataPreview.meta_data.uiMetaData = uiMetaData;
    var dataPreview = Object.assign({}, prevDataPreview);

    return{
        type: "DATA_VALIDATION_PREVIEW",
        dataPreview,
        isSubsetting
    }
}

export function addComponents(colSlug){
    return (dispatch) => {
        var transformSettings = store.getState().datasets.dataTransformSettings.slice();
        var dataColumnRemoveValues = [];
        var dataColumnReplaceValues = [];

        for(var i =0;i<transformSettings.length;i++){
            if(transformSettings[i].slug == colSlug){
                for(var j=0;j<transformSettings[i].columnSetting.length;j++){
                    if(transformSettings[i].columnSetting[j].actionName == REPLACE){
                        var replacementValues = transformSettings[i].columnSetting[j].replacementValues;
                        for(var k=0;k<replacementValues.length;k++){
                            //Differentiate remove/replace values
                            if(replacementValues[k].name.indexOf("remove") != -1){
                                dataColumnRemoveValues.push(replacementValues[k])
                            }else{
                                dataColumnReplaceValues.push(replacementValues[k])
                            }
                        }
                    }

                }//end of for columnsettings
                break;
            }
        }

        if(dataColumnRemoveValues.length == 0){
            dataColumnRemoveValues.push({"id":1,"name":"remove1","valueToReplace":"","replacedValue":"","replaceType":"equals"});

        }if(dataColumnReplaceValues.length == 0){
            dataColumnReplaceValues.push({"replaceId":1,"name":"replace1","valueToReplace":"","replacedValue":"","replaceType":"equals"});
        }

        dispatch(updateColumnReplaceValues(dataColumnReplaceValues))
        dispatch(updateColumnRemoveValues(dataColumnRemoveValues))
    }
}
function updateColumnRemoveValues(removeValues){
    return{
        type: "DATA_VALIDATION_REMOVE_VALUES",
        removeValues
    }
}
function updateColumnReplaceValues(replaceValues){
    return{
        type: "DATA_VALIDATION_REPLACE_VALUES",
        replaceValues
    }
}
export function addMoreComponentsToReplace(editType){
    return (dispatch) => {
        if(editType == REMOVE){
            var dataColumnRemoveValues = store.getState().datasets.dataSetColumnRemoveValues.slice();
            if(dataColumnRemoveValues.length > 0){
                var max = dataColumnRemoveValues.reduce(function(prev, current) {
                    return (prev.id > current.id) ? prev : current
                });
                let length = max.id+1;
                dataColumnRemoveValues.push({"id":length,"name":"remove"+length,"valueToReplace":"","replacedValue":"","replaceType":"equals"});

            }else{
                dataColumnRemoveValues.push({"id":1,"name":"remove1","valueToReplace":"","replacedValue":"","replaceType":"equals"});
            }

            dispatch(updateColumnRemoveValues(dataColumnRemoveValues))
        }else{
            var dataColumnReplaceValues = store.getState().datasets.dataSetColumnReplaceValues.slice();
            if(dataColumnReplaceValues.length > 0){
                var max = dataColumnReplaceValues.reduce(function(prev, current) {
                    return (prev.replaceId > current.replaceId) ? prev : current

                });
                let length = max.replaceId+1;
                dataColumnReplaceValues.push({"replaceId":length,"name":"replace"+length,"valueToReplace":"","replacedValue":"","replaceType":"equals"});
            }else{
                dataColumnReplaceValues.push({"replaceId":1,"name":"replace1","valueToReplace":"","replacedValue":"","replaceType":"equals"});
            }

            dispatch(updateColumnReplaceValues(dataColumnReplaceValues))
        }

    }
}
export function removeComponents(data,editType){
    return (dispatch) => {
        if(editType == REMOVE){
            var dataColumnRemoveValues = store.getState().datasets.dataSetColumnRemoveValues.slice();
            for (var i=0;i<dataColumnRemoveValues.length;i++) {
                if(dataColumnRemoveValues[i].id == data.id){
                    dataColumnRemoveValues.splice(i,1);
                    break;
                }
            }
            dispatch(updateColumnRemoveValues(dataColumnRemoveValues))
        }else{
            var dataColumnReplaceValues = store.getState().datasets.dataSetColumnReplaceValues.slice();
            for (var i=0;i<dataColumnReplaceValues.length;i++) {
                if(dataColumnReplaceValues[i].replaceId == data.replaceId){
                    dataColumnReplaceValues.splice(i,1);
                    break;
                }
            }
            dispatch(updateColumnReplaceValues(dataColumnReplaceValues))
        }
    }
}
export function handleInputChange(event){
    return (dispatch) => {
        var dataColumnRemoveValues = store.getState().datasets.dataSetColumnRemoveValues.slice();
        for (var i=0;i<dataColumnRemoveValues.length;i++) {
            if(dataColumnRemoveValues[i].id == event.target.id){
                if(event.target.type == "text"){
                    dataColumnRemoveValues[i].valueToReplace = event.target.value;
                    break;
                }else {
                    dataColumnRemoveValues[i].replaceType = event.target.value;
                    break;
                }

            }
        }
        dispatch(updateColumnRemoveValues(dataColumnRemoveValues))
    }
}
export function handleInputChangeReplace(targetTextBox,event){
    return (dispatch) => {
        var dataSetColumnReplaceValues = store.getState().datasets.dataSetColumnReplaceValues.slice();
        for (var i=0;i<dataSetColumnReplaceValues.length;i++) {
            if(dataSetColumnReplaceValues[i].replaceId == event.target.id){
                if(targetTextBox == NEWVALUE){
                    dataSetColumnReplaceValues[i].replacedValue = event.target.value;
                    break;
                }
                else if(targetTextBox == CURRENTVALUE){
                    dataSetColumnReplaceValues[i].valueToReplace = event.target.value;
                    break;
                }else{
                    dataSetColumnReplaceValues[i].replaceType = event.target.value;
                    break;
                }
            }
        }
        dispatch(updateColumnReplaceValues(dataSetColumnReplaceValues))
    }
}

export function updateSelectAllAnlysis(flag){
    return{
        type: "DATA_SET_SELECT_ALL_ANALYSIS",
        flag
    }
}

export function popupAlertBox(msg,props,url){
    bootbox.alert(msg,function(){
        props.history.push(url)
    });
}
export function deselectAllVariablesDataPrev(flag){
  let dataPrev=store.getState().datasets.dataPreview
  let slug=store.getState().datasets.selectedDataSet
  if(dataPrev&&dataPrev.meta_data){
  for(var i=0;i<dataPrev.meta_data.uiMetaData.varibaleSelectionArray.length;i++){
    if(dataPrev.meta_data.uiMetaData.varibaleSelectionArray[i].columnType == "datetime" || dataPrev.meta_data.uiMetaData.varibaleSelectionArray[i].dateSuggestionFlag)
    continue;
    dataPrev.meta_data.uiMetaData.varibaleSelectionArray[i].selected=flag;
  }
  dispatchDataPreview(dataPrev,slug)
}
}

export function makeAllVariablesTrueOrFalse(value){
  return{
    type:"MAKE_ALL_TRUE_OR_FALSE",
    value
  }
}

export function uncheckHideAnalysisList(){
    return (dispatch) => {
        var dataSetMeasures = store.getState().datasets.CopyOfMeasures.slice();
        var dataSetDimensions = store.getState().datasets.CopyOfDimension.slice();
        var targetVariableType = store.getState().signals.getVarType;
        let measureArray = $.grep(dataSetMeasures,function(val,key){
            return(val.selected == true && val.targetColumn == false);
        });
        let dimensionArray = $.grep(dataSetDimensions,function(val,key){
            return(val.selected == true && val.targetColumn == false);
        });
        if(targetVariableType == "dimension"){
            if(measureArray.length < 1 && dimensionArray.length < 1){
                dispatch(saveDeselectedAnalysisList($("#chk_analysis_association").val()));
                dispatch(saveDeselectedAnalysisList($("#chk_analysis_prediction").val()));
            }

        }
        else if(targetVariableType == "measure"){
            if(dimensionArray.length < 1)
            dispatch(saveDeselectedAnalysisList($("#chk_analysis_performance").val()));

            if(measureArray.length < 1)
            dispatch(saveDeselectedAnalysisList($("#chk_analysis_influencer").val()));

            if(measureArray.length < 1 && dimensionArray.length < 1)
            dispatch(saveDeselectedAnalysisList($("#chk_analysis_prediction").val()));
        }
    }
}
export function saveDeselectedAnalysisList(name){
    var totalAnalysisList = store.getState().datasets.dataSetAnalysisList;
    var prevAnalysisList = jQuery.extend(true, {}, store.getState().datasets.dataSetPrevAnalysisList);
    var analysisList = [];
    var renderList = {};
    var trendSettings = [];
    if(store.getState().signals.getVarType == "measure"){
        analysisList = totalAnalysisList.measures.analysis;
    }else{
        analysisList = totalAnalysisList.dimensions.analysis;
        trendSettings = totalAnalysisList.dimensions.trendSettings;
    }

    for(var i=0;i<analysisList.length;i++){
                if(analysisList[i].name == name){
                    analysisList[i].status = false;
                    if(analysisList[i].noOfColumnsToUse != null){
                            for(var j=0;j<analysisList[i].noOfColumnsToUse.length;j++){
                                if(analysisList[i].noOfColumnsToUse[j].name == "custom"){
                                    analysisList[i].noOfColumnsToUse[j].status = false;
                                    analysisList[i].noOfColumnsToUse[j].value = null;
                                }else{
                                    analysisList[i].noOfColumnsToUse[j].status = false;
                                }
                            }
                    }
                    break;
                }
            }

            if(name.indexOf("trend") != -1){
            if(store.getState().signals.getVarType != "measure"){
                for(var i in trendSettings){
                    trendSettings[i].status = false;
                }
            }
        }

    if(store.getState().signals.getVarType == "measure"){
    totalAnalysisList.measures.analysis = analysisList
    }else{
        totalAnalysisList.dimensions.analysis = analysisList
        totalAnalysisList.dimensions.trendSettings = trendSettings;
    }
    renderList.measures = totalAnalysisList.measures;
    renderList.dimensions = totalAnalysisList.dimensions;
    return {
        type: "UPDATE_ANALYSIS_LIST_SELECT_ALL",
        renderList,
        prevAnalysisList,
        flag:false,
    }
}
export function showAllVariables(array,slug){
    $.each(array.meta_data.uiMetaData.varibaleSelectionArray,function(key,item){
        item.targetColumn = false;
    });
    return {
            type: "DATA_PREVIEW",
            dataPreview:array,
            slug,
    }
}

export function disableAdvancedAnalysisElements(elementName,action){
    if(elementName == "association")
    return {
            type: "ADVANCE_ANALYSIS_ASSOCIATION",
            disble:action,
    }
    else if(elementName == "prediction")
    return {
            type: "ADVANCE_ANALYSIS_PREDICTION",
            disble:action,
    }
    else if(elementName == "performance")
    return {
            type: "ADVANCE_ANALYSIS_PERFORMANCE",
            disble:action,
    }
    else if(elementName == "influencer")
    return {
            type: "ADVANCE_ANALYSIS_INFLUENCER",
            disble:action,
    }
}
export function resetSubsetting(slug){
    return {
            type: "RESET_SUBSETTED_DATASET",
            slug,
    }
}
export function updateVariableSelectionArray(summary,eidt){
    if(!$.isEmptyObject(summary))
    {
        var newVariableSelectionArray = store.getState().apps.modelSummary.config.config.COLUMN_SETTINGS.variableSelection;
        var newDataPreview = store.getState().datasets.dataPreview;
        newDataPreview.meta_data.uiMetaData.varibaleSelectionArray = newVariableSelectionArray;
        var flag = true;
        return {
            type:"UPDATE_VARAIABLE_SELECTION_ARRAY",
            newDataPreview,
            flag,

        }
    }
    else if(eidt=="edit"){
        var newVariableSelectionArray = store.getState().datasets.modelEditconfig.config.config.COLUMN_SETTINGS.variableSelection;
        var newDataPreview = store.getState().datasets.dataPreview;
        newDataPreview.meta_data.uiMetaData.varibaleSelectionArray = newVariableSelectionArray;
        var flag = false;
        return {
            type:"UPDATE_VARAIABLE_SELECTION_ARRAY",
            newDataPreview,
            flag,

        }
    }

    else{
        var newDataPreview = store.getState().datasets.dataPreview;
        var flag = false;
        return {
            type:"UPDATE_VARAIABLE_SELECTION_ARRAY",
            newDataPreview,
            flag,
        }
    }
}

export function clearDataCleansing(){
    return {type:"CLEAR_DATACLEANSING"}
}
export function clearFeatureEngineering(){
    return {type:"CLEAR_FEATUREENGINEERING"}
}

export function setCreateSignalLoaderFlag(flag){
    return {
        type : "SET_CREATE_SIG_LOADER_FLAG",flag
    }
}

export function variableSlectionBack(flag){
    return {
        type : "SET_VARIABLE_SELECTION_BACK",flag
    }
}
export function SaveScoreName(value){
    return {
        type : "SAVE_SCORE_NAME",value
    }
}
export function saveSelectedColSlug(slug){
    return{
        type:"ACTIVE_COL_SLUG",slug
    }
}
export function paginationFlag(flag){
    return{
        type:"PAGINATION_FLAG",flag
    }
}
export function clearDataList(){
    return{
        type:"CLEAR_DATA_LIST"
    }
}
export function clearSubset(){
    return{
        type:"CLEAR_SUBSET"
    }
}
export function setAlreadyUpdated(flag){
    return{
        type:"ALREADY_UPDATED",flag
    }
}
export function setMeasureColValues(name,value){
    return{
        type:"CUR_MEASURE_COL",name,value
    }
}
export function setDimensionColValues(name,value){
    return{
        type:"CUR_DIMENSION_COL",name,value
    }
}
export function setDatetimeColValues(name,value){
    return{
        type:"CUR_DATETIME_COL",name,value
    }
}
export function selMeasureCol(name){
    return{
        type:"SEL_MEASURE_COL",name
    }
}
export function selDimensionCol(name){
    return{
        type:"SEL_DIMENSION_COL",name
    }
}
export function selDatetimeCol(name){
    return{
        type:"SEL_DATETIME_COL",name
    }
}
export function selectAllDimValues(flag){
    return{
        type:"SELECT_ALL_DIM_VAL",flag
    }
}
export function selectDimValues(val,flag){
    return{
        type:"SELECT_DIM_VAL",val,flag
    }
}
export function  getValueOfFromParam() {
    if(window.location === undefined){

    }else{
      const params = new URLSearchParams(window.location.search);
      return params.get('from');
    }
}