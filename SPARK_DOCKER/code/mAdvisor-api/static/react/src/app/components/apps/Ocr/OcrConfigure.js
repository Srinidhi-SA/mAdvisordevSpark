import React from "react";
import { connect } from "react-redux";
import { storeSelectedConfigureTabAction, submitReviewerConfigAction, clearReviewerConfigStatesAction, fetchSeconadryReviewerList, fetchInitialReviewerList, setIRLoaderFlagAction, setSRLoaderFlagAction, fetchReviewersRules } from "../../../actions/ocrActions";
import { OcrInitialReview } from "./OcrInitialReview";
import { OcrSecondaryReview } from "./OcrSecondaryReview";
import store from "../../../store";
import { statusMessages } from "../../../helpers/helper";
import { OcrTopNavigation } from "./ocrTopNavigation";

@connect((store) => {
  return {
    configureTabSelected : store.ocr.configureTabSelected,
    selectedIRList : store.ocr.iRConfigureDetails.selectedIRList,
    selectedSRList : store.ocr.sRConfigureDetails.selectedSRList,
    iRConfigureDetails : store.ocr.iRConfigureDetails,
    sRConfigureDetails : store.ocr.sRConfigureDetails,
    iRToggleFlag : store.ocr.iRToggleFlag,
    sRToggleFlag : store.ocr.sRToggleFlag,
  };
})

