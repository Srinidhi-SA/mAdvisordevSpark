//all the ocr related actions..
import { API } from "../helpers/env";
import { getUserDetailsOrRestart, statusMessages } from "../helpers/helper";
import store from "../store";
function getHeader(token) {
	return {
		Authorization: token
	};
};

export function getHeaderForJson(token) {
	return { Authorization: token, 'Content-Type': 'application/json' };
}

export function saveOcrFilesToStore(files) {
	return {
		type: "OCR_UPLOAD_FILE",
		files
	}
}

export function saveImagePageFlag(flag) {
	return {
		type: "SAVE_IMAGE_FLAG",
		flag
	}
}
export function saveDocumentPageFlag(flag) {
	return {
		type: "SAVE_DOCUMENT_FLAG",
		flag
	}
}
export function saveRevDocumentPageFlag(flag) {
	return {
		type: "SAVE_REV_DOCUMENT_FLAG",
		flag
	}
}

export function saveImageDetails(data) {
	return {
		type: "SAVE_IMAGE_DETAILS",
		data
	}
}
export function pdfPagination(data) {
	return {
		type: "PDF_PAGINATION",
		data
	}
}

export function clearImageDetails() {
	return {
		type: "CLEAR_IMAGE_DETAILS",
	}
}
//Actions for fetching Projects list 
export function updateOcrImage(data) {
	return {
		type: "UPDATE_OCR_IMAGE",
		data
	}
}

export function updateCustomImage(data) {
	return {
		type: "UPDATE_CUSTOM_IMAGE",
		data
	}
}

export function getOcrProjectsList(pageNo) {
	return (dispatch) => {
		return fetchProjects(pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(fetchProjectsSuccess(json))
			}
			else {
				dispatch(fetchProjectsFail(json))
			}
		})
	}
}

function fetchProjects(pageNo = store.getState().ocr.projectPage, token) {
	let search_project = store.getState().ocr.search_project;
	let ProjectPageSize = store.getState().ocr.projectTablePagesize;
	var userRole = getUserDetailsOrRestart.get().userRole
	if(ProjectPageSize==="All"){
			if (userRole == "ReviewerL1" || userRole == "ReviewerL2") {
					return fetch(API + '/ocr/project/reviewer/?page_number=' + pageNo + '&name=' + search_project + '&page=' + ProjectPageSize, {
						method: 'get',
						headers: getHeader(token)
					}).then(response => Promise.all([response, response.json()]));
			}
			else {
					return fetch(API + '/ocr/project/?name=' + search_project + '&page_number=' + pageNo + '&page=' + ProjectPageSize, {
						method: 'get',
						headers: getHeader(token)
					}).then(response => Promise.all([response, response.json()]));
			}
	}
	else{
				if (userRole == "ReviewerL1" || userRole == "ReviewerL2") {
					return fetch(API + '/ocr/project/reviewer/?page_number=' + pageNo + '&name=' + search_project + '&page_size=' + ProjectPageSize, {
						method: 'get',
						headers: getHeader(token)
					}).then(response => Promise.all([response, response.json()]));
			}
			else {
					return fetch(API + '/ocr/project/?name=' + search_project + '&page_number=' + pageNo + '&page_size=' + ProjectPageSize, {
						method: 'get',
						headers: getHeader(token)
					}).then(response => Promise.all([response, response.json()]));
			}	
	}
}

export function fetchProjectsSuccess(doc) {
	var data = doc;
	return {
		type: "OCR_PROJECT_LIST",
		data,
	}
}

export function fetchProjectsFail(data) {
	return {
		type: "OCR_PROJECT_LIST_FAIL",
		data,
	}
}
////

//Actions for fetching documentlist based on the 'Project' selected
export function getOcrUploadedFiles(pageNo) {
	return (dispatch) => {
		return fetchUploadedFiles(pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(fetchUploadsSuccess(json))
				dispatch(setProjectTabLoaderFlag(false));
			}
			else {
				dispatch(fetchUploadsFail(json))
			}
		})
	}
}

