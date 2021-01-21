import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import { decimalPlaces } from "../../helpers/helper";
import ReactBootstrapSlider from 'react-bootstrap-slider';
import { MultiSelect } from "primereact/multiselect";
import { updateAlgorithmData } from "../../actions/appActions";


@connect((store) => {
    return {
      editmodelFlag:store.datasets.editmodelFlag,
    };
})

export class RegressionParameter extends React.Component {
  constructor(props) {
    super(props);
    if(this.props.editmodelFlag){
      if(this.props.parameterData.paramType == "number"){
        this.state = {
          min: this.props.parameterData.valueRange[0],
          max: this.props.parameterData.valueRange[1],
          defaultVal:this.props.parameterData.acceptedValue!=null?this.props.parameterData.acceptedValue:this.props.parameterData.defaultValue,
          name:this.props.parameterData.name,
        };
      }else{
        this.state = {
          defaultVal:this.props.parameterData.defaultValue,
          name:this.props.parameterData.name,
        };
      }
    }else{
      if(this.props.parameterData.paramType == "number"){
        this.state = {
            min:(this.props.parameterData.valueRange != null)?this.props.parameterData.valueRange[0]:"",
            max: (this.props.parameterData.valueRange != null)?this.props.parameterData.valueRange[1]:"",
            defaultVal:this.props.parameterData.defaultValue,
            name:this.props.parameterData.name,
        };
      }else{
        this.state = {
          defaultVal:this.props.parameterData.defaultValue,
          name:this.props.parameterData.name,
        };
      }
    }
    if(this.props.parameterData.paramType == "list"){
      this.state = {
        dropValues : ""
      };
    }
  }

