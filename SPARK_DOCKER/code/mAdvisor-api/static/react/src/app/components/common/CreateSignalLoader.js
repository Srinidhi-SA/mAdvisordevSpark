import React from "react";
import {connect} from "react-redux";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {Modal, Button} from "react-bootstrap";
import {openCsLoaderModal, closeCsLoaderModal} from "../../actions/createSignalActions";
import {hideDataPreview} from "../../actions/dataActions";
import { DYNAMICLOADERINTERVAL, handleJobProcessing} from "../../helpers/helper";
import {clearCreateSignalInterval} from "../../actions/signalActions";
import {STATIC_URL} from "../../helpers/env";

@connect((store) => {
  return {
    login_response: store.login.login_response,
    createSignalLoaderModal: store.signals.createSignalLoaderModal,
    createSignalLoaderValue: store.signals.createSignalLoaderValue,
    loaderText: store.signals.loaderText,
    signalData: store.signals.signalData,
	signalLoadedText: store.signals.signalLoadedText,
	sigLoaderidxVal: store.signals.sigLoaderidxVal,
	sigLoaderidx:store.signals.sigLoaderidx,
  };
})

export class CreateSignalLoader extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillReceiveProps(newProps){
	if(newProps.sigLoaderidxVal != this.props.sigLoaderidxVal)
		if(store.getState().signals.createSignalLoaderModal){
			var array = this.props.signalLoadedText
			if(Object.values(array).length>0 && array!=undefined){
				for (var x = this.props.sigLoaderidx; x < (newProps.sigLoaderidxVal-2); x++) {
					var sigProg = setTimeout(function(i) {
						 if(store.getState().signals.createSignalLoaderModal){
							if(document.getElementsByClassName("sigProgress")[0].innerHTML === "100%"){
								clearTimeout(sigProg);
								return false;
							}else
							$("#loadingMsgs")[0].innerHTML = "Step " + (i+1) + ": " + array[i];
							$("#loadingMsgs1")[0].innerHTML ="Step " + (i+2) + ": " + array[i+1];
							$("#loadingMsgs2")[0].innerHTML ="Step " + (i+3) + ": " + array[i+2];
						}
					}, x * 2000, x);
				}
			}
		}
	}

  openModelPopup() {
    this.props.dispatch(openCsLoaderModal())
  }
  closeModelPopup() {
    this.props.dispatch(closeCsLoaderModal());
    this.props.dispatch(hideDataPreview());
    clearCreateSignalInterval();
  }
  cancelSignalProcessing() {
    this.props.dispatch(closeCsLoaderModal());
    this.props.dispatch(hideDataPreview());
    clearCreateSignalInterval();
    this.props.dispatch(handleJobProcessing(this.props.signalData.slug));
  }
    render() {
        var that = this;
        if(this.props.signalData != null){
            setTimeout(function() {
                if(that.props.signalData.hasOwnProperty("proceed_for_loading") && !that.props.signalData.proceed_for_loading){
                    that.props.history.push("/signals");
                }
            },DYNAMICLOADERINTERVAL)}

        let imgsrc_url=STATIC_URL+"assets/images/Processing_mAdvisor.gif"
		$('#text-carousel').carousel();
        return (
                <div id="createSignalLoader">

                <Modal show={store.getState().signals.createSignalLoaderModal}  backdrop="static" onHide={this.closeModelPopup.bind(this)} dialogClassName="modal-colored-header">

                <Modal.Body style={{marginBottom:"0"}}>


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

		<img src={imgsrc_url} className="img-responsive"/>


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

						</div>
						<div className="col-sm-3 text-center">
							{store.getState().signals.createSignalLoaderValue >= 0?<h2 className="text-white sigProgress">{store.getState().signals.createSignalLoaderValue}%</h2>:<h5 style={{display:"block", textAlign: "center" }} className="loaderValue sigProgress">In Progress</h5>}

						</div>
					</div>
					</div>


                   
										
                  </div>
                </div>
              </div>
            </div>










          </Modal.Body>
              <Modal.Footer>
                <div>
                  <Link to="/signals" style={{
                    paddingRight: "10px"
                  }} onClick={this.cancelSignalProcessing.bind(this)}>
                    <Button onClick={this.cancelSignalProcessing.bind(this)}>Cancel</Button>
                  </Link>
                  <Link to="/signals" onClick={this.closeModelPopup.bind(this)}>
                    <Button bsStyle="primary" >Hide</Button>
                  </Link>
                </div>
              </Modal.Footer>
        </Modal>
      </div>
    );
  }
}
