export default function reducer(state = {
		dataUploadShowModal:false,
		imgUploadShowModal:false,
}, action) {

	switch (action.type) {
	case "SHOW_MODAL":
	{
		return {
			...state,
			dataUploadShowModal:true,
		}
	}
	break;

	case "HIDE_MODAL":
	{
		return {
			...state,
			dataUploadShowModal:false,
		}
	}
	break;
	case "SHOW_IMG_MODAL":
	{
		return {
			...state,
			imgUploadShowModal:true,
		}
	}
	break;
	case "HIDE_IMG_MODAL":
	{
		return {
			...state,
			imgUploadShowModal:false,
		}
	}
	break;
 }
return state
}
