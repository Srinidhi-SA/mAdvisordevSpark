//Reviewers document table contains list of documents belongs to particular reviewer
import React from 'react'
import { Link } from 'react-router-dom';
import { getRevrDocsList, saveImagePageFlag,saveImageDetails,saveSelectedImageName,saveRevDocumentPageFlag,ocrRdFilterDetails,resetRdFilterSearchDetails,clearImageDetails,storeSearchInRevElem,rDocTablePagesize,pdfPagination,savePdfFlag,saveTaskId} from '../../../actions/ocrActions';
import { connect } from "react-redux";
import { Pagination } from "react-bootstrap";
import { STATIC_URL } from '../../../helpers/env';
import { getUserDetailsOrRestart, statusMessages } from "../../../helpers/helper"
import { API } from "../../../helpers/env";
import { Scrollbars } from 'react-custom-scrollbars';
import { Modal, Button, } from "react-bootstrap/";

@connect((store) => {
  return {
    login_response: store.login.login_response,
    OcrRevwrDocsList: store.ocr.OcrRevwrDocsList,
    documentFlag: store.ocr.documentFlag,
    revDocumentFlag:store.ocr.revDocumentFlag,
    reviewerName: store.ocr.selected_reviewer_name,
    projectName:store.ocr.selected_project_name,
    template: store.ocr.filter_rd_template,
  };
})

export class RevDocTable extends React.Component {
  constructor(props) {
    super(props)
    this.props.dispatch(getRevrDocsList())
    this.state = {
      filterVal:'',
      deleteDocSlug: "",
      deleteDocFlag: false,
      deleteDocName: "",
      deleteTask: "",
    }
  }
  componentWillUnmount() {
  this.props.dispatch(saveRevDocumentPageFlag(false));
  }

