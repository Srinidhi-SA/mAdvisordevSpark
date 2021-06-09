//Reviewers table with list of reviewers
import React, { Component } from 'react'
import {getOcrReviewersList,saveRevDocumentPageFlag,selectedReviewerDetails,ocrRevFilterAccuracy, ReviewerTablePagesize}from '../../../actions/ocrActions'
import { connect } from "react-redux";
import store from "../../../store";
import { Pagination } from "react-bootstrap";
import { STATIC_URL } from '../../../helpers/env';
import { Link } from "react-router-dom";

@connect((store) => {
  return {
    OcrReviewerList: store.ocr.OcrReviewerList
  };
})

export default class OcrReviewersTable extends Component {
  constructor(props) {
    super(props)
    this.state = {
      filterVal:'',
    }
  }

componentWillMount = () => this.props.dispatch(getOcrReviewersList())
 
handlePagination = (pageNo) => this.props.dispatch(getOcrReviewersList(pageNo))

handlePageRow = (e) => {
  this.props.dispatch(ReviewerTablePagesize(e.target.value));
  this.props.dispatch(getOcrReviewersList())
}
handleDocumentPageFlag = (slug,name) => {
  this.props.dispatch(saveRevDocumentPageFlag(true));
  this.props.dispatch(selectedReviewerDetails(slug,name))
}

handleFil = (mode) => {                 
  this.disableInputs(mode,'')
  this.setState({filterVal:mode})
}

disableInputs = (mode,reset) => {    
  let  idList=['CEQL','CGTE','CLTE']
  
  let disableIds=reset!='reset'?idList.filter(i=>i!=mode):idList

  if(document.getElementById(mode).value.trim()!='')
  disableIds.map(i=>$(`#${i}`).attr('disabled', true))
  else
  disableIds.map(i=>$(`#${i}`).attr('disabled', false))
}

filterRevList = (reset) => {
  var filterByVal=''

  if(reset!='reset')
    filterByVal = $(`#${this.state.filterVal}`).val().trim()!=''?(this.state.filterVal.slice(1,4)+$(`#${this.state.filterVal}`).val().trim()):"";
  
  this.props.dispatch(ocrRevFilterAccuracy(filterByVal))
  this.props.dispatch(getOcrReviewersList())
  if(reset=='reset'){
    if(this.state.filterVal!=""){
      document.getElementById(this.state.filterVal).value=""
    this.disableInputs(this.state.filterVal,'reset')
    }
  }
}
  render() {
    const pages = this.props.OcrReviewerList.total_number_of_pages;
    const current_page = this.props.OcrReviewerList.current_page;
    let paginationTag = null
    if (pages >= 1) {
      paginationTag = (
         <div className="col-md-12 text-center">
            <div className="footer" id="Pagination">
               <div className="pagination pageRow">
               <span>Rows per page:</span>
               <select className="xs-mr-20 xs-ml-10" onChange={this.handlePageRow} value={store.getState().ocr.reviewerTablePagesize}>
                  <option value="12">12</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="All">All</option>
               </select>
               <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handlePagination} first last next prev boundaryLinks items={pages} activePage={current_page} />
               </div>
            </div>
         </div>
      )
   }

    var reviewersTable = (
      this.props.OcrReviewerList != '' ? (this.props.OcrReviewerList.data.length != 0 ? this.props.OcrReviewerList.data.map((item, index) => {
        return (
          <tr key={index} id={index}>
            <td>
              <i className="fa fa-user-o"></i>
            </td>
            <td><Link to='/apps/ocr-mq44ewz7bp/reviewer/' onClick={() => { this.handleDocumentPageFlag(item.ocr_profile.slug,item.username) }} title={item.username}>{item.username}</Link></td>
            <td>{item.ocr_profile.role[0]}</td>
            <td>{item.ocr_data.assignments}</td>
            <td>{item.ocr_data.completionPercentage}%</td>
            <td>{item.ocr_data.accuracyModel}%</td>
            <td>{new Date(item.last_login).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
            <td><label className={item.ocr_profile.active?"label-success":"label-warning"}>{item.ocr_profile.active?"Active":"Inactive"}</label></td>
          </tr>
        )
      }
      )
        : (<tr><td className='text-center' colSpan={8}>"No data found for your selection"</td></tr>)
      )
        : (<tr><td colSpan={8}><img src={STATIC_URL + "assets/images/Preloader_2.gif"} /></td></tr>)
        )
    return (
      <div className="row">
        <div className="col-md-3 col-sm-12">
           <h4>Reviewers</h4>
        </div>
        <div className="col-sm-12 xs-mt-20">
          <div className="table-responsive" style={{overflowX:'inherit', minHeight:250, background:'rgb(255, 255, 255)'}}>
            <table className="table table-condensed table-hover cst_table ">
              <thead>
                <tr>
                  <th><i className="fa fa-user-o"></i></th>
                  <th>Reviewer Name</th>
                  <th>Role</th>
                  <th>Assignment</th>
                  <th>Complete %</th>
                  <th className="dropdown" >
                    <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Confidence Level" aria-expanded="true">
                      <span>Model Accuracy</span> <b className="caret"></b>
                    </a>
                    <ul className="dropdown-menu scrollable-menu filterOptions">
                      <li><a className="cursor" onClick={()=>this.filterRevList('reset')} name="all" data-toggle="modal" data-target="#modal_equal">All</a></li>
                      <li><a>Equal to</a>
                        <input id='CEQL' onChange={()=>this.handleFil('CEQL')} type='number' ></input></li>
                      <li><a>Greater than</a>
                        <input id='CGTE' onChange={()=>this.handleFil('CGTE')} type='number' ></input></li>
                      <li><a>Less than</a>
                        <input id='CLTE' onChange={()=>this.handleFil('CLTE')} type='number'></input></li>
                      <button className="btn btn-primary filterCheckBtn" onClick={()=>this.filterRevList('')}><i className="fa fa-check"></i></button>
                    </ul>
                  </th>
                  <th>Last Login</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody className="no-border-x">
                {reviewersTable}
              </tbody>
            </table>
          {paginationTag}
          </div>
        </div>
      </div>
    )
  }
}
