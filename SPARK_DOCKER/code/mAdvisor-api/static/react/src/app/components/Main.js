import React from "react";
import LeftPanel from "./common/LeftPanel";
import TopPanel from "./common/TopPanel";
import { Redirect } from "react-router";
import {checkChatbotPresent} from "../helpers/helper";
import {cookieObj} from '../helpers/cookiesHandler';
import Notifications from 'react-notify-toast';
import connect from "react-redux/lib/connect/connect";

@connect((store) => {
  return {
       login_response: store.login.login_response};
})
export class Main extends React.Component {
  constructor(props){
    super(props);
  }
  
  addChatbotScript() {
    if(!checkChatbotPresent()){
      if(window.location.pathname.indexOf("datamgmt")==-1){
        const script = document.createElement("script");
        script.src = "https://prodx.in/m-advisor-measure/client-plugin/bot.js";
        script.async = true;
        document.body.appendChild(script);
      }
   }
 }
  render() {
    if(document.cookie.indexOf("JWT")>0){
      return (
        <div className="main_wrapper">
          <LeftPanel/>
          <TopPanel/>
          <Notifications options={{zIndex: 200, top: '70px'}} />
            {this.props.children}
        </div>
      );
    } else {
        sessionStorage.clear();
        cookieObj.clearCookies();
      return(<Redirect to={"/login"} />);
    }

  }
}
