import {API} from "../helpers/env";
import {getUserDetailsOrRestart} from "../helpers/helper";

function getHeader(token){
	return {
		'Authorization': token,
		'Content-Type': 'application/json'
	};
}

function dataSourceFlag(flag){
	return{
		type: "DATA_SOURCE_FLAG",flag
	}
}
export function getDataSourceList(){
	return (dispatch) => {
		return fetchDataSourceList(getUserDetailsOrRestart.get().userToken).then(([response, json]) =>{
			if(response.status === 200){
				dispatch(fetchDataSrcSuccess(json))
				dispatch(dataSourceFlag(false));
			}
			else{
				dispatch(fetchdDataSrcError(json))
			}
		})
	}
}
function fetchDataSrcSuccess(dataSrcList){

	return {
		type: "DATA_SOURCE_LIST",
		dataSrcList,
	}
}
export function fileUpload(file){
	return (dispatch) => {
		return dataUpload(getUserDetailsOrRestart.get().userToken,file).then(([response, json]) =>{
			if(response.status === 200){
				dispatch(fileUploadSuccess(json))
			}
			else{
				dispatch(fileUploadError(json))
			}
		})
	}
}
function fetchDataSourceList(token) {
	return fetch(API+'/api/datasource/get_config_list',{
		method: 'get',
		headers: getHeader(token)
	}).then( response => Promise.all([response, response.json()]));
}

export function saveFileToStore(files) {
	$("#fileErrorMsg").addClass("visibilityHidden");
	return {
		type: "DATA_UPLOAD_FILE",
		files
	}
}
export function updateSelectedDataSrc(selectedDataSrcType) {
	return {
		type: "DATA_SOURCE_SELECTED_TYPE",
		selectedDataSrcType
	}
}
export function updateDbDetails(evt){
    $("#"+evt.target.id).css("border-color","#e0e0e0");
}

export function clearDataUploadFile(){
	return {
		type: "CLEAR_DATA_UPLOAD_FILE"
	}
}
