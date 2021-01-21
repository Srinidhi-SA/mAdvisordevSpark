import React from "react";
import {Tabs, Tab} from "react-bootstrap";
import {Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {API} from "../../helpers/env.js"


import {updateCurrentAppByID, updateModelSummaryFlag, updateScoreSummaryFlag} from "../../actions/appActions";

@connect((store) => {
  return {currentAppId: store.apps.currentAppId, currentAppDetails: store.apps.currentAppDetails};
})

export class RegressionAppList extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
    if (this.props.currentAppDetails == null)
      this.props.dispatch(updateCurrentAppByID(13))
    this.props.dispatch(updateScoreSummaryFlag(false))
    this.props.dispatch(updateModelSummaryFlag(false))
  }

  render() {
    let app_page = "models"
    if (this.props.match.url.indexOf("scores") != -1)
      app_page = "scores"
    if (this.props.currentAppDetails != null) {
      let url = "/apps/" + this.props.currentAppDetails.slug + "/" + app_page
      return (<Redirect to ={url}/>)
    } else {
      return (
        <div className="side-body"></div>
      );
    }
  }
}
