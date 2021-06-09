import React from "react";
import { connect } from "react-redux";
import { Modal, Button, } from "react-bootstrap";
import { getUserDetailsOrRestart } from "../../../helpers/helper"
import { STATIC_URL } from "../../../helpers/env.js";
import { Scrollbars } from 'react-custom-scrollbars';
import store from "../../../store";
import { open, close } from "../../../actions/dataUploadActions";
import {getOcrUploadedFiles, saveS3BucketDetails, getS3BucketFileList, setS3Loader, saveS3SelFiles, uploadS3Files, clearS3Data, uploadS3FileSuccess, hideS3Modal} from '../../../actions/ocrActions'
import {MultiSelect} from "primereact/multiselect";
import { API } from "../../../helpers/env";
import ReactTooltip from 'react-tooltip';
@connect((store) => {
  return {
    OcrfileUpload: store.ocr.OcrfileUpload,
    login_response: store.login.login_response,
    showModal: store.dataUpload.dataUploadShowModal,
    ocrS3BucketDetails: store.ocr.ocrS3BucketDetails,
    s3Uploaded: store.ocr.s3Uploaded,
    s3Loader: store.ocr.s3Loader,
    s3FileList: store.ocr.s3FileList,
    s3FileFetchErrorFlag: store.ocr.s3FileFetchErrorFlag,
    s3FileFetchSuccessFlag : store.ocr.s3FileFetchSuccessFlag,
    s3SelFileList : store.ocr.s3SelFileList,
    s3FileUploadErrorFlag : store.ocr.s3FileUploadErrorFlag,
    s3FileFetchErrorMsg : store.ocr.s3FileFetchErrorMsg,
    projectslug: store.ocr.selected_project_slug,
  };
})

export class OcrUpload extends React.Component {
  constructor(props) {
    super(props);
    this.fileSizeFlag;
    // this.props.dispatch(close());
    this.state = {
      selectedFiles: "",
      uploaded: false,
      loader: false,
      s3FileList1:[],
      hideModalFlag: false
    }
  }

  getHeader = token => {
    return { Authorization: token };
  };

  openPopup() {
    this.setState({
      selectedFiles: "",
      loader: false,
      uploaded: false,
      s3FileList1:[]
    })
    this.props.dispatch(open());
  }

  closePopup() {
    this.props.dispatch(close())
    this.props.dispatch(clearS3Data());
  }

  onDrop = event => {
    document.getElementById("resetMsg").innerText = "";
    document.getElementById("allUploadFail").innerText="";
    var allowType = ['image/png', 'image/jpeg', 'image/jpg', 'image/tif','application/pdf']
    var formatErr = Object.values(event.target.files).map(i => i.type).map((i, ind) => {
      return allowType.includes(i)
    })

    if (formatErr.includes(false)) {
      document.getElementById("resetMsg").innerText = "Only image files are accepted. Please try again.";
      return false
    }
    this.setState({ selectedFiles: Object.values(event.target.files), })
  }

  removeFile(item) {
    this.setState({
      selectedFiles: Object.values(this.state.selectedFiles).filter(i => i.name != item)
    },()=>{
      if (this.state.selectedFiles==""){
        document.getElementById("allUploadFail").innerText="";
      }
    }
    )
  }

  saveS3Details(e){
    document.getElementById("resetMsg").innerText = "";
    this.props.dispatch(saveS3BucketDetails(e.target.name,e.target.value));
  }
  saveFileForUpload(e){
    document.getElementById("resetMsg").innerText = "";
    this.setState({s3FileList1: e.target.value})
    this.props.dispatch(saveS3SelFiles(e.target.value));
  }

  validateAndFetchS3Files(){
    if($(".bucket_name")[0].value === "" || $(".bucket_name")[0].value === undefined){
      document.getElementById("resetMsg").innerText = "Please Enter Bucket Name";
      return false;
    }else if($(".access_key_id")[0].value === "" || $(".access_key_id")[0].value === undefined){
      document.getElementById("resetMsg").innerText = "Please Enter Access Key";
      return false;
    }else if($(".secret_key")[0].value === "" || $(".secret_key")[0].value === undefined){
      document.getElementById("resetMsg").innerText = "Please Enter Secret Key";
      return false;
    }else{
      document.getElementById("resetMsg").innerText = "";
      this.props.dispatch(setS3Loader(true));
      this.props.dispatch(getS3BucketFileList(this.props.ocrS3BucketDetails));
    }
  }

