import store from "../store";
import {sessionObject} from '../helpers/manageSessionStorage';
import {API} from "../helpers/env";
import {getUserDetailsOrRestart} from "../helpers/helper";
import { sessionService } from 'redux-react-session';
import { browserHistory } from 'react-router';
import {cookieObj} from '../helpers/cookiesHandler';

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
	}).then( response => Promise.all([response, response.json()])).catch(function(error) {
        $("#errormsg").html("Login unsuccessful. Please try again in sometime.")
    });
}


function fetchPostsSuccess(payload) {
var token = payload.token;
//sessionObject.manageSession(payload);
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

//to fetch user Profile
export function openImg() {
  return {type: "SHOW_IMG_MODAL"}
}

export function closeImg() {
  return {type: "HIDE_IMG_MODAL"}
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
//for image upload

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

  function clearImageURL(){
    return{
      type:"CLEAR_PROFILE_IMAGE"

    }

  }
  function triggerImgUpload() {
    var data = new FormData();
    data.append("image", store.getState().dataSource.fileUpload);
    // data.append("website",sessionStorage.email)
    // data.append("bio","jfhsndfn")
    // data.append("phone",sessionStorage.phone)

    return fetch(API + '/api/upload_photo/', {
      method: 'put',
      headers: getHeaderWithoutContent(getUserDetailsOrRestart.get().userToken),
      body: data
    }).then(response => Promise.all([response, response.json()]));

  }

  export function imgUploadError(josn) {
    return {type: "IMG_UPLOAD_TO_SERVER_ERROR", json}
  }

export function saveProfileImage(imageURL) {
  return {
    type: "SAVE_PROFILE_IMAGE",
    imgUrl:imageURL
  }

}
