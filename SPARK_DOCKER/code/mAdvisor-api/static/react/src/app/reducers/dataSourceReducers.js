export default function reducer(state = {
		dataSourceList:{},
		fileUpload:{},
		selectedDataSrcType:"fileUpload"
}, action) {
	if(window.location.href.includes("autoML")){
	$("#left-tabs-example-tab-MySQL").css("cursor", "not-allowed");
	$("#left-tabs-example-tab-mssql").css("cursor", "not-allowed");
	$("#left-tabs-example-tab-Hana").css("cursor", "not-allowed");
	$("#left-tabs-example-tab-Hdfs").css("cursor", "not-allowed");
	$("#left-tabs-example-tab-S3").css("cursor", "not-allowed");
	}
	switch (action.type) {
	case "DATA_SOURCE_LIST":
	{
		return {
			...state,
			dataSourceList:action.dataSrcList,
		}
	}
	break;
	case "DATA_SOURCE_SELECTED_TYPE":
	{
		return {
			...state,
			selectedDataSrcType:action.selectedDataSrcType,
		}
	}
	break;
	case "DATA_UPLOAD_FILE":
	{
		return {
			...state,
			fileUpload:action.files,
		}
	}
	break;
	case "CLEAR_DATA_UPLOAD_FILE":
	{
		return {
			...state,
			fileUpload:{},
		}
	}
	break;
	}
	return state
}
