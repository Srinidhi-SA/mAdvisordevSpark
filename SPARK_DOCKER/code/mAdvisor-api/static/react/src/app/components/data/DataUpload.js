import React from "react";
import {connect} from "react-redux";
import { Modal, Button } from "react-bootstrap";
import store from "../../store";
import { ACCESSDENIED} from "../../helpers/helper";
import { open, close, dataUpload} from "../../actions/dataUploadActions";
import { saveFileToStore, updateSelectedDataSrc} from "../../actions/dataSourceListActions";
import { DataSourceList} from "./DataSourceList";

@connect((store) => {
  return {
    showModal: store.dataUpload.dataUploadShowModal,
    fileDataUpload: store.dataUpload.fileUpload,
    selectedDataset: store.datasets.selectedDataSet,
    dataList: store.datasets.dataList};
})

export class DataUpload extends React.Component {
  constructor(props) {
    super(props);
    this.props.dispatch(close());
  }
  openPopup=()=> {
    this.props.dispatch(open());
    var files = [
      {
        name: "",
        size: ""
      }
    ]
    this.props.dispatch(saveFileToStore(files))

  }
  closePopup= ()=> {
    this.props.dispatch(close())
    this.props.dispatch(updateSelectedDataSrc("fileUpload"))
  }
  uploadData = () => {
    this.props.dispatch(dataUpload());
  }
  render() {
    var isDataUpload = this.props.dataList.permission_details.create_dataset;
    let cls = "newCardStyle firstCard"
    let title = "";
    if (!isDataUpload) {
      cls += " disable-card";
      title = ACCESSDENIED
    }
    return (
      <div className="col-md-3 xs-mb-15 list-boxes" title={title}>
        <div className={cls} onClick={this.openPopup}>
          <div className="card-header"></div>
          <div className="card-center newStoryCard">			
            <h2 class="text-center"><i class="fa fa-file-text-o fa-2x"></i> Upload Data </h2>
          </div>
        </div>
        <div id="uploadData" role="dialog" className="modal fade modal-colored-header">
          <Modal show={store.getState().dataUpload.dataUploadShowModal} onHide={this.closePopup} dialogClassName="modal-colored-header uploadData">
            <Modal.Header closeButton>
              <h3 className="modal-title">Upload Data</h3>
            </Modal.Header>
            <Modal.Body>
              <DataSourceList/>
            </Modal.Body>
            <Modal.Footer>
              <Button id="Du_dataCloseBtn" onClick={this.closePopup}>Close</Button>
              <Button id="Du_loadDataBtn" bsStyle="primary" onClick={this.uploadData}>Load Data</Button>
            </Modal.Footer>
          </Modal>
        </div>
      </div>
    )
  }
}
