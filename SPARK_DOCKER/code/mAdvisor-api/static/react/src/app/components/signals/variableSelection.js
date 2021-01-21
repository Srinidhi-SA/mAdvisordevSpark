import React from "react";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import {push} from "react-router-redux";
import {Button,Form,FormGroup} from "react-bootstrap";
import store from "../../store";
import {selectedAnalysisList,selectAllAnalysisList,updateSelectAllAnlysis,saveAdvanceSettings,checkAllAnalysisSelected,showAllVariables,disableAdvancedAnalysisElements,variableSlectionBack} from "../../actions/dataActions";
import {updateCsLoaderValue} from "../../actions/createSignalActions";
import {createSignal,emptySignalAnalysis,advanceSettingsModal,checkIfDateTimeIsSelected,checkIfTrendIsSelected,updateCategoricalVariables,checkAnalysisIsChecked,changeSelectedVariableType,hideTargetVariable,resetSelectedTargetVariable, saveSignalName} from "../../actions/signalActions";
import {DataVariableSelection} from "../data/DataVariableSelection";
import {CreateSignalLoader} from "../common/CreateSignalLoader";
import {openCsLoaderModal,closeCsLoaderModal} from "../../actions/createSignalActions";
import {AdvanceSettings} from "./AdvanceSettings";
import {getAllSignalList} from "../../actions/signalActions";
import ReactTooltip from 'react-tooltip'
import {SET_VARIABLE,statusMessages} from "../../helpers/helper";

@connect((store) => {
    return {
        dataPreview: store.datasets.dataPreview,
        selectedSignal: store.signals.selectedSignal,
        selectedSignalAnalysis: store.signals.signalAnalysis,
        getVarType: store.signals.getVarType,
        getVarText: store.signals.getVarText,
        selVarSlug:store.signals.selVarSlug,
        dataSetTimeDimensions:store.datasets.dataSetTimeDimensions,
        selectedVariablesCount: store.datasets.selectedVariablesCount,
        dataSetAnalysisList:store.datasets.dataSetAnalysisList,
        dimensionSubLevel:store.datasets.dimensionSubLevel,
        dataSetSelectAllAnalysis:store.datasets.dataSetSelectAllAnalysis,
        selectedVariablesCount: store.datasets.selectedVariablesCount,
        allSignalList:store.signals.allSignalList,
        CopyTimeDimension : store.datasets.CopyTimeDimension,
        fromVariableSelectionPage : store.signals.fromVariableSelectionPage,
        setSigName : store.signals.setSigName
    };
})



export class VariableSelection extends React.Component {
    constructor(props) {
        super(props);
        this.signalFlag =true;
        this.props.dispatch(emptySignalAnalysis());
    }