  getHeader = token => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json'
    };
  };

  handlePagination = (pageNo) =>  this.props.dispatch(getRevrDocsList(pageNo))
  
  handleRPageRow=(e)=>{
    this.props.dispatch(rDocTablePagesize(e.target.value));
    this.props.dispatch(getRevrDocsList())
  }
  handleImagePageFlag = (slug,name,doctype) => {
    this.getImage(slug,doctype)
    this.props.dispatch(saveSelectedImageName(name));
    this.props.dispatch(saveImagePageFlag(true));
    this.fetchTask(slug,doctype);
  }

  fetchTask = (slug, doctype) => {
    return fetch(API + '/ocr/ocrimage/get_task_id/?slug=' + slug, {
      method: 'get',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
    }).then(response => response.json())
      .then(data => {
        if (data.message == "SUCCESS") {
          this.props.dispatch(saveTaskId(data))
        }
      })
  }
  
  getImage = (slug,doctype) => {
    if (doctype == "pdf") {
      return fetch(API + '/ocr/ocrimage/retrieve_pdf/?slug=' + slug + '&page_size=1&page_number=1', {
        method: 'get',
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      }).then((response) => response.json())
        .then(json => {
          this.props.dispatch(saveImageDetails(json.data[0]));
          this.props.dispatch(savePdfFlag(slug));
          this.props.dispatch(pdfPagination(json));
        })
    }
    else {
    return fetch(API + '/ocr/ocrimage/'+ slug +'/', {
      method: 'get',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
    }).then(response => response.json())
      .then(data => {
        this.props.dispatch(saveImageDetails(data));
      });
  }
}

  handleFil = (mode) =>{
    this.disableInputs(mode,'')
    this.setState({filterVal:mode})
  }
 
  disableInputs = (mode,reset,filterOn=null) => {
    if(reset=="reset"){ //clear entered value and enable all fields on reset(All)
      var selectedFieldIds = filterOn=='confidence'? ['CEQL','CGTE','CLTE']:['FEQL','FGTE','FLTE'];
      selectedFieldIds.map(i=>document.getElementById(i).value='')
      selectedFieldIds.map(i=>$(`#${i}`).attr('disabled', false))
      
    }else{ //disable  other two fields on entering value
      let idList = mode[0]=="C"? ['CEQL','CGTE','CLTE']:['FEQL','FGTE','FLTE'];
      let disableIds=idList.filter(i=>i!=mode)
       if(document.getElementById(mode).value.trim()!='')
       disableIds.map(i=>$(`#${i}`).attr('disabled', true))
       else
       disableIds.map(i=>$(`#${i}`).attr('disabled', false))
    }
}

  filterRevDocrList = (filtertBy, filterOn,reset ) => {
    var filterByVal=''
    if(reset!='reset'){
      filterByVal = (filterOn==('confidence')||(filterOn=='fields'))?$(`#${this.state.filterVal}`).val().trim()!=''?(this.state.filterVal.slice(1,4)+$(`#${this.state.filterVal}`).val().trim()):"":filtertBy;
    }
    this.props.dispatch(ocrRdFilterDetails(filterOn,filterByVal))
    this.props.dispatch(getRevrDocsList())
    if(reset=='reset'){
      this.disableInputs(this.state.filterVal,'reset',filterOn)
    }
  }

  handleSearchBox = () => {
    var searchElememt=document.getElementById('searchInRev').value.trim()
    this.props.dispatch(storeSearchInRevElem(searchElememt))
    this.props.dispatch(getRevrDocsList())
  }
  clearSearchElement = () => {
    document.getElementById('searchInRev').value=""
    this.props.dispatch(storeSearchInRevElem(''));
    this.props.dispatch(getRevrDocsList())
  }

  closeDeletePopup = () =>  this.setState({ deleteDocFlag: false })
 
  openDeletePopUp = (name, slug, task) => this.setState({ deleteDocName: name, deleteDocSlug: slug, deleteDocFlag: true, deleteTask: task})

 deleteDocument = () => {
  let task = this.state.deleteTask[0].id;
  return fetch(API + '/ocrflow/review/' + task + '/', {
     method: 'put',
     headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
     body: JSON.stringify({ deleted: true ,"image_slug": this.state.deleteDocSlug})
  }).then(response => response.json())
     .then(data => {
        if (data.message === "Deleted") {
          this.closeDeletePopup(),
          bootbox.alert(statusMessages("success", "Document deleted.", "small_mascot"))
          this.props.dispatch(getRevrDocsList())
        }
     })
}
  render() {
    const pages = this.props.OcrRevwrDocsList.total_number_of_pages;
    const current_page = this.props.OcrRevwrDocsList.current_page;
    let paginationTag = null
    let breadcrumb=null;
    if (pages >= 1) {
      paginationTag = (
        <div className="col-md-12 text-center">
          <div className="footer" id="Pagination">
            <div className="pagination pageRow">
            <span>Rows per page:</span>
                <select className="xs-mr-20 xs-ml-10" onChange={this.handleRPageRow}>
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
    breadcrumb=(
      <ol className="breadcrumb">
        <li className="breadcrumb-item">
          <a href="/apps/ocr-mq44ewz7bp/reviewer/">
            <i className="fa fa-arrow-circle-left"></i>
            {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole == "Superuser")? 'Reviewers':'Projects'}
          </a>
        </li>
        <li className="breadcrumb-item active">
          <a style={{'cursor':'default'}}>
            {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole == "Superuser")? this.props.reviewerName : this.props.projectName}
          </a>
        </li>
      </ol>
    )
    var OcrRevDocTableHtml = (
      this.props.OcrRevwrDocsList != '' ? (this.props.OcrRevwrDocsList.data.length != 0 ? this.props.OcrRevwrDocsList.data.map((item, index) => {
        return (
          <tr key={index} id={index}>
             <td>
              <i style={{ color: '#414f50', fontSize: 14 }} className={item.ocrImageData.doctype == "pdf" ? "fa fa-file-pdf-o" : "fa fa-file-image-o"}></i>
            </td>
            <td><Link to={`/apps/ocr-mq44ewz7bp/reviewer/${item.ocrImageData.name}`}onClick={() => { this.handleImagePageFlag(item.ocrImageData.slug,item.ocrImageData.name,item.ocrImageData.doctype) }} title={item.ocrImageData.name}>{item.ocrImageData.name}</Link></td>
            <td>{item.status}</td>
            <td>{item.ocrImageData.classification}</td>
            <td>{item.ocrImageData.fields}</td>
            <td>{item.ocrImageData.confidence}</td>
            <td>{new Date(item.created_on).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
            <td>{new Date(item.modified_at).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
            <td>{item.modified_by}</td>
            <td>
              <span title="Delete" style={{ cursor: 'pointer', fontSize: 16 }} className="fa fa-trash text-danger xs-mr-5" onClick={() => this.openDeletePopUp(item.ocrImageData.name, item.ocrImageData.slug, item.tasks)}></span>
            </td>
          </tr>
        )
      }
      )
        : (<tr><td className='text-center' colSpan={9}>"No data found for your selection"</td></tr>)
      )
        : (<tr><td colSpan={8}><img src={STATIC_URL + "assets/images/Preloader_2.gif"} /></td></tr>)
        )
    let templateOptions= (this.props.OcrRevwrDocsList!=""?
    this.props.OcrRevwrDocsList.values.map((item,index)=>{
      return(
          <li key={index}><a className={ this.props.template == item ? "active cursor" : "cursor" } onClick={()=> this.filterRevDocrList(item,'template')} name={item} data-toggle="modal" data-target="#modal_equal"> {item}</a></li>
      )}):
      "")
    return (
    <div>
      <div className="row">
        <div className="col-md-6">
         {breadcrumb}
        </div>
        <div className="col-md-6 text-right">
          <div className="form-inline xs-mb-10">
            <span className="search-wrapper">
              {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole == "Superuser")?
              <div className="form-group xs-mr-5">
                <input type="text" title="Search Project..." id="searchInRev" className="form-control btn-rounded " onKeyUp={this.handleSearchBox} placeholder="Search project..."></input>
                <button className="close-icon"  style={{position:"absolute",left:'165px',top:'7px'}} onClick={this.clearSearchElement} type="reset"></button>
              </div>
                :""}
            </span>
          </div>
        </div>
      </div>
            <div className="table-responsive noSwipe xs-pb-10" style={{minHeight:250,background:'#fff',overflow:'inherit'}}>
          {/* if total_data_count_wf <=1 then only render table else show panel box */}
            {this.props.OcrRevwrDocsList != '' ? 
             (
            <Scrollbars style={{ width: 'calc(100% - 1px)', height:390 }}>
            <table id="reviewDocumentTable" className="tablesorter table table-condensed table-hover cst_table ocrTable">
             <thead>
              <tr>
              <th><i className="fa fa-file-text-o"></i></th>
                <th>NAME</th>
                <th className="dropdown" >
                  <a href="#" data-toggle="dropdown"  className="dropdown-toggle cursor" title="Status" aria-expanded="true">
                    <span>STATUS</span> <b className="caret"></b>
                  </a>
                  <ul className="dropdown-menu scrollable-menu">
                    <li><a className="cursor" onClick={()=>this.filterRevDocrList('', 'status')} name='all'>All</a></li>
                    <li><a className="cursor" onClick={()=>this.filterRevDocrList('pendingL1', 'status')} name="pending">Review Pending(L1)</a></li>
                    <li><a className="cursor" onClick={()=>this.filterRevDocrList('pendingL2', 'status')} name="reviewed">Review Pending(L2)</a></li>
                    <li><a className="cursor" onClick={()=>this.filterRevDocrList('reviewedL1', 'status')} name="pending">Review Completed(L1)</a></li>
                    <li><a className="cursor" onClick={()=>this.filterRevDocrList('reviewedL2', 'status')} name="reviewed">Review Completed(L2)</a></li>
                  </ul>
                </th>
                <th className="dropdown" >
                          <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Template" aria-expanded="true">
                            <span>TEMPLATE</span> <b className="caret"></b>
                          </a>
                          <ul className="dropdown-menu scrollable-menu dropdownScroll template xs-pl-0" style={{minWidth:'130px'}}>
                          <Scrollbars className="templateScroll" style={{ height: 160,overflowX:'hidden' }} >
                            <li><a className={ this.props.template == "" ? "active cursor" : "cursor" } onClick={()=>this.filterRevDocrList('', 'template')} name='all'>All</a></li>
                            {templateOptions}
                             </Scrollbars>
                          </ul>
                        </th>
                <th className="dropdown" >
                          <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Fields" aria-expanded="true">
                            <span>FIELDS</span> <b className="caret"></b>
                          </a>
                          <ul className="dropdown-menu scrollable-menu filterOptions">
                            <li><a className="cursor" onClick={()=>this.filterRevDocrList('', 'fields','reset')} name="all" data-toggle="modal" data-target="#modal_equal">All</a></li>
                            <li><a>Equal to</a> 
                             <input id='FEQL' onChange={()=>this.handleFil('FEQL')} type='number'></input></li>
                            <li><a>Greater than</a>
                             <input id='FGTE' onChange={()=>this.handleFil('FGTE')} type='number'></input></li>
                            <li><a>Less than</a>
                             <input id='FLTE' onChange={()=>this.handleFil('FLTE')} type='number'></input></li>
                            <button className="btn btn-primary filterCheckBtn"  onClick={()=>this.filterRevDocrList('', 'fields','')}><i className="fa fa-check"></i></button>
                         </ul>
                        </th>
                       <th className="dropdown" >
                          <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Confidence Level" aria-expanded="true">
                            <span>ACCURACY</span> <b className="caret"></b>
                          </a>
                          <ul className="dropdown-menu scrollable-menu filterOptions">
                            <li><a className="cursor" onClick={()=>this.filterRevDocrList('', 'confidence','reset')} name="all" data-toggle="modal" data-target="#modal_equal">All</a></li>
                            <li><a >Equal to</a>
                             <input id='CEQL' onChange={()=>this.handleFil('CEQL')} type='number' ></input></li>
                            <li><a >Greater than</a>
                             <input id='CGTE' onChange={()=>this.handleFil('CGTE')} type='number' ></input></li>
                            <li><a >Less than</a>
                             <input id='CLTE' onChange={()=>this.handleFil('CLTE')} type='number'></input></li>
                            <button className="btn btn-primary filterCheckBtn" onClick={()=>this.filterRevDocrList( '', 'confidence','')}><i className="fa fa-check"></i></button>
                          </ul>
                        </th>
                <th>Created</th>
                <th>Modified</th>
                <th>Modified By</th>
                <th>ACTION</th>
              </tr>
             </thead>
             <tbody className="no-border-x">
              {OcrRevDocTableHtml}
             </tbody>
            </table>
            </Scrollbars>)
            : (<img id="loading" className="xs-pt-0" src={STATIC_URL + "assets/images/Preloader_2.gif"} />)
          }
          {paginationTag}
         </div>
         <div id="deleteProject" role="dialog" className="modal fade modal-colored-header">
               <Modal backdrop="static" show={this.state.deleteDocFlag} onHide={this.closeDeletePopup} dialogClassName="modal-colored-header">
                  <Modal.Header closeButton>
                     <h3 className="modal-title">Delete Project</h3>
                  </Modal.Header>
                  <Modal.Body style={{ padding: '20px 15px 25px 15px' }}>
                     <div className="row">
                        <div className="col-sm-4">
                           <img style={{ width: '100%' }} src={STATIC_URL + "assets/images/alert_warning.png"} />
                        </div>
                        <div className="col-sm-8">
                           <h4 className="text-warning">Warning !</h4>
                           <div>Are you sure you want to delete {this.state.deleteDocName} document?</div>
                           <div className="xs-mt-10">
                              <Button bsStyle="primary" onClick={this.deleteDocument}>Yes</Button>
                              <Button onClick={this.closeDeletePopup}>No</Button>
                           </div>
                        </div>
                     </div>
                  </Modal.Body>
               </Modal>
            </div>
    </div>
    )
  }
  componentWillUnmount = () => {
    this.props.dispatch(clearImageDetails());
    this.props.dispatch(resetRdFilterSearchDetails())
  }
}