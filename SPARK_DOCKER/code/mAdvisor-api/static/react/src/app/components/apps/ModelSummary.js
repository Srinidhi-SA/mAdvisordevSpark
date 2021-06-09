import React from "react";
import {connect} from "react-redux";
import {getDeploymentList} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {openDeployModalAction, closeDeployModalAction} from "../../actions/modelManagementActions"
import {isEmpty,getUserDetailsOrRestart} from "../../helpers/helper";
import {getAlgoAnalysis, setmmLoaderFlag} from "../../actions/signalActions";
import { Deployment } from "./Deployment";
import { Card } from "../signals/Card";
import Scrollbars from "react-custom-scrollbars/lib/Scrollbars";

@connect((store) => {
  return {
    algoAnalysis:store.signals.algoAnalysis,
  };
})

export class ModelSummary extends React.Component {
  constructor(props) {
  super(props);
  this.state = {loader : true}
  }
  
  componentWillMount() {
  this.props.dispatch(getAlgoAnalysis(getUserDetailsOrRestart.get().userToken, this.props.match.params.slug));
  this.props.dispatch(getDeploymentList(this.props.match.params.slug));
  this.props.dispatch(setmmLoaderFlag(true));
  }

  componentDidMount(){
    setInterval(function() {
      var evt = document.createEvent('UIEvents');
      evt.initUIEvent('resize', true, false,window,0);
      window.dispatchEvent(evt);
    }, 500);
  }

  closeModelSummary(){
  window.history.back();
  }
  
  markFlag(){
    this.props.dispatch(setmmLoaderFlag(false));
  }

  getCards(i){
    let that = this;
    let cardDataList = "";
    let listOfCardList = this.props.algoAnalysis.data.listOfNodes[i].listOfCards;
    cardDataList = listOfCardList.map((data, i) => {
      let appId = that.props.algoAnalysis.app_id
      var cardDataArray = data.cardData;
      if(cardDataArray.length>0){
        if(cardDataArray[0].dataType === "dataBox"){
          if(cardDataArray[0].data.length === 5){
            let columnsTemplates = cardDataArray[0].data.map((data,i)=>{
              return(<div key={i} className="col-md-5ths col-sm-6 col-xs-12 bgStockBox">
                <h3 className="text-center">{data.value}<br/><small>{data.name}</small></h3>
                  <Scrollbars className="performanceCard" style={{height:"78px"}} renderTrackHorizontal={props => <div {...props} style={{display: 'none'}} className="track-horizontal"/>}>
                    <div style={{padding:"5px 10px"}} >{data.description}</div>
                  </Scrollbars>
                </div>);
              });
              return <div className="row ov_card_boxes">{columnsTemplates}</div>;
            }else{
              return (<div key={i} className="row ov_card_boxes"><Card cardData={cardDataArray} cardWidth={100}/></div>)
            }
        }else{
          return (<div key={i} className= {data.cardWidth===100?"col-md-12":"col-md-6"}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
        }
      }
    });
    return cardDataList
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
      var algoAnalysis = this.props.algoAnalysis;
      let overview = this.getCards(0);
      let performance = this.getCards(1);

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
                  <li onClick={this.markFlag.bind(this)}><a href="#performance" data-toggle="tab">Performance</a></li>
                  <li><a href="#deployment" data-toggle="tab">Deployment</a></li>
                </ul>
                <div class="tab-content xs-pt-20">
                  <div id="overview" class="tab-pane active cont">{overview}</div>
                  <div id="performance" class="tab-pane cont">{performance}</div>
                  <div id="deployment" class="tab-pane cont">
                    <Deployment/>
                  </div>
                </div>
                <div class="buttonRow text-right clearfix"> <a href="javascript:;" onClick={this.closeModelSummary.bind(this)}class="btn btn-primary">Close </a> </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
  openDeployModal(item) {
    this.props.dispatch(openDeployModalAction(item));
  }

  closeDeployModal() {
    this.props.dispatch(closeDeployModalAction());
  }
}