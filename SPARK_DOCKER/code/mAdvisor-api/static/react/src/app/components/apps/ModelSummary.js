import React from "react";
import {connect} from "react-redux";
import store from "../../store"
import {getDeploymentList} from "../../actions/appActions";
var dateFormat = require('dateformat');
import {STATIC_URL} from "../../helpers/env.js"
import {openDeployModalAction, closeDeployModalAction} from "../../actions/modelManagementActions"
import {isEmpty,getUserDetailsOrRestart} from "../../helpers/helper";
import {getAlgoAnalysis} from "../../actions/signalActions";
import {CardHtml} from "../../components/signals/CardHtml";
import {CardTable} from "../common/CardTable";
import {DataBox} from "../common/DataBox";
import $ from "jquery";
import { Deployment } from "./Deployment";
import { ModelSummeryButton } from "../common/ModelSummeryButton";
import { C3ChartNew } from "../C3ChartNew";
import { Scrollbars } from "react-custom-scrollbars";

@connect((store) => {
  return {
    login_response: store.login.login_response,
  algoList: store.apps.algoList,
    currentAppId: store.apps.currentAppId,
  algoAnalysis:store.signals.algoAnalysis,
  dataPreview: store.datasets.dataPreview,
  currentAppDetails:store.apps.currentAppDetails,
  deploymentList:store.apps.deploymentList
  };
})

export class ModelSummary extends React.Component {
  constructor(props) {
  super(props);
  }
  
  componentWillMount() {
  this.props.dispatch(getAlgoAnalysis(getUserDetailsOrRestart.get().userToken, this.props.match.params.slug));
  this.props.dispatch(getDeploymentList(this.props.match.params.slug));
  setInterval(function() {
    var evt = document.createEvent('UIEvents');
    evt.initUIEvent('resize', true, false,window,0);
    window.dispatchEvent(evt);
  }, 500);
  }

  closeModelSummary(){
  window.history.back();
  }
  
  calculateWidth(width){
  let colWidth  = parseInt((width/100)*12);
  let divClass="col-md-"+colWidth;
  return divClass;
  }
  
  renderCardData(c3,cardWidth){
  var htmlData = c3.map((story, i) => {
    let randomNum = Math.random().toString(36).substr(2,8);
    switch (story.dataType) {
      case "html":
            if(!story.hasOwnProperty("classTag"))story.classTag ="none";
            return (<CardHtml key={randomNum} htmlElement={story.data} type={story.dataType} classTag={story.classTag}/>);
            break;
      case "c3Chart":
            let chartInfo=[]
            if(!$.isEmptyObject(story.data)){
            if(story.chartInfo){
              chartInfo=story.chartInfo
            }
            if(story.widthPercent &&  story.widthPercent != 100){
              let width  = parseInt((story.widthPercent/100)*12)
              let divClass="col-md-"+width;
              let sideChart=false;
              if(story.widthPercent < 50)sideChart=true;
              return (<div key={randomNum} class={divClass} style={{display:"inline-block",paddingLeft:"30px"}}><C3ChartNew chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div>);
            }else if(story.widthPercent == 100){
              let divClass="";
              let parentDivClass = "col-md-12";
              if(!cardWidth || cardWidth > 50)
              divClass = "col-md-12"
              else
              divClass = "col-md-12";
              let sideChart=false;
              return (<div key={randomNum} className={parentDivClass}><div class={divClass} style={{display:"inline-block",paddingLeft:"30px"}}><C3ChartNew chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div></div>);
            }else{
              let parentDivClass = "col-md-12";
              return (<div key={randomNum} className={parentDivClass}><div><C3ChartNew chartInfo={chartInfo} classId={randomNum} data={story.data.chart_c3} yformat={story.data.yformat} y2format={story.data.y2format}  guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div></div>);
            }
            }
            break;
      case "table":
            if(!story.tableWidth)story.tableWidth = 100;
            var colClass= this.calculateWidth(story.tableWidth)
            let tableClass ="table table-bordered table-condensed table-striped table-fw-widget"
            colClass = colClass;
            return (<div className={colClass} key={randomNum}><CardTable  jsonData={story.data} type={story.dataType}/></div>);
            break;
      case "dataBox":
            let bgStockBox = "bgStockBox"
            if(this.props.algoAnalysis.app_id == 2){
              return (<DataBox  key={i} jsonData={story.data} type={story.dataType}/>);
            }else{
              return( 
                story.data.map((data,index)=>{
                return (
                  <div className="col-md-5ths col-sm-6 col-xs-12 bgStockBox">
                    <h3 className="text-center">{data.value}<br/><small>{data.name}</small></h3>
                    <Scrollbars className="performanceCard" style={{height:"78px"}} renderTrackHorizontal={props => <div {...props} style={{display: 'none'}} className="track-horizontal"/>}>
                      <div style={{padding:"5px 10px"}} >{data.description}</div>
                    </Scrollbars>
                  </div>
                );
              })
              );
            }
            break;
      case "button":
            return (<ModelSummeryButton key={randomNum} data={story.data.chart_c3} tabledownload={story.data.download_url} classId={randomNum} type={story.dataType}/>);
            break;
    }
    });
  return htmlData;
  }

