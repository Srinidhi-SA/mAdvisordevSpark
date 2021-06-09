import React from "react";
import {NavLink, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {appsStoreSearchEle, appsStoreSortElements, getAppsList, updateAppsFilterList} from "../../actions/appActions"
import {hideDataPreview, getDataList,storeDataSearchElement,storeDataSortElements, clearDataList} from "../../actions/dataActions";
import {getList,storeSearchElement,emptySignalAnalysis, clearSignalList, storeSortElements} from "../../actions/signalActions";
import {getUserDetailsOrRestart} from "../../helpers/helper";
import {APPS_ALLOWED,ENABLE_KYLO_UI} from "../../helpers/env.js";
import ReactNotifications from 'react-browser-notifications';

@connect((store) => {
  return {
    apps_regression_modelName: store.apps.apps_regression_modelName,
  };
})

class LeftPanel extends React.Component {

  constructor(props) {
    super(props);
  }
  componentDidMount() {
    if(this.props.location.pathname.indexOf("/apps-") >= 0)
    $('.navbar-nav')[0].childNodes[1].childNodes[0].className = " sdb sdb_app active";
  }
  changeToSignalTab(){
    this.hideDataPrev()
    this.props.dispatch(storeSearchElement(""))
    this.props.dispatch(storeSortElements(null,null));
    this.props.dispatch(clearSignalList())
    this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
  }
  changeToDataTab(){
    this.hideDataPrev()
    this.props.dispatch(storeDataSearchElement(""));
    this.props.dispatch(storeDataSortElements("",""));
    this.props.dispatch(clearDataList());
    this.props.dispatch(getDataList(1));
  }
  changeToAppsTab(){
    this.hideDataPrev()
    this.props.dispatch(appsStoreSearchEle(""));
    this.props.dispatch(appsStoreSortElements("",""));
    this.props.dispatch(updateAppsFilterList([]));
    this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken,1))
  }
  hideDataPrev(){
    this.props.dispatch(hideDataPreview());
    this.props.dispatch(emptySignalAnalysis());
  }
  showNotifications= () => {
    if(this.n.supported()) this.n.show();
  }
  handleClick =(event)=> {
    window.focus()
    this.n.close(event.target.tag);
  }
  render() {
    let notifyBody= this.props.apps_regression_modelName + " model created successfully."
    let view_data_permission=getUserDetailsOrRestart.get().view_data_permission
    let view_signal_permission = getUserDetailsOrRestart.get().view_signal_permission
    let enable_kylo = ENABLE_KYLO_UI;
    let apps_allowed = APPS_ALLOWED;
    return (
      <div>
        <ReactNotifications onRef={ref => (this.n = ref)} title="mAdvisor" body= {notifyBody} icon= "devices-logo.png" tag="abcdef" onClick={event => this.handleClick(event)} />
        <button className="notifyBtn noDisplay" onClick={this.showNotifications}>Notify Me!</button>
          <div className="side-menu collapse navbar-collapse" id="side-menu">
            <div className="side-menu-container">
              <ul className="nav navbar-nav">
                <li className={(view_signal_permission=="true")?"":"notAllowed"} title={(view_signal_permission=="true")?"":"Access Denied"}>
                  <NavLink id="signalTab" onClick={this.changeToSignalTab.bind(this)} to="/signals"
                    isActive={(match,location) => /^[/]signal/.test(location.pathname)} className={(view_signal_permission=="true")?"sdb":"sdb sdb_signal deactivate"} >
                    <i className="fa fa-podcast fa-2x" aria-hidden="true"></i><br />Signal
                  </NavLink>
                </li>
                <li>
                  <NavLink id="appsTab" onClick={this.changeToAppsTab.bind(this)} to="/apps"
                    isActive={(match,location) => /^[/]apps/.test(location.pathname)} className={(apps_allowed==true)?" sdb":""} >
                    <i className="fa fa-cubes fa-2x" aria-hidden="true"></i><br/>Apps
                  </NavLink>
                </li>
                <li className={(view_data_permission=="true")?"":"notAllowed"}>
                  <NavLink id="dataTab" onClick={this.changeToDataTab.bind(this)} to="/data"
                    activeClassName={(view_data_permission=="true")?"active":false} className={(view_data_permission=="true")?"sdb":"sdb sdb_data deactivate"} >
                    <i className="fa fa-database fa-2x" aria-hidden="true"></i><br />Data
                  </NavLink>
                </li>
                {(enable_kylo==true||enable_kylo=="True"||enable_kylo=="true")?
                  <li>
                    <NavLink onClick={this.hideDataPrev.bind(this)} isActive={(match,location) => /^[/]datamgmt/.test(location.pathname)} className=" sdb" to="/datamgmt">
                      <i className="fa fa-folder-open fa-2x" aria-hidden="true"></i><br />Data<br />manage
                    </NavLink>
                  </li>:<div/>
                }                
                <li>
                  <NavLink onClick={this.hideDataPrev.bind(this)} target="_blank" activeClassName="active" className="sdb" to="/static/userManual/UserManual.html">
                    <i className="fa fa-question-circle fa-2x" aria-hidden="true"></i><br />Help
                  </NavLink>
                </li>
              </ul>
            </div>
          </div>
      </div>
    );
  }
}
export default withRouter(LeftPanel);
