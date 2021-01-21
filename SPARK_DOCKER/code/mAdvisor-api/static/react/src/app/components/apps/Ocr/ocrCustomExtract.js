import React from 'react';
import { saveImagePageFlag, updateOcrImage, updateCustomImage, clearImageDetails, closeFlag, setProjectTabLoaderFlag, tabActiveVal } from '../../../actions/ocrActions';
import { connect } from "react-redux";
import { API } from "../../../helpers/env";
import { getUserDetailsOrRestart, statusMessages } from "../../../helpers/helper";
import { Scrollbars } from 'react-custom-scrollbars';
import { STATIC_URL } from '../../../helpers/env';
import { store } from '../../../store';
import { Tabs, Tab } from 'react-bootstrap';

@connect((store) => {
  return {
    customImgPath: store.ocr.customImgPath,
    originalImgPath: store.ocr.originalImgPath,
    imageSlug: store.ocr.imageSlug,
    ocrImgHeight: store.ocr.ocrImgHeight,
    ocrImgWidth: store.ocr.ocrImgWidth,
    customImageName: store.ocr.customImageName,
    labelsList: store.ocr.labelsList,
  };
})

export class OcrCustomExtract extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      drag: false,
      rect: {},
      endX: "",
      endY: "",
      dragText: "",
      imageDetails: "",
      point1: [],
      point3: [],
      loader: false,
      labelValue: "",
    }
  }

  componentDidMount() {
    var canvas = document.getElementById("ocrCanvas");
    var ctx = canvas.getContext("2d");
    var OcrImg = document.getElementById("customImg");
    OcrImg.onload = () => {
      this.setState({ loader: true });
      ctx.canvas.height = this.props.ocrImgHeight;
      ctx.canvas.width = this.props.ocrImgWidth;
      ctx.drawImage(OcrImg, 0, 0, this.props.ocrImgWidth, this.props.ocrImgHeight);
    };
    canvas.addEventListener('mousedown', this.mouseDown, false);
    canvas.addEventListener('mouseup', this.mouseUp, false);
    canvas.addEventListener('mousemove', this.mouseMove, false);
  }

  mouseDown = (e) => {
    var canvas = document.getElementById("ocrCanvas");
    let canvasrect = canvas.getBoundingClientRect();
    this.state.rect.startX = e.clientX - canvasrect.left;
    this.state.rect.startY = e.clientY - canvasrect.top;
    this.setState({ drag: true });
  }

  mouseUp = (e) => {
    this.setState({ drag: false });
    var OcrImg = document.getElementById("customImg");
    let canvas = document.getElementById("ocrCanvas");
    let canvasrect = canvas.getBoundingClientRect();
    var ctx = canvas.getContext("2d");
    let canvasX = event.clientX - canvasrect.left;
    let canvasY = event.clientY - canvasrect.top;
    this.setState({ endX: canvasX, endY: canvasY });
    let p1 = [];
    p1.push(this.state.rect.startX, this.state.rect.startY);
    this.setState({ point1: p1 });
    let p2 = [];
    p2.push(this.state.endX, this.state.endY);
    this.setState({ point3: p2 });
    var offset = $("#customScroll").offset();
    var X1 = (e.pageX - offset.left);
    var Y1 = (e.pageY - offset.top);
    var dialog = document.getElementById("labelDialog");
    if (p1.toString() != p2.toString()) {
      dialog.setAttribute("style", `position: absolute; left: ${X1}px ;top:  ${Y1}px;display: block; z-index:99`);
      document.getElementById("dialogLoader").classList.add("dialogLoader_ITE")
      this.getTextLabel(p1, p2);
    }
    else if (p1.toString() === p2.toString()) {
      ctx.clearRect(0, 0, this.props.ocrImgWidth, this.props.ocrImgHeight);
      ctx.drawImage(OcrImg, 0, 0, this.props.ocrImgWidth, this.props.ocrImgHeight);
      document.getElementById("labelDialog").style.display = 'none';
    }
  }

  mouseMove = (e) => {
    var OcrImg = document.getElementById("customImg");
    var canvas = document.getElementById("ocrCanvas");
    let canvasrect = canvas.getBoundingClientRect();
    var ctx = canvas.getContext("2d");
    if (this.state.drag) {
      ctx.clearRect(0, 0, this.props.ocrImgWidth, this.props.ocrImgHeight);
      ctx.drawImage(OcrImg, 0, 0, this.props.ocrImgWidth, this.props.ocrImgHeight);
      this.state.rect.w = (e.clientX - canvasrect.left) - this.state.rect.startX;
      this.state.rect.h = (e.clientY - canvasrect.top) - this.state.rect.startY;
      ctx.strokeStyle = '#2a93ff';
      ctx.strokeRect(this.state.rect.startX, this.state.rect.startY, this.state.rect.w, this.state.rect.h);
    }
  }

  closeDialog = () => {
    document.getElementById("labelDialog").style.display = 'none';
  }

  getHeader = (token) => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json',
    }
  }

  getTextLabel = (p1, p2) => {
    return fetch(API + '/ocr/ocrimage/get_word_custom/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "p1": p1, "p3": p2 })
    }).then(response => response.json())
      .then(data => {
        if (data.message == "SUCCESS") {
          this.setState({ imageDetails: data, dragText: data.data });
          document.getElementById("dialogLoader").classList.remove("dialogLoader_ITE")
          document.getElementById("dragText").value = this.state.dragText;
        }
      });
  }
  createLabel = () => {
    document.getElementById("labelDialog").style.display = 'none';
    document.getElementById("customImgLoad").classList.add("loader_ITE_confidence")
    return fetch(API + '/ocr/ocrimage/save_word_custom/', {
      method: 'post',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "slug": this.props.imageSlug, "p1": this.state.point1, "p3": this.state.point3, "label": this.state.labelValue })
    }).then(response => response.json())
      .then(data => {
        if (data.message == "SUCCESS") {
          this.props.dispatch(updateCustomImage(data.generated_image));
          setTimeout(() => {
            document.getElementById("customImgLoad").classList.remove("loader_ITE_confidence")
          }, 2000);
        }
      });
  }
  render() {
    if (this.state.loader) {
      document.getElementById("customBodyloader").style.display = "none";
      document.getElementById("content").style.display = "block";
    }
    return (
      <div>
        <img id="customBodyloader" style={{ position: 'relative', left: '50%', marginLeft: -64, paddingBottom: '8%', paddingTop: '8%' }} src={STATIC_URL + "assets/images/Preloader_2.gif"} />
        <div className="row" id="content" style={{ display: 'none' }}>
          <div className="col-sm-7">
            <div style={{ backgroundColor: '#fff', padding: 15 }}>
              <div id="customImgLoad"></div>
              <Scrollbars style={{ height: 700 }} id="customScroll">
                <canvas
                  onClick={this.handleCoords}
                  id="ocrCanvas"
                ></canvas>

                <img style={{ display: 'none' }}
                  id="customImg"
                  src={this.props.customImgPath}
                />
              </Scrollbars>
            </div>

            <div class="popover fade top in" role="tooltip" id="labelDialog" style={{ display: 'none' }}>
              <span onClick={this.closeDialog} style={{ float: 'right', cursor: 'pointer', color: '#3a988c', paddingRight: 10, paddingTop: 5 }}><i class="fa fa-close"></i></span>
              <div class="popover-content">
                <div className="row">
                  <div id="dialogLoader"></div>
                  <div className="col-sm-12">
                    <div class="form-group" style={{ marginBottom: 15 }}>
                      <label class="form-label">Text</label>
                      <Scrollbars style={{ height: 95 }} >
                        <textarea rows="4" className="form-control" type="text" id="dragText" style={{ fontSize: 14 }} />
                      </Scrollbars>
                    </div>
                  </div>
                  <div className="col-sm-12">
                    <label for="labels">Create or Select Label</label>
                    <input class="form-control" list="labels" name="customLabel" id="customLabel" onInput={(e) => this.setState({ labelValue: e.target.value })} />
                    <datalist id="labels">
                      {
                        this.props.labelsList != undefined && this.props.labelsList.map((i) =>
                          <option key={i}>{i}</option>
                        )
                      }
                    </datalist>
                  </div>
                  <div className="col-sm-12" style={{ marginTop: 20 }}>
                    <button className="btn-primary" style={{ padding: '5px 10px', float: 'right', border: 'none' }} onClick={this.createLabel}>SAVE</button>
                  </div>
                  <div className="col-sm-12" id="successMsg" style={{ paddingTop: 5, color: '#ff8c00' }}></div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-sm-5">
            <div style={{ fontSize: 13, fontWeight: 600 }}>{this.props.customImageName}</div>
            <Tabs defaultActiveKey="label" id="customTab" className="subTab" style={{ marginTop: 25 }}>
              <Tab eventKey="label" title="Labels">
                <div>There is no label added yet.<br></br> Please make a selection on the image and add respective labels.</div>
              </Tab>
              <Tab eventKey="json" title="JSON">
                <div></div>
              </Tab>
            </Tabs>

          </div>
        </div>
      </div>
    )
  }



}