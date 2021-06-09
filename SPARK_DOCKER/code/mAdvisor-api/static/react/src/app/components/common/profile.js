import React from "react";
import {Scrollbars} from 'react-custom-scrollbars';
import {connect} from "react-redux";
import store from "../../store";
import {isEmpty, getUserDetailsOrRestart} from "../../helpers/helper";
import {STATIC_URL, API} from "../../helpers/env";
import renderHTML from 'react-render-html';
import {saveFileToStore,clearDataUploadFile} from "../../actions/dataSourceListActions";
import Dropzone from 'react-dropzone'
import { Modal, Button } from "react-bootstrap";
import { uploadImg, getUserProfile, saveProfileImage} from "../../actions/loginActions";
import {openImg, closeImg} from "../../actions/dataUploadActions";
import { C3ChartNew } from "../C3ChartNew";

@connect((store) => {
  return {
    profileInfo: store.login.profileInfo, 
    fileUpload: store.dataSource.fileUpload, 
    imgUploadShowModal:store.dataUpload.imgUploadShowModal,
    profileImgURL: store.login.profileImgURL};
})

export class Profile extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
      this.props.dispatch(getUserProfile(getUserDetailsOrRestart.get().userToken))
      this.props.dispatch(saveProfileImage(getUserDetailsOrRestart.get().image_url))
      this.props.dispatch(clearDataUploadFile())

  }

  popupMsg() {
    $("#fileErrorMsg").removeClass("visibilityHidden");
    $("#fileErrorMsg").html("Only PNG and JPEG files are allowed to upload.Please retry.");
  }
  popupMsgForSize() {
    bootbox.alert("Maximum allowed file size is 2MB")
  }
  onDrop(files) {
    this.props.dispatch(saveFileToStore(files))
  }
  openPopup() {
    this.props.dispatch(openImg());
    var files = [
      {
        name: "",
        size: ""
      }
    ]
    this.props.dispatch(saveFileToStore(files))

  }
  closePopup() {
    this.props.dispatch(closeImg())
  }

  uploadProfileImage() {
    if(this.props.fileUpload)
    this.props.dispatch(uploadImg());
    else {
      $("#fileErrorMsg").removeClass("visibilityHidden");
      $("#fileErrorMsg").html("Please select a file");

    }
  }
  resetOnchange=(e)=>{
      if(e.target.value!="")
        document.getElementById("resetMsg").innerText=""
  }

