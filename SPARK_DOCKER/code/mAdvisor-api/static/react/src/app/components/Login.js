import React from "react";
import ReactTooltip from 'react-tooltip'
import {connect} from "react-redux";
import {Redirect} from 'react-router';
// import {authenticateFunc,getList,storyList} from "../../services/ajax.js";
import {authenticateFunc} from "../actions/loginActions";
import store from "../store";
import {STATIC_URL, API} from "../helpers/env";
import {isEmpty,getUserDetailsOrRestart,USERDETAILS,removeChatbotOnLogout,hidechatbot} from "../helpers/helper";
import {sessionObject} from '../helpers/manageSessionStorage';
// import $ from "jquery";

@connect((store) => {
  return {login_response: store.login.login_response, errmsg:store.login.errmsg};
})

export class Login extends React.Component {
  constructor() {

    super();
    this.state = {
      uId: '',
      pwd: '',
      errmsg:""
    };
  }
  onChangeUId(e) {
    const userId = e.target.value;
    this.setState({uId: userId});
  }
  onChangePwd(e) {
    const password = e.target.value;
    this.setState({pwd: password});
  }

  componentDidMount(){
    hidechatbot()
  }

  doAuth() {
  if(this.state.uId==""||this.state.uId==null||this.state.uId.trim().length==0){
    this.state.errmsg = "Please enter the username!"
    $("#errormsg").text(this.state.errmsg);
  }else if(this.state.pwd==""||this.state.pwd==null){
    this.state.errmsg = "Please enter the password!"
    $("#errormsg").text(this.state.errmsg);
  }else{
    this.props.dispatch(authenticateFunc(this.state.uId, this.state.pwd))
    $("#errormsg").text(this.state.errmsg);
  }
  }
  render() {
    const forgotLink = API + "/reset-password/"; 
    this.state.errmsg = this.props.errmsg;
    if (document.cookie.indexOf("JWT ") > 0 ) {
      document.body.className = "";
      return (<Redirect to={"/"} />);
    } else {
    	document.body.className = "ma-splash-screen";
    	   localStorage.JWT = "Test Local Storage"
         removeChatbotOnLogout()
      return (

          <div className="ma-wrapper ma-login">
            <div className="ma-content">
              <div className="main-content">

				<div class="ma-content-left">
				</div>

			  <div class="ma-content-right">
             <form action="javascript:void(0);">
                <div className="login-container">
                  <div className="panel panel-default">
                    <div className="panel-heading"><img src={STATIC_URL + "assets/images/m_adv_logo.png" } alt="mAdvisor" className="img-responsive logo-img"/></div>
                    <div className="panel-body no-border">

                      <div className="login-form">
                        <div className="form-group">
                          <div className="input-group">
                            <input id="username" type="text" value={this.state.uId} onChange={this.onChangeUId.bind(this)} placeholder="Username" autoComplete="off" className="form-control"/>
                            
                          </div>
                        </div>
                        <div className="form-group">
                          <div className="input-group">
                            <input id="password" type="password" value={this.state.pwd} onChange={this.onChangePwd.bind(this)} placeholder="Password" className="form-control"/>
                          
                          </div>
                        </div>
                        <div className="form-group footer row">
                         
                          <div className="col-xs-6 text-right">
                            
                          </div>

                        </div>
						            <a href = {forgotLink} className="xs-mt-20 pull-left">Forgot Password?</a>                      
                      
                        <div className="form-group login-submit pull-right">
                          <button onClick={this.doAuth.bind(this)} id="login" className="btn btn-primary xs-pl-20 xs-pr-20 xs-pt-5 xs-pb-5">SIGN IN</button>
                        </div>
						            <div className="clearfix"></div>
                        <div className = "text-danger text-center" id="errormsg">{this.state.errmsg}</div>

                      </div>
                    </div>
                  </div>
                </div>
              </form>
		 </div>
              </div>
            </div>
          </div>


      );

    }
  }

}
