import React from "react";
import {connect} from "react-redux";
import {
  Tab,
  Row,
  Col,
  Nav,
  NavItem
} from "react-bootstrap";
import Dropzone from 'react-dropzone'
import store from "../../store";
import $ from "jquery";
import { FILEUPLOAD, bytesToSize} from "../../helpers/helper";
import { getDataSourceList, saveFileToStore, updateSelectedDataSrc } from "../../actions/dataSourceListActions";
import { getAllDataList } from "../../actions/dataActions";
import { Scrollbars } from 'react-custom-scrollbars';
import { STATIC_URL } from "../../helpers/env";
@connect((store) => {
  return {
    fileUpload: store.dataSource.fileUpload,
    allDataList:store.datasets.allDataSets,
    dataSourceLoaderFlag: store.dataSource.dataSourceLoaderFlag
  };
})

export class DataSourceList extends React.Component {

  constructor(props) {
    super(props);
  }
  componentWillMount() {
    this.props.dispatch(getDataSourceList());
    this.props.dispatch(getAllDataList());
  }
  onDrop(files) {
    let empltyFile= [];
    empltyFile[0] = {
      "name": "",
      "size": ""
    };
    this.props.dispatch(saveFileToStore(empltyFile))
    var duplicateFlag="";
    var duplicateName="";
    if (files.length > 0) {
      if(this.props.allDataList!=""){
        var alldatasetList = this.props.allDataList.data.map(i=>i.name.toLowerCase());
        for (var i=0;i<files.length;i++){
          if(alldatasetList.includes(files[i].name.toLowerCase().split('.').slice(0, -1).join('.'))){
            duplicateFlag= true;
            duplicateName= files[i].name;
          }
        }
      }

      if (files[0].size == 0) {
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("The uploaded file is empty, please upload the correct file");
      }
      else if(duplicateFlag){
        files[0] = {
          "name": "",
          "size": ""
        };
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html(`Dataset with ${duplicateName} name already exists`);
      }
      else {
        $("#fileErrorMsg").addClass("visibilityHidden");
        this.props.dispatch(saveFileToStore(files))
      }
    }else {
      files[0] = {
        "name": "",
        "size": ""
      };
      this.props.dispatch(saveFileToStore(files))
    }
  }

