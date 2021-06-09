import React from "react";
import {Pagination} from "react-bootstrap";
import {Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {AppsLoader} from "../common/AppsLoader";
import {getAudioFile,getAudioFileList,storeAudioSearchElement,handleAudioDelete,handleAudioRename} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {SEARCHCHARLIMIT} from "../../helpers/helper";
import Dialog from 'react-bootstrap-dialog'
import {AudioFileCard} from "./AudioFileCard";
import {LatestAudioFile} from "./LatestAudioFiles";

@connect((store) => {
	return {
		audioFileSummaryFlag:store.apps.audioFileSummaryFlag,
		audioFileSlug:store.apps.audioFileSlug,
		audioList:store.apps.audioList,
		audio_search_element:store.apps.audio_search_element
	};
})


export class AudioFileList extends React.Component {
  constructor(props) {
    super(props);
    this.handleSelect = this.handleSelect.bind(this);
  }
  componentWillMount(){
	  var pageNo = 1;
	  if(this.props.history.location.search.indexOf("page") != -1){
			pageNo = this.props.history.location.search.split("page=")[1];
			this.props.dispatch(getAudioFileList(pageNo));
		}else{
			this.props.dispatch(getAudioFileList(pageNo));
		}
  }
  handleAudioDelete(slug){
	  this.props.dispatch(handleAudioDelete(slug,this.refs.dialog));
  }
  handleAudioRename(slug,name){
	  this.props.dispatch(handleAudioRename(slug,this.refs.dialog,name));
  }
  getAudioFileSummary(slug){
	 this.props.dispatch(getAudioFile(slug));
  }
  _handleKeyPress = (e) => {
	  if (e.key === 'Enter') {
		  if (e.target.value != "" && e.target.value != null)
		  this.props.history.push('/apps/audio?search=' + e.target.value + '')
		  this.props.dispatch(storeAudioSearchElement(e.target.value));
		  this.props.dispatch(getAudioFileList(1));

	  }
  }
	onChangeOfSearchBox(e){
		if(e.target.value==""||e.target.value==null){
			this.props.dispatch(storeAudioSearchElement(""));
			this.props.history.push('/apps/audio')
			this.props.dispatch(getAudioFileList(1));

		}else if (e.target.value.length > SEARCHCHARLIMIT) {
			this.props.history.push('/apps/audio?search=' + e.target.value + '')
			this.props.dispatch(storeAudioSearchElement(e.target.value));
			this.props.dispatch(getAudioFileList(1));
		}
	}
  render() {
    if(store.getState().apps.audioFileSummaryFlag){
        let _link = "/apps/audio/"+store.getState().apps.audioFileSlug;
        return(<Redirect to={_link}/>);
    }
    const audioList = store.getState().apps.audioList.data;

    if (audioList) {
		const pages = store.getState().apps.audioList.total_number_of_pages;
		const current_page = store.getState().apps.current_page;
	
		let paginationTag = null
        const audioFileList = <AudioFileCard data={audioList}/>
		if(pages > 1){
			paginationTag = <Pagination  ellipsis bsSize="medium" maxButtons={10} onSelect={this.handleSelect} first last next prev boundaryLinks items={pages} activePage={current_page}/>
		}
		
		return (
				<div className="side-body">
				<LatestAudioFile props={this.props}/>
				<div className="main-content">

					<div className="row">
					  
						<div className="col-md-12">
							
							<div class="btn-toolbar pull-right">
				<div class="input-group">
				
				<div className="search-wrapper">
					<form>
					<input type="text" name="audio_file" onKeyPress={this._handleKeyPress.bind(this)} onChange={this.onChangeOfSearchBox.bind(this)} title="Media Files" id="audio_file" className="form-control search-box" placeholder="Search Audio files..." required />
					<span className="fa fa-search form-control-feedback"></span>
					<button className="close-icon" type="reset"></button>
					</form>
				</div>

				</div>
                  <div class="btn-group hidden">
                    <button type="button" data-toggle="dropdown" title="Sorting" class="btn btn-default dropdown-toggle" aria-expanded="false">
                      <i class="glyphicon glyphicon-sort"></i>
                    </button>
                    <ul role="menu" class="dropdown-menu dropdown-menu-right">
                        <li>
                          <a href="#" ><i class="fa fa-sort-alpha-asc"></i>&nbsp;&nbsp;Name Ascending</a>
                        </li>
                        <li>
                          <a href="#" ><i class="fa fa-sort-alpha-desc"></i>&nbsp;&nbsp;Name Descending</a>
                        </li>
                        <li>
                          <a href="#" ><i class="fa fa-long-arrow-down arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i>&nbsp;&nbsp;Date Ascending</a>
                        </li>
                        <li>
                          <a href="#" ><i class="fa fa-long-arrow-up arrIcon"></i><i style={{fontSize:12}} class="fa fa-calendar-check-o"></i>&nbsp;&nbsp;Date Descending</a>
                        </li>
                    </ul>
                  </div>
				  </div>	
							
						</div>	<div class="clearfix"></div>
				</div>
				
				<div class="clearfix xs-m-10"></div>
				
				<div className="row">
				{audioFileList}
				<div className="clearfix"></div>
				</div>
				<div className="ma-datatable-footer"  id="idPagination">
				<div className="dataTables_paginate">
				{paginationTag}
				</div>
				</div>
				</div>
				 <Dialog ref="dialog" />
				 <AppsLoader match={this.props.match}/>
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

	  if (this.props.audio_search_element) {
		  this.props.history.push('/apps/audio?search=' + this.props.model_search_element+'?page='+eventKey+'')
	  } else
		  this.props.history.push('/apps/audio?page='+eventKey+'')

		  this.props.dispatch(getAudioFileList(eventKey));
  }

}
