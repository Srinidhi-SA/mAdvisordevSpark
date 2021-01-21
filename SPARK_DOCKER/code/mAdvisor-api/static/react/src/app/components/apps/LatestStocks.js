import React from "react";
import {MainHeader} from "../common/MainHeader";
import {Tabs,Tab,Pagination,Tooltip,OverlayTrigger,Popover} from "react-bootstrap";
import {AppsModelList} from "./AppsModelList";
import {AppsScoreList} from "./AppsScoreList";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {APPID1,APPID2,APPID3,APPNAME1,APPNAME2,APPNAME3,getUserDetailsOrRestart} from "../../helpers/helper.js"
import {getStockAnalysis,updateStockSlug,addDefaultStockSymbolsComp} from "../../actions/appActions";
import Dialog from 'react-bootstrap-dialog'
import {AppsCreateStockAnalysis} from "./AppsCreateStockAnalysis";
import {STATIC_URL} from "../../helpers/env.js";
import {DetailOverlay} from "../common/DetailOverlay";
import {AppsLoader} from "../common/AppsLoader";
import {StocksCard} from "./StocksCard";

var dateFormat = require('dateformat');

@connect((store) => {
    return {login_response: store.login.login_response,
        currentAppId:store.apps.currentAppId,
        stockList: store.apps.stockAnalysisList,
         dataPreviewFlag: store.datasets.dataPreviewFlag,
         stockAnalysisFlag:store.apps.stockAnalysisFlag,
         stockSlug:store.apps.stockSlug,
        signal: store.signals.signalAnalysis,
        latestStocks:store.apps.latestStocks,
    };
})

export class LatestStocks extends React.Component {
    constructor(props) {
        super(props);
    }

    getPreviewData(e) {
        this.props.dispatch(updateStockSlug(e.target.id))
        this.props.dispatch(getStockAnalysis(e.target.id))
    }
    resetAnalyzepopup(){
        this.props.dispatch(addDefaultStockSymbolsComp());
    }
    render() {
        var data = this.props.latestStocks;
        let addButton =   <div onClick={this.resetAnalyzepopup.bind(this)}><AppsCreateStockAnalysis match={this.props.props.match}/></div>;
        let latestStocks = "";
        if(data){
            latestStocks =  <StocksCard data={data} loadfunc={this.props.loadfunc}/>;
        }
        return (
                <div class="dashboard_head">
             <div class="page-head">
                  <h3 class="xs-mt-0">Stock Analytics</h3>
                  </div>
                <div class="active_copy">
                <div class="row">
                {addButton}
                {latestStocks}
                </div>
                </div>
                </div>
        );
    }


}
