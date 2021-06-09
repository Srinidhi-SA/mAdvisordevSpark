import { COOKIEEXPIRETIMEINDAYS } from './env.js';


export const cookieObj = {
  storeCookies: function (userDetail) {
    var now = new Date();
    var exp = new Date(now.getTime() + COOKIEEXPIRETIMEINDAYS * 24 * 60 * 60 * 1000);
    var expires = exp.toUTCString();
    if (userDetail.token)
    document.cookie = "userToken=" + userDetail.token + "; " + "expires=" + expires + "; path=/";
    document.cookie = "userName=" + userDetail.user.username + "; " + "expires=" + expires + "; path=/";
    document.cookie = "email=" + userDetail.user.email + "; " + "expires=" + expires + "; path=/";
    document.cookie = "date=" + userDetail.user.date_joined + "; " + "expires=" + expires + "; path=/";
    document.cookie = "phone=" + userDetail.profile.phone + "; " + "expires=" + expires + "; path=/";
    document.cookie = "last_login=" + userDetail.user.last_login + "; " + "expires=" + expires + "; path=/";
    document.cookie = "is_superuser=" + userDetail.user.is_superuser + "; " + "expires=" + expires + "; path=/";
    document.cookie = "image_url=" + userDetail.profile.image_url + "; " + "expires=" + expires + "; path=/";
    if (userDetail.view_permission && userDetail.view_permission != null) {
      document.cookie = "view_signal_permission=" + userDetail.view_permission.view_signal + "; " + "expires=" + expires + "; path=/";
      document.cookie = "view_data_permission=" + userDetail.view_permission.view_dataset + "; " + "expires=" + expires + "; path=/";
      document.cookie = "view_score_permission=" + userDetail.view_permission.view_score + "; " + "expires=" + expires + "; path=/";
      document.cookie = "view_trainer_permission=" + userDetail.view_permission.view_trainer + "; " + "expires=" + expires + "; path=/";
    }
    document.cookie = "dm_token=" + userDetail.profile.kylo_password + "; " + "expires=" + expires + "; path=/";
    if(userDetail.ocr_profile != null){
    document.cookie = "userRole=" + userDetail.ocr_profile.role[0] + "; " + "expires=" + expires + "; path=/";
    }

  },

  clearCookies: function () {
    var now = new Date();
    var exp = new Date(now.getTime() - COOKIEEXPIRETIMEINDAYS * 24 * 60 * 60 * 1000);
    var expires = exp.toUTCString();
    document.cookie = "userRole=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "userToken=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "userName=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "email=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "date=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "phone=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "last_login=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "is_superuser=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "image_url=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "view_signal_permission=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "view_data_permission=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "view_score_permission=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "view_trainer_permission=;" + "; " + "expires=" + expires + "; path=/";
    document.cookie = "dm_token=;" + "; " + "expires=" + expires + "; path=/";
    sessionStorage.clear();
    var noOfUrls = window.history.length;
    window.history.go("-" + noOfUrls - 1);
    window.history.replaceState(null, null, "/login");
  }
}
