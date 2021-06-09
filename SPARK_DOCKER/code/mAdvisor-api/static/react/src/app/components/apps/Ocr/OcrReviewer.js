import React from "react";
import { connect } from "react-redux";
import OcrReviewersTable from '../../apps/Ocr/OcrReviewersTable';
import {OcrDocument} from "./OcrDocument";
import { OcrTopNavigation } from "./ocrTopNavigation";
import {saveRevDocumentPageFlag,selectedReviewerDetails}from '../../../actions/ocrActions'
import { getUserDetailsOrRestart } from "../../../helpers/helper";
import store from "../../../store";
import {RevProjectTable} from './RevProjectTable'
import { RevDocTable } from "./RevDocTable";

@connect((store) => {
  return {
    revDocumentFlag: store.ocr.revDocumentFlag,
  };
})

export class OcrReviewer extends React.Component {
  constructor(props) {
   super(props);
   var userRole=getUserDetailsOrRestart.get().userRole
   if(userRole == "ReviewerL1" || userRole == "ReviewerL2"){ //Skipping revTable to load if userRole is reviewer_  ||
    this.props.dispatch(selectedReviewerDetails('',getUserDetailsOrRestart.get().userName))
   }  
  }

  componentWillMount(){
    if(store.getState().ocr.selected_reviewer_name!="" && (getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole == "Superuser"))
      this.props.dispatch(saveRevDocumentPageFlag(true)); //onClick of BreadCrumb(reviewerName) if selRevName is not empty, setting flag true to Show RevDocTable
  }
  render()
   { 
    var  renderComponents=null;
    var userRole=getUserDetailsOrRestart.get().userRole
    if(userRole == "ReviewerL1" || userRole == "ReviewerL2"){ 
    renderComponents=(
      (store.getState().ocr.revDocumentFlag && store.getState().ocr.selected_project_name)?<RevDocTable/>:
      <RevProjectTable/>)
    }
    else{
    renderComponents=(store.getState().ocr.revDocumentFlag?
    <OcrDocument/>
    :
    <OcrReviewersTable/>
   )
    }
    return (
    <div className="side-body">
      <OcrTopNavigation/>
      <div className="main-content">
        <section className="ocr_section box-shadow">
          <div className="container-fluid">
          {renderComponents}
          </div>
        </section>
      </div>
    </div>
    );
  }
}
