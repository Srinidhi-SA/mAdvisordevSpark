import React from "react";
import store from "../../store";
import { connect } from "react-redux";
import { Pagination } from "react-bootstrap";
import {
    getAppsScoreList,
    updateScoreSlug,
    handleScoreRename,
    handleScoreDelete,
    storeScoreSearchElement,
    storeAppsScoreSortElements,
    getAppDetails,
    refreshAppsScoreList
} from "../../actions/appActions";
import { STATIC_URL } from "../../helpers/env.js"
import { SEARCHCHARLIMIT } from  "../../helpers/helper"
import Dialog from 'react-bootstrap-dialog'
import { ScoreCard }  from "./ScoreCard";
import { LatestScores } from "./LatestScores";
import { updateAnalystModeSelectedFlag } from "../../actions/appActions"
import { paginationFlag } from "../../actions/dataActions";
@connect((store) => {
  return {
    scoreList: store.apps.scoreList,
    score_search_element: store.apps.score_search_element,
    apps_score_sorton:store.apps.apps_score_sorton, 
    apps_score_sorttype:store.apps.apps_score_sorttype
  };
})

export class AppsScoreList extends React.Component {
  constructor(props) {
    super(props);
      this.handleSelect = this.handleSelect.bind(this);
  }

  componentWillMount() {
    if(this.props.match.path.includes("analyst")) {
      this.props.dispatch(updateAnalystModeSelectedFlag(true));
    }else{
      this.props.dispatch(updateAnalystModeSelectedFlag(false));
    } 
    var pageNo = 1;
    if(this.props.history.location.search!=""){
      let urlParams = new URLSearchParams(this.props.history.location.search);
      pageNo = (urlParams.get("page")!="")?urlParams.get("page"):pageNo
      let searchELem = (urlParams.get('search')!=null)?urlParams.get('search'):"";
      let sortELem = (urlParams.get('sort')!=null)?urlParams.get('sort'):"";
      let sortType = (urlParams.get('type')!=null)?urlParams.get('type'):"";
      this.props.dispatch(storeScoreSearchElement(searchELem));
      this.props.dispatch(storeAppsScoreSortElements(sortELem,sortType));
      this.props.dispatch(getAppsScoreList(pageNo));
    }else if(this.props.history.location.search.indexOf("page") != -1){
      pageNo = this.props.history.location.search.split("page=")[1];
    }
    if(store.getState().apps.currentAppId == ""){
      this.props.dispatch(getAppDetails(this.props.match.params.AppId,pageNo));
    }else{
      this.props.dispatch(getAppsScoreList(pageNo));
    }
  }
  componentDidMount(){
    this.props.dispatch(refreshAppsScoreList(this.props));
  }
  getScoreSummary(slug) {
    this.props.dispatch(updateScoreSlug(slug))
  }
  handleScoreDelete(slug) {
    this.props.dispatch(handleScoreDelete(slug, this.refs.dialog));
  }
  handleScoreRename(slug, name) {
    this.props.dispatch(handleScoreRename(slug, this.refs.dialog, name));
  }
  
  _handleKeyPress = (e) => {
    var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
    if (e.key === 'Enter') {
      if(e.target.value != "" && e.target.value != null){
        if(this.props.apps_score_sorton!="" && this.props.apps_score_sorton!=null && this.props.apps_score_sorttype!=null){
          this.props.history.push('/apps/' + this.props.match.params.AppId + modeSelected + '/scores?search=' + e.target.value+''+'&sort=' + this.props.apps_score_sorton + '&type='+this.props.apps_score_sorttype)
        }else{
          this.props.history.push('/apps/'+this.props.match.params.AppId+modeSelected+'/scores?search=' + e.target.value + '')
        }
      }
      this.props.dispatch(storeScoreSearchElement(e.target.value));
      this.props.dispatch(getAppsScoreList(1));
    }
  }
  
  onChangeOfSearchBox(e) {
    var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
    if (e.target.value == "" || e.target.value == null) {
      this.props.dispatch(storeScoreSearchElement(""));
      this.props.dispatch(getAppsScoreList(1));
      this.props.history.push('/apps/' + this.props.match.params.AppId + modeSelected + '/scores'+ '')
    } else if (e.target.value.length > SEARCHCHARLIMIT) {
      if(this.props.apps_score_sorton!="" && this.props.apps_score_sorton!=null && this.props.apps_score_sorttype!=null){
        this.props.history.push('/apps/' + this.props.match.params.AppId + modeSelected + '/scores?search=' + e.target.value+''+'&sort=' + this.props.apps_score_sorton + '&type='+this.props.apps_score_sorttype)
      }else{
        this.props.history.push('/apps/' + this.props.match.params.AppId + modeSelected + '/scores?search=' + e.target.value+'')
      }
      this.props.dispatch(storeScoreSearchElement(e.target.value));
      this.props.dispatch(getAppsScoreList(1));
    } else{
      this.props.dispatch(storeScoreSearchElement(e.target.value));
    }
  }
    
