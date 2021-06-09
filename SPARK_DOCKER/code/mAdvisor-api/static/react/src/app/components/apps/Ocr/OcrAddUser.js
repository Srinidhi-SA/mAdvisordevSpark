import React from "react";
import { connect } from "react-redux";
import { Modal, Button} from "react-bootstrap";
import store from "../../../store";
import { closeAddUserPopup, saveNewUserDetails, createNewUserAction, saveNewUserProfileDetails , submitNewUserProfileAction, fetchAllOcrUsersAction, setCreateUserLoaderFlag, fetchOcrListByReviewerType} from "../../../actions/ocrActions";
import { STATIC_URL } from "../../../helpers/env.js";
import { MultiSelect } from 'primereact/multiselect';

@connect((store) => {
  return {
    addUserPopupFlag : store.ocr.addUserPopupFlag,
    createUserFlag : store.ocr.createUserFlag,
    curUserSlug : store.ocr.curUserSlug,
    newUserDetails : store.ocr.newUserDetails,
    newUserProfileDetails : store.ocr.newUserProfileDetails,
    ocrUserProfileFlag : store.ocr.ocrUserProfileFlag,
    loaderFlag : store.ocr.loaderFlag,
    ocrReviwersList : store.ocr.ocrReviwersList,
    selectedTabId : store.ocr.selectedTabId,
    appsList: store.ocr.appsList,
  };
})

export class OcrAddUser extends React.Component{
    constructor(props){
        super(props);
        this.state={
			appId:[]
		}
    }

    closeAddUserPopup(){
        this.props.selectedTabId === "none"?this.props.dispatch(fetchAllOcrUsersAction(store.getState().ocr.ocrUserPageNum)):this.props.dispatch(fetchOcrListByReviewerType(parseFloat(this.props.selectedTabId),store.getState().ocr.ocrUserPageNum));
        this.props.dispatch(closeAddUserPopup());
    }
    saveNewUserDetails(e){
        document.getElementById("resetMsg").innerText = ""
        let name = e.target.name;
        let value = e.target.value;
        this.props.dispatch(saveNewUserDetails(name,value));
    }
    submitNewUserDetails(){
        let mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        let paswdFormat=  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,15}$/;
        let userNameFormat= /^(?=.{8,20}$)[^\\._]?[a-zA-Z0-9]+([._][a-zA-Z0-9]+)*[^\\._]?$/;
        let nameFormat= /^([a-zA-Z]){4,}$/;
        
