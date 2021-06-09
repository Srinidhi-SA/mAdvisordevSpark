import React from "react";
import Scrollbars from "react-custom-scrollbars/lib/Scrollbars";
import {connect} from "react-redux";
import { STATIC_URL } from "../../helpers/env";
import { CREATEMODEL, CREATESCORE, CREATESIGNAL, isEmpty, MINROWINDATASET, showHideSideChart, showHideSideTable } from "../../helpers/helper";
import store from "../../store";
import { DataValidation } from "./DataValidation";
import { Button } from "react-bootstrap";
import { clearSubset, getAllDataList, getDataList, getDataSetPreview, getValueOfFromParam, hideDataPreview, hideDataPreviewDropDown, makeAllVariablesTrueOrFalse, popupAlertBox, saveSelectedColSlug, selDatetimeCol, selDimensionCol, selMeasureCol, setAlreadyUpdated, setDatetimeColValues, setDimensionColValues, setMeasureColValues } from "../../actions/dataActions";
import { getAppDetails, hideDataPreviewRightPanels, saveSelectedValuesForModel } from "../../actions/appActions";
import { fromVariableSelectionPage, resetSelectedTargetVariable } from "../../actions/signalActions";
import { clearDataPreview, clearLoadingMsg, dataSubsetting } from "../../actions/dataUploadActions";
import { SubSetting } from "./SubSetting";
import { C3ChartNew } from "../C3ChartNew";
import { DataValidationEditValues } from "./DataValidationEditValues";
import { DataUploadLoader } from "../common/DataUploadLoader";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    activeColSlug: store.datasets.activeColSlug,
    subsettingDone: store.datasets.subsettingDone,
    datasets:store.datasets.dataList.data,
    allDataList:store.datasets.allDataSets,
    createSigLoaderFlag : store.datasets.createSigLoaderFlag,
    dataTransformSettings : store.datasets.dataTransformSettings,
    updatedSubSetting: store.datasets.updatedSubSetting,
  };
})

export class DataPreview extends React.Component {
  constructor(props) {
    super(props);
    this.isSubsetted = false;
    this.buttons = {};
    this.chartId = "_side";
    this.firstTimeSideTable = [];
    this.firstTimeSideChart = {};
    this.firstTimeColTypeForChart = null;
  }

  componentWillMount() {
    this.props.dispatch(clearSubset())
    this.props.dispatch(getAllDataList());
    const from = getValueOfFromParam();
    if (from === 'createSignal') {
      if (this.props.match.path.includes("slug")&& this.props.match.path.includes("data")) {
        this.buttons['close'] = {
          url: "/data",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/data/" + this.props.match.params.slug + "/createSignal",
          text: CREATESIGNAL
        };
        this.props.dispatch(fromVariableSelectionPage(true));
      }else if(this.props.match.path.includes("slug")&& this.props.match.path.includes("signals")){
        this.buttons['close'] = {
          url: "/signals",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/signals/" + this.props.match.params.slug + "/createSignal",
          text: CREATESIGNAL
        };
      }
    }else{
      this.props.dispatch(getDataList(1));
      if(this.props.dataPreview == null || isEmpty(this.props.dataPreview) || this.props.dataPreview.status == 'FAILED') {
        this.props.dispatch(getDataSetPreview(this.props.match.params.slug)); //Called on refreshing data preview
      }
      if(this.props.match.path.includes("AppId")) {
        this.props.dispatch(getAppDetails(this.props.match.params.AppId));
      }
      if(this.props.match.path.includes("models") && this.props.match.path.includes("modelSlug") && this.props.match.path.includes("slug")) {
        let modeSelected =  window.location.pathname.includes("analyst")?"/analyst":"/autoML"
        this.buttons['close'] = {
          url: "/apps/"+this.props.match.params.AppId+modeSelected+"/models/"+this.props.match.params.modelSlug,
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/apps/" + this.props.match.params.AppId + modeSelected+ "/models/" + this.props.match.params.modelSlug + "/data/" + this.props.match.params.slug + "/createScore",
          text: CREATESCORE
        };
      }else if(this.props.match.path.includes("models") && this.props.match.path.includes("slug")){
        let modeSelected =  window.location.pathname.includes("analyst")?"/analyst":"/autoML"
        this.buttons['close'] = {
          url: "/apps/"+this.props.match.params.AppId+modeSelected+"/models",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/apps/" + this.props.match.params.AppId + modeSelected+"/models/data/" + this.props.match.params.slug + "/createModel",
          text: CREATEMODEL
        };
      }else if(this.props.match.path.includes("robo")){
        this.buttons['close'] = {
          url: "/apps-robo",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/apps-robo/" + store.getState().apps.roboDatasetSlug + "/" + store.getState().signals.signalAnalysis.slug,
          text: "Compose Insight"
        };
      }else if(this.props.match.path.includes("slug") && !this.props.match.path.includes("signals")){
        this.props.dispatch(resetSelectedTargetVariable());
        this.props.dispatch(fromVariableSelectionPage(false));
        this.buttons['close'] = {
          url: "/data",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/data/" + this.props.match.params.slug + "/createSignal",
          text: CREATESIGNAL
        };
      }else if(this.props.match.path.includes("slug") && this.props.match.path.includes("signals")){
        this.props.dispatch(resetSelectedTargetVariable());
        this.props.dispatch(fromVariableSelectionPage(false));
        this.buttons['close'] = {
          url: "/signals",
          text: "Close"
        };
        this.buttons['create'] = {
          url: "/signals/" + this.props.match.params.slug + "/createSignal",
          text: CREATESIGNAL
        };
      }
    }
  }

