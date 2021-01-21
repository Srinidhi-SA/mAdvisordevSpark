import React from "react";
import {MainHeader} from "../common/MainHeader";
import {Tabs,Tab,Pagination,Tooltip,OverlayTrigger,Popover} from "react-bootstrap";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {APPID4,APPNAME4} from "../../helpers/helper.js";
import {AudioFileUpload} from "./AudioFileUpload";
import {AppsLoader} from "../common/AppsLoader";
import {getAudioFile,getAudioFileList} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {isEmpty,SEARCHCHARLIMIT,getUserDetailsOrRestart} from "../../helpers/helper";
import {DetailOverlay} from "../common/DetailOverlay";
import Dialog from 'react-bootstrap-dialog'
import Breadcrumb from 'react-breadcrumb';
import {AudioFileCard} from "./AudioFileCard";
var dateFormat = require('dateformat');

@connect((store) => {
    return {login_response: store.login.login_response,
        currentAppId:store.apps.currentAppId,
        latestAudioList:store.apps.latestAudioList,
        };
})


export class LatestAudioFile extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
      var data = store.getState().apps.latestAudioList;
      let addButton =  <AudioFileUpload match={this.props.match}/>;

      let latestAudioFiles = "";
      if(data){
          latestAudioFiles =  <AudioFileCard data={data}/>;
      }
      return (
              <div class="dashboard_head">
              <div class="page-head">
              <h3 class="xs-mt-0 text-capitalize">Media Files</h3>
              </div>
              <div class="active_copy">
              <div class="row">
              {addButton}
              {latestAudioFiles}
              </div>
              </div>
              </div>
              
      );
  }


}
