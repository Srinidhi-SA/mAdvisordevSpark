import React from "react";
import {connect} from "react-redux";
import { Redirect} from "react-router-dom";
import store from "../../store";
import {
  getList,
  storeSearchElement,
  storeSortElements,
  assignSignalData,
  refreshSignals,
  getAllSignalList,
  clearSignalList
} from "../../actions/signalActions";
import { Pagination } from "react-bootstrap";

import {STATIC_URL} from "../../helpers/env";
import {SEARCHCHARLIMIT, getUserDetailsOrRestart, isEmpty} from "../../helpers/helper"
import {getAllDataList, hideDataPreview,getAllUsersList,setEditModelValues,fetchModelEditAPISuccess,variableSlectionBack, paginationFlag} from "../../actions/dataActions";
import {CreateSignalLoader} from "../common/CreateSignalLoader";
import {LatestSignals} from "./LatestSignals";
import {SignalCard} from "./SignalCard";
import {showLoading} from 'react-redux-loading-bar';
import {Share} from "../common/Share";
import {saveTopLevelValuesAction} from "../../actions/featureEngineeringActions";
import {clearDataPreview} from "../../actions/appActions";

@connect((store) => {
  return {
    signalList: store.signals.signalList.data,
    signal_search_element: store.signals.signal_search_element,
    signal_sorton: store.signals.signal_sorton,
    signal_sorttype: store.signals.signal_sorttype,
    signalAnalysis: store.signals.signalAnalysis,
    userList:store.datasets.allUserList
  };
})

