import React from "react";
import {connect} from "react-redux";
import {CreateSignal} from "./CreateSignal";
import {SignalCard} from "./SignalCard";

@connect((store) => {
    return {
     latestSignalList: store.signals.latestSignals
    };
})

export class LatestSignals extends React.Component {
    constructor(props) {
        super(props);
        this.props=props;
    }
    render() {
        var data = this.props.latestSignalList;
        let addButton = addButton = <CreateSignal url={this.props.props.match.url}/>;
        let latestSignals = "";
        if(data){
            latestSignals =  <SignalCard data={data}/>;
        }
        return (
        <div class="dashboard_head">
            <div class="page-head">
                <h3 class="xs-mt-0">Signals</h3>
            </div>
            <div class="active_copy">
              <div class="row">
                {addButton}
                {latestSignals}
              </div>    
            </div>
        </div>      
        );
    }
    
}