function fetchUploadedFiles(pageNo = store.getState().ocr.docTablePage, token) {
	let filter_assignee = store.getState().ocr.filter_assignee
	let filter_status = store.getState().ocr.filter_status
	let filter_confidence = store.getState().ocr.filter_confidence
	let search_document = store.getState().ocr.search_document
	let selected_project_slug = store.getState().ocr.selected_project_slug
	let tabActive = store.getState().ocr.tabActive == '' ? 'active' : store.getState().ocr.tabActive;
	let filter_fields = store.getState().ocr.filter_fields
	let filter_template = store.getState().ocr.filter_template
	let pageSize = store.getState().ocr.docTablePagesize
	if (search_document == '' && pageSize != "All") {
		return fetch(API + '/ocr/ocrimage/get_ocrimages/?projectslug=' + selected_project_slug + '&imageStatus=' + tabActive + '&status=' + filter_status + '&confidence=' + filter_confidence + '&fields=' + filter_fields + '&assignee=' + filter_assignee + '&template=' + filter_template + '&page_number=' + pageNo + '&page_size=' + pageSize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else if (search_document == '' && pageSize === "All") {
		return fetch(API + '/ocr/ocrimage/get_ocrimages/?projectslug=' + selected_project_slug + '&imageStatus=' + tabActive + '&status=' + filter_status + '&confidence=' + filter_confidence + '&fields=' + filter_fields + '&assignee=' + filter_assignee + '&template=' + filter_template + '&page=' + pageSize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else {
		return fetch(API + '/ocr/ocrimage/get_ocrimages/?projectslug=' + selected_project_slug + '&imageStatus=' + tabActive + '&name=' + search_document + '&status=' + filter_status + '&confidence=' + filter_confidence + '&fields=' + filter_fields + '&assignee=' + filter_assignee + '&template=' + filter_template + '&page_number=' + pageNo + '&page_size=' + pageSize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]))
	};
}

export function fetchUploadsSuccess(doc) {
	var data = doc;
	return {
		type: "OCR_UPLOADS_LIST",
		data,
	}
}

export function fetchUploadsFail(data) {
	return {
		type: "OCR_UPLOADS_LIST_FAIL",
		data,
	}
}
export function docTablePage(page) {
	return {
		type: "DOC_TABLE_PAGE",
		page,
	}
}
export function docTablePagesize(pagesize) {
	return {
		type: "DOC_TABLE_PAGESIZE",
		pagesize,
	}
}
export function rDocTablePagesize(pagesize) {
	return {
		type: "RDOC_TABLE_PAGESIZE",
		pagesize,
	}
}
export function projectTablePagesize(pagesize) {
	return {
		type: "PROJECT_TABLE_PAGESIZE",
		pagesize,
	}
}
export function userTablePagesize(pagesize) {
	return {
		type: "USER_TABLE_PAGESIZE",
		pagesize,
	}
}
export function ReviewerTablePagesize(pagesize) {
	return {
		type: "REVIEWER_TABLE_PAGESIZE",
		pagesize,
	}
}
export function projectPage(page) {
	return {
		type: "PROJECT_PAGE",
		page,
	}
}
////
export function setProjectTabLoaderFlag(flag) {
	return {
		type: "SET_PROJECT_TAB_LOADER_FLAG", flag
	}
}
//Actions for Reviewers list 
export function getOcrReviewersList(pageNo) {
	return (dispatch) => {
		return fetchReviewersList(pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(fetchReviewersSuccess(json))
			}
			else {
				dispatch(fetchReviewersFail(json))
			}
		})
	}
}

function fetchReviewersList(pageNo = 1, token) {
	let filter_rev_time = store.getState().ocr.filter_rev_time;
	let filter_rev_accuracy = store.getState().ocr.filter_rev_accuracy;
	let reviewerTablePagesize = store.getState().ocr.reviewerTablePagesize;
	if (reviewerTablePagesize === "All"){
	return fetch(API + '/ocr/user/reviewer_detail_list/?time=' + filter_rev_time + '&accuracy=' + filter_rev_accuracy + '&page_number=' + pageNo  + '&page=' + reviewerTablePagesize, {
		method: 'get',
		headers: getHeader(token)
	}).then(response => Promise.all([response, response.json()]));
}
else{
	return fetch(API + '/ocr/user/reviewer_detail_list/?time=' + filter_rev_time + '&accuracy=' + filter_rev_accuracy + '&page_number=' + pageNo  + '&page_size=' + reviewerTablePagesize, {
		method: 'get',
		headers: getHeader(token)
	}).then(response => Promise.all([response, response.json()]));
}
}

export function fetchReviewersSuccess(doc) {
	var data = doc;
	return {
		type: "OCR_REVIEWERS_LIST",
		data,
	}
}

export function fetchReviewersFail(data) {
	return {
		type: "OCR_REVIEWERS_LIST_FAIL",
		data,
	}
}
////

//Actions for fetching documentlist based on the 'Reviewer' selected
export function getRevrDocsList(pageNo) {
	return (dispatch) => {
		return fetchRevrDocsList(pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(fetchRevrDocsSuccess(json))
			}
			else {
				dispatch(fetchRevrDocsFail(json))
			}
		})
	}
}

