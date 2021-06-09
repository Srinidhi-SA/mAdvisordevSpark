import {API} from "../helpers/env";
import {DYNAMICLOADERINTERVAL} from "../helpers/helper";
import store from "../store";
import { DULOADERPERVALUE, LOADERMAXPERVALUE, DEFAULTINTERVAL, DULOADERPERMSG,getUserDetailsOrRestart} from "../helpers/helper";
import { getDataSetPreview, updateDatasetName, openDULoaderPopup,hideDULoaderPopup} from "./dataActions";
import {closeModelPopup} from "./appActions";

export var dataPreviewInterval = null;

export function getHeaderWithoutContent(token) {
  return {'Authorization': token};
}
function getHeader(token) {
  return {'Authorization': token, 'Content-Type': 'application/json'};
}
export function dataUpload() {
    var dbDetails = {};
    return (dispatch) => {
    if (store.getState().dataSource.selectedDataSrcType == "fileUpload") {
        if(store.getState().dataSource.fileUpload[0].name!=""){
            $("#fileErrorMsg").addClass("visibilityHidden");
            dispatch(uploadFileOrDB());
        }else{
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Please add a new file or select an existing dataset.");
        }
    }
    else{
        var elements = document.getElementById(store.getState().dataSource.selectedDataSrcType).elements;
        var flag = false;
        for(var i=0;i<elements.length;i++){
           
            if(elements[i].required &&  elements[i].value == ""){
                $("#"+elements[i].id).css("border-color","red");
                $("#"+elements[i].id).trigger("focus");
                flag = true;
            }else{
                $("#"+elements[i].id).css("border-color","#e0e0e0");
                dbDetails[elements[i].name] = elements[i].value
            }
        }
        if(!flag)
        dispatch(uploadFileOrDB(dbDetails));
    }
    }

}
function uploadFileOrDB(dbDetails){
    return (dispatch) => {
        dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
        dispatch(dataUploadLoaderMsg(DULOADERPERMSG));
        dispatch(close());
        //close model DB popup when user is trying to upload data in model creation
        dispatch(closeModelPopup())
        dispatch(openDULoaderPopup());

        return triggerDataUpload(getUserDetailsOrRestart.get().userToken,dbDetails).then(([response, json]) => {
          if (response.status === 200) {
              dispatch(updateDatasetName(json[0].slug))
              dispatch(dataUploadSuccess(json[0], dispatch))
          } else {
            dispatch(dataUploadError(json))
          }
        }).catch(function(error) {
              bootbox.alert("Connection lost. Please try again later.")
              dispatch(hideDULoaderPopup());
              dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
              clearInterval(dataPreviewInterval);
          });
      }
}
function triggerDataUpload(token,dbDetails) {
  if (store.getState().dataSource.selectedDataSrcType == "fileUpload") {
    var data = new FormData();
    for (var x = 0; x < store.getState().dataSource.fileUpload.length; x++) {
      data.append("input_file", store.getState().dataSource.fileUpload[x]);
    }
    return fetch(API + '/api/datasets/', {
      method: 'post',
      headers: getHeaderWithoutContent(token),
      body: data
    }).then(response => Promise.all([response, response.json()]));
  } else {
    return fetch(API + '/api/datasets/', {
      method: 'post',
      headers: getHeader(token),
      body: JSON.stringify({datasource_details: dbDetails, datasource_type: store.getState().dataSource.selectedDataSrcType})
    }).then(response => Promise.all([response, response.json()]));
  }
}

export function triggerDataUploadAnalysis(data,percentage, message){
    return (dispatch) => {
        dispatch(dataUploadLoaderValue(percentage));
        dispatch(dataUploadLoaderMsg(message));
        dispatch(openDULoaderPopup());
        dataUploadSuccess(data,dispatch)
    }
}
function dataUploadSuccess(data, dispatch) {
  let msg = store.getState().datasets.dataLoaderText
  let loaderVal = store.getState().datasets.dULoaderValue;
  let dataset = data.slug
  if(data.hasOwnProperty("proceed_for_loading") && !data.proceed_for_loading){
      msg = "Your dataset will be uploaded in background...";
      dispatch(dataUploadLoaderMsg(msg));
      setTimeout(function() {
          dispatch(hideDULoaderPopup());
          dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
      },DYNAMICLOADERINTERVAL);
  }
  else{
    dataPreviewInterval = setInterval(function() {
        let loading_message = store.getState().datasets.loading_message
        dispatch(getDataSetPreview(data.slug, dataPreviewInterval));
        if (store.getState().datasets.dULoaderValue < LOADERMAXPERVALUE) {
          if (loading_message && loading_message.length > 0) {
            if(loading_message[loading_message.length - 1].display&&loading_message[loading_message.length - 1].display==true){
          msg = loading_message[loading_message.length - 1].shortExplanation
        }
            loaderVal = loading_message[loading_message.length - 1].globalCompletionPercentage
          }
          dispatch(dataUploadLoaderValue(loaderVal));
          dispatch(dataUploadLoaderMsg(msg));
        } else {
          dispatch(clearLoadingMsg())
        }

      }, DEFAULTINTERVAL);
      dispatch(dataUploadLoaderValue(loaderVal));

}
  return {
      type: "SELECTED_DATASET",
      dataset
  }
}

export function dataUploadError(json) {
  return {type: "DATA_UPLOAD_TO_SERVER_ERROR", json}
}

export function open() {
  return {type: "SHOW_MODAL"}
}

export function close() {
  return {type: "HIDE_MODAL"}
}

export function openImg() {
  return {type: "SHOW_IMG_MODAL"}
}

export function closeImg() {
  return {type: "HIDE_IMG_MODAL"}
}

export function dataUploadLoaderValue(value) {
  return {type: "DATA_UPLOAD_LOADER_VALUE", value}
}

export function dataUploadLoaderMsg(message) {
  return {type: "DATA_UPLOAD_LOADER_MSG", message}
}

export function dataSubsetting(subsetRq, slug) {
  return (dispatch) => {
   dispatch(dataUploadLoaderValue(DULOADERPERVALUE));
    dispatch(dataUploadLoaderMsg(DULOADERPERMSG));
   dispatch(close());
 dispatch(openDULoaderPopup());
    return triggerDataSubsetting(subsetRq, slug).then(([response, json]) => {
    if (response.status === 200) {
        dispatch(updateDatasetName(json.slug))
        dispatch(dataUploadSuccess(json, dispatch))
        dispatch(updateSubsetSuccess(json))
      } else {
          dispatch(clearLoadingMsg())
          dispatch(dataUploadError(json))
      }
    });
  }
}

function triggerDataSubsetting(subsetRq, slug) {
  return fetch(API + '/api/datasets/' + slug + '/', {
    method: 'put',
    headers: getHeader(getUserDetailsOrRestart.get().userToken),
    body: JSON.stringify(subsetRq)
  }).then(response => Promise.all([response, response.json()]));
}

function updateSubsetSuccess(subsetRs) {
  return {type: "SUBSETTED_DATASET", subsetRs}
}
export function clearDataPreview() {
  return {type: "CLEAR_DATA_PREVIEW"}
}

export function clearLoadingMsg() {
  return {type: "CLEAR_LOADING_MSG"}
}
export function clearDatasetPreview(){
    clearInterval(dataPreviewInterval)
}
