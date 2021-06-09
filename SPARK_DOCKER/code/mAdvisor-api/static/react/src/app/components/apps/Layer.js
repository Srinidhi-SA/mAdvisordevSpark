import React, { Component } from 'react'
import {updateTensorFlowArray,addTensorFlowArray,deleteTensorFlowArray} from '../../actions/appActions'
import store from "../../store";
import { connect } from "react-redux";
import {statusMessages} from  "../../helpers/helper";

@connect((store) => {
	return {
    tensorFlowInputs:store.apps.tensorFlowInputs,
  };
})

export default class Layer extends Component {

  componentDidMount(){
    if(this.props.tensorFlowInputs[this.props.id-1] === undefined)
      this.props.dispatch(addTensorFlowArray(this.props.id,this.props.layerType))
  }
    
  shouldComponentUpdate(nextProps){
    return false
  }

  myChangeHandler(item,e){
    let name = item.name;
    let val = e.target.value === "--Select--"? null:e.target.value; 
    if(name=="units" && val<1){
      e.target.parentElement.lastElementChild.innerHTML = "value range is 1 to infinity"
    }else if(name=="units" &&!Number.isInteger(parseFloat(e.target.value))){
      e.target.parentElement.lastElementChild.innerHTML = "Decimals are not allowed"
    }else if(name=="rate" &&(val<=0||val>=1)){
      e.target.parentElement.lastElementChild.innerHTML = "value range is 0.1 to 0.9"
    }else{
    e.target.parentElement.lastElementChild.innerHTML=""
    val=name=="units"?Math.trunc(Number(val)).toString():val
    this.props.dispatch(updateTensorFlowArray(this.props.id,name,val))
    }
    if(e.target.parentElement.lastElementChild.innerHTML !=""){
      e.target.classList.add("regParamFocus");
    }else
      e.target.classList.remove("regParamFocus");
  }

  getOptions(item) {
    var arr = item.defaultValue.map(j=>j.displayName);
    arr.unshift("--Select--")
    var selectedValue = "";
    if(this.props.tensorFlowInputs[this.props.id-1] != undefined){
      selectedValue = this.props.tensorFlowInputs[this.props.id-1][item.name]
    }
    var optionsHtml = arr.map(k => {
      return <option key={k} value={k}> {k}</option>
    })
    return <div className= {`${item.name}_tf`}><select className= {`form-control ${item.name}_tf`} defaultValue={selectedValue!=""?selectedValue:""} onChange={this.myChangeHandler.bind(this,item)}>{optionsHtml} </select>  <div className="error"></div></div>
  }

  deleteLayer=(id)=>{
    var tfLayerList=this.props.tensorFlowInputs.filter(i=>i!==null).map(i=>i.layer).filter(i=>i!=null)
    var arrayToId=this.props.tensorFlowInputs.filter(i=>i!==null).findIndex(p => p.layerId == id)
    var currLayer=tfLayerList[arrayToId],prevLayer=tfLayerList[arrayToId-1];
    var nextLayer=tfLayerList.length!=arrayToId?tfLayerList[arrayToId+1]:"";
    if(arrayToId==0 && nextLayer=="Dropout"){
      bootbox.alert(statusMessages("warning", "First layer should not be a Dropout.", "small_mascot"));
    }
    else if(tfLayerList.length>=2 && currLayer==="Dense" && prevLayer==="Dropout" && nextLayer==="Dropout"){
      bootbox.alert(statusMessages("warning", "Consecutive Dropout layers are not allowed.", "small_mascot"));
    }else{
      document.getElementById(id).innerHTML=""
      this.props.dispatch(deleteTensorFlowArray(id))
    }
  }
  
  render() { 
    var mandateField= ["Activation","Units","Rate","Batch Normalization","use_bias"]
    var rendercontent = this.props.parameters.map((item,index)=>{
      if(item.paramType=="list"){
        return (
          <div key={item.displayName} className ="row mb-20">
            <div className="form-group">
              <label className={mandateField.includes(item.displayName)? "col-md-2 mandate" : "col-md-2"}>{item.displayName}</label>
              <label className="col-md-4">{item.description}</label>
              <div className="col-md-6">
                <div className ="row">
                  <div className="col-md-6">
                    {this.getOptions(item)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      }else{
        var defVal = ""
        if(this.props.tensorFlowInputs[this.props.id-1] != undefined){
          defVal = this.props.tensorFlowInputs[this.props.id-1][item.name]
        }
        return (
          <div key={item.name} className ="row mb-20">
            <div className="form-group">
              <label className={mandateField.includes(item.displayName)? "col-md-2 mandate" : "col-md-2"}>{item.displayName}</label>
              <label className="col-md-4">{item.description}</label>
              <div className="col-md-6">
                <div className ="row">
                  <div className= "col-md-2">
                    <input type="number" className={`form-control ${item.name}_tf`}  name={item.name} onChange={this.myChangeHandler.bind(this,item)} defaultValue={defVal}></input>
                    <div className="error"></div>
                  </div>
                </div> 
              </div>
            </div>
          </div>       
        )
      }
    })
    return ( 
      <div id={this.props.id}>
        <div className="row layerPanel" >
          <div className="layer">
            <div className="layerHeader">
              {this.props.layerType}
              <i className="fa fa-chevron-up" type="button" data-toggle="collapse" data-target={`#collapseExample${this.props.id}`} aria-expanded="true" aria-controls={`collapseExample${this.props.id}`}></i>
              <i onClick={this.deleteLayer.bind(this,this.props.id)} className="fa fa-trash-o" type="button"></i>
            </div>
            <div className="collapse in" id={`collapseExample${this.props.id}`}>
              <div className="card card-body">
                <div className="layerBody">
                  {rendercontent}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