function fetchRevrDocsList(pageNo = 1, token) {
	let filter_rd_fields = store.getState().ocr.filter_rd_fields
	let filter_rd_template = store.getState().ocr.filter_rd_template
	let filter_rd_status = store.getState().ocr.filter_rd_status
	let filter_rd_confidence = store.getState().ocr.filter_rd_confidence
	let selected_reviewer_name = store.getState().ocr.selected_reviewer_name
	let search_project = store.getState().ocr.search_project_in_revtable
	let selected_project_name = store.getState().ocr.selected_project_name
	let rPageSize = store.getState().ocr.rDocTablePagesize

	var userRole = getUserDetailsOrRestart.get().userRole
	if (rPageSize != "All") {
		if (userRole == "ReviewerL1" || userRole == "ReviewerL2") {
			return fetch(API + '/ocrflow/review/assigned_requests/?username=' + getUserDetailsOrRestart.get().userName + '&reviewStatus=' + filter_rd_status + '&template=' + filter_rd_template + '&accuracy=' + filter_rd_confidence + '&project=' + selected_project_name + '&field_count=' + filter_rd_fields + '&page_number=' + pageNo + '&page_size=' + rPageSize, {
				method: 'get',
				headers: getHeader(token)
			}).then(response => Promise.all([response, response.json()]))
		}
		else {
			return fetch(API + '/ocrflow/review/assigned_requests/?username=' + selected_reviewer_name + '&reviewStatus=' + filter_rd_status + '&template=' + filter_rd_template + '&accuracy=' + filter_rd_confidence + '&project=' + search_project + '&field_count=' + filter_rd_fields + '&page_number=' + pageNo + '&page_size=' + rPageSize, {
				method: 'get',
				headers: getHeader(token)
			}).then(response => Promise.all([response, response.json()]))
		}
	}
	if (rPageSize === "All") {
		{
			if (userRole == "ReviewerL1" || userRole == "ReviewerL2") {
				return fetch(API + '/ocrflow/review/assigned_requests/?username=' + getUserDetailsOrRestart.get().userName + '&reviewStatus=' + filter_rd_status + '&template=' + filter_rd_template + '&accuracy=' + filter_rd_confidence + '&project=' + selected_project_name + '&field_count=' + filter_rd_fields + '&page=' + rPageSize, {
					method: 'get',
					headers: getHeader(token)
				}).then(response => Promise.all([response, response.json()]))
			}
			else {
				return fetch(API + '/ocrflow/review/assigned_requests/?username=' + selected_reviewer_name + '&reviewStatus=' + filter_rd_status + '&template=' + filter_rd_template + '&accuracy=' + filter_rd_confidence + '&project=' + search_project + '&field_count=' + filter_rd_fields + '&page=' + rPageSize, {
					method: 'get',
					headers: getHeader(token)
				}).then(response => Promise.all([response, response.json()]))
			}
		}
	}
}

export function fetchRevrDocsSuccess(doc) {
	var data = doc;
	return {
		type: "OCR_REV_DOCS_LIST",
		data,
	}
}

export function fetchRevrDocsFail(data) {
	return {
		type: "OCR_REV_DOCS_LIST_FAIL",
		data,
	}
}
////

export function setS3Loader(flag) {
	return {
		type: "SET_S3_LOADER", flag
	}
}

export function saveS3BucketDetails(name, val) {
	return {
		type: "SAVE_S3_BUCKET_DETAILS",
		name,
		val,
	}
}

export function clearS3Data() {
	return {
		type: "CLEAR_S3_DATA"
	}
}

export function getS3BucketFileList(s3BucketDetails) {
	return (dispatch) => {
		return fetchS3FileDetails(s3BucketDetails, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.status != "FAILED") {
				dispatch(fetchs3DetailsSuccess(json))
			} else if (response.status === 200 && json.status === "FAILED") {
				dispatch(fetchs3DetailsError(true));
				dispatch(s3FetchErrorMsg(json.message));
			} else {
				dispatch(fetchs3DetailsError(true))
			}
		})
	}
}

function fetchS3FileDetails(s3BucketDetails, token) {
	return fetch(API + '/ocr/ocrimage/get_s3_files/', {
		method: 'post',
		headers: getHeaderForJson(token),
		body: JSON.stringify(s3BucketDetails)
	}).then(response => Promise.all([response, response.json()]));
}

export function fetchs3DetailsSuccess(data) {
	var len = (data.file_list).length;
	let fileList = [];
	for (var i = 0; i < len; i++) {
		if (/\.(jpe?g|tif|png|pdf)$/i.test(data.file_list[i])) {
			fileList.push(data.file_list[i]);
		}
	}
	return {
		type: "SAVE_S3_FILE_LIST", fileList
	}
}

export function fetchs3DetailsError(flag) {
	return {
		type: "S3_FILE_ERROR_MSG", flag
	}
}
export function s3FetchErrorMsg(msg) {
	return {
		type: "S3_FETCH_ERROR_MSG", msg
	}
}
export function saveS3SelFiles(fileName) {
	return {
		type: "SAVE_SEL_S3_FILES", fileName
	}
}

