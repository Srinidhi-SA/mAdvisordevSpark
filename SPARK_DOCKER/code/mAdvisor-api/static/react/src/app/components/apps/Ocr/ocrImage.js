import React from 'react';
import { setProjectTabLoaderFlag, tabActiveVal } from '../../../actions/ocrActions';
import { connect } from "react-redux";
import { getUserDetailsOrRestart } from "../../../helpers/helper";
import { OcrCompleteExtract } from './OcrCompleteExtract';
import { OcrCustomExtract } from './ocrCustomExtract';
import { Tabs, Tab } from 'react-bootstrap';
@connect((store) => {
  return {
    projectName: store.ocr.selected_project_name,
    reviewerName: store.ocr.selected_reviewer_name,
    selected_image_name: store.ocr.selected_image_name,
  };
})

export class OcrImage extends React.Component {

  breadcrumbClick = () => {
    history.go(-1);
    this.props.dispatch(tabActiveVal('backlog'));
    this.props.dispatch(setProjectTabLoaderFlag(true));
  }

  render() {
    return (
      <div>
        <OcrCompleteExtract />
        {/* <div className="row">
        <div class="col-sm-12">
              {window.location.href.includes("reviewer") ? (<ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/apps/ocr-mq44ewz7bp/reviewer/"><i class="fa fa-arrow-circle-left"></i>{((getUserDetailsOrRestart.get().userRole == "Admin") || (getUserDetailsOrRestart.get().userRole == "Superuser")) ? "Reviewers" : "Projects"}</a></li>
                {((getUserDetailsOrRestart.get().userRole == "Admin") || (getUserDetailsOrRestart.get().userRole == "Superuser")) ?
                  <li class="breadcrumb-item active"><a onClick={() => history.go(-1)} href="#">{this.props.reviewerName}</a></li> :
                  <li class="breadcrumb-item active"><a onClick={() => history.go(-1)} href="#">{this.props.projectName}</a></li>
                }
                <li class="breadcrumb-item active"><a style={{ 'cursor': 'default' }} >{this.props.selected_image_name}</a></li>
              </ol>)
                : (<ol class="breadcrumb">
                  <li class="breadcrumb-item"><a href="/apps/ocr-mq44ewz7bp/project/"><i class="fa fa-arrow-circle-left"></i> Projects</a></li>
                  <li class="breadcrumb-item active"><a onClick={this.breadcrumbClick} href="#">{this.props.projectName}</a></li>
                  <li class="breadcrumb-item active"><a style={{ 'cursor': 'default' }}> {this.props.selected_image_name}</a></li>
                </ol>)
              }
            </div>
        </div> 
        
        <Tabs defaultActiveKey="complete" id="imageTab">
          <Tab eventKey="complete" title="Complete Extraction">
            <OcrCompleteExtract />
          </Tab>
          <Tab eventKey="custom" title="Custom Extraction">
            <OcrCustomExtract />
          </Tab>
        </Tabs> */}
      </div>
    )
  }



}