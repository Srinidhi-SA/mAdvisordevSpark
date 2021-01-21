import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import {Link} from "react-router-dom";
import store from "../../store";
import {Modal,Button} from "react-bootstrap";
import {openAppsLoaderValue,closeAppsLoaderValue,getAppsModelList,clearAppsIntervel,updateModelSummaryFlag,getHeader, showCreateModalPopup,} from "../../actions/appActions";
import {hideDataPreview, getDataSetPreview} from "../../actions/dataActions";
import renderHTML from 'react-render-html';
import HeatMap from '../../helpers/heatmap';
import {STATIC_URL, API} from "../../helpers/env";
import {handleJobProcessing, getUserDetailsOrRestart} from "../../helpers/helper";

@connect((store) => {
	return {login_response: store.login.login_response,
		appsLoaderModal:store.apps.appsLoaderModal,
		appsLoaderPerValue:store.apps.appsLoaderPerValue,
		appsLoaderText:store.apps.appsLoaderText,
		appsLoadedText:store.apps.appsLoadedText,
		appsLoaderImage:store.apps.appsLoaderImage,
		dataLoadedText:store.datasets.dataLoadedText,
		currentAppId: store.apps.currentAppId,
	    modelSlug: store.apps.modelSlug,
		scoreSlug:store.apps.scoreSlug,
		stockSlug:store.apps.stockSlug,
		roboDatasetSlug:store.apps.roboDatasetSlug,
		currentAppDetails:store.apps.currentAppDetails,
		modelLoaderidxVal: store.apps.modelLoaderidxVal,
		modelLoaderidx:store.apps.modelLoaderidx,
	};
})


export class AppsLoader extends React.Component {
  constructor(){
    super();
	}



	componentWillUpdate(){
   	var getText = [];
		if((this.props.appsLoaderPerValue < 0) && (Object.keys(this.props.appsLoadedText).length <= 0) ){
				$("#loadingMsgs1").empty()
				$("#loadingMsgs2").empty()
		}
		else if((this.props.appsLoaderPerValue >= 0) && (Object.keys(this.props.appsLoadedText).length > 0) && (document.getElementById("loadingMsgs1") != null) && (document.getElementById("loadingMsgs1").innerText === "")){		 
			if(window.location.pathname == "/apps-stock-advisor/"){
		    return false
		 	}
		}
}
	componentWillReceiveProps(newProps){
		if(newProps.modelLoaderidxVal != this.props.modelLoaderidxVal)
			if((window.location.pathname != "/apps-stock-advisor/") && (store.getState().apps.appsLoaderModal)){
				var array = this.props.appsLoadedText
				if(Object.values(array).length>1){
					for (var x = this.props.modelLoaderidx; x < (newProps.modelLoaderidxVal-2); x++) {
						var appsProg = setTimeout(function(i) {
							if(store.getState().apps.appsLoaderModal && document.getElementsByClassName("appsPercent")[0].innerHTML === "100%"){
								clearTimeout(appsProg);
								return false;
							}else if(store.getState().apps.appsLoaderModal){
								$("#loadingMsgs")[0].innerHTML = "Step " + (i+1) + ": " + array[i];
								$("#loadingMsgs1")[0].innerHTML ="Step " + (i+2) + ": " + array[i+1];
								$("#loadingMsgs2")[0].innerHTML ="Step " + (i+3) + ": " + array[i+2];
							}
						}, x * 2000, x);
					}
				}
			}
	}
	 
	componentDidUpdate(){
		 if(window.location.pathname == "/apps-stock-advisor/" && (Object.keys(this.props.dataLoadedText).length >0) ){
		 	 var node = document.createElement("I");

			(document.getElementById("loadingMsgs").innerText=='Please wait while analysing...'||
			this.props.appsLoaderText==document.getElementById("loadingMsgs").innerText.split(': ')[1])
			?"":document.getElementById("loadingMsgs").appendChild(node).classList.add('tickmark');

		  	var indexVal= Object.values(this.props.dataLoadedText).indexOf(this.props.appsLoaderText)
		   var updatedMsgs =Object.values(this.props.dataLoadedText).slice(indexVal,Object.values(this.props.dataLoadedText).length)

		   this.loadMsgs(indexVal,updatedMsgs)
		   } 
	   }

	 loadMsgs(indexVal,updatedMsgs){ 
		var x = document.getElementById("loadingMsgs");
		var x1 = document.getElementById("loadingMsgs1");
		var x2 = document.getElementById("loadingMsgs2");
		setTimeout(() => {
		x.innerHTML = "Step " + (indexVal+1) + ": " +updatedMsgs[0]; 
		x1.innerHTML = updatedMsgs[1]==undefined?"":"Step " + (indexVal+2) + ": " +updatedMsgs[1];
		x2.innerHTML =updatedMsgs[2]==undefined?"":"Step " + (indexVal+3) + ": " + updatedMsgs[2];
		 }, 3000);
		
		}
	openModelPopup(){
			this.props.dispatch(showCreateModalPopup())
  		this.props.dispatch(openAppsLoaderValue())
		}
		
  closeModelPopup(){
		this.props.dispatch(updateModelSummaryFlag(false));
		this.props.dispatch(hideDataPreview());
	  this.props.dispatch(closeAppsLoaderValue());
		clearAppsIntervel();
	}
	
