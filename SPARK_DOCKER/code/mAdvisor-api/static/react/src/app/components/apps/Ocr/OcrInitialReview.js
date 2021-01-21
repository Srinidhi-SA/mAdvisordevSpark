import React from "react";
import { connect } from "react-redux";
import { Checkbox } from "primereact/checkbox";
import { saveIRToggleValAction, saveIRConfigAction, saveIRSearchElementAction, autoAssignmentAction} from "../../../actions/ocrActions";
import { Scrollbars } from 'react-custom-scrollbars';
import { STATIC_URL } from "../../../helpers/env";
import store from "../../../store";

@connect((store) => {
  return {
    iRList : store.ocr.iRList,
    iRToggleFlag : store.ocr.iRToggleFlag,
    activeiR : store.ocr.iRConfigureDetails.active,
    selectedIRList : store.ocr.iRConfigureDetails.selectedIRList,
    remainDocs : store.ocr.iRConfigureDetails.test,
    max_docs_per_reviewer : store.ocr.iRConfigureDetails.max_docs_per_reviewer,
    iRLoaderFlag : store.ocr.iRLoaderFlag,
    iRSearchElem : store.ocr.iRSearchElem
  };
})

export class OcrInitialReview extends React.Component {
  constructor(props) {
    super(props);
  }

  saveInitialReviwerToggleVal(e){
    this.props.dispatch(saveIRToggleValAction(e.target.checked))
    var stgName = "initial"
    this.props.dispatch(autoAssignmentAction(stgName,store.getState().ocr.iRToggleFlag));
  }
  saveIRConfig(e){
    if(e.target.id === "assigniRDocsToAll"){
        this.props.dispatch(saveIRConfigAction("selectedIRList",[]));
    }
    if(e.target.name === "selectedIR"){
        let curIRSelUsers= this.props.selectedIRList != undefined ? [...this.props.selectedIRList] :[]
        e.target.checked? curIRSelUsers.push(e.target.value): curIRSelUsers.splice(curIRSelUsers.indexOf(e.value), 1);
        this.props.dispatch(saveIRConfigAction("selectedIRList",curIRSelUsers));
    } 
    else if(e.target.name === "selectAllIR"){
        let nameList = [];
        nameList = e.target.checked?e.target.value.map(i=>i.name):[]
        this.props.dispatch(saveIRConfigAction("selectedIRList",nameList));
    }else if(e.target.name === "activeiR" && e.target.value === "all"){
        this.props.dispatch(saveIRConfigAction("active",e.target.value));
        let nameList = [];
        nameList = e.target.checked?Object.values(this.props.iRList).map(i=>i.name):[]
        this.props.dispatch(saveIRConfigAction("selectedIRList",nameList));
    }
    else if(e.target.name === "activeiR" && e.target.value === "select"){
        this.props.dispatch(saveIRConfigAction("active",e.target.value));
    }
    else if(e.target.name === "testiR"){
        this.props.dispatch(saveIRConfigAction("test",e.target.value));
    }
    else{
        this.props.dispatch(saveIRConfigAction(e.target.name,e.target.value));
    }
  }
  searchIRElement(e){
    this.props.dispatch(saveIRSearchElementAction(e.target.value));
  }

