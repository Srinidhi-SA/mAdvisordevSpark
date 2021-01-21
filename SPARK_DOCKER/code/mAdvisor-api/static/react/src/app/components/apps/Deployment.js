import React from "react";
import { connect } from "react-redux";
import {isEmpty} from "../../helpers/helper";
import {STATIC_URL,EMR} from "../../helpers/env.js";
import {handleDeploymentDeleteAction,createDeploy,viewDeployment} from "../../actions/appActions";
import Dialog from 'react-bootstrap-dialog';
import { DeployPopup } from "./DeployPopup";
import {Button,Modal} from "react-bootstrap";
import {openDeployModalAction, closeDeployModalAction,saveDeployValueAction,closeViewModalAction} from "../../actions/modelManagementActions";

@connect((store) => {
  return {
    login_response: store.login.login_response,
    dataPreview: store.datasets.dataPreview,
    selectedItem: store.datasets.selectedItem,
    featureEngineering:store.datasets.featureEngineering,
    deploymentList:store.apps.deploymentList,
		algoAnalysis:store.signals.algoAnalysis,
    deployShowModal: store.apps.deployShowModal,
    deployData: store.apps.deployData,
    deployItem: store.apps.deployItem,
    deploymentData:store.apps.deploymentData,
    viewDeploymentFlag:store.apps.viewDeploymentFlag,
  };
})

