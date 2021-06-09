import React from "react";
import { Scrollbars } from 'react-custom-scrollbars';
import { connect } from "react-redux";
import store from "../../store"
import { InputSwitch } from 'primereact/inputswitch';
import { getDataSetPreview, getValueOfFromParam } from "../../actions/dataActions";
import { Button } from "react-bootstrap";
import { getRemovedVariableNames } from "../../helpers/helper.js"
import { isEmpty } from "../../helpers/helper";
import {
  missingValueTreatmentSelectedAction,
  outlierRemovalSelectedAction,
  variableSelectedAction,
  checkedAllAction,
  dataCleansingCheckUpdate,
  removeDuplicateObservationsAction,
  dataCleansingDataTypeChange,
  searchTable,
  sortTable
} from "../../actions/dataCleansingActions";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    apps_regression_modelName: store.apps.apps_regression_modelName,
    currentAppDetails: store.apps.currentAppDetails,
    datasets: store.datasets,
    checkedAll: store.datasets.checkedAll,
    editmodelFlag:store.datasets.editmodelFlag,
    modelEditconfig:store.datasets.modelEditconfig,
    selectedVariables:store.datasets.selectedVariables
  };
})

export class DataCleansing extends React.Component {
  constructor(props) {
    super(props);
    this.buttons = {};
    this.state = {
      value1: false,
      value2: false,
      checked: true,
    };
  }