export function uploadS3Files(selectedFiles, projectSlug) {
	let data = Object.assign({ "dataSourceType": "S3" }, { "file_names": selectedFiles }, store.getState().ocr.ocrS3BucketDetails, { "projectslug": projectSlug })
	return (dispatch) => {
		return uploadS3FilesAPI(data, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.message != "FAILED") {
				dispatch(uploadS3FileSuccess(true));
			} else if (response.status === 200 && json.message === "FAILED") {
				dispatch(uploadS3FileError())
			} else {
				dispatch(uploadS3FileError())
			}
		})
	}
}
function uploadS3FilesAPI(data, token) {
	return fetch(API + '/ocr/ocrimage/', {
		method: 'post',
		headers: getHeaderForJson(token),
		body: JSON.stringify(data)
	}).then(response => Promise.all([response, response.json()]));
}
export function uploadS3FileSuccess(flag) {
	return {
		type: "SET_S3_UPLOADED", flag
	}
}
export function uploadS3FileError() {
	return {
		type: "S3_FILE_UPLOAD_ERROR_MSG"
	}
}
export function storeOcrSortElements(ocrFilesSortOn, ocrFilesSortType) {
	return {
		type: "OCR_FILES_SORT",
		ocrFilesSortOn,
		ocrFilesSortType
	}
}
export function storeOcrFilterStatus(status) {
	return {
		type: "FILTER_BY_STATUS",
		status,
	}
}
export function storeOcrFilterConfidence(confidence) {
	return {
		type: "FILTER_BY_CONFIDENCE",
		confidence,
	}
}
export function storeOcrFilterAssignee(assignee) {
	return {
		type: "FILTER_BY_ASSIGNEE",
		assignee
	}
}
export function storeOcrFilterTemplate(template) {
	return {
		type: "FILTER_BY_TEMPLATE",
		template
	}
}
export function storeOcrFilterFields(fields) {
	return {
		type: "FILTER_BY_FIELDS",
		fields
	}
}
export function ocrRdFilterStatus(status) {
	return {
		type: "FILTER_RD_BY_STATUS",
		status,
	}
}
export function ocrRdFilterConfidence(confidence) {
	return {
		type: "FILTER_RD_BY_CONFIDENCE",
		confidence,
	}
}

export function ocrRdFilterFields(fields) {
	return {
		type: "FILTER_RD_BY_FIELDS",
		fields
	}
}

export function ocrRdFiltertemplate(template) {
	return {
		type: "FILTER_RD_BY_TEMPLATE",
		template
	}
}

export function ocrRevFilterTime(time) {
	return {
		type: "FILTER_REV_BY_TIME",
		time,
	}
}

export function ocrRevFilterAccuracy(accuracy) {
	return {
		type: "FILTER_REV_BY_ACCURACY",
		accuracy
	}
}
export function updateCheckList(list) {
	return {
		type: "UPDATE_CHECKLIST",
		list
	}
}
//Actions for Manage User screen
export function openAddUserPopup() {
	return {
		type: "OPEN_ADD_USER_POPUP"
	}
}
export function closeAddUserPopup() {
	return {
		type: "CLOSE_ADD_USER_POPUP"
	}
}
export function setUserTableLoaderFlag(flag) {
	return {
		type: "SET_USER_TABLE_LOADER_FLAG", flag
	}
}

