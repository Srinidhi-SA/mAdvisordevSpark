import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {
  updateScoreSlug,
  handleScoreRename,
  handleScoreDelete,
  openAppsLoader,
  createScoreSuccessAnalysis,
  showCreateModalPopup,
  clearScoreList
} from "../../actions/appActions";
import {DetailOverlay} from "../common/DetailOverlay";
import {STATIC_URL} from "../../helpers/env.js"
import {getUserDetailsOrRestart,SUCCESS,INPROGRESS, FAILED, statusMessages,setDateFormatHelper} from  "../../helpers/helper"
import Dialog from 'react-bootstrap-dialog'
import {openShareModalAction} from "../../actions/dataActions";

@connect((store) => {
  return {
    scoreList: store.apps.scoreList,
  };
})

export class ScoreCard extends React.Component {
  constructor(props) {
    super(props);
  }
    
  handleScoreDelete(slug) {
    this.props.dispatch(handleScoreDelete(slug, this.dialog));
  }
  
  handleScoreRename(slug, name) {
    this.props.dispatch(handleScoreRename(slug, this.dialog, name));
  }
  
  getScoreSummary(slug,status,sharedSlug) {
    if(status==FAILED){
      bootbox.alert({
        message:statusMessages("error","Unable to create Score. Please check your connection and try again.","failed_mascot"),
        className:"fCard"
      });
    }else{
      this.props.dispatch(updateScoreSlug(slug,sharedSlug));
    }
  }
  
  openDataLoaderScreen(data){
    this.props.dispatch(showCreateModalPopup())
    this.props.dispatch(openAppsLoader(data.completed_percentage,data.completed_message));
    this.props.dispatch(createScoreSuccessAnalysis(data));
  }
  
  openShareModal(shareItem,slug,itemType) {
    this.props.dispatch(openShareModalAction(shareItem,slug,itemType));
  }

  render() {
    var scoreList = this.props.data;
    const appsScoreList = scoreList.map((data, i) => {
      if(data.status==FAILED){
        var scoreLink = window.location.pathname.slice(0, window.location.pathname.lastIndexOf('/')) + "/scores/";
      }else{
        var scoreLink = window.location.pathname.slice(0, window.location.pathname.lastIndexOf('/')) + "/scores/" + data.slug;
      }
      
      var percentageDetails = "";
      if(data.status == INPROGRESS){
        percentageDetails =   <div class=""><i className="fa fa-circle inProgressIcon"></i><span class="inProgressIconText">{data.completed_percentage >= 0 ? data.completed_percentage+' %':"In Progress"}</span></div>;
      }else if(data.status == SUCCESS){
        data.completed_percentage = 100;
        percentageDetails =   <div class=""><i className="fa fa-check completedIcon"></i><span class="inProgressIconText">{data.completed_percentage}&nbsp;%</span></div>;
      }else if(data.status == FAILED){
        percentageDetails =  <div class=""><font color="#ff6600">Failed</font></div>
      }
        
      var permissionDetails = data.permission_details;
      var isDropDown = permissionDetails.remove_score || permissionDetails.rename_score; 
      return (
        <div className="col-md-3 xs-mb-15 list-boxes" key={i}>
          <div className="rep_block newCardStyle" name={data.name}>
            <Link id={data.slug} to={data.status == INPROGRESS?"#":scoreLink} onClick={data.status == INPROGRESS?this.openDataLoaderScreen.bind(this,data):this.getScoreSummary.bind(this, data.slug,data.status,data.shared_slug)}>
            <div className="card-header"></div>
            <div className="card-center-tile">
              <div className="row">            
                <div className="col-xs-12">
                  <h5 className="title newCardTitle pull-left">
                    <span>{data.name}</span>
                  </h5>
                  <div className="pull-right">
                    <img src={STATIC_URL + "assets/images/apps_score_icon.png"} alt="LOADING"/>
                  </div>
                  <div className="clearfix"></div>
                  <div className="clearfix"></div>
                    {percentageDetails}                
                  </div>
                </div>
              </div>
            </Link>
            <div className="card-footer">
              <Link id={data.slug} to={data.status == INPROGRESS?"#":scoreLink} onClick={data.status == INPROGRESS?this.openDataLoaderScreen.bind(this,data):this.getScoreSummary.bind(this, data.slug,data.status,data.shared_slug)}>
                <div className="left_div">
                  <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                  <span className="footerTitle">{setDateFormatHelper(data.created_at)}</span>
                </div>
              </Link>
              {isDropDown == true ?
                <div class="btn-toolbar pull-right">
                  <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                    <i className="ci glyphicon glyphicon-option-vertical"></i>
                  </a>
                  <ul className="dropdown-menu dropdown-menu-right drp_cst_width" aria-labelledby="dropdownMenuButton">
                    <li className="xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10"><DetailOverlay details={data}/> </li>
                    <li className="xs-pl-20 xs-pr-20 xs-pb-10">
                      {permissionDetails.rename_score == true ?
                        <span onClick={this.handleScoreRename.bind(this, data.slug, data.name)}>
                        <a className="dropdown-item btn-primary" href="#renameCard" data-toggle="modal">
                          <i className="fa fa-pencil"></i>
                        &nbsp;&nbsp;Rename</a>
                        </span>:""}
                      {permissionDetails.remove_score == true ?
                        <span onClick={this.handleScoreDelete.bind(this, data.slug)}>
                          <a className="dropdown-item btn-primary" href="#deleteCard" data-toggle="modal">
                            <i className="fa fa-trash-o"></i>
                            &nbsp;&nbsp;{data.status == "INPROGRESS"? "Stop": "Delete"}
                          </a>
                        </span>:""}
                      {data.status == "SUCCESS"? 
                        <span  className="shareButtonCenter" onClick={this.openShareModal.bind(this,data.name,data.slug,"score")}>
                          <a className="dropdown-item btn-primary" href="#shareCard" data-toggle="modal">
                            <i className="fa fa-share-alt"></i>
                          &nbsp;&nbsp;{"Share"}</a>
                        </span>: ""}
                      <div className="clearfix"></div>
                    </li>
                  </ul>
                </div>
              :""}
            </div>
          </div>
          <Dialog ref={(el) => { this.dialog = el }} />
        </div>
      )
    });
    return(
      <div >
        {(appsScoreList.length>0)?(appsScoreList):(
          <div>
            <div className="text-center text-muted xs-mt-50">
              <h2>No results found..</h2>
            </div>
          </div>
        )}
      </div>
    );
  }
  componentWillUnmount(){
    if(!store.getState().datasets.paginationFlag)
      this.props.dispatch(clearScoreList());
  }
}
