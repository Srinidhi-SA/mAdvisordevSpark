export default function reducer(state = {
		dataSourceList:{},
		fileUpload:{},
		selectedDataSrcType:"fileUpload",
		dataSourceLoaderFlag: true
}, action) {
	switch (action.type) {
	case "DATA_SOURCE_LIST":
	{
		return {
			...state,
			dataSourceList:action.dataSrcList,
		}
	}
	break;
	case "DATA_SOURCE_FLAG":{
		return{
			...state,
			dataSourceLoaderFlag : action.flag
		}
	}
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
