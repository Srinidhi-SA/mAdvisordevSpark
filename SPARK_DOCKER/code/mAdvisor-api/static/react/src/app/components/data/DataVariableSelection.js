import React from "react";
import { Scrollbars } from 'react-custom-scrollbars';
import { connect } from "react-redux";
import { Popover, OverlayTrigger } from "react-bootstrap";
import store from "../../store";
import $ from "jquery";
import {
  updateSelectedVariables, 
  resetSelectedVariables,
  updateDatasetVariables,
  handleDVSearch,
  handelSort,
  handleSelectAll,
  deselectAllVariablesDataPrev,
  makeAllVariablesTrueOrFalse,
  updateVariableSelectionArray,
  getTotalVariablesSelected,
  selectAllAnalysisList,
  setDefaultTimeDimensionVariable,
  getValueOfFromParam,
  updateSelectedVariablesFromEdit
} from "../../actions/dataActions";
import {resetSelectedTargetVariable} from "../../actions/signalActions";

@connect(( store ) => {
  return {
    dataSetMeasures:store.datasets.dataSetMeasures,
    dataSetDimensions:store.datasets.dataSetDimensions,
    dataSetTimeDimensions:store.datasets.dataSetTimeDimensions,
    isUpdate:store.datasets.isUpdate,
    modelSummary:store.apps.modelSummary,
    createScoreShowVariables:store.datasets.createScoreShowVariables,
    CopyTimeDimension: store.datasets.CopyTimeDimension,
    editmodelFlag:store.datasets.editmodelFlag,
    fromVariableSelectionPage : store.signals.fromVariableSelectionPage
  };
} )

export class DataVariableSelection extends React.Component {
  constructor( props ) {
    super( props );
    this.firstLoop = true;
    this.handleCheckboxEvents = this.handleCheckboxEvents.bind( this );
    this.measures = [];
    this.dimensions = [];
    this.datetime = [];
    this.dimensionDateTime = [];
    this.possibleAnalysisList = {};
  }

    handleCheckboxEvents(e){
        this.props.dispatch( updateSelectedVariables(e))
        if(window.location.href.includes("/createSignal") && e.target.name ==  "date_type"){
            if(this.props.CopyTimeDimension.filter(i=>(i.selected==true)).length == 0){
                $("#chk_analysis_trend").prop("disabled",true);
                $("#chk_analysis_trend")[0].checked = false
                this.props.dispatch(selectAllAnalysisList(true))
            }else{
                $("#chk_analysis_trend").prop("disabled",false);
                this.props.dispatch(selectAllAnalysisList(true))
            }
        }
    }

    componentDidMount(){
        const from = getValueOfFromParam();
        if(from === 'data_cleansing') {
            let dtList = store.getState().datasets.dataSetTimeDimensions
            if(dtList.length!=0 && dtList.filter(i=>(i.selected===true)).length === 0 && document.getElementById("unselect") != undefined){
                document.getElementById("unselect").checked =true
            }
        }else if(this.props.fromVariableSelectionPage || this.props.editmodelFlag || store.getState().datasets.varibleSelectionBackFlag){
        }else{
            window.scrollTo(0, 0);
            if(this.props.match.path.includes("createScore") && store.getState().apps.currentAppDetails != null && store.getState().apps.currentAppDetails.app_type == "REGRESSION"){
                deselectAllVariablesDataPrev(true);
            this.props.dispatch(resetSelectedVariables(true));
        }else{
            this.props.dispatch(resetSelectedVariables(true));
            deselectAllVariablesDataPrev(true);
        }
        this.props.dispatch(resetSelectedTargetVariable());
        }
        if(from !== 'data_cleansing'){
              this.props.dispatch(updateDatasetVariables(this.measures,this.dimensions,this.datetime,this.possibleAnalysisList,true));
        }
      }

    componentWillMount(){
        if(this.props.editmodelFlag)
            this.props.dispatch(makeAllVariablesTrueOrFalse(false));
    }

