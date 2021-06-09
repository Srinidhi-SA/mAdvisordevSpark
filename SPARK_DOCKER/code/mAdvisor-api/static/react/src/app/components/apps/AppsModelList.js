import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Pagination} from "react-bootstrap";
import {getAppsModelList,updateModelSlug,updateModelSummaryFlag,handleModelDelete,handleModelRename,storeModelSearchElement,
    storeAppsModelSortElements,getAppDetails,refreshAppsModelList,getAllModelList,storeAppsModelFilterElement,clearAppsAlgoList,clearModelList
} from "../../actions/appActions";
import {paginationFlag, updateSelectedVariablesAction} from "../../actions/dataActions";
import {SEARCHCHARLIMIT} from  "../../helpers/helper"
import {STATIC_URL} from "../../helpers/env.js";
import Dialog from 'react-bootstrap-dialog'
import {DataUploadLoader} from "../common/DataUploadLoader";
import {ModelsCard} from "./ModelsCard";
import {LatestModels} from "./LatestModels";  

@connect((store) => {
    return {
        modelList: store.apps.modelList,
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
    }
    componentWillMount() {
        this.props.dispatch(clearModelList());
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
        if (e.key === 'Enter') {
            if (e.target.value != "" && e.target.value != null)
                this.props.history.push(this.props.match.url+'?search=' + e.target.value + '')
            this.props.dispatch(storeModelSearchElement(e.target.value));
            this.props.dispatch(getAppsModelList(1));
        }
    }
    onChangeOfSearchBox(e){
        if(e.target.value==""||e.target.value==null){
            this.props.dispatch(storeModelSearchElement(""));
            this.props.history.push(this.props.match.url)
            this.props.dispatch(getAppsModelList(1));            
        }else if (e.target.value.length > SEARCHCHARLIMIT) {
            if($(".mode_filter").val()!=""&& $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
                this.props.history.push(this.props.match.url+'?mode='+$(".mode_filter").val()+'/&search=' + e.target.value + '')
            }
            else{
                this.props.history.push(this.props.match.url+'?search=' + e.target.value + '')
            }
            this.props.dispatch(storeModelSearchElement(e.target.value));
            this.props.dispatch(getAppsModelList(1));
        }else{
            this.props.dispatch(storeModelSearchElement(e.target.value));
        }
    }
        
    doSorting(sortOn, type){
        this.props.dispatch(storeModelSearchElement(""));
        if($(".mode_filter").val()!=""&& $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
            this.props.history.push(this.props.match.url+'?mode=' + $(".mode_filter").val() + '/models?sort=' + sortOn + '&type='+type);
        }else{
            this.props.history.push(this.props.match.url+'?sort=' + sortOn + '&type='+type);
        }
        this.props.dispatch(storeAppsModelSortElements(sortOn,type));
        this.props.dispatch(getAppsModelList(1));
    }
    filterByMode(){
        this.props.dispatch(storeAppsModelFilterElement($(".mode_filter").val()));
        if(this.props.model_search_element && $(".mode_filter").val()!="" && $(".mode_filter").val()!=null &&this.props.mode_filter_by != null){
            this.props.history.push(this.props.match.url+'?mode=' + $(".mode_filter").val() +'/models?search=' + this.props.model_search_element + '')
        }else if($(".mode_filter").val()!="" && $(".mode_filter").val()!=null && this.props.mode_filter_by != null){
            this.props.history.push(this.props.match.url+'?mode=' + $(".mode_filter").val());
        }else if($(".mode_filter").val()==""&& this.props.model_search_element){
            this.props.history.push(this.props.match.url+'?search=' + this.props.model_search_element + '');
        }else{
            this.props.history.push(this.props.match.url);
        }
        this.props.dispatch(getAppsModelList(1));    
    }
       
    render() {
        const modelList = store.getState().apps.modelList.data;
        var createModelPermission = store.getState().apps.modelList.permission_details;
        let appsModelList = null;
        if (modelList) {
            const pages = store.getState().apps.modelList.total_number_of_pages;
            const current_page = store.getState().apps.current_page;            
            let paginationTag = null
            if(pages > 1){
                paginationTag = <Pagination  ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect.bind(this)} first last next prev boundaryLinks items={pages} activePage={current_page}/>
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
                                        <div className="search-wrapper">
                                            <input type="text" name="model_insights" defaultValue={this.props.model_search_element} onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Model Insights" id="model_insights" className="form-control search-box" placeholder="Search Model insights..." required />
                                            <span className="fa fa-search form-control-feedback"></span>
                                            <button className="close-icon" type="reset" onClick={this.clearSearchElement.bind(this)}></button>
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
                                             <a href="javascript:;" onClick={this.doSorting.bind(this,'created_at','asc')}><i class="fa fa-long-arrow-down arrIcon" ></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i> Date Ascending</a>
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
                        {store.getState().datasets.paginationFlag &&
                            <div className="paginationFlg">
                              <img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
                            </div>
                        }
                        {!store.getState().datasets.paginationFlag &&
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
        if (this.props.model_search_element) {
            this.props.history.push(this.props.match.url+'?search=' + this.props.model_search_element+'&page='+eventKey+'')
        }  else if(this.props.apps_model_sorton){
            this.props.history.push(this.props.match.url+'?sort=' + this.props.apps_model_sorton +'&type='+this.props.apps_model_sorttype+'&page=' + eventKey + '');
        }else if(this.props.mode_filter_by!="" && this.props.mode_filter_by!=null){
            this.props.history.push(this.props.match.url+'?filllter=' + this.props.mode_filter_by +'&type='+this.props.apps_model_sorttype+'&page=' + eventKey + '');
        }else
            this.props.history.push(this.props.match.url+'?page='+eventKey+'')
        this.props.dispatch(getAppsModelList(eventKey));
    }
    clearSearchElement(){
        this.props.dispatch(storeModelSearchElement(""));
        this.props.dispatch(storeAppsModelSortElements("",""));
        var modeSelected= window.location.pathname.includes("autoML")?'/autoML':'/analyst'
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