export function fetchAllOcrUsersAction(pageNo) {
	return (dispatch) => {
		return fetchAllOcrUsersAPI(pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(saveAllOcrUsersList(json));
				dispatch(setUserTableLoaderFlag(false));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to fetch", "small_mascot"));
			}
		})
	}
}
export function fetchAllOcrUsersAPI(pageNo, token) {
	if (pageNo === undefined) {
		pageNo = 1;
	}
	let searchElement = store.getState().ocr.ocrSearchElement;
	let userTablePagesize = store.getState().ocr.userTablePagesize;
	if (userTablePagesize === "All") {
	if (searchElement != "") {
		return fetch(API + '/ocr/user/?first_name=' + searchElement + '&page_number=' + pageNo + '&page=' + userTablePagesize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else {
		return fetch(API + "/ocr/user/?page_number=" + pageNo + '&page=' + userTablePagesize, {
			method: "get",
			headers: getHeaderForJson(token),
		}).then(response => Promise.all([response, response.json()]));
	}
}
else{
	if (searchElement != "") {
		return fetch(API + '/ocr/user/?first_name=' + searchElement + '&page_number=' + pageNo + '&page_size=' + userTablePagesize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else {
		return fetch(API + "/ocr/user/?page_number=" + pageNo + '&page_size=' + userTablePagesize, {
			method: "get",
			headers: getHeaderForJson(token),
		}).then(response => Promise.all([response, response.json()]));
	}
}
}
function saveAllOcrUsersList(json) {
	return {
		type: "SAVE_ALL_OCR_USERS_LIST",
		json
	}
}

export function storeSelectedTabId(id) {
	return {
		type: "SELECTED_TAB_ID", id
	}
}
export function fetchOcrListByReviewerType(id, pageNo) {
	return (dispatch) => {
		return fetchOcrListByReviewerTypeAPI(id, pageNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(saveAllOcrUsersList(json));
				dispatch(setUserTableLoaderFlag(false));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to fetch", "small_mascot"));
			}
		})
	}
}
function fetchOcrListByReviewerTypeAPI(id, pageNo, token) {
	if (pageNo === undefined) {
		pageNo = 1;
	}
	let searchElement = store.getState().ocr.ocrSearchElement;
	let userTablePagesize = store.getState().ocr.userTablePagesize;

	if (userTablePagesize === "All") {
	if (searchElement != "") {
		return fetch(API + "/ocr/user/reviewer_list/?role=" + id + "&first_name=" + searchElement + "&page_number=" + pageNo + '&page=' + userTablePagesize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else {
		return fetch(API + "/ocr/user/reviewer_list/?role=" + id + "&page_number=" + pageNo + '&page=' + userTablePagesize, {
			method: "get",
			headers: getHeaderForJson(token),
		}).then(response => Promise.all([response, response.json()]));
	}
}else{
	if (searchElement != "") {
		return fetch(API + "/ocr/user/reviewer_list/?role=" + id + "&first_name=" + searchElement + "&page_number=" + pageNo + '&page_size=' + userTablePagesize, {
			method: 'get',
			headers: getHeader(token)
		}).then(response => Promise.all([response, response.json()]));
	}
	else {
		return fetch(API + "/ocr/user/reviewer_list/?role=" + id + "&page_number=" + pageNo + '&page_size=' + userTablePagesize, {
			method: "get",
			headers: getHeaderForJson(token),
		}).then(response => Promise.all([response, response.json()]));
	}	
}
}

export function getReviewersListAction() {
	return (dispatch) => {
		return getReviewersListApi(getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(saveReviewersList(json));
			} else {
				bootbox.alert(statusMessages("warning", "No roles found", "small_mascot"));
			}
		})
	}
}
export function getallAppsList() {
	return (dispatch) => {
		return getallApps(getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(saveAppsList(json.appIDMapping));
			} else {
				bootbox.alert(statusMessages("warning", "List of Apps is empty", "small_mascot"));
			}
		})
	}
}
function getReviewersListApi(token) {
	return fetch(API + "/ocr/groups/", {
		method: "get",
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}

function getallApps(token) {
	return fetch(API + "/api/get_app_id_map/", {
		method: "get",
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}
export function saveReviewersList(json) {
	return {
		type: "SAVE_REVIEWERS_LIST", json
	}
}
export function saveAppsList(data) {
	return {
		type: "SAVE_APPS_LIST", data
	}
}

export function saveNewUserDetails(name, value) {
	return {
		type: "SAVE_NEW_USER_DETAILS", name, value
	}
}
export function setCreateUserLoaderFlag(flag) {
	return {
		type: "SET_CREATE_USER_LOADER_FLAG", flag
	}
}
export function createNewUserAction(userDetails) {
	var formdt = new FormData();
	for (let key in userDetails) {
		formdt.append(key, userDetails[key]);
	}
	return (dispatch) => {
		return createNewUserAPI(formdt, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.created) {
				dispatch(createNewUserSuccess(json.created, json.ocr_profile_slug));
				dispatch(setCreateUserLoaderFlag(false));
			} else if (response.status === 200 && !json.created) {
				dispatch(setCreateUserLoaderFlag(false));
				$("#resetMsg")[0].innerText = Object.values(json.message[Object.keys(json.message)[0]])[0]
			} else {
				bootbox.alert(statusMessages("warning", "Failed", "small_mascot"));
			}
		})
	}
}
function createNewUserAPI(data, token) {
	return fetch(API + "/ocr/user/", {
		method: "post",
		headers: getHeader(token),
		body: data,
	}).then(response => Promise.all([response, response.json()]));
}
function createNewUserSuccess(flag, slug) {
	return {
		type: "CREATE_NEW_USER_SUCCESS", flag, slug
	}
}

export function saveNewUserProfileDetails(name, value) {
	return {
		type: "SAVE_NEW_USER_PROFILE", name, value
	}
}
export function submitNewUserProfileAction(userProfileDetails, curUserSlug) {
	return (dispatch) => {
		return submitNewUserProfileAPI(userProfileDetails, curUserSlug, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.updated) {
				dispatch(userProfileCreationSuccess(json.updated));
			} else if (response.status === 200 && !json.updated) {
				bootbox.alert(statusMessages("warning", json.message, "small_mascot"));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to update roles or status", "small_mascot"));
			}
		})
	}
}
function submitNewUserProfileAPI(data, slug, token) {
	return fetch(API + "/ocr/userprofile/" + slug + "/", {
		method: "put",
		headers: getHeaderForJson(token),
		body: JSON.stringify(data)
	}).then(response => Promise.all([response, response.json()]));
}
function userProfileCreationSuccess(flag) {
	return {
		type: "USER_PROFILE_CREATED_SUCCESS", flag
	}
}

export function saveSelectedOcrUserList(curSelList) {
	return {
		type: "SAVE_SELECTED_USERS_LIST", curSelList
	}
}