  componentDidMount() {
    showHideSideTable(this.firstTimeSideTable);
    showHideSideChart(this.firstTimeColTypeForChart, this.firstTimeSideChart);
  }

  componentWillUpdate() {
    let currentDataset = store.getState().datasets.selectedDataSet
    if(!isEmpty(this.props.dataPreview) && currentDataset != this.props.match.params.slug && this.props.dataPreview != null && this.props.dataPreview.status != 'FAILED'){
      if (!this.props.match.path.includes("robo")) {
        let url=""
        if(this.props.match.path.includes("data"))
          url= '/data/' + currentDataset;
        if(this.props.match.path.includes("signals"))
          url= '/signals/' + currentDataset;
        this.props.history.push(url)
      }
    }
    if(!isEmpty(this.props.dataPreview) && this.props.dataPreview != null && this.props.dataPreview.status == 'FAILED') {
      this.props.dispatch(clearDataPreview())
      this.props.dispatch(clearLoadingMsg())
      let url = '/data/'
      this.props.history.push(url)
    }
    if(this.props.match.path.includes("apps-stock-advisor")){
      hideDataPreviewRightPanels();
    }
  }

  moveToVariableSelection() {
    if(this.props.dataPreview.meta_data.uiMetaData.metaDataUI[0].value < MINROWINDATASET && this.buttons.create.url.indexOf("apps-robo") == -1){
      bootbox.alert("Minimum " + MINROWINDATASET + " rows are required for analysis!!")
    }else if(this.props.dataPreview.meta_data.uiMetaData.varibaleSelectionArray && (this.props.dataPreview.meta_data.uiMetaData.varibaleSelectionArray.length == 0 || (this.props.dataPreview.meta_data.uiMetaData.varibaleSelectionArray.length == 1 && this.props.dataPreview.meta_data.uiMetaData.varibaleSelectionArray[0].dateSuggestionFlag == true))) {
      bootbox.alert("Not enough data to run analysis. Please upload/connect a differenct dataset.")
    }else{
      let url = this.buttons.create.url;
      if(this.buttons.create.url.indexOf("apps-robo") != -1){
        url = "/apps-robo/" + store.getState().apps.roboDatasetSlug + "/" + store.getState().signals.signalAnalysis.slug
        this.props.history.push(url);
      }else{
        this.props.history.push(url);
      }
    }
  }

