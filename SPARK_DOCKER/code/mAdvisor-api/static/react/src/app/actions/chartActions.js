import { getUserDetailsOrRestart } from "../helpers/helper";
import { getHeader } from "./appActions";
import { API } from "../helpers/env";
import store from "../store";

export function chartObjStore(chartObj) {
	return {
		type: "CHART_OBJECT",
		chartObj
	}
}
export function chartdate(name,value) {
	return {
		type: "C3_DATE",name,value
	}
}

export function setCloudImageLoader(flag){
	return {
		type: "SET_CLOUD_IMG_LOADER",flag
	}
}
export function fetchWordCloudImg(data){
	return (dispatch) => {
		return fetchWordCloudImgAPI(data,getUserDetailsOrRestart.get().userToken,dispatch).then(([response,json]) => {
			if(response.status === 200){
				dispatch(setCloudImageLoader(false));
				dispatch(wordCloudImgResponse(json));
			}else{
				bootbox.alert(statusMessages("warning","Failed","small_mascot"));
			}
		})
	}
}
function fetchWordCloudImgAPI(data,token){
	return fetch(API+"/api/stockdataset/"+data.slug+"/fetch_word_cloud/?symbol="+data.symbol+"&date="+data.date,{
		method : "get",
		headers : getHeader(token),
	}).then(response => Promise.all([response,response.json()]));
}
export function clearCloudImgResp(){
	let jsn = {}
	return {
		type: "CLOUD_IMG_RESPONSE",jsn
	}
}
export function wordCloudImgResponse(jsn) {
	return {
		type: "CLOUD_IMG_RESPONSE",jsn
	}
}
export function clearC3Date(){
	return {
		type: "CLEAR_C3_DATE"
	}
}