  handleSubmit(acceptedFiles) {
    let activeId = $(".ocrFileTab").find(".active")[0].innerText;
    let projectSlug= this.props.projectslug;
    this.fileSizeFlag= false;

    if(activeId === "UPLOAD LOCAL FILE"){
      if (acceptedFiles.length == 0) {
        document.getElementById("resetMsg").innerText = "Please select files to upload.";
        return false
      }
      acceptedFiles.map(i=>{
        if(i.size >= 20000000){
          document.getElementById("resetMsg").innerText="Please select file with less than 20MB.";
          this.fileSizeFlag=true
        }
      })

    if(!this.fileSizeFlag){
      document.getElementById("resetMsg").innerText = "";
      document.getElementById("allUploadFail").innerText="";
      $("#dataCloseBtn").hide()
      this.setState({ loader: true })
      $("#hideUploadBtn").show();
      var data = new FormData();
    for (var x = 0; x < acceptedFiles.length; x++) {
      data.append("imagefile", acceptedFiles[x]);
    }
    data.append("dataSourceType", "fileUpload");
    data.append("projectslug", projectSlug);
    return fetch(API + '/ocr/ocrimage/', {
      method: "POST",
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: data
    }).then(response => response.json()).then(json => {
      if (json.message === "SUCCESS" && json.invalid_files== 0){
        this.state.hideModalFlag?this.setState({hideModalFlag:false}):this.setState({ uploaded: true })
      }
      else if(json.serializer_data.length==0){
        $("#dataCloseBtn").show()
        this.setState({ loader: false })
        document.getElementById("allUploadFail").innerText=`Upload failed for the selected files as ${json.invalid_files[0].message}`;
      }
      else if(json.invalid_files.length > 0 && json.serializer_data.length > 0){
        this.setState({ uploaded: true })
        document.getElementById("uploadError").innerText=`Upload failed for ${json.invalid_files.map(i=>i.image).toString()} as ${json.invalid_files[0].message}`;
      }

    })
  }
    }
    else if(activeId === "AMAZON S3 BUCKET"){
      if($(".p-multiselect-label")[0].innerHTML === "Choose"){
        document.getElementById("resetMsg").innerText = "Please select files to upload.";
        return false
      }
      this.props.dispatch(setS3Loader(true));
      this.props.dispatch(uploadS3Files(this.props.s3SelFileList,projectSlug));
    }
  }
 hideModel=()=>{
  this.closePopup();
  this.setState({hideModalFlag:true});
  this.props.dispatch(hideS3Modal(true));
  var refreshList=setInterval(() =>{
  this.props.dispatch(getOcrUploadedFiles());
  if(store.getState().ocr.tabActive=='active'){
  clearInterval( refreshList )
  return false
  }
  }, 3000);
  refreshList;
  setTimeout(function( ) { clearInterval( refreshList );}, 180000);
  this.props.dispatch(getOcrUploadedFiles());
}
  proceedClick() {
    this.closePopup()
    this.props.dispatch(getOcrUploadedFiles())
  }

  getTabContent(e){
    document.getElementById("resetMsg").innerText = "";
    if(e.target.id === "ocrImageTab"){
      $("#dataCloseBtn").show();
      document.getElementById("loadDataBtn").disabled = true;
      document.getElementById("dataCloseBtn").disabled = false;
      if(!this.state.loader && this.state.uploaded){
        this.setState({uploaded:false,loader:false,selectedFiles:""})
        $("#dataCloseBtn").show();
        $("#loadDataBtn").show();
      } 
      else if(this.state.loader && this.state.uploaded){
        this.setState({loader:false})
        $("#dataCloseBtn").hide();
        document.getElementById("loadDataBtn").disabled = false;
      } 
      else if( !this.state.loader && (this.state.selectedFiles != "") ){
        this.setState({selectedFiles:""})
      }
    }
    else if(e.target.id === "ocrS3Tab"){
      $("#fetchS3FileBtn").show();
      $("#dataCloseBtn").show();
      document.getElementById("loadDataBtn").disabled = true;
      document.getElementById("dataCloseBtn").disabled = true;
      if(this.props.s3Loader && (this.props.s3Uploaded === false) ){
        $("#dataCloseBtn").show();
        document.getElementById("loadDataBtn").disabled = true;
      }
      else if(this.props.s3Uploaded && !this.props.s3FileFetchSuccessFlag && this.props.s3Loader){
        this.props.dispatch(setS3Loader(false));
        $("#dataCloseBtn").hide();
        document.getElementById("loadDataBtn").disabled = false;
      }
      else if(this.props.s3Uploaded && !this.props.s3Loader){
        this.props.dispatch(uploadS3FileSuccess(false));
        $("#dataCloseBtn").show();
        document.getElementById("loadDataBtn").disabled = true;
      }else if(this.props.s3FileFetchSuccessFlag){
        $("#fetchS3FileBtn").hide();
        document.getElementById("dataCloseBtn").disabled = false;
      }
    }
  }