  popupMsg() {
    $("#fileErrorMsg").removeClass("visibilityHidden");
    $("#fileErrorMsg").html("The file format is not supported. Please try again with a csv file.");
  }
  handleSelect(key) {
    this.props.dispatch(updateSelectedDataSrc(key))
  }
  handleInputChange(event) {
    $("#"+event.target.id).css("border-color","#e0e0e0");
  }
  deleteFile(item){
    var deletedFiles= store.getState().dataSource.fileUpload.filter(i=>i!=item);
    if(deletedFiles.length<1){
      deletedFiles[0] = {
        "name": "",
        "size": ""
      };
      this.props.dispatch(saveFileToStore(deletedFiles));
    }
    this.props.dispatch(saveFileToStore(deletedFiles));
  }
  render() {
    const dataSrcList = store.getState().dataSource.dataSourceList.conf;

    if (dataSrcList) {
      const navTabs = dataSrcList.map((data, i) => {
        return (
          <NavItem eventKey={data.dataSourceType} key={i} onSelect={this.handleSelect.bind(this)}>
            {data.dataSourceName}
          </NavItem>
        )
      });
      const navTabContent = dataSrcList.map((data, i) => {
        let fields = data.formFields;
        let formList = null;
        var divId = "data_upload_" + i;
        var dataSrcType = data.dataSourceType
				let msg=<div><label className="pb-2">Select an existing dataset</label>{this.props.renderDatasets}</div>
				if(this.props.renderDatasets == "No Datasets")
				  msg=<div><label>No datasets available.Please upload some data or connect to a database</label></div>
        const fieldsList = fields.map((field, j) => {
          if (field.fieldType == "file") {
            if (this.props.renderDatasets) {
              return (
                <div key={j}>
                  <div class="form-group col-md-12 pt-10">
                    {msg}
                  </div>
                  <div className="clearfix"></div>
                </div>
              );
            } else {
              return (
                <div  key={j} class="tab-pane active cont fade in">
                  <h4 className="lg-mb-30">
                    File Upload
                    {/* <div class="pull-right">
                      <div class="db_images db_file_upload"></div>
                    </div> */}
                  </h4>
                  <div className="clearfix"></div>
                  <div className="dropzone ">
                    <Dropzone id={1} onDrop={this.onDrop.bind(this)} accept=".csv" multiple={true} onDropRejected={this.popupMsg}>
                      <p>Please drag and drop your file here or browse.</p>
                    </Dropzone>
                  </div>
                      <Scrollbars style={{ height: 100 }}>
                        <ul className={this.props.fileUpload[0].name != ""
                          ? "list-unstyled bullets_primary"
                          : "list-unstyled"} style={{marginBottom:0,paddingTop:10}}>
                            {(this.props.fileUpload[0].name!="")&&
                            this.props.fileUpload.map(file=>{
                              return(
                              <li className="xs-p-0">
                                {file.name}
                                <span> - </span> {bytesToSize(file.size)}
                                <span className="xs-ml-15" onClick={this.deleteFile.bind(this, file)}>
                                  <i class="fa fa-times" style={{ color: '#555', cursor: 'pointer' }}></i>
                                </span>  
                              </li>
                              )
                            })
                          }
                          <li className="text-danger visibilityHidden" id="fileErrorMsg">Please select csv file to upload.</li>
                        </ul>
                      </Scrollbars>
                </div>
              )
            }
          } else {
            //to put default port
            let placeHolder = field.placeHolder
            return (
              <div className="form-group" key={j} id={j}>
                <label for="fl1" className="col-sm-3 control-label">{field.labelName}</label>
                <div className="col-sm-9">
                  <input id={dataSrcType + field.fieldName} defaultValue={field.defaultValue} type={field.fieldType} required={field.required} title={"Please Enter " + field.labelName} name={field.fieldName} onChange={this.handleInputChange.bind(this)} placeholder={placeHolder} className="form-control" maxLength={field.maxLength}/>
                </div>
              </div>
            )
          }

        });
        if (data.dataSourceType.toLowerCase() != FILEUPLOAD.toLowerCase()) {
          formList = <div id={divId}>
            <form role="form" className="form-horizontal" id={data.dataSourceType}>{fieldsList}</form>
          </div>
        } else {
          formList = <div id={divId}>{fieldsList}</div>
        }
        return (
          <Tab.Pane key={i} eventKey={data.dataSourceType}>
            {formList}
          </Tab.Pane>
        )
      });
      return (
        <div>
          <Tab.Container id="left-tabs-example" defaultActiveKey="fileUpload">
		        <div className="container-fluid">
              <Row className="clearfix">
                {(window.location.href.includes("autoML"))?
                  ""
                  :
                  <Col sm={3}>
                    <Nav bsStyle="pills" stacked>
                      {navTabs}
                    </Nav>
                  </Col>
                }
                {(window.location.href.includes("autoML"))?
                    <Col sm={12}>
                    <Tab.Content animation>
                      {navTabContent}
                    </Tab.Content>
                  </Col>
                :
                  <Col sm={9}>
                    <Tab.Content animation>
                      {navTabContent}
                    </Tab.Content>
                  </Col>
                }
              </Row>
			      </div>
          </Tab.Container>
        </div>
      )
    }else if(this.props.dataSourceLoaderFlag){
      return(
        <div style={{display:"flex",alignItems:"center",justifyContent: "center"}}>
          <img style={{margin:"5em"}} src={STATIC_URL+"assets/images/Preloader_2.gif"} />
        </div>
      )
    } else {
      return (
        <div>No DataSource</div>
      )
    }
  }
}