export class Signals extends React.Component {
  constructor(props) {
    super(props);
    this.handleSelect = this.handleSelect.bind(this);
  }
  componentWillMount() {
    this.props.dispatch(getAllSignalList());
    this.props.dispatch(clearDataPreview())
    this.props.dispatch(hideDataPreview())
    this.props.dispatch(setEditModelValues(false));
    this.props.dispatch(fetchModelEditAPISuccess(""))
    this.props.dispatch(saveTopLevelValuesAction("false",""))
    this.props.dispatch(variableSlectionBack(false)); 
    if(getUserDetailsOrRestart.get().view_data_permission=="true")
      this.props.dispatch(getAllDataList());
    this.props.dispatch(assignSignalData(null));
    
    var pageNo = 1;
    if(this.props.history.location.search!=""){
      let urlParams = new URLSearchParams(this.props.history.location.search);
      pageNo = (urlParams.get("page")!="")?urlParams.get("page"):pageNo

      let searchELem = urlParams.get('search')!=null?urlParams.get('search'):"";
      let sortELem = urlParams.get('sort')!=null?urlParams.get('sort'):"";
      let sortType = urlParams.get('type')!=null?urlParams.get('type'):"";
      
      this.props.dispatch(storeSearchElement(searchELem));
      this.props.dispatch(storeSortElements(sortELem,sortType));
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken,pageNo))
    }else 
    if (this.props.history.location.search.indexOf("page") != -1) {
      pageNo = this.props.history.location.search.split("page=")[1];
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, pageNo));
    } else{
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, pageNo));
    }

  }

  componentDidMount() {
    this.props.dispatch(refreshSignals(this.props));
    this.props.dispatch(getAllUsersList(this.props));
  }

  handleSelect(eventKey) {
    this.props.dispatch(paginationFlag(true));
    if(this.props.signal_search_element) {
      if (this.props.signal_sorton) {
        this.props.history.push('/signals?search=' + this.props.signal_search_element + '&sort=' + this.props.signal_sorton + '&page=' + eventKey + '');
      } else {
        this.props.history.push('/signals?search=' + this.props.signal_search_element + '&page=' + eventKey + '');
      }
    }else if (this.props.signal_sorton) {
      this.props.history.push('/signals?sort=' + this.props.signal_sorton + '&type=' + this.props.signal_sorttype + '&page=' + eventKey + '');
    }else
      this.props.history.push('/signals?page=' + eventKey + '');
    this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, eventKey));
  }

  _handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (e.target.value != "" && e.target.value != null){
        if(this.props.signal_sorton)
          this.props.history.push('/signals?search='+e.target.value+'&sort=' + this.props.signal_sorton + '&type=' + this.props.signal_sorttype)
        else
          this.props.history.push('/signals?search=' + e.target.value + '')
      }
      this.props.dispatch(storeSearchElement(e.target.value));
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
    }
  }
  
  doSorting(sortOn, type) {
    if(this.props.signal_search_element)
      this.props.history.push('/signals?search='+this.props.signal_search_element+'&sort='+ sortOn + '&type=' + type)
    else
      this.props.history.push('/signals?sort=' + sortOn + '&type=' + type);
    this.props.dispatch(showLoading());
    this.props.dispatch(storeSortElements(sortOn, type));
    this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
  }

  onChangeOfSearchBox(e) {
    if (e.target.value == "" || e.target.value == null) {
      this.props.dispatch(storeSearchElement(""));
      if(this.props.signal_sorton)
        this.props.history.push('/signals?sort=' + this.props.signal_sorton + '&type=' + this.props.signal_sorttype)
      else
        this.props.history.push('/signals');
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
    } else if (e.target.value.length > SEARCHCHARLIMIT) {
      if(this.props.signal_sorton)
        this.props.history.push('/signals?search='+e.target.value+'&sort=' + this.props.signal_sorton + '&type=' + this.props.signal_sorttype)
      else
        this.props.history.push('/signals?search=' + e.target.value + '')
      this.props.dispatch(storeSearchElement(e.target.value));
      this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
    }else{
      this.props.dispatch(storeSearchElement(e.target.value));
    }
  }

  clearSearchElement(){
    this.props.dispatch(storeSearchElement(""));
    if(this.props.signal_sorton)
      this.props.history.push('/signals?sort=' + this.props.signal_sorton + '&type=' + this.props.signal_sorttype)
    else
      this.props.history.push('/signals');
    this.props.dispatch(getList(getUserDetailsOrRestart.get().userToken, 1));
  }

  render() {
    document.body.className = "";
    if(!isEmpty(store.getState().signals.signalAnalysis) && $.isPlainObject(store.getState().signals.signalAnalysis)) {
      var viewed=store.getState().signals.signalAnalysisViewed;
      if(!viewed && viewed!="") {  
        let _link = "/signals/" + store.getState().signals.signalAnalysis.slug;
        return (<Redirect to={_link}/>);
      }
    }
    var data = this.props.signalList;
    const pages = store.getState().signals.signalList.total_number_of_pages;
    const current_page = store.getState().signals.signalList.current_page;
    let paginationTag = null;
    let storyList = null;
    if(pages>=1){
      paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
    }
    if(data){
      storyList = <SignalCard data={data}/>;
      return (
        <div className="side-body">
          <LatestSignals props={this.props}/>
          <div className="main-content">
            <div class="row">
              <div class="col-md-12">
                <div class="btn-toolbar pull-right">
                  <div class="input-group">
                    <div className="search-wrapper">
                      <input type="text" value={this.props.signal_search_element} name="search_signals" onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Search Signals" id="search_signals" className="form-control search-box" placeholder="Search signals..." required/>
                        <span className="fa fa-search form-control-feedback"></span>
                        <button className="close-icon" onClick={this.clearSearchElement.bind(this)} type="reset"></button>
                    </div>
                  </div>
                  <div class="btn-group">
                    <button type="button" title="Sorting" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                      <i class="glyphicon glyphicon-sort"></i>
                    </button>
                    <ul role="menu" class="dropdown-menu dropdown-menu-right">
                      <li>
                        <a href="#" onClick={this.doSorting.bind(this, 'name', 'asc')}>
                          <i class="fa fa-sort-alpha-asc"></i>&nbsp;&nbsp;Name Ascending
                        </a>
                      </li>
                      <li>
                        <a href="#" onClick={this.doSorting.bind(this, 'name', 'desc')}>
                          <i class="fa fa-sort-alpha-desc"></i>&nbsp;&nbsp;Name Descending
                        </a>
                      </li>
                      <li>
                        <a href="#" onClick={this.doSorting.bind(this, 'created_at', 'asc')}>
                        <i class="fa fa-long-arrow-down arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i>&nbsp;Date Ascending
                        </a>
                      </li>
                      <li>
                        <a href="#" onClick={this.doSorting.bind(this, 'created_at', 'desc')}>
                        <i class="fa fa-long-arrow-up arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i>&nbsp;Date Descending
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
				      </div>
            </div>
              {store.getState().datasets.paginationFlag &&
                <div className="main-content">
                  <div className="paginationFlg">
                    <img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
                  </div>
                </div>
              }
              {!store.getState().datasets.paginationFlag &&
                <div className="row">
                  {storyList}
                  <div className="clearfix"></div>
                </div>
              }
            <div className="ma-datatable-footer" id="idSignalPagination">
              <div className="dataTables_paginate">
                {paginationTag}
              </div>
            </div>
            <CreateSignalLoader history={this.props.history}/>
            <Share usersList={this.props.userList}/>
          </div>
        </div>
      );
    }else{
      return(
        <div className="side-body">
          <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
        </div>
      )
    }
  }
  componentWillUnmount(){
    this.props.dispatch(storeSearchElement(""));
    this.props.dispatch(storeSortElements(null,null));
    this.props.dispatch(clearSignalList())
  }
}
