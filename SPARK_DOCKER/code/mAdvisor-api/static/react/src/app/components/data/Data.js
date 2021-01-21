import React from "react";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import { Pagination } from "react-bootstrap";
import store from "../../store";
import {Share} from "../common/Share"
import {getDataList,refreshDatasets,setEditModelValues,storeSignalMeta, storeDataSearchElement,storeDataSortElements,getAllUsersList,fetchModelEditAPISuccess,variableSlectionBack, paginationFlag, clearDataList} from "../../actions/dataActions";
import {STATIC_URL} from "../../helpers/env.js"
import {SEARCHCHARLIMIT} from  "../../helpers/helper"
import {DataUploadLoader} from "../common/DataUploadLoader";
import Dialog from 'react-bootstrap-dialog';
import {DataCard}  from "./DataCard";
import {LatestDatasets} from "./LatestDatasets";

@connect((store) => {
  return {
    dataList: store.datasets.dataList,
    dataPreview: store.datasets.dataPreview,
    userList:store.datasets.allUserList,
    data_search_element: store.datasets.data_search_element,
	  data_sorton:store.datasets.data_sorton,
	  data_sorttype:store.datasets.data_sorttype,
  };
})

export class Data extends React.Component {
  constructor(props) {
    super(props);
    this.selectedData = "";
  }
  componentWillMount() {
    var pageNo = 1;
    this.props.dispatch(setEditModelValues("","",false));
    this.props.dispatch(fetchModelEditAPISuccess(""))
    this.props.dispatch(storeSignalMeta(null, this.props.match.url));
    this.props.dispatch(variableSlectionBack(false));

    if(this.props.history.location.search!=""){
      let urlParams = new URLSearchParams(this.props.history.location.search);
      pageNo = (urlParams.get("page")!="")?urlParams.get("page"):pageNo
      let searchELem = (urlParams.get('search')!=null)?urlParams.get('search'):"";
      let sortELem = (urlParams.get('sort')!=null)?urlParams.get('sort'):"";
      let sortType = (urlParams.get('type')!=null)?urlParams.get('type'):"";
      this.props.dispatch(storeDataSearchElement(searchELem));
      this.props.dispatch(storeDataSortElements(sortELem,sortType));
      this.props.dispatch(getDataList(pageNo));
    }else if (this.props.history.location.search.indexOf("page") != -1) {
      pageNo = this.props.history.location.search.split("page=")[1];
      this.props.dispatch(getDataList(pageNo));
    }else
      this.props.dispatch(getDataList(pageNo));
    }
  componentDidMount(){
     this.props.dispatch(refreshDatasets(this.props));
     this.props.dispatch(getAllUsersList(this.props));
     
  }

  _handleKeyPress = e => {
    if (e.key === 'Enter') {
      if (e.target.value != "" && e.target.value != null)
        this.props.history.push('/data?search=' + e.target.value + '')
      this.props.dispatch(storeDataSearchElement(e.target.value));
      this.props.dispatch(getDataList(1));
    }
  }
  onChangeOfSearchBox= e => {
    if(e.target.value==""||e.target.value==null){
      if(this.props.data_sorton!="" && this.props.data_sorttype!=""){
        this.props.history.push('/data?sort='+this.props.data_sorton + '&type='+this.props.data_sorttype)
      }else{
        this.props.history.push('/data');
      }
      this.props.dispatch(storeDataSearchElement(""));
      this.props.dispatch(getDataList(1));
    }else if (e.target.value.length > SEARCHCHARLIMIT) {
      if(this.props.data_sorton!="" && this.props.data_sorttype!=""){
        this.props.history.push('/data?search='+e.target.value+'&sort='+this.props.data_sorton + '&type='+this.props.data_sorttype)
      }else{
        this.props.history.push('/data?search=' + e.target.value + '')
      }
      this.props.dispatch(storeDataSearchElement(e.target.value));
      this.props.dispatch(getDataList(1));
    }else{
      this.props.dispatch(storeDataSearchElement(e.target.value));
    }
  }

  doSorting=(sortOn, type)=>{
    this.props.dispatch(storeDataSortElements(sortOn,type));
    if(this.props.data_search_element)
      this.props.history.push('/data?search='+this.props.data_search_element+'&sort='+sortOn + '&type='+type)
	  else
      this.props.history.push('/data?sort=' + sortOn + '&type='+type);
  	this.props.dispatch(getDataList(1));
  }

  clearSearchElement= () =>{
    this.props.dispatch(storeDataSearchElement(""));
    if(this.props.data_sorton != "" && this.props.data_sorttype!="")
      this.props.history.push('/data?sort=' + this.props.data_sorton + '&type=' + this.props.data_sorttype)
    else
      this.props.history.push('/data');
    this.props.dispatch(getDataList(1));
  }

