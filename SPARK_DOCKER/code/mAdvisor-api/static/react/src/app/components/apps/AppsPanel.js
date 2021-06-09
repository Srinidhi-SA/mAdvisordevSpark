import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Pagination} from "react-bootstrap";
import {Link, Redirect} from "react-router-dom";
import {
  updateSelectedApp,
  getAppsList,
  appsStoreSortElements,
  appsStoreSearchEle,
  updateModelSummaryFlag,
  uploadStockAnalysisFlag,
  closeAppsLoaderValue,
  updateScoreSummaryFlag,
  clearModelSummary,
  showRoboDataUploadPreview,
  updateAudioFileSummaryFlag,
  updateAppsFilterList,
  getAppsFilteredList,
  clearDataPreview,
} from "../../actions/appActions";
import {STATIC_URL,APPS_ALLOWED} from "../../helpers/env.js"
import { API } from "../../helpers/env";;
import { SEARCHCHARLIMIT,getUserDetailsOrRestart} from "../../helpers/helper.js"
import {cookieObj} from '../../helpers/cookiesHandler';
import { dashboardMetrics,selectedProjectDetails,saveDocumentPageFlag } from '../../actions/ocrActions';

@connect((store) => {
  return {
    appsList: store.apps.appsList,
    storeAppsSearchElement: store.apps.storeAppsSearchElement,
    storeAppsSortByElement: store.apps.storeAppsSortByElement,
    storeAppsSortType: store.apps.storeAppsSortType,
    app_filtered_keywords: store.apps.app_filtered_keywords
  };
})

