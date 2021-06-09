import {applyMiddleware, createStore} from "redux"
import logger from "redux-logger"
import thunk from "redux-thunk"
import promise from "redux-promise-middleware"
import reducer from "./reducers"
import {cookieObj} from './helpers/cookiesHandler';
const err = () => (next) => (action) => {
  try {
    next(action);
  } catch (e) {
    let expiredSignMsg = "Signature has expired.";
    if(action.json == undefined){
        bootbox.alert("Something went wrong.Please try again.",function(){
            window.location.assign("/signals")
        })
    }
    else if (action.json["exception"] == expiredSignMsg) {
        sessionStorage.clear();
        cookieObj.clearCookies();
        location.reload();

    }else if (action.json["exception"].indexOf("Permission")!=-1) {
    }
    else{
        sessionStorage.clear();
        cookieObj.clearCookies();
        location.reload();
    }
  }
}

const middleware = applyMiddleware(promise(), thunk, logger, err)

const store = createStore(reducer, middleware)

export default store;