export function selectAllOcrUsers(flag) {
	return {
		type: "SELECT_ALL_USERS", flag
	}
}

export function deleteOcrUserAction(userNames) {
	let data = { "username": userNames }
	return (dispatch) => {
		return deleteOcrActionAPI(data, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.deleted) {
				store.getState().ocr.selectedTabId === "none" ?
					dispatch(fetchAllOcrUsersAction(store.getState().ocr.ocrUserPageNum))
					: dispatch(fetchOcrListByReviewerType(parseFloat(store.getState().ocr.selectedTabId), store.getState().ocr.ocrUserPageNum));
				bootbox.alert(statusMessages("success", json.message, "small_mascot"));
				dispatch(clearUserFlagAction());
				dispatch(deleteUserFlag(false));
			} else if (response.status === 200 && !json.deleted) {
				bootbox.alert(statusMessages("warning", "Unable to delete", "small_mascot"));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to delete", "small_mascot"));
			}
		})
	}
}
function deleteOcrActionAPI(data, token) {
	return fetch(API + "/ocr/user/", {
		method: "delete",
		headers: getHeaderForJson(token),
		body: JSON.stringify(data)
	}).then(response => Promise.all([response, response.json()]));
}

export function activateOcrUserAction(userNames) {
	let data = { "username": userNames, "is_active": "True" }
	return (dispatch) => {
		return activateOcrActionAPI(data, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.updated) {
				store.getState().ocr.selectedTabId === "none" ?
					dispatch(fetchAllOcrUsersAction(store.getState().ocr.ocrUserPageNum))
					: dispatch(fetchOcrListByReviewerType(parseFloat(store.getState().ocr.selectedTabId), store.getState().ocr.ocrUserPageNum));
				bootbox.alert(statusMessages("success", json.message, "small_mascot"));
				dispatch(clearUserFlagAction());
			} else if (response.status === 200 && !json.updated) {
				bootbox.alert(statusMessages("warning", "Unable activate users", "small_mascot"));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to activate", "small_mascot"));
			}
		})
	}
}
function activateOcrActionAPI(data, token) {
	return fetch(API + "/ocr/userprofile/edit_status/", {
		method: "post",
		headers: getHeaderForJson(token),
		body: JSON.stringify(data)
	}).then(response => Promise.all([response, response.json()]));
}

export function deActivateOcrUserAction(userNames) {
	let data = { "username": userNames, "is_active": "False" }
	return (dispatch) => {
		return deActivateOcrActionAPI(data, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.updated) {
				store.getState().ocr.selectedTabId === "none" ?
					dispatch(fetchAllOcrUsersAction(store.getState().ocr.ocrUserPageNum))
					: dispatch(fetchOcrListByReviewerType(parseFloat(store.getState().ocr.selectedTabId), store.getState().ocr.ocrUserPageNum));
				dispatch(clearUserFlagAction());
				bootbox.alert(statusMessages("success", json.message, "small_mascot"));
			} else if (response.status === 200 && !json.updated) {
				bootbox.alert(statusMessages("warning", "Unable deactivate users", "small_mascot"));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to deactivate", "small_mascot"));
			}
		})
	}
}
function deActivateOcrActionAPI(data, token) {
	return fetch(API + "/ocr/userprofile/edit_status/", {
		method: "post",
		headers: getHeaderForJson(token),
		body: JSON.stringify(data)
	}).then(response => Promise.all([response, response.json()]));
}

