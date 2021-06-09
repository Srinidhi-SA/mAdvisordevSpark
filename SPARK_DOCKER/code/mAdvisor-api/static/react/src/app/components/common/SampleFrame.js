import React from "react";
import {getUserDetailsOrRestart,hidechatbot,removeChatbotOnLogout} from "../../helpers/helper";
import {KYLO_UI} from "../../helpers/env";

export class SampleFrame extends React.Component {
  constructor(){
    super();
  }

  componentWillMount(){
   hidechatbot()
  removeChatbotOnLogout()
  }

  render() {
    var encodedUri= encodeURIComponent("/index.html#!/"+this.props.match.params.kylo_url)
     var kylo_url= KYLO_UI+"/assets/integration.html?username="+getUserDetailsOrRestart.get().userName+"&password="+getUserDetailsOrRestart.get().dm_token+"&redirect="+encodedUri
   return (
   <div class="side-body">
   <div class="page-head"></div>
   <div class="clearfix"></div>
	<div class="main-content">
  <iframe id="myId" className="myClassname"src={kylo_url} style={{height:'600px',width:"100%",display:'initial',position:'relative'}} allowFullScreen={true}></iframe>
	</div>
	</div>
       );
  }
}
