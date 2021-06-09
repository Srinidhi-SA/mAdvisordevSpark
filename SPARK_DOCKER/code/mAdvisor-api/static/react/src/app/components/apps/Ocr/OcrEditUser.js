import React from "react";
import { connect } from "react-redux";
import { Modal, Button} from "react-bootstrap";
import store from "../../../store";
import { fetchAllOcrUsersAction, closeEditUserModalAction, enableEditingUserAction, SaveEditedUserDetailsAction, submitEditUserDetailsAction, setCreateUserLoaderFlag, submitEditedUserRolesAction, editDetailsFormAction, editRolesFormAction, fetchOcrListByReviewerType} from "../../../actions/ocrActions";
import { STATIC_URL } from "../../../helpers/env.js";
import { MultiSelect } from 'primereact/multiselect';

@connect((store) => {
  return {
    editOcrUserFlag : store.ocr.editOcrUserFlag,
    enableEditingFlag : store.ocr.enableEditingFlag,
    editedUserDetails : store.ocr.editedUserDetails,
    loaderFlag : store.ocr.loaderFlag,
    editUserSuccessFlag : store.ocr.editUserSuccessFlag,
    roleFormSel : store.ocr.roleFormSel,
    detailsFormSel : store.ocr.detailsFormSel,
    selUserSlug : store.ocr.selUserSlug,
    ocrReviwersList : store.ocr.ocrReviwersList,
    selectedTabId : store.ocr.selectedTabId,
    appsList: store.ocr.appsList,
  };
})

export class OcrEditUser extends React.Component{
    constructor(props){
        super(props);
        this.state={
			appId: this.props.selectedAppList
		}
    }

    componentDidUpdate(){
        if(this.props.enableEditingFlag){

            document.getElementById("first_name").disabled=false
            document.getElementById("last_name").disabled=false
            document.getElementById("username").disabled=false
            document.getElementById("email").disabled=false
            document.getElementById("role").disabled=false
            document.getElementById("is_active").disabled=false
            document.getElementById("appList").classList.remove("applist-disabled")

            document.getElementById("fname").classList.add("mandate")
            document.getElementById("lname").classList.add("mandate")
            document.getElementById("uname").classList.add("mandate")
            document.getElementById("mail").classList.add("mandate")
            document.getElementById("rtype").classList.add("mandate")
            document.getElementById("iactive").classList.add("mandate")   
        }
    }

    closeEditUserModal(){
        this.props.selectedTabId === "none"?this.props.dispatch(fetchAllOcrUsersAction(store.getState().ocr.ocrUserPageNum)):this.props.dispatch(fetchOcrListByReviewerType(parseFloat(this.props.selectedTabId),store.getState().ocr.ocrUserPageNum));
        this.props.dispatch(enableEditingUserAction(false));
        this.props.dispatch(closeEditUserModalAction(false));
    }
    enableEditingUser(){
        this.props.dispatch(enableEditingUserAction(true));
    }
    saveuserEditedDetails(e){
        this.props.dispatch(SaveEditedUserDetailsAction(e.target.name,e.target.value));
    }
    saveAppList=()=>{
        document.getElementById("resetMsg").innerText = "";
        this.props.dispatch(editRolesFormAction(true));
        this.props.dispatch(SaveEditedUserDetailsAction("appList",this.state.appId));
    }
    submitEditedForms(){
        let mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if(document.getElementById("first_name").value === ""||document.getElementById("last_name").value === "" || document.getElementById("username").value === "" || document.getElementById("email").value === "" ){
            document.getElementById("resetMsg").innerText = "Please enter mandatory fields"
        }
        else if(!mailFormat.test(document.getElementById("email").value)){
            document.getElementById("resetMsg").innerText = "Invalid Email"
        }
        else if(!this.props.roleFormSel && !this.props.detailsFormSel){
            document.getElementById("resetMsg").innerText = "No changes to save"
        }
        else if(this.props.roleFormSel && this.props.detailsFormSel){
            document.getElementById("resetMsg").innerText = ""
            this.props.dispatch(setCreateUserLoaderFlag(true))

            let allowedVariables1 = ["email","first_name","last_name","username"];
            let filteredVariables1 = Object.keys(this.props.editedUserDetails).filter(key => allowedVariables1.includes(key)).reduce((obj, key) => {
                obj[key] = this.props.editedUserDetails[key];
                return obj;
            }, {});
            this.props.dispatch(submitEditUserDetailsAction(filteredVariables1));
            let allowedVariables2 = ["role","is_active"];
            let filteredVariables2 = Object.keys(this.props.editedUserDetails).filter(key => allowedVariables2.includes(key)).reduce((obj, key) => {
                obj[key] = this.props.editedUserDetails[key];
                return obj;
            }, {});
            this.props.dispatch(submitEditedUserRolesAction(filteredVariables2,this.props.ocrReviwersList,this.props.selUserSlug));
        }
        else if(this.props.detailsFormSel){
            document.getElementById("resetMsg").innerText = ""
            this.props.dispatch(setCreateUserLoaderFlag(true))
            let allowedVariables1 = ["email","first_name","last_name","username"];
            let filteredVariables1 = Object.keys(this.props.editedUserDetails).filter(key => allowedVariables1.includes(key)).reduce((obj, key) => {
                obj[key] = this.props.editedUserDetails[key];
                return obj;
            }, {});
            this.props.dispatch(submitEditUserDetailsAction(filteredVariables1));
        }
        else if(this.props.roleFormSel){
            if(document.getElementById("role").value === "none" || document.getElementById("is_active").value === "none"  || this.props.editedUserDetails.appList.length === 0){
                document.getElementById("resetMsg").innerText = "Please enter mandatory fields"
            }else{
                document.getElementById("resetMsg").innerText = ""
                this.props.dispatch(setCreateUserLoaderFlag(true))
                let allowedVariables = ["role","is_active","appList"];
                let filteredVariables = Object.keys(this.props.editedUserDetails).filter(key => allowedVariables.includes(key)).reduce((obj, key) => {
                    obj[key] = this.props.editedUserDetails[key];
                    return obj;
                }, {});
                this.props.dispatch(submitEditedUserRolesAction(filteredVariables,this.props.ocrReviwersList,this.props.selUserSlug));    
            }
        }
    }

