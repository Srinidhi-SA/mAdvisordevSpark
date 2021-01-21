
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
import {AppsCreateScore} from "./AppsCreateScore";
import {getAppsScoreSummary} from "../../actions/appActions";
import {DetailOverlay} from "../common/DetailOverlay";
import {STATIC_URL} from "../../helpers/env.js"
import {SEARCHCHARLIMIT,getUserDetailsOrRestart} from  "../../helpers/helper"
import Dialog from 'react-bootstrap-dialog'
import {ScoreCard}  from "./ScoreCard";
var dateFormat = require('dateformat');

 
@connect((store) => {
    return {login_response: store.login.login_response,
        latestScores: store.apps.latestScores};
})

//var selectedData = null;
export class LatestScores extends React.Component {
    constructor(props) {
        super(props);
        this.props=props;
    }
    
    componentWillMount(){
        
    }
    
    render() {
        var data = this.props.latestScores;
  var latestScores = "";
        if(data){
            latestScores =  <ScoreCard match = {this.props.props.match} data={data}/>;
        }
        return (
                <div class="dashboard_head">
                <div class="active_copy apps-cards">
                <div class="row">
                {latestScores}
                </div>
                </div>
                </div>
                
        );
    }
    
}