  applyDataSubset(){
    if(this.props.datasets.length>0){
      this.props.datasets.map(dataset=> dataset.name.toLowerCase()).includes($("#newSubsetName").val().toLowerCase()) ? duplicateName=true:"";     
    }
    if(this.props.allDataList.data!=""){
      for(var i=0;i<this.props.allDataList.data.length;i++){
        if(this.props.allDataList.data[i].name.toLowerCase()==$("#newSubsetName").val().toLowerCase())
          var duplicateName=true
      }
    }
    if(duplicateName){
      bootbox.alert("Same dataset name already exists, Please try changing name!")
    }
    else{
      this.new_subset = $("#newSubsetName").val()
      if(this.new_subset == "" || this.new_subset == null){
        bootbox.alert("Please enter new config name!")
      }else if( (this.new_subset != "" || this.new_subset != null) && this.new_subset.trim()==""){
        bootbox.alert("Please enter valid config name!");
        $("#newSubsetName").val("").focus();
      }else{
        let transformationSettings = {};
        transformationSettings.existingColumns = store.getState().datasets.dataTransformSettings;
        var nonDeletedColumns = 0;
        let dataPrev = this.props.dataPreview.meta_data;
        $.each(dataPrev.uiMetaData.metaDataUI,function(key,val){
          if(val.name == "noOfColumns"){
            nonDeletedColumns = val.value;
            return false;
          }
        });
        if(nonDeletedColumns == 0){
          bootbox.alert("Atleast one column is needed to create a new dataset")
          return;
        }
        let subSettingRq = {
          'filter_settings': store.getState().datasets.updatedSubSetting,
          'name': this.new_subset,
          'subsetting': true,
          'transformation_settings': transformationSettings
        };
        this.props.dispatch(dataSubsetting(subSettingRq,this.props.dataPreview.slug))
        this.props.dispatch(saveSelectedValuesForModel(store.getState().apps.apps_regression_modelName, "", ""))
        this.props.dispatch(makeAllVariablesTrueOrFalse(true));
        this.props.dispatch(resetSelectedTargetVariable())
      }
    }
  }

  closePreview() {
    const url = this.buttons.close.url;
    this.props.dispatch(hideDataPreview());
    this.props.history.push(url);
  }