    updateFormSelected(e){
        document.getElementById("resetMsg").innerText = ""
        if(e.currentTarget.id === "userProfileDetails"){
            this.props.dispatch(editDetailsFormAction(true));
        }else{
            this.props.dispatch(editRolesFormAction(true));
        }
    }
    handleAllAppsOptions=() =>{
        var appList=this.props.appsList.map(i=>i)
          return appList.map(function (item) {
            return { "label": item.displayName, "value": item.app_id };
          });
        }

    render(){
        return(
            <Modal backdrop="static" className="editUser" show={this.props.editOcrUserFlag} onHide={this.closeEditUserModal.bind(this)}>
                <Modal.Header>
                    <button type="button" className="close" data-dismiss="modal" onClick={this.closeEditUserModal.bind(this)}>&times;</button>
                    <h4 className="modal-title">Edit User</h4>
                </Modal.Header>
                <Modal.Body id="editUsers">
                        {!this.props.editUserSuccessFlag &&
                            <div className="ocrUserFormLabel" >
                                <form role="form" id="userProfileDetails" onChange={this.updateFormSelected.bind(this)}>
                                    <div className="row">
                                        <div className="col-sm-6">
                                            <label id="fname" for="first_name">First Name</label>
                                            <input type="text" id="first_name" name="first_name" placeholder="First Name" defaultValue={this.props.editedUserDetails.first_name} disabled onInput={this.saveuserEditedDetails.bind(this)} />
                                        </div>
                                        <div className="col-sm-6">
                                            <label id="lname" for="last_name">Last Name</label>
                                            <input type="text" id="last_name" name="last_name" placeholder="Last Name" defaultValue={this.props.editedUserDetails.last_name} disabled onInput={this.saveuserEditedDetails.bind(this)} />
                                        </div>
                                        <div className="col-sm-6">
                                        <label id="uname" for="username">User Name</label>
                                            <input type="text" id="username" name="username" placeholder="User Name" defaultValue={this.props.editedUserDetails.username} disabled onInput={this.saveuserEditedDetails.bind(this)} />
                                        </div>
                                        <div className="col-sm-6">
                                            <label id="mail" for="email">Email</label>
                                            <input type="email" id="email" name="email" placeholder="Email" defaultValue={this.props.editedUserDetails.email} disabled onInput={this.saveuserEditedDetails.bind(this)} />
                                        </div>
                                    </div>
                                </form>
                                <form role="form" id="userProfileRoles" onChange={this.updateFormSelected.bind(this)}>
                                <div className="row">
                                    <div className="col-sm-12 allApplist">
                                        <label className="mandate xs-mb-5" >Select required App</label>
                                        <MultiSelect id="appList" className="applist-disabled"
                                        value={this.state.appId} style={{width: "100%" }} name="app_list" 
                                        options={this.handleAllAppsOptions()} onChange={(e)=>this.setState({appId:e.value},this.saveAppList)}
                                        filter={true} placeholder="Choose Apps" />
                                    </div>
                                    <div className="col-sm-6">
                                        <label id="rtype" for="role">Roles</label>
                                        <select name="role" id="role" disabled onChange={this.saveuserEditedDetails.bind(this)} defaultValue={this.props.editedUserDetails.role != undefined?this.props.editedUserDetails.role:"none"}>
                                            <option key={'none'} id="none" value="none">--select--</option>
                                            {this.props.ocrReviwersList.map(i=>{return <option key={i.id} value={i.name}>{i.name}</option>})}
                                        </select>
                                    </div>
                                    <div className="col-sm-6">
                                        <label id="iactive" for="is_active">Status</label>
                                        <select name="is_active" id="is_active" disabled onChange={this.saveuserEditedDetails.bind(this)} defaultValue={this.props.editedUserDetails.is_active}>
                                            <option value="none" id="none">--select--</option>
                                            <option value="True" id="active">Active</option>
                                            <option value="False" id="inactive">Inactive</option>
                                        </select>
                                    </div >
                                </div>
                                </form>
                            </div>
                        }
                        {this.props.loaderFlag && !this.props.editUserSuccessFlag &&
                            <div className="add-editUserLoader" >
                                <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                            </div>
                        }
                        {this.props.editUserSuccessFlag &&
                             <div className="ocrSuccess wow bounceIn" data-wow-delay=".25s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10">
                                <img src={STATIC_URL + "assets/images/success_outline.png"} style={{width: 105 }} />
                                 <span className="userSaved">Saved Successfully</span>
                            </div>
                        }
                </Modal.Body>
                <Modal.Footer>
                    <div id="resetMsg"></div>
                    {!this.props.enableEditingFlag?<Button bsStyle="primary" id="editUser" onClick={this.enableEditingUser.bind(this)}>Edit</Button>:""}
                    {this.props.enableEditingFlag && !this.props.editUserSuccessFlag?<Button bsStyle="primary" id="saveEditedUser" onClick={this.submitEditedForms.bind(this)}>Save</Button>:""}
                    <Button bsStyle="default" onClick={this.closeEditUserModal.bind(this)}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}