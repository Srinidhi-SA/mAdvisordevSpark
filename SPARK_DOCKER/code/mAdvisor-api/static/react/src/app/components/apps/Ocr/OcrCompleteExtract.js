import React from 'react';
import { saveImagePageFlag, updateOcrImage, clearImageDetails, closeFlag, setProjectTabLoaderFlag, tabActiveVal, saveImageDetails, pdfPagination } from '../../../actions/ocrActions';
import { connect } from "react-redux";
import { Pagination } from "react-bootstrap";
import { API } from "../../../helpers/env";
import { getUserDetailsOrRestart, statusMessages } from "../../../helpers/helper";
import { Scrollbars } from 'react-custom-scrollbars';
import { STATIC_URL } from '../../../helpers/env';
import { store } from '../../../store';
import ReactTooltip from 'react-tooltip';
@connect((store) => {
  return {
    ocrImgPath: store.ocr.ocrImgPath,
    originalImgPath: store.ocr.originalImgPath,
    imageSlug: store.ocr.imageSlug,
    ocrDocList: store.ocr.OcrRevwrDocsList,
    docTaskId: store.ocr.docTaskId,
    projectName: store.ocr.selected_project_name,
    reviewerName: store.ocr.selected_reviewer_name,
    selected_image_name: store.ocr.selected_image_name,
    is_closed: store.ocr.is_closed,
    template: store.ocr.template,
    classification: store.ocr.classification,
    ocrImgHeight: store.ocr.ocrImgHeight,
    ocrImgWidth: store.ocr.ocrImgWidth,
    pdfSize: store.ocr.pdfSize,
    pdfNumber: store.ocr.pdfNumber,
    pdfDoc: store.ocr.pdfDoc,
    pdfSlug: store.ocr.pdfSlug,
  };
})