  componentWillMount() {
    const from = getValueOfFromParam();
    if (from === 'feature_Engineering') {
      if (this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null) {
        let mod =  window.location.pathname.includes("analyst")?"analyst":"autoML"
        this.props.history.replace("/apps/"+this.props.match.params.AppId+"/"+mod+"/models/data/"+this.props.match.params.slug)
      }
    }else if (this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null) {
      let mod =  window.location.pathname.includes("analyst")?"analyst":"autoML"
      this.props.history.replace("/apps/"+this.props.match.params.AppId+"/"+mod+"/models/data/"+this.props.match.params.slug)
    }else{
      if(this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null) {
        window.history.go(-1);
      }
      if(this.props.dataPreview == null || isEmpty(this.props.dataPreview) || this.props.dataPreview.status == 'FAILED') {
        this.props.dispatch(getDataSetPreview(this.props.match.params.slug));
      }else{

      }
      var proccedUrl = this.props.match.url.replace('dataCleansing', 'featureEngineering');
      if (this.props.match.path.includes("slug")) {
        this.buttons['proceed'] = {
          url: proccedUrl,
          text: "Proceed"
        };
      }
      var removedVariables = getRemovedVariableNames(this.props.datasets);
      var considerItems = this.props.datasets.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i => ((i.consider === false) && (i.ignoreSuggestionFlag === false)) || ((i.consider === false) && (i.ignoreSuggestionFlag === true) && (i.ignoreSuggestionPreviewFlag === true))).map(j => j.name);
        this.props.dataPreview.meta_data.scriptMetaData.columnData.map(item => {
        if(removedVariables.indexOf(item.name) != -1 || considerItems.indexOf(item.name) != -1)
          return "";
        this.props.dispatch(variableSelectedAction(item.name, item.slug, true));
        });
      if(this.props.editmodelFlag){
        this.setOutliersOnEdit()
        this.setMissingValuesOnEdit()
      }
    }
  }

  setOutliersOnEdit(){
    var outliers=Object.values(this.props.modelEditconfig.outlier_config)
    for(var i=0;i<outliers.length;i++){
      this.props.dispatch(outlierRemovalSelectedAction(outliers[i].name,outliers[i].type,this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(j=>j.name==outliers[i].name)[0].slug,outliers[i].treatment))
    }
  }

  setMissingValuesOnEdit(){
    var missingValues =Object.values(this.props.modelEditconfig.missing_value_config)
    for(var i=0;i<missingValues.length;i++){
      this.props.dispatch(missingValueTreatmentSelectedAction(missingValues[i].name,missingValues[i].type,this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(j=>j.name==missingValues[i].name)[0].slug,missingValues[i].treatment)
      )
    }
  }

  componentDidUpdate(){
    var selectElements = document.getElementsByTagName("select");
    var i,j;
    for (i = 1; i < selectElements.length; i++) {
      for(j=0;j<selectElements[i].options.length;j++){
        if(selectElements[i].options.length>=4){
          if( selectElements[i].selectedOptions[0].value==selectElements[i].options[j].value)
            selectElements[i].options[j].style.display = 'none';
          else
            selectElements[i].options[j].style.display = 'inline';
        }
      }
    }
  }

  componentDidMount() {
    var selectElements = document.getElementsByTagName("select");
    var i,j;
    for (i = 0; i < selectElements.length; i++) {
      for(j=0;j<selectElements[i].options.length;j++){
        if(selectElements[i].options[j].selected)
          selectElements[i].options[j].style.display = 'none';
        else
          selectElements[i].options[j].style.display = 'inline';
      }
    }
  }

  sortTable(n) {
    sortTable(n,"dctable");
  }

  searchTable() {
    searchTable("dctable",1,8);
  }
  
  shouldComponentUpdate(nextProps) {
    return true;
  }

  missingValueTreatmentOnChange(colSlug,event) {
    this.props.dispatch(missingValueTreatmentSelectedAction(event.target.dataset["colname"], event.target.dataset["coltype"], event.target.dataset["colslug"], event.target.value));
    this.handleDropdownOptions(colSlug, event,'missingValue')
  }

  outlierRemovalOnChange(colSlug,event) {
    this.props.dispatch(outlierRemovalSelectedAction(event.target.dataset["colname"], event.target.dataset["coltype"], event.target.dataset["colslug"], event.target.value));
    this.handleDropdownOptions(colSlug, event,'outlier')
  }

  variableCheckboxOnChange(event) {
    const checkBoxIndex = event.target.dataset["index"];
    this.props.dispatch(dataCleansingCheckUpdate(checkBoxIndex, event.target.checked));
    this.props.dispatch(variableSelectedAction(event.target.dataset["colname"], event.target.dataset["colslug"], event.target.checked));
    if (Object.values(this.props.datasets.selectedVariables).includes(false)) {
      this.props.dispatch(checkedAllAction(false));
    }else{
      this.props.dispatch(checkedAllAction(true));
    }
  }

  checkedAllOnChange(event) {
    this.props.dispatch(checkedAllAction(event.target.checked));
    var removedVariables = getRemovedVariableNames(this.props.datasets);
    var considerItems = this.props.datasets.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i => ((i.consider === false) && (i.ignoreSuggestionFlag === false)) || ((i.consider === false) && (i.ignoreSuggestionFlag === true) && (i.ignoreSuggestionPreviewFlag === true))).map(j => j.name);

    if (!event.target.checked) {
      this.props.dataPreview.meta_data.scriptMetaData.columnData.map(item => {
        if (removedVariables.indexOf(item.name) != -1 || considerItems.indexOf(item.name) != -1)
          return "";
        this.props.dispatch(variableSelectedAction(item.name, item.slug, false));
      });
    } else {
      this.props.dataPreview.meta_data.scriptMetaData.columnData.map(item => {
        if (removedVariables.indexOf(item.name) != -1 || considerItems.indexOf(item.name) != -1)
          return "";
        this.props.dispatch(variableSelectedAction(item.name, item.slug, true));
      });
    }
  }

  handleDuplicateObservationsOnChange(event) {
    this.setState({ value2: event.target.value })
    this.props.dispatch(removeDuplicateObservationsAction(event.target.name, event.target.value));
  }

  handlefilterOptions(e){
    var select = document.getElementById('sdataType');
    for(var i=0;i<select.options.length;i++){
      if(select.options[i].value==e.target.value)
        select.options[i].style.display='none'
      else
        select.options[i].style.display='inline'
    }
    var tds = document.getElementsByTagName("tr");
    let count = 0;
    for(var i = 1; i<tds.length; i++) {
      if(tds[i].className.includes(e.target.value)) {
        tds[i].style.display = ""
      }else{
        tds[i].style.display = "none"
        count++
      }
    }
  }

  handleDropdownOptions(colSlug,event,type){
    var select
    if(type=='dataType')
     select = document.getElementById(`${colSlug}dataType`);
    else if(type=='missingValue')
     select = document.getElementById(`${colSlug}missingValue`);
    else if(type=='outlier')
     select = document.getElementById(`${colSlug}outlier`);

    var selectedOption = event.target.value
    for(var i=0;i<select.options.length;i++){
      if(select.options[i].value==selectedOption)
        select.options[i].style.display='none'
      else
        select.options[i].style.display='inline'
    }
  }
  
  handleDataTypeChange(colSlug, event) {
    this.props.dispatch(dataCleansingDataTypeChange(colSlug, event.target.value));
    this.handleDropdownOptions(colSlug, event,'dataType')
  }

  getUpdatedDataType(colSlug) {
    var colType = ""
    if(!this.props.editmodelFlag)
      colType = this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(item => item.slug == colSlug)[0].columnType
    else
      colType = this.props.dataPreview.meta_data.uiMetaData.varibaleSelectionArray.filter(item=>item.slug == colSlug)[0].columnType
    var arr = ["Measure", "Dimension", "Datetime"]
    var selectedOption = arr.filter((i)=>i.toLowerCase() == colType.toLowerCase())[0]
    var optionsHtml = arr.map((item ,index)=> {
      return <option key={index} value={item.toLowerCase()} > {item}</option>
    })
    return <select className="form-control" defaultValue={selectedOption.toLowerCase()} id={colSlug+'dataType'} onChange={this.handleDataTypeChange.bind(this, colSlug)} >{colType}{optionsHtml}</select>
  }

  getOutlierRemovalOptions(dataType, colName, colSlug,outnum,missingnum) {
    let disble = (outnum===0)?true:false;
    var data_cleansing = this.props.dataPreview.meta_data.uiMetaData.fe_config.data_cleansing;
    if (dataType in data_cleansing && "outlier_removal" in data_cleansing[dataType] && !disble) {
      var dcHTML = (data_cleansing[dataType].outlier_removal.operations.map((item,index)=><option key={index} value={item.name} >{item.displayName}</option>))
      var selectedValue = "none";
      if (colSlug in this.props.datasets.outlierRemoval) {
        selectedValue = this.props.datasets.outlierRemoval[colSlug].treatment
      }
      return (
        <select className="form-control"  id={colSlug+'outlier'} data-coltype={dataType} data-colName={colName} data-colslug={colSlug} onChange={this.outlierRemovalOnChange.bind(this,colSlug)} value={selectedValue} >{dcHTML}</select>
      );
    }
    else return ""
  }

  proceedFeatureEngineering() {
    var proccedUrl = this.props.match.url.replace('dataCleansing', 'featureEngineering');
    this.props.history.push(proccedUrl);
  }

  handleBack=()=>{
    this.props.history.replace(`/apps/${this.props.match.params.AppId}/analyst/models/data/${this.props.match.params.slug}/createModel?from=data_cleansing`);
  }

  getMissingValueTreatmentOptions(dataType, colName, colSlug,outnum,missingnum) {
    let disble = (parseInt(missingnum)===0)?true:false
    var data_cleansing = this.props.dataPreview.meta_data.uiMetaData.fe_config.data_cleansing;
    if (dataType in data_cleansing && "missing_value_treatment" in data_cleansing[dataType] && !disble) {
      var dcHTML = (data_cleansing[dataType].missing_value_treatment.operations.map((item,index) => <option key={index} value={item.name} >{item.displayName}</option>))
      var selectedValue = "none";
      if (colSlug in this.props.datasets.missingValueTreatment) {
        selectedValue = this.props.datasets.missingValueTreatment[colSlug].treatment
      }
      return (
       <select className="form-control" data-coltype={dataType} id={colSlug+'missingValue'} data-colslug={colSlug} data-colname={colName} onChange={this.missingValueTreatmentOnChange.bind(this,colSlug)} value={selectedValue}>{dcHTML}</select>
      );
    }
    else { return ""; }
  }

  render() {
    var cleansingHtml = <span>"Loading..."</span>;
    if (this.props.dataPreview != null) {
      var removedVariables = getRemovedVariableNames(this.props.datasets);
      var considerItems = this.props.datasets.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i => ((i.consider === false) && (i.ignoreSuggestionFlag === false)) || ((i.consider === false) && (i.ignoreSuggestionFlag === true) && (i.ignoreSuggestionPreviewFlag === true))).map(j => j.name);
      var removedVariables = getRemovedVariableNames(this.props.datasets);
      cleansingHtml = this.props.dataPreview.meta_data.scriptMetaData.columnData.map((item, index) => {
        let outnum = 1;
        let missingnum = 1;
        if (removedVariables.indexOf(item.name) != -1 || considerItems.indexOf(item.name) != -1)
          return null;
        else {
          return (
            <tr className={('all ' + item.columnType)} key={index} id="mssg">
              <td class="filter-false sorter-false">
                <div class="ma-checkbox inline">
                  <input key={Math.random()} id={item.slug} type="checkbox" className="needsclick variableToBeSelected" value={item.name} defaultChecked={(this.props.selectedVariables[item.slug])?true:false} data-index={index} data-colname={item.name} data-colslug={item.slug} onChange={this.variableCheckboxOnChange.bind(this)}/>
                  <label for={item.slug}></label>
                </div>
              </td>
              <td className="text-left">{item.name}</td>
              <td>{this.getUpdatedDataType(item.slug)}</td>
              <td>
                {item.columnStats.filter(function (items) {
                  return items.name == "numberOfUniqueValues"
                }).map((option, index) => {
                  return (<span key={index}>{option.value}</span>);
                }
                )}
              </td>
              <td>
                {item.columnStats.filter(function (items) {
                  return items.name == "numberOfNulls"
                }).map((option, index) => {
                  missingnum = option.value;
                  return (<span key={index}>{option.value}</span>);
                }
                )}
              </td>
              <td>
                {item.columnStats.filter(function (items) {
                  return items.name == "Outliers"
                }).map((option,index) => {
                  outnum = option.value;
                  return (<span key={index}>{option.value}</span>);
                }
                )}
              </td>
              <td>{this.getMissingValueTreatmentOptions(item.columnType, item.name, item.slug,outnum,missingnum)}</td>
              <td>{this.getOutlierRemovalOptions(item.columnType, item.name, item.slug,outnum,missingnum)}</td>
            </tr>
          );
        }
      })
    }

    return (
      <div className="side-body">
        <div className="page-head">
          <h3 className="xs-mt-0 xs-mb-0 text-capitalize"> Data Cleansing</h3>
        </div>
        <div className="main-content">
          <div class="row">
            <div class="col-md-12">
              <div class="panel box-shadow xs-m-0">
                <div class="panel-body no-border xs-p-20">
                  <div class="clearfix xs-mb-5"></div>
                  <div class="form-group">
                    <label for="rd2" class="col-sm-5 control-label"><i class="fa fa-angle-double-right"></i> Do you want to remove duplicate rows/observations  in the dataset?</label>
                    <div class="col-sm-7">
                      <div className="content-section implementation">
                        <InputSwitch id="rd2" checked={store.getState().datasets.duplicateObservations} name="remove_duplicate_observations" onChange={this.handleDuplicateObservationsOnChange.bind(this)} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="panel box-shadow ">
                <div class="panel-body no-border xs-p-20">
                  <div class="row xs-mb-10">
                    <div className="col-md-6">
                      <div class="form-inline" >
                        <div class="form-group">
                          <label for="sdataType">Filter Data Type: </label>
                          <select id="sdataType" onChange={this.handlefilterOptions.bind(this)}className="form-control cst-width">
                            <option value="all">All</option>
                            <option value="measure">Measure</option>
                            <option value="dimension">Dimension</option>
                            <option value="datetime">Datetime</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-inline" >
                        <div class="form-group pull-right">
                          <input type="text" id="search" className="form-control" placeholder="Search variables..." onKeyUp={this.searchTable.bind(this)}></input>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="table-responsive noSwipe xs-pb-10">
                    <Scrollbars style={{ height: 500 }}>
                      <table id="dctable" className="tablesorter table table-condensed table-hover table-bordered">
                        <thead>
                          <tr className="myHead">
                            <th className="hideSortImg">
                              <div class="ma-checkbox inline">
                                <input id="myCheckAll" type="checkbox" className="needsclick" checked={this.props.checkedAll} onChange={this.checkedAllOnChange.bind(this)} />
                                <label for="myCheckAll"></label>
                              </div>
                            </th>
                            <th onClick={this.sortTable.bind(this,1)}><b>Variable name</b></th>
                            <th onClick={this.sortTable.bind(this,2)}><b>Data type</b></th>
                            <th onClick={this.sortTable.bind(this,3)}><b>No of unique values</b></th>
                            <th onClick={this.sortTable.bind(this,4)}><b>No of missing values</b></th>
                            <th onClick={this.sortTable.bind(this,5)}><b>No of outliers</b></th>
                            <th className="hideSortImg"><b>Missing value treatment</b></th>
                            <th className="hideSortImg"><b>Outlier removal</b></th>
                          </tr>
                        </thead>
                        <tbody className="no-border-x">
                          {cleansingHtml}
                        </tbody>
                      </table>
                    </Scrollbars>
                  </div>
                </div>
                <div className="panel-body box-shadow">
                <div class="buttonRow">
                  <Button id="dataCleanBack" onClick={this.handleBack} bsStyle="primary"><i class="fa fa-angle-double-left"></i> Back</Button>
                  <Button id="dataCleanProceed" onClick={this.proceedFeatureEngineering.bind(this)} bsStyle="primary" style={{float:"right"}}>Proceed <i class="fa fa-angle-double-right"></i></Button>
                </div>
                  <div class="xs-p-10"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
