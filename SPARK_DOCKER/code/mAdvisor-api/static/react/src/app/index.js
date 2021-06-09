import React from "react";
import {render} from "react-dom";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import {Provider} from "react-redux"
import store from "./store"
import {Main} from "./components/Main";
import {Home} from "./components/Home";
import {Login} from "./components/Login";
import {Apps} from "./components/apps/Apps";
import {Data} from "./components/data/Data";
import {DataPreview} from "./components/data/DataPreview";
import {Signals} from "./components/signals/Signals";
import {Signal} from "./components/signals/Signal";
import {SignalDocumentMode} from "./components/signals/SignalDocumentMode";
import {OverViewPage} from "./components/signals/overViewPage";
import {VariableSelection} from "./components/signals/variableSelection";
import {ModelVariableSelection} from "./components/apps/ModelVariableSelection";
import {ModelBuildingModeSelection} from "./components/apps/ModelBuildingModeSelection"
import {DataCleansing} from "./components/apps/DataCleansing"
import {FeatureEngineering} from "./components/apps/FeatureEngineering"
import {ModelManagement} from "./components/apps/ModelManagement"
import {ModelSummary} from "./components/apps/ModelSummary"
import {AppsModelHyperDetail} from "./components/apps/AppsModelHyperDetail";
import {ScoreVariableSelection} from "./components/apps/ScoreVariableSelection";
import {AppsScoreDetail} from "./components/apps/AppsScoreDetail";
import {AppsPanel} from "./components/apps/AppsPanel";
import {RoboInsightList} from "./components/apps/RoboInsightList";
import {RoboDataUploadPreview} from "./components/apps/RoboDataUploadPreview";
import {RoboDocumentMode} from "./components/apps/RoboDocumentMode";
import {Profile} from "./components/common/profile";
import {AudioFileList} from "./components/apps/AudioFileList";
import {AudioFileSummary} from "./components/apps/AudioFileSummary";
import {AppsStockAdvisorList} from "./components/apps/AppsStockAdvisorList";
import {AppsStockDataPreview} from "./components/apps/AppsStockDataPreview";
import {AppsStockDocumentMode} from "./components/apps/AppsStockDocumentMode";
import {DataPreviewLeftPanel} from "./components/data/DataPreviewLeftPanel";
import {ModelAlgorithmSelection} from "./components/apps/ModelAlgorithmSelection";
import {AlgorithmSelection} from "./components/apps/AlgorithmSelection";
import {getUserDetailsOrRestart} from "./helpers/helper";
import {Redirect} from "react-router-dom";
import {APPS_ALLOWED} from "./helpers/env.js";
import {SampleFrame} from "./components/common/SampleFrame";
import {KyloMenuList} from "./components/common/KyloMenuList";
import {LexClass} from "./components/apps/lex";
import {OcrMain} from "./components/apps/Ocr/OcrMain";
import {OcrProject} from "./components/apps/Ocr/OcrProject";
import {OcrManageUser} from "./components/apps/Ocr/OcrMangeUser";
import {OcrConfigure} from "./components/apps/Ocr/OcrConfigure";
import {OcrReviewer} from "./components/apps/Ocr/OcrReviewer";