        if(document.getElementById("first_name").value === "" || document.getElementById("last_name").value === "" || document.getElementById("username").value === "" || document.getElementById("email").value === "" || document.getElementById('password1').value === "" || document.getElementById('password2').value === ""){
            document.getElementById("resetMsg").innerText = "Please enter mandatory fields"
        }else if(!nameFormat.test(document.getElementById("first_name").value)){
            document.getElementById("resetMsg").innerText = "First Name should have only alphabets with minimum 4 characters"
        }else if(!nameFormat.test(document.getElementById("last_name").value)){
            document.getElementById("resetMsg").innerText = "Last Name should have only alphabets with minimum 4 characters"
        }else if(!userNameFormat.test(document.getElementById("username").value)){
            document.getElementById("resetMsg").innerText = "Please enter valid User Name"
        }else if(!mailFormat.test(document.getElementById("email").value)){
            document.getElementById("resetMsg").innerText = "Invalid Email Id"
        }else if(!paswdFormat.test(document.getElementById("password1").value)){
            document.getElementById("resetMsg").innerText = "Please enter a strong password"
        }else if(document.getElementById("password1").value != document.getElementById("password2").value){
            document.getElementById("resetMsg").innerText = "Password and Confirm Passwords doesnot match"
        }else{
            document.getElementById("resetMsg").innerText = ""
            this.props.dispatch(setCreateUserLoaderFlag(true));
            this.props.dispatch(createNewUserAction(this.props.newUserDetails));
        }
    }
    saveUserStatus=(e)=>{
        let name=e.target.name;
        let value = e.target.value;
        if(name==="role")
            this.props.dispatch(saveNewUserProfileDetails(name,parseFloat(value)));
        else
            this.props.dispatch(saveNewUserProfileDetails(name,value));
    }
    submitNewUserStatus(){
        if(document.getElementById("role").value === "none" || document.getElementById("is_active").value === "none" || this.state.appId.length==0){
            document.getElementById("resetMsg").innerText = "Please select mandatory fields"
        }else{
            this.setState({appId:[]});
            document.getElementById("resetMsg").innerText = ""
            this.props.dispatch(setCreateUserLoaderFlag(true));
            this.props.dispatch(submitNewUserProfileAction(this.props.newUserProfileDetails,this.props.curUserSlug));
        }
    }
    handleAllAppsOptions=() =>{
        var appList=this.props.appsList.map(i=>i)
          return appList.map(function (item) {
            return { "label": item.displayName, "value": item.app_id };
          });
    }
    handleAppList=()=>{
        this.props.dispatch(saveNewUserProfileDetails("app_list",this.state.appId));
    }
    render(){
        let disabledValue = this.props.createUserFlag?true:false      
        var isMandatory=this.props.createUserFlag?"":"mandate"
            return(
                <Modal className="addUserModel" backdrop="static" show={this.props.addUserPopupFlag} onHide={this.props.createUserFlag?null:this.closeAddUserPopup.bind(this)}>
                    <Modal.Header>
                        <button type="button" className="close" data-dismiss="modal" onClick={this.closeAddUserPopup.bind(this)}>&times;</button>
                        <h4 className="modal-title">Add User</h4>
                    </Modal.Header>
                    <Modal.Body id="addUsers">
                        {!this.props.ocrUserProfileFlag &&
                            <div className="ocrUserFormLabel">
                            <div className="row">
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="first_name">First Name</label>
                                    <input type="text" id="first_name" name="first_name" placeholder="First Name" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue} />
                                </div>
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="last_name" >Last Name</label>
                                    <input type="text" id="last_name" name="last_name" placeholder="Last Name" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue} />
                                </div>
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="username">User Name</label>
                                    <input type="text" id="username" name="username" placeholder="User Name" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue}/>
                                </div>
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="email">Email</label>
                                    <input  type="email" id="email" name="email" placeholder="Email" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue}/>
                                </div>
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="password">Password</label>         
                                    <input type="password" id="password1" name="password1" placeholder="Password" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue}/>
                                </div>
                                <div className="col-sm-6">
                                    <label className={isMandatory} for="confirmPassword">Confirm Password</label>   
                                    <input type="password" id="password2" name="password2" placeholder="Confirm Password" onInput={this.saveNewUserDetails.bind(this)} disabled={disabledValue} />                                       
                                </div>
                            </div>
                                {this.props.createUserFlag &&
                                <div className="row">
                                    <div className="col-sm-12 allApplist">
                                    <label className="mandate">Select required App</label>
                                    <MultiSelect value={this.state.appId} style={{marginBottom:15,width: "100%" }} name="app_list"
                                            options={this.handleAllAppsOptions()} onChange={(e)=> this.setState({appId: e.value},this.handleAppList)}
                                            filter={true} placeholder="Choose Apps" />
                                    </div>
                                    <div className="col-sm-6">
                                    <label className="mandate" for="userRoles">Roles</label>   
                                    <select name="role" id="role" onChange={this.saveUserStatus.bind(this)}>
                                        <option id="none" value="none">--select--</option>
                                         {this.props.ocrReviwersList.map(i=>{return <option key={i.id} value={i.id}>{i.name}</option>})}
                                    </select>  
                                    </div>
                                    <div className="col-sm-6">
                                        <label for="userRoles" className="mandate">Status</label>
                                        <select name="is_active" id="is_active" onChange={this.saveUserStatus.bind(this)}>
                                            <option value="none" id="none" >--select--</option>
                                            <option value="True" id="active">Active</option>
                                            <option value="False" id="inactive">Inactive</option>
                                        </select>
                                    </div>
                                </div>       
                                }
                                {!this.props.ocrUserProfileFlag && !this.props.createUserFlag &&
                                    <div>
                                        <div>Please follow the below format for Username and Password.</div>
                                         <ul className="xs-pl-20">
                                             <li>Username must contain only alphanumeric character, underscore, and dot with 8-20 characters.</li>
                                             <li>Underscore and dot can not be next to each other and multiple times in a row.</li>
                                             <li>Password must contain 8-15 letters with atleast 1 number and 1 special character</li>
                                         </ul>          
                                    </div>  
                                }
                            </div>
                        }
                       {this.props.loaderFlag && !this.props.ocrUserProfileFlag &&
                            <div className="add-editUserLoader">
                                <img className="ocrLoader" src={STATIC_URL + "assets/images/Preloader_2.gif"} />
                            </div>
                        }   
                        {this.props.ocrUserProfileFlag && 
                            <div className="col-md-12 ocrSuccess wow bounceIn" data-wow-delay=".25s" data-wow-offset="20" data-wow-duration="5s" data-wow-iteration="10">
                                <img src={STATIC_URL + "assets/images/success_outline.png"} style={{ height: 105, width: 105, marginTop:"75px" }} />
                                    <span className="userSaved">User Added Successfully</span>
                            </div>
                        }
                    </Modal.Body>
                    <Modal.Footer>
                        <div id="resetMsg" style={{width:'60%'}}></div>
                        {(!this.props.createUserFlag && !this.props.ocrUserProfileFlag)?<Button bsStyle="primary" id="createUserBtn" onClick={this.submitNewUserDetails.bind(this)}>Create User</Button>:""}
                        {!this.props.ocrUserProfileFlag?<Button bsStyle="primary" id="addUser" disabled={this.props.createUserFlag?false:true} onClick={this.submitNewUserStatus.bind(this)}>Save</Button>:""}
                        {this.props.ocrUserProfileFlag?<Button bsStyle="primary" id="addUser" onClick={this.closeAddUserPopup.bind(this)}>Close</Button>:""}
                    </Modal.Footer>
                </Modal>
        );
    }
}