    componentDidUpdate(){
        if( (this.props.isUpdate && this.props.createScoreShowVariables && this.props.match.path.includes("/createScore")) || (this.props.isUpdate && !this.props.match.path.includes("/createScore"))) {
            if(this.props.match.path.includes("createScore") && store.getState().apps.currentAppDetails != null && store.getState().apps.currentAppDetails.app_type == "REGRESSION"){
                this.props.dispatch(resetSelectedVariables(true));
            }else if(this.props.editmodelFlag){
                this.props.dispatch(updateSelectedVariablesFromEdit())
            }else if(store.getState().datasets.varibleSelectionBackFlag){
            }else{  
                this.props.dispatch( resetSelectedVariables(true));
                deselectAllVariablesDataPrev(true);
            }
            this.props.dispatch(updateDatasetVariables(this.measures,this.dimensions,this.datetime,this.possibleAnalysisList,false));
        }
        let dtList = store.getState().datasets.dataSetTimeDimensions
        if(!store.getState().datasets.varibleSelectionBackFlag && !this.props.editmodelFlag && dtList.length!=0 && document.getElementById("unselect") != undefined){
            if(dtList.filter(i=>(i.selected===true)).length === 0 && !document.getElementById("unselect").checked){
                this.props.dispatch(setDefaultTimeDimensionVariable(dtList[0]));
            }else if(dtList.filter(i=>i.selected).length === 0){
                document.getElementById("unselect").checked =true
            }
        }else if(dtList.length!=0 && dtList.filter(i=>(i.selected===true)).length === 0 && document.getElementById("unselect") != null){
            document.getElementById("unselect").checked =true
        }
      }

    handleDVSearch(evt){
        evt.preventDefault();
        if(evt.target.name == "measure" && evt.target.value == "")
            $("#measureSearch").val("");
        if(evt.target.name == "dimension" && evt.target.value == "")
            $("#dimensionSearch").val("");
        if(evt.target.name == "datetime" && evt.target.value == "")
            $("#datetimeSearch").val("");
        this.props.dispatch(handleDVSearch(evt));
    }

    handelSort(variableType,sortOrder){
        this.props.dispatch(handelSort(variableType,sortOrder))
    }
    handleSelectAll(evt){
        this.props.dispatch(handleSelectAll(evt))
    }

