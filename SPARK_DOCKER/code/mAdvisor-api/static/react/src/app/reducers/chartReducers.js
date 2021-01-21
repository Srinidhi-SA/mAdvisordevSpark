export default function reducer(state = {
	chartObj:{},
	date:{},
	cloudImgResp:{},
	cloudImgFlag:false

}, action) {

	switch (action.type) {
		case "CHART_OBJECT":
		{
			return {
				...state,
				chartObj: action.chartObj
			}
		}
		break;
		case "C3_DATE":
		{
			let curDateInfo = state.date
			curDateInfo[action.name] = action.value
			return {
				...state,
				date: curDateInfo
			}
		}
		break;
		case "SET_CLOUD_IMG_LOADER":{
			return {
				...state,
				cloudImgFlag : action.flag
			}
		}
		case "CLOUD_IMG_RESPONSE":
		{
			return {
				...state,
				cloudImgResp : action.jsn
			}
		}
		break;
		case "CLEAR_C3_DATE":
		{
			return{
				...state,
				date : {},
			}
		}
	}
	return state
}