  handleSelect= eventKey =>{
    this.props.dispatch(paginationFlag(true));
		if(this.props.data_search_element){
      if(this.props.data_sorton)
        this.props.history.push('/data?search=' + this.props.data_search_element +'&sort='+this.props.data_sorton +'&type='+this.props.data_sorttype+ '&page=' + eventKey + '');
      else
        this.props.history.push('/data?search=' + this.props.data_search_element + '&page=' + eventKey + '');
    }else if(this.props.data_sorton!="" && this.props.data_sorttype!=undefined){
	    this.props.history.push('/data?sort=' + this.props.data_sorton +'&type='+this.props.data_sorttype+'&page=' + eventKey + '');
	  }else{
      this.props.history.push('/data?page=' + eventKey + '');
    }
    this.props.dispatch(getDataList(eventKey));
  }

  render() {
    if (store.getState().datasets.dataPreviewFlag && this.props.dataPreview &&this.props.dataPreview.status!="FAILED") {
      if(!store.getState().datasets.dataPreview.viewed) {
      let _link = "/data/" + store.getState().datasets.selectedDataSet;
      return (<Redirect to={_link}/>);
      }
    }

    const dataSets = store.getState().datasets.dataList.data;
    if (dataSets) {
      const pages = store.getState().datasets.dataList.total_number_of_pages;
      const current_page = store.getState().datasets.dataList.current_page;
      let paginationTag = null;
      let dataList = <DataCard data={dataSets} match={this.props.match}/>;
      if(pages>=1)
        paginationTag = <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
      return (
        <div className="side-body">
        <LatestDatasets props={this.props}/>
          <div class="main-content">
            <div class="row">
              <div class="col-md-12">
			          <div class="btn-toolbar pull-right">
                  <div class="input-group">
                    <div className="search-wrapper">
                      <input type="text" name="search_data"  value= {this.props.data_search_element} onKeyPress={this._handleKeyPress} onChange={this.onChangeOfSearchBox} title="type here to Search data" id="search_data" className="form-control search-box" placeholder="Search data..." required />
                      <span className="zmdi zmdi-search form-control-feedback"></span>
                      <button className="close-icon" type="reset" onClick={this.clearSearchElement}></button>
                    </div>
                  </div>
                  <div class="btn-group">
                    <button type="button" data-toggle="dropdown" title="Sorting" class="btn btn-default dropdown-toggle" aria-expanded="false">
                      <i class="zmdi zmdi-hc-lg zmdi-sort-asc"></i>
                    </button>
                    <ul role="menu" class="dropdown-menu dropdown-menu-right">
                        <li>
                          <a href="#" onClick={()=>this.doSorting('name','asc')}><i class="zmdi zmdi-sort-amount-asc"></i>&nbsp;&nbsp;Name Ascending</a>
                        </li>
                        <li>
                          <a href="#" onClick={()=>this.doSorting('name','desc')}><i class="zmdi zmdi-sort-amount-desc"></i>&nbsp;&nbsp;Name Descending</a>
                        </li>
                        <li>
                          <a href="#" onClick={()=>this.doSorting('created_at','asc')}><i class="zmdi zmdi-calendar-alt"></i>&nbsp;&nbsp;Date Ascending</a>
                        </li>
                        <li>
                          <a href="#" onClick={()=>this.doSorting('created_at','desc')}><i class="zmdi zmdi-calendar"></i>&nbsp;&nbsp;Date Descending</a>
                        </li>
                    </ul>
                  </div>
				         </div>
              </div>
            </div>
            <div class="clearfix"></div>
            {
              store.getState().datasets.paginationFlag &&
              <div className="row">
                <div className="paginationFlg">
                  <img src={STATIC_URL+"assets/images/pageLoader.gif"} style={{margin:"auto"}}></img>
                </div>
              </div>
            }{
              !store.getState().datasets.paginationFlag &&
              <div className="row">
            {dataList}
              <div className="clearfix"></div>
            </div>
            }
            <div className="ma-datatable-footer" id="idPagination">
              <div className="dataTables_paginate">
                {paginationTag}
              </div>
            </div>
            <DataUploadLoader/>
            <Share usersList={this.props.userList}/>
        </div>
      </div>
      );
    } else {
      return (
        <div className="side-body">
          <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
           <Dialog ref={(el) => { this.dialog = el }}/>
        </div>
      )
    }
  }

  componentWillUnmount(){
    this.props.dispatch(storeDataSearchElement(""));
    this.props.dispatch(storeDataSortElements("",""));
    this.props.dispatch(clearDataList())
  }
}
