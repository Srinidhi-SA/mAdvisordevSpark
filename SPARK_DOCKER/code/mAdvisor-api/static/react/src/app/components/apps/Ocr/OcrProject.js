import React from "react";
import { connect } from "react-redux";
import {OcrDocument} from "./OcrDocument";
import { OcrProjectScreen } from "./OcrProjectScreen";
import { OcrTopNavigation } from "./ocrTopNavigation";
import store from '../../../store';
import { saveDocumentPageFlag, saveRevDocumentPageFlag, fetchProjectsSuccess } from '../../../actions/ocrActions';

@connect((store) => {
  return {
    documentFlag: store.ocr.documentFlag,
    imageFlag: store.ocr.imageFlag,
    revDocumentFlag:store.ocr.revDocumentFlag,
  };
})

export class OcrProject extends React.Component {
  constructor(props) {
    super(props);
    if(this.props.documentFlag==''&&this.props.revDocumentFlag==''&& window.location.pathname.includes('reviewer')){
    window.history.go(-1)
  }}
  componentWillMount(){
    this.props.dispatch(fetchProjectsSuccess(""))
    if(store.getState().ocr.selected_project_name!=""){
      this.props.dispatch(saveDocumentPageFlag(true)); // onClick of BreadCrumb(projectName) if selProjName is not empty, setting flag true to Show ProDocTable 
    }
  if(window.location.pathname.includes('project')){
  this.props.dispatch(saveRevDocumentPageFlag(false));
  }
  }

    render() {
   var  renderComponents=null;
   renderComponents=((this.props.documentFlag||this.props.imageFlag)?
    <OcrDocument/>
    :
    <OcrProjectScreen/>
   )
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