    render(){
    if(isEmpty(this.props.algoAnalysis)){
    return (
      <div className="side-body">
        <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
      </div>
    );
    }else if(isEmpty(this.props.algoAnalysis.data)){
    return (
      <div className="side-body">
      <div className="main-content">
        <h1>There is no data</h1>
      </div>
      </div>
    );
    }else{
      var overviewCard = "";
      var performanceCard="";
      var algoAnalysis = this.props.algoAnalysis;
      
      var overviewPage = this.props.algoAnalysis.data.listOfNodes.filter(row => row.name === "Overview");
      var oVtop = overviewPage.map(card => card.listOfCards);
      let olen = oVtop[0].length;
      var j =0;
      var loop = 0;

      var th = [];    //table heading
      var tdata = [];   //table data
      var tw = [];    //table width
      var tableHeading = [];
      var tableData = [];

      //Rendering Summary and Settings Tables
      for(j=0;j<olen;j++){
        loop ++;
        if(loop-1 == j){
          th[j] = oVtop.map(fun => fun[j].cardData[0])
          tdata[j] = oVtop.map(fun => fun[j].cardData[1])
          tw[j] = oVtop.map(fun => fun[j].cardWidth)[0]
        }
        if(j == 0){
          tableHeading[0] = this.renderCardData(th[j],tw[j]);
          tableData[0] = this.renderCardData(tdata[j],tw[j]);
        }else{
          tableHeading[1] = this.renderCardData(th[j],tw[j]);
          tableData[1] = this.renderCardData(tdata[j],tw[j]);
        }
      }

      var performancePage = this.props.algoAnalysis.data.listOfNodes.filter(row => row.name === "Performance");
      var top = performancePage.map(card => card.listOfCards);
      let plen = top[0].length;
      var i = 0;
      var count = 0;

      var chartData = []
      var chartHeading = []
      var chartButton = []
      var h = []      //card heading
      var cd = []     //card data
      var w = []      //card width
      var topCards = ""
      var button = []

      //Rendering Charts
      for(i=0;i<plen;i++){
        if(i == 0){
          //render top cards for first iteration
          cd[i] = top.map(fun => fun[i].cardData[0])
          w[i] = top.map(fun => fun[i].cardWidth)[0]
          topCards = this.renderCardData(cd[i],w[i]);
        }else{
          count ++;
          //pick chart values
          if(count == i){
            h[i] = top.map(fun => fun[i].cardData[0])
            cd[i] = top.map(fun => fun[i].cardData[1])
            w[i] = top.map(fun => fun[i].cardWidth)[0]
            if(this.props.algoAnalysis.app_id == 13 && count == 1){
              button[0] = top.map(fun => fun[i].cardData[2])
            }
          }
          //Render chart values
          if(count == 1){
            chartHeading[1] = this.renderCardData(h[1],w[1]);
            chartData[1] = this.renderCardData(cd[1],w[1]);
            if(this.props.algoAnalysis.app_id == 13 && count == 1){
              chartButton[1] = this.renderCardData(button[0],w[1]);
            }
          }else if(count == 2){
            chartHeading[2] = this.renderCardData(h[2],w[2]);
            chartData[2] = this.renderCardData(cd[2],w[2]);
          }else if(count == 3){
            chartHeading[3] = this.renderCardData(h[3],w[3]);
            chartData[3] = this.renderCardData(cd[3],w[3]);
          }else if(this.props.algoAnalysis.app_id == 2 && count == 4){
            chartHeading[4] = this.renderCardData(h[4],w[4]);
            chartData[4] = this.renderCardData(cd[4],w[4]);
          }
        }
      }
      
      overviewCard=(
        <div class="row">
          <div class="col-md-6">
            <div className="sm-ml-15 sm-pb-10">{tableHeading[0]}</div>
            {tableData[0]}
          </div>
          <div class="col-md-6">
            <div className="sm-ml-15 sm-pb-10">{tableHeading[1]}</div>
            {tableData[1]}
          </div>
        </div>
      )
      
      let newClass = ""
      if(this.props.algoAnalysis.app_id == 13){
        newClass = "col-md-12";
      }else{
        newClass = "col-md-6"
      }
      performanceCard = (
        <div>
          <div class="row ov_card_boxes">
            {topCards} 
          </div>
          <div class="row xs-mt-10">
            <div class="col-md-6">
              {chartHeading[1]}
              {chartData[1]}
              {chartButton[1]}
            </div>
            <div class="col-md-6">
              {chartHeading[2]}
              {chartData[2]}
            </div>
          </div>
          <hr/>
          <div class="row xs-mt-10">
            <div class= {newClass} >  
              {chartHeading[3]}
              {chartData[3]}
            </div>
            <div class={newClass}>
              {chartHeading[4]}
              {chartData[4]}
            </div>
          </div>
        </div>
      )
    }

    return (
      <div class="side-body">
        <div class="main-content">
          <div class="page-head">
            <h3 class="xs-mt-0 xs-mb-0 text-capitalize">Model ID: {algoAnalysis.name}</h3>
          </div>
          <div class="panel panel-mAd box-shadow">
            <div class="panel-body no-border xs-p-20">
              <div id="pDetail" class="tab-container">
                <ul class="nav nav-tabs">
                  <li class="active"><a href="#overview" data-toggle="tab">Overview</a></li>
                  <li><a href="#performance" data-toggle="tab">Performance</a></li>
                  <li><a href="#deployment" data-toggle="tab">Deployment</a></li>
                </ul>
                <div class="tab-content xs-pt-20">
                  <div id="overview" class="tab-pane active cont">                
                    {overviewCard}
                  </div>
                  <div id="performance" class="tab-pane cont">
                    {performanceCard}
                  </div>
                  <div id="deployment" class="tab-pane cont">
                    <Deployment/>
                  </div>
                </div>
                <div class="buttonRow text-right"> <a href="javascript:;" onClick={this.closeModelSummary.bind(this)}class="btn btn-primary">Close </a> </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
  openDeployModal(item) {
    this.props.dispatch(openDeployModalAction(item));
  }

  closeDeployModal() {
    this.props.dispatch(closeDeployModalAction());
  }
}
