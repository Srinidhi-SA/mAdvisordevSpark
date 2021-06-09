import React from "react";
import store from "../../store";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {openShareModalAction,fetchModelEdit,getDataSetPreview,setEditModelValues} from "../../actions/dataActions";
import {handleModelDelete,handleModelRename,openAppsLoader,createModelSuccessAnalysis, showCreateModalPopup, clearModelList, clearModelSummary} from "../../actions/appActions";
import {DetailOverlay} from "../common/DetailOverlay";
import {getUserDetailsOrRestart,SUCCESS,INPROGRESS, FAILED, statusMessages,setDateFormatHelper} from  "../../helpers/helper"
import {STATIC_URL} from "../../helpers/env.js";
import Dialog from 'react-bootstrap-dialog'
    
    
@connect((store) => {
    return {
        modelList: store.apps.modelList,
        modelSlug:store.apps.modelSlug,
    };
})
    
export class ModelsCard extends React.Component {
    constructor(props) {
        super(props);
    }
    
    handleModelDelete(slug){
        this.props.dispatch(handleModelDelete(slug,this.dialog));
    }
    handleModelRename(slug,name){
        this.props.dispatch(handleModelRename(slug,this.dialog,name));
    }
    openDataLoaderScreen(data){
        this.props.dispatch(showCreateModalPopup())
        this.props.dispatch(openAppsLoader(data.completed_percentage,data.completed_message));
        this.props.dispatch(createModelSuccessAnalysis(data));
    }
    getFailedMsg(status,itemSlug) {
        if(status==FAILED){
            bootbox.alert({
                message:statusMessages("error",this.props.data.filter(i=>(i.slug==itemSlug))[0].completed_message,"failed_mascot"),
                className:"fCard"
            });
        }
        else
            return;
    }
    openShareModal(shareItem,slug,itemType) {
        this.props.dispatch(openShareModalAction(shareItem,slug,itemType));
    }
    handleEditModel(dataSlug,modelSlug){
        this.props.dispatch(setEditModelValues(true));
        this.props.dispatch(getDataSetPreview(dataSlug));
        this.props.dispatch(fetchModelEdit(modelSlug))
    }

