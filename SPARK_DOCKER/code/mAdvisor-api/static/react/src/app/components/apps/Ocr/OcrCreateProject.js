import React from "react";
import { connect } from "react-redux";
import { Modal, Button, } from "react-bootstrap";
import { getUserDetailsOrRestart } from "../../../helpers/helper"
import store from "../../../store";
import { open, close } from "../../../actions/dataUploadActions";
import { getOcrProjectsList,storeProjectSearchElem,saveDocumentPageFlag,selectedProjectDetails } from '../../../actions/ocrActions';
import { API } from "../../../helpers/env";
import ReactTooltip from 'react-tooltip';
@connect((store) => {
  return {
    login_response: store.login.login_response,
    showModal: store.dataUpload.dataUploadShowModal,
    OcrProjectList: store.ocr.OcrProjectList,
  };
})

export class OcrCreateProject extends React.Component {
  constructor(props) {
    super(props);
    this.props.dispatch(close())
  }

  openPopup() {
    this.props.dispatch(open());
  }

  closePopup() {
    this.props.dispatch(close())
  }

  getHeader = token => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json'
    };
  };

  handleSubmit() {
    let ProjectNameFormat= /^(?=.{8,20}$)[^\\._]?[a-zA-Z0-9]+([._][a-zA-Z0-9]+)*[^\\._]?$/;
    var projectName = document.getElementById('projectName').value

    if (projectName.trim() == "") {
      document.getElementById("resetMsg").innerText = "Please enter project name.";
      return false;
    }
    else if(!ProjectNameFormat.test(document.getElementById("projectName").value)){
      document.getElementById("resetMsg").innerText = "Please enter valid Project Name"
      return false;
    }
  
    var projectDetails = {
      "name": projectName
    }

    return fetch(API + '/ocr/project/', {
      method: "POST",
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify(projectDetails)
    }).then(response => response.json()).then(json => {
      if (json.project_serializer_message === "SUCCESS") {
        this.closePopup()
        this.props.dispatch(selectedProjectDetails(json.project_serializer_data.slug,json.project_serializer_data.name))
        this.props.dispatch(saveDocumentPageFlag(true));
      }
      else
        document.getElementById("resetMsg").innerText = "Project creation failed, Please try again.";
    })
  }


  proceedClick() {
    this.closePopup()
  }

  handleSearchBox(){
    var searchElememt=document.getElementById('search').value.trim()
    this.props.dispatch(storeProjectSearchElem(searchElememt))
    this.props.dispatch(getOcrProjectsList())
  }
  clearSearchElement(){
    document.getElementById('search').value=""
    this.props.dispatch(storeProjectSearchElem(''));
    this.props.dispatch(getOcrProjectsList())
  }

  render() {
    return (
        <div className="row xs-mt-5" style={{ display: 'flex', marginBottom: '1%', alignItems: 'center' }}>
          <div className="col-md-6">
          {this.props.OcrProjectList != '' &&
          <div>
            <div className="col-md-4">
              <h4 className="xs-mt-0 xs-p-5 text-center bg-white box-shadow">{store.getState().ocr.OcrProjectList.overall_info.totalProjects} <i className="fa fa-briefcase fa-1x xs-pl-5 text-light"></i> <br></br><small> PROJECTS</small></h4>
            </div>
            <div className="col-md-4">
              <h4 className="xs-mt-0 xs-p-5 text-center bg-white box-shadow"> {store.getState().ocr.OcrProjectList.overall_info.totalDocuments} <i className="fa fa-file-text-o fa-1x xs-pl-5 text-light"></i><br></br><small> DOCUMENTS</small></h4>
            </div>
            <div className="col-md-4">
              <h4 className="xs-mt-0 xs-p-5 text-center bg-white box-shadow">{store.getState().ocr.OcrProjectList.overall_info.totalReviewers} <i className="fa fa-user-o fa-1x xs-pl-5 text-light"></i><br></br><small> REVIEWERS</small></h4>
            </div>			            
          </div>
          }
          </div>
          <div className="col-md-6 col-md-offset-2 text-right">
            <div className="form-inline">
			        <ReactTooltip place="top" type="light"/>
              <button id="btn_ceate_project" className="btn btn-primary btn-rounded xs-mr-5 000" title="Create Project" onClick={this.openPopup.bind(this)} style={{textTransform:'none'}}><i className="fa fa-plus"></i> New Project</button>
              <span className="search-wrapper">
                <div className="form-group xs-mr-5">
                  <input type="text" title="Search Project..." id="search" className="form-control btn-rounded "  onKeyUp={this.handleSearchBox.bind(this)} placeholder="Search project..."></input>
                  <button className="close-icon"  style={{position:"absolute",left:'165px',top:'7px'}}  onClick={this.clearSearchElement.bind(this)}type="reset"></button>
                </div>
              </span>
            </div>
          </div>
          <div id="uploadData" role="dialog" className="modal fade modal-colored-header">
            <Modal backdrop="static" show={store.getState().dataUpload.dataUploadShowModal} onHide={this.closePopup.bind(this)} dialogClassName="modal-colored-header">
              <Modal.Header closeButton>
                <h3 className="modal-title">Create Project</h3>
              </Modal.Header>
              <Modal.Body className="xs-pl-30 xs-pr-30">
                  <div className="row">
                    <div className="col-md-12">
                      <div className="form-group">
                        <label for="projectName" className="form-label">Project Name <span className="text-danger">*</span></label>
                        <input className="form-control" id="projectName" type="text" placeholder="Project Name" defaultValue={name} />
                      </div>
                    </div>
                    <div className="col-md-12">
                      <div className="form-group">
                        <label for="projectType" className="form-label">Project Type </label>
                        <select id="projectType" className="form-control">
                          <option>Select</option>
                          <option>Financial Services</option>
                          <option>Medical, Health</option>
                          <option>Web Tech</option>
                          <option>Marketing and Customer Experience</option>
                          <option>Others</option>
                        </select>
                      </div>
                    </div>
                    <div className="col-md-12">
                      <div className="form-group">
                        <label for="projectLead" className="form-label">Project Lead</label>
                        <input className="form-control" id="projectLead" type="text" placeholder="Lead Name" />
                      </div>
                    </div>
                  <div className="xs-mt-15 xs-ml-15 xs-mb-0">
                      <ul className="xs-pl-20">
                          <li>Project Name must contain only alphanumeric character, underscore, and dot.</li>
                          <li>Project Name should have 8-20 characters.</li>
                          <li>Underscore and dot can not be next to each other and multiple times in a row.</li>
                      </ul>          
                  </div> 
                </div>
              </Modal.Body>
              <Modal.Footer>
                <div id="resetMsg"></div>
                <Button id="Cp_dataCloseBtn" onClick={this.closePopup.bind(this)}> Close</Button>
                <Button id="Cp_loadDataBtn" onClick={this.handleSubmit.bind(this)} bsStyle="primary">Save</Button>
              </Modal.Footer>
            </Modal>
          </div>
        </div>
    )
  }
}
