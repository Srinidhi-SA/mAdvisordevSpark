import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import { setPyTorchLayer, updateAlgorithmData, pytorchValidateFlag, deletePyTorchLayer } from "../../actions/appActions";

@connect((store)=>{
    return{
        pyTorchLayer:store.apps.pyTorchLayer,
        idLayer:store.apps.idLayer,
    }
})

export class PyLayer extends React.Component {
    constructor(props){
        super(props);
    }

    deleteLayer(layerNumber){
        let newIdArray = this.props.idLayer.filter(function (items) {
            return items != layerNumber
        });
        this.props.dispatch(deletePyTorchLayer(layerNumber,newIdArray));
    }

    selectHandleChange(parameterData,e){
        e.target.classList.remove("regParamFocus")
        if(parameterData.name === "activation" && (e.target.value === "ReLU" || e.target.value === "LeakyReLU") ){
            $("#suggest_pt")[0].innerHTML = "Select Kaiming Normal or Kaiming Unifrom from  weight_init for best results";
        }
        else if(parameterData.name === "activation" && (e.target.value === "Tanh" || e.target.value === "Sigmoid") ){
            $("#suggest_pt")[0].innerHTML = "Select Xavier Normal or Xavier Unifrom from  weight_init for best results";
        }else if(parameterData.name === "activation"){
            $("#suggest_pt")[0].innerHTML = ""
        }
        if(this.props.idNum === 1 && parameterData.name === "activation" && e.target.value != "Sigmoid" && ($(".loss_pt")[0].value === "NLLLoss" || $(".loss_pt")[0].value === "BCELoss") ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Please select Sigmoid as Loss is "+ $(".loss_pt")[0].value
            e.target.classList.add('regParamFocus')        
        }else if(parameterData.name === "weight_init" && e.target.value === "Dirac"){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Used only for Image Data"
            e.target.classList.add('regParamFocus')
        }else{
            e.target.parentElement.lastElementChild.innerText = ""
            this.props.dispatch(pytorchValidateFlag(true));
            let layerArry = this.props.idNum;
            if(parameterData.name === "activation" || parameterData.name === "batchnormalization" || parameterData.name === "dropout" || parameterData.name === "bias_init" || parameterData.name === "weight_init"){
                let layerDt = this.props.pyTorchLayer[layerArry];
                if(layerDt[parameterData.name].name != e.target.value){
                    layerDt[parameterData.name] = {"name":"None"}
                }
                layerDt[parameterData.name].name = e.target.value;
                let defValArr = parameterData.defaultValue.filter(i=>(i.name===e.target.value))[0];
                if(defValArr != undefined)
                    if(defValArr.parameters != null)
                        defValArr.parameters.map(idx=>{
                            if(idx.name === "add_bias_kv" || idx.name === "add_zero_attn" || idx.name === "bias" || idx.name === "head_bias" || idx.name === "affine" || idx.name === "track_running_stats" || idx.name === "num_parameters" || idx.name === "mode" || idx.name === "nonlinearity"){
                                let subDefaultVal = idx.defaultValue.filter(sel=>sel.selected)[0];
                                let defVal = layerDt[parameterData.name];
                                if(subDefaultVal === undefined){
                                    subDefaultVal = "None";
                                    defVal[idx.name] = subDefaultVal;
                                }
                                else
                                    defVal[idx.name] = subDefaultVal.displayName;
                            }else{
                                let defVal = layerDt[parameterData.name];
                                defVal[idx.name] = idx.defaultValue;
                            }
                        });
                this.props.dispatch(setPyTorchLayer(parseInt(layerArry),layerDt,parameterData.name))
            }else if(parameterData.name === "weight_constraint"){
                let layerDt = this.props.pyTorchLayer[layerArry];
                if(layerDt[parameterData.name].name != e.target.value){
                    layerDt[parameterData.name] = {"constraint":"None"}
                }
                if(e.target.value){
                    layerDt[parameterData.name].constraint = e.target.value
                    let defValArr = parameterData.defaultValue.filter(i=>(i.name===e.target.value))[0];
                    if(defValArr != undefined)
                        if(defValArr.parameters != null)
                            defValArr.parameters[0].map(idx=>{
                                let defVal = layerDt[parameterData.name];
                                defVal[idx.name] = idx.defaultValue;
                            });
                    this.props.dispatch(setPyTorchLayer(parseInt(layerArry),layerDt,parameterData.name))
                }
            }else{
                let newLyrVal = this.props.pyTorchLayer[layerArry];
                newLyrVal[parameterData.name] = e.target.value;
                let defValArr = parameterData.defaultValue.filter(i=>(i.name===e.target.value))[0];
                defValArr.parameters.map(idx=>{
                    let defVal = layerDt[parameterData.name];
                    defVal[idx.name] = idx.defaultValue;
                });
                this.props.dispatch(pytorchValidateFlag(true));
                this.props.dispatch(setPyTorchLayer(parseInt(layerArry),newLyrVal))
            }
            this.props.dispatch(updateAlgorithmData(this.props.parameterData.algorithmSlug,parameterData.name,e.target.value,this.props.type));
        }
    }

