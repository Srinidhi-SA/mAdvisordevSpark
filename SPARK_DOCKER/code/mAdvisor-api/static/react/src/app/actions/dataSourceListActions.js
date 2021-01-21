import {API} from "../helpers/env";
import {HOST,PORT,SCHEMA,USERNAME,PASSWORD,TABLENAME,getUserDetailsOrRestart} from "../helpers/helper";

function getHeader(token){
	return {
		'Authorization': token,
		'Content-Type': 'application/json'
	};
}

export function getDataSourceList(){
	return (dispatch) => {
		return fetchDataSourceList(getUserDetailsOrRestart.get().userToken).then(([response, json]) =>{
			if(response.status === 200){
				dispatch(fetchDataSrcSuccess(json))
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
function fetchDataSourceList(token,file) {
	return fetch(API+'/api/datasource/get_config_list',{
		method: 'get',
		headers: getHeader(token)
	}).then( response => Promise.all([response, response.json()]));
}

export function saveFileToStore(files) {
	$("#fileErrorMsg").addClass("visibilityHidden");
	var file = files[0]
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
	/*if(evt.target.name.toLowerCase() == HOST.toLowerCase()){
		var host  = evt.target.value;
		return {
			type: "DB_HOST_NAME",
			host
		}
	}
	else if(evt.target.name.toLowerCase() == PORT.toLowerCase()){
		var port  = evt.target.value;
		return {
			type: "DB_PORT_NAME",
			port
		}
	}
	else if(evt.target.name.toLowerCase() == USERNAME.toLowerCase()){
		var username  = evt.target.value;
		return {
			type: "DB_USER_NAME",
			username
		}
    }
	else if(evt.target.name.toLowerCase() == SCHEMA.toLowerCase()){
		var schema  = evt.target.value;
		return {
			type: "DB_SCHEMA",
			schema
		}
    }
	else if(evt.target.name.toLowerCase() == PASSWORD.toLowerCase()){
		var password  = evt.target.value;
		return {
			type: "DB_PASSWORD",
			password
		}
    }
	else if(evt.target.name.toLowerCase() == TABLENAME.toLowerCase()){
		var tablename  = evt.target.value;
		return {
			type: "DB_TABLENAME",
			tablename
		}
    }*/
}

export function clearDataUploadFile(){
	return {
		type: "CLEAR_DATA_UPLOAD_FILE"
	}
}
