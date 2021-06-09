import React from "react";
import {connect} from "react-redux";
import {getUserDetailsOrRestart,SUCCESS,INPROGRESS,FAILED, statusMessages, setDateFormatHelper} from "../../helpers/helper.js"
import {getStockAnalysis,updateStockSlug,handleStockDelete,handleStockModelRename,openAppsLoader,callStockAnalysisApi, showCreateModalPopup} from "../../actions/appActions";
import Dialog from 'react-bootstrap-dialog'
import {STATIC_URL} from "../../helpers/env.js";
import {DetailOverlay} from "../common/DetailOverlay";

@connect((store) => {
    return {
        stockList: store.apps.stockAnalysisList,
        stockAnalysisFlag:store.apps.stockAnalysisFlag,
        stockSlug:store.apps.stockSlug,
    };
})

export class StocksCard extends React.Component {
    constructor(props) {
        super(props);
    }
    getPreviewData(status,e) {
        if(status==FAILED){
            bootbox.alert({message:statusMessages("error","Stock analysis could not be created.","failed_mascot"),
                className:"fCard"
            });
        }else{
            this.props.dispatch(updateStockSlug(e.target.id))
            this.props.dispatch(getStockAnalysis(e.target.id))
            this.props.loadfunc();
        }
    }
    handleDelete(slug){
        this.props.dispatch(handleStockDelete(slug,this.dialog));
    }
    handleRename(slug,name){
        this.props.dispatch(handleStockModelRename(slug,this.dialog,name));
    }

    openDataLoaderScreen(data){
        this.props.dispatch(showCreateModalPopup());
        this.props.dispatch(openAppsLoader(data.completed_percentage,data.completed_message));
        this.props.dispatch(callStockAnalysisApi(data.slug));
    }

    render() {
        const stockAnalysisList = this.props.data;
        const stockTemplateList = stockAnalysisList.map((data, i) => {
            var stockLink = <a class="cursor" id={data.slug} onClick={this.getPreviewData.bind(this,data.status)}>{data.name}</a>;
            var percentageDetails = "";
            if(data.status == INPROGRESS){
                percentageDetails =   <div class=""><i className="fa fa-circle inProgressIcon"></i><span class="inProgressIconText">{data.completed_percentage >= 0 ?data.completed_percentage+' %':"In Progress"}</span></div>;
                stockLink = <a class="cursor" onClick={this.openDataLoaderScreen.bind(this,data)}> {data.name}</a>;
            }else if(data.status == SUCCESS){
                data.completed_percentage = 100;
                percentageDetails =   <div class=""><i className="fa fa-check completedIcon"></i><span class="inProgressIconText">{data.completed_percentage}&nbsp;%</span></div>;
            }else if(data.status == FAILED){
                percentageDetails =  <div class=""><font color="#ff6600">Failed</font></div>
            }
            var permissionDetails = data.permission_details;
            var isDropDown = permissionDetails.remove_stock || permissionDetails.rename_stock; 
            return (
                <div className="col-md-3 top20 list-boxes" key={i}>
                    <div className="rep_block newCardStyle" name={data.name}>
                        <div className="card-header"></div>
                        <div className="card-center-tile">
                            <div className="row">
                                <div className="col-xs-12">
                                    <h5 className="title newCardTitle pull-left">
                                        {stockLink}
                                    </h5>
                                    <div className="pull-right">
                                        <img src={ STATIC_URL + "assets/images/apps_model_icon.png" } alt="LOADING"/>
                                    </div>
                                    <div className="clearfix"></div>
                                    <div className="clearfix"></div>
                                    {percentageDetails}
                                </div>
                            </div>
                        </div>
                        <div className="card-footer">
                            <div className="left_div">
                                <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                                <span className="footerTitle">{setDateFormatHelper(data.created_at)}</span>
                            </div>
                            {isDropDown == true ? <div class="btn-toolbar pull-right">
                                <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                                <i className="ci glyphicon glyphicon-option-vertical"></i>
                                </a>
                                <ul className="dropdown-menu dropdown-menu-right drp_cst_width" aria-labelledby="dropdownMenuButton">
                                    <li className="xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10"><DetailOverlay details={data}/> </li>
                                    <li className="xs-pl-20 xs-pr-20 xs-pb-10">
                                        {permissionDetails.rename_stock == true ?
                                        <span onClick={this.handleRename.bind(this, data.slug, data.name)}>
                                        <a className="dropdown-item btn-primary" href="#renameCard" data-toggle="modal">
                                        <i className="fa fa-pencil"></i>
                                        &nbsp;&nbsp;Rename</a>
                                        </span>:""}
                                        {permissionDetails.remove_stock == true ?
                                        <span onClick={this.handleDelete.bind(this, data.slug)}>
                                        <a className="dropdown-item btn-primary" href="#deleteCard" data-toggle="modal">
                                        <i className="fa fa-trash-o"></i>&nbsp;&nbsp;{data.status == "INPROGRESS"
                                        ? "Stop": "Delete"}</a>
                                        </span>:""}
                                        <div className="clearfix"></div>
                                    </li>
                                </ul>
                            </div>:""}
                        </div>
                    </div>
                    <Dialog ref={(el) => { this.dialog = el }} />
                </div>
            )
        });
        return(
            <div>
                {(stockTemplateList.length>0)?(stockTemplateList):
                    (<div><div className="text-center text-muted xs-mt-50">
                        <h2>No results found..</h2>
                    </div></div>)
                }
            </div>
        );
    }
}
