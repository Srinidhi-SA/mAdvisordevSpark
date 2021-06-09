import store from "../store";
import {API} from "../helpers/env";
import {getUserDetailsOrRestart} from "../helpers/helper";
import {cookieObj} from '../helpers/cookiesHandler';
import {closeImg} from "../actions/dataUploadActions";
import { COOKIEEXPIRETIMEINDAYS } from '../helpers/env.js';

export function getHeaderWithoutContent(token) {
  return {'Authorization': token};
}


export function authenticateFunc(username,password) {
    return (dispatch) => {
    return fetchPosts(username,password).then(([response, json]) =>{
        if(response.status === 200){
        dispatch(fetchPostsSuccess(json))
      }
      else{
        dispatch(fetchPostsError(json))
      }
    })
  }
}

function fetchPosts(username,password) {
  return fetch(API+'/api-token-auth/',{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
				username: username,
				password: password,
		 })
	}).then( response => Promise.all([response, response.json()])).catch(function() {
        $("#errormsg").html("Login unsuccessful. Please try again in sometime.")
    });
}


function fetchPostsSuccess(payload) {
cookieObj.storeCookies(payload)
  return {
    type: "AUTHENTICATE_USER",
    payload
  }
}

function fetchPostsError(json) {
  return {
    type: "ERROR",
    json
  }
}

export function getUserProfile(token) {
    return (dispatch) => {
    return fetchUserProfile(token).then(([response, json]) =>{
        if(response.status === 200){
        dispatch(fetchProfileSuccess(json))
      }
      else{
        dispatch(fetchProfileError(json))
      }
    })
  }
}

function fetchUserProfile(token) {
  return fetch(API+'/api/get_info/',{
		method: 'GET',
		headers: {
      'Authorization': token,
      'Content-Type': 'application/json'
		}
	}).then( response => Promise.all([response, response.json()]));
}


function fetchProfileSuccess(profileInfo) {
  cookieObj.storeCookies(profileInfo)
  return {
    type: "PROFILE_INFO",
    profileInfo
  }
}

function fetchProfileError(json) {
  return {
    type: "PROFILE_ERROR",
    json
  }
}

export function uploadImg(){
    return (dispatch) => {
      return triggerImgUpload().then(([response, json]) => {
        if (response.status === 200) {
           dispatch(saveProfileImage(json.image_url))
           dispatch(closeImg());
              } else {
          dispatch(imgUploadError(json))
        }
      });
    }
  }

  function triggerImgUpload() {
    var data = new FormData();
    data.append("image", store.getState().dataSource.fileUpload[0]);

    return fetch(API + '/api/upload_photo/', {
      method: 'PUT',
      headers: getHeaderWithoutContent(getUserDetailsOrRestart.get().userToken),
      body: data
    }).then(response => Promise.all([response, response.json()]));

  }

  export function imgUploadError(json) {
    return {type: "IMG_UPLOAD_TO_SERVER_ERROR", json}
  }

export function saveProfileImage(imageURL) {
  
 if(getUserDetailsOrRestart.get().image_url=="null"){
  var now = new Date();
  var exp = new Date(now.getTime() + COOKIEEXPIRETIMEINDAYS * 24 * 60 * 60 * 1000);
  var expires = exp.toUTCString();
  document.cookie = "image_url=" + imageURL + "; " + "expires=" + expires + "; path=/";
 }
  if(imageURL!="null"||!imageURL)
  imageURL=imageURL + new Date().getTime()
  return {
    type: "SAVE_PROFILE_IMAGE",
    imgUrl:imageURL
  }

}