export function openEditUserModalAction(flag, userSlug, userDt) {
	let edtDet = store.getState().ocr.editedUserDetails;
	edtDet.first_name = userDt.first_name;
	edtDet.last_name = userDt.last_name;
	edtDet.username = userDt.username;
	edtDet.email = userDt.email;
	edtDet.role = userDt.ocr_profile.role[0];
	edtDet.is_active = userDt.ocr_profile.active ? "True" : "False";
	edtDet.appList = userDt.custom_app_perm.app_list.map(i => i.app_id);

	return {
		type: "OPEN_EDIT_USER_POPUP", flag, userSlug, userDt, edtDet
	}
}
export function closeEditUserModalAction(flag) {
	return {
		type: "CLOSE_EDIT_USER_POPUP", flag
	}
}
export function enableEditingUserAction(flag) {
	return {
		type: "ENABLE_EDITING_USER", flag
	}
}
export function SaveEditedUserDetailsAction(name, val) {
	return {
		type: "SAVE_EDITED_USER_DETAILS", name, val
	}
}
export function editDetailsFormAction(flag) {
	return {
		type: "FORM_DETAILS_SELECTED", flag
	}
}
export function editRolesFormAction(flag) {
	return {
		type: "FORM_ROLES_SELECTED", flag
	}
}
export function submitEditUserDetailsAction(editedUserDt) {
	var formdt = new FormData();
	for (let key in editedUserDt) {
		formdt.append(key, editedUserDt[key]);
	}
	return (dispatch) => {
		return submitEditUserDetailsAPI(formdt, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.updated) {
				dispatch(setCreateUserLoaderFlag(false));
				dispatch(editUserSuccess(true));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to Edit user details", "small_mascot"));
			}
		})
	}
}
function submitEditUserDetailsAPI(data, token) {
	return fetch(API + "/ocr/user/edit/", {
		method: "post",
		headers: getHeader(token),
		body: data,
	}).then(response => Promise.all([response, response.json()]));
}
export function submitEditedUserRolesAction(editedUserDt, reviewersList, slug) {
	editedUserDt.role = reviewersList.filter(i => i.name === editedUserDt.role)[0].id
	return (dispatch) => {
		return submitEditedUserRolesAPI(editedUserDt, slug, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200 && json.updated) {
				dispatch(setCreateUserLoaderFlag(false));
				dispatch(editUserSuccess(true));
			} else {
				bootbox.alert(statusMessages("warning", "Failed to edit user roles", "small_mascot"));
			}
		})
	}
}
function submitEditedUserRolesAPI(data, slug, token) {
	let curDt = { "is_active": data.is_active, "role": parseFloat(data.role), "app_list": data.appList }
	return fetch(API + "/ocr/userprofile/" + slug + "/", {
		method: "put",
		headers: getHeaderForJson(token),
		body: JSON.stringify(curDt),
	}).then(response => Promise.all([response, response.json()]));
}
export function editUserSuccess(flag) {
	return {
		type: "EDIT_USER_SUCCESS", flag
	}
}
export function storeDocSearchElem(elem) {
	return {
		type: "SEARCH_OCR_DOCUMENT",
		elem
	}
}
export function storeProjectSearchElem(elem) {
	return {
		type: "SEARCH_OCR_PROJECT",
		elem
	}
}
export function storeSearchInRevElem(elem) {
	return {
		type: "SEARCH_OCR_PROJECT_IN_REV",
		elem
	}
}
export function tabActiveVal(elem) {
	return {
		type: "TAB_ACTIVE_VALUE",
		elem
	}
}
export function clearUserFlagAction() {
	return {
		type: "CLEAR_USER_FLAG"
	}
}
export function saveUserSearchElementAction(val) {
	return {
		type: "OCR_USER_SEARCH_ELEMENT", val
	}
}
export function saveOcrUserPageNumAction(val) {
	return {
		type: "OCR_USER_PAGE_NUM", val
	}
}
export function clearUserSearchElementAction() {
	return {
		type: "CLEAR_USER_SEARCH_ELEMENT",
	}
}