    handleAnlysisList(e){
        this.props.dispatch(selectedAnalysisList(e));
        this.props.dispatch(saveAdvanceSettings());
        this.props.dispatch(checkAllAnalysisSelected())
    }
    handleAllAnlysis(evt){
        this.props.dispatch(updateSelectAllAnlysis(evt.target.checked));
        this.props.dispatch(selectAllAnalysisList(evt.target.checked));
    }
    openAdvanceSettingsModal(){
        this.props.dispatch(advanceSettingsModal(true));
    }
    createSignal(event){
        event.preventDefault();
        let letters = /^[0-9a-zA-Z\d-_\s]+$/;
        var isAnalysisChecked = checkAnalysisIsChecked();
        if($('#signalVariableList option:selected').val() == ""){
            bootbox.alert("Please select a variable to analyze...");
            return false;
        }
        else if($('#createSname').val()!="" && $('#createSname').val().trim() == ""){
            bootbox.alert(statusMessages("warning","Please enter a valid signal name.","small_mascot"));
            $('#createSname').val("").focus();
            return false;
        }
        else if (letters.test(document.getElementById("createSname").value) == false){

            bootbox.alert(statusMessages("warning", "Please enter signal name in a correct format. It should not contain special characters @,#,$,%,!,&.", "small_mascot"));
            $('#createSname').val("").focus();
            return false;

        }
    else if(Object.values(this.props.allSignalList).map(i=>i.name.toLowerCase()).includes($('#createSname').val().toLowerCase())){
        bootbox.alert(statusMessages("warning", "Signal with same name alrady exists, Please try changing name!", "small_mascot"));
        $('#createSname').val("").focus();
        return false;
    }
    
        if(store.getState().datasets.dataSetTimeDimensions.length > 0){
            if(store.getState().datasets.selectedVariablesCount == 1 &&  $("#analysisList").find(".overview").next("div").find("input[type='checkbox']").prop("checked") == true){
              bootbox.alert("Insufficient variables selected for your chosen analysis.Please select more.");
                return false;
            }
        }
        else{
            if(store.getState().datasets.selectedVariablesCount == 0 || (store.getState().datasets.selectedVariablesCount == 0 &&  $("#analysisList").find(".overview").next("div").find("input[type='checkbox']").prop("checked") == true)){
              bootbox.alert("Insufficient variables selected for your chosen analysis.Please select more.");
                return false;
            }
        }

        if(!isAnalysisChecked){

            bootbox.alert("Please select atleast one analysis to Proceed..");

            return false;
        }

        var trendIsChecked = checkIfTrendIsSelected();
        var dateTimeIsSelected = checkIfDateTimeIsSelected();
            if(dateTimeIsSelected == undefined && trendIsChecked == true){
                bootbox.alert("Please select one of the date dimensions.");
                return false;
            }

        this.signalFlag = false;
        this.props.dispatch(updateCsLoaderValue(-1))
        this.props.dispatch(openCsLoaderModal());
        let analysisList =[],config={}, postData={};


        config['variableSelection'] = store.getState().datasets.dataPreview.meta_data.uiMetaData.varibaleSelectionArray

        if(this.props.getVarType.toLowerCase() == "measure"){

            postData['advanced_settings'] = this.props.dataSetAnalysisList.measures;

        }else if(this.props.getVarType.toLowerCase() == "dimension"){
            postData['advanced_settings'] = this.props.dataSetAnalysisList.dimensions;
            this.props.dataSetAnalysisList.dimensions.targetLevels.push(this.props.dimensionSubLevel);

        }
        postData["config"]=config;
        postData["dataset"]=this.props.dataPreview.slug;
        postData["name"]=$("#createSname").val().trim();
       this.props.dispatch(createSignal(postData));
    }

    setPossibleList(event){
        this.props.dispatch(hideTargetVariable(event,"signals"));
    }

    componentWillMount(){
        if(this.props.fromVariableSelectionPage){

      }
      else if(store.getState().datasets.varibleSelectionBackFlag){
      ""
      }else{
            if (this.props.dataPreview == null) {
               var setPath=this.props.history.location.pathname.includes("/data/")?"/data/":"/signals/"
               this.props.history.replace(setPath+this.props.match.params.slug)
            }
            this.props.dispatch(closeCsLoaderModal());
            this.props.dispatch(resetSelectedTargetVariable());
            this.props.dispatch(updateSelectAllAnlysis(false));
            if(this.props.dataPreview != null)
            this.props.dispatch(showAllVariables(this.props.dataPreview,this.props.match.params.slug));
        }
    }

    componentDidMount(){
        if(this.props.fromVariableSelectionPage){
            if(this.props.selVarSlug != null)
                document.getElementsByName(this.props.selVarSlug)[0].selected = true;
            var hel = store.getState().datasets.CopyOfMeasures.filter(i=>i.slug==this.props.selVarSlug)[0];
            if(hel.targetColumn === true && hel.actualColumnType === "measure")
                $("#idCategoricalVar")[0].parentNode.classList.remove("hidden")
                if(hel.columnType === "dimension")
                    $("#idCategoricalVar")[0].checked = true
            $("#createSname")[0].value = this.props.setSigName;
        }
        var that = this;
        this.props.dispatch(getAllSignalList());
    }