  setSelectedColSlug(slug){
    if(this.props.activeColSlug != slug){
      if(this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i=>i.slug===slug)[0].columnType === "datetime"){
        $("#tab_visualizations")[0].style.display = "none"
      }else{
        $("#tab_visualizations")[0].style.display = ""
        $(".chart").empty();
        $(".visualizeLoader")[0].style.display = ""
      }
      this.props.dispatch(saveSelectedColSlug(slug));
      this.props.dispatch(setAlreadyUpdated(false));
      let colData = this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i=>i.slug===slug)[0];
    if(colData.columnType === "measure"){
      colData.columnStats.map((stats) => {
        if(stats.name == "min"){
          this.props.dispatch(setMeasureColValues("min",stats.value));
          this.props.dispatch(setMeasureColValues("curMin",stats.value));
        }else if(stats.name == "max"){
          this.props.dispatch(setMeasureColValues("max",stats.value));
          this.props.dispatch(setMeasureColValues("curMax",stats.value));
        }
      });
      this.props.dispatch(setMeasureColValues("textboxUpdated",false));
      if(this.props.updatedSubSetting.measureColumnFilters.length>0 && this.props.updatedSubSetting.measureColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selMeasureCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }else if(colData.columnType === "dimension"){
      colData.columnStats.map((stats) => {
        if(stats.name == "LevelCount"){
          this.props.dispatch(setDimensionColValues("dimensionList",stats.value))
          this.props.dispatch(setDimensionColValues("curDimensionList",Object.keys(stats.value)))
          this.props.dispatch(setDimensionColValues("selectedDimensionList",Object.keys(stats.value)))
        }
      });
      if(this.props.updatedSubSetting.dimensionColumnFilters.length>0 && this.props.updatedSubSetting.dimensionColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selDimensionCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }else if(colData.columnType === "datetime"){
      colData.columnStats.map((stats) => {
        if(stats.name === "firstDate"){
          this.props.dispatch(setDatetimeColValues("startDate",stats.value));
          this.props.dispatch(setDatetimeColValues("curstartDate",stats.value));
        }else if(stats.name == "lastDate"){
          this.props.dispatch(setDatetimeColValues("endDate",stats.value));
          this.props.dispatch(setDatetimeColValues("curendDate",stats.value)); 
        }
      });
      if(this.props.updatedSubSetting.timeDimensionColumnFilters.length>0 && this.props.updatedSubSetting.timeDimensionColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selDatetimeCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }
    }
  }

  render() {
    let dataPrev = this.props.dataPreview;
    let isDataValidationAllowed = false;
    let isSubsettingAllowed = false;
    let isCreateAllowed = false;
    this.isSubsetted = this.props.subsettingDone;

    if(dataPrev && !isEmpty(dataPrev) && dataPrev.status!="FAILED"){
      dataPrev = this.props.dataPreview.meta_data;
      let permission_details = this.props.dataPreview.permission_details;
      isDataValidationAllowed = permission_details.data_validation;
      isSubsettingAllowed = permission_details.subsetting_dataset;
      
      if(this.buttons.create.text == CREATESIGNAL){
        isCreateAllowed = permission_details.create_signal;
      }else if(this.buttons.create.text == CREATEMODEL) {
        isCreateAllowed = permission_details.create_trainer;
      }else if(this.buttons.create.text == CREATESCORE || "Create Score"){
        isCreateAllowed = permission_details.create_score;
        isDataValidationAllowed = false;
      }else if(this.buttons.create.text == "Compose Insight") {
        isCreateAllowed = true
      }

      if(this.props.createSigLoaderFlag){
        return(
          <div>
            <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
            <div className="text-center text-muted">
              <h3>Please wait while loading...</h3>
            </div>
          </div>
        );
      }else if(dataPrev==="" || isEmpty(dataPrev.uiMetaData)){
        return(
        <div className="side-body">
          <div className="page-head">
            <div className="row">
              <div className="col-md-8">
                <h3 style={{"display": "inline"}}> Data Preview </h3>
                <h4 style={{"display": "inline"}}>{this.props.dataPreview.name!=""?`(${this.props.dataPreview.name.replace(".csv","")})`:""}</h4>
              </div>
            </div>
          </div>
          <div className="main-content">No Data Preview available</div>
        </div> 
        );
      }else{
        const topInfo = dataPrev.uiMetaData.metaDataUI.map((item,i)=>{
          if(item.display && item.name!="companyNames" && item.name!="timeline"){
            return(
              <div key={i} className="col-md-5ths col-xs-6 data_preview xs-mb-15">
                <div className="bgStockBox" style={{height:this.props.match.path.includes("apps-stock-advisor")?"60px":""}} >
                  <div className="row" style={{paddingTop:this.props.match.path.includes("apps-stock-advisor")?"5px":""}} >
                    <div className="col-xs-8 xs-pr-0">
                      <h4 className="xs-pt-5 xs-pb-5">
                        {item.displayName}
                      </h4>
                    </div>
                    <div className="col-xs-4 xs-pl-0 text-right">
                      <h4 className="xs-pt-5 xs-pb-5 text-info">
                        {item.value}
                      </h4>
                    </div>
                    <div class="clearfix"></div>
                  </div>
                </div>
              </div>
            );
          }
        });
        let stockInfo = ""
        if(this.props.match.path.includes("apps-stock-advisor") || this.props.match.path.includes("apps-stock-advisor-analyze")){
          stockInfo = dataPrev.uiMetaData.metaDataUI.map((item,i)=>{
            if(item.display && (item.name==="companyNames"||item.name==="timeline")){
              return(
                <div key={i} className="stockTopInfo">
                  <div className="col-md-4">{item.displayName}</div>
                  <div className="col-md-8 text-right text-info">
                    <Scrollbars height="50px">
                      <div style={{paddingRight:"10px"}} >
                        {(item.name==="companyNames")?item.value.join(", "):item.value}
                      </div>
                    </Scrollbars>
                  </div>
                </div>
              )}
          })
        }
        const tableThTemplate = dataPrev.uiMetaData.columnDataUI.map((thElement,thIndex)=>{
          let cls = thElement.slug + " dropdown";
          if(this.props.dataTransformSettings.length!=0){
            cls = this.props.dataTransformSettings.filter((i=>i.slug===thElement.slug))[0]
            .columnSetting.filter(i=>i.actionName==="delete")[0].status?
            cls+" dataPreviewUpdateCol":cls
          }

          let iconCls = null;
          let dataValidationCom = "";
          const anchorCls = thElement.slug + " dropdown-toggle cursor";
          switch(thElement.columnType){
            case "measure":
              iconCls = "mAd_icons ic_mes_s";
              break;
            case "dimension":
              iconCls = "mAd_icons ic_dime_s";
              break;
            case "datetime":
              iconCls = "timeDimIcon fa fa-clock-o";
              break;
          }
          if(isDataValidationAllowed){
            dataValidationCom = <DataValidation name={thElement.name} slug={thElement.slug} />
          }
          if(!thElement.consider){
            return(
              <th key={thIndex} className={cls} title={thElement.ignoreSuggestionMsg} onClick={this.setSelectedColSlug.bind(this,thElement.slug)}>
                <a href="#" data-toggle="dropdown" className={anchorCls}>
                  <i className={iconCls}></i>
                  <span>{thElement.name}</span>{this.props.match.url.indexOf('/apps-stock-advisor/')<0?<b className="caret"></b>:""}
                </a>
                {this.props.match.url.indexOf('/apps-stock-advisor/')<0?dataValidationCom:""}
              </th>
            );
          }else{
            return(
              <th key={thIndex} className={cls} onClick={this.setSelectedColSlug.bind(this,thElement.slug)}>
                <a href="#" data-toggle="dropdown" id={thElement.slug} className={anchorCls} title={thElement.name}>
                  <i className={iconCls}></i>
                  <span>{thElement.name}</span>
                  {this.props.match.url.indexOf('/apps-stock-advisor/')<0?<b className="caret"></b>:""}
                </a>
                {dataValidationCom}
              </th>
            );
          }

        })
        const tableRowsTemplate = dataPrev.uiMetaData.sampleDataUI.map((trElement,trIndex)=>{
          const tds = trElement.map((tdElement, tdIndex)=>{

            let clsName  = ((this.props.activeColSlug==="" && tdIndex===0) || 
            (this.props.activeColSlug === dataPrev.uiMetaData.columnDataUI[tdIndex].slug) )?
            dataPrev.uiMetaData.columnDataUI[tdIndex].slug+" activeColumn":dataPrev.uiMetaData.columnDataUI[tdIndex].slug
            
            if(this.props.dataTransformSettings.length!=0){
            clsName = this.props.dataTransformSettings.filter((i=>i.slug===dataPrev.uiMetaData.columnDataUI[tdIndex].slug))[0]
              .columnSetting.filter(i=>i.actionName==="delete")[0].status?
              clsName+" dataPreviewUpdateCol":clsName
            }

            if(!dataPrev.uiMetaData.columnDataUI[tdIndex].consider){
              if(dataPrev.uiMetaData.columnDataUI[tdIndex].ignoreSuggestionPreviewFlag){
                let cls = clsName + " greyout-col";
                return(
                  <td key={tdIndex} className={cls} title={tdElement} onClick={this.setSelectedColSlug.bind(this,dataPrev.uiMetaData.columnDataUI[tdIndex].slug)}>{tdElement}</td>
                );
              }else{
                return(
                  <td key={tdIndex} className={clsName} title={tdElement} onClick={this.setSelectedColSlug.bind(this,dataPrev.uiMetaData.columnDataUI[tdIndex].slug)}>{tdElement}</td>
                );
              }
            }else{
              return(
                <td key={tdIndex} className={clsName} title={tdElement} onClick={this.setSelectedColSlug.bind(this,dataPrev.uiMetaData.columnDataUI[tdIndex].slug)}>{tdElement}</td>
              );
            }
          });
          return(
            <tr key={trIndex}>
              {tds}
            </tr>
          );
        });
        
        let sideTableTemplate = ""
        let firstTimeSubSetting = ""
        let firstChart = ""

        if(dataPrev.scriptMetaData.columnData[0].chartData != null){
          if(!isEmpty(dataPrev.scriptMetaData.columnData[0])){
            let tabData = (this.props.activeColSlug==="")? dataPrev.scriptMetaData.columnData[0]: dataPrev.scriptMetaData.columnData.filter(i=>i.slug===this.props.activeColSlug)[0]
            const sideTable = tabData.columnStats;
            this.firstTimeSideTable = sideTable;
            firstTimeSubSetting = tabData
            sideTableTemplate = sideTable.map((tableItem,tableIndex)=>{
              if(tableItem.display){
                return(<tr key={tableIndex}>
                        <td className="item">{tableItem.displayName}</td>
                        <td>&nbsp;:&nbsp;</td>
                        <td><span title={tableItem.value} className="stat-txtControl">{tableItem.value}</span></td>
                      </tr>)
              }
            })
          }

          let colDat = (this.props.activeColSlug==="")? dataPrev.scriptMetaData.columnData[0]: dataPrev.scriptMetaData.columnData.filter(i=>i.slug===this.props.activeColSlug)[0]
          const sideChart = colDat.chartData.chart_c3
          this.firstTimeSideChart = colDat.chartData;
          this.firstTimeColTypeForChart = colDat.columnType;
          if(!$.isEmptyObject(this.firstTimeSideChart)){
            let chartInfo = [];
            firstChart = <C3ChartNew chartInfo={chartInfo} classId={this.chartId} data={sideChart} yformat={colDat.chartData.yformat} xdata={colDat.chartData.xdata} sideChart={true} />;
          }
        }
        
        return (
          <div className="side-body">
            <div className="page-head">
              <div className="row">
                <div className="col-md-8">
                  <h3 style={{"display": "inline"}}> Data Preview </h3>
                  <h4 style={{"display": "inline"}}>{this.props.dataPreview.name!=""?`(${this.props.dataPreview.name.replace(".csv","")})`:""}</h4>
                </div>
              </div>
              <div className="clearfix"></div>
            </div>
            <div className="main-content">
              <div className="row d_preview">{topInfo}</div>
                {(this.props.match.path.includes("apps-stock-advisor") || this.props.match.path.includes("apps-stock-advisor-analyze"))?<div className="col-md-5 stockInfo">{stockInfo}</div>:"" }
                <div className="row">
                  <div className="col-md-9 preview_content">
                    <div className="clearfix"></div>
                    <div className="table-responsive noSwipe xs-pb-10">
                      <Scrollbars style={{height:855}}>
                        <table className="table table-condensed table-hover table-bordered table-striped cst_table">
                          <thead>
                            <tr>{tableThTemplate}</tr>
                          </thead>
                          <tbody className="no-border-x">
                            {tableRowsTemplate}
                          </tbody>
                        </table>
                      </Scrollbars>
                    </div>
                  </div>
                  <div className="col-md-3 preview_stats">
                    <div id="tab_statistics" className="panel-group accordion accordion-semi box-shadow">
                      <div className="panel panel-default">
                        <div className="panel-heading">
                          <h4 className="panel-title">
                            <a data-toggle="collapse" data-parent="#tab_statistics" href="#pnl_stc" aria-expanded="true" className="">Statistics
                              <i className="fa fa-angle-down pull-right"></i>
                            </a>
                          </h4>
                        </div>
                        <div id="pnl_stc" className="panel-collapse collapse in" aria-expanded="true">
                          <div className="xs-pt-10 xs-pr-5 xs-pb-5 xs-pl-5">
                            <table className="no-border no-strip skills" cellPadding="3" cellSpacing="0" id="side-table">
                              <tbody className="no-border-x no-border-y">
                                {sideTableTemplate}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div id="tab_visualizations" className="panel-group accordion accordion-semi box-shadow">
                      <div className="panel panel-default">
                        <div className="panel-heading">
                          <h4 className="panel-title">
                            <a data-toggle="collapse" data-parent="#tab_visualizations" href="#pnl_visl" aria-expanded="true" className="">Visualization
                              <i className="fa fa-angle-down pull-right"></i>
                            </a>
                          </h4>
                        </div>
                        <div id="pnl_visl" className="panel-collapse collapse in" aria-expanded="true">
                          <div className="xs-pt-5 xs-pr-5 xs-pb-5 xs-pl-5">
                            <div className="visualize_body">
                              <div className="visualizeLoader" style={{display:"none"}}>
                                <img id="chartLoader" src={STATIC_URL+"assets/images/loaderChart.gif"}/>
                              </div>
                              <div id="side-chart" style={{paddingTop: "12px"}}>
                                {firstChart}
                                <div className="clearfix"></div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    {isSubsettingAllowed &&
                      <div id="sub_settings" className="box-shadow">
                        <SubSetting item={firstTimeSubSetting}/>
                      </div>
                    }
                  </div>
                  <div className="clearfix"></div>
                </div>
                <div className="row buttonRow" id="dataPreviewButton">
                  <div className="col-md-12">
                    <div className="panel xs-md-0">
                      <div className="panel-body box-shadow">
                        <div className="navbar">
                          <ul className="nav navbar-nav navbar-right">
                            <li>
                              {this.isSubsetted && !this.props.location.pathname.includes("/models/data") &&
                              <div className="form-group">
                                <input type="text" name="newSubsetName" id="newSubsetName" className="form-control input-sm col-sm-12" placeholder="New Dataset Name"/>
                              </div>}
                            </li>
                            <li className="text-right">
                              <Button id="dpClose" onClick={this.closePreview.bind(this)}>{this.buttons.close.text}</Button>
                              {(this.isSubsetted && !this.props.location.pathname.includes("/models/data"))?
                                (<Button bsStyle="primary" onClick={this.applyDataSubset.bind(this)} >Save Config</Button>):
                                (<Button id="dataPreviewCreateModel" onClick={this.moveToVariableSelection.bind(this)} disabled={!isCreateAllowed} bsStyle="primary">{this.buttons.create.text}</Button>)
                              }
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            <DataValidationEditValues/>
            <DataUploadLoader/>
          </div>
        );
      }
    }else{
      return(
        <div className="side-body">
          <div className="page-head"></div>
          <img id="loading" src={STATIC_URL+"assets/images/Preloader_2.gif"} />
        </div>
      )
    }
  }
}