  componentDidMount(){
    $(".learningCls").prop("disabled",true);
    $(".multi").prop("disabled",false);
    $(".powerT").prop("disabled",true);
    $(".fractionCls").prop("disabled",true);
    $(".nesterovsCls").prop("disabled",true);
    $(".momentumCls").prop("disabled",true);
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.parameterData.acceptedValue !== nextProps.parameterData.acceptedValue && nextProps.parameterData.acceptedValue == null) {
      this.setState({
        defaultVal:this.props.parameterData.defaultValue,
      });
    }
    if (this.props.tuneName != "none" && nextProps.tuneName != "none" && this.props.tuneName !== nextProps.tuneName && this.props.parameterData.paramType == "list" && this.props.type == "TuningParameter")
      setTimeout(function(){ $('.multi').multiselect('refresh'); }, 0);
  }

  componentWillMount(){
    setTimeout(function(){ $('.single').multiselect('destroy'); }, 0);
  }

  handleSkLearnParamsForTune(e){
    var target = e.target.value[0]
    if(e.target.value.length===2){
      target = e.target.value[0]+e.target.value[1]
    }else if(e.target.value.length===3){
      target = "solverAll"
    }
    switch(target){
      case "adam":
      case "adamlbfgs":
      case "lbfgsadam":
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"power_t",0.5,this.props.type));
          $(".powerT")[0].parentElement.querySelector(".range-validate").innerHTML = ""
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"momentum",0.9,this.props.type));
          $(".momentumCls")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        break;
      case "lbfgs":
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"epsilon",8,this.props.type));
        $("input.epsilonGrid")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"n_iter_no_change",10,this.props.type));
        $("input.iterationGrid")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"learning_rate_init",0.001,this.props.type));
        $("input.learningClsInit")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"power_t",0.5,this.props.type));
        $(".powerT")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"momentum",0.9,this.props.type));
        $(".momentumCls")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_1 ",0.9,this.props.type));
        $(".beta1")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_2 ",0.999,this.props.type));
        $(".disNum")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        break;
      case "sgd":
      case "lbfgssgd":
      case "sgdlbfgs":
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"epsilon",8,this.props.type));
        $("input.epsilonGrid")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_1 ",0.9,this.props.type));
        $(".beta1")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_2 ",0.999,this.props.type));
        $(".disNum")[0].parentElement.querySelector(".range-validate").innerHTML = ""
        break;
      default :""
        break;
    }
  }
  handleSkLearnParams(e){
    var paramsArray=[".learningCls",".disNum",".beta1",".learningClsInit",".earlyStop",".powerT",".shuffleCls",".epsilonCls",".iterationCls",".nesterovsCls",".momentumCls"]
      switch(e.target.value){
        case "sgd":
          var flagsToSetSgd=[false,true,true,false,false,false,false,true,false,false,false] //caution:true/false Order should be same as paramsArray order
          for(var i=0;i<=paramsArray.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArray[i]).prop("disabled",flagsToSetSgd[i]);
              if(flagsToSetSgd[i] && $(paramsArray[i])[0].tagName === "INPUT"){
                $(paramsArray[i])[0].parentElement.querySelector(".range-validate").innerHTML = ""
              }
            }
          }
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"epsilon",8,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_1 ",0.9,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_2 ",0.999,this.props.type));

          $(".epsilonCls .slider-horizontal").addClass("epsilonDisable");
          $(".iterationCls .slider-horizontal").removeClass("epsilonDisable");
        break;
        case "adam":
          var flagsToSetAdam=[true,false,false,false,false,true,false,false,false,true,true,];//caution:true/false Order should be same as paramsArray order
          for(i=0;i<=paramsArray.length;i++){
            for(j=0;j<1;j++){
              $(paramsArray[i]).prop("disabled",flagsToSetAdam[i]);
              if(flagsToSetAdam[i] && $(paramsArray[i])[0].tagName === "INPUT"){
                $(paramsArray[i])[0].parentElement.querySelector(".range-validate").innerHTML = ""
              }
            }
          }
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"power_t",0.5,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"momentum",0.9,this.props.type));

          $(".epsilonCls .slider-horizontal").removeClass("epsilonDisable");
          $(".iterationCls .slider-horizontal").removeClass("epsilonDisable");
        break;
        case "lbfgs":
          var flagsToSetlbfgs=[true,true,true,true,true,true,true,true,true,true,true,];//caution:true/false Order should be same as paramsArray order
          for(var i=0;i<=paramsArray.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArray[i]).prop("disabled",flagsToSetlbfgs[i]);
              if(flagsToSetlbfgs[i] && $(paramsArray[i])[0].tagName === "INPUT"){
                $(paramsArray[i])[0].parentElement.querySelector(".range-validate").innerHTML = ""
              }
            }
          }
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"epsilon",8,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"n_iter_no_change",10,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"learning_rate_init",0.001,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"power_t",0.5,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"momentum",0.9,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_1 ",0.9,this.props.type));
          this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,"beta_2 ",0.999,this.props.type));

          $(".iterationCls .slider-horizontal").addClass("epsilonDisable");
          $(".epsilonCls .slider-horizontal").addClass("epsilonDisable");
        break;
        default : "";
        break;
      }
      if(e.target.className=="form-control single earlyStop" && e.target.value == "true"){
        $(".fractionCls").prop("disabled",false);
      }else if(e.target.className=="form-control single earlyStop" && e.target.value == "false"){
        $(".fractionCls").prop("disabled",true);
      }else if($('.earlyStop').val() == "true" && (e.target.value == "sgd" || e.target.value == "adam") ){
        $(".fractionCls").prop("disabled",false);
      }else if($('.earlyStop').val() == "true" && (e.target.value == "lbfgs") ){
        $(".fractionCls").prop("disabled",true);
      }
    
  }
  checkType(val,type,min,max){
    if(val === min || val === max){
        return {"iserror":false,"errmsg":""};
    }else{
        var allowedTypes = "";
        var wrongCount = 0;
        var that = this;
          $.each(type,function(k,v){
              if(v == "float"){
                  (k == 0)?allowedTypes = "decimals" : allowedTypes+= ", decimals";
                  if(val % 1 == 0)
                  wrongCount++;
              }
              else if(v == "int"){
                  (k == 0)?allowedTypes = "numbers" : allowedTypes+= ", numbers";
                  if(val % 1 != 0 || parseInt(val.toString().split(".")[1])==0)
                  wrongCount++;
              }
              else if(v == null && val != null){
                  type.splice(k,1);
                  that.checkType(val,type,min,max);
              }
          });
      if(wrongCount != 0 && wrongCount == type.length)
        return {"iserror":true,"errmsg":"Only "+allowedTypes+" are allowed"};
      else
        return {"iserror":false,"errmsg":""};
    }
  }
  validateRangeandFieldForTune(e,min,max,type){
    this.setState({ defaultVal: e.target.value });
    this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,this.props.parameterData.name,e.target.value,this.props.type));
    
    const regex = /^\s*(([0-9]\d*)?(\.\d+)?)\s*-\s*(([0-9]\d*)?(\.\d+)?)\s*$/;
    const letter = /[a-zA-Z]/;
    if(e.target.value === ""){
      e.target.parentElement.lastElementChild.innerHTML = "Please Enter Value";
    }else if(letter.test(e.target.value)){
      e.target.parentElement.lastElementChild.innerHTML = "Only numbers are allowed";
    }else{
      e.target.parentElement.lastElementChild.innerHTML = "";
      e.target.classList.remove("regParamFocus");
    }
    const parts = e.target.value.split(/,|\u3001/);
    for (let i = 0; i < parts.length; ++i){
      const match = parts[i].match(regex);
      if (match) {
        var checkType = this.checkType(match[1],type,min,max);
        var checkType2 = this.checkType(match[4],type);
        if(checkType.iserror == true){
          e.target.parentElement.lastElementChild.innerHTML = checkType.errmsg
          return false;
        }
        if(checkType2.iserror == true){
          e.target.parentElement.lastElementChild.innerHTML = checkType2.errmsg
          e.target.classList.add("regParamFocus");
          return false;
        }
        let match1 = parseFloat(match[1])
        let match2 = parseFloat(match[4])
        if((Number(match1) != match1) || (Number(match2) != match2)){
          e.target.parentElement.lastElementChild.innerHTML = "Enter a valid number";
          e.target.classList.add("regParamFocus");
          return false;
        }
        if(match1<min || match2<min || match1>max ||match2>max || match1>match2 || match1==="" || match2==="" || match1===match2){
          e.target.parentElement.lastElementChild.innerHTML = "Invalid Range"
          return false;
        }
      }
      else{
        var isSingleNumber = parts[i].split(/-|\u3001/);
        if(isSingleNumber.length > 1){
          e.target.parentElement.lastElementChild.innerHTML = "Valid range is "+min+"-"+max;
          e.target.classList.add("regParamFocus");
          return false;
        }
        if(Number(parts[i]) != parts[i]){
          e.target.parentElement.lastElementChild.innerHTML = "Enter a valid number";
          e.target.classList.add("regParamFocus");
          return false;
        }
        if(parts[i] === ""){
          e.target.parentElement.lastElementChild.innerHTML = "";
        }else if(parts[i] < min || parts[i] > max){
          e.target.parentElement.lastElementChild.innerHTML = "Valid range is "+min+"-"+max;
          e.target.classList.add("regParamFocus");
          return false;
        }
        var checkType = this.checkType(parts[i],type,min,max);
        if(checkType.iserror == true){
          e.target.parentElement.lastElementChild.innerHTML = checkType.errmsg;
          return false;
        }
        
      }
    }
  }
  validateRangeandField(e){
    let value = e.target.value;
    let floatTypeParams = ["regParam","elasticNetParam","threshold","minInfoGain","smoothing","tol","C","min_samples_split","min_samples_leaf","eta","subsample","colsample_bytree","colsample_bylevel","alpha","learning_rate_init","power_t","momentum","validation_fraction","beta_1 ","beta_2 ","max_leaf_nodes","stepSize"]
    if(value === ""){
      e.target.parentElement.lastElementChild.innerHTML = "Enter a valid number"
    }else if(value < this.state.min || value > this.state.max){
      e.target.parentElement.lastElementChild.innerHTML = "Valid Range is "+this.state.min+"-"+ this.state.max
    }else if(!Number.isInteger(parseFloat(value)) && !floatTypeParams.includes(e.target.name) ){
      e.target.parentElement.lastElementChild.innerHTML = "Decimals are not allowed"
    }else 
      e.target.parentElement.lastElementChild.innerHTML = ""
    
    if(e.target.parentElement.lastElementChild.innerHTML !=""){
      e.target.classList.add("regParamFocus");
    }else
      e.target.classList.remove("regParamFocus");
    
    ($(".momentumCls").val())>=0.1?$(".nesterovsCls").prop("disabled",false):$(".nesterovsCls").prop("disabled",true)
    this.setState({ defaultVal: value });
    this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,this.props.parameterData.name,value,this.props.type));
  }
  handleChange(paramType,e){
    if(paramType === "list"){
      this.props.isTuning?this.handleSkLearnParamsForTune(e):this.handleSkLearnParams(e);
      this.setState({dropValues: e.value})
      this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,this.props.parameterData.name,e.target.value,this.props.type));
    }
    else if(paramType === "number"){
      (this.props.isTuning && this.props.parameterData.uiElemType != "textBox")?this.validateRangeandFieldForTune(e,this.state.min,this.state.max,this.props.parameterData.expectedDataType):this.validateRangeandField(e)
    }
    else if(paramType === "slider"){
      this.setState({ defaultVal: e.target.value });
      var index=0
      if((document.getElementsByName(this.state.name).length==2) && ($('li.active')[0].innerText=="NEURAL NETWORK (SKLEARN)")&& (this.state.name=="max_iter"||this.state.name=="tol")){
        index=1
        }

      document.getElementsByName(this.state.name)[index].parentElement.querySelector(".range-validate").innerText = ""
      document.getElementsByName(this.state.name)[index].parentElement.querySelector(".form-control").classList.remove("regParamFocus")
      this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,this.props.parameterData.name,e.target.value,this.props.type));
    }
    else if(paramType === "checkbox"){
      this.setState({ defaultVal: e.target.checked });
      this.props.dispatch(updateAlgorithmData(this.props.algorithmSlug,this.props.parameterData.name,e.target.checked,this.props.type));
    }

  }
  
  disableANNParams(parameterData,options){
    var paramsArrayGrid=[".disNum",".beta1",".learningClsInit",".powerT",".iterationGrid",".epsilonGrid",".momentumCls",".learningGrid .multiselect",".shuffleGrid .multiselect"];
    switch(parameterData.name){
      case"solver":
        if((options.map(i=>i)[2].selected && parameterData.defaultValue.map(i=>i)[2].displayName=="sgd")&&
          (options.map(i=>i)[1].selected && parameterData.defaultValue.map(i=>i)[1].displayName=="lbfgs")&&
          (options.map(i=>i)[0].selected && parameterData.defaultValue.map(i=>i)[0].displayName=="adam")){                 
          var flagsToSolverAll=[false,false,false,false,false,false,false,false,false,]
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",flagsToSolverAll[i]);
            }
          }
        }
        else if((options.map(i=>i)[2].selected && parameterData.defaultValue.map(i=>i)[2].displayName=="sgd")&&
          (options.map(i=>i)[1].selected && parameterData.defaultValue.map(i=>i)[1].displayName=="lbfgs")){
          var solverSgdLbfgs=[true,true,false,false,false,true,false,false,false,]
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverSgdLbfgs[i]);
            }
          }
        }
        else if((options.map(i=>i)[0].selected && parameterData.defaultValue.map(i=>i)[0].displayName=="adam")&&
          (options.map(i=>i)[1].selected && parameterData.defaultValue.map(i=>i)[1].displayName=="lbfgs")){
          var solverAdamLbfgs=[false,false,false,true,false,false,true,true,false,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverAdamLbfgs[i]);
            }
          }
        }
        else if((options.map(i=>i)[0].selected && parameterData.defaultValue.map(i=>i)[0].displayName=="adam")&&
          (options.map(i=>i)[2].selected && parameterData.defaultValue.map(i=>i)[2].displayName=="sgd")){
          var solverAdamSgd=[false,false,false,false,false,false,false,false,false,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverAdamSgd[i]);
            }
          }
        }
        else if(options.map(i=>i)[1].selected && parameterData.defaultValue.map(i=>i)[1].displayName=="lbfgs"){
          var solverLbfgs=[true,true,true,true,true,true,true,true,true,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverLbfgs[i]);
            }
          }
        }
        else if(options.map(i=>i)[0].selected && parameterData.defaultValue.map(i=>i)[0].displayName=="adam"){
          var solverAdam=[false,false,false,true,false,false,true,true,false,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverAdam[i]);
            }
          }
        }
        else if(options.map(i=>i)[2].selected && parameterData.defaultValue.map(i=>i)[2].displayName=="sgd"){
          var solverSgd=[true,true,false,false,false,true,false,false,false,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverSgd[i]);
            }
          }
        }              
        else{
          var solverdefault=[false,false,false,false,false,false,false,false,false,];
          for(var i=0;i<=paramsArrayGrid.length;i++){
            for(var j=0;j<1;j++){
              $(paramsArrayGrid[i]).prop("disabled",solverdefault[i]);
            }
          }
          $(".earlyStop").prop("disabled",false);
        }
        break;
      default:"";
    }
  }
  getClassNameList(parameterData,tune){
      if(tune){
        if(parameterData.displayName === "Activation"){
          return {"rowCls":"activation"}
        }else if(parameterData.displayName === "Solver Used"){
          return {"rowCls":"solverGrid"}
        }else if(parameterData.displayName === "Learning Rate"){
          return {"rowCls":"learningGrid"}
        }else if(parameterData.displayName === "Shuffle"){
          return {"rowCls":"shuffleGrid"}
        }else if(parameterData.displayName === "Batch Size"){
          return {"rowCls":"batchGrid"}
        }else if(parameterData.displayName === "Fit Intercept"){
          return {"rowCls":"InterceptGrid"}
        }else if(parameterData.displayName === "Criterion"){
          return {"rowCls":"criterionGrid"}
        }else if(parameterData.displayName === "Bootstrap Sampling"){
          return {"rowCls":"bootstrapGrid"}
        }else if(parameterData.displayName === "Booster Function"){
          return {"rowCls":"boosterGrid"}
        }else if(parameterData.displayName === "Tree Construction Algorithm"){
          return {"rowCls":"treeGrid"}
        }else {
          return {"rowCls":"row"}
        }
      }
      if(parameterData.name === "learning_rate"){
        return {"cls":"form-control single learningCls"}
      }else if(parameterData.name === "early_stopping"){
        return {"cls":"form-control single earlyStop"}
      }else if(parameterData.name === "shuffle"){
        return {"cls":"form-control single shuffleCls"}
      }else if(parameterData.name === "nesterovs_momentum"){
        return {"cls":"form-control single nesterovsCls"}
      }else{
        return {"cls":"form-control single"}
      }
  }
  getClassNameNumber(parameterData,tune){
      if(parameterData.uiElemType === "textBox"){
        if(parameterData.displayName === "Beta 1"){
          return {"cls":"form-control beta1"}
        }else if(parameterData.displayName === "Beta 2"){
          return {"cls":"form-control disNum"}
        }else if(parameterData.displayName === "Learning Rate Initialize"){
          return {"cls":"form-control learningClsInit"}
        }else if(parameterData.displayName === "Power T"){
          return {"cls":"form-control powerT"}
        }else if(parameterData.displayName === "Validation Fraction"){
          return {"cls":"form-control fractionCls"}
        }else if(parameterData.displayName === "Momentum"){
          return {"cls":"form-control momentumCls"}
        }else if(parameterData.displayName === "Alpha"){
          return {"cls":"form-control alphaCls",type:"text"}
        }else if(parameterData.displayName === "Batch Size"){
          return {"cls":"form-control batchCls",type:"text"}
        }else if(parameterData.displayName === "Hidden Layer Size"){
          return {"cls":"form-control hiddenCls",type:"text"}
        }else if(parameterData.displayName === "Number of Epochs"){
          return {"cls":"form-control epochsCls"}
        }else{
          return {"cls":`form-control ${this.state.name}`,type:"number"}
        }
      }
      else if(parameterData.uiElemType === "slider"){
        if(tune){
          if(parameterData.displayName === "Epsilon"){
            return {"cls":"form-control epsilonGrid"}
          }else if(parameterData.displayName === "No of Iteration"){
            return {"cls":"form-control iterationGrid"}
          }else if(parameterData.displayName === "Maximum Solver Iterations"){
            if(parameterData.defaultValue==200)
              return {"cls":"form-control maxSolverGrid"}
            else
              return {"cls":`form-control ${this.state.name}`}
          }else if(parameterData.displayName === "Convergence tolerance of iterations(e^-n)"){
            if(parameterData.neural)
              return {"cls":"form-control convergGrid"}
            else
              return {"cls":`form-control ${this.state.name}`}
          }else{
            return {"cls":`form-control ${this.state.name}`}
          }
        }else{
          if(parameterData.displayName === "Epsilon"){
            return {
              "cls":"col-xs-10 epsilonCls",
              "sliderTextCls":"form-control epsilonCls inputWidth"
            }
          }else if(parameterData.displayName === "No of Iteration"){
            return {
              "cls":"col-xs-10 iterationGrid",
              "sliderTextCls":"form-control iterationCls inputWidth"
            }
          }else if(parameterData.displayName === "Maximum Solver Iterations"){
            if(parameterData.defaultValue==200)
              return {
                "cls":"col-xs-10 maxIterationsCls",
                "sliderTextCls":"form-control maxIterationsCls inputWidth"
              }
            else
              return {
                "cls":"col-xs-10",
                "sliderTextCls":`form-control ${this.state.name} inputWidth`
              }
          }else if(parameterData.displayName === "Convergence tolerance of iterations(e^-n)"){
            if(parameterData.neural)
              return {
                "cls":"col-xs-10",
                "sliderTextCls":"form-control convergenceCls inputWidth"
              }
            else
              return {
                "cls":"col-xs-10",
                "sliderTextCls":`form-control ${this.state.name} inputWidth`
              }
          }else if(parameterData.displayName === "Max Depth"){
              return {
                "cls":"col-xs-10 maxDepthCls",
                "sliderTextCls":"form-control maxDepthCls inputWidth"
              }
          }else{
            return {
              "cls":"col-xs-10",
              "sliderTextCls":`form-control ${this.state.name} inputWidth`
            }
          }
        }
      }
  }

  renderParameterData(parameterData,tune){
    var getClassNameList = this.getClassNameList(parameterData,tune);
    var getClassNameNumber = this.getClassNameNumber(parameterData,tune);
    switch (parameterData.paramType) {
      case "list":
        var optionsTemp =[], optionsTemp1 =[], optionsTemp2 = [];
        let options = parameterData.defaultValue;
        if(tune){
          var selectedValue =[];
          for (var prop in options) {
            if(options[prop].selected){
              selectedValue.push(options[prop].name)
            }
            if(this.props.parameterData.defaultValue.map(val=>val)[0].displayName=="adam"){//to run below switch conditon  only for ANN, #1363      
              this.disableANNParams(parameterData,options);
            }
            //If nontuning normal dropdown
            optionsTemp.push(
              <option key={prop} className={prop} value={options[prop].name} selected={options[prop].selected?"selected":""}>
                {options[prop].displayName}
              </option>);
            //If tuning MultiSelect dropdown
            optionsTemp1.push({"key":prop,"label": options[prop].displayName, 'value': options[prop].name})
            if(options[prop].selected)
              optionsTemp2.push(options[prop].name);
            this.state.dropValues = Array.from(new Set(optionsTemp2));
          }
        }
        else{
          var selectedValue="";
          var selectedOption=options.filter(i=>i.selected).length>0?options.filter(i=>i.selected)[0].name:""
          for (var prop in options) {
            if(options[prop].selected)
              selectedValue = options[prop].name;
            optionsTemp.push(<option key={prop} className={prop} value={options[prop].name}>{options[prop].displayName}</option>);
          }
        }
        return(
          <div className= {"row" + " "+getClassNameList.rowCls}>
            {tune?
              <div className="col-md-4 for_multiselect">
                <MultiSelect value={this.state.dropValues} className={"form-control multi"+ ((selectedValue.length == 0)? ' regParamFocus':'')} options={optionsTemp1} onChange={this.handleChange.bind(this,"list")} placeholder="None Selected"/>
                </div>:
              <div className="col-md-6 for_multiselect">
                <select ref={(el) => { this.eleSel = el }} defaultValue={selectedOption} className={getClassNameList.cls} multiple={false} onChange={this.handleChange.bind(this,"list")}>
                  {optionsTemp}
                </select>
              </div>
            }
            <div className="clearfix"></div>
            {tune ?<div className="col-md-6 check-multiselect text-danger">{(selectedValue.length == 0)?"Please select at least one":""}</div>:""}
          </div>
        );
        break;
      case "number":
        if(parameterData.uiElemType == "textBox"){
          return (
            <div className="row">
              <div className="col-md-2">
                <input type="number" className={getClassNameNumber.cls} name={this.state.name} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault() } value={this.state.defaultVal?this.state.defaultVal:""} onChange={this.handleChange.bind(this,"number")}/>
                <div className="clearfix"></div>
                <div className="range-validate text-danger"></div>
              </div>
            </div>
          );
        }
        else if(parameterData.uiElemType == "slider"){
          if(tune){
            return(
              <div className="row">
                <div className="col-md-12">
                  <div className="row">
                    <div className="col-md-2">
                      <div className="clr-alt4 gray-box">{this.state.min}</div>
                    </div>
                    <div className="col-md-2">
                      <div className="clr-alt4 gray-box">{this.state.max}</div>
                    </div>
                    <div className="col-md-6">
                      <input type="text" className={getClassNameNumber.cls} value={this.state.defaultVal} name={this.state.name} placeholder={(this.state.min<1 && this.state.max==1)?"e.g. 0.5-0.7, 0.4, 1":"e.g. 3-10, 10-400, 10"} onChange={this.handleChange.bind(this,"number")} />
                      <div className="clearfix"></div>
                      <div className="range-validate text-danger"></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          }
          else{
            let diff = this.state.max - this.state.min;
            if(diff <= 1){
              var step = 0.1;
            }else{
              let precision = decimalPlaces(this.state.max);
              var step = (1 / Math.pow(10, precision));
            }
            return (
              <div className="row">                        
                <div className="col-md-6 col-sm-2">
                  <div className="col-xs-1 clr-alt4">{this.state.min}</div>
                  <div className={getClassNameNumber.cls}>
                    <ReactBootstrapSlider value={this.state.defaultVal} triggerSlideEvent="true" step={step} max={this.state.max} min={this.state.min} change={this.handleChange.bind(this,"slider")}/>
                  </div>
                  <div className="col-xs-1 clr-alt4"> {this.state.max}</div>
                </div>
                <div className="col-md-4 col-sm-4">
                  <input type="number" onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault() } min = {this.state.min} max = {this.state.max} className={getClassNameNumber.sliderTextCls} name={this.state.name} value={this.state.defaultVal} onChange={this.handleChange.bind(this,"number")} />
                  <div className="clearfix"></div>
                  <div className="range-validate text-danger"></div>
                </div>
              </div>
            );
          }
        }
        break;
      case "textbox":
        return (
          <div className="row">
            <div className="col-md-6">
              <input type="text" className="form-control" name={this.state.name} value={this.state.defaultVal} onChange={this.handleChange.bind(this,"textbox")} />
            </div>
          </div>
        );
        break;
      case "boolean":
        var chkBox = this.props.uniqueTag+this.props.parameterData.name;
        return ( 
          <div className="ma-checkbox inline">
            <input  type="checkbox" id={chkBox} name={chkBox} checked={this.state.defaultVal} onChange={this.handleChange.bind(this,"checkbox")} />
            <label htmlFor={chkBox}>&nbsp;</label>
          </div>
        );
        break;
      default:
        return ""
        break;
    }
  }

  render() {
    let parameterData = this.props.parameterData;
    let tune = this.props.isTuning;
    return (
      <div class="col-md-6">
        {this.renderParameterData(parameterData,tune)}
      </div>
    );
  }
}