export function selectedProjectDetails(slug, name) {
	return {
		type: "SELECTED_PROJECT_SLUG",
		slug, name
	}
}
export function selectedReviewerDetails(slug, name) {
	return {
		type: "SELECTED_REVIEWER_DETAILS",
		slug, name
	}
}
export function saveSelectedImageName(name) {
	return {
		type: "SELECTED_IMAGE_NAME",
		name
	}
}
export function saveSelectedTemplate(template) {
	return {
		type: "SELECTED_TEMPLATE",
		template
	}
}
//Configure Page Actions
export function storeSelectedConfigureTabAction(selTab) {
	return {
		type: "SAVE_SEL_CONFIGURE_TAB", selTab
	}
}
export function setIRLoaderFlagAction(flag) {
	return {
		type: "SET_IR_LOADER_FLAG", flag
	}
}
export function fetchReviewersRules() {
	return (dispatch) => {
		return fetchReviewersRulesAPI(getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(saveRulesForConfigPage(json))
			} else {
				bootbox.alert(statusMessages("warning", "Failed", "small_mascot"));
			}
		})
	}
}
function fetchReviewersRulesAPI(token) {
	return fetch(API + "/ocrflow/rules/get_rules/", {
		method: "get",
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}
function saveRulesForConfigPage(data) {
	return {
		type: "SAVE_RULES_FOR_CONFIGURE", data
	}
}
export function fetchInitialReviewerList(roleNo) {
	return (dispatch) => {
		return fetchInitialReviewerListAPI(roleNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(setIRLoaderFlagAction(false))
				dispatch(saveInitialReviewerList(json));
			} else {
				bootbox.alert(statusMessages("warning", "Failed", "small_mascot"));
			}
		})
	}
}
function fetchInitialReviewerListAPI(roleNo, token) {
	return fetch(API + "/ocr/user/get_ocr_users/?role=" + roleNo, {
		method: "get",
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}
export function saveInitialReviewerList(data) {
	return {
		type: "SAVE_IR_LIST", data
	}
}
export function saveIRToggleValAction(val) {
	return {
		type: "STORE_IR_TOGGLE_FLAG", val
	}
}
export function autoAssignmentAction(stage, val) {
	return (dispatch) => {
		return autoAssignmentActionAPI(stage, val, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				bootbox.alert(statusMessages("warning", json.message, "small_mascot"))
			} else {
				bootbox.alert(statusMessages("warning", "Failed", "small_mascot"));
			}
		})
	}
}
function autoAssignmentActionAPI(stage, val, token) {
	let ConvertedVal = val === true ? "True" : "False"
	var formdt = new FormData();
	formdt.append("autoAssignment", ConvertedVal);
	formdt.append("stage", stage);
	return fetch(API + "/ocrflow/rules/autoAssignment/", {
		method: "post",
		body: formdt,
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}
export function saveIRConfigAction(name, value) {
	return {
		type: "SAVE_IR_DATA", name, value
	}
}
export function saveIRSearchElementAction(val) {
	return {
		type: "STORE_IR_SEARCH_ELEMENT", val
	}
}
export function setSRLoaderFlagAction(flag) {
	return {
		type: "SET_SR_LOADER_FLAG", flag
	}
}
export function fetchSeconadryReviewerList(roleNo) {
	return (dispatch) => {
		return fetchSeconadryReviewerListAPI(roleNo, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				dispatch(setSRLoaderFlagAction(false));
				dispatch(saveSeconadryReviewerList(json));
			} else {
				bootbox.alert(statusMessages("warning", "Failed", "small_mascot"));
			}
		})
	}
}
function fetchSeconadryReviewerListAPI(roleNo, token) {
	return fetch(API + "/ocr/user/get_ocr_users/?role=" + roleNo, {
		method: "get",
		headers: getHeader(token),
	}).then(response => Promise.all([response, response.json()]));
}
export function saveSeconadryReviewerList(data) {
	return {
		type: "SAVE_SR_LIST", data
	}
}
export function saveSRToggleValAction(val) {
	return {
		type: "STORE_SR_TOGGLE_FLAG", val
	}
}
export function saveSRSearchElementAction(val) {
	return {
		type: "STORE_SR_SEARCH_ELEMENT", val
	}
}
export function saveSRConfigAction(name, value) {
	return {
		type: "SAVE_SR_DATA", name, value
	}
}
export function submitReviewerConfigAction(selTab, config) {
	let data = {}
	let reviewerConfig = {
		"auto": { "active": "False", "max_docs_per_reviewer": "", "remainaingDocsDistributionRule": "" },
		"custom": { "active": "False", "max_docs_per_reviewer": "", "selected_reviewers": [], "remainaingDocsDistributionRule": "" }
	}
	let rule = "";
	if (selTab === "initialReview") {
		let reqValues1 = { "active": config.active, "selected_reviewers": config.selectedIRList, "max_docs_per_reviewer": parseInt(config.max_docs_per_reviewer), "remainaingDocsDistributionRule": parseInt(config.test) }
		if (reqValues1.active === "all") {
			reqValues1.active = "True"
			reviewerConfig.auto = reqValues1;
			delete (reviewerConfig.auto.selected_reviewers)
		} else if (reqValues1.active === "select") {
			reqValues1.active = "True"
			reviewerConfig.custom = reqValues1;
		}
		data = reviewerConfig
		rule = "modifyRulesL1"
	}
	else if (selTab === "secondaryReview") {
		let reqValues2 = { "active": config.active, "selected_reviewers": config.selectedSRList, "max_docs_per_reviewer": parseInt(config.max_docs_per_reviewer), "remainaingDocsDistributionRule": parseInt(config.test) }
		if (reqValues2.active === "all") {
			reqValues2.active = "True"
			reviewerConfig.auto = reqValues2;
			delete (reviewerConfig.auto.selected_reviewers)
		} else if (reqValues2.active === "select") {
			reqValues2.active = "True"
			reviewerConfig.custom = reqValues2;
		}
		data = reviewerConfig
		rule = "modifyRulesL2"
	}
	return (dispatch) => {
		return submitReviewerConfigAPI(data, rule, getUserDetailsOrRestart.get().userToken, dispatch).then(([response, json]) => {
			if (response.status === 200) {
				bootbox.alert(statusMessages("success", "All the given rules for the reviewer assignment is saved successfully.", "small_mascot"))
			} else {
				bootbox.alert(statusMessages("warning", "Failed to edit user roles", "small_mascot"));
			}
		})
	}
}
function submitReviewerConfigAPI(data, rule, token) {
	return fetch(API + "/ocrflow/rules/" + rule + "/", {
		method: "post",
		headers: getHeaderForJson(token),
		body: JSON.stringify(data),
	}).then(response => Promise.all([response, response.json()]));
}
export function clearReviewerConfigStatesAction() {
	return {
		type: "CLEAR_REVIEWER_CONFIG"
	}
}
export function dashboardMetrics(data) {
	return {
		type: "DASHBOARD_METRICS",
		data
	}
}
export function closeFlag(data) {
	return {
		type: "CLOSE_FLAG",
		data
	}
}
	export function deleteUserFlag(flag) {
		return {
			type: "USER_DELETE_FLAG",
			flag
		}
}