resetPassword=()=>{
  var num=/[0-9]/;
  var char= /[A-Za-z]/;
  if($(".oldPass").val()==="" || $(".newPass").val()==="" || $(".confirmPass").val()===""  ){
    document.getElementById("resetMsg").innerText="Please enter *mandatory fields"
  }
  else if( $(".newPass").val()!= $(".confirmPass").val()){
    document.getElementById("resetMsg").innerText="New password and confirm password should be same"
  }
  else if(($(".newPass").val().length<8) || !char.test($(".newPass").val()) || !num.test($(".newPass").val())){
    document.getElementById("resetMsg").innerText="Password must contain at least 8 characters and can't be entirely numeric."
  }
  else{
    var oldPassword= $(".oldPass").val();
    var newPassword= $(".confirmPass").val();
    this.resetAPI(oldPassword,newPassword).then(([response, json]) =>{
      if(response.status === 200){
        $("#resetModal").modal('hide');
          bootbox.alert(`Password changed successfully.`)
      }
      else{
        document.getElementById("resetMsg").innerText="Old password is wrong"
      }
    })
  }
}
getHeader=(token)=>{
  return {
      'Authorization': token,
      'Content-Type': 'application/json'
  }
}
resetAPI=(oldPassword,newPassword) =>{
   return fetch(API+'/api/change-user-password/',{
      method: 'put',
      headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      body: JSON.stringify({ "old_password": oldPassword, "new_password": newPassword})
   }).then( response => Promise.all([response, response.json()]));
}
  addDefaultSrc(ev) {
    ev.target.src = STATIC_URL + "assets/images/iconp_default.png"
  }

  setDateFormat(created_at){
    let date = new Date( Date.parse(created_at) );
    let fomattedDate=date.toLocaleString('default', { month: 'short' })+" "+date.getDate()+","+date.getFullYear()
   return fomattedDate
   }

   handleErr(e){
		e.target.src =	STATIC_URL + "assets/images/avatar.png"
	}

  render() {
    let lastLogin = null;
    if (getUserDetailsOrRestart.get().last_login != "null") {
      lastLogin = this.setDateFormat(getUserDetailsOrRestart.get().last_login);
    } else {
      lastLogin = this.setDateFormat(new Date());
    }

    if (isEmpty(this.props.profileInfo)) {
      return (
        <div className="side-body">
          <div className="page-head">
            <div className="row">
              <div className="col-md-8">
                <h3 className="xs-mt-0 text-capitalize">My Page</h3>
              </div>
            </div>
          </div>
          <div className="main-content">
            <div>
              <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
            </div>
          </div>
        </div>
      )
    } else {
      var fileName = ""
      var fileSize=0
      if(store.getState().dataSource.fileUpload.length>0){
        fileName=store.getState().dataSource.fileUpload[0].name;
        fileSize=store.getState().dataSource.fileUpload[0].size
      }

      let fileSizeInKB = (fileSize / 1024).toFixed(3)
      if (fileSizeInKB > 2000)
        this.popupMsgForSize()
      let imgSrc = API + this.props.profileImgURL + fileSizeInKB + new Date().getTime();
      let statsList = this.props.profileInfo.info.map((analysis, i) => {
        return (
          <div key={i} className="col-md-2 co-sm-4 col-xs-6">
            <h2 className="text-center text-primary xs-pb-0">{analysis.count}<br/>
              <small>{analysis.displayName}
              </small>
            </h2>
          </div>
        )
      });
      
      let recentActivity = this.props.profileInfo.recent_activity.map((recAct, i) => {

        let img_name = STATIC_URL + "assets/images/iconp_" + recAct.content_type + ".png";
        var timediff = new Date().getTime() - new Date(recAct.action_time).getTime()

        var hoursDifference = Math.floor(timediff / 1000 / 60 / 60);
        var minutesDifference = Math.floor(timediff / 1000 / 60);
        var secondsDifference = Math.floor(timediff / 1000);

        let action_time_string=this.setDateFormat(recAct.action_time)
        if(hoursDifference<60){
          if(hoursDifference==0){
            if(minutesDifference==0)
            action_time_string=secondsDifference+" sec ago"
            else {
              action_time_string=minutesDifference+" min ago"
            }
          }else {
            action_time_string=hoursDifference+" hrs ago"
          }
        }

        let msg=recAct.message_on_ui
        msg=msg.charAt(0).toUpperCase()+msg.slice(1)+"."
        return (
          <li key={i}>
            <img onError={this.addDefaultSrc} src={img_name} className="img-responsive pull-left xs-pl-5 xs-pr-10"/>
            <span className="pull-left xs-pt-10">
              <div class="crop">{msg}</div>
            </span>
            <span className="pull-right xs-pt-10">
              {action_time_string}
            </span>
          </li>
        )
      });
      let chartInfo=[]
      return (
        <div className="side-body">
          <div className="page-head">
            <div className="row">
              <div className="col-md-8">
                <h3 className="xs-mt-0 text-capitalize">My Page</h3>
              </div>
            </div>
          </div>
        
          <div className="main-content">
            <div className="user-profile">
              <div className="panel panel-default xs-mb-15">
                <div className="panel-body no-border box-shadow">
                  <div className="user-display">
                    <div className="user-avatar col-md-2 text-center">
                    {(!this.props.profileImgURL||this.props.profileImgURL==null||this.props.profileImgURL=="null")
                      ?<i className="profileImg_alpha avatar-img img-circle">{getUserDetailsOrRestart.get().userName.substr(0,1).toUpperCase()}</i>
                      :<img src={imgSrc} onError={this.handleErr.bind(this)} className="img-responsive img-center img-circle"/>
                      }
                      <a onClick={this.openPopup.bind(this)} href="javascript:void(0)">
                        <i class="fa fa-camera" style={{
                          fontSize: "36px",
                          color: "grey"
                        }}></i>
                      </a>
                      <div id="uploadImg" role="dialog" className="modal fade modal-colored-header">
                        <Modal show={store.getState().dataUpload.imgUploadShowModal} onHide={this.closePopup.bind(this)} dialogClassName="modal-colored-header uploadData">
                          <Modal.Header closeButton>
                            <h3 className="modal-title">Upload Image</h3>
                          </Modal.Header>
                          <Modal.Body>

                            <div className="row">
                              <div className="col-md-9 col-md-offset-1 col-xs-12">
                                <div className="clearfix"></div>

                                <div style={{paddingTop:65}} className="dropzone md-pl-50">
                                  <Dropzone id={1} onDrop={this.onDrop.bind(this)} accept=".png, .jpg,.jpeg" onDropRejected={this.popupMsg}>
                                    <p>Please drag and drop your file here or browse.</p>
                                  </Dropzone>
                                  <aside>
                                    <ul className={fileName != ""
                                      ? "list-unstyled bullets_primary"
                                      : "list-unstyled"}>
                                      <li>{fileName}</li>
                                      <li className="text-danger visibilityHidden" id="fileErrorMsg">Please select .png or .jpg file to upload.</li>
                                    </ul>
                                  </aside>
                                </div>

                                <div className="xs-pt-10"></div>
                                <div className="clearfix"></div>

                              </div>
                            </div>
                          </Modal.Body>
                          <Modal.Footer>
                            <Button onClick={this.closePopup.bind(this)}>Close</Button>
                            <Button bsStyle="primary" onClick={this.uploadProfileImage.bind(this)}>Upload Image</Button>
                          </Modal.Footer>
                        </Modal>
                      </div>
                    </div>

                    <div className="user-info col-md-10">

                      <div className="panel-default">

                        <div className="panel-body no-border">
                          <div className="row">
                            <div className="col-md-6">
                              <h3>{getUserDetailsOrRestart.get().userName}</h3>
                              <table className="full-table-width no-border no-strip skills">
                                <tbody className="no-border-x no-border-y full-width">
                                  <tr>
                                    <td className="item" width="30">
                                      <span className="fa fa-envelope"></span>
                                    </td>
                                    <td>
                                      <b>
                                        {getUserDetailsOrRestart.get().email}</b>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td className="item xs-pt-5">
                                      <span className="fa fa-phone"></span>
                                    </td>
                                    <td className="xs-pt-5">
                                      <b>
                                        {getUserDetailsOrRestart.get().phone}
                                      </b>
                                    </td>
                                  </tr>
								  <tr>
									<td className="item xs-pt-5">
									</td>
									<td>
										<a data-toggle="modal" data-target="#resetModal" style={{cursor:'pointer'}}>Change Password</a>
									  <div class="modal fade" id="resetModal" role="dialog">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
          <h4 class="modal-title">Change Password</h4>
        </div>
        <div class="modal-body">
        <div className="row mt-18">
         <div className="col-sm-4">
          <label className="mandate">Old Password:</label>
         </div>
        <div className="col-sm-8">
          <input className="form-control oldPass" type="password" onChange={this.resetOnchange}/>
       </div>
        </div>
        <div className="row mt-18">
         <div className="col-sm-4">
          <label className="mandate">New Password:</label>
         </div>
        <div className="col-sm-8">
        <input className="form-control newPass" type="password" onChange={this.resetOnchange}/>
       </div>
        </div>
        <div className="row mt-18">
         <div className="col-sm-4">
          <label className="mandate">Confirm New Password:</label>
         </div>
        <div className="col-sm-8">
        <input className="form-control confirmPass" type="password" onChange={this.resetOnchange}/>
       </div>
        </div>
      </div>
      <div class="modal-footer" style={{marginTop: 18}}>
          <div id="resetMsg"></div>
          <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" onClick={this.resetPassword}>Save</button>
        </div>
    </div>
  </div>
  </div>
                  </td>
								  </tr>
                                </tbody>
                              </table>
                            </div>
                            <div className="col-md-3 col-md-offset-3">
                              <p className="xs-pt-30">
                                Date Joined :&nbsp;
                                <b>
                                  {this.setDateFormat(getUserDetailsOrRestart.get().date)}</b>
                                <br/>
                                Last Login :&nbsp;
                                <b>{lastLogin}</b>
                                <br/>
                                User type:&nbsp;
                                <b>{(getUserDetailsOrRestart.get().is_superuser==true)?"Super user":"User"}</b>

                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="clearfix"></div>
                  </div>
                  <div className="clearfix"></div>
                  <div className="row text-center">

                    {statsList}
                  </div>
                </div>
              </div>
            </div>
            <div className="row">
              <div className="col-md-4">
                <div className="panel xs-mb-0">
                  <div className="panel-body no-border box-shadow">
                    <div className="minHP">
                      <h5 class="text-center">TOTAL SPACE</h5>
                      <C3ChartNew chartInfo={chartInfo} classId="_profile" data={this.props.profileInfo.chart_c3}/>
                      <div className="xs-pl-20">{renderHTML(this.props.profileInfo.comment)}</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-8">
                <div className="row">
                  <div className="col-md-12 text-right hidden">
                    <p className="xs-p-20">
                      <br/>
                      Date Joined :
                      <b>
                        {this.setDateFormat(getUserDetailsOrRestart.get().date)}</b>
                      <br/>
                      Last Login :
                      <b>{lastLogin}</b>
                      <br/>
                      User type:
                      <b>{(getUserDetailsOrRestart.get().is_superuser)?"Super user":"User"}</b>

                    </p>
                  </div>
                  <div className="clearfix"></div>
                  <div className="col-md-12">
                    <div className="panel xs-mb-0">
                      <div className="panel-body no-border box-shadow">
                        <div className="minHP">
                          <h5>RECENT ACTIVITY</h5>
                          <Scrollbars style={{ height: 302 }} renderTrackHorizontal={props => <div {...props} className="track-horizontal" style={{
                            display: "none"
                          }}/>} renderThumbHorizontal={props => <div {...props} className="thumb-horizontal" style={{
                            display: "none"
                          }}/>}>

                            <ul className="list-unstyled recActivity">
                              {recentActivity}
                            </ul>
                          </Scrollbars>
                        </div>
                      </div>
                    </div>
                  </div>
                <div className="clearfix"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

      );
    }

  }
}