export class Deployment extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.pickValue = this.pickValue.bind(this);
  }

  componentWillMount() {
  }

  handleDeploymentDelete(slug) {
    var algoSlug= this.props.algoAnalysis.slug; 
    this.props.dispatch(handleDeploymentDeleteAction(slug,algoSlug, this.refs.dialog));
  }

  handleViewClicked(slug){
    this.props.dispatch(viewDeployment(slug));
  }

  pickValue(actionType, event){
    if(this.state[this.props.deployItem] == undefined){
      this.state[this.props.deployItem] = {}
    }
    if(event.target.type == "checkbox"){
      this.state[this.props.deployItem][event.target.name] = event.target.checked;
    }
    else{
      this.state[this.props.deployItem][event.target.name] = event.target.value;
    }
  }
  
  handleCreateClicked(actionType,event){
    if(actionType == "deployData"){
      this.validateDeployData(actionType,event);
    }else{
      var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.deployItem][event.target.name]));
      this.props.dispatch(saveDeployValueAction(this.props.deployItem, dataToSave));
      this.closeDeployModal();
      this.props.dispatch(createDeploy(this.props.deployItem));
    }
  }

  validateDeployData(actionType,event){
    var slugData = this.state[this.props.deployItem];
    if(slugData != undefined && this.state[this.props.deployItem] != undefined){
      var deployData = this.state[this.props.deployItem];
      if(deployData.name == undefined|| deployData.name == null || deployData.name == ""){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter deployment name");
        $("input[name='name']").focus();
        return;
      }else if(deployData.datasetname == undefined|| deployData.datasetname == null || deployData.datasetname == ""){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter dataset name");
        $("input[name='datasetname']").focus();
        return;
      }else if(deployData.file_name == undefined|| deployData.file_name == null || deployData.file_name == ""){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter filename");
        $("input[name='file_name']").focus();
        return;
      }else if(deployData.access_key_id == undefined|| deployData.access_key_id == null || deployData.access_key_id == ""){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter access key password");
        $("input[name='access_key_id']").focus();
        return;
      }else if(deployData.secret_key == undefined|| deployData.secret_key == null || deployData.secret_key == ""){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter secret key password");
        $("input[name='secret_key']").focus();
        return;
      }else if(deployData.timing_details == undefined|| deployData.timing_details == "none"){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please select frequency");
        $("select[name='timing_details']").focus();
        return;
      }
      var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.deployItem]));
      this.props.dispatch(saveDeployValueAction(this.props.deployItem, dataToSave));
      this.closeDeployModal();
      this.props.dispatch(createDeploy(this.props.deployItem));
    }else{
      $("#fileErrorMsg").removeClass("visibilityHidden");
      $("input[name='name']").css("border-color","red");
		  $("input[name='datasetname']").css("border-color","red");
      $("input[name='file_name']").css("border-color","red");
      $("input[name='access_key_id']").css("border-color","red");
      $("input[name='secret_key']").css("border-color","red");
      $("select[name='timing_details']").css("border-color","red");
      $("#fileErrorMsg").html("Please enter Mandatory fields * ");
    }
  }

  render() {
    if(isEmpty(this.props.deploymentList)){
			return (
        <div className="side-body">
            <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
        </div>
      );
		}else{
    var deployPopup = "";
    var deployData = "";
    var viewPopup = "";
    var viewData = "";
		var deploymentList = this.props.deploymentList;
    var deploymentTable = "";
    deployData = "deployData";
      deployPopup = (
        <div class="col-md-3 xs-mb-15 list-boxes" >
          <div id="deployPopup" role="dialog" className="modal fade modal-colored-header">
            <Modal show={this.props.deployShowModal} onHide={this.closeDeployModal.bind(this)} dialogClassName="modal-colored-header">
              <Modal.Header closeButton>
                <h3 className="modal-title">Deploy Model</h3>
              </Modal.Header>
              <Modal.Body>
                <DeployPopup parentPickValue={this.pickValue}/>
              </Modal.Body> 
              <Modal.Footer>
                <Button onClick={this.closeDeployModal.bind(this)}>Cancel</Button>
                <Button bsStyle="primary" onClick={this.handleCreateClicked.bind(this,deployData)}>Deploy</Button>
              </Modal.Footer>
            </Modal>
          </div>
        </div>
      )
     if(this.props.viewDeploymentFlag){
      var deptData = this.props.deploymentData;
      viewData = deptData.config.dataset_details.datasource_details;
      return (
      viewPopup = (
        <div class="col-md-3 xs-mb-15 list-boxes" >
          <div id="viewPopup" role="dialog" className="modal fade modal-colored-header">
            <Modal show={this.props.viewDeploymentFlag} onHide={this.closeViewModal.bind(this)} dialogClassName="modal-colored-header">
              <Modal.Header closeButton>
                <h4 className="modal-title">Deployment Details</h4>
              </Modal.Header>
              <Modal.Body>
                <div class="modal-body">
                  <table class="tablesorter table table-striped table-hover table-bordered">
                    <tbody>
                      <tr>
                        <td className="text-left"><b>Deployment name</b></td>
                        <td className="text-left">{deptData.name}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Dataset name</b></td>
                        <td className="text-left">{viewData.datasetname}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Filename</b></td>
                        <td className="text-left">{viewData.file_name}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Bucket name</b></td>
                        <td className="text-left">{viewData.bucket_name}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Access </b></td>
                        <td className="text-left">{viewData.access_key_id}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Secret name</b></td>
                        <td className="text-left">{viewData.secret_key}</td>
                      </tr>
                      <tr>
                        <td className="text-left"><b>Frequency of Score</b></td>
                        <td className="text-left">{deptData.config.timing_details}</td>
                      </tr>
                    </tbody>
                  </table>
                  </div>
              </Modal.Body> 
              <Modal.Footer>
                <Button onClick={this.closeViewModal.bind(this)}>Close</Button>
              </Modal.Footer>
            </Modal>
          </div>
        </div>
      )
      );
     }

      if(deploymentList.data.length == 0){
        deploymentTable = <h4 style={{textAlign:"center"}}>No Deployments Available</h4>
        return(
          <div id="deployment" class="tab-pane">
          {deployPopup} {viewPopup}
          <button class="btn btn-warning btn-shade4 pull-right" onClick={this.openDeployModal.bind(this,this.props.algoAnalysis.slug)}>Add New Deployment</button><br/><br/>
          <div class="clearfix"></div>
          <div>
            {deploymentTable}
            </div>
          <Dialog ref="dialog"/>
        </div>
        );
      }
      else {
        deploymentTable = deploymentList.data.map((deploy,key )=> {
        return (
            <tr key={key} className={('all ' + deploy.name)}>
        <td>
          <label for="txt_lName1">{`${key + 1}`}&nbsp;&nbsp;&nbsp;</label>
        </td>
      <td className="text-left"> {deploy.name}</td>
      <td  className="text-left"> {deploy.name}</td>
      <td className="text-left"> {deploy.status}</td>
      <td ><span className="text-success"></span> {deploy.updated_at}</td>
      <td > {deploy.name}</td>
      <td > {deploy.name}</td>
      {/* <td > {deploy.name}</td> */}
      <td>
          <div class="pos-relative">
            <a class="btn btn-space btn-default btn-round btn-xs" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
              <i class="ci zmdi zmdi-hc-lg zmdi-more-vert"></i>
            </a>    
            <ul class="dropdown-menu dropdown-menu-right">
            <li><a bsStyle="cst_button" onClick={this.handleViewClicked.bind(this,deploy.slug)}>View</a></li>
              <li><a onClick={this.handleDeploymentDelete.bind(this,deploy.slug)}  >Delete</a></li>       
            </ul>
          </div>
        </td>
    </tr>);
    }) 
    }
    
    return (
			<div id="deployment" class="tab-pane">
          {deployPopup} {viewPopup}
				<button class="btn btn-warning btn-shade4 pull-right" onClick={this.openDeployModal.bind(this,this.props.algoAnalysis.slug)}>Add New Deployment</button><br/><br/>
					<div class="clearfix"></div>
						<table class="tablesorter table table-striped table-hover table-bordered break-if-longText">
							<thead>
								<tr className="myHead">
									<th>#</th>
									<th class="text-left"><b>Name</b></th>
									<th class="text-left"><b>Deployment Type</b></th>
									<th><b>Status</b></th>
									<th><b>Deployed On</b></th>
									<th><b>Runtime</b></th>
									<th><b>Jobs Triggered</b></th>
									<th><b>Action</b></th>
								</tr>
							</thead>
						<tbody>
							{deploymentTable}
						</tbody>
					</table>
          <Dialog ref="dialog"/>
			  </div>
      );
    }
  }
  openDeployModal(slug) {
    this.props.dispatch(openDeployModalAction(slug));
  }
  
  closeDeployModal() {
    this.props.dispatch(closeDeployModalAction());
  }

  closeViewModal() {
    this.props.dispatch(closeViewModalAction());
  }
}
