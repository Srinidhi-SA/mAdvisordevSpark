import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {AudioFileUpload} from "./AudioFileUpload";
import {AudioFileCard} from "./AudioFileCard";

@connect((store) => {
    return {
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
