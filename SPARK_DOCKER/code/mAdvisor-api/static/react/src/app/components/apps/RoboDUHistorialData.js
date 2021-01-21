import React from "react";
import {MainHeader} from "../common/MainHeader";
import {Tabs,Tab} from "react-bootstrap";
import {DataPreview} from "../data/DataPreview";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {getDataSetPreview} from "../../actions/dataActions";
import {STATIC_URL} from "../../helpers/env.js"

@connect((store) => {
	return {login_response: store.login.login_response, 
		currentAppId:store.apps.currentAppId,
		dataPreview: store.datasets.dataPreview,
		customerDataset_slug:store.apps.customerDataset_slug,
		historialDataset_slug:store.apps.historialDataset_slug,
		externalDataset_slug:store.apps.externalDataset_slug,
		};
})


export class RoboDUHistorialData extends React.Component {
  constructor(props) {
    super(props);
  }
 
  render() {
     let dataPreview = store.getState().datasets.dataPreview;
    		if(dataPreview){
    			return (   <div className="apps_tabs_content">
    	            <DataPreview />
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
