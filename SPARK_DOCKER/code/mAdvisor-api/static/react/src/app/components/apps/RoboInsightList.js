import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";

import {Pagination} from "react-bootstrap";
import {getAppsRoboList, getRoboDataset, handleInsightDelete, handleInsightRename, storeRoboSearchElement,clearRoboSummary,storeRoboSortElements,refreshRoboInsightsList} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js";
import {RoboDataUpload} from "./RoboDataUpload";
import {AppsLoader} from "../common/AppsLoader";
import Dialog from 'react-bootstrap-dialog'
import {SEARCHCHARLIMIT} from "../../helpers/helper";
import {RoboInsightCard} from "./RoboInsightCard";
import {LatestRoboInsights} from "./LatestRoboInsights";

@connect((store) => {
  return {
    login_response: store.login.login_response,
    roboList: store.apps.roboList,
    currentAppId: store.apps.currentAppId,
    showRoboDataUploadPreview: store.apps.showRoboDataUploadPreview,
    roboDatasetSlug: store.apps.roboDatasetSlug,
    roboSummary: store.apps.roboSummary,
    dataPreviewFlag: store.datasets.dataPreviewFlag,
    robo_search_element: store.apps.robo_search_element,
    customerDataset_slug:store.apps.customerDataset_slug,
	historialDataset_slug:store.apps.historialDataset_slug,
	externalDataset_slug:store.apps.externalDataset_slug,
	robo_sorton:store.apps.robo_sorton,
	robo_sorttype:store.apps.robo_sorttype
  };
})

export class RoboInsightList extends React.Component {
  constructor(props) {
    super(props);
    this.handleSelect = this.handleSelect.bind(this);
  }
  componentWillMount() {
    var pageNo = 1;
    if (this.props.history.location.search.indexOf("page") != -1) {
      pageNo = this.props.history.location.search.split("page=")[1];
      this.props.dispatch(getAppsRoboList(pageNo));
    } else
      this.props.dispatch(getAppsRoboList(pageNo));
    }
  getInsightPreview(slug) {
	this.props.dispatch(clearRoboSummary());
    this.props.dispatch(getRoboDataset(slug));
  }
  handleInsightRename(slug, name) {
    this.props.dispatch(handleInsightRename(slug, this.refs.dialog, name))
  }
  handleInsightDelete(slug) {
    this.props.dispatch(handleInsightDelete(slug, this.refs.dialog))
  }
  _handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (e.target.value != "" && e.target.value != null)
        this.props.history.push('/apps-robo?search=' + e.target.value + '')

      this.props.dispatch(storeRoboSearchElement(e.target.value));
      this.props.dispatch(getAppsRoboList(1));

    }
  }
  componentDidMount(){
      this.props.dispatch(refreshRoboInsightsList());
  }
  onChangeOfSearchBox(e) {
    if (e.target.value == "" || e.target.value == null) {
      this.props.dispatch(storeRoboSearchElement(""));
      this.props.dispatch(getAppsRoboList(1));
      this.props.history.push('/apps-robo')

    } else if (e.target.value.length > SEARCHCHARLIMIT) {
      this.props.history.push('/apps-robo?search=' + e.target.value + '')
      this.props.dispatch(storeRoboSearchElement(e.target.value));
      this.props.dispatch(getAppsRoboList(1));
    }else{
        this.props.dispatch(storeRoboSearchElement(e.target.value));
    }
  }

    doSorting(sortOn, type){
        this.props.history.push('/apps-robo?sort=' + sortOn + '&type='+type);
        this.props.dispatch(storeRoboSortElements(sortOn,type));
        this.props.dispatch(getAppsRoboList(1));
  }
  render() {
    if (this.props.dataPreviewFlag) {
      let _link = "/apps-robo-list/" + store.getState().apps.roboDatasetSlug+"/customer/data/"+store.getState().apps.customerDataset_slug
      return (<Redirect to={_link}/>);
    }

    const roboList = store.getState().apps.roboList.data;
    if (roboList) {
      const pages = store.getState().apps.roboList.total_number_of_pages;
      const current_page = store.getState().apps.current_page;
      let addButton = null;
      let paginationTag = null;
      const appsRoboList = <RoboInsightCard data={roboList} />;
      if (current_page == 1 || current_page == 0) {
        addButton = <RoboDataUpload match={this.props.match}/>
      }
      if (pages > 1) {
        paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
      }
      
      return (
        <div className="side-body">
        <LatestRoboInsights props={this.props}/>
          <div className="main-content">
            <div class="row">
              <div className="col-md-12">
                <div class="btn-toolbar pull-right">				
				<div className="input-group">
				
				<div className="input-group">
					<div className="search-wrapper">
						<input type="text" name="robo_insights" value={this.props.robo_search_element} onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Robo Insights" id="robo_insights" className="form-control search-box"  placeholder="Search robo insights..." required />
						<span className="fa fa-search form-control-feedback"></span>
						<button className="close-icon" type="reset" onClick={this.clearSearchElement.bind(this)}></button>
					</div>
				</div>
				</div>
				
				<div className="btn-group">
                    <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false">
                    <i className="glyphicon glyphicon-sort"></i>
                    </button>
                    <ul role="menu" className="dropdown-menu dropdown-menu-right">
                    <li>
                    <a href="javascript:;" onClick={this.doSorting.bind(this,'name','asc')}><i class="fa fa-sort-alpha-asc"></i> Name Ascending</a>
                    </li>
                    <li>
                    <a href="javascript:;" onClick={this.doSorting.bind(this,'name','desc')}><i class="fa fa-sort-alpha-desc"></i> Name Descending</a>
                    </li>
                    <li>
                    <a href="javascript:;" onClick={this.doSorting.bind(this,'created_at','asc')}><i class="fa fa-long-arrow-down arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i> Date Ascending</a>
                    </li>
                    <li>
                    <a href="javascript:;" onClick={this.doSorting.bind(this,'created_at','desc')}><i class="fa fa-long-arrow-up arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i> Date Descending</a>
                    </li>
                    </ul>
                </div>				
			  </div>
              </div>
            </div>
			<div class="clearfix xs-m-10"></div>
            <div className="row">
             {appsRoboList}
              <div className="clearfix"></div>
            </div>
            <div className="ma-datatable-footer" id="idPagination">
              <div className="dataTables_paginate">
                {paginationTag}
              </div>
            </div>
          </div>
          <AppsLoader match={this.props.match}/>
          <Dialog ref="dialog"/>
        </div>

      );
    } else {
      return (
        <div>
          <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
        </div>
      )
    }
  }
  handleSelect(eventKey) {
    if (this.props.robo_search_element) {
      this.props.history.push('/apps-robo?search=' + this.props.robo_search_element + '?page=' + eventKey + '')
    } else if(this.props.robo_sorton){
	     this.props.history.push('/apps-robo?sort=' + this.props.robo_sorton +'&type='+this.props.robo_sorttype+'&page=' + eventKey + '');
	}else
      this.props.history.push('/apps-robo?page=' + eventKey + '')

    this.props.dispatch(getAppsRoboList(eventKey));
  }
  clearSearchElement(e){
      this.props.dispatch(storeRoboSearchElement(""));
      if(this.props.robo_sorton)
      this.props.history.push('/apps-robo?sort=' + this.props.robo_sorton +'&type='+this.props.robo_sorttype);
      else
      this.props.history.push('/apps-robo');
      this.props.dispatch(getAppsRoboList(1));
  }
}