    componentWillUpdate(){

        if(!this.props.getVarType){
            $("#allAnalysis").prop("disabled",true);
            $("#advance-setting-link").hide();
        }else{
            $("#allAnalysis").prop("disabled",false);
            $("#advance-setting-link").show();
        }
    }
    componentDidUpdate(){
        var that = this;
        let dataPrev = this.props.dataPreview;
        if(window.location.href.includes("/createSignal") && !$.isEmptyObject(dataPrev)){
            let measureArray = $.grep(dataPrev.meta_data.uiMetaData.varibaleSelectionArray,function(val,key){
                return(val.columnType == "measure" && val.selected == true && val.targetColumn == false);
            });
            let dimensionArray = $.grep(dataPrev.meta_data.uiMetaData.varibaleSelectionArray,function(val,key){
                return(val.columnType == "dimension"  && val.selected == true && val.targetColumn == false);
            });
            if(that.props.getVarType == "dimension"){
                if(measureArray.length >= 1 || dimensionArray.length >= 1){
                    $("#chk_analysis_association").prop("disabled",false);
                    $("#chk_analysis_prediction").prop("disabled",false);
                    this.props.dispatch(disableAdvancedAnalysisElements("association",false));
                    this.props.dispatch(disableAdvancedAnalysisElements("prediction",false));
                }
                else{
                    $("#chk_analysis_association").prop("disabled",true);
                    $("#chk_analysis_prediction").prop("disabled",true);
                    this.props.dispatch(disableAdvancedAnalysisElements("association",true));
                    this.props.dispatch(disableAdvancedAnalysisElements("prediction",true));
                }
            }
            else if(that.props.getVarType == "measure"){
                if(dimensionArray.length >= 1){
                    $("#chk_analysis_performance").prop("disabled",false);
                    this.props.dispatch(disableAdvancedAnalysisElements("performance",false));
                }else{
                    $("#chk_analysis_performance").prop("disabled",true);
                    this.props.dispatch(disableAdvancedAnalysisElements("performance",true));
                }
                if(measureArray.length >= 1){
                    $("#chk_analysis_influencer").prop("disabled",false);
                    this.props.dispatch(disableAdvancedAnalysisElements("influencer",false));
                }else{
                    $("#chk_analysis_influencer").prop("disabled",true);
                    this.props.dispatch(disableAdvancedAnalysisElements("influencer",true));
                }
                if(measureArray.length >= 1 || dimensionArray.length >= 1){
                    $("#chk_analysis_prediction").prop("disabled",false);
                    this.props.dispatch(disableAdvancedAnalysisElements("prediction",false));
                }else{
                    $("#chk_analysis_prediction").prop("disabled",true);
                    this.props.dispatch(disableAdvancedAnalysisElements("prediction",true));
                }
            }
        }

        if(!this.props.getVarType){
            $("#allAnalysis").prop("disabled",true);
            $("#advance-setting-link").hide();
        }else{
            $("#allAnalysis").prop("disabled",false);
            $("#advance-setting-link").show();
            let disableSelectAll = false;
            $('.possibleAnalysis[type="checkbox"]').each(function() {
                if($(this).prop('disabled') == true)
                    disableSelectAll = true;
            });
            if(disableSelectAll == true){
                $("#allAnalysis").prop("disabled",true);
                $("#allAnalysis")[0].checked = true;
            }else{
                if(this.props.CopyTimeDimension.filter(i=>(i.selected == true)).length == 0 && this.props.CopyTimeDimension.length !=0){
                    $("#unselect")[0].checked = true;
                    $("#allAnalysis").prop("disabled",true);
                    $("#chk_analysis_trend").prop("disabled",true);
                }else{
                    $("#allAnalysis").prop("disabled",false);
                
                }
            }
        }
    }
    handleCategoricalChk(event){
        this.props.dispatch(updateCategoricalVariables(this.props.selVarSlug,this.props.getVarText,SET_VARIABLE,event));
        this.props.dispatch(changeSelectedVariableType(this.props.selVarSlug,this.props.getVarText,SET_VARIABLE,event))
    }
    renderAnalysisList(analysisList){
        var countSignal = 0;
        let list =  analysisList.map((metaItem,metaIndex) =>{
            if(metaItem.status==true) countSignal++;
            let id = "chk_analysis_"+ metaItem.name;
            let cls = "ma-checkbox inline "+metaItem.name;
            return(<div key={metaIndex} className={cls}><input id={id} type="checkbox" className="possibleAnalysis" value={metaItem.name} checked={metaItem.status} onClick={this.handleAnlysisList.bind(this)}  /><label htmlFor={id}>{metaItem.displayName}</label></div>);
        });
        if(analysisList.length!=countSignal){setTimeout(function(){ $("#allAnalysis").prop("checked",false);  }, 0);  }
        if(analysisList.length==countSignal){setTimeout(function(){ $("#allAnalysis").prop("checked",true);  }, 0);  }
        return list;
    }
    handleBack=()=>{
      this.props.dispatch(variableSlectionBack(true));
        const slug = this.props.match.params.slug;
        if(this.props.match.path.includes("data"))
        this.props.history.replace(`/data/${slug}?from=createSignal`)
        else if(this.props.match.path.includes("signals"))
        this.props.history.replace(`/signals/${slug}?from=createSignal`);
    }
    setSignalName(event){
        this.props.dispatch(saveSignalName(event.target.value));
    }
    render(){
        var that= this;
        if(!$.isEmptyObject(this.props.selectedSignalAnalysis) && !that.signalFlag){
            $('body').pleaseWait('stop');
            let _link = "/signals/"+this.props.selectedSignal;
            return(<Redirect to={_link}/>)
            ;
        }

        let dataPrev = store.getState().datasets.dataPreview;
        let renderSelectBox = null;
        let renderSubList=null;
        if(dataPrev){
            const metaData = dataPrev.meta_data.uiMetaData.varibaleSelectionArray;
            if(metaData){
                renderSelectBox = metaData.map((metaItem,metaIndex) =>{
                    if(metaItem.columnType !="datetime" && !metaItem.dateSuggestionFlag && !metaItem.uidCol){
                        return(
                            <option key={metaItem.slug}  data-dataType={metaItem.columnType} name={metaItem.slug}   value={metaItem.name}>{metaItem.name}</option>
                        );
                    }
                })
            }else{
                renderSelectBox = <option>No Variables</option>
            }

            let possibleAnalysis = store.getState().datasets.dataSetAnalysisList;
            if(!$.isEmptyObject(possibleAnalysis)){
                if(that.props.getVarType == "dimension"){
                    possibleAnalysis = possibleAnalysis.dimensions.analysis;
                    renderSubList = this.renderAnalysisList(possibleAnalysis);
                }else if(that.props.getVarType == "measure"){
                    possibleAnalysis = possibleAnalysis.measures.analysis;
                    renderSubList = this.renderAnalysisList(possibleAnalysis);
                }
            }
        }
        
        return (
        <div className="side-body">
            <div className="main-content">
                <div className="panel panel-default xs-mb-0">
                    <div className="panel-body no-border box-shadow">
                        <Form onSubmit={this.createSignal.bind(this)} className="form-horizontal">
                            <FormGroup role="form">
                            <label for="signalVariableList" className="col-lg-2 control-label cst-fSize">I want to analyze </label>
                            <div className="col-lg-4">                 
                                <select className="form-control" id="signalVariableList" defaultValue={store.getState().signals.getVarText}  onChange={this.setPossibleList.bind(this)}>
                                  <option value="">--Select--</option>
                                  {renderSelectBox}
                                </select>                 
                            </div>
                            <div className="col-lg-4">
                             <div className="ma-checkbox inline treatAsCategorical hidden" >
                               <input id="idCategoricalVar" type="checkbox" onClick={this.handleCategoricalChk.bind(this)}/>
                               <label htmlFor="idCategoricalVar">Treat as categorical variable</label>
                             </div>
                            </div>
                            </FormGroup>
                            <FormGroup role="form">
                            <DataVariableSelection match={this.props.match}/>
                            </FormGroup>
                            <FormGroup role="form"> 
                                <AdvanceSettings />
                                <div className="col-md-12">
                                    <div className="panel panel-alt4 panel-alt4 cst-panel-shadow">
                                        <div className="panel-heading text-center">Type of Signals&nbsp;&nbsp; 
                                        {this.props.getVarType?
                                        <span>
                                            <ReactTooltip place="bottom" className='customeTheme' effect="solid"/>
                                            <i class="btn btn-default fa fa-info btn-sig-info" data-html="true" data-tip={(this.props.getVarType == "measure") ?
                                                "<b>Overview:</b> Contains Distribution Analysis consisting of Mean, Average, Median, Quartiles for numerical variables."+
                                                "<br/><b>Trend:</b> Extracting an underlying pattern of behavior in a time series."+
                                                "<br/><b>Performance:</b> ANOVA test assesses whether the averages of more than two groups are statistically different from each other."+
                                                "<br/><b>Influencers:</b> Model the relationship between two or more explanatory variables and a response variable by fitting <br/>a linear equation to observed data."+
                                                "<br/><b>Prediction:</b> A graph that uses a branching method to illustrate every possible outcome of a decision."
                                                :
                                                "<b>Overview:</b> Univariate Freq. Distribution shows a summarized grouping of data divided into mutually exclusive classes <br/>and the number of occurrences in a class."+
                                                "<br/><b>Trend:</b> Extracting an underlying pattern of behavior in a time series."+
                                                "<br/><b>Association:</b> The chi-square test can be used to determine the association between categorical variables."+
                                                "<br/><b>Prediction:</b> A graph that uses a branching method to illustrate every possible outcome of a decision."
                                                }>
                                            </i>
                                        </span>
                                        :""}
                                        
                                        </div>
                                        <div className="panel-body text-center" id="analysisList" >
                                            <div className="ma-checkbox inline"><input id="allAnalysis" type="checkbox" className="allAnalysis" checked={store.getState().datasets.dataSetSelectAllAnalysis} onClick={this.handleAllAnlysis.bind(this)}  /><label htmlFor="allAnalysis">Select All</label></div>
                                            {renderSubList}
                                            <div className="pull-right cursor">
                                                <a className="cursor" id="advance-setting-link" onClick={this.openAdvanceSettingsModal.bind(this)}>Advanced Settings</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            <div class="clearfix xs-m-10"></div>
                            <div className="col-lg-2">
                                <Button id="signalBack" onClick={this.handleBack} bsStyle="primary"><i className="fa fa-angle-double-left"></i> Back</Button>
                            </div>
                            <div className="col-lg-5 col-lg-offset-5">
                                <div class="input-group xs-mb-15">
                                    <input type="text" name="createSname" id="createSname"  required={true} onChange={this.setSignalName.bind(this)}  defaultValue={store.getState().datasets.varibleSelectionBackFlag?store.getState().signals.setSigName:""}  class="form-control" placeholder="Enter a signal name"/><span class="input-group-btn">
                                    <button id="signalCreate" type="submit" class="btn btn-primary">Create Signal</button></span>
                                </div>
                            </div>
                            </FormGroup>
                        </Form>
                    </div>
                </div>
            <CreateSignalLoader history={this.props.history} />
            </div>
        </div>
        )
    }

}