    changeTextBoxValue(parameterData,e){
        let val = e.target.value;
        if(!Number.isInteger(parseFloat(val)) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Enter a positive integer"
            e.target.classList.add('regParamFocus')        
        }
        else if(val === ""){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Enter value"
            e.target.classList.add('regParamFocus')        
        }
        else if(val<=0){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Enter value greater than 0"
            e.target.classList.add('regParamFocus')        
        }else{
            this.props.dispatch(pytorchValidateFlag(true));
            e.target.parentElement.lastElementChild.innerText = ""
            e.target.classList.remove('regParamFocus')        
            let layerArry = this.props.idNum
            let newLyrVal = this.props.pyTorchLayer[layerArry];
            newLyrVal[parameterData.name] = parseInt(val);
            this.props.dispatch(setPyTorchLayer(parseInt(layerArry),newLyrVal))
        }
        if(document.getElementsByClassName("batchnormalization_pt")[this.props.idNum-1].value === "BatchNorm1d"){
            document.getElementsByClassName("num_features_pt")[this.props.idNum-1].value = e.target.value;
            let layerArry = this.props.idNum;
            let newLyrVal = this.props.pyTorchLayer[layerArry];
            newLyrVal.batchnormalization.num_features = parseInt(e.target.value)
            this.props.dispatch(setPyTorchLayer(parseInt(layerArry),newLyrVal))
        }
    }
    setChangeLayerSubParams(subparameterData,defaultParamName,e){
        this.props.dispatch(pytorchValidateFlag(true));
        e.target.parentElement.lastElementChild.innerText = ""
        e.target.classList.remove('regParamFocus')   
        let layerArry = this.props.idNum
        let newsubLyrVal = this.props.pyTorchLayer[layerArry];
        newsubLyrVal[defaultParamName][subparameterData.name] = e.target.value;
        this.props.dispatch(setPyTorchLayer(parseInt(layerArry),newsubLyrVal));
    }
    setLayerSubParams(subparameterData,defaultParamName,e){
        let name = subparameterData.name;
        let val = e.target.value;
        if( (name === "alpha" || name === "lambd" || name === "max_val" || name === "negative_slope" || name === "init" || name === "num_parameters" || name === "lower" || name === "upper" || name === "momentum" || name === "eps" || name === "p") && (val>1 || val<0 || val === "")){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is 0 to 1"
            e.target.classList.add('regParamFocus')        
        }
        else if(name === "min_val" && (val>1 || val<-1 || val === "")){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is -1 to 1"
            e.target.classList.add('regParamFocus')        
        }
        else if( name === "min_val" && ($(".min_val_pt")[this.props.idNum-1].value > $(".max_val_pt")[this.props.idNum-1].value)){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "min_val should be less than max_val"
            e.target.classList.add('regParamFocus')        
        }
        else if(name === "max_val" && ($(".min_val_pt")[this.props.idNum-1].value > $(".max_val_pt")[this.props.idNum-1].value)){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "max_val should be greater than min_val"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "embed_dim" || name === "num_heads" || name === "kdim" || name === "vdim" || name === "beta" || name === "threshold" || name === "div_value") && (val<0 || val === "")){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Enter a positive integer"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "n_classes" || name === "dim") && val<0){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Enter a positive integer"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "embed_dim" || name === "num_heads" || name === "dim" || name === "n_classes" || name === "kdim" || name === "vdim") && !Number.isInteger(parseFloat(val)) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Decimals not allowed"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "lower_bound" || name === "upper_bound") && $(".input_unit_pt")[0].value === ""){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Please enter Input units"
            e.target.classList.add('regParamFocus')        
        }
        else if( name === "lower_bound" && (val< (-1/Math.sqrt($(".input_unit_pt")[0].value)) || val==="") ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Value should be greater than "+ (-1/Math.sqrt($(".input_unit_pt")[0].value))
            e.target.classList.add('regParamFocus')        
        }
        else if( name === "upper_bound" && (val> (1/Math.sqrt($(".input_unit_pt")[0].value)) || val === "") ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Value should be greater than "+ 1/Math.sqrt($(".input_unit_pt")[0].value)
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "lower_bound" || name === "upper_bound")&& ( $(".lower_bound_pt")[0].value>$(".upper_bound_pt")[0].value )){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "Lower bound must be less than Upper bound"
            e.target.classList.add('regParamFocus')        
        }
        else if(defaultParamName === "weight_init" && name === "std" && (val<=0 || val>5)){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is 1 to 5"
            e.target.classList.add('regParamFocus')        
        }
        else if( ( name === "std" || name === "a" || name === "sparsity") && ( val<-1 || val>1 || val==="" ) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is -1 to 1"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "mean" || name === "min" || name === "max")  && ( val<0 || val>1 || val==="" ) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is 0 to 1"
            e.target.classList.add('regParamFocus')        
        }
        else if( name === "gain"  && ( val<0 || val>2 || val==="" ) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is 0 to 2"
            e.target.classList.add('regParamFocus')        
        }
        else if( (name === "val" || name === "sparsity")  && ( val<-2 || val>2 || val==="" ) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "value range is -2 to 2"
            e.target.classList.add('regParamFocus')        
        }
        else if( ($("#min_pt")[0]!=undefined && $("#max_pt")[0]!=undefined) && ($("#min_pt")[0].value > $("#max_pt")[0].value) ){
            this.props.dispatch(pytorchValidateFlag(false));
            e.target.parentElement.lastElementChild.innerText = "min should be less than max"
            e.target.classList.add('regParamFocus')        
        }
        else{
            this.props.dispatch(pytorchValidateFlag(true));
            e.target.parentElement.lastElementChild.innerText = ""
            e.target.classList.remove('regParamFocus')        
            let layerArry = this.props.idNum
            let newsubLyrVal = this.props.pyTorchLayer[layerArry];
            newsubLyrVal[defaultParamName][subparameterData.name] = parseFloat(e.target.value);
            this.props.dispatch(setPyTorchLayer(parseInt(layerArry),newsubLyrVal));
        }
    }

    getsubParams(item,defaultParamName){
        if(defaultParamName === "weight_constraint"){
            item = item[0]
        }
        let arr1 = []
        for(var i=0;i<item.length;i++){
            switch(item[i].uiElemType){
                case "textBox":
                    var mandateField = ["alpha","lambd","min_val","max_val","negative_slope","dropout","kdim","vdim","init","lower","upper","beta","threshold","threshold","value","div_value","eps","momentum","lower bound","upper bound","mean","std","val","gain","a","sparsity"];
                    let itemName = item[i].name;
                    if(item[i].name === "num_features"){
                        var defVal = this.props.pyTorchLayer[this.props.idNum][defaultParamName][itemName];
                        if(this.props.pyTorchLayer[this.props.idNum].units_op != "None"){
                            defVal = parseInt(this.props.pyTorchLayer[this.props.idNum].units_op)
                        }
                        var disableField = true;
                    }else{
                        var defVal = this.props.pyTorchLayer[this.props.idNum][defaultParamName][itemName];
                        var disableField = false;
                    }
                    arr1.push(
                        <div key={item[i].name} class="row mb-20">
                            <label className={mandateField.includes(item[i].displayName)? "col-md-2 mandate" : "col-md-2"}>{item[i].displayName}</label>
                            <label className ="col-md-4">{item[i].description}</label>
                            <div className="col-md-1">
                                <input type="number" key={`form-control ${item[i].name}_pt`} class={`form-control ${item[i].name}_pt`} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault() } defaultValue={defVal} onChange={this.setLayerSubParams.bind(this,item[i],defaultParamName)} disabled={disableField}/>
                                <div key={`${item[i].name}_pt`} className="error_pt"></div>
                            </div>
                        </div>
                    );
                    break;
                case "checkbox":
                        var options = item[i].defaultValue.map(i=>{ return {name: i.displayName, sel: i.selected} })
                        var mandateField = ["bias","add_bias_kv","add_zero_attn","head_bias","track_running_stats","affine","num_parameters","mode","nonlinearity"];
                        var selectedValue = ""
                        var sel = ""
                        sel = this.props.pyTorchLayer[this.props.idNum][defaultParamName][item[i].name];
                        var optionsTemp = []
                        optionsTemp.push(<option key={'None'} value="None">--select--</option>)
                        options.map((k,index) => {
                            if(k.name === sel)
                                selectedValue = true;
                            else selectedValue = false;
                            optionsTemp.push(<option key={k.name}value={k.name}> {k.name}</option>)
                        })
                        arr1.push(
                            <div key={item[i].name} class="row mb-20">
                                <label className={mandateField.includes(item[i].displayName)? "col-md-2 mandate" : "col-md-2"}>{item[i].displayName}</label>
                                <label className="col-md-4">{item[i].description}</label>
                                <div className = "col-md-3">
                                    <select key={`form-control ${item[i].name}_pt`} defaultValue={sel} className={`form-control ${item[i].name}_pt`} ref={(el) => { this.eleSel = el }} onChange={this.setChangeLayerSubParams.bind(this,item[i],defaultParamName)}>
                                        {optionsTemp}
                                    </select>
                                    <div key={`${item[i].name}_pt`} className="error_pt"></div>
                                </div>
                            </div>
                        );
                    break;
                case "slider":
                    var mandateField =["p"]
                    arr1.push(
                        <div key={item[i].name}  class="row mb-20">
                            <label className={mandateField.includes(item[i].displayName)? "col-md-2 mandate" : "col-md-2"}>{item[i].displayName}</label>
                            <label className="col-md-4">{item[i].description}</label>
                                <div className="col-md-1">
                                    <input type="number" key={`form-control ${item[i].name}_pt`} className={`form-control ${item[i].name}_pt`} defaultValue={this.props.pyTorchLayer[this.props.idNum][defaultParamName][item[i].name]} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault() } onChange={this.setLayerSubParams.bind(this,item[i],defaultParamName)}/>
                                    <div key={`${item[i].name}_pt`} className="error_pt"></div>
                                </div>
                        </div>
                    );
                    break;
                default:
                    arr1.push(
                        <div key={item[i].displayName} className="row mb-20">
                            <label className="col-md-2">{item[i].displayName}</label>
                            <label className="col-md-4">{item[i].description}</label>
                        </div>
                    )
                    break;

            }
        }
        return arr1;
    }
    
    renderPyTorchData(parameterData){
        let lyr = this.props.idNum
        switch (parameterData.paramType) {
            case "list":
                var options = parameterData.defaultValue
                var mandateField= ["bias_init","weight_init"]
                var selectedValue = ""
                var optionsTemp =[];
                var sel = ";"
                optionsTemp.push(<option key={'None'} value="None">--Select--</option>)
                for (var prop in options) {
                    if(parameterData.name === "activation"){
                        selectedValue = this.props.pyTorchLayer[lyr].activation.name
                        sel = (options[prop].name === selectedValue)?true:false
                    }else if(parameterData.name === "batchnormalization"){
                        selectedValue = this.props.pyTorchLayer[lyr].batchnormalization.name
                        sel = (options[prop].name === selectedValue)?true:false
                    }else if(parameterData.name === "dropout"){
                        selectedValue = this.props.pyTorchLayer[lyr].dropout.name
                        sel = (options[prop].name === selectedValue)?true:false
                    }else if(parameterData.name === "bias_init"){
                        selectedValue = this.props.pyTorchLayer[lyr].bias_init.name
                        sel = (options[prop].displayName === selectedValue)?true:false
                    }else if(parameterData.name === "weight_init"){
                        selectedValue = this.props.pyTorchLayer[lyr].weight_init.name
                        sel = (options[prop].name === selectedValue)?true:false
                    }else if(parameterData.name === "weight_constraint"){
                        selectedValue = this.props.pyTorchLayer[lyr].weight_constraint.constraint
                        sel = (options[prop].name === selectedValue)?true:false
                    }else if(options[prop].selected){
                        selectedValue = options[prop].name;
                    }
                    optionsTemp.push(<option key={prop} className={prop} value={options[prop].name} >{options[prop].displayName}</option>);
                }
                
                return(
                    <div key={parameterData.name}>
                        <div className = "row mb-20">
                            <label className = {mandateField.includes(parameterData.displayName)? "col-md-2 mandate" : "col-md-2"}>{parameterData.displayName}</label>
                            <label className = "col-md-4">{parameterData.description}</label>
                            <div className = "col-md-3">
                                <select ref={(el) => { this.eleSel = el }} defaultValue={selectedValue} key={`form-control ${parameterData.name}_pt`} className={`form-control ${parameterData.name}_pt`} onChange={this.selectHandleChange.bind(this,parameterData)} >
                                    {optionsTemp}
                                </select>
                                <div key={`${parameterData.name}_pt`} className = "error_pt"></div>
                            </div>
                        </div>
                        {(selectedValue != "None" && selectedValue != "" && selectedValue != undefined && selectedValue != "Ones" && selectedValue != "Zeros" && selectedValue != "Eyes" && selectedValue != "Default" && selectedValue != "Other" && selectedValue !="Dirac" && selectedValue !="False")?
                                (parameterData.name === "dropout"? 
                                this.getsubParams((options.filter(i=>i.name===selectedValue)[0].parameters),parameterData.name)
                                : options.filter(i=>i.name === selectedValue)[0].parameters === null? ""
                                :this.getsubParams((options.filter(i=>i.name===selectedValue)[0].parameters),parameterData.name)) 
                                :""
                            }
                        <div className = "clearfix"></div>
                    </div>
                   );
                break;
            case "number":
                if(parameterData.uiElemType == "textBox"){
                    var mandateField = ["Input Units","Output Units"]
                    switch(parameterData.displayName){
                        case "Input Units":
                            var classN= "form-control input_unit_pt";
                            if(this.props.idNum>1){
                                var defVal = parseInt(this.props.pyTorchLayer[this.props.idNum-1].units_op)
                                var disableVal = true
                            }else{
                                var defVal = this.props.pyTorchLayer[this.props.idNum][parameterData.name];
                                var disableVal = false
                            }
                            break;
                        case "Output Units":
                            var classN= "form-control output_unit_pt";
                            var defVal = this.props.pyTorchLayer[this.props.idNum][parameterData.name];
                            var disableVal = false
                            break;
                        default:
                            classN= "form-control";
                            var defVal = this.props.pyTorchLayer[this.props.idNum][parameterData.name];
                            var disableVal = false
                            break;
                    }
                    return (
                        <div  key={parameterData.name} className="row mb-20">
                            <label className = {mandateField.includes(parameterData.displayName)? "col-md-2 mandate" : "col-md-2"}>{parameterData.displayName}</label>
                            <label className = "col-md-4">{parameterData.description}</label>
                            <div className = "col-md-1">
                                <input type="number" key={`form-control ${parameterData.name}_pt`} className={classN} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault() } defaultValue={defVal} onChange={this.changeTextBoxValue.bind(this,parameterData)} disabled={disableVal} />
                                <div key={`${parameterData.name}_pt`} className = "error_pt"></div>
                            </div>
                            <div class = "clearfix"></div> 
                        </div>
                    );
                }
                break;
            default:
                return (
                    <div key={parameterData.name} className = "row mb-20">
                        <label className="col-md-4">{parameterData.displayName}</label>
                        <label className="col-md-4">{parameterData.description}</label>
                        <div className="error_pt"></div>
                    </div>
                );
        }
    }
    render() {
        var cls =`layerPanel ${this.props.idNum}`
        var clsId = `layer${this.props.idNum}`
        let renderPyTorchLayer = this.props.parameterData.parameters.filter(i=>i.displayName === "Layer")[0].defaultValue[0].parameters.map((layerData,index)=>{
            if(layerData.display){
                const lyr = this.renderPyTorchData(layerData);
                return lyr;
            }
        });
        return (
            <div class={cls} id={clsId}>
                <div class="layerHeader" id={this.props.idNum}>
                    Linear Layer {this.props.idNum}
                    <i className="fa fa-chevron-up" type="button" data-toggle="collapse" data-target={`#collpseExample${this.props.idNum}`} aria-expanded="true" aria-controls={`collpseExample${this.props.idNum}`} />
                    {(this.props.idLayer.length === this.props.idNum)?
                        <i className="fa fa-trash-o" type="button" onClick={this.deleteLayer.bind(this,this.props.idNum)}/>
                        :""
                    }
                </div>
                <div className="collapse in" id={`collpseExample${this.props.idNum}`}>
                    <div className="card card-body">
                        <div class="layerBody xs-pl-15">
                            {renderPyTorchLayer}
                        </div>
                        <div id="suggest_pt" className="mb-20 error_pt"></div>
                    </div>
                </div>
            </div>
        );

    }
}