  render() {
    let iReviewerTable = ""
    if(this.props.iRLoaderFlag){
        iReviewerTable = <div style={{ height: "150px", background: "#ffffff", position: 'relative' }}>
                            <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                        </div>
    }
    else if(Object.keys(this.props.iRList).length === 0){
        iReviewerTable = <div className="noOcrUsers">
            <span>No Users Found<br/></span>
        </div>
    }else {
        let listForIRTable = Object.values(this.props.iRList);
        if(this.props.iRSearchElem != ""){
            let iRSearchResults = listForIRTable.filter(s => s.name.includes(this.props.iRSearchElem));
            listForIRTable = iRSearchResults.length === 0?[]:iRSearchResults
        }
        let iRListCount = listForIRTable.length;
        let getDisabledVal = false
        if( $("#assigniRDocsToAll")[0] !=undefined && $("#assigniRDocsToAll")[0].checked){
            getDisabledVal = true
            this.saveIRConfig.bind(this)
        }
        iReviewerTable = 
        <Scrollbars autoHeight autoHeightMin={100} autoHeightMax={300}>
            <table className = "table table-bordered table-hover" id="iRtable" style={{background:"#FFF"}}>
                <thead><tr id="iRtHead">
                    <th className="text-center xs-pr-5" style={{width:"80px"}}>
                        <Checkbox id="selectAllIR" name="selectAllIR" value={listForIRTable} onChange={this.saveIRConfig.bind(this)} checked={( this.props.activeiR === "all" && iRListCount!=0)?true:(this.props.selectedIRList !=undefined && iRListCount!=0 && iRListCount === this.props.selectedIRList.length)?true:false} disabled={getDisabledVal}/>
                    </th>
                    <th style={{width:"40%"}}>NAME</th>
                    <th>EMAIL</th>
                </tr></thead>
                <tbody>
                        { 
                        listForIRTable.length != 0?
                            listForIRTable.map((item,index) => {
                                return (
                                    <tr key={index}>
                                        <td className="text-center">
                                            <Checkbox name="selectedIR" id={item.name} value={item.name} onChange={this.saveIRConfig.bind(this)} checked={ (this.props.activeiR==="all")?true:(this.props.selectedIRList !=undefined && this.props.selectedIRList.includes(item.name))} disabled={getDisabledVal}/>
                                        </td>
                                        <td>{item.name}</td>
                                        <td>{item.email}</td>
                                    </tr>
                                )
                            })
                            :
                            <tr>
                                <td colSpan="3" style={{padding: "50px",textAlign: "center",color: "#29998c"}}>No Users Found</td>
                            </tr>
                    }
                </tbody>
            </table>
        </Scrollbars>
    }
    return (
        <div className="ocrInitialReview">
            <div className="row alert alert-gray">
                <div className="col-md-12">
                    <div className="form-group">
                        <div className="checkbox checbox-switch switch-success">
                            <label>
                                <input type="checkbox" name="iRToggleFlag" defaultChecked={this.props.iRToggleFlag} onChange={this.saveInitialReviwerToggleVal.bind(this)}/>
                                <span></span>
                                Enable automatic reviewer assignment<br/>
                                <small>when enabled, documents that enter workflow will be assigned to reviewers according to your choices below</small>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
                <div className="row alert alert-gray">
                <div className="col-md-12">
                    <h4>Select how to assign documents</h4>
                    <div className="row col-md-8" style={{margin:"0px"}}>
                        <div className="ma-radio">
                            <input type="radio" name="activeiR" value="all" id="assigniRDocsToAll" onClick={this.saveIRConfig.bind(this)} checked={this.props.activeiR === "all"}/>
                            <label for="assigniRDocsToAll">Distribute documents randomnly and evenly to all reviewers</label>
                        </div>
                        {this.props.activeiR === "all" &&
                            <div className="row">
                                <label className="label-control col-md-5 xs-ml-50 mandate" for="iRdocsCountToAll">Maximum number of documents per reviewer</label>
                                <div className="col-md-3">
                                    <input type="number" className="form-control inline" id="iRdocsCountToAll" name="max_docs_per_reviewer" defaultValue={this.props.max_docs_per_reviewer} placeholder="Enter Number..."onInput={this.saveIRConfig.bind(this)} />
                                </div>
                            </div>
                        }
                        <div className="ma-radio">
                            <input type="radio" name="activeiR" value="select" id="assigniRDocsToSelect" onClick={this.saveIRConfig.bind(this)} defaultChecked={!(this.props.activeiR === "all")}/>
                            <label for="assigniRDocsToSelect">Distribute documents randomnly and evenly over selected reviewers</label>
                        </div>
                        {this.props.activeiR === "select" &&
                            <div className="row">
                                <label className="label-control col-md-5 xs-ml-50 mandate" for="iRdocsCountToSelect">Maximum number of documents per reviewer</label>
                                <div className="col-md-3">
                                    <input type="number" className="form-control inline" id="iRdocsCountToSelect" name="max_docs_per_reviewer" defaultValue={this.props.max_docs_per_reviewer} placeholder="Enter Number..." onInput={this.saveIRConfig.bind(this)} />
                                </div>
                            </div>
                        }
                    </div>
                </div>
            </div>
            
            <div className="row alert alert-gray">
                <div className="col-md-12">
                    <h4>Reviewers 
                        { this.props.activeiR === "all" &&
                            <span id="countVal">
                                {this.props.iRList !=0?" ("+Object.keys(this.props.iRList).length+")":"(0)"}</span>
                        }
                        { this.props.activeiR != "all" &&
                            <span id="countVal">{this.props.selectedIRList !=undefined?" ("+this.props.selectedIRList.length+")":"(0)"}</span>
                        }
                    </h4>
                    <div className="pull-right xs-mb-10">
                        <input type="text" id="searchIR" className="form-control" title="Search Name..." style={{marginTop:"-30px"}} placeholder="Search Name..." onKeyUp={this.searchIRElement.bind(this)} />
                    </div>
                    <div className="clearfix"></div>
                    <div className="table-responsive">
                        {iReviewerTable}
                    </div>
                      
                    <div className="col-md-12 alert alert-white xs-mt-15">
                        <div className="col-md-12">
                            <h4>How would you like to assign any remaining documents?</h4>
                            <div className="ma-radio">
                                <input type="radio" name="testiR" value="1" id="assignRemaningIRDocs" onClick={this.saveIRConfig.bind(this)} checked={this.props.remainDocs === "1"||this.props.remainDocs === 1?true:false} />
                                <label for="assignRemaningIRDocs">Continue to distribute even if limits are met</label>
                            </div>
                            <div className="ma-radio">
                                <input type="radio" name="testiR" value="2" id="assignRemaningIRDocs1" onClick={this.saveIRConfig.bind(this)} checked={this.props.remainDocs === "2"||this.props.remainDocs === 2?true:false}/>
                                <label for="assignRemaningIRDocs1">Leave unassigned and move to backlogs</label>
                            </div>
                            <div className="ma-radio">
                                <input type="radio" name="testiR" value="3" id="assignRemaningIRDocs2" onClick={this.saveIRConfig.bind(this)} checked={this.props.remainDocs === "3"||this.props.remainDocs === 3?true:false}/>
                                <label for="assignRemaningIRDocs2">Select reviewers to assign</label>
                            </div>
                        </div>
                    </div>
                     
                </div>
            </div>
            
        </div>
    );
  }
}
