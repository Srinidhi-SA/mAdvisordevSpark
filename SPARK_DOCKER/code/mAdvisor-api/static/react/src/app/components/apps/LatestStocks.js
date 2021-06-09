import React from "react";
import {connect} from "react-redux";
import {addDefaultStockSymbolsComp} from "../../actions/appActions";
import {AppsCreateStockAnalysis} from "./AppsCreateStockAnalysis";
import {StocksCard} from "./StocksCard";

@connect((store) => {
    return {
        latestStocks:store.apps.latestStocks,
    };
})

export class LatestStocks extends React.Component {
    constructor(props) {
        super(props);
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
