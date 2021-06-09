import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import {updateAlgorithmData, tensorValidateFlag, changeLayerType, addPanels, saveEditTfInput} from "../../actions/appActions";
import Layer from './Layer';
import {statusMessages} from  "../../helpers/helper";


@connect((store) => {
    return {
        algorithmData:store.apps.regression_algorithm_data,
        manualAlgorithmData:store.apps.regression_algorithm_data_manual,
        tensorValidateFlag: store.datasets.tensorValidateFlag,
        datasetRow: store.datasets.dataPreview.meta_data.uiMetaData.metaDataUI[0].value,
        tfAlgorithmSlug: store.apps.regression_algorithm_data_manual.filter(i=>i.algorithmName=="Neural Network (TensorFlow)")[0].algorithmSlug,
        layerType:store.apps.layerType,
        panels:store.apps.panels,
        editmodelFlag:store.datasets.editmodelFlag,
        modelEditconfig: store.datasets.modelEditconfig,
    };
})

export class TensorFlow extends React.Component {

  constructor(props) {
      super(props);
  }

  componentWillMount(){
    if(this.props.editmodelFlag && this.props.panels.length ===0){
      let editTfInput = Object.assign([],this.props.modelEditconfig.config.config.ALGORITHM_SETTING.filter(i=>i.algorithmName==="Neural Network (TensorFlow)")[0].tensorflow_params.hidden_layer_info);
      this.props.dispatch(saveEditTfInput(editTfInput));
      let len = editTfInput.length;
      for(var i=1;i<=len;i++){
        this.props.dispatch(addPanels(i));
      }
    }
  }

  componentDidMount(){
      this.props.dispatch(updateAlgorithmData(this.props.tfAlgorithmSlug,"batch_size",this.props.datasetRow-1,"NonTuningParameter"));
    }
  
  changeTextboxValue(item,e){
      let name = item.name;
      let val = e.target.value === "--Select--"? null:e.target.value;
      if(name=="number_of_epochs" && val<1){
      e.target.parentElement.lastElementChild.innerHTML = "value range is 1 to infinity"
      }
      else if(name=="batch_size" && ((val < 0 ) || (val > this.props.datasetRow-1)||val=="")){
        e.target.parentElement.lastElementChild.innerHTML = `value range is 1 to ${this.props.datasetRow-1}`
      }
      else if(name == "learning_rate" && (val < 0 || val > 1 || val == "")){
        e.target.parentElement.lastElementChild.innerHTML = "value range is 0 to 1"
      }
      else if(name != "learning_rate" && (!Number.isInteger(parseFloat(val)) && val!="")){
        e.target.parentElement.lastElementChild.innerHTML = "Decimals are not allowed"
      }
      else{
        e.target.parentElement.lastElementChild.innerHTML = "" 
        let finalVal = name == "learning_rate" ? Number(val).toString() : Math.trunc(Number(val)).toString()
        this.props.dispatch(updateAlgorithmData(this.props.tfAlgorithmSlug,item.name,finalVal,"NonTuningParameter"));
      }
      if(e.target.parentElement.lastElementChild.innerHTML !=""){
        e.target.classList.add("regParamFocus");
      }else
        e.target.classList.remove("regParamFocus");
  }
  
