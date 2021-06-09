import React from 'react'
import { Link } from 'react-router-dom';
import {
  getOcrUploadedFiles, saveImagePageFlag, saveDocumentPageFlag, saveImageDetails, pdfPagination,storeOcrTableFilterDetails,resetOcrTableFilterValues,
  saveSelectedImageName, updateCheckList, setProjectTabLoaderFlag, storeDocSearchElem, tabActiveVal, clearImageDetails, docTablePage, docTablePagesize
} from '../../../actions/ocrActions';
import { connect } from "react-redux";
import store from "../../../store";
import { Modal, Pagination, Button } from "react-bootstrap";
import { STATIC_URL } from '../../../helpers/env';
import { Checkbox } from 'primereact/checkbox';
import { getUserDetailsOrRestart, statusMessages } from "../../../helpers/helper"
import { OcrUpload } from "./OcrUpload";
import { API } from "../../../helpers/env";
import ReactTooltip from 'react-tooltip';
import { Scrollbars } from 'react-custom-scrollbars';
@connect((store) => {
  return {
    login_response: store.login.login_response,
    OcrDataList: store.ocr.OcrDataList,
    documentFlag: store.ocr.documentFlag,
    projectName: store.ocr.selected_project_name,
    revDocumentFlag: store.ocr.revDocumentFlag,
    reviewerName: store.ocr.selected_reviewer_name,
    projectTabLoaderFlag: store.ocr.projectTabLoaderFlag,
  };
})

export class OcrTable extends React.Component {
  constructor(props) {
    super(props)
    this.props.dispatch(getOcrUploadedFiles())
    this.state = {
      checkedList: [],
      showRecognizePopup: false,
      recognized: false,
      loader: false,
      exportName: "",
      tab: 'pActive',
      filterVal: '',
      exportType: "json",
      checkAll: false,
      aSyncExtractId: [],
      deleteDocSlug: "",
      deleteDocFlag: false,
      deleteDocName: "",
    }
  }

