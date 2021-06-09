import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {openShareModalAction} from "../../actions/dataActions";
import {SUCCESS,FAILED,INPROGRESS,getUserDetailsOrRestart, statusMessages, setDateFormatHelper} from "../../helpers/helper";
import { emptySignalAnalysis,handleDelete,handleRename,triggerSignalAnalysis,clearSignalList} from "../../actions/signalActions";
import {STATIC_URL} from "../../helpers/env";
import {DetailOverlay} from "../common/DetailOverlay";
import Dialog from 'react-bootstrap-dialog';
import {openCsLoaderModal} from "../../actions/createSignalActions";
import store from "../../store";

@connect((store) => {
    return {
        signalList: store.signals.signalList.data,
        paginationFlag: store.datasets.paginationFlag
      };
})

export class SignalCard extends React.Component {
    constructor(props) {
        super(props);
        this.props=props;
    }
    getSignalAnalysis(status,itemSlug) {
      if(status==FAILED){
        bootbox.alert({
          message:statusMessages("error",this.props.signalList.filter(i=>(i.slug===itemSlug))[0].completed_message,"failed_mascot"),
          className:"fCard"
        });
      }else{
        this.props.dispatch(emptySignalAnalysis());
      }
      }
    handleDelete(slug,evt) {
        this.props.dispatch(handleDelete(slug, this.dialog,evt));
      }

      handleRename(slug, name) {
        this.props.dispatch(handleRename(slug, this.dialog, name));
      }
      openLoaderScreen(slug, percentage, message) {
          var signalData = {};
          signalData.slug = slug
          this.props.dispatch(openCsLoaderModal());
          this.props.dispatch(emptySignalAnalysis());
          this.props.dispatch(triggerSignalAnalysis(signalData, percentage, message));
    }
        openShareModal(shareItem,slug,itemType) {
          this.props.dispatch(openShareModalAction(shareItem,slug,itemType));
         }
    render() {
       var listData = this.props.data;
        const storyListDetails = listData.map((story, i) => {
            var iconDetails = "";
            var percentageDetails = "";
            var signalLink = story.status==FAILED? "/signals/" : "/signals/" + story.slug;
            var completed_percent = story.completed_percentage
            if(completed_percent>99)
            completed_percent=99
              if(story.status == INPROGRESS){
                  percentageDetails =   <div class=""><i className="fa fa-circle inProgressIcon"></i><span class="inProgressIconText">&nbsp;{completed_percent >= 0 ? completed_percent+' %':"In Progress"}&nbsp;</span></div>
              }else if(story.status == SUCCESS){
                  story.completed_percentage = 100;
                  percentageDetails =   <div class=""><i className="fa fa-check completedIcon"></i><span class="inProgressIconText">&nbsp;{story.completed_percentage}&nbsp;%</span></div>
              }else if(story.status == FAILED){
                percentageDetails =   <div class=""><font color="#ff6600">Failed</font></div>
              }

              var imgLink = story.type == "dimension"?STATIC_URL + "assets/images/s_d_carIcon.png":STATIC_URL + "assets/images/s_m_carIcon.png"
              iconDetails = <img src={imgLink} alt="LOADING"/>
              var permissionDetails = story.permission_details;
              var isDropDown = permissionDetails.remove_signal || permissionDetails.rename_signal;

            return (
              <div className="col-md-3 xs-mb-15 list-boxes" key={i}>
                <div id={story.name} className="rep_block newCardStyle" name={story.name}>
                <Link to={story.status == INPROGRESS?"#":signalLink} id={story.slug} onClick={story.status== INPROGRESS?this.openLoaderScreen.bind(this,story.slug,completed_percent,story.completed_message):this.getSignalAnalysis.bind(this,story.status,story.slug)}>
                  <div className="card-header"></div>
                  <div className="card-center-tile">
                    <div className="row">
                      <div className="col-xs-12">
                        <h5 className="title newCardTitle pull-left">
                          <span>{story.name}</span>
                        </h5>
						            <div className="pull-right">{iconDetails}</div>
					             <div className="clearfix"></div>
                           {percentageDetails}
                      </div>
                    </div>
                  </div>
                </Link>
                  <div className="card-footer">
                <Link to={story.status == INPROGRESS?"#":signalLink} id={story.slug} onClick={story.status== INPROGRESS?this.openLoaderScreen.bind(this,story.slug,completed_percent,story.completed_message):this.getSignalAnalysis.bind(this,story.status)}>
                  <div className="left_div">
                    <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                    <span className="footerTitle">{setDateFormatHelper(story.created_at)}</span>
                  </div>
                </Link>

					{isDropDown == true ? <div class="btn-toolbar pull-right">
                      <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                        <i className="ci glyphicon glyphicon-option-vertical"></i>
                      </a>
                      <ul className="dropdown-menu dropdown-menu-right drp_cst_width" aria-labelledby="dropdownMenuButton">
						<li className="xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10"><DetailOverlay details={story}/> </li>
						<li className="xs-pl-20 xs-pr-20 xs-pb-10">
							
							{permissionDetails.rename_signal == true ?
                        <span onClick={this.handleRename.bind(this, story.slug, story.name)}>
                          <a className="dropdown-item btn-primary" href="#renameCard" data-toggle="modal">
                            <i className="fa fa-pencil"></i>&nbsp;&nbsp;Rename</a>
                        </span>:""}
						
					    {permissionDetails.remove_signal == true ?
                        <span onClick={this.handleDelete.bind(this, story.slug)}>
                          <a className="dropdown-item btn-primary" href="#deleteCard" data-toggle="modal">
                            <i className="fa fa-trash-o"></i>&nbsp;&nbsp;{story.status == "INPROGRESS"
                              ? "Stop"
                              : "Delete"}</a>
                        </span> :""}
              {story.status == "SUCCESS"? <span  className="shareButtonCenter"onClick={this.openShareModal.bind(this,story.name,story.slug,"signals")}>
              <a className="dropdown-item btn-primary" href="#shareCard" data-toggle="modal">
              <i className="fa fa-share-alt"></i>&nbsp;&nbsp;{"Share"}</a>
              </span>: ""}
						<div className="clearfix"></div>
						</li>
					 
						 </ul>
            </div>:<div class="btn-toolbar pull-right"></div>}

                      </div>
                </div>
                   <Dialog ref={(el) => { this.dialog = el }}/>
              </div>
            )
          });
             return( <div>
           {
              (storyListDetails.length>0)
              ?(storyListDetails)
              :(<div className="text-center text-muted xs-mt-50"><h2>No results found..</h2></div>)
              }
           </div>);
    }
  componentWillUnmount(){
    if(!store.getState().datasets.paginationFlag)
      this.props.dispatch(clearSignalList());
  }
}
