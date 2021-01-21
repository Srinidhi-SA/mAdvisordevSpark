import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Link, Redirect} from "react-router-dom";
import {push} from "react-router-redux";

import {MainHeader} from "../common/MainHeader";
import {
  Tabs,
  Tab,
  Pagination,
  Tooltip,
  OverlayTrigger,
  Popover
} from "react-bootstrap";
import {storeRoboSearchElement} from "../../actions/appActions";
import {DetailOverlay} from "../common/DetailOverlay";
import {STATIC_URL} from "../../helpers/env.js";
import {RoboDataUpload} from "./RoboDataUpload";
import {AppsLoader} from "../common/AppsLoader";
import Dialog from 'react-bootstrap-dialog'
import {SEARCHCHARLIMIT,getUserDetailsOrRestart} from "../../helpers/helper";
import {RoboInsightCard} from "./RoboInsightCard";

var dateFormat = require('dateformat');

@connect((store) => {
  return {
    login_response: store.login.login_response,
    roboList: store.apps.roboList,
    currentAppId: store.apps.currentAppId,
    showRoboDataUploadPreview: store.apps.showRoboDataUploadPreview,
    roboDatasetSlug: store.apps.roboDatasetSlug,
    roboSummary: store.apps.roboSummary,
    dataPreviewFlag: store.datasets.dataPreviewFlag,
    robo_search_element: store.apps.robo_search_element,
    customerDataset_slug:store.apps.customerDataset_slug,
    historialDataset_slug:store.apps.historialDataset_slug,
    externalDataset_slug:store.apps.externalDataset_slug,
    latestRoboInsights:store.apps.latestRoboInsights,
  };
})

export class LatestRoboInsights extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
      var data = this.props.latestRoboInsights;
      let addButton =   <RoboDataUpload match={this.props.props.match}/>;
      let latestRoboInsights = "";
      if(data){
          latestRoboInsights =  <RoboInsightCard data={data}/>;
      }
      return (
              <div class="dashboard_head">
           <div class="page-head">
                <h3 class="xs-mt-0">Robo Advisor Insights</h3>
                </div>
              <div class="active_copy">
              <div class="row">
              {addButton}
              {latestRoboInsights}
              </div>
              </div>
              </div>
      );
    }
}