class App extends React.Component {
  hasSignalRoutePermission() {
    if (getUserDetailsOrRestart.get().view_signal_permission == "true")
      return true
    else
      return false
  }
  hasDataRoutePermission() {
    if (getUserDetailsOrRestart.get().view_data_permission == "true")
      return true
    else
      return false
  }
  hasTrainerRoutePermission() {
    if (getUserDetailsOrRestart.get().view_trainer_permission == "true"&&APPS_ALLOWED==true)
      return true
    else
      return false
  }
  hasScoreRoutePermission() {
    if (getUserDetailsOrRestart.get().view_score_permission == "true"&&APPS_ALLOWED==true)
      return true
    else
      return false
  }
  render() {
    sessionStorage.url = window.location.pathname;
    //we need to do this as BrowserRouter dont pass history and props if we call components directly
    //signal related routing permissions
    const signals = (props) => {
      if (this.hasSignalRoutePermission()) {
        switch (props.match.path) {
          case "/signals":
            {
              return (<Signals {...props}/>)
            }
            break;
          case "/signals/:slug":
            {
             var list=store.getState().signals.allSignalList
            if(Object.values(list).map(i=>i.slug).includes(props.match.params.slug)||store.getState().signals.selectedSignal==props.match.params.slug||Object.keys(list).length === 0|| store.getState().signals.signalAnalysis.slug==props.match.params.slug)
              {
                if(document.getElementsByClassName('cst-fSize')[0]!=undefined && document.getElementsByClassName('cst-fSize')[0].innerText=="I want to analyze")
                return (<DataPreview {...props}/>)
                else 
                return (<Signal {...props}/>)
              }else{
                return (<DataPreview {...props}/>)
              }
            }
            break;
          case "/signals/:slug/:l1":
          {
          if(props.match.params.l1=="createSignal") 
              return (<VariableSelection {...props}/>)
            else
              return (<OverViewPage {...props}/>)
          }
            break;
          case "/signals/:slug/:l1/:l2/:l3":
            {
              return (<OverViewPage {...props}/>)
            }
            break;
          case "/signals/:slug/:l1/:l2":
            {
              return (<OverViewPage {...props}/>)
            }
            break;
          case "/signaldocumentMode/:slug":
            {
              return (<SignalDocumentMode {...props}/>)
            }
            break;
          case "/signals?page=:slug":
            {
              return (<Signals {...props}/>)
            }
            break;
          case "/signals?search=:slug":
            {
              return (<Signals {...props}/>)
            }
            break;
        }

      } else if (this.hasDataRoutePermission()) {
        return (<Redirect to="/data"/>)
      } else {
        //currently sending it to app, otherwise it should go to Login
        return (<Redirect to="/apps"/>)
      }
    }
    //data related routing permissions
    const data = (props) => {
      if (this.hasDataRoutePermission()) {
        switch (props.match.path) {

          case "/data":
            {
              return (<Data {...props}/>)
            }
            break;

          case "/data/:slug":
            {
              return (<DataPreview {...props}/>)
            }
            break;
          case "data?page=:slug":
            {
              return (<Data {...props}/>)
            }
            break;
          case "/data/:slug/createSignal":
            {
              return (<VariableSelection {...props}/>)
            }
            break;
            case "/apps/:AppId/analyst/models/data/:slug":
            {
              return (<DataPreview {...props}/>)
            }
            break;
          case "/apps/:AppId/analyst/models/:modelSlug/data/:slug":
            {
              return (<DataPreview {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/models/:modelSlug/data/:slug":
            {
              return (<DataPreview {...props}/>)
            }
            break;
        }

      } else if (this.hasSignalRoutePermission()) {
        return (<Redirect to="/signals"/>)
      } else {
        //currently sending it to app, otherwise it should go to Login
        return (<Redirect to="/apps"/>)
      }
    }
    //app trainer and score route permission
    const trainer = (props) => {
      if (this.hasTrainerRoutePermission()) {
        switch (props.match.path) {
          case "/apps/:AppId/analyst/models":
            {
              return (<Apps {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/models":
              {
                return (<Apps {...props}/>)
              }
              break;
          case "/apps/:AppId/analyst/models?page=:slug":
            {
              return (<Apps {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/models?page=:slug":
              {
                return (<Apps {...props}/>)
              }
              break;
          case "/apps/:AppId/analyst/models/:slug":
            {
              return (<AppsModelHyperDetail {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/models/:slug":
              {
                return (<AppsModelHyperDetail {...props}/>)
              }
              break;

        }

      } else if (this.hasScoreRoutePermission()) {
        let score_url = "/apps"
        if (props.match.params.AppId)
          score_url = "/apps/" + props.match.params.AppId + "/analyst/scores"
        return (<Redirect to={score_url}/>)
      } else {
        return (<Redirect to="/apps"/>)
      }
    }

    const score = (props) =>  {
      if (this.hasScoreRoutePermission()) {
        switch (props.match.path) {
          case "/apps/:AppId/analyst/scores":
            {
              return (<Apps {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/scores":
              {
                return (<Apps {...props}/>)
              }
              break;
          case "/apps/:AppId/analyst/scores?page=:slug":
            {
              return (<Apps {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/scores?page=:slug":
            {
              return (<Apps {...props}/>)
            }
            break;
          case "/apps/:AppId/analyst/scores/:slug":
            {
              return (<AppsScoreDetail {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/scores/:slug":
            {
              return (<AppsScoreDetail {...props}/>)
            }
            break;
          case "/apps/:AppId/analyst/scores/:slug/dataPreview":
            {
              return (<DataPreviewLeftPanel {...props}/>)
            }
            break;
            case "/apps/:AppId/autoML/scores/:slug/dataPreview":
              {
                return (<DataPreviewLeftPanel {...props}/>)
              }
              break;
        }

      } else if (this.hasTrainerRoutePermission()) {
        let model_url = "/apps"
        var modeSelected= window.location.pathname.includes("autoML")?'/autoML':'/analyst'
        if (props.match.params.AppId)
          model_url = "/apps/" + props.match.params.AppId +modeSelected+"/models"
        return (<Redirect to={model_url}/>)
      } else {
        return (<Redirect to="/apps"/>)
      }
    }

    return (
      <BrowserRouter>
        <Switch>
          <Route exact path="/login" component={Login}/>
          <Main>
            <Route exact path="/" component={Home}/>
            <Route exact path="/apps/lex" component={LexClass}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/" component={OcrMain}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/project/" component={OcrProject}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/project/:imageSlug" component={OcrProject}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/reviewer/:imageSlug" component={OcrProject}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/manageUser/" component={OcrManageUser}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/configure/" component={OcrConfigure}/>
            <Route exact path="/apps/ocr-mq44ewz7bp/reviewer/" component={OcrReviewer}/>
            <Route exact path="/user-profile" component={Profile}/>
            <Route exact path="/signals" render={signals}/> 
            <Route exact path="/signals/:slug" render={signals}/>
            <Route exact path="/signals/:slug/:l1" render={signals}/>
            <Route exact path="/signals/:slug/:l1/:l2/:l3" render={signals}/>
            <Route exact path="/signals/:slug/:l1/:l2" render={signals}/>
            <Route path="/variableselection" component={VariableSelection}/>
            <Route path="/signaldocumentMode/:slug" render={signals}/>
            <Route exact path="/data" render={data}/>
            <Route exact path="/data/:slug" render={data}/>
            <Route exact path="/apps" component={AppsPanel}/>
            <Route exact path="/apps?page=:slug" component={AppsPanel}/>
            <Route exact path="/apps/:AppId/autoML/models" render={trainer}/>
            <Route exact path="/apps/:AppId/analyst/models" render={trainer}/>
            <Route exact path="/apps/:AppId/autoML/scores" render={score}/>
            <Route exact path="/apps/:AppId/analyst/scores" render={score}/>
            <Route exact path="/apps/:AppId/analyst/scores?page=:slug" render={score}/>
            <Route exact path="/apps/:AppId/autoML/models/data/:slug/createModel" component={ModelVariableSelection}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug/createModel" component={ModelVariableSelection}/>
            <Route exact path="/apps/:AppId/autoML/models/:slug" render={trainer}/>
            <Route exact path="/apps/:AppId/analyst/models/:slug" render={trainer}/>
            <Route exact path="/apps/:AppId/autoML/scores/:slug" render={score}/>
            <Route exact path="/apps/:AppId/analyst/scores/:slug" render={score}/>
            <Route exact path="/apps/:AppId/autoML/models/:modelSlug/data/:slug/createScore" component={ScoreVariableSelection}/>
            <Route exact path="/apps/:AppId/analyst/models/:modelSlug/data/:slug/createScore" component={ScoreVariableSelection}/>
            <Route exact path="/data?page=:slug" render={data}/>
            <Route exact path="/data/:slug/createSignal" render={data}/>   
            <Route exact path="/signals?page=:slug" render={signals}/>
            <Route exact path="/signals?search=:slug" render={signals}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug" render={data}/>
            <Route exact path="/apps/:AppId/analyst/models/:modelSlug/data/:slug" render={data}/>
            <Route exact path="/apps-robo" component={RoboInsightList}/>
            <Route exact path="/apps-robo-list/:roboSlug/:tabName/data/:slug" component={RoboDataUploadPreview}/>
            <Route exact path="/apps-robo/:slug/:l1" component={OverViewPage}/>
            <Route exact path="/apps-robo/:slug/:l1/:l2" component={OverViewPage}/>
            <Route exact path="/apps-robo/:slug/:l1/:l2/:l3" component={OverViewPage}/>
            <Route exact path="/apps-robo-document-mode/:slug" component={RoboDocumentMode}/>
            <Route exact path="/apps/:AppId/autoML/models/:modelSlug/data/:slug" render={data}/>
            <Route exact path="/apps-robo/:roboSlug" component={RoboDataUploadPreview}/>
            <Route exact path="/apps-robo-list" component={RoboInsightList}/>
            <Route exact path="/apps/audio" component={AudioFileList}/>
            <Route exact path="/apps/audio/:audioSlug" component={AudioFileSummary}/>
            <Route exact path="/apps/audio?page=:pageNo" component={AudioFileList}/>
            <Route exact path="/apps-stock-advisor" component={AppsStockAdvisorList}/>
            <Route exact path="/apps-stock-advisor-analyze/data/:slug" component={AppsStockDataPreview}/>
            <Route exact path="/apps-stock-advisor/:slug" component={OverViewPage}/>
            <Route exact path="/apps-stock-advisor/:slug/:l1" component={OverViewPage}/>
            <Route exact path="/apps-stock-advisor/:slug/:l1/:l2/:l3" component={OverViewPage}/>
            <Route exact path="/apps-stock-advisor/:slug/:l1/:l2" component={OverViewPage}/>
            <Route exact path="/apps-stock-document-mode/:slug" component={AppsStockDocumentMode}/>
            <Route exact path="/apps/:AppId/analyst/scores/:slug/dataPreview" render={score}/>
            <Route exact path="/apps/:AppId/autoML/scores/:slug/dataPreview" render={score}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug/createModel/algorithmSelection" component={AlgorithmSelection}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug/createModel/parameterTuning" component={ModelAlgorithmSelection}/>
            <Route exact path="/apps/:AppId/modeSelection" component={ModelBuildingModeSelection}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug/createModel/dataCleansing" component={DataCleansing}/>
            <Route exact path="/apps/:AppId/analyst/models/data/:slug/createModel/featureEngineering" component={FeatureEngineering}/>
            <Route exact path="/apps/:AppId/analyst/modelManagement" component={ModelManagement}/>
            <Route exact path="/apps/:AppId/autoML/modelManagement" component={ModelManagement}/>
            <Route exact path="/apps/:AppId/autoML/modelManagement/:slug" component={ModelSummary}/> 
            <Route exact path="/apps/:AppId/analyst/modelManagement/:slug" component={ModelSummary}/> 
            <Route exact path="/datamgmt" component={KyloMenuList}/>
            <Route exact path="/datamgmt/selected_menu/:kylo_url" component={SampleFrame}/>
        </Main>
        </Switch>
      </BrowserRouter>
    );
  }

}

render(
  <Provider store={store}>

  <App/>

</Provider>, window.document.getElementById('app'));
