import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../store";



@connect((store) => {
  return {
       login_response: store.login.login_response};
})

export class Home extends React.Component {
  constructor(){
    super();
  }
  render() {
	let redirectUrl = sessionStorage.url;
	if(redirectUrl == undefined || redirectUrl == "/" || redirectUrl == "/login" || redirectUrl == ""){
		redirectUrl = "/apps"	
	}
    return(
      <div>
    <Redirect to ={redirectUrl}/>

      </div>
    )
  }
}