  componentWillUnmount() {
    this.props.dispatch(saveDocumentPageFlag(false));
  }
  getHeader = token => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json'
    };
  };
  handlePagination = (pageNo) => {
    this.setState({ checkAll: false, checkedList: [] })
    this.props.dispatch(docTablePage(pageNo))
    this.props.dispatch(getOcrUploadedFiles(pageNo))
  }
  handlePageRow=(e)=>{
    this.props.dispatch(docTablePagesize(e.target.value));
    this.setState({ checkAll: false, checkedList: [] });
    this.props.dispatch(getOcrUploadedFiles());
  }
  handleImagePageFlag = (slug,name,doctype) => {
    this.getImage(slug,doctype)
    this.props.dispatch(saveSelectedImageName(name));
    this.props.dispatch(saveImagePageFlag(true));
  }

  getImage = (slug, doctype) => {
    if (doctype == "pdf") {
      return fetch(API + '/ocr/ocrimage/retrieve_pdf/?slug=' + slug + '&page_size=1&page_number=1', {
        method: 'get',
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      }).then((response) => response.json())
        .then(json => {
          this.props.dispatch(saveImageDetails(json.data[0]));
          this.props.dispatch(pdfPagination(json));
        })
    }
    else {
      return fetch(API + '/ocr/ocrimage/' + slug + '/', {
        method: 'get',
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      }).then(response => response.json())
        .then(data => {
          this.props.dispatch(saveImageDetails(data));
        });
    }
  }

  handleFil = (mode) =>  {
    this.disableInputs(mode, '')
    this.setState({ filterVal: mode })
  }

  disableInputs = (mode, reset, filterOn=null) => {
    if(reset=="reset"){ //clear entered value and enable all fields on reset(All)
      var selectedFieldIds = filterOn=='confidence'? ['CEQL','CGTE','CLTE']:['FEQL','FGTE','FLTE'];
      selectedFieldIds.map(i=>document.getElementById(i).value='')
      selectedFieldIds.map(i=>$(`#${i}`).attr('disabled', false))
      
    }else{//disable other two inputs while entering value
      let idList = mode[0] == "C" ? ['CEQL', 'CGTE', 'CLTE'] : ['FEQL', 'FGTE', 'FLTE']  
      let disableIds = idList.filter(i => i != mode)
      
      if (document.getElementById(mode).value.trim() != '')
      disableIds.map(i => $(`#${i}`).attr('disabled', true))
      else
      disableIds.map(i => $(`#${i}`).attr('disabled', false))
    }
  }

  filterOcrList = (filtertBy, filterOn, reset) => {
    var filterByVal = ''
    if (reset != 'reset') {
      filterByVal = (filterOn == ('confidence') || (filterOn == 'fields')) ? $(`#${this.state.filterVal}`).val().trim() != '' ? (this.state.filterVal.slice(1, 4) + $(`#${this.state.filterVal}`).val().trim()) : "" : filtertBy;
    }
    this.props.dispatch(storeOcrTableFilterDetails(filterOn,filterByVal))
    this.props.dispatch(getOcrUploadedFiles())
    if (reset == 'reset') {
      this.disableInputs(this.state.filterVal, 'reset',filterOn)
    }
  }

  handleCheck(data, e) {
    let updateList = [...this.state.checkedList];
    e.checked ? updateList.push(e.value) : updateList.splice(updateList.indexOf(e.value), 1);
    this.setState({ checkedList: updateList });

    let overallSlugs = data.OcrDataList.data.map(i => i.slug);
    if (overallSlugs.length == updateList.length)// make checkAll is true if both the arrays length is same
      this.setState({ checkAll: true })
    else
      this.setState({ checkAll: false })
  }

  handleCheckAll(data, e) {
    this.setState({ checkAll: e.target.checked })
    let overallSlugs = data.OcrDataList.data.map(i => i.slug);

    if (e.target.checked) //If checkAll is true update the state with all the slugs present in the list.
      this.setState({ checkedList: overallSlugs });
    else
      this.setState({ checkedList: [] })
  }

  handleRecognise = () => {
    let recognizeList = [];
    let dataList = this.props.OcrDataList.data;
    for (var i = 0; i < this.state.checkedList.length; i++) {
      let val = dataList.filter(j => j.slug == this.state.checkedList[i])[0].status;
      recognizeList.push(val);
    }
    if (this.state.checkedList.length == 0) {
      bootbox.alert("Please select the image file to recognize.")
      return false;
    }
    else if (!recognizeList.includes("Ready to Recognize")) {
      bootbox.alert("Please select the file with status ready to recognize.")
      return false;
    }
    this.props.dispatch(updateCheckList(this.state.checkedList))
    var postData = {
      'slug': this.state.checkedList
    }
    this.setState({ showRecognizePopup: true, loader: true, recognized: false })
    return fetch(API + '/ocr/ocrimage/extract2/', {
      method: "post",
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify(postData)
    }).then(response => response.json())
      .then(json => {
        if (json.length != 0) {
          var idArray = json.tasks.map(i => i.id)
          this.setState({ aSyncExtractId: idArray })
          this.handleAsyncRecognize();
        }
      })
  }

  handleAsyncRecognize = () => {
    return fetch(API + '/ocr/ocrimage/poll_recognize/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ 'id': this.state.aSyncExtractId })
    }).then(response => response.json())
      .then(json => {
        if (json.map(i => i.state).includes("PROGRESS")) {
          setTimeout(() => {
            this.handleAsyncRecognize();
          }, 5000)
        }
        else if (!json.map(i => i.result[0].message === "SUCCESS").includes(false)) {
          this.setState({ loader: false, recognized: true })
          this.setState({ checkAll: false, checkedList: [] })
        }
        else if (json.map(i => i.result[0].message === "SUCCESS").includes(false)) {
          var failed = json.filter(i => i.result[0].message === "FAILED");
          var imageDetail = failed.map(i => i.result[0].name)[0]
          var message = failed.map(i => i.result[0].error)[0]
          this.closePopup();
          this.setState({ checkAll: false, checkedList: [] })
          this.props.dispatch(getOcrUploadedFiles());
          bootbox.alert(statusMessages("warning", "Recognition failed for " + imageDetail + " due to " + message));
        }
      }
      )
  }

  closePopup = () => {
    this.setState({ showRecognizePopup: false })
  }

  hideClick = () => {
    this.closePopup();
    this.setState({ checkAll: false, checkedList: [] })
    var refreshList = setInterval(() => {
      this.props.dispatch(getOcrUploadedFiles());
      if (store.getState().ocr.tabActive == 'active') {
        clearInterval(refreshList)
        return false
      }
    }, 5000);
    refreshList;
    setTimeout(function () { clearInterval(refreshList); }, 180000);
    this.props.dispatch(getOcrUploadedFiles());
  }

  proceedClick = () => {
    this.closePopup();
    this.setState({ checkAll: false, checkedList: [] })
    this.props.dispatch(getOcrUploadedFiles());
  }

  handleSearchBox = () => {
    var searchElememt = document.getElementById('search').value.trim()
    this.props.dispatch(storeDocSearchElem(searchElememt))
    this.props.dispatch(getOcrUploadedFiles())
  }

  filterByImageStatus = (e) => {
    this.setState({ checkAll: false, checkedList: [] })
    this.props.dispatch(setProjectTabLoaderFlag(true));
    this.props.dispatch(resetOcrTableFilterValues());
    this.props.dispatch(tabActiveVal(e.target.id))
    this.props.dispatch(getOcrUploadedFiles())
  }

  handleExport = () => {
    let dataList = this.props.OcrDataList.data;
    let checkList = this.state.checkedList;
    let statusList = [];
    for (var i = 0; i < checkList.length; i++) {
      let val = dataList.filter(j => j.slug == checkList[i])[0].status;
      statusList.push(val);
    }
    if (this.state.checkedList.length == 0) {
      bootbox.alert("Please select the file to export.")
      return false;
    }
    else if (this.state.checkedList.length > 1) {
      bootbox.alert("Please select only one file to export.")
      return false;
    }
    else if (statusList != "Ready to Export") {
      bootbox.alert("Please select the file with status ready to export.")
      return false;
    }

    this.props.dispatch(updateCheckList(this.state.checkedList));
    this.setState({ exportName: dataList.filter(i => i.slug == checkList)[0].name })
    var exportData = {
      'slug': this.state.checkedList,
      'format': this.state.exportType,
    }
    if (this.state.exportType === "json") {
      return fetch(API + '/ocr/ocrimage/export_data/', {
        method: "post",
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
        body: JSON.stringify(exportData)
      }).then(response => response.json()).then(json => {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(json));
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", `${this.state.exportName}.json`);
        dlAnchorElem.click();
        this.setState({ checkAll: false, checkedList: [] })
      })
    }
    else if (this.state.exportType === "xml") {
      return fetch(API + '/ocr/ocrimage/export_data/', {
        method: "post",
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
        body: JSON.stringify(exportData)
      }).then(response => response.text()).then(json => {
        var dataStr = "data:text/plain;charset=utf-8," + encodeURIComponent(json);
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", `${this.state.exportName}.xml`);
        dlAnchorElem.click();
        this.setState({ checkAll: false, checkedList: [] })
      })
    }
    else if (this.state.exportType === "csv") {
      return fetch(API + '/ocr/ocrimage/export_data/', {
        method: "post",
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
        body: JSON.stringify(exportData)
      }).then(response => response.text()).then(json => {
        var blob = new Blob([json], { type: 'text/csv;charset=utf-8;' });
        var url = URL.createObjectURL(blob);
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", url);
        dlAnchorElem.setAttribute("download", `${this.state.exportName}.csv`);
        dlAnchorElem.click();
        this.setState({ checkAll: false, checkedList: [] })
      })
    }
  }

  closeDeletePopup = () => {
    this.setState({ deleteDocFlag: false })
 }
 openDeletePopUp = (name, slug) => {
    this.setState({ deleteDocName: name, deleteDocSlug: slug, deleteDocFlag: true})
 }

 deleteDocument = () => {
  return fetch(API + '/ocr/ocrimage/' + this.state.deleteDocSlug + '/', {
     method: 'put',
     headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
     body: JSON.stringify({ deleted: true })
  }).then(response => response.json())
     .then(data => {
        if (data.message === "Deleted") {
          this.closeDeletePopup(),
          bootbox.alert(statusMessages("success", "Document deleted.", "small_mascot"))
          this.props.dispatch(getOcrUploadedFiles());
        }
     })
}

  render() {
    const pages = this.props.OcrDataList.total_number_of_pages;
    const current_page = this.props.OcrDataList.current_page;
    let paginationTag = null
    if (pages >= 1) {
      paginationTag = (
        <div className="col-md-12 text-center">
          <div className="footer" id="Pagination">             
            <div className="pagination pageRow">
            <span>Rows per page:</span>
                <select className="xs-mr-20 xs-ml-10" onChange={this.handlePageRow}>
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

    var getAssigneeOptions = (this.props.OcrDataList != '' ? this.props.OcrDataList.data.length != 0 ? [...new Set(this.props.OcrDataList.data.map(i => i.assignee).filter(j => j != null))].map((item,index) => {
      return <li key={index}><a className="cursor" onClick={()=>this.filterOcrList(item, 'assignee')} name="all" data-toggle="modal" data-target="#modal_equal"> {item}</a></li>
    }
    ) : '' : '')

    var getTemplateOptions = (this.props.OcrDataList != '' ? this.props.OcrDataList.values.map((item,index) => {
      return <li key={index}><a className= { store.getState().ocr.filter_template== item ? "active cursor" : "cursor" } onClick={()=>this.filterOcrList(item, 'template')} name="all" data-toggle="modal" data-target="#modal_equal"> {item}</a></li>
    }
    ) : '')



    var ShowModel = (<div id="uploadData" role="dialog" className="modal fade modal-colored-header">
      <Modal backdrop="static" show={this.state.showRecognizePopup} onHide={this.closePopup} dialogClassName="modal-colored-header">
        <Modal.Body className="xs-p-0">
          <div className="row xs-m-0">
            <h4 className="text-center">Recognizing Document</h4>
            {(this.state.loader && !this.state.recognized) &&
              <img src={STATIC_URL + "assets/images/Processing_mAdvisor.gif"} className="img-responsive" style={{ margin: "auto" }} />
            }
            {this.state.recognized &&
              <img src={STATIC_URL + "assets/images/alert_success.png"} className="img-responsive" style={{ margin: "auto" }} />
            }
            <div className="recognizeImgSteps">
              <div className="row">
                <div className="col-sm-9">
                  <ul>
                    <li>Fetching image</li>
                    <li>Text extraction</li>
                    <li>Template Classification</li>
                    <li>Pre processing and mapping</li>
                    <li>Output file created</li>
                  </ul>
                </div>
                <div className="col-sm-3 text-center">
                  {(this.state.loader && !this.state.recognized) &&
                    <h5 className="loaderValue">In Progress</h5>
                  }
                  {this.state.recognized &&
                    <h5 className="loaderValue">Completed</h5>
                  }
                </div>
              </div>
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <div id="resetMsg"></div>
          <Button id="Rd_dataCloseBtn" onClick={this.hideClick} bsStyle="primary">Hide</Button>
          <Button id="Rd_loadDataBtn" onClick={this.proceedClick} disabled={this.state.loader} bsStyle="primary">Proceed</Button>
        </Modal.Footer>
      </Modal>
    </div>)

    var OcrTableHtml = (
      this.props.OcrDataList != '' ? (this.props.OcrDataList.data.length != 0 ? this.props.OcrDataList.data.map((item, index) => {
        var status = ["Ready to Recognize", "Recognizing", "Uploading"]
        return (
          <tr key={index} id={index}>
            <td>
              <Checkbox id={item.slug} name={item.name} value={item.slug} onChange={this.handleCheck.bind(this, this.props)} checked={this.state.checkedList.includes(item.slug)}></Checkbox>
            </td>
            <td>
              <i style={{ color: '#414f50', fontSize: 14 }} className={item.type == ".pdf" ? "fa fa-file-pdf-o" : "fa fa-file-image-o"}></i>
            </td>
            <td style={status.includes(item.status) ? { cursor: 'not-allowed' } : { cursor: 'pointer' }}>
              <Link title={item.name} style={status.includes(item.status) ? { pointerEvents: 'none' } : { pointerEvents: 'auto' }} to={`/apps/ocr-mq44ewz7bp/project/${item.name}`} onClick={() => { this.handleImagePageFlag(item.slug, item.name, item.doctype) }}>{item.name}</Link>
            </td>
            <td>{item.status}</td>
            {store.getState().ocr.tabActive == 'active' &&
              <td>{item.role}</td>
            }
            <td>{item.classification}</td>
            <td>{item.fields}</td>
            <td>{item.confidence}</td>
            {store.getState().ocr.tabActive == 'active' && <td>{item.assignee}</td>}
            <td>{item.created_by}</td>
            <td>{item.modified_by}</td>
            <td>{new Date(item.modified_at).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
            <td>
              <span title="Delete" style={{ cursor: 'pointer', fontSize: 16 }} className="fa fa-trash text-danger xs-mr-5" onClick={() => this.openDeletePopUp(item.name, item.slug)}></span>
            </td>
          </tr>
        )
      }
      )
        : (<tr><td className='text-center' colSpan={11}>"No data found for your selection"</td></tr>)
      )
        : (<tr><td colSpan={11}><img src={STATIC_URL + "assets/images/Preloader_2.gif"} /></td></tr>)
        )

    return (
      <div>
        <div className="row">
          <div className="col-sm-6">
            <a id="downloadAnchorElem" style={{ display: 'none' }}></a>
            {this.props.revDocumentFlag ? (<ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/apps/ocr-mq44ewz7bp/reviewer/" title="Reviewers"><i className="fa fa-arrow-circle-left"></i> Reviewers</a></li>
              <li className="breadcrumb-item active"><a style={{ 'cursor': 'default' }}>{this.props.reviewerName}</a></li>
            </ol>) : (<ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/apps/ocr-mq44ewz7bp/project/" title="Projects"><i className="fa fa-arrow-circle-left"></i> Projects</a></li>
              <li className="breadcrumb-item active"><a style={{ 'cursor': 'default' }}>{this.props.projectName}</a></li>
            </ol>)
            }
          </div>

          {this.props.OcrDataList != '' ? this.props.OcrDataList.total_data_count_wf >= 1 ?
            <div className="col-sm-6 text-right">
              <div className="form-inline">
                <OcrUpload uploadMode={'topPanel'} />

                <ReactTooltip place="top" type="light" />
                <Button onClick={this.handleRecognise} title="Recognize" style={{ textTransform: 'none' }} className="xs-ml-5 xs-mr-5 btn-color" data-tip="Select documents and click here to run ITE operation" >Recognize</Button>

                <ReactTooltip place="left" type="light" id="exportTip" />
                <ul className="export" >
                  <li className="dropdown">
                    <a className="dropdown-toggle" data-toggle="dropdown" href="#">
                      <span data-for="exportTip" className="xs-pr-10" data-tip='Select documents from the list below and click here to export. Documents with status "Ready to Export" only can be exported'>
                        <i className="fa fa-paper-plane"></i>  Export
                      </span>
                      <b className="caret"></b>
                    </a>
                    <ul className="dropdown-menu" onClick={(e) => this.setState({ exportType: e.target.text.toLowerCase() }, this.handleExport)}>
                      <li><a role="tab" value="json" data-toggle="tab">JSON</a></li>
                      <li><a role="tab" value="xml" data-toggle="tab">CSV</a></li>
                      <li><a role="tab" value="csv" data-toggle="tab">XML</a></li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div> : "" : ""}
        </div>



        <div className="tab-container">
          {this.props.OcrDataList != '' ? this.props.OcrDataList.total_data_count_wf >= 1 ? <ul className="nav nav-tabs" style={{ cursor: "default" }}>
            <li className="active"><a data-toggle="tab" id="backlog" name="Backlog" onClick={this.filterByImageStatus} data-tip="Documents that are pending assignment are displayed here">Backlog</a></li>
            <li className=""><a data-toggle="tab" id="active" name="Active" onClick={this.filterByImageStatus} data-tip="Documents that are assigned for review are displayed here">Active</a></li>

            <li className="pull-right">
              <div className="form-group xs-mt-10 xs-mb-0">
                <input type="text" id="search" className="form-control btn-rounded" title="Search by name..." onKeyUp={this.handleSearchBox} placeholder="Search by name..."></input>
              </div>
            </li>
          </ul> : "" : ""}

          <div className="tab-content xs-pl-0 xs-pr-0 xs-pt-0 xs-mt-5">
            <div id="nav" className={this.state.tab === "pActive" ? "tab-pane fade in active" : "tab-pane fade"}>
              <div className="table-responsive noSwipe xs-pb-10" style={{ minHeight: 300 }}>
                {/* if total_data_count_wf <=1 then only render table else show panel box */}
                {!this.props.projectTabLoaderFlag ? this.props.OcrDataList != '' ? this.props.OcrDataList.total_data_count_wf >= 1 ? (
                  <div>
                  <Scrollbars style={{ width: 'calc(100% - 1px)', height: 360 }}>
                    <table id="documentTable" className="tablesorter table table-condensed table-hover cst_table ocrTable">
                      <thead>
                        <tr>
                          {this.props.OcrDataList != '' ? this.props.OcrDataList.data.length != 0 ?
                          <th>
                          <Checkbox onChange={this.handleCheckAll.bind(this, this.props)} checked={this.state.checkAll}></Checkbox>
                          </th>:null:null}
                          <th><i className="fa fa-file-text-o"></i></th>
                          <th>NAME</th>
                          <th className="dropdown" >
                            <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Status" aria-expanded="true">
                              <span>STATUS</span> <b className="caret"></b>
                            </a>
                            <ul className="dropdown-menu scrollable-menu dropdownScroll">
                              <li><a className="cursor" onClick={()=>this.filterOcrList('', 'status')}>All</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('R', 'status')}>Ready to Recognize</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('A', 'status')}>Ready to Assign</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('V1', 'status')}>Ready to Verify(L1)</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('C1', 'status')}>L1 Verified</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('V2', 'status')}>Ready to Verify(L2)</a></li>
                              <li><a className="cursor" onClick={()=>this.filterOcrList('E', 'status')}>Ready to Export</a></li>
                            </ul>
                          </th>
                          {store.getState().ocr.tabActive == 'active' &&
                            <th>ROLE</th>
                          }
                          <th className="dropdown" >
                            <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Template" aria-expanded="true">
                              <span>TEMPLATE</span> <b className="caret"></b>
                            </a>
                            <ul className="dropdown-menu scrollable-menu dropdownScroll template" style={{ minWidth: '130px',paddingLeft:0 }}>
                              <Scrollbars className="templateScroll" style={{ height: 160, overflowX: 'hidden' }} >
                                <li><a className= { store.getState().ocr.filter_template== "" ? "active cursor" : "cursor" }  onClick={()=>this.filterOcrList('', 'template')} name='all'>All</a></li>
                                {getTemplateOptions} 
                              </Scrollbars>
                            </ul>
                          </th>
                          <th className="dropdown" >
                            <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Fields" aria-expanded="true">
                              <span>FIELDS</span> <b className="caret"></b>
                            </a>
                            <ul className="dropdown-menu scrollable-menu filterOptions">
                              <li><a className="cursor" onClick={()=>this.filterOcrList('', 'fields', 'reset')} name="all" data-toggle="modal" data-target="#modal_equal">All</a></li>
                              <li><a >Equal to</a>
                                <input id='FEQL' onChange={()=>this.handleFil('FEQL')} type='number'></input></li>
                              <li><a>Greater than</a>
                                <input id='FGTE' onChange={()=>this.handleFil('FGTE')} type='number'></input></li>
                              <li><a>Less than</a>
                                <input id='FLTE' onChange={()=>this.handleFil('FLTE')} type='number'></input></li>
                              <button className="btn btn-xs btn-primary pull-right xs-mt-10 xs-mr-5 filterCheckBtn" onClick={()=>this.filterOcrList('', 'fields', '')}><i className="fa fa-check"></i></button>
                            </ul>
                          </th>
                          <th className="dropdown" >
                            <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Confidence Level" aria-expanded="true">
                              <span>ACCURACY</span> <b className="caret"></b>
                            </a>
                            <ul className="dropdown-menu scrollable-menu filterOptions">
                              <li><a className="cursor" onClick={()=>this.filterOcrList('', 'confidence', 'reset')} name="all" data-toggle="modal" data-target="#modal_equal">All</a></li>
                              <li><a>Equal to</a>
                                <input id='CEQL' onChange={()=>this.handleFil('CEQL')} type='number' ></input></li>
                              <li><a>Greater than</a>
                                <input id='CGTE' onChange={()=>this.handleFil('CGTE')} type='number' ></input></li>
                              <li><a>Less than</a>
                                <input id='CLTE' onChange={()=>this.handleFil('CLTE')} type='number'></input></li>
                              <button className="btn btn-xs btn-primary filterCheckBtn pull-right xs-mt-10 xs-mr-5" onClick={()=>this.filterOcrList('', 'confidence', '')}><i className="fa fa-check"></i></button>

                            </ul>
                          </th>
                          {store.getState().ocr.tabActive == 'active' ? <th className="dropdown" >
                            <a href="#" data-toggle="dropdown" className="dropdown-toggle cursor" title="Assignee" aria-expanded="true">
                              <span>ASSIGNEE</span> <b className="caret"></b>
                            </a>
                            <ul className="dropdown-menu scrollable-menu dropdownScroll">
                              <li><a className="cursor" onClick={()=>this.filterOcrList('', 'assignee')} name='all'>All</a></li>
                              {getAssigneeOptions}
                            </ul>
                          </th> : null}
                          <th>Created By</th>
                          <th>Modified By</th>
                          <th>Last Modified</th>
                          <th>ACTION</th>
                        </tr>
                      </thead>
                      <tbody className="no-border-x">
                        {OcrTableHtml}
                      </tbody>
                    </table>
                  </Scrollbars>
                  {paginationTag}
                  </div>
                  )
                  :
                  (<div className="panel">
                    <div className="panel-body">
                      <div className="xs-mt-3 xs-mb-3 text-center">
                        <div className="icon-container">
                          <OcrUpload uploadMode={'mainPanel'} />
                          <span className="class">Add a workflow by clicking on the above icon</span>
                        </div>
                      </div>
                    </div>
                  </div>)
                  : (<img className="xs-pt-0" id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"} />)
                  : (<img className="xs-pt-0" id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"} />)
                }
                {ShowModel}
              </div>
            </div>
          </div>
        </div>
        <div role="dialog" className="modal fade modal-colored-header">
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
  }
}