  render() {
    let fetchBtnVal = "none";
    let hideBtnVal = "none";
    let uploadBtn = true;
    let uploadBtnstyle = "";
    let proceedBtn = true;

    if(this.props.showModal){
      let activeId = ($(".ocrFileTab").find(".active")[0] !=undefined)?$(".ocrFileTab").find(".active")[0].innerText:"UPLOAD LOCAL FILE"
      if(activeId === "UPLOAD LOCAL FILE"){
        if(this.state.uploaded){
          proceedBtn = false
          hideBtnVal = "none"
        }else if(this.state.loader && !this.state.uploaded){
          hideBtnVal = ""
        }else{
          hideBtnVal = "none"
          uploadBtn = false
          proceedBtn = true
        }
      }else if(activeId === "AMAZON S3 BUCKET"){
        if(this.props.s3Uploaded){
          uploadBtnstyle = "none"
          proceedBtn = false
          hideBtnVal = "none"
        }else if(this.props.s3Loader && !this.props.s3Uploaded && !(this.props.s3FileList === "")){
          hideBtnVal = ""
          uploadBtnstyle = "none"
        }else if(this.props.s3FileFetchSuccessFlag && !this.props.s3FileFetchErrorFlag){
          fetchBtnVal = "none"
          uploadBtn = false
          hideBtnVal = "none"
        }else{
          fetchBtnVal = ""
          uploadBtn = true
          proceedBtn = true
          hideBtnVal = "none"
        }
      }
    }

    let errorMsg = ""
    if(this.props.s3FileFetchErrorFlag && !this.props.s3Uploaded){
      errorMsg = this.props.s3FileFetchErrorMsg;
    }else if(this.props.s3FileUploadErrorFlag){
      errorMsg = this.props.s3FileFetchErrorMsg;
    }

    var fileNames = this.state.selectedFiles != "" ? Object.values(this.state.selectedFiles).map((item, index) => (
      <li key={index}>{item.name} -{item.size/1000} KB
        <span className="xs-ml-15" onClick={this.removeFile.bind(this, item.name)}>
          <i className="fa fa-times" aria-hidden="true" style={{ color: '#555', cursor: 'pointer' }}></i>
        </span>
      </li>
    ))
      : <div className="xs-pl-20 text-center">No files chosen.<br/>Please select file to proceed.</div>
    let optionsTemp = [];
    for(var i=0; i<this.props.s3FileList.length; i++){
      optionsTemp.push({"value":this.props.s3FileList[i],"label":this.props.s3FileList[i]});
    }
    return (
 
      <div style={{ display:"inline-block" }}>
      <ReactTooltip place="top" type="light"/> 
      {this.props.uploadMode == 'topPanel'?
      <Button bsStyle="primary" onClick={this.openPopup.bind(this)} data-tip="Upload Documents" ><i className="fa fa-upload"></i></Button>:
      <div className="icon " onClick={this.openPopup.bind(this)}><i  className="fa fa-upload fa-2x xs-mt-10"></i></div>}
 
        <div id="uploadData" role="dialog" className="modal fade modal-colored-header">
          <Modal show={store.getState().dataUpload.dataUploadShowModal} onHide={this.closePopup.bind(this)} dialogClassName="modal-colored-header ocrUploadModal" backdrop="static">
            <Modal.Header closeButton>
              <h3 className="modal-title">Upload Data</h3>
            </Modal.Header>

            <Modal.Body className="xs-p-0">
              <div className="tab-container ocrFileTab">
                  <ul className="ocrUploadTabs nav-tab" onClick={this.getTabContent.bind(this)}>
                    <li className="active"><a className="nav-link" data-toggle="tab" href="#ocrImage" id="ocrImageTab">Upload Local File</a></li>
                    <li><a className="nav-link" data-toggle="tab" href="#ocrS3" id="ocrS3Tab">Amazon S3 Bucket</a></li>
                  </ul>
              </div>
              <div className="tab-content xs-p-0">
                <div id="ocrImage" className="tab-pane active row xs-m-0">
                  {!this.state.uploaded &&
                    <div>
                      <div className="col-md-5 ocrUploadHeight">
                        <div className="dropzoneOcr">
                          <input className="ocrUpload" type="file" multiple onChange={this.onDrop} title=" " />
                          <img style={{ height: 64, width: 64, opacity: 0.4, zIndex: 0, cursor: 'pointer' }} src={STATIC_URL + "assets/images/ocrUpload.svg"} />
                          <span>Upload files</span>
                        </div>
                      </div>
                      <div className="col-md-7">
                        <Scrollbars className="ocrUploadHeight">
                          <ul className="list-unstyled bullets_primary" style={{ display: 'table-cell', margin: 'auto', height: 250, verticalAlign: 'middle' }}>
                            {fileNames}
                          </ul>
                        </Scrollbars>
                      </div>
                      <div id="allUploadFail" style={{color:'#ff0000',padding:10}}></div>
                    </div>
                  }

                  {(this.state.loader  && !this.state.uploaded) &&
                    <div style={{ height: '100%', width:'100%',position:'absolute',zIndex:9999999,top:0,background: 'rgba(189, 216, 214, 0.5)' }}>
                      <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                    </div>
                  }

                  {this.state.uploaded &&
                    <div className="col-md-12 ocrSuccess">
                      <img className="wow bounceIn" data-wow-delay=".75s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10" src={STATIC_URL + "assets/images/success_outline.png"} style={{ height: 105, width: 105 }} />

                      <div className="wow bounceIn" data-wow-delay=".25s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10">
                        <span className="xs-pt-10" style={{ color: 'rgb(50, 132, 121)', display: 'block' }}>Uploaded Successfully</span></div>
                    <div id="uploadError" style={{position:'absolute',bottom:0,padding:'10px 10px 0px 10px',textAlign:'center'}}></div>
                    </div>
                  }
                </div>

                <div id="ocrS3" className="tab-pane" style={{height:"260px",position:"relative"}}>
                  {!this.props.s3Uploaded &&
                    <div className="s3Detail">
                        <label className="col-sm-4 mandate" for="bucket_name">Bucket Name</label>
                        <div className="col-sm-8 s3DetailsInput">
                          <input type="text" id="bucket_name" name="bucket_name" onInput={this.saveS3Details.bind(this)} className="form-control bucket_name" autoComplete="off"/>
                        </div>
                        <label className="col-sm-4 mandate" for="access_key_id">Access key</label>
                        <div className="col-sm-8 s3DetailsInput">
                          <input type="text" name="access_key_id" id="access_key_id" onInput={this.saveS3Details.bind(this)} className="form-control access_key_id" autoComplete="off"/>
                        </div>
                        <label className="col-sm-4 mandate" for="secret_key">Secret key</label>
                        <div className="col-sm-8 s3DetailsInput">
                          <input type="text" name="secret_key" id="secret_key" onInput={this.saveS3Details.bind(this)} className="form-control secret_key" autoComplete="off"/>
                        </div>
                        {!this.props.s3Uploaded && this.props.s3FileFetchSuccessFlag && (this.props.s3FileList != "") &&
                            <div>
                              <label className="col-sm-4 mandate">Select Files</label>
                              <div className="col-sm-8 s3DetailsInput s3Multiselect">
                                <MultiSelect value={this.state.s3FileList1} options={optionsTemp} style={{minWidth:'12em'}} onChange={this.saveFileForUpload.bind(this)} placeholder="Choose" className="form-control single"/>
                              </div>
                            </div>
                        }
                        <ReactTooltip place="top" type="light"/> 
                        <Button id="fetchS3FileBtn" bsStyle="default" onClick={this.validateAndFetchS3Files.bind(this)} data-tip="Please click here to get files" style={{display:fetchBtnVal}}><i className="fa fa-files-o"></i> Fetch Files</Button>
                    </div>
                  }
                  {this.props.s3Uploaded &&
                    <div className="col-md-12 ocrSuccess">
                    <img className="wow bounceIn" data-wow-delay=".75s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10" src={STATIC_URL + "assets/images/success_outline.png"} style={{ height: 105, width: 105 }} />
                    <div className="wow bounceIn" data-wow-delay=".25s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10">
                      <span  className="xs-pt-10" style={{color: 'rgb(50, 132, 121)', display: 'block' }}>Uploaded Successfully</span></div>
                  </div>
                  }
                </div>
                {this.props.s3Loader && (this.props.s3Uploaded === false) &&
                    <div style={{ height: '100%', width:'100%',position:'absolute',zIndex:9999999,top:0,background: 'rgba(189, 216, 214, 0.5)' }} >
                      <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                    </div>
                  }
            </div>
            </Modal.Body>
            <Modal.Footer>
              <div id="resetMsg">{errorMsg}</div>
              <Button id="hideUploadBtn" bsStyle="primary" onClick={this.hideModel} style={{display:hideBtnVal}}>Hide</Button>
              <Button id="dataCloseBtn" bsStyle="primary" onClick={this.handleSubmit.bind(this, this.state.selectedFiles)} disabled={uploadBtn} style={{display:uploadBtnstyle}}>Upload Data</Button>
              <Button id="loadDataBtn" bsStyle="primary" onClick={this.proceedClick.bind(this)} disabled={proceedBtn}>Proceed</Button>
            </Modal.Footer>
          </Modal>
        </div>
      </div>
    )
  }

}
