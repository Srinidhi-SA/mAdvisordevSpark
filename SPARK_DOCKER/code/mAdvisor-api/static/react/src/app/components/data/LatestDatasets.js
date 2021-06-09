import React from "react";
import {connect} from "react-redux";
import {DataUpload} from "./DataUpload";
import {DataCard} from "./DataCard";

@connect((store) => {
    return {
        latestDatasets: store.datasets.latestDatasets};
})

export class LatestDatasets extends React.Component {
    constructor(props) {
        super(props);
        this.props=props;
    }

    render() {
        var data = this.props.latestDatasets;
        let addButton = <DataUpload/>;
        let latestDatasets = "";
        if(data){
            latestDatasets =  <DataCard data={data} match={this.props.props.match}/>;
        }
        return (
        <div class="dashboard_head">
            <div class="page-head">
                <h3 class="xs-mt-0">Data</h3>
            </div>
            <div class="active_copy">
                <div class="row">
                {addButton}
                {latestDatasets}
                </div>
            </div>
        </div>       
        );
    }
    
}
