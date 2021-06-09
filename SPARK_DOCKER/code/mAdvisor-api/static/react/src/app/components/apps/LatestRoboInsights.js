import React from "react";
import {connect} from "react-redux";
import {RoboDataUpload} from "./RoboDataUpload";
import {RoboInsightCard} from "./RoboInsightCard";


@connect((store) => {
  return {
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
