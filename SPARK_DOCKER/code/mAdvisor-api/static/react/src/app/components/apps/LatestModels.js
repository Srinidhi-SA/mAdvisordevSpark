import React from "react";
import {connect} from "react-redux";
import {AppsCreateModel} from "./AppsCreateModel";
import {ModelsCard} from "./ModelsCard";
 
@connect((store) => {
    return {
        latestModels: store.apps.latestModels
    };
})

export class LatestModels extends React.Component {
    constructor(props) {
        super(props);
        this.props=props;
    }
   
    render() {
        var data = this.props.latestModels;
        let addButton  = "";
        addButton  = <AppsCreateModel match={this.props.props.match} isEnableCreate={this.props.permissions.create_trainer}/>;
        let latestModels = "";
        if(data){
            latestModels =  <ModelsCard match = {this.props.props.match} data={data}/>;
        }
        return (
            <div class="dashboard_head">
                <div class="active_copy apps-cards">
                    <div class="row">
                        {addButton}
                        {latestModels}
                    </div>
                </div>
            </div>    
        );
    }
}
