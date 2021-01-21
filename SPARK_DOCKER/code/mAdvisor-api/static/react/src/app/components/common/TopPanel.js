import React from "react";
import {Redirect} from 'react-router';
import LoadingBar from 'react-redux-loading-bar';
import {Link} from "react-router-dom";
import {cookieObj} from '../../helpers/cookiesHandler';
import {getUserDetailsOrRestart,removeChatbotOnLogout,hidechatbot} from  "../../helpers/helper"
import {STATIC_URL} from "../../helpers/env";
import {clearSignalAnalysisBeforeLogout} from "../../actions/signalActions";
 import {connect} from "react-redux";
 @connect((store) => {
   return {login_res:store.login.login_response};
 })
export default class TopPanel extends React.Component {
    constructor(props){
		super(props);
		this.state = {loginFlag: true}
	}
	logout(){
		this.props.dispatch(clearSignalAnalysisBeforeLogout());
		  this.setState({
             loginFlag: false
         });
         hidechatbot()
         removeChatbotOnLogout()
         cookieObj.clearCookies();
	}
	render(){
		if(!this.state.loginFlag){
			return(<Redirect to="/login" />);
		}else{
    var userManualPath=STATIC_URL+"userManual/UserManual.html"
			return(
		            <div>
								<nav className="navbar navbar-default navbar-fixed-top" role="navigation">
								<LoadingBar style={{ backgroundColor: '#148071', height: '3px' }} />
									<div className="navbar-header">
										<div className="brand-wrapper">
											<button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#side-menu">
												<span className="sr-only">Toggle navigation</span>
												<span className="icon-bar"></span>
												<span className="icon-bar"></span>
												<span className="icon-bar"></span>
											</button>

											<div className="brand-name-wrapper">
												<a className="navbar-brand" href="/"></a>
											</div>
										</div>
									</div>
									<div className="dropdown ma-user-nav">
										<a className="dropdown-toggle" href="#" data-toggle="dropdown">
											<i className="avatar-img img-circle">{getUserDetailsOrRestart.get().userName.substr(0,1).toUpperCase()}</i>
											<img src="" alt="M" className="avatar-img img-circle hide"/>&nbsp;
											<span className="user-name">{getUserDetailsOrRestart.get().userName}</span>
											<span className="caret"></span>
										</a>
										<ul className="dropdown-menu dropdown-menu-right">
											<li>
												<Link to="/user-profile"><i class="zmdi zmdi-account-o zmdi-hc-lg" aria-hidden="true"></i>&nbsp;&nbsp;Profile</Link>
											</li>
											{/* <li><a href={userManualPath} target="_blank"><i class="zmdi zmdi-help-outline zmdi-hc-lg" aria-hidden="true"></i>&nbsp;&nbsp;User Manual</a></li> */}
											<li>
												<a href="javascript:;" className="logout" onClick={this.logout.bind(this)}><i class="zmdi zmdi-sign-in zmdi-hc-lg" aria-hidden="true"></i>&nbsp;&nbsp;Logout</a>
											</li>
										</ul>
									</div>
									<div className="clearfix"></div>
								</nav>
								</div>

		 );
		}
  }

}
