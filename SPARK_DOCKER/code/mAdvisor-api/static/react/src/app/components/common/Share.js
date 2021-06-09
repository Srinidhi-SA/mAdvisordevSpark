import React from "react";
import { connect } from "react-redux";
import { MultiSelect } from 'primereact/multiselect';
import { Button, Modal} from "react-bootstrap";
import {closeShareModalAction,handleShareItem} from "../../actions/dataActions";
@connect((store) => {
  return {
    shareItemName: store.datasets.shareItem,
    shareItemSlug: store.datasets.shareItemSlug,
    shareModelShow:store.datasets.shareModelShow,
    shareItemType:store.datasets.shareItemType
  };
})

export class Share extends React.Component {
  constructor(props) {
    super(props);
    this.state={
			userIds:[]
		}
  }

  closeShareModal() {
    this.props.dispatch(closeShareModalAction());
    this.setState({userIds:[]})

  }
  getMultiSelectOptions() {
  var UserNames=Object.values(this.props.usersList.allUsersList).map(i=>i)
    return UserNames.map(function (item) {
      return { "label": item.name, "value": item.Uid };
    });
  }
  proceedToShare(userIds){
    if($(".shareMultiselect .p-multiselect-label").text() === "Choose users"){
      document.getElementById("resetMsg").innerText= "Please Choose user";
    }
    else{
      document.getElementById("resetMsg").innerText= " ";
      handleShareItem(userIds,this.props.shareItemSlug,this.props.shareItemType,this.props.shareItemName);
      this.closeShareModal()
      this.setState({userIds:[]})
    }
  }

  render() {
   var rendermultiselect= (this.props.usersList.allUsersList!=undefined && <div className="form-group">
       <div className="content-section implementation multiselect-demo width-multisel">
       <MultiSelect className="shareMultiselect" value={this.state.userIds} options={this.getMultiSelectOptions()} onChange={(e) => this.setState({userIds: e.value})}
        style={{ minWidth: '22em',maxWidth:"22em",width: "90%"}}  filter={true} placeholder="Choose users" />
       </div>
       </div>)
    var renderOptions =
      (
      <div>
       {rendermultiselect}
      </div>
      )

    return (
<div id="sharePopup" role="dialog" className="modal fade modal-colored-header ">
  <Modal show={this.props.shareModelShow} onHide={this.closeShareModal.bind(this)} dialogClassName="modal-colored-header modal-md modalOpacity" style={{ overflow: 'inherit' }} >
    <Modal.Header>
      <h3 className="modal-title">Share</h3>
    </Modal.Header>
    <Modal.Body style={{minHeight:"320px",minWidth:"10px"}}>
     <div className="row">
     <div className="col-sm-3">
     <label>{this.props.shareItemType} name:</label>
     </div>
     <div className="col-sm-9">
     <h4>{this.props.shareItemName}</h4>
     </div>
     <div className="col-sm-3" style={{paddingTop:"3%"}}>
     <label>Share with:</label>
     </div>
     <div className="col-sm-9" style={{paddingTop:"3%"}}>
              {renderOptions}
     </div>
           
      </div>
    </Modal.Body>
    <Modal.Footer>
    <div id="resetMsg"></div>
      <Button onClick={this.closeShareModal.bind(this)}>Cancel</Button>
      <Button bsStyle="primary" form="shareForm" content="Submit" onClick={this.proceedToShare.bind(this,this.state.userIds)} value="Submit">Share</Button>
    </Modal.Footer>
    </Modal>
  </div>);}}