export class AppsPanel extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
    var pageNo = 1;
    if(this.props.history.location.search!=""){
      let urlParams = new URLSearchParams(this.props.history.location.search);
      pageNo = (urlParams.get("pageNo")!="")?urlParams.get("pageNo"):pageNo
      if(urlParams.get('filterApplied')!=null){
        let lst = urlParams.get('filterApplied').split(",");
        this.props.dispatch(updateAppsFilterList(lst));
        this.props.dispatch(getAppsFilteredList(getUserDetailsOrRestart.get().userToken,pageNo))
      }else{
        let searchELem = (urlParams.get('search')!=null)?urlParams.get('search'):"";
        let sortELem = (urlParams.get('sort')!=null)?urlParams.get('sort'):"";
        let sortType = (urlParams.get('type')!=null)?urlParams.get('type'):"";
        this.props.dispatch(appsStoreSearchEle(searchELem));
        this.props.dispatch(appsStoreSortElements(sortELem,sortType));
        this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken,pageNo));
      }
    }else if (this.props.history.location.search.indexOf("pageNo") != -1) {
      pageNo = this.props.history.location.search.split("pageNo=")[1];
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, pageNo));
    } else
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, pageNo));
    this.props.dispatch(selectedProjectDetails('',''));
    this.props.dispatch(saveDocumentPageFlag(false));
  }

  onChangeAppsSearchBox(e) {
    if (e.target.value == "" || e.target.value == null) {
      this.props.dispatch(appsStoreSearchEle(""));
      if(this.props.storeAppsSortByElement!="" && this.props.storeAppsSortByElement!=null){
        this.props.history.push('/apps?sort=' + this.props.storeAppsSortByElement + '&type=' + this.props.storeAppsSortType);
      }else{
        this.props.history.push('/apps');
      }
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, 1));

    } else if (e.target.value.length > SEARCHCHARLIMIT) {
      if(this.props.storeAppsSortByElement!="" && this.props.storeAppsSortByElement!=null){
        this.props.history.push('/apps?search='+ e.target.value +'&sort=' + this.props.storeAppsSortByElement + '&type=' + this.props.storeAppsSortType);
      }else{
        this.props.history.push('/apps?search=' + e.target.value + '')
      }
      this.props.dispatch(appsStoreSearchEle(e.target.value));
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, 1));
    }
    if(this.props.app_filtered_keywords!=null)
      this.props.dispatch(updateAppsFilterList([]));
 }
  _handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (e.target.value != "" && e.target.value != null)
        this.props.history.push('/apps?search=' + e.target.value + '')
      this.props.dispatch(appsStoreSearchEle(e.target.value));
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, 1));
    }
  }
  handleCheckboxChange(e) {
    this.props.dispatch(appsStoreSearchEle(""));
    this.props.dispatch(appsStoreSortElements("",""))
    e.preventDefault();
    var array = this.props.app_filtered_keywords;
    var index = array.indexOf(e.target.name)
    if (e.target.checked && !index > -1) {
      array.push(e.target.name)
    } else if (!e.target.checked) {
      if (index > -1)
        array.splice(index, 1);
      }
    this.props.dispatch(updateAppsFilterList(array))
    this.props.dispatch(getAppsFilteredList(getUserDetailsOrRestart.get().userToken, 1))
    if(array.length>0)
    this.props.history.push('/apps?filterApplied=' + array)
    else
    this.props.history.push('/apps')
    if (document.getElementById('search_apps').value.trim() != ""){
        document.getElementById('search_apps').value = "";
    }
  }
  gotoAppsList(appId, appName,appDetails) {
    this.props.dispatch(updateSelectedApp(appId, appName,appDetails));
    this.props.dispatch(updateModelSummaryFlag(false));
    this.props.dispatch(updateScoreSummaryFlag(false));
    this.props.dispatch(showRoboDataUploadPreview(false));
    this.props.dispatch(updateAudioFileSummaryFlag(false));
    this.props.dispatch(closeAppsLoaderValue());
    this.props.dispatch(uploadStockAnalysisFlag(false));
    this.props.dispatch(clearModelSummary());
    this.props.dispatch(clearDataPreview());
    if(appDetails.displayName === "ITE"){
     this.getITEDashboardMetrics();
    }
  }

  getHeader = (token) => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json',
    }
  }

  getITEDashboardMetrics=()=>{
      return fetch(API + '/ocr/get_dashboard_metrics/', {
        method: 'get',
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      }).then(response => response.json())
      .then(data=>{
        if(data != ""){
          this.props.dispatch(dashboardMetrics(data));
        }
      })
  }  
  handleSelect(eventKey) {
    if (this.props.app_filtered_keywords.length == this.props.appsList.data[0].tag_keywords.length) {
      this.props.history.push('/apps?page=' + eventKey + '');
      this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, eventKey));
    } else {
      this.props.history.push('/apps?appliedFilter=' + this.props.app_filtered_keywords + '&pageNo=' + eventKey + '');
      this.props.dispatch(getAppsFilteredList(getUserDetailsOrRestart.get().userToken, eventKey));
    }
  }
  handleSearchReset() {
    this.props.dispatch(appsStoreSearchEle(""));
    if(this.props.storeAppsSortByElement!="" && this.props.storeAppsSortByElement!=null){
      this.props.history.push('/apps?sort=' + this.props.storeAppsSortByElement + '&type=' + this.props.storeAppsSortType);
    }else{
      this.props.history.push('/apps');
    }
    this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, 1));
  }
  handleSorting(sortBy, sortType) {
    this.props.dispatch(updateAppsFilterList([]))
    if(store.getState().apps.storeAppsSearchElement!=""){
      this.props.history.push('/apps?search='+ store.getState().apps.storeAppsSearchElement +'&sort=' + this.props.storeAppsSortByElement + '&type=' + this.props.storeAppsSortType);
    }else{
      this.props.history.push('/apps?sort=' + sortBy + '&type=' + sortType);
    }
    this.props.dispatch(appsStoreSortElements(sortBy, sortType));
    this.props.dispatch(getAppsList(getUserDetailsOrRestart.get().userToken, 1));
  }

  render() {
    if(APPS_ALLOWED==false){
      if(getUserDetailsOrRestart.get().view_signal_permission=="true")
        return (<Redirect to="/signals"/>)
      else if (getUserDetailsOrRestart.get().view_data_permission=="true") {
        return (<Redirect to="/data"/>)
      }else{
        cookieObj.clearCookies();
        return (<Redirect to="/login"/>)
      }
    }
  
    var appsLists = this.props.appsList.data;
    var top3 = this.props.appsList.top_3;
    var appListTemplate = "";
    let filterListTemplate = "";
    let paginationTag = null
    let filteredKeywords = this.props.app_filtered_keywords
    if (this.props.storeAppsSearchElement != "" && (this.props.location.search == "" || this.props.location.search == null)) {
      this.props.dispatch(appsStoreSearchEle(""));
      let search_element = document.getElementById('search_apps');
      if (search_element)
        document.getElementById('search_apps').value = "";
    }

    if ((this.props.location.sort !=undefined) && (this.props.location.sort == "" || this.props.location.sort == null)) {
      this.props.dispatch(appsStoreSortElements("", null));
    }

    if (appsLists != undefined && appsLists.length > 0) {
      const pages = this.props.appsList.total_number_of_pages;
      const current_page = this.props.appsList.current_page;
      filteredKeywords = appsLists[0].tag_keywords
    if (pages > 1) {
      paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect.bind(this)} first last next prev boundaryLinks items={pages} activePage={current_page}/>
    }
    appListTemplate = appsLists.map((data, index) => {
      var tagsList = data.tags.map((tagsList, i) => {
        return (
          <li key={i}>
            <a href="#">
            <i className="fa fa-tag"></i>&nbsp;{tagsList.displayName}</a>
          </li>
        )
      });
      return (
        <div key={index} class="col-md-4 xs-mb-20">
          <div className="app-block">
            <Link className="app-link" id={data.name} onClick={this.gotoAppsList.bind(this, data.app_id, data.name,data)} to= 
              {(data.app_id == 2 || data.app_id == 13) ? 
                data.app_url.replace("/models","") +"/modeSelection": 
                (data.displayName== "ITE" && (getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole ==  "Superuser"))?
                data.app_url.concat("project"):
                ((data.displayName== "ITE" && (getUserDetailsOrRestart.get().userRole == "ReviewerL1" || getUserDetailsOrRestart.get().userRole ==  "ReviewerL2"))?         
                data.app_url.concat("reviewer"):
                data.app_url.replace("/models","") + "/" 
                )
                }>
                <div className="col-md-4 col-sm-3 col-xs-5 xs-p-20">
                  <img src={STATIC_URL + "assets/images/" + data.iconName} className="img-responsive"/>
                </div>
                <div className="col-md-8 col-sm-9 col-xs-7">
                  <h4>{data.displayName}</h4>
                  <p>{data.description}</p>
                </div>
                <div class="clearfix"></div>
              </Link>
              <div className="card-footer">
                <ul className="app_labels">
                  {tagsList}
                </ul>
                <div id="myPopover" className="pop_box hide">
                  <p>Info</p>
                </div>
              </div>
            </div>
          <div className="clearfix"></div>
        </div>
        )
      });
      filterListTemplate = appsLists[0].tag_keywords.map((tag, i) => {
        let checked = false
        if (this.props.app_filtered_keywords.indexOf(tag) > -1)
          checked = true
        return (
          <li key={i} className="xs-pl-10">
            <div key={i} className="ma-checkbox inline">
              <input id={`chk_mes1_ ${i}`} type="checkbox" name={tag} checked={checked} onClick={this.handleCheckboxChange.bind(this)}/>
              <label htmlFor={`chk_mes1_ ${i}`}>{tag}</label>
            </div>
          </li>
        )
      });
    }else{
      if (appsLists != undefined && appsLists.length == 0) {
        if(top3.length > 0){
          filterListTemplate = top3[0].tag_keywords.map((tag, i) => {
            let checked = false
            if (this.props.app_filtered_keywords.indexOf(tag) > -1)
              checked = true
            return (
              <li key={i} className="xs-pl-10">
                <div key={i} className="ma-checkbox inline">
                  <input id={`chk_mes1_ ${i}`} type="checkbox" name={tag} checked={checked} onClick={this.handleCheckboxChange.bind(this)}/>
                  <label htmlFor={`chk_mes1_ ${i}`}>{tag}</label>
                </div>
              </li>
            )
          });
        }
        appListTemplate =  <div><br/><div className="text-center text-muted xs-mt-50"><h2>No results found..</h2></div></div>
      }else{
        return(
          <div className="side-body">
            <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
          </div>
        )
      }
    }
    return (
      <div className="side-body">
        <div class="page-head">
          <div class="row">
            <div class="col-md-7">
              <h3 className="xs-mt-0 nText">Apps</h3>
            </div>
            <div class="col-md-5">
              <div class="btn-toolbar pull-right">
                <div class="input-group">
                  <div className="search-wrapper">
                    <form>
                      <input defaultValue={store.getState().apps.storeAppsSearchElement} type="text" name="search_apps" onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeAppsSearchBox.bind(this)} title="Search Apps..." id="search_apps" className="form-control search-box" placeholder="Search Apps..." required/>
                      <span className="fa fa-search form-control-feedback"></span>
                      <button className="close-icon" type="reset" onClick={this.handleSearchReset.bind(this)}></button>
                    </form>
                  </div>
                </div>
                <div class="btn-group">
                  <button type="button" title="Sorting" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                    <i className="glyphicon glyphicon-sort"></i>
                  </button>
                  <ul role="menu" class="dropdown-menu dropdown-menu-right">
                    <li>
                      <a href="#" onClick={this.handleSorting.bind(this, 'name', 'asc')}>
                        <i class="fa fa-sort-alpha-asc"></i>
                        &nbsp;Name Ascending</a>
                    </li>
                    <li>
                      <a href="#" onClick={this.handleSorting.bind(this, 'name', '-')}>
                        <i class="fa fa-sort-alpha-desc"></i>
                        &nbsp;Name Descending</a>
                    </li>
                  </ul>
                </div>
                    
                <div class={this.props.app_filtered_keywords.length>0? "btn-group selected":"btn-group"}>
                  <button type="button" title="Filter" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                    <i class="fa fa-filter fa-lg"></i>
                  </button>
                  <ul role="menu" class="dropdown-menu dropdown-menu-right">
                    {filterListTemplate}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="main-content">
          <div className="row">
            {appListTemplate}
            <div className="clearfix"></div>
          </div>
          <div className="ma-datatable-footer" id="idSignalPagination">
            <div className="dataTables_paginate">
              {paginationTag}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