  doSorting(sortOn, type){
    var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
    if(this.props.score_search_element!=""){
    this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/scores?search='+this.props.score_search_element+'&sort=' + sortOn + '&type='+type);
    }else{
      this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/scores?sort=' + sortOn + '&type='+type);
    }
    this.props.dispatch(storeAppsScoreSortElements(sortOn,type));
    this.props.dispatch(getAppsScoreList(1));
  }
     
  render() {
    const scoreList = store.getState().apps.scoreList.data;
    var appsScoreList = null;
    if(scoreList) {
      const pages = store.getState().apps.scoreList.total_number_of_pages;
      let current_page = store.getState().apps.current_page;
      let paginationTag = null
      if (pages > 1) {
        paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
      }
      appsScoreList = <ScoreCard match = {this.props.match} data={scoreList} />
      return (
        <div>
          <LatestScores props={this.props}/>
          <div className="main-content">
            <div className="row">
              <div className="col-md-8"></div>
              <div className="col-md-4">
        				<div class="btn-toolbar pull-right">
                  <div className="input-group">
      							<div className="search-wrapper">
			      					<input type="text" name="score_insights" value={this.props.score_search_element} onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Score Insights" id="score_insights" className="form-control search-box"  placeholder="Search Score insights... " required />
						      		<span className="zmdi zmdi-search form-control-feedback"></span>
								      <button className="close-icon" type="reset" onClick={this.clearSearchElement.bind(this)}></button>
							      </div>							
				          </div>
                  <div className="btn-group">
                    <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false">
                      <i className="zmdi zmdi-hc-lg zmdi-sort-asc"></i>
                    </button>
                    <ul role="menu" className="dropdown-menu dropdown-menu-right">
                      <li>
                        <a href="javascript:;" onClick={this.doSorting.bind(this,'name','asc')}><i class="zmdi zmdi-sort-amount-asc"></i> Name Ascending</a>
                      </li>
                      <li>
                        <a href="javascript:;" onClick={this.doSorting.bind(this,'name','desc')}><i class="zmdi zmdi-sort-amount-desc"></i> Name Descending</a>
                      </li>
                      <li>
                        <a href="javascript:;" onClick={this.doSorting.bind(this,'created_at','asc')}><i class="zmdi zmdi-calendar-alt"></i> Date Ascending</a>
                      </li>
                      <li>
                        <a href="javascript:;" onClick={this.doSorting.bind(this,'created_at','desc')}><i class="zmdi zmdi-calendar"></i> Date Descending</a>
                      </li>
                    </ul>
                  </div>
                </div>			
              </div>
            </div>          
            <div class="clearfix xs-m-10"></div>
            {store.getState().datasets.paginationFlag &&
              <div className="paginationFlg">
                <img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
              </div>
            }
            {!store.getState().datasets.paginationFlag &&
              <div className="row">
                {appsScoreList}
                <div className="clearfix"></div>
              </div>
            }
            <div className="ma-datatable-footer" id="idPagination">
              <div className="dataTables_paginate">
                {paginationTag}
              </div>
            </div>
          </div>	
        <Dialog ref="dialog"/>
        </div>
      );
    }else {
      return (
        <div>
          <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
        </div>
      )
    }
  }
  
  handleSelect(eventKey) {
    this.props.dispatch(paginationFlag(true))
    var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
    if(this.props.score_search_element!="" && this.props.apps_score_sorton!="" && this.props.score_search_element!=null && this.props.apps_score_sorton!=null){
      this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/scores?search=' + this.props.score_search_element + '&sort=' + this.props.apps_score_sorton +'&type='+this.props.apps_score_sorttype+ '?page=' + eventKey + '')
    }else if ((this.props.score_search_element!="" && this.props.score_search_element!=null) && (this.props.apps_score_sorton==="" || this.props.apps_score_sorton===null)) {
      this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/scores?search=' + this.props.score_search_element + '?page=' + eventKey + '')
    }else if((this.props.score_search_element==="" || this.props.score_search_element===null) && (this.props.apps_score_sorton!=""&&this.props.apps_score_sorton!=null)){
      this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/scores?sort=' + this.props.apps_score_sorton +'&type='+this.props.apps_score_sorttype+'&page=' + eventKey + '');
    }else
      this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/scores?page=' + eventKey + '')
      this.props.dispatch(getAppsScoreList(eventKey));
    }

    clearSearchElement(e){
      var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
      this.props.dispatch(storeScoreSearchElement(""));
      if(this.props.apps_score_sorton)
        this.props.history.push('/apps/'+this.props.match.params.AppId+modeSelected +'/scores?sort=' + this.props.apps_score_sorton +'&type='+this.props.apps_score_sorttype);
      else
        this.props.history.push('/apps/'+this.props.match.params.AppId+modeSelected +'/scores');
      this.props.dispatch(getAppsScoreList(1));
    }

    componentWillUnmount(){
      this.props.dispatch(storeScoreSearchElement(""));
      this.props.dispatch(storeAppsScoreSortElements("",""))
    }
}
