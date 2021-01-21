import React from "react";
import { connect } from "react-redux";
import { saveSRToggleValAction, saveSRConfigAction, saveSRSearchElementAction, autoAssignmentAction } from "../../../actions/ocrActions";
import { Checkbox } from "primereact/checkbox";
import { Scrollbars } from 'react-custom-scrollbars';
import { STATIC_URL } from "../../../helpers/env";
import store from "../../../store";

@connect((store) => {
    return{
        sRList : store.ocr.sRList,
        sRToggleFlag : store.ocr.sRToggleFlag,
        active : store.ocr.sRConfigureDetails.active,
        selectedSRList : store.ocr.sRConfigureDetails.selectedSRList,
        remainDocs : store.ocr.sRConfigureDetails.test,
        max_docs_per_reviewer : store.ocr.sRConfigureDetails.max_docs_per_reviewer,
        sRLoaderFlag : store.ocr.sRLoaderFlag,
        sRSearchElem : store.ocr.sRSearchElem,
    };
})

export class OcrSecondaryReview extends React.Component{
    constructor(props){
        super(props);
    }

    saveSecondaryReviwerToggleVal(e){
        this.props.dispatch(saveSRToggleValAction(e.target.checked))
        var stgName = "secondary"
        this.props.dispatch(autoAssignmentAction(stgName,store.getState().ocr.sRToggleFlag));
    }
    saveSRConfig(e){
        if(e.target.id === "assignSRDocsToAll"){
            this.props.dispatch(saveSRConfigAction("selectedSRList",[]));
        }
        if(e.target.name === "selectedSR"){
            let curSRSelUsers= this.props.selectedSRList != undefined ? [...this.props.selectedSRList] :[]
            e.target.checked? curSRSelUsers.push(e.target.value): curSRSelUsers.splice(curSRSelUsers.indexOf(e.value), 1);
            this.props.dispatch(saveSRConfigAction("selectedSRList",curSRSelUsers));
        } 
        else if(e.target.name === "selectAllSR"){
            let nameList = [];
            nameList = e.target.checked?e.target.value.map(i=>i.name):[]
            this.props.dispatch(saveSRConfigAction("selectedSRList",nameList));
        }else if(e.target.name === "active" && e.target.value === "all"){
            this.props.dispatch(saveSRConfigAction(e.target.name,e.target.value));
            let nameList = [];
            nameList = e.target.checked?Object.values(this.props.sRList).map(i=>i.name):[]
            this.props.dispatch(saveSRConfigAction("selectedSRList",nameList));
        }
        else{
            this.props.dispatch(saveSRConfigAction(e.target.name,e.target.value));
        }
      }
    searchSRElement(e){
        this.props.dispatch(saveSRSearchElementAction(e.target.value))
    }

