import React from "react";
import {DataPreview} from "../data/DataPreview";
import store from "../../store";
import {connect} from "react-redux";
import {STATIC_URL} from "../../helpers/env.js"

@connect((store) => {
	return {
		dataPreview: store.datasets.dataPreview,
	};
})


export class RoboDUTabsContent extends React.Component {
  constructor(props) {
		super(props);
  }
  render() {
		if(store.getState().datasets.dataPreview){
			return (
				<div className="apps_tabs_content">
					<DataPreview history={this.props.history} match={this.props.match}/>
				</div>
			);
		}else{
			return (
				<div>
					<img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif"} />
				</div>
 			);
		}  
  }
}
