import React from "react";
import {MainHeader} from "../common/MainHeader";
import {Tabs, Tab} from "react-bootstrap";
import {AppsModelList} from "./AppsModelList";
import {AppsScoreList} from "./AppsScoreList";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {Button, Dropdown, Menu, MenuItem} from "react-bootstrap";
import {Share} from "../common/Share"
import {saveTopLevelValuesAction} from "../../actions/featureEngineeringActions";


import {connect} from "react-redux";
import {
  APPID1,
  APPID2,
  APPID3,
  APPNAME1,
  APPNAME2,
  APPNAME3,
  getUserDetailsOrRestart
} from "../../helpers/helper.js"
import {
  activateModelScoreTabs,
  storeModelSearchElement,
  storeScoreSearchElement,
  getAppsModelList,
  getAppsScoreList,
  getAppsAlgoList,
  refreshAppsAlgoList,
  updateModelSummaryFlag,
  updateScoreSummaryFlag,
  parameterTuningVisited,
  clearTensorFlowArray,
  selectMetricAction,
  clearDataPreview,
  clearPyTorchValues,

} from "../../actions/appActions";
import {AppsLoader} from "../common/AppsLoader";
import {getAllUsersList,getDataSetPreview,setEditModelValues,fetchModelEditAPISuccess,variableSlectionBack} from "../../actions/dataActions";


@connect((store) => {
  return {
    login_response: store.login.login_response,
    userList:store.datasets.allUserList,
    modelList: store.apps.modelList,
    algolist:store.algoList,
    currentAppId: store.apps.currentAppId,
    scoreList: store.apps.scoreList,
    activateModelScoreTabs: store.apps.activateModelScoreTabs,
    appsSelectedTabId: store.apps.appsSelectedTabId,
    scoreSummaryFlag: store.apps.scoreSummaryFlag,
    modelSummaryFlag: store.apps.modelSummaryFlag
  };
})

export class Apps extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
    if(store.getState().datasets.editmodelFlag){
     this.props.dispatch(clearDataPreview());
    }
       this.props.dispatch(updateModelSummaryFlag(false));
       this.props.dispatch(updateScoreSummaryFlag(false));
       this.props.dispatch(getAllUsersList());
       this.props.dispatch(parameterTuningVisited(false))
       this.props.dispatch(clearTensorFlowArray());
       this.props.dispatch(clearPyTorchValues());
       this.props.dispatch(variableSlectionBack(false));
      
       //have to recheck next 3actions needed or not
      this.props.dispatch(setEditModelValues("","",false));
       this.props.dispatch(fetchModelEditAPISuccess(""))
      this.props.dispatch(selectMetricAction("", "", ""));
      this.props.dispatch(saveTopLevelValuesAction("false",""))



    //checking for score and model tab
    if (this.props.match.url.indexOf("model") != -1) {
      this.props.dispatch(activateModelScoreTabs("model"));
    } else if (this.props.match.url.indexOf("score") != -1) {
      this.props.dispatch(activateModelScoreTabs("score"));
    }
    
  }
  modifyUrl(tabId) {
    this.props.dispatch(updateModelSummaryFlag(false));
    this.props.dispatch(activateModelScoreTabs(tabId));
    this.props.dispatch(storeModelSearchElement(""));
    this.props.dispatch(getAppsModelList(1));
    this.props.dispatch(storeScoreSearchElement(""));
    this.props.dispatch(getAppsScoreList(1));
    this.props.dispatch(getAppsAlgoList(1));
    if (tabId == "score") {
      let modelLink= window.location.href.includes("autoML") ? "/autoML/scores" : "/analyst/scores"
      this.props.history.push('/apps/' + this.props.match.params.AppId + modelLink )
    } 
    
    else{
      
      let modelLink= window.location.href.includes("autoML") ? "/autoML/models" : "/analyst/models"
      this.props.history.push('/apps/' + this.props.match.params.AppId + modelLink)
    }
   }

  proceedToModelManagement(tabId)
  {
    var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
    if (tabId == "score")
    {
      this.props.dispatch(getAppsAlgoList(1));
      this.props.dispatch(refreshAppsAlgoList(this.props));
     this.props.history.push('/apps/' + this.props.match.params.AppId +modeSelected +'/modelManagement');
    }else{
      this.props.dispatch(getAppsAlgoList(1));
      this.props.dispatch(refreshAppsAlgoList(this.props));
    this.props.history.push('/apps/' + this.props.match.params.AppId + modeSelected +'/modelManagement');
    }
  }


  render() {
    var appId = this.props.currentAppId;
    
    if (store.getState().apps.modelSummaryFlag) {
      if(!store.getState().apps.modelSummary.viewed){  
      let modelLink = this.props.location.pathname.includes("autoML") ? "/autoML/models/" : "/analyst/models/";
      let _link = "/apps/" + this.props.match.params.AppId + modelLink + store.getState().apps.modelSlug;
      return (<Redirect to={_link}/>);
      }
    }
     if (store.getState().apps.scoreSummaryFlag) {
      if(!store.getState().apps.scoreSummary.viewed){  
      let modelLink= this.props.location.pathname.includes("autoML") ? "/autoML/scores/" : "/analyst/scores/"
      let _link1 = "/apps/" + this.props.match.params.AppId + modelLink + store.getState().apps.scoreSlug;
      return (<Redirect to={_link1}/>);
      }
    }
    let models = <AppsModelList history={this.props.history} match={this.props.match}/>

    let scores = <AppsScoreList history={this.props.history} match={this.props.match}/>

    let modelManagement = ""

    if(appId==2 || appId == 13){
      modelManagement = <Button  onClick={this.proceedToModelManagement.bind(this)} bsStyle="primary">Manage Models</Button>
    }else{
      modelManagement = "";
    }

    return (
      <div className="side-body">
        <div className="main-content">
        <div class="buttonRow pull-right">
        {modelManagement}
        </div>
          <Tabs id="apps_tab" defaultActiveKey="score" activeKey={store.getState().apps.appsSelectedTabId} onSelect={this.modifyUrl.bind(this)} className="apps_list">
            {(getUserDetailsOrRestart.get().view_trainer_permission == "true")
              ? <Tab eventKey="model"  title="Models">{models}</Tab>
              : <Tab eventKey="model" disabled title="Models">{models}</Tab>}
            {(getUserDetailsOrRestart.get().view_score_permission == "true")
              ? <Tab eventKey="score" title="Scores">{scores}</Tab>
              : <Tab eventKey="score" disabled  title="Scores">{scores}</Tab>}
          </Tabs>
          <AppsLoader match={this.props.match}/>
          <Share usersList={this.props.userList}/>

        </div>
      </div>
    );
  }
}