  cancelCreateModel(){
		this.props.dispatch(updateModelSummaryFlag(false));
		this.props.dispatch(hideDataPreview());
		if((this.props.match.url).indexOf("/createScore") > 0 || (this.props.match.url).indexOf("/analyst/scores") > 0)
		this.props.dispatch(handleJobProcessing(this.props.scoreSlug));
		else if((this.props.match.url).indexOf("/apps-stock-advisor") >=0 )
		this.props.dispatch(handleJobProcessing(this.props.stockSlug));
		else if((this.props.match.url).indexOf("/apps-robo") >=0 )
		this.props.dispatch(handleJobProcessing(this.props.roboDatasetSlug));
		else
		this.props.dispatch(handleJobProcessing(this.props.modelSlug));
		this.props.dispatch(closeAppsLoaderValue());
		clearAppsIntervel();
	}

  render() {
		$('#text-carousel').carousel();
		let img_src=STATIC_URL+store.getState().apps.appsLoaderImage;
		var hideUrl = "";
		if(store.getState().apps.currentAppDetails != null)
			if(this.props.match && (this.props.match.url).indexOf("/createModel") > 0 || this.props.match && (this.props.match.url).indexOf("/createScore") > 0){
				let	appURL = "/"+store.getState().apps.currentAppDetails.app_url;
				let mURL;
				if(window.location.href.includes("analyst")){
					mURL = appURL.replace("models","analyst/models/")
				}else{
					mURL = appURL.replace("models","autoML/models/")
				}
				store.getState().apps.currentAppDetails != null ? hideUrl = mURL:hideUrl = "/apps/"+store.getState().apps.currentAppId+"/analyst/models";
			} else if((this.props.match.url).includes("/apps-stock-advisor-analyze"))
				hideUrl = "/apps-stock-advisor";
			else
				hideUrl = this.props.match.url;

   return (
          <div id="dULoader">
				<Modal show={store.getState().apps.appsLoaderModal} backdrop="static" onHide={this.closeModelPopup.bind(this)} dialogClassName="modal-colored-header">
      	<Modal.Body>
		<div className="row">
		<div className="col-md-12">
                <div className="panel xs-mb-0 modal_bg_processing">
                  <div className="panel-body no-border xs-p-0">

				<div id="text-carousel" class="carousel slide vertical" data-ride="carousel">

				<div class="row">
				<div class="col-xs-offset-1 col-xs-10">
				<div class="carousel-inner">
				<div class="item active">
				<div class="carousel-content">
					<h4 className="text-center">
					mAdvisor - Data scientist in a box
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					One click AutoML solution
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Automated AI and Machine Learning Techniques with zero manual intervention
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					User friendly interface for Business users with one click solution
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Advanced feature engineering options in analyst mode
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Build predictive models and deploy them for real-time prediction on unseen data
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Suitable for datasets of any size
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Gives you best results from multiple models
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Expandable and scalable adoption of new use cases
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					APD helps users to analyze and create data stories from large volumes of data
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Uses statistical techniques and machine learning algorithms to identify patterns within data sets
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Get insights and conclusive analysis in natural language
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Responsive visualization layer help to create intuitive analysis and bring data to life
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Import dataset from various sources and channels like, Local file system,  MySQL, MSSQL, SAP HANA, HDFS and S3
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Customer portfolio analysis using Robo-Advisor
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Insights about stock price using news article contents in Stock-Sense
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					mAdvisor Narratives for BI - automated insights engine extension for BI platforms such as Qlik Sense, Tableau, Power BI
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Narratives for BI - Translates data from charts and visualization into meaningful summaries
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Flexible deployment options - both cloud and on-premise deployments available
				</h4>
				</div>
				</div>
				<div class="item">
				<div class="carousel-content">
				   <h4 className="text-center">
					Login using your organization credentials
				</h4>
				</div>
				</div>

				</div>
				</div>
				</div>


				</div>

				<img src={img_src} className="img-responsive"/>

				<div className="modal_stepsBlock xs-p-10">
					<div className="row">
						<div className="col-sm-9">
							<p><b>mAdvisor evaluating your data set</b></p>
							<div class="modal-steps" id="loadingMsgs">
								Please wait while analysing...
							</div>
							<div class="modal-steps active" id="loadingMsgs1">
                                </div>
                                <div class="modal-steps" id="loadingMsgs2">
                                </div>
								{/* <ul class="modal-steps"> */}
								{/*	<li>----</li>*/}
									{/* <li class="active"></li> */}
								{/*	<li>----</li>*/}
								{/* </ul> */}

						</div>
						<div className="col-sm-3 text-center">
							{store.getState().apps.appsLoaderPerValue >= 0?<h2 class="text-white appsPercent">{store.getState().apps.appsLoaderPerValue}%</h2>:<h5 className="loaderValue appsPercent" style={{display:"block", textAlign: "center" }}>In Progress</h5>}
				  	</div>
					</div>
					</div>





				{/*store.getState().apps.appsLoaderPerValue >= 0 ?<div className="p_bar_body hidden">
				<progress className="prg_bar" value={store.getState().apps.appsLoaderPerValue} max={95}></progress>
				<div className="progress-value"><h3>{store.getState().apps.appsLoaderPerValue} %</h3></div>
				</div>:""*/}


			</div>


		</div>
		</div>
	</div>
		</Modal.Body>
		<Modal.Footer>
                <div>
                  <Link to={this.props.match.url} style={{
                    paddingRight: "10px"
                  }} >
                    <Button onClick={this.cancelCreateModel.bind(this)}>Cancel</Button>
                  </Link>
                  <Link to={hideUrl} >
                   <Button bsStyle="primary" onClick={this.closeModelPopup.bind(this)}>Hide</Button>
                   </Link>
                </div>
              </Modal.Footer>
		</Modal>
          </div>
       );
  }
}
