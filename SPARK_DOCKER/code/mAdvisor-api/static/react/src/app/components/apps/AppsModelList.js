import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Link, Redirect} from "react-router-dom";
import {push} from "react-router-redux";

import {MainHeader} from "../common/MainHeader";
import {Tabs,Tab,Pagination,Tooltip,OverlayTrigger,Popover} from "react-bootstrap";
import {AppsCreateModel} from "./AppsCreateModel";
import {getAppsModelList,updateModelSlug,
    updateModelSummaryFlag,handleModelDelete,handleModelRename,storeModelSearchElement,storeAppsModelSortElements,getAppDetails,refreshAppsModelList,getAllModelList,storeAppsModelFilterElement, clearAppsAlgoList} from "../../actions/appActions";
import {paginationFlag, updateSelectedVariablesAction} from "../../actions/dataActions";
import {DetailOverlay} from "../common/DetailOverlay";
import {SEARCHCHARLIMIT,getUserDetailsOrRestart} from  "../../helpers/helper"
import {STATIC_URL} from "../../helpers/env.js";
import Dialog from 'react-bootstrap-dialog'
import {DataUploadLoader} from "../common/DataUploadLoader";
import {ModelsCard} from "./ModelsCard";
import {LatestModels} from "./LatestModels";
var dateFormat = require('dateformat');
    
    
    @connect((store) => {
        return {login_response: store.login.login_response,
            modelList: store.apps.modelList,
            algoList: store.apps.algoList,
            modelSummaryFlag:store.apps.modelSummaryFlag,
            modelSlug:store.apps.modelSlug,
            currentAppId:store.apps.currentAppId,
            model_search_element: store.apps.model_search_element,
            apps_model_sorton:store.apps.apps_model_sorton,
            apps_model_sorttype:store.apps.apps_model_sorttype,
            mode_filter_by:store.apps.filter_models_by_mode
        };
    })
    
    export class AppsModelList extends React.Component {
        constructor(props) {
            super(props);
            this.handleSelect = this.handleSelect.bind(this);
        }
        componentWillMount() {
            var pageNo = 1;
            if(this.props.history.location.search!=""){
                let urlParams = new URLSearchParams(this.props.history.location.search);
                pageNo = (urlParams.get("page")!="")?urlParams.get("page"):pageNo
                let searchELem = (urlParams.get('search')!=null)?urlParams.get('search'):"";
                let sortELem = (urlParams.get('sort')!=null)?urlParams.get('sort'):"";
                let sortType = (urlParams.get('type')!=null)?urlParams.get('type'):"";
                this.props.dispatch(storeModelSearchElement(searchELem));
                this.props.dispatch(storeAppsModelSortElements(sortELem,sortType));
                this.props.dispatch(getAppsModelList(pageNo));
            }else if(this.props.history.location.search.indexOf("page") != -1){
                pageNo = this.props.history.location.search.split("page=")[1];
            }
            if(store.getState().apps.currentAppId == ""){
                this.props.dispatch(getAppDetails(this.props.match.params.AppId,pageNo));
            }else{
                this.props.dispatch(getAppsModelList(pageNo));
            }
            this.props.dispatch(clearAppsAlgoList())
            this.props.dispatch(updateModelSummaryFlag(false));
            this.props.dispatch(updateSelectedVariablesAction(false));
        }
        componentDidMount(){
            this.props.dispatch(refreshAppsModelList(this.props));
           this.props.dispatch(getAllModelList(store.getState().apps.currentAppId));
           this.props.dispatch(storeModelSearchElement(""));
            this.props.dispatch(storeAppsModelSortElements("",""));
            this.props.dispatch(storeAppsModelFilterElement(""));
        }
        getModelSummary(slug){
            this.props.dispatch(updateModelSlug(slug))
        }
        handleModelDelete(slug){
            this.props.dispatch(handleModelDelete(slug,this.refs.dialog));
        }
        handleModelRename(slug,name){
            this.props.dispatch(handleModelRename(slug,this.refs.dialog,name));
        }
        _handleKeyPress = (e) => {
            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
            if (e.key === 'Enter') {
                if (e.target.value != "" && e.target.value != null)
                    this.props.history.push('/apps/'+this.props.match.params.AppId+modeSelected+'/models?search=' + e.target.value + '')
                    this.props.dispatch(storeModelSearchElement(e.target.value));
                this.props.dispatch(getAppsModelList(1));
                
            }
        }
        onChangeOfSearchBox(e){
            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';

            if(e.target.value==""||e.target.value==null){
                this.props.dispatch(storeModelSearchElement(""));
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models'+'')
                this.props.dispatch(getAppsModelList(1));
                
            }else if (e.target.value.length > SEARCHCHARLIMIT) {
                if($(".mode_filter").val()!=""&& $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?mode='+$(".mode_filter").val()+'/&search=' + e.target.value + '')
                }
                else{
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?search=' + e.target.value + '')

                }
                this.props.dispatch(storeModelSearchElement(e.target.value));
                this.props.dispatch(getAppsModelList(1));
            }
            else{
                this.props.dispatch(storeModelSearchElement(e.target.value));
            }
        }
        
        doSorting(sortOn, type){
            this.props.dispatch(storeModelSearchElement(""));
            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
            if($(".mode_filter").val()!=""&& $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/models?mode=' + $(".mode_filter").val() + '/models?sort=' + sortOn + '&type='+type);
            }
             else{
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/models?sort=' + sortOn + '&type='+type);
            }
            this.props.dispatch(storeAppsModelSortElements(sortOn,type));
            this.props.dispatch(getAppsModelList(1));
        }
        filterByMode(){

            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML';
            
            this.props.dispatch(storeAppsModelFilterElement($(".mode_filter").val()));
            if(this.props.model_search_element && $(".mode_filter").val()!="" && $(".mode_filter").val()!=null &&this.props.mode_filter_by != null){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?mode=' + $(".mode_filter").val() +'/models?search=' + this.props.model_search_element + '')
            }
            else if($(".mode_filter").val()!="" && $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/models?mode=' + $(".mode_filter").val());
            }
            else if($(".mode_filter").val()==""&& this.props.model_search_element){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/models?search=' + this.props.model_search_element + '');
            }
            else{
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected+'/models');
            }
            this.props.dispatch(getAppsModelList(1));    
        }
       
        render() {
           const modelList = store.getState().apps.modelList.data;
            const algoList = store.getState().apps.algoList;
            var createModelPermission = store.getState().apps.modelList.permission_details;
            let appsModelList = null;
            if (modelList) {
                const pages = store.getState().apps.modelList.total_number_of_pages;
                const current_page = store.getState().apps.current_page;
                
                let paginationTag = null
                if(pages > 1){
                    paginationTag = <Pagination  ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
                }
                appsModelList = <ModelsCard match={this.props.match} data={modelList}/>;
                return (
                        <div>
                        <LatestModels props={this.props} permissions={createModelPermission}/>
                        <div className="main-content">
                        <div className="row">
                        <div className="col-md-6">

                        <select defaultValue="filterByMode" className="mode_filter form-control" style={{"width":"35%"}} id="filterby" title="Filter By Mode" onChange={this.filterByMode.bind(this)}>
                        <option value="filterByMode" disabled>Filter By Mode</option>
                        <option value="">All</option>
                        <option value="analyst">Analyst</option>
                        <option value="autoML">Auto ML</option>
                        </select>
                        
                        </div>
                        <div className="col-md-6">
                        <div className="btn-toolbar pull-right">
                        <div className="input-group">
                        
                        {/*<input type="text" name="model_insights" onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Model Insights" id="model_insights" className="form-control" placeholder="Search Model insights..."/>*/}
                        
                        <div className="search-wrapper">
                        <input type="text" name="model_insights" defaultValue={this.props.model_search_element} onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Model Insights" id="model_insights" className="form-control search-box" placeholder="Search Model insights..." required />
                        <span className="zmdi zmdi-search form-control-feedback"></span>
                        <button className="close-icon" type="reset" onClick={this.clearSearchElement.bind(this)}></button>
                        </div>
                        
                        </div>
                        <div className="btn-group">
                        {/*<button type="button" className="btn btn-default" title="Select All Card">
											<i className="fa fa-address-card-o fa-lg"></i>
										</button>*/}
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
                        {
                            store.getState().datasets.paginationFlag &&
                            <div className="paginationFlg">
                              <img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
                            </div>
                        }
                        {
                            !store.getState().datasets.paginationFlag &&
                            <div className="row">
                            {appsModelList}
                            <div className="clearfix"></div>
                            </div>
                        }
                        <div className="ma-datatable-footer"  id="idPagination">
                        <div className="dataTables_paginate">
                        {paginationTag}
                        </div>
                        </div>
                        </div>
                        <Dialog ref="dialog" />
                            <DataUploadLoader/>
                        </div>
                        
                );
            }else {
                return (
                        <div>
                        <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif"} />
                        </div>
                )
            }
        }
        handleSelect(eventKey) {
            this.props.dispatch(paginationFlag(true))
            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
            if (this.props.model_search_element) {
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?search=' + this.props.model_search_element+'&page='+eventKey+'')
            }  else if(this.props.apps_model_sorton){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?sort=' + this.props.apps_model_sorton +'&type='+this.props.apps_model_sorttype+'&page=' + eventKey + '');
            }else if(this.props.mode_filter_by!="" && this.props.mode_filter_by!=null){
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?filllter=' + this.props.mode_filter_by +'&type='+this.props.apps_model_sorttype+'&page=' + eventKey + '');
            }else
                this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?page='+eventKey+'')
                this.props.dispatch(getAppsModelList(eventKey));
        }
        clearSearchElement(e){
            this.props.dispatch(storeModelSearchElement(""));
            this.props.dispatch(storeAppsModelSortElements("",""));

            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
            if(this.props.mode_filter_by!="" && this.props.mode_filter_by!=null)
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?mode='+ this.props.mode_filter_by);
            else if(this.props.apps_model_sorton)
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models?sort='+ this.props.apps_model_sorton +'&type='+this.props.apps_model_sorttype);
            else
            this.props.history.push('/apps/'+this.props.match.params.AppId+ modeSelected +'/models');
            this.props.dispatch(getAppsModelList(1));
        }

        componentWillUnmount(){
            this.props.dispatch(storeModelSearchElement(""));
            this.props.dispatch(storeAppsModelSortElements("",""));
            this.props.dispatch(storeAppsModelFilterElement(""))
        }
    }
