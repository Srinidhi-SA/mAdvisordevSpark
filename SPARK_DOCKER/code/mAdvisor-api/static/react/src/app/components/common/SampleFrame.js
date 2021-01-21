import React from "react";
import Iframe from 'react-iframe'
import {getUserDetailsOrRestart,hidechatbot,removeChatbotOnLogout} from "../../helpers/helper";
import {KYLO_UI,API} from "../../helpers/env";


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
     <Iframe url={kylo_url}
             width="100%"
             height="600px"
             id="myId"
             className="myClassname"
             display="initial"
             position="relative"
             allowFullScreen/>
	
	</div>
	</div>
       );
  }
}