  handleSelectBox(item,e){
    var loss=$(".loss_tf").val()
    if(e.target.classList.value=="form-control layer_tf"||e.target.classList.value=="form-control optimizer_tf"){
      this.props.dispatch(updateAlgorithmData(this.props.tfAlgorithmSlug,item.name,e.target.value,"NonTuningParameter"));
    }else if(e.target.classList.value=="form-control metrics_tf" && loss=="sparse_categorical_crossentropy" && $(".metrics_tf").val().indexOf("sparse")==-1){
      document.getElementById("loss_tf").innerText=""
      document.getElementsByClassName("loss_tf")[0].classList.remove("regParamFocus");
      document.getElementById("metrics_tf").innerText="Metrics should be sparse."
      document.getElementsByClassName("metrics_tf")[0].classList.add("regParamFocus");
    }
    else if(e.target.classList.value=="form-control loss_tf" && loss!="sparse_categorical_crossentropy" && $(".metrics_tf").val().indexOf("sparse")!=-1){
      document.getElementById("metrics_tf").innerText=""
      document.getElementsByClassName("metrics_tf")[0].classList.remove("regParamFocus",);
      document.getElementById("loss_tf").innerText="Loss should be sparse."
      document.getElementsByClassName("loss_tf")[0].classList.add("regParamFocus");
    }
    else if($(".loss_tf").val().indexOf("sparse")==-1&& $(".metrics_tf").val().indexOf("sparse")!=-1){
      document.getElementById("loss_tf").innerText=""
      document.getElementsByClassName("loss_tf")[0].classList.remove("regParamFocus");
      document.getElementById("metrics_tf").innerText="Metrics should not be sparse."
      document.getElementsByClassName("metrics_tf")[0].classList.add("regParamFocus");
    }
    else if($(".metrics_tf").val().indexOf("sparse")==-1 && $(".loss_tf").val().indexOf("sparse")!=-1){
      document.getElementById("metrics_tf").innerText=""
      document.getElementsByClassName("metrics_tf")[0].classList.remove("regParamFocus");
      document.getElementById("loss_tf").innerText="Loss should not be sparse."
      document.getElementsByClassName("loss_tf")[0].classList.add("regParamFocus");
    }
    else{
      document.getElementById("metrics_tf").innerText=""
      document.getElementById("loss_tf").innerText=""
      document.getElementsByClassName("metrics_tf")[0].classList.remove("regParamFocus");
      document.getElementsByClassName("loss_tf")[0].classList.remove("regParamFocus");
      this.props.dispatch(updateAlgorithmData(this.props.tfAlgorithmSlug,item.name,e.target.value,"NonTuningParameter"));
    }
  }

  getOptions(item) {
      var arr = item.defaultValue.map(j=>{ return {name: j.displayName, sel: j.selected} })
      var selectedOption=arr.filter(i=>i.sel)[0].name
      var options = arr.map(k => {
        return <option key={k.name} value={k.name}> {k.name}</option>
      })
      return <select onChange={this.handleSelectBox.bind(this,item)} defaultValue={selectedOption} className={`form-control ${item.name}_tf`}> {options} </select>
  }
    
  layerValidate=(slectedLayer,tfArray)=>{
      if(tfArray.length>=2)
        var prevLayer=tfArray[tfArray.length-1].layer;
      if(tfArray.length==0 && (slectedLayer=="Dropout"||slectedLayer=="Lambda")){
        bootbox.alert(statusMessages("warning", "First level must be Dense.", "small_mascot"));
        return false
      }
      else if(tfArray.length>=2 && (slectedLayer=="Dropout" && prevLayer=="Dropout"||slectedLayer=="Lambda" && prevLayer=="Lambda")){
        bootbox.alert(statusMessages("warning", "Please select an alternate layer.", "small_mascot"));
        return false
      }
      else{
        this.addLayer(slectedLayer);
      }
  }

  parameterValidate=()=>{
    let unitLength= document.getElementsByClassName("units_tf").length
    let rateLength= document.getElementsByClassName("rate_tf").length
    var errMsgLen=document.getElementsByClassName("error").length

      for(let i=0; i<unitLength; i++){
        var unitFlag;
        if(document.getElementsByClassName("units_tf")[i].value===""){
          document.getElementsByClassName("units_tf")[i].classList.add("regParamFocus");
          unitFlag = true;
        }
      }

      for(let i=0; i<rateLength; i++){
        var rateFlag;
        if(document.getElementsByClassName("rate_tf")[i].value===""){
          rateFlag = true;
          document.getElementsByClassName("rate_tf")[i].classList.add("regParamFocus");
        }
      }
        
      for(let i=0; i<errMsgLen; i++){
        var errMsgFlag;
        if(document.getElementsByClassName("error")[i].innerText!="")
          errMsgFlag = true;
      }

    if (($(".activation_tf option:selected").text().includes("--Select--"))||($(".batch_normalization_tf option:selected").text().includes("--Select--"))||(unitFlag)||(rateFlag)){
      for(let i=0;i<$(".form-control.activation_tf").length;i++){
        if( $(".form-control.activation_tf")[i].value=="--Select--")
          $(".form-control.activation_tf")[i].classList.add("regParamFocus")
      }
      for(let i=0;i<$(".form-control.batch_normalization_tf").length;i++){
        if( $(".form-control.batch_normalization_tf")[i].value=="--Select--")
          $(".form-control.batch_normalization_tf")[i].classList.add("regParamFocus")
      }     
      this.props.dispatch(tensorValidateFlag(false));
      bootbox.alert(statusMessages("warning", "Please enter all the mandatory fields for TensorFlow Algorithm.", "small_mascot"));
    }else if(errMsgFlag){
      this.props.dispatch(tensorValidateFlag(false));
      bootbox.alert(statusMessages("warning", "Please resolve erros to add new layer in TensorFlow.", "small_mascot"));
    }else{
      this.props.dispatch(tensorValidateFlag(true));
    }
     
  }