    render() {
        let sReviewerTable = ""
        if(this.props.sRLoaderFlag){
            sReviewerTable = <div style={{ height: "150px", background: "#ffffff", position: 'relative' }}>
                                <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                            </div>
        }
        else if(Object.keys(this.props.sRList).length === 0){
            sReviewerTable = <div className="noOcrUsers">
                <span>No Users Found<br/></span>
            </div>
        }else {
            let listForSRTable = Object.values(this.props.sRList);
            if(this.props.sRSearchElem != ""){
                let sRSearchResults = listForSRTable.filter(s => s.name.includes(this.props.sRSearchElem));
                listForSRTable = sRSearchResults.length === 0?[]:sRSearchResults
            }
            let sRListCount = listForSRTable.length;
            let getDisabledVal = false
            if($("#assignSRDocsToAll")[0] !=undefined && $("#assignSRDocsToAll")[0].checked){
                getDisabledVal = true
                this.saveSRConfig.bind(this)
            }
            sReviewerTable = 
            <Scrollbars autoHeight autoHeightMin={100} autoHeightMax={300}>
                <table className = "table table-bordered table-hover" id="sRTable" style={{background:"#FFF"}}>
                    <thead><tr id="sRHead">
                        <th className="text-center xs-pr-5" style={{width:"80px"}}><Checkbox id="selectAllSR" name="selectAllSR" value={listForSRTable} onChange={this.saveSRConfig.bind(this)} checked={( this.props.active === "all" && sRListCount!=0)?true:(this.props.selectedSRList != undefined && sRListCount!=0 && sRListCount === this.props.selectedSRList.length)?true:false} disabled={getDisabledVal}/></th>
                        <th style={{width:"40%"}}>NAME</th>
                        <th>EMAIL</th>
                    </tr></thead>
                    <tbody>
                        {
                        listForSRTable.length != 0?
                            listForSRTable.map((item) => {
                                    return (
                                        <tr key={item.name}>
                                            <td className="text-center">
                                                <Checkbox name="selectedSR" id={item.name} value={item.name} onChange={this.saveSRConfig.bind(this)} checked={ (this.props.active==="all")?true:(this.props.selectedSRList !=undefined && this.props.selectedSRList.includes(item.name))} disabled={getDisabledVal}/>
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
            <div className="ocrSecondaryReview">
                <div className="row alert alert-gray">
                    <div className="col-md-12">
                        <div className="form-group">
                            <div className="checkbox checbox-switch switch-success">
                                <label>
                                    <input type="checkbox" name="sRToggleFlag" checked={this.props.sRToggleFlag} onChange={this.saveSecondaryReviwerToggleVal.bind(this)}/>
                                    <span></span>
                                    Enable automatic reviewer assignment<br/>
                                    <small>when enabled, documents that are verified will be assigned to auditors according to your choices below</small>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
                  
                    <div className="row alert alert-gray">
                    <div className="col-md-12">
                        <h4>Select sampling procedure for Audit</h4>
                        <div className="row col-md-8" style={{margin:"0px"}}>
                            <div className="ma-radio">
                                <input type="radio" name="active" value="all" id="assignSRDocsToAll" onClick={this.saveSRConfig.bind(this)} checked={this.props.active === "all"?true:false}/>
                                <label for="assignSRDocsToAll">Distribute documents randomnly and evenly</label>
                            </div>
                            {this.props.active === "all" &&
                                <div className="row">
                                    <label className="label-control col-md-5 xs-ml-50 mandate" for="sRdocsCountToAll">Maximum number of documents per Auditor</label>
                                    <div className="col-md-3">
                                        <input type="number" className="form-control inline" id="sRdocsCountToAll" name="max_docs_per_reviewer" defaultValue={this.props.max_docs_per_reviewer} placeholder="Enter Number..." onInput={this.saveSRConfig.bind(this)} />
                                    </div>
                                </div>
                            }
                            <div className="ma-radio">
                                <input type="radio" name="active" value="select" id="assignSRDocsToSelect" onClick={this.saveSRConfig.bind(this)} checked={this.props.active === "select"?true:false}/>
                                <label for="assignSRDocsToSelect">Distribute documents randomnly and evenly from each of the reviewer</label>
                            </div>
                            {this.props.active === "select" &&
                                <div className="row">
                                    <label className="label-control col-md-5 xs-ml-50 mandate" for="sRdocsCountToSelect">Maximum number of documents per Auditor</label>
                                    <div className="col-md-3">
                                        <input type="number" className="form-control inline" id="sRdocsCountToSelect" name="max_docs_per_reviewer" defaultValue={this.props.max_docs_per_reviewer} placeholder="Enter Number..." onInput={this.saveSRConfig.bind(this)} />
                                    </div>
                                </div>
                            }
                        </div>
                    </div>
                </div>
                 
                <div className="row alert alert-gray">
                    <div className="col-md-12">
                        <h4>Reviewers 
                            { this.props.active === "all" &&
                                <span id="sRCountVal">{this.props.sRList !=0?" ("+Object.keys(this.props.sRList).length+")":"(0)"}</span>
                            }
                            { this.props.active != "all" &&
                                <span id="sRCountVal">{this.props.selectedSRList !=undefined?" ("+this.props.selectedSRList.length+")":"(0)"}</span>
                            }
                        </h4>
                        <div className="pull-right xs-mb-10">
                            <input type="text" id="searchSR" className="form-control" title="Search Name..." style={{marginTop:"-30px"}} placeholder="Search Name..." onKeyUp={this.searchSRElement.bind(this)}/>
                        </div>
                        <div className="clearfix"></div>
                        <div className="table-responsive">
                            {sReviewerTable}
                        </div> 
                        <div className="col-md-12 alert alert-white xs-mt-15">
                            <div className="col-md-12">
                                <h4>How would you like to assign any remaining documents?</h4>
                                <div className="ma-radio">
                                    <input type="radio" name="test" value="1" id="assignRemaningSRDocs" onClick={this.saveSRConfig.bind(this)} checked={this.props.remainDocs === "1"||this.props.remainDocs === 1?true:false}/>
                                    <label for="assignRemaningSRDocs">Continue to distribute even if limits are met</label>
                                </div>
                                <div className="ma-radio">
                                    <input type="radio" name="test" value="2" id="assignRemaningSRDocs1" onClick={this.saveSRConfig.bind(this)} checked={this.props.remainDocs === "2"||this.props.remainDocs === 2?true:false}/>
                                    <label for="assignRemaningSRDocs1">Leave unassigned</label>
                                </div>
                                <div className="ma-radio">
                                    <input type="radio" name="test" value="3" id="assignRemaningSRDocs2" onClick={this.saveSRConfig.bind(this)} checked={this.props.remainDocs === "3"||this.props.remainDocs === 3?true:false}/>
                                    <label for="assignRemaningSRDocs2">Select auditors to assign</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> 
            </div>
        );
    }
}