import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {DetailOverlay} from "../common/DetailOverlay";
import { getDataSetPreview, storeSignalMeta, handleDelete, handleRename,resetSubsetting,getAllDataList,getAllUsersList, clearDataList} from "../../actions/dataActions";
import { openDULoaderPopup, updateDatasetName,openShareModalAction} from "../../actions/dataActions";
import {triggerDataUploadAnalysis} from "../../actions/dataUploadActions";
import {STATIC_URL} from "../../helpers/env.js"
import {getUserDetailsOrRestart,SUCCESS,INPROGRESS,HANA,MYSQL,MSSQL,HDFS, FAILED, statusMessages, setDateFormatHelper} from  "../../helpers/helper"
import Dialog from 'react-bootstrap-dialog'
import {clearDataPreview} from "../../actions/dataUploadActions";
import store from "../../store"

@connect((store) => {
    return {
        dataList: store.datasets.dataList,
        allDataList:store.datasets.allDataSets,
    };
})

export class DataCard extends React.Component {
    constructor(props) {
        super(props);
    }
    componentWillMount() {
        this.props.dispatch(getAllDataList());
        this.props.dispatch(getAllUsersList())
      }
    
    getPreviewData(status,dataSlug) {
        if(status==FAILED){
            bootbox.alert({
                message:statusMessages("error",this.props.data.filter(i=>(i.slug===dataSlug))[0].completed_message,"failed_mascot"),
                className:"fCard"
            });
        }else{
            var that = this;
            this.selectedData = dataSlug 
            this.props.dispatch(clearDataPreview());
            this.props.dispatch(storeSignalMeta(null, that.props.match.url));
            this.props.dispatch(getDataSetPreview(this.selectedData));
            this.props.dispatch(resetSubsetting(this.selectedData));
        }
    }
    
    handleDelete(slug,evt) {
        this.props.dispatch(handleDelete(slug, this.dialog,evt));
    }
    handleRename(slug, name,dataList) {
        var allDataList=this.props.allDataList
        this.props.dispatch(handleRename(slug, this.dialog, name,allDataList,dataList));
    }
    openShareModal(shareItem,slug,itemType) {
        this.props.dispatch(openShareModalAction(shareItem,slug,itemType));
    }
    openDataLoaderScreen(slug, percentage, message){
        var dataUpload = {};
        dataUpload.slug = slug
        this.props.dispatch(openDULoaderPopup());
        this.props.dispatch(updateDatasetName(slug));
        this.props.dispatch(triggerDataUploadAnalysis(dataUpload, percentage, message));
    }
   
    render() { 
        const dataSets = this.props.data;
        const dataList=this.props.dataList;

        const dataSetList = dataSets.map((data, i) => { 
            var iconDetails = "";
            if(data.status == FAILED){
                var dataSetLink = "/data/";
            }else{
                var dataSetLink = "/data/" + data.slug;
            }
            var percentageDetails = "";
            
            if(data.status == INPROGRESS){
                percentageDetails =   <div class=""><i className="fa fa-circle inProgressIcon"></i><span class="inProgressIconText">{data.completed_percentage >= 0 ? data.completed_percentage+' %':"In Progress"}</span></div>
            }else if(data.status == SUCCESS){
                data.completed_percentage = 100;
                percentageDetails =   <div class=""><i className="fa fa-check completedIcon"></i><span class="inProgressIconText">{data.completed_percentage}&nbsp;%</span></div>
            }else if(data.status == FAILED){
                percentageDetails =  <div class=""><font color="#ff6600">Failed</font></div>
            }
            
            let src = STATIC_URL + "assets/images/File_Icon.png"
            if(data.datasource_type == HANA){
                src = STATIC_URL + "assets/images/sapHana_Icon.png"
            }else if (data.datasource_type == MYSQL) {
                src = STATIC_URL + "assets/images/mySQL_Icon.png"
            }else if (data.datasource_type == MSSQL) {
                src = STATIC_URL + "assets/images/SqlServer_Icons.png"
            }else if (data.datasource_type == HDFS) {
                src = STATIC_URL + "assets/images/hadoop_Icons.png"
            }else {
                src = STATIC_URL + "assets/images/File_Icon.png"
            }
            iconDetails = <img src={src} alt="LOADING"/>;
            var permissionDetails = data.permission_details;
            var isDropDown = permissionDetails.remove_dataset || permissionDetails.rename_dataset;
            
            return (
                <div className="col-md-3 xs-mb-15 list-boxes" key={i}>
                    <div id={data.name} className="rep_block newCardStyle" name={data.name}>
                        <Link id={data.slug} to={data.status == INPROGRESS?"#":dataSetLink} onClick={data.status == INPROGRESS?this.openDataLoaderScreen.bind(this,data.slug,data.completed_percentage,data.completed_message):this.getPreviewData.bind(this,data.status,data.slug)}>
                            <div className="card-header"></div>
                            <div className="card-center-tile">
                                <div className="row">
                                    <div className="col-xs-12">
                                        <h5 className="title newCardTitle pull-left">
                                            <span>{data.name}</span>
                                        </h5>
                                        <div className="pull-right">{iconDetails}</div>
                                        <div className="clearfix"></div>
                                        <div className="clearfix"></div>
                                        {percentageDetails}
                                    </div>   
                                </div>
                            </div>
                        </Link>
                        <div className="card-footer">
                            <Link id={data.slug} to={data.status == INPROGRESS?"#":dataSetLink} onClick={data.status == INPROGRESS?this.openDataLoaderScreen.bind(this,data.slug,data.completed_percentage,data.completed_message):this.getPreviewData.bind(this,data.status,data.slug)}>
                                <div className="left_div">
                                    <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                                    <span className="footerTitle">{setDateFormatHelper(data.created_at)}</span>
                                </div>
                            </Link>
                            {isDropDown == true ?<div class="btn-toolbar pull-right">
                                <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                                    <i className="ci glyphicon glyphicon-option-vertical"></i>
                                </a>
                                <ul className="dropdown-menu dropdown-menu-right drp_cst_width" aria-labelledby="dropdownMenuButton">
							        <li className="xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10"><DetailOverlay details={data}/> </li>
							        <li className="xs-pl-20 xs-pr-20 xs-pb-10">
                                        {permissionDetails.rename_dataset == true ?  <span onClick={this.handleRename.bind(this, data.slug, data.name,dataList.data)}>
                                        <a className="dropdown-item btn-primary" href="#renameCard" data-toggle="modal">
                                            <i className="fa fa-pencil"></i>&nbsp;&nbsp;Rename
                                        </a>
                                        </span>:""}

                                        {permissionDetails.remove_dataset == true ? <span onClick={this.handleDelete.bind(this, data.slug)}>
                                            <a className="dropdown-item btn-primary" href="#deleteCard" data-toggle="modal">
                                                <i className="fa fa-trash-o"></i>&nbsp;&nbsp;
                                                {data.status == "INPROGRESS"? "Stop": "Delete"}
                                            </a>
                                        </span>: ""}
                                        {data.status == "SUCCESS"? <span  className="shareButtonCenter"onClick={this.openShareModal.bind(this,data.name,data.slug,"datasets")}>
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
        return(
            <div>
            {(dataSetList.length>0)?(dataSetList)
                :(<div><div className="text-center text-muted xs-mt-50"><h2>No results found..</h2></div></div>)
            }
            </div>
        );
    }
    
    componentWillUnmount(){
        if(!store.getState().datasets.paginationFlag)
        this.props.dispatch(clearDataList())
    }
}