export class OcrConfigure extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillMount(){
    this.props.dispatch(clearReviewerConfigStatesAction());
    this.props.dispatch(storeSelectedConfigureTabAction("initialReview"));
  }
  
  componentDidMount(){
    this.props.dispatch(setIRLoaderFlagAction(true));
    this.props.dispatch(fetchReviewersRules());
    this.props.dispatch(fetchInitialReviewerList(3));
  }

  saveSelectedConfigureTab(e){
    this.props.dispatch(fetchReviewersRules());
    this.props.dispatch(clearReviewerConfigStatesAction());
    this.props.dispatch(storeSelectedConfigureTabAction(e.target.name));
    if(e.target.name === "initialReview"){
      document.getElementById("searchSR").value = ""
      this.props.dispatch(setIRLoaderFlagAction(true));
      this.props.dispatch(fetchInitialReviewerList(3));
    }else{
      document.getElementById("searchIR").value = ""
      this.props.dispatch(setSRLoaderFlagAction(true));
      this.props.dispatch(fetchSeconadryReviewerList(4))
    }
  }

  submitReviewerConfig(){
    if(this.props.configureTabSelected === "initialReview"){
      if(!this.props.iRToggleFlag){
        let msg= statusMessages("warning","Enable automatic reviewer assignment, to assign documents to reviewers according to your choices.","small_mascot");
        bootbox.alert(msg);
      }else if(!document.getElementById("assigniRDocsToAll").checked && !document.getElementById("assigniRDocsToSelect").checked){
        let msg= statusMessages("warning","Please select how to assign documents","small_mascot");
        bootbox.alert(msg);
      }else if(document.getElementById("assigniRDocsToSelect").checked && this.props.selectedIRList.length === 0){
        let msg= statusMessages("warning","Please select reviewers","small_mascot");
        bootbox.alert(msg);
      }else if((document.getElementById("assignRemaningIRDocs").checked|| document.getElementById("assignRemaningIRDocs1").checked || document.getElementById("assignRemaningIRDocs2").checked)===false){
        let msg= statusMessages("warning","Please input how to assign remaining documents","small_mascot");
        bootbox.alert(msg);
      }else if(document.getElementById("assigniRDocsToAll").checked ){
        if(document.getElementById("iRdocsCountToAll").value ==="" || !Number.isInteger(parseFloat(document.getElementById("iRdocsCountToAll").value)) || parseFloat(document.getElementById("iRdocsCountToAll").value) < 1 ){
          let msg= statusMessages("warning","Please enter valid input.","small_mascot");
          bootbox.alert(msg);
        }
        else{
          this.props.dispatch(submitReviewerConfigAction("initialReview",this.props.iRConfigureDetails));
        }
      }else if(document.getElementById("assigniRDocsToSelect").checked){
        if(document.getElementById("iRdocsCountToSelect").value === "" || !Number.isInteger(parseFloat(document.getElementById("iRdocsCountToSelect").value)) || parseFloat(document.getElementById("iRdocsCountToSelect").value) < 1 ){
          let msg= statusMessages("warning","Please enter valid input.","small_mascot");
          bootbox.alert(msg);
        }
        else{
          this.props.dispatch(submitReviewerConfigAction("initialReview",this.props.iRConfigureDetails));
        }
      }
    }
    else if(this.props.configureTabSelected === "secondaryReview"){
      if(!this.props.sRToggleFlag){
        let msg= statusMessages("warning","Enable automatic reviewer assignment, to assign verified documents to auditors according to your choices.","small_mascot");
        bootbox.alert(msg);
      }
      else if(!document.getElementById("assignSRDocsToAll").checked && !document.getElementById("assignSRDocsToSelect").checked){
        let msg= statusMessages("warning","Please select sampling procedure for Audit","small_mascot");
        bootbox.alert(msg);
      }
      else if(document.getElementById("assignSRDocsToSelect").checked && this.props.selectedSRList.length === 0){
        let msg= statusMessages("warning","Please select reviewers","small_mascot");
        bootbox.alert(msg);
      }
      else if((document.getElementById("assignRemaningSRDocs").checked || document.getElementById("assignRemaningSRDocs1").checked || document.getElementById("assignRemaningSRDocs2").checked)===false){
        let msg= statusMessages("warning","Please input how to assign remaining documents","small_mascot");
        bootbox.alert(msg);
      }
      else if(document.getElementById("assignSRDocsToAll").checked){
        if(document.getElementById("sRdocsCountToAll").value === "" || !Number.isInteger(parseFloat(document.getElementById("sRdocsCountToAll").value)) || parseFloat(document.getElementById("sRdocsCountToAll").value) < 1){
          let msg= statusMessages("warning","Please enter valid input.","small_mascot");
          bootbox.alert(msg);
        }
        else{
          this.props.dispatch(submitReviewerConfigAction("secondaryReview",this.props.sRConfigureDetails));
        }
      }
      else if(document.getElementById("assignSRDocsToSelect").checked){
        if(document.getElementById("sRdocsCountToSelect").value === "" || !Number.isInteger(parseFloat(document.getElementById("sRdocsCountToSelect").value)) || parseFloat(document.getElementById("sRdocsCountToSelect").value) < 1 ){
          let msg= statusMessages("warning","Please enter valid input.","small_mascot");
          bootbox.alert(msg);
        }
        else{
          this.props.dispatch(submitReviewerConfigAction("secondaryReview",this.props.sRConfigureDetails));
        }
      }
    }
  }

  clearReviewerConfigStates(){
    this.props.dispatch(clearReviewerConfigStatesAction())
  }

  render() {
    return (
      <div className="side-body">
          <OcrTopNavigation/>
		  <div className="main-content">
          <section className="ocr_section box-shadow">
            <div className="container-fluid">
                <h3 className="nText">Stages</h3>
                <ul className="nav nav-tabs">
                  <li className={this.props.configureTabSelected === "initialReview"?"active":""}>
                    <a data-toggle="tab" href="#initialReview" name="initialReview" title="Initial Review" onClick={this.saveSelectedConfigureTab.bind(this)}>Initial Review</a>
                  </li>
                  <li>
                    <a data-toggle="tab" href="#secondaryReview" name="secondaryReview" title="Secondary Review" onClick={this.saveSelectedConfigureTab.bind(this)}>Secondary Review</a>
                  </li>
                </ul>
                <div className="tab-content">
                  <div id="initialReview" className={this.props.configureTabSelected === "initialReview"?"tab-pane fade in active":"tab-pane fade"}>
                    <OcrInitialReview/>
                  </div>
                  <div id="secondaryReview" className="tab-pane fade">
                    <OcrSecondaryReview/>
                  </div>
                  <div className="row">
                      <div className="col-md-12 text-right xs-mt-10 xs-mb-10">
                          <button className="btn btn-default" title="Cancel" onClick={this.clearReviewerConfigStates.bind(this)}>Cancel</button> 
                          <button className="btn btn-primary" title="Save" onClick={this.submitReviewerConfig.bind(this)}><i className="fa fa-check-circle"></i> &nbsp; Save</button>
                      </div>
                  </div>
                </div>
            </div>
            </section>
			</div>
      </div>
    );
  }

}
