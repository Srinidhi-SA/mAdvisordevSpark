import React from "react";
import {Redirect} from 'react-router';
import LoadingBar from 'react-redux-loading-bar';
import {Link} from "react-router-dom";
import {cookieObj} from '../../helpers/cookiesHandler';
import {getUserDetailsOrRestart,removeChatbotOnLogout,hidechatbot} from  "../../helpers/helper"
import {clearSignalAnalysisBeforeLogout} from "../../actions/signalActions";
 import {connect} from "react-redux";
import {STATIC_URL, API} from "../../helpers/env";
import { saveProfileImage} from "../../actions/loginActions";

 @connect((store) => {
	 return {login_res:store.login.login_response,
		profileImgURL: store.login.profileImgURL};
 })
export default class TopPanel extends React.Component {
    constructor(props){
		super(props);
		this.state = {loginFlag: true}
		this.props.dispatch(saveProfileImage(getUserDetailsOrRestart.get().image_url))
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

	handleErr(e){
		e.target.src =	STATIC_URL + "assets/images/avatar.png"
	}

	render(){
		if(!this.state.loginFlag){
			return(<Redirect to="/login" />);
		}else{
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
											{(!this.props.profileImgURL||this.props.profileImgURL==null||this.props.profileImgURL=="null")
											?<i className="avatar-img img-circle">{getUserDetailsOrRestart.get().userName.substr(0,1).toUpperCase()}</i>
											:<img src={API + this.props.profileImgURL} style={{width: 45, height:45,border:'3px solid #fff', borderRadius: '50%'}} onError={this.handleErr.bind(this)} />}
											<img src="" alt="M" className="avatar-img img-circle hide"/>&nbsp;
											<span className="user-name">{getUserDetailsOrRestart.get().userName}</span>
											<span className="caret"></span>
										</a>
										<ul className="dropdown-menu dropdown-menu-right">
											<li>
												<Link to="/user-profile"><i class="fa fa-user" aria-hidden="true"></i>&nbsp;&nbsp;Profile</Link>
											</li>
											<li>
												<a href="javascript:;" className="logout" onClick={this.logout.bind(this)}><i class="fa fa-sign-out" aria-hidden="true"></i>&nbsp;&nbsp;Logout</a>
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