    render() {
        var modelList = this.props.data;
        var appsModelList = modelList.map((data, i) => {
            if(data.status==FAILED){
                var modelLink = this.props.match.url
            }else{
                var modelLink = this.props.match.url + "/" + data.slug;
            }
                var percentageDetails = "";
                if(data.status == INPROGRESS){
                    var setAppLoaderVal = data.completed_percentage;
                    percentageDetails =   <div class=""><i className="fa fa-circle inProgressIcon"></i><span class="inProgressIconText">{setAppLoaderVal >= 0 ? setAppLoaderVal +' %':"In Progress"}</span></div>;
                }else if(data.status == SUCCESS){
                    data.completed_percentage = 100;
                    percentageDetails =   <div class=""><i className="fa fa-check completedIcon"></i><span class="inProgressIconText">{data.completed_percentage}&nbsp;%</span></div>;  
                }else if(data.status == FAILED){
                    percentageDetails =  <div class=""><font color="#ff6600">Failed</font></div>
                }
                var permissionDetails = data.permission_details;
                var isDropDown = permissionDetails.remove_trainer || permissionDetails.rename_trainer;
                return (
                    <div className="col-md-3 xs-mb-15 list-boxes" key={i}>
                        <div id={data.name} className="rep_block newCardStyle" name={data.name}>
                            <Link to={data.status == INPROGRESS?"#":modelLink} id={data.slug} onClick={data.status== INPROGRESS?this.openDataLoaderScreen.bind(this,data):this.getFailedMsg.bind(this,data.status,data.slug)}>
                                <div className="card-header"></div>
                                <div className="card-center-tile">
                                    <div className="row">
                                        <div className="col-xs-12">                
                                            <h5 className="title newCardTitle pull-left">
                                                <span>{data.name}</span>
                                            </h5>                         
                                            <div className="pull-right">{store.getState().apps.currentAppDetails.app_type == "REGRESSION"?<img src={ STATIC_URL + "assets/images/apps_regression_icon.png" } alt="LOADING"/>:<img src={ STATIC_URL + "assets/images/apps_model_icon.png" } alt="LOADING"/>}</div>
                                            <div className="clearfix"></div>
                                            <div className="row">
                                                <div className="col-xs-12">
                                                    <div className="pull-left">
                                                        {percentageDetails}
                                                    </div>
                                                    <div className="pull-right" style={{"color":"#00998c"}}>
                                                        {(data.mode!=""&& data.mode!=null)?data.mode:"Analyst"}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>                                    
                                    </div>
                                </div>
                            </Link>
                            <div className="card-footer">
                                <Link to={data.status == INPROGRESS?"#":modelLink} id={data.slug} onClick={data.status== INPROGRESS?this.openDataLoaderScreen.bind(this,data):this.getFailedMsg.bind(this,data.status,data.slug)}>                      
                                    <div className="left_div">
                                        <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                                        <span className="footerTitle">{setDateFormatHelper(data.created_at, "mmm d,yyyy HH:MM")}</span>
                                    </div>
                                </Link>
                                {
                                    isDropDown == true ? <div class="btn-toolbar pull-right">
                                    <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                                        <i className="ci glyphicon glyphicon-option-vertical"></i>
                                    </a>
                                    <ul className="dropdown-menu dropdown-menu-right drp_cst_width" aria-labelledby="dropdownMenuButton">
                                        <li className="xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10"><DetailOverlay details={data}/> </li>
                                        <li className="xs-pl-20 xs-pr-20 xs-pb-10">
                                            {permissionDetails.rename_trainer == true ?
                                            <span onClick={this.handleModelRename.bind(this,data.slug,data.name)}>
                                                <a className="dropdown-item btn-primary" href="#renameCard" data-toggle="modal">
                                                <i className="fa fa-pencil"></i>&nbsp;&nbsp;Rename</a>
                                            </span>:""}
                                            {permissionDetails.remove_trainer == true ?
                                            <span onClick={this.handleModelDelete.bind(this,data.slug)} >
                                                <a className="dropdown-item btn-primary" href="#deleteCard" data-toggle="modal">
                                                <i className="fa fa-trash-o"></i>&nbsp;&nbsp;{data.status == "INPROGRESS"
                                                ? "Delete "
                                                : "Delete"}</a>
                                            </span>:""}
                                            <div style={{display:'flex',justifyContent:'center',width: '100%'}}>
                                                {data.status == "SUCCESS"? <span  className="shareButton"onClick={this.openShareModal.bind(this,data.name,data.slug,"trainer")}>
                                                    <a className="dropdown-item btn-primary" href="#shareCard" data-toggle="modal">
                                                    <i className="fa fa-share-alt"></i>&nbsp;&nbsp;{"Share"}</a>
                                                </span>: ""} 
                                                {(data.status == "SUCCESS" && data.mode ==="analyst" && data.shared != true)?
                                                <span onClick={this.handleEditModel.bind(this,data.dataset,data.slug)} style={{marginTop:'2%'}}>
                                                    <Link to={`/apps/"${this.props.match.params.AppId}/analyst/models/data/${data.dataset}/createModel`} id={data.slug} className="editButton btn-primary">
                                                    <i className="fa fa-edit"></i>&nbsp;&nbsp;{"Edit"}</Link>
                                                </span>               
                                                : ""} 
                                            </div>                        
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
                <div>
                {
                    (appsModelList.length>0)
                        ?(appsModelList)
                        :(<div><div className="text-center text-muted xs-mt-50"><h2>No results found..</h2></div></div>)
                }
            </div>);
    }
    componentWillUnmount(){
        if(!store.getState().datasets.paginationFlag){
            this.props.dispatch(clearModelList());
            this.props.dispatch(clearModelSummary());
        }
    }
}
