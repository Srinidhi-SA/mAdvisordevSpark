import React from "react";
import {MainHeader} from "../common/MainHeader";
import {Tabs,Tab,Pagination,Tooltip,OverlayTrigger,Popover} from "react-bootstrap";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {APPID4,APPNAME4} from "../../helpers/helper.js";
import {AudioFileUpload} from "./AudioFileUpload";
import {AppsLoader} from "../common/AppsLoader";
import {getAudioFile,getAudioFileList,handleAudioDelete,handleAudioRename} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {isEmpty,SEARCHCHARLIMIT,getUserDetailsOrRestart} from "../../helpers/helper";
import {DetailOverlay} from "../common/DetailOverlay";
import Dialog from 'react-bootstrap-dialog'
import Breadcrumb from 'react-breadcrumb';

var dateFormat = require('dateformat');

@connect((store) => {
    return {login_response: store.login.login_response,
        currentAppId:store.apps.currentAppId,
        audioFileSummaryFlag:store.apps.audioFileSummaryFlag,
        audioFileSlug:store.apps.audioFileSlug,
        audioList:store.apps.audioList,
        audio_search_element:store.apps.audio_search_element
        };
})


export class AudioFileCard extends React.Component {
  constructor(props) {
    super(props);
  }
 
  handleAudioDelete(slug){
      this.props.dispatch(handleAudioDelete(slug,this.dialog));
  }
  handleAudioRename(slug,name){
      this.props.dispatch(handleAudioRename(slug,this.dialog,name));
  }
  getAudioFileSummary(slug){
     this.props.dispatch(getAudioFile(slug));
  }

  render() {
    const audioList = this.props.data;
    
        const appsAudioList = audioList.map((data, i) => {
            var modelLink = "/apps/audio/" + data.slug;
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
            return (
                    <div className="col-md-3 top20 list-boxes" key={i}>
                    <div className="rep_block newCardStyle" name={data.name}>
                    <div className="card-header"></div>
                    <div className="card-center-tile">
                    <div className="row">
                    
                    <div className="col-xs-12">
                    <h5 className="title newCardTitle pull-left">
                    <Link to={modelLink} id= {data.slug} onClick={this.getAudioFileSummary.bind(this,data.slug)}>{data.name}</Link>
                    </h5>
                    <div className="clearfix"></div>
                    {percentageDetails}

                    <div class="btn-toolbar pull-right">
                    {/*<!-- Rename and Delete BLock  -->*/}
                    <a className="dropdown-toggle more_button" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="More..">
                    <i className="ci zmdi zmdi-hc-lg zmdi-more-vert"></i>
                    </a>
                    <ul className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                    <li onClick={this.handleAudioRename.bind(this,data.slug,data.name)}>
                    <a className="dropdown-item" href="#renameCard" data-toggle="modal">
                    <i className="fa fa-pencil"></i>&nbsp;&nbsp; Rename</a>
                    </li>
                    <li onClick={this.handleAudioDelete.bind(this,data.slug)} >
                    <a className="dropdown-item" href="#deleteCard" data-toggle="modal">
                    <i className="fa fa-trash-o"></i>&nbsp;&nbsp; Delete</a>
                    </li>
                    </ul>
                    {/*<!-- End Rename and Delete BLock  -->*/}
                            
                    </div>
                    
                    <div className="clearfix"></div>
                        
                        {/* <div class="inProgressIcon">
                            <i class="fa fa-circle"></i>
                            <span class="inProgressIconText">&nbsp;{story.completed_percentage}&nbsp;%</span>
                            </div> */}
                            
                    {/*<!-- Popover Content link -->*/}
                     <OverlayTrigger trigger="click" rootClose  placement="left" overlay={<Popover id="popover-trigger-focus"><DetailOverlay details={data}/></Popover>}><a  className="pover cursor">
                     <div class="card_icon">
                    <img src={ STATIC_URL + "assets/images/apps_model_icon.png" } alt="LOADING"/>
                    </div>
                    </a></OverlayTrigger>
                    
                    </div>
                    
                 
                    
                    
                    </div>
                    </div>
                    <div className="card-footer">
                    <div className="left_div">
                    <span className="footerTitle"></span>{getUserDetailsOrRestart.get().userName}
                    <span className="footerTitle">{dateFormat(data.created_at, "mmm d,yyyy HH:MM")}</span>
                    </div>

                     
                            </div>
                            </div>
                             <Dialog ref={(el) => { this.dialog = el }} />

                            </div>
            )
        });
        return(<div >
                {
                    (appsAudioList.length>0)
                    ?(appsAudioList)
                    :(<div><div className="text-center text-muted xs-mt-50"><h2>No results found..</h2></div></div>)
                }

                </div>);

  }


}