  addLayer=(slectedLayer)=>{
    const nextId = this.props.panels.length + 1
    this.props.dispatch(changeLayerType(slectedLayer));
    this.props.dispatch(addPanels(nextId));
  }

  handleClick(){ 
    var slectedLayer=document.getElementsByClassName('form-control layer_tf')[0].value //instead of picking slectedLayer from store config, using documentObject of selectBox.
    var tfArray= store.getState().apps.tensorFlowInputs;
    if (tfArray.length>0) {
      this.parameterValidate();
    }
    if(store.getState().datasets.tensorValidateFlag || tfArray.length == 0){
      this.layerValidate(slectedLayer,tfArray)
    }
  }

  render() {
    if(this.props.layerType==="Dense")
      var data=this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[0].parameters
    else if(this.props.layerType==="Dropout")
      data=this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[1].parameters
    var algorithmData=this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters.filter(i=>i.name!="layer")
    var rendercontent = algorithmData.map((item,index)=>{
      if(item.paramType=="list"){
        return (
          <div key={item.name} className ="row mb-20">
            <div className="form-group">
              <label className="col-md-2">{item.displayName}</label>
              <label className="col-md-4">{item.description}</label>
              <div className="col-md-6">
                <div className ="row">
                  <div className="col-md-6">
                    {this.getOptions(item)}
                    <div id={`${item.name}_tf`} className="error"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      }else
        return (
          <div  key={item.name} className ="row mb-20">
            <div class="form-group">
              <label class="col-md-2 control-label read">{item.displayName}</label>
              <label className="col-md-4">{item.description}</label>
              <div className="col-md-6">
                <div className ="row">
                  <div className="col-md-2">
                    <input type="number" className= {`form-control ${item.name}_tf`} onChange={this.changeTextboxValue.bind(this,item)} defaultValue={item.displayName==="Learning Rate"?item.defaultValue:(item.acceptedValue!=""? item.acceptedValue:(item.displayName ==="Batch Size"? this.props.datasetRow -1 : item.defaultValue))}/>
                    <div className="error"></div>
                  </div>
                </div> 
              </div>
            </div>
          </div>
        )
    })
    return (
      <div className="col-md-12">
        <div className="row mb-20">
          <div class="form-group">
            <label class="col-md-2">Layer</label>
            <label className="col-md-4">A layer is a class implementing common Neural Networks Operations, such as convolution, batch norm, etc.</label>
            <div className="col-md-6">
              <div className ="row">
                <div className="col-md-6">
                  {this.getOptions(this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0])}
                </div>
                <div className="col-md-6 text-center">
                  <div style={{cursor:'pointer',display:'inline-block'}} onClick={this.handleClick.bind(this,)}>
                    <span className="addLayer"> <i className="fa fa-plus" style={{color: '#fff'}}></i></span>
                    <span className="addLayerTxt">Add layer</span>
                  </div>            
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className='panel-wrapper'>
          {store.getState().apps.panels.map((panelId) => {
              let tenFlwInp = store.getState().apps.tensorFlowInputs;
              if( (tenFlwInp.length != 0) && (panelId <= tenFlwInp.length)){
                data = (tenFlwInp[panelId-1].layer === "Dense")? this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[0].parameters : this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[1].parameters;
                var layrTyp = tenFlwInp[panelId-1].layer
              }else{
                data = (this.props.layerType === "Dense")? this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[0].parameters : this.props.manualAlgorithmData.filter(i=>i.algorithmName === "Neural Network (TensorFlow)")[0].parameters[0].defaultValue[1].parameters;
                var layrTyp = this.props.layerType
              }
              return (<Layer key={panelId} id={panelId} parameters={data} layerType={layrTyp} />);
            })
          }
        </div>
        <div id="layerArea"></div>
        {rendercontent}
      </div>
    );
  }
}
