import React from "react";
import {connect} from "react-redux";
import Dialog from 'react-bootstrap-dialog'
import {Modal,Button} from "react-bootstrap";
import store from "../../store";
import {openRoboDataPopup,closeRoboDataPopup,saveFilesToStore,uploadFiles,clearRoboDataUploadFiles} from "../../actions/appActions";
import Dropzone from 'react-dropzone'
import {CUSTOMERDATA,HISTORIALDATA,EXTERNALDATA} from "../../helpers/helper"

@connect((store) => {
	return {
		appsRoboShowModal: store.apps.appsRoboShowModal,
		customerDataUpload:store.apps.customerDataUpload,
		historialDataUpload:store.apps.historialDataUpload,
		externalDataUpload:store.apps.externalDataUpload,
		};
})

export class RoboDataUpload extends React.Component {
	constructor(props) {
		super(props);
	}
	componentWillMount() {
		//this.props.dispatch(storeSignalMeta(null,this.props.match.url));
		this.props.dispatch(closeRoboDataPopup());
	}
	openRoboDataPopup(){
		this.props.dispatch(clearRoboDataUploadFiles())
    	this.props.dispatch(openRoboDataPopup())
    }
    closeRoboDataPopup(){
    	this.props.dispatch(closeRoboDataPopup())
    }
    onDropCustomerData(files) {
		this.props.dispatch(saveFilesToStore(files,CUSTOMERDATA))
	}
    onDropHistorialData(files) {
		this.props.dispatch(saveFilesToStore(files,HISTORIALDATA))
	}
    onDropExternalData(files) {
		this.props.dispatch(saveFilesToStore(files,EXTERNALDATA))
	}
	popupMsg(){
		alert("Only CSV files are allowed to upload")
	}
	uploadFiles(){
		this.props.dispatch(uploadFiles(this.refs.dialog,$("#roboInsightName").val()));
	}
	render() {
		  var fileName = store.getState().apps.customerDataUpload.name;
	        var fileSize = store.getState().apps.customerDataUpload.size;
	
		return (
				<div class="col-md-3 top20 list-boxes" onClick={this.openRoboDataPopup.bind(this)}>
				<div class="newCardStyle firstCard">
				<div class="card-header"></div>
				<div class="card-center newStoryCard">
								
				<div class="col-xs-3 col-xs-offset-1 xs-pr-0"><i class="fa fa-file-text-o fa-4x"></i></div>
				<div class="col-xs-6 xs-m-0 xs-pl-0 lineHeight"><small>Robo Advisor <br/>Insights</small></div>
				
				</div>
				</div>
				
				<div id="newModel"  role="dialog" className="modal fade modal-colored-header">
				<Modal show={store.getState().apps.appsRoboShowModal} onHide={this.closeRoboDataPopup.bind(this)} dialogClassName="modal-colored-header">
				<Modal.Header closeButton>
				<h3 className="modal-title">Robo Data Upload</h3>
				</Modal.Header>
				<Modal.Body>
				  <div className="form-group">
				  <div className="row">
				  <label className="col-md-3">Name</label>
				  <div className="col-md-9">
				  <input id="roboInsightName" type="text"  placeholder="Enter Insight Name" className="form-control customInput" />
					</div>
				  </div>
				  <div className="clearfix"></div>
				  
				  <div className="row">
				  <label className="col-md-3">Customer Data</label>
				  <div className="col-md-9">
				  <div className="dropzone rb_insight_upload">
					<Dropzone onDrop={this.onDropCustomerData.bind(this)} accept=".csv" onDropRejected={this.popupMsg}>
					<p>Please drag and drop your file here or browse.</p>
					</Dropzone>
					<aside>
			          <ul className="list-unstyled">
			            	<li>{fileName} - {fileSize}</li>
			          </ul>
			        </aside>
					</div>
					</div>
				  </div>
				  <div className="clearfix"></div>
				  
				  <div className="row">
				  <label className="col-md-3">Historial Data </label>
				  <div className="col-md-9">
				  <div className="dropzone rb_insight_upload">
					<Dropzone onDrop={this.onDropHistorialData.bind(this)} accept=".csv" onDropRejected={this.popupMsg}>
					<p>Please drag and drop your file here or browse.</p>
					</Dropzone>
					<aside>
			          <ul className="list-unstyled">
			            	<li>{store.getState().apps.historialDataUpload.name} - { store.getState().apps.historialDataUpload.size}</li>
			          </ul>
			        </aside>
					</div>
					</div>
				  </div>
				  
				  <div className="row">
				  <label className="col-md-3">External Data </label>
				  <div className="col-md-9">
				  <div className="dropzone rb_insight_upload">
					<Dropzone onDrop={this.onDropExternalData.bind(this)} accept=".csv" onDropRejected={this.popupMsg}>
					<p>Please drag and drop your file here or browse.</p>
					</Dropzone>
					<aside>
			          <ul className="list-unstyled">
			            	<li>{store.getState().apps.externalDataUpload.name} - { store.getState().apps.externalDataUpload.size}</li>
			          </ul>
			        </aside>
					</div>
					</div>
				  </div>
				  
				</div>
				</Modal.Body>
				<Modal.Footer>
				<Button className="btn btn-primary md-close" onClick={this.closeRoboDataPopup.bind(this)}>Close</Button>
                <Button bsStyle="primary" onClick={this.uploadFiles.bind(this)}>Upload</Button>
				</Modal.Footer>
				</Modal>
				</div>
				<Dialog ref="dialog" />
				</div>


		)
	}

}	  