export class OcrCompleteExtract extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      text: "",
      imageDetail: "",
      heightLightVal: "10",
      zoom: "Reset",
      x: "",
      y: "",
      img1Load: false,
      img2Load: false,
      badScanFlag: false,
      feedback: "",
      template: "",
    }
  }

  componentDidMount() {
    var OcrImg = document.getElementById("ocrImg");
    OcrImg.onload = () => {
      this.refs.rootImg && this.setState({ img2Load: true });
    };
    $('[data-toggle="popover"]').popover({
      placement: 'top'
    });
  }
  handleCoords = (e) => {
    if ((this.props.is_closed) || (this.state.badScanFlag)) {
      bootbox.alert("This document is submitted for review so editing is restricted");
    }
    else {
      document.getElementById("successMsg").innerText = " ";
      var offset = $("#ocrImg").offset();
      var X = (e.pageX - offset.left);
      var Y = (e.pageY - offset.top);
      if (this.state.zoom == "Reset") {
        this.setState({ x: X, y: Y });
        this.extractText(X, Y);
      }
      else if (this.state.zoom == "110%") {
        var xaxis = X / 1.10;
        var yaxis = Y / 1.10;
        this.setState({ x: xaxis, y: yaxis });
        this.extractText(xaxis, yaxis);
      }
      else if (this.state.zoom == "125%") {
        var xaxis = X / 1.25;
        var yaxis = Y / 1.25;
        this.setState({ x: xaxis, y: yaxis });
        this.extractText(xaxis, yaxis);
      }
      else if (this.state.zoom == "150%") {
        var xaxis = X / 1.50;
        var yaxis = Y / 1.50;
        this.setState({ x: xaxis, y: yaxis });
        this.extractText(xaxis, yaxis);
      }
      var offset = $("#ocrScroll").offset();
      var X1 = (e.pageX - offset.left);
      var Y1 = (e.pageY - offset.top);
      var popOver = document.getElementById("popoverOcr");
      popOver.setAttribute("style", `position: absolute; left: ${X1}px ;top:  ${Y1 - 33}px;display: block; z-index:99`);
    }

  }

  handleMarkComplete = () => {
    let id = this.props.docTaskId;
    let slug= this.props.pdfDoc ? this.props.pdfSlug : this.props.imageSlug
    var data = {
      "status":"reviewed",
      "remarks":"good",
      "task_id": id,
      "slug": slug,
    }
    return fetch(API + '/ocrflow/tasks/submit_task/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
        if (data.submitted === true) {
          this.props.dispatch(closeFlag(data));
          this.finalAnalysis();
          bootbox.alert(statusMessages("success", "Changes have been successfully saved. Thank you for reviewing the document.", "small_mascot"));
        }
      });
  }
  handleBadScan = () => {
    if (this.state.feedback != "") {
    let id = this.props.docTaskId;
    let slug= this.props.pdfDoc ? this.props.pdfSlug : this.props.imageSlug
    var data = {
      "bad_scan": this.state.feedback,
      "task_id": id,
      "slug": slug,
    }
    return fetch(API + '/ocrflow/tasks/feedback/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
        if (data.submitted === true) {
          $('#modal_badscan').hide();
          $('.modal-backdrop').hide();
          this.setState({ badScanFlag: true });
          document.getElementById("badScan").disabled = true;
          document.getElementById("mac").disabled = true;
          bootbox.alert(statusMessages("success", "Feedback submitted.", "small_mascot"));
        }
      })
    }
    else {
      document.getElementById("resetMsg").innerText = "Please provide the feedback"
    }

    // if (this.state.feedback != "") {
    //   let feedbackID = this.props.docTaskId;
    //   var data = new FormData();
    //   data.append("bad_scan", this.state.feedback);
    //   data.append("slug", this.props.imageSlug);
    //   return fetch(API + '/ocrflow/tasks/feedback/?feedbackId=' + feedbackID, {
    //     method: 'post',
    //     headers: this.getHeaderWithoutContent(getUserDetailsOrRestart.get().userToken),
    //     body: data
    //   }).then(response => response.json())
    //     .then(data => {
    //       if (data.submitted === true) {
    //         $('#modal_badscan').hide();
    //         $('.modal-backdrop').hide();
    //         this.setState({ badScanFlag: true });
    //         document.getElementById("badScan").disabled = true;
    //         document.getElementById("mac").disabled = true;
    //         bootbox.alert(statusMessages("success", "Feedback submitted.", "small_mascot"));
    //       }
    //     });
    // }
    // else {
    //   document.getElementById("resetMsg").innerText = "Please provide the feedback"
    // }
  }
  finalAnalysis = () => {
    return fetch(API + '/ocr/ocrimage/final_analysis/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ 'slug': this.props.imageSlug })
    }).then(response => response.json());
  }
  saveTemplate = () => {
    return fetch(API + '/ocr/ocrimage/update_template/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ 'slug': this.props.imageSlug, 'template': this.state.template })
    }).then(response => response.json())
      .then(data => {
        if (data.message == "SUCCESS") {
          bootbox.alert(statusMessages("success", "Template Updated.", "small_mascot"));
        }
      }

      )
  }

  closePopOver = () => {
    document.getElementById("popoverOcr").style.display = 'none';
  }
  zoomIn = () => {
    var img = document.getElementById("ocrImg");
    var originalimg = document.getElementById("originalOcrImg");
    if (this.state.zoom == "Reset") {
      img.style.width = this.props.ocrImgWidth + "px";
      img.style.height = this.props.ocrImgHeight + "px";
      originalimg.style.width = this.props.ocrImgWidth + "px";
      originalimg.style.height = this.props.ocrImgHeight + "px";
    }
    else if (this.state.zoom == "110%") {
      img.style.width = this.props.ocrImgWidth * 1.1 + "px";
      img.style.height = this.props.ocrImgHeight * 1.1 + "px";
      originalimg.style.width = this.props.ocrImgWidth * 1.1 + "px";
      originalimg.style.height = this.props.ocrImgHeight * 1.1 + "px";
    }
    else if (this.state.zoom == "125%") {
      img.style.width = this.props.ocrImgWidth * 1.25 + "px";
      img.style.height = this.props.ocrImgHeight * 1.25 + "px";
      originalimg.style.width = this.props.ocrImgWidth * 1.25 + "px";
      originalimg.style.height = this.props.ocrImgHeight * 1.25 + "px";
    }
    else if (this.state.zoom == "150%") {
      img.style.width = this.props.ocrImgWidth * 1.50 + "px";
      img.style.height = this.props.ocrImgHeight * 1.50 + "px";
      originalimg.style.width = this.props.ocrImgWidth * 1.50 + "px";
      originalimg.style.height = this.props.ocrImgHeight * 1.50 + "px";
    }
  }

  imageScroll = (e) => {
    $("#originalImgDiv div").attr("id", "scrollOriginal");
    $("#ocrScroll div").attr("id", "scrollOcr");
    document.getElementById("scrollOriginal").scrollLeft = e.target.scrollLeft;
    document.getElementById("scrollOcr").scrollLeft = e.target.scrollLeft;
    document.getElementById("scrollOriginal").scrollTop = e.target.scrollTop;
    document.getElementById("scrollOcr").scrollTop = e.target.scrollTop;
  }

  getHeader = (token) => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json',
    }
  }

  getHeaderWithoutContent = (token) => {
    return {
      'Authorization': token,
    }
  }

  extractText = (x, y) => {
    document.getElementById("loader").classList.add("loader_ITE");
    return fetch(API + '/ocr/ocrimage/get_word/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "x": x, "y": y })
    }).then(response => response.json())
      .then(data => {
        this.setState({ imageDetail: data, text: data.word });
        document.getElementById("loader").classList.remove("loader_ITE")
        document.getElementById("ocrText").value = this.state.text;
      });
  }

  updateText = () => {
    document.getElementById("loader").classList.add("loader_ITE")
    let index = this.state.imageDetail.index;
    return fetch(API + '/ocr/ocrimage/update_word/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "x": this.state.x, "y": this.state.y, "word": this.state.text })
    }).then(response => response.json())
      .then(data => {
        if (data.message === "SUCCESS") {
          this.props.dispatch(updateOcrImage(data.generated_image));
          setTimeout(() => {
            document.getElementById("loader").classList.remove("loader_ITE");
            document.getElementById("successMsg").innerText = "Updated successfully.";
          }, 2000);
        }
      });

  }
  notClear = () => {
    document.getElementById("loader").classList.add("loader_ITE")
    let index = this.state.imageDetail.index;
    return fetch(API + '/ocr/ocrimage/not_clear/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "index": index, "word": this.state.text })
    }).then(response => response.json())
      .then(data => {
        if (data.marked === true) {
          document.getElementById("loader").classList.remove("loader_ITE");
          document.getElementById("successMsg").innerText = "Not clear marked.";
        }
      });

  }

  hightlightField = () => {
    document.getElementById("confidence_loader").classList.add("loader_ITE_confidence")
    return fetch(API + '/ocr/ocrimage/confidence_filter/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "filter": Number(this.state.heightLightVal) / 100, })
    }).then(response => response.json())
      .then(data => {
        if (data.message === "SUCCESS") {
          this.props.dispatch(updateOcrImage(data.generated_image));
          setTimeout(() => {
            document.getElementById("confidence_loader").classList.remove("loader_ITE_confidence")
          }, 2000);
        }
      });
  }

  handleText = (e) => {
    this.setState({ text: e.target.value });
    document.getElementById("successMsg").innerText = " ";
  }

  handleImageLoad = () => {
    this.refs.rootImg && this.setState({ img1Load: true });
  }
  breadcrumbClick = () => {
    history.go(-1);
    this.props.dispatch(tabActiveVal('backlog'));
    this.props.dispatch(setProjectTabLoaderFlag(true));
  }
  handleClose = () => {
    this.props.dispatch(saveImagePageFlag(false));
  }
  handlePagination = (pageNo) => {
    return fetch(API + '/ocr/ocrimage/retrieve_pdf/?slug=' + this.props.imageSlug + '&page_size=1&page_number=' + pageNo, {
      method: 'get',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
    }).then((response) => response.json())
      .then(json => {
        this.props.dispatch(saveImageDetails(json.data[0]));
        this.props.dispatch(pdfPagination(json));
      })
  }
  render() {
    let username = ["Devk", "Devc", "Devj"];
    if (this.state.img1Load && this.state.img2Load) {
      document.getElementById("imgLoader").style.display = "none";
      document.getElementById("imgSection").style.display = "block";
    }
    let mark_text = this.props.is_closed != true ? "Mark as complete" : "Completed";
    if (mark_text == "Completed") {
      document.getElementById("badScan").disabled = true
      document.getElementById("mac").disabled = true
    }
    return (
      <div ref="rootImg">
        <img id="imgLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
        <div className="row" id="imgSection" style={{ display: 'none' }}>
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
            <div className="col-sm-12">
              {!username.includes(getUserDetailsOrRestart.get().userName) &&
                <ul className="export" style={{ float: 'right' }} >
                  <li className="dropdown">
                    <a className="dropdown-toggle" data-toggle="dropdown" href="#">
                      <span style={{ paddingRight: 10 }}>Select fields with confidence less than </span>
                      <b className="caret"></b>
                    </a>
                    <ul className="dropdown-menu confidence" style={{ left: 195 }} onClick={(e) => this.setState({ heightLightVal: e.target.className }, this.hightlightField)}>
                      <li><a className="10" role="tab" data-toggle="tab">10%</a></li>
                      <li><a className="20" role="tab" data-toggle="tab">20%</a></li>
                      <li><a className="30" role="tab" data-toggle="tab">30%</a></li>
                      <li><a className="40" role="tab" data-toggle="tab">40%</a></li>
                      <li><a className="50" role="tab" data-toggle="tab">50%</a></li>
                      <li><a className="60" role="tab" data-toggle="tab">60%</a></li>
                      <li><a className="70" role="tab" data-toggle="tab">70%</a></li>
                      <li><a className="80" role="tab" data-toggle="tab">80%</a></li>
                      <li><a className="90" role="tab" data-toggle="tab">90%</a></li>
                      <li><a className="100" role="tab" data-toggle="tab">100%</a></li>
                    </ul>
                  </li>
                </ul>
              }
              {(this.props.classification != "" && this.props.template.length != 0) &&
                <div class="form-group pull-right ocr_highlightblock" style={{ cursor: 'pointer' }}>
                  <label class="control-label xs-mb-0">Template</label>
                  <select class="form-control inline-block 1-100 template" id="subTemplate" defaultValue={this.props.classification} onChange={(e) => this.setState({ template: e.target.value }, this.saveTemplate)}>
                    {this.props.template.map((i, index) => (
                      <option key={index} value={i}>{i}</option>
                    ))
                    }
                  </select>
                </div>
              }
            </div>
          
          <div className="col-sm-6">
            <div style={{ backgroundColor: '#fff', padding: 15 }}>
              <div className="ocrImgTitle">Original</div>
              <Scrollbars style={{ height: 700 }} id="originalImgDiv" onScroll={this.imageScroll}>
                <img style={{ height: `${this.props.ocrImgHeight}px`, width: `${this.props.ocrImgWidth}px` }}
                  src={this.props.originalImgPath}
                  id="originalOcrImg"
                  onLoad={(e) => this.handleImageLoad(e)}
                />
              </Scrollbars>
            </div>
          </div>
          <div className="col-sm-6">
            <div style={{ backgroundColor: '#fff', padding: 15 }}>
              <div className="ocrImgTitle">OCR</div>
              <ul className="export" style={{ float: 'right' }} >
                <li className="dropdown">
                  <a className="dropdown-toggle" data-toggle="dropdown" href="#">
                    <span style={{ paddingRight: 10 }}>
                      <i className="fa fa-search-plus" style={{ fontSize: 15 }}></i>  Zoom
                      </span>
                    <b className="caret"></b>
                  </a>
                  <ul className="dropdown-menu" style={{ left: 9 }} onClick={(e) => this.setState({ zoom: e.target.text }, this.zoomIn)}>
                    <li><a role="tab" data-toggle="tab">110%</a></li>
                    <li><a role="tab" data-toggle="tab">125%</a></li>
                    <li><a role="tab" data-toggle="tab">150%</a></li>
                    <li><a role="tab" data-toggle="tab">Reset</a></li>
                  </ul>
                </li>
              </ul>
              <div id="confidence_loader"></div>
              <Scrollbars id="ocrScroll" style={{ height: 700 }} onScroll={this.imageScroll}>
                <img style={{ height: `${this.props.ocrImgHeight}px`, width: `${this.props.ocrImgWidth}px` }}
                  id="ocrImg"
                  onClick={this.handleCoords}
                  src={this.props.ocrImgPath}
                />
              </Scrollbars>
              <div class="popover fade top in" role="tooltip" id="popoverOcr" style={{ display: 'none' }}>
                <div class="arrow" style={{ left: '91%' }}></div>
                <h3 class="popover-title">Edit
                <span onClick={this.closePopOver} style={{ float: 'right', cursor: 'pointer' }}><i class="fa fa-close"></i></span>
                </h3>
                <div class="popover-content">
                  <div id="loader"></div>
                  <div className="row">
                    <div className="col-sm-10" style={{ paddingRight: 5 }}>
                      <input type="text" id="ocrText" placeholder="Enter text.." onChange={this.handleText} />
                    </div>
                    <div className="col-sm-2" style={{ paddingLeft: 0 }}>
                      <button onClick={this.updateText} ><i class="fa fa-check"></i></button>
                    </div>
                    <div className="col-sm-12" id="successMsg" style={{ paddingTop: 5, color: '#ff8c00' }}></div>
                  </div>
                </div>
              </div>
            </div>

          </div>
          {this.props.pdfDoc &&
          <div className="col-sm-12 text-center sm-mt-30">
          <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handlePagination} first last next prev boundaryLinks items={this.props.pdfSize} activePage={this.props.pdfNumber} />
          </div>
          }
          <div class="col-sm-12 text-right" style={{ marginTop: '3%' }}>
            {(getUserDetailsOrRestart.get().userRole == "ReviewerL1" || getUserDetailsOrRestart.get().userRole == "ReviewerL2") ?
              <div style={{ display: 'inline' }}>
                <ReactTooltip place="top" type="light" />
                <button class="btn btn-warning" id="badScan" data-toggle="modal" data-target="#modal_badscan" data-tip="Tell us if you are not happy with the output">
                  <i class="fa fa-info-circle"></i> Bad Recognition
                </button>
                <button class="btn btn-primary" id="mac" onClick={this.handleMarkComplete}><i class="fa fa-check-circle"></i> &nbsp; {mark_text}</button>
              </div>
              :
              <div></div>
            }
            <button type="button" class="btn btn-default" style={{ cursor: 'pointer', marginLeft: 5, border: '1px solid #ccc' }} onClick={this.handleClose}>
              <i class="fa fa-times-circle" style={{ fontSize: 15, color: '#7a7a7a' }}></i> Close
            </button>
          </div>
          </div>
          <div class="modal fade" id="modal_badscan" tabIndex="-1" role="dialog" aria-labelledby="modal_badscan_modalTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal">&times;</button>
                  <h4 class="modal-title">Send feedback to the team</h4>
                </div>
                <div class="modal-body">
                  <div class="form-group">
                    <label for="txt_bscan">Tell us how would we improve?</label>
                    <input type="text" class="form-control" id="txt_bscan" placeholder="Enter text" onChange={(e) => this.setState({ feedback: e.target.value })} />
                    <p>For technical support, please contact info@madvisor-dev.marlabs.com</p>
                  </div>
                </div>
                <div class="modal-footer">
                  <div id="resetMsg"></div>
                  <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary" onClick={this.handleBadScan}>Submit</button>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
  }

  componentWillUnmount = () => {
    this.props.dispatch(saveImagePageFlag(false));
    this.props.dispatch(clearImageDetails());
  }

}