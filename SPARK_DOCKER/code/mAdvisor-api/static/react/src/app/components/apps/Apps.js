import React from "react";
import {Tabs, Tab} from "react-bootstrap";
import {AppsModelList} from "./AppsModelList";
import {AppsScoreList} from "./AppsScoreList";
import {Redirect} from "react-router-dom";
import store from "../../store";
import {Button} from "react-bootstrap";
import {Share} from "../common/Share"
import {saveTopLevelValuesAction} from "../../actions/featureEngineeringActions";
import {connect} from "react-redux";
import {getUserDetailsOrRestart} from "../../helpers/helper.js"
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
import {getAllUsersList,setEditModelValues,fetchModelEditAPISuccess,variableSlectionBack} from "../../actions/dataActions";


@connect((store) => {
  return {
    userList:store.datasets.allUserList,
    currentAppId: store.apps.currentAppId,
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
    this.props.dispatch(setEditModelValues(false));
    this.props.dispatch(fetchModelEditAPISuccess(""))
    this.props.dispatch(selectMetricAction("", "", ""));
    this.props.dispatch(saveTopLevelValuesAction("false",""))

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
    let modelLink= window.location.href.includes("autoML") ? "/autoML" : "/analyst"
    if (tabId == "score") {
      this.props.history.push('/apps/' + this.props.match.params.AppId + modelLink +"/scores" )
    }else{
      this.props.history.push('/apps/' + this.props.match.params.AppId + modelLink + "/models")
    }
   }

  proceedToModelManagement(){
    var modeSelected= window.location.pathname.includes("autoML")?'/autoML':'/analyst'
    this.props.dispatch(getAppsAlgoList(1));
    this.props.dispatch(refreshAppsAlgoList(this.props));
    this.props.history.push('/apps/' + this.props.match.params.AppId +modeSelected +'/modelManagement');
  }


  render() {
    let modelLink = this.props.location.pathname.includes("autoML") ? "/autoML" : "/analyst";
    if(store.getState().apps.modelSummaryFlag) {
      if(!store.getState().apps.modelSummary.viewed){  
        let _link = "/apps/" + this.props.match.params.AppId + modelLink + "/models/" + store.getState().apps.modelSlug;
        return (<Redirect to={_link}/>);
      }
    }
     if (store.getState().apps.scoreSummaryFlag) {
      if(!store.getState().apps.scoreSummary.viewed){  
      let _link1 = "/apps/" + this.props.match.params.AppId + modelLink + "/scores/" + store.getState().apps.scoreSlug;
      return (<Redirect to={_link1}/>);
      }
    }
    let models = <AppsModelList history={this.props.history} match={this.props.match}/>
    let scores = <AppsScoreList history={this.props.history} match={this.props.match}/>
    let modelManagement = ""

    if(this.props.currentAppId==2 || this.props.currentAppId == 13){
      modelManagement = <Button onClick={this.proceedToModelManagement.bind(this)} bsStyle="primary">Manage Models</Button>
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
