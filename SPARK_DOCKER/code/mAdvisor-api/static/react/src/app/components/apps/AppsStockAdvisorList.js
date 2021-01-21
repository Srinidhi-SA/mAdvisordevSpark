import React from "react";
import {Pagination} from "react-bootstrap";
import {Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {SEARCHCHARLIMIT} from "../../helpers/helper.js"
import {getAppsStockList,storeStockModelSearchElement,storeStockAppsModelSortElements,refreshStockAppsList,clearDataPreview,getAllStockAnalysisList} from "../../actions/appActions";
import Dialog from 'react-bootstrap-dialog'
import {STATIC_URL} from "../../helpers/env.js";
import {AppsLoader} from "../common/AppsLoader";
import {StocksCard} from "./StocksCard";
import {LatestStocks} from "./LatestStocks";
import { paginationFlag } from "../../actions/dataActions";


@connect((store) => {
	return {
		stockList: store.apps.stockAnalysisList,
		stockAnalysisFlag:store.apps.stockAnalysisFlag,
		stockSlug:store.apps.stockSlug,
		signal: store.signals.signalAnalysis,
		stock_model_search_element: store.apps.stock_model_search_element,
		stock_apps_model_sorton:store.apps.stock_apps_model_sorton,
		stock_apps_model_sorttype:store.apps.stock_apps_model_sorttype
	};
})

export class AppsStockAdvisorList extends React.Component {
	constructor(props) {
		super(props);
		this.state={
			showLoader : false
		}
		this.callShowloader = this.callShowloader.bind(this);
	}
	componentWillMount(){
		this.props.dispatch(clearDataPreview());
		this.props.dispatch(getAllStockAnalysisList());
		var pageNo = 1;
		if(this.props.history.location.search!=""){
      let urlParams = new URLSearchParams(this.props.history.location.search);
      pageNo = (urlParams.get("page")!="")?urlParams.get("page"):pageNo
      let searchELem = (urlParams.get('search')!=null)?urlParams.get('search'):"";
      let sortELem = (urlParams.get('sort')!=null)?urlParams.get('sort'):"";
      let sortType = (urlParams.get('type')!=null)?urlParams.get('type'):"";
      this.props.dispatch(storeStockModelSearchElement(searchELem));
      this.props.dispatch(storeStockAppsModelSortElements(sortELem,sortType));
      this.props.dispatch(getAppsStockList(pageNo));
    }else if(this.props.history.location.search.indexOf("page") != -1){
			pageNo = this.props.history.location.search.split("page=")[1];
			this.props.dispatch(getAppsStockList(pageNo));
		}else{
			this.props.dispatch(getAppsStockList(pageNo));
		}
	}
	componentDidMount(){
		window.scrollTo(0, 0);
		this.props.dispatch(refreshStockAppsList(this.props));
		this.setState({showloader:false})
	}
	callShowloader(){
		this.setState({showLoader:true});
	}
	_handleKeyPress = (e) => {
		if (e.key === 'Enter') {
			if (e.target.value != "" && e.target.value != null)
				this.props.history.push('apps-stock-advisor?search=' + e.target.value + '');
			this.props.dispatch(storeStockModelSearchElement(e.target.value));
			this.props.dispatch(getAppsStockList(1));
		}
	}
	doSorting(sortOn, type){
		if(this.props.stock_model_search_element!="" && this.props.stock_model_search_element!=null){
			this.props.history.push('apps-stock-advisor?search=' + this.props.stock_model_search_element + '&sort=' + sortOn + '&type='+type+'')
		}else{
			this.props.history.push('apps-stock-advisor?sort=' + sortOn + '&type='+type);
		}
		this.props.dispatch(storeStockAppsModelSortElements(sortOn,type));
		this.props.dispatch(getAppsStockList(1));
	}
	onChangeOfSearchBox(e){
		if(e.target.value==""||e.target.value==null){
			this.props.dispatch(storeStockModelSearchElement(""));
			this.props.history.push('apps-stock-advisor'+'')
			this.props.dispatch(getAppsStockList(1));
		}else if (e.target.value.length > SEARCHCHARLIMIT) {
			if(this.props.stock_apps_model_sorton!="" && this.props.stock_apps_model_sorton!=null){
				this.props.history.push('apps-stock-advisor?search=' + e.target.value + '&sort=' + this.props.stock_apps_model_sorton + '&type='+this.props.stock_apps_model_sorttype+ '')
			}else{
				this.props.history.push('apps-stock-advisor?search=' + e.target.value + '')
			}
			this.props.dispatch(storeStockModelSearchElement(e.target.value));
			this.props.dispatch(getAppsStockList(1));
		}else{
			this.props.dispatch(storeStockModelSearchElement(e.target.value));
		}
	}

	render() {
		if (store.getState().datasets.dataPreviewFlag){
			let _link = "/apps-stock-advisor-analyze/data/" + store.getState().datasets.selectedDataSet;
			return (<Redirect to={_link}/>);
		}
		if(this.props.stockAnalysisFlag){
			let _linkAnalysis = "/apps-stock-advisor/"+this.props.stockSlug+"/"+this.props.signal.listOfNodes[0].slug;
			return (<Redirect to={_linkAnalysis}/>);
		}
	
		const stockAnalysisList = this.props.stockList.data;
		if (stockAnalysisList) {
			const pages = this.props.stockList.total_number_of_pages;
			const current_page = this.props.stockList.current_page;
			let paginationTag = null;	
			if (pages >= 1) {
				paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect.bind(this)} first last next prev boundaryLinks items={pages} activePage={current_page}/>
			}
			var stockList = <StocksCard data={stockAnalysisList} loadfunc={this.callShowloader}/>;
			const {showLoader} = this.state;
			if(showLoader) {
				return (
					<img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
				);
			}
			else{
				return (
					<div className="side-body">
						<LatestStocks props={this.props} loadfunc={this.callShowloader}/>
						<div class="main-content">
							<div class="row">
								<div class="col-md-12">
									<div class="btn-toolbar pull-right">
          		      <div class="input-group">
              			  <div className="search-wrapper">
                    		<input type="text" name="search_stock" value={this.props.stock_model_search_element} onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Search Stock" id="search_stock" className="form-control search-box" placeholder="Search Stock Analysis..." required />
                    		<span className="zmdi zmdi-search form-control-feedback"></span>
                    		<button className="close-icon" type="reset" onClick={this.clearSearchElement.bind(this)}></button>
                			</div>
                		</div>
                  	<div class="btn-group">
                    	<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><i class="zmdi zmdi-hc-lg zmdi-sort-asc"></i> </button>
                    	<ul role="menu" class="dropdown-menu dropdown-menu-right">
                        <li>
                          <a href="#" onClick={this.doSorting.bind(this,'name','asc')}><i class="zmdi zmdi-sort-amount-asc"></i> Name Ascending</a>
                        </li>
                        <li>
                          <a href="#" onClick={this.doSorting.bind(this,'name','desc')}><i class="zmdi zmdi-sort-amount-desc"></i> Name Descending</a>
                        </li>
                        <li>
                          <a href="#" onClick={this.doSorting.bind(this,'created_at','asc')}><i class="zmdi zmdi-calendar-alt"></i> Date Ascending</a>
                        </li>
                        <li>
                          <a href="#" onClick={this.doSorting.bind(this,'created_at','desc')}><i class="zmdi zmdi-calendar"></i> Date Descending</a>
                        </li>
                      </ul>
                  </div>
                </div>
							</div>
						<div class="clearfix"></div>
						</div>
						<div class="clearfix xs-m-10"></div>
						{store.getState().datasets.paginationFlag &&
							<div className="paginationFlg">
								<img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
							</div>
						}
						{!store.getState().datasets.paginationFlag &&
							<div className="row">
								{stockList}
								<div className="clearfix"></div>
							</div>
						}
						<div className="ma-datatable-footer" id="idPagination">
							<div className="dataTables_paginate">
								{paginationTag}
							</div>
						</div>
						<AppsLoader match={this.props.match}/>
						<Dialog ref="dialog"/>
						</div>
					</div>
				);
			}
		} else {
			return (
				<div>
					<img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
					<Dialog ref="dialog"/>
				</div>
			)
		}
	}

	handleSelect(eventKey) {
		this.props.dispatch(paginationFlag(true))
		if(this.props.stock_model_search_element!="" && this.props.stock_model_search_element!=null && this.props.stock_apps_model_sorton!=""){
			this.props.history.push('/apps-stock-advisor?search=' + this.props.stock_model_search_element+'&sort=' + this.props.stock_apps_model_sorton +'&type='+this.props.stock_apps_model_sorton+'&page=' + eventKey + '');
		}else if(this.props.stock_model_search_element && (this.props.stock_apps_model_sorton==="" || this.props.stock_apps_model_sorton===null)) {
			this.props.history.push('/apps-stock-advisor?search=' + this.props.stock_model_search_element+'?page='+eventKey+'')
		}else if(this.props.stock_apps_model_sorton && (this.props.stock_model_search_element===null || this.props.stock_model_search_element==="")){
			this.props.history.push('/apps-stock-advisor?sort=' + this.props.stock_apps_model_sorton +'&type='+this.props.stock_apps_model_sorton+'&page=' + eventKey + '');
		}else{
			this.props.history.push('/apps-stock-advisor?page='+eventKey+'')
		}
		this.props.dispatch(getAppsStockList(eventKey));
	}
	clearSearchElement(e){
		this.props.dispatch(storeStockModelSearchElement(""));
		if(this.props.stock_apps_model_sorton){
			this.props.history.push('/apps-stock-advisor?sort=' + this.props.stock_apps_model_sorton +'&type='+this.props.stock_apps_model_sorttype);
		}else{
			this.props.history.push('/apps-stock-advisor');
		}
		this.props.dispatch(getAppsStockList(1));
	}

	componentWillUnmount(){
		this.props.dispatch(storeStockModelSearchElement(""));
		this.props.dispatch(storeStockAppsModelSortElements("",""));
	}
}