    render() {
        let dataPrev = store.getState().datasets.dataPreview;
        let modelSummary = this.props.modelSummary;
        const popoverLeft = (
            <Popover id="popover-trigger-hover-focus">
                <p>mAdvisor has identified this as date suggestion.This could be used for trend analysis. </p>
            </Popover>
        );
        let timeSuggestionToolTip = (
            <div className="col-md-2"><OverlayTrigger trigger={['hover', 'focus']}  rootClose placement="top" overlay={popoverLeft}>
                <a className="pover cursor">
                    <i class="fa fa-info-circle pe-2x"></i>
                </a>
                </OverlayTrigger>
            </div>
        )

        if(dataPrev) {
            if(this.props.match.path.includes("/createScore") && !$.isEmptyObject(modelSummary))
                this.props.dispatch(updateVariableSelectionArray(modelSummary));
            this.possibleAnalysisList = store.getState().datasets.varibleSelectionBackFlag?store.getState().datasets.dataSetAnalysisList:dataPrev.meta_data.uiMetaData.advanced_settings
            var  metaData = dataPrev.meta_data.uiMetaData.varibaleSelectionArray;
            this.measures = [];
            this.dimensions = [];
            this.datetime = [];
            this.dimensionDateTime =[];
            metaData.map(metaItem => {
                if( (this.props.isUpdate && this.props.createScoreShowVariables && this.props.match.path.includes("/createScore")) || (this.props.isUpdate && !this.props.match.path.includes("/createScore"))) {
                    switch(metaItem.columnType){
                        case "measure":
                            if(metaItem.setVarAs == null){
                                this.measures.push( metaItem);
                            }else if(metaItem.setVarAs != null){
                                this.dimensions.push(metaItem);
                            }
                            break;
                        case "dimension":
                            if(!metaItem.dateSuggestionFlag){
                                this.dimensions.push( metaItem);
                            }else if(metaItem.dateSuggestionFlag){
                                this.dimensionDateTime.push(metaItem)
                            }
                            break;
                        case "datetime":
                            this.datetime.push( metaItem);
                            break;
                    }
                }
            });
            this.datetime = this.datetime.concat(this.dimensionDateTime);
            var varCls = "";
            if(store.getState().datasets.dataSetMeasures.length > 0){
                if(store.getState().datasets.dataSetMeasures.length == 1 && store.getState().datasets.dataSetMeasures[0].targetColumn){
                    $(".measureAll").prop("disabled",true);
                    var measureTemplate = <label id="noMeasures">No measure variable present</label>
                }else{
                    var measureTemplate = store.getState().datasets.dataSetMeasures.map(mItem => {
                        if(mItem.targetColumn || mItem.uidCol)varCls="hidden";
                        else varCls = "";
                        return(
                            <li className={varCls} key={mItem.slug}><div className="ma-checkbox inline"><input id={mItem.slug} name={mItem.setVarAs} type="checkbox" className="measure" onChange={this.handleCheckboxEvents} value={mItem.name} checked={mItem.selected} /><label htmlFor={mItem.slug} className="radioLabels"><span>{mItem.name}</span></label></div> </li>
                        );
                    });
                    $(".measureAll").prop("disabled",false);
                }
            }else{
                $(".measureAll").prop("disabled",true);
                var measureTemplate = <label id="noMeasures">No measure variable present</label>
            }

            if(store.getState().datasets.dataSetDimensions.length > 0){
                if(store.getState().datasets.dataSetDimensions.length == 1 && store.getState().datasets.dataSetDimensions[0].targetColumn){
                    $(".dimensionAll").prop("disabled",true);
                    var dimensionTemplate = <label id="noDimensions" >No dimension variable present</label>
                }else{
                    var dimensionTemplate = store.getState().datasets.dataSetDimensions.map(dItem => {
                        if(dItem.targetColumn ||  dItem.uidCol)varCls="hidden";
                        else varCls = "";
                        return (
                            <li className={varCls} key={dItem.slug}><div className="ma-checkbox inline"><input id={dItem.slug} name={dItem.setVarAs} type="checkbox" className="dimension" onChange={this.handleCheckboxEvents} value={dItem.name} checked={dItem.selected} /><label htmlFor={dItem.slug}> <span>{dItem.name}</span></label></div> </li>
                        );
                    });
                    $(".dimensionAll").prop("disabled",false);
                }
            }else{
                $(".dimensionAll").prop("disabled",true);
                var dimensionTemplate = <label id="noDimensions" >No dimension variable present</label>
            }

            if(store.getState().datasets.dataSetTimeDimensions.length > 0){
                var datetimeTemplate = store.getState().datasets.dataSetTimeDimensions.map(dtItem => {
                    if(dtItem.uidCol)varCls="hidden";
                    else varCls = "";
                    if(dtItem.columnType != "dimension"){
                        return (
                            <li className={varCls} key={dtItem.slug}>
                                <div className="ma-radio inline">
                                    <input type="radio" className="timeDimension" onClick={this.handleCheckboxEvents}  name="date_type" id={dtItem.slug} value={dtItem.name} checked={dtItem.selected} />
                                    <label htmlFor={dtItem.slug}>{dtItem.name}</label>
                                </div>
                            </li>
                        );
                    }else{
                        return (
                            <li className={varCls} key={dtItem.slug}>
                                <div className="ma-radio inline col-md-10">
                                    <input type="radio" className="timeDimension" onClick={this.handleCheckboxEvents}  name="date_type" id={dtItem.slug} value={dtItem.name} checked={dtItem.selected} />
                                    <label htmlFor={dtItem.slug}>{dtItem.name}</label>
                                </div>{timeSuggestionToolTip}
                            </li>
                        );
                    }
                });
            }else{
                var datetimeTemplate = <label>No date dimensions to display</label>
            }

            if(this.props.match.path.includes("/createScore") && store.getState().apps.currentAppDetails != null && store.getState().apps.currentAppDetails.app_type == "REGRESSION"){
                let measureArray = $.grep(dataPrev.meta_data.uiMetaData.varibaleSelectionArray,function(val,key){
                    return(val.columnType == "measure" && val.selected == false && val.targetColumn == false && val.dateSuggestionFlag == false);
                });
                let dimensionArray = $.grep(dataPrev.meta_data.uiMetaData.varibaleSelectionArray,function(val,key){
                    return(val.columnType == "dimension"  && val.selected == false && val.targetColumn == false && val.dateSuggestionFlag == false);
                });
            }
            
            return (
                <div>
                    <div className="col-lg-12">
                        <label>Including the following variables:</label>
                        </div>
                        <div className="col-md-4">
                            <div className="panel panel-primary-p1 cst-panel-shadow">
                                <div className="panel-heading"><i className="mAd_icons ic_inflnce"></i> Measures</div>
                                <div className="panel-body">
                                    <div className="row">
                                        <div className="col-md-12 col-sm-12 xs-pr-0">
                                            <div class="btn-toolbar pull-right">
    											<div class="input-group">
	        										<div className="search-wrapper">
			            								<input type="text" name="measure" onChange={this.handleDVSearch.bind(this)} title="Search Measures" id="measureSearch" className="form-control search-box" placeholder="Search measures..."  />
                                                        <span className="fa fa-search form-control-feedback"></span>
                                                        <button className="close-icon" name="measure" onClick={this.handleDVSearch.bind(this)}  type="reset"></button>
                                                    </div>
                                                </div>
                                                <div class="btn-group">
                                                    <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i class="glyphicon glyphicon-sort"></i></button>
                                                    <ul role="menu" className="dropdown-menu dropdown-menu-right">
                                                        <li onClick={this.handelSort.bind(this,"measure","ASC")} className="cursor"><a><i class="fa fa-sort-alpha-asc"></i> Ascending</a></li>
                                                        <li onClick={this.handelSort.bind(this,"measure","DESC")} className="cursor"><a><i class="fa fa-sort-alpha-desc"></i> Descending</a></li>
                                                    </ul>
                                                </div>
                                            </div>
                                            <div className="ma-checkbox inline">
                                                <input id="measure" type="checkbox" className="measureAll" onChange={this.handleSelectAll.bind(this)} checked={(store.getState().datasets.dataSetMeasures.length === 0 || (this.props.dataSetMeasures.length===1 && this.props.dataSetMeasures[0].targetColumn) )?false:store.getState().datasets.measureAllChecked}/>
                                                <label htmlFor="measure">Select All</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="xs-pb-10"></div>
                                    <div className="row">
                                        <div className="col-md-12 cst-scroll-panel">
                                            <Scrollbars>
                                                <ul className="list-unstyled">{measureTemplate}</ul>
                                            </Scrollbars>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="panel panel-primary-p2 cst-panel-shadow">
                                <div className="panel-heading"><i style={{marginBottom:3}}className="mAd_icons ic_perf "></i> Dimensions</div>
                                <div className="panel-body">
                                    <div className="row">
                                        <div className="col-md-12 col-sm-12 xs-pr-0">
											<div class="btn-toolbar pull-right">
												<div class="input-group">
    												<div className="search-wrapper">
        												<input type="text" name="dimension" onChange={this.handleDVSearch.bind(this)} title="Search Dimension" id="dimensionSearch" className="form-control search-box" placeholder="Search dimension..."  />
                                                        <span className="fa fa-search form-control-feedback"></span>
                                                        <button className="close-icon"  name="dimension"  onClick={this.handleDVSearch.bind(this)}  type="reset"></button>
                                                    </div>
                                                </div>
                                                <div class="btn-group">
                                                    <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i class="glyphicon glyphicon-sort"></i></button>
                                                    <ul role="menu" className="dropdown-menu dropdown-menu-right">
                                                        <li onClick={this.handelSort.bind(this,"dimension","ASC")} className="cursor"><a><i class="fa fa-sort-alpha-asc"></i> Ascending</a></li>
                                                        <li onClick={this.handelSort.bind(this,"dimension","DESC")} className="cursor"><a><i class="fa fa-sort-alpha-desc"></i> Descending</a></li>
                                                    </ul>
                                                </div>
                                            </div>
                                            <div className="ma-checkbox inline">
                                                <input id="dimension" type="checkbox" className="dimensionAll" onChange={this.handleSelectAll.bind(this)} checked={(store.getState().datasets.dataSetDimensions.length === 0 || (this.props.dataSetDimensions.length===1 && this.props.dataSetDimensions[0].targetColumn) )?false:store.getState().datasets.dimensionAllChecked}/>
                                                <label htmlFor="dimension">Select All</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="xs-pb-10"></div>
                                    <div className="row">
                                        <div className="col-md-12 cst-scroll-panel">
                                            <Scrollbars>
                                                <ul className="list-unstyled">{dimensionTemplate}</ul>
                                            </Scrollbars>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="panel panel-primary-p3 cst-panel-shadow">
                                <div className="panel-heading">
                                <i style={{marginRight:4}}class="fa fa-calendar-check-o"></i>
                                 Dates</div>
                                <div className="panel-body">
                                    <div className="row">
                                        <div className="col-md-12 col-sm-12 xs-pr-0">
                                            <div class="btn-toolbar pull-right">
                                            <div class="input-group">
												<div className="search-wrapper">
    												<input type="text" name="datetime" onChange={this.handleDVSearch.bind(this)} title="Search Time Dimensions" id="datetimeSearch" className="form-control search-box" placeholder="Search time dimensions..."/>
	    											<span className="fa fa-search form-control-feedback"></span>
		    										<button className="close-icon" name="datetime" onClick={this.handleDVSearch.bind(this)} type="reset"></button>
												</div>
                                            </div>
                                            <div class="btn-group">
                                                <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i class="glyphicon glyphicon-sort"></i></button>
                                                <ul role="menu" className="dropdown-menu dropdown-menu-right">
                                                    <li onClick={this.handelSort.bind(this,"datetime","ASC")} className="cursor"><a><i class="fa fa-sort-alpha-asc"></i> Ascending</a></li>
                                                    <li onClick={this.handelSort.bind(this,"datetime","DESC")} className="cursor"><a><i class="fa fa-sort-alpha-desc"></i> Descending</a></li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="xs-pb-10"></div>
                                <div className="row">
                                    <div className="col-md-12 cst-scroll-panel">
                                        <Scrollbars>
                                            <ul className="list-unstyled">{datetimeTemplate}
                                                {store.getState().datasets.dataSetTimeDimensions.length > 0 && 
                                                    <div class="ma-radio inline">
                                                        <input type="radio" className="timeDimension" onClick={this.handleCheckboxEvents} id="unselect" name="date_type"  />
                                                        <label htmlFor="unselect">None</label>
                                                    </div>
                                                }
                                            </ul>
                                        </Scrollbars>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4 col-md-offset-5">
                        <h4>{store.getState().datasets.selectedVariablesCount} Variables selected </h4>
                    </div>
                </div>
            );
        }else{
            return (
                <div className="col-lg-12">
                    <h4 className="text-center">No data Available</h4>
                </div>
            );
        }
    }
}
