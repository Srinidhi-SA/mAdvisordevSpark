import React from "react";
import { connect } from "react-redux";
import store from "../../store";
import {Modal,Button, Tooltip,OverlayTrigger,} from "react-bootstrap";
import {advanceSettingsModal} from "../../actions/signalActions";
import {selectedAnalysisList,cancelAdvanceSettings,saveAdvanceSettings,checkAllAnalysisSelected} from "../../actions/dataActions";

@connect((store) => {
	return {
		advanceSettingsModal:store.signals.advanceSettingsModal,
		dataPreview: store.datasets.dataPreview,
		getVarType: store.signals.getVarType,
		dataSetAnalysisList:store.datasets.dataSetAnalysisList,
	};
})

export class AdvanceSettings extends React.Component {
	constructor(props){
		super(props);
	}

	closeAdvanceSettingsModal(){
		this.props.dispatch(cancelAdvanceSettings());
		this.props.dispatch(advanceSettingsModal(false));
		this.props.dispatch(checkAllAnalysisSelected())
	}
	updateAdvanceSettings(){
		let isError = false;
		$('.error_pt ').each(function(){
			if($(this)[0].innerHTML != ""){
				isError = true;
			}
		});
		if(isError){
			document.getElementById("resolveError").innerText="Please resolve above errors"
		}else{
			this.props.dispatch(saveAdvanceSettings());
			this.props.dispatch(advanceSettingsModal(false));
			this.props.dispatch(checkAllAnalysisSelected())
		}
	}

	handleAnlysisListActions(e){
		this.props.dispatch(selectedAnalysisList(e));
		this.props.dispatch(checkAllAnalysisSelected())
	}
	handleSubLevelAnalysis(evt){
		if(!(evt.target.childNodes[0].disabled)){
			this.props.dispatch(selectedAnalysisList(evt.target.childNodes[0],"noOfColumnsToUse"))
		}
	}
	handleCustomInput(evt){
		document.getElementById("resolveError").innerText=""
		this.props.dispatch(selectedAnalysisList(evt.target,"noOfColumnsToUse"))
		if(evt.target.value === "" || evt.target.value.startsWith("0") ){
			evt.target.nextSibling.innerText = "Please enter a valid number"
		}else if( (parseFloat(evt.target.value)^0) != parseFloat(evt.target.value) || evt.target.value.includes(".") ){
			evt.target.nextSibling.innerText = "Decimals are not allowed"
		}else if( (parseInt(evt.target.value)<parseInt(evt.target.min)) || (parseInt(evt.target.value)>parseInt(evt.target.max)) ){
			evt.target.nextSibling.innerText="Valid Range is "+evt.target.min+"-"+evt.target.max
		}else{
			evt.target.nextSibling.innerText = ""
		}
	}
	handleBinningInput(evt){
		document.getElementById("resolveError").innerText=""
		this.props.dispatch(selectedAnalysisList(evt.target,"association"))
		if(evt.target.value === "" || evt.target.value.startsWith("0")){
			evt.target.nextSibling.innerText = "Please enter a value"
		}else if( (parseFloat(evt.target.value)^0) != parseFloat(evt.target.value) || evt.target.value.includes(".")){
			evt.target.nextSibling.innerText = "Decimals are not allowed"
		}else if( (parseInt(evt.target.value)<parseInt(evt.target.min)) || (parseInt(evt.target.value) > parseInt(evt.target.max)) ){
			evt.target.nextSibling.innerText="Value Range is "+evt.target.min+"-"+evt.target.max
		}else{
			evt.target.nextSibling.innerText=""
		}
	}
	handleTrendAnalysis(evt){
		this.props.dispatch(selectedAnalysisList(evt.target,"trend"))
	}
	renderAllAnalysisList(analysisList,trendSettings){
		let associationPlaceholder = "1-"+ store.getState().datasets.dataSetDimensions.length;
		let customMaxValue = store.getState().datasets.dataSetDimensions.length;

		let list =   analysisList.map((metaItem,metaIndex) =>{
			let id = "chk_analysis_advance"+ metaIndex;
			let disableElement = false;
			if(metaItem.name == "performance")
			disableElement = store.getState().datasets.advancedAnalysisPerformance;
			else if(metaItem.name == "prediction")
			disableElement = store.getState().datasets.advancedAnalysisPrediction;
			else if(metaItem.name == "association")
			disableElement = store.getState().datasets.advancedAnalysisAssociation;
			else if(metaItem.name == "influencer")
			disableElement = store.getState().datasets.advancedAnalysisInfluencer;
			if(metaItem.name.indexOf("trend") != -1){
				if(trendSettings){
					var specificMeasureClsName = "col-md-8 visibilityHidden";
					let specificMeasureStatus = false;
					let trendSub = trendSettings.map((trendSubItem,trendSubIndex)=>{
						let val = trendSubItem.name;
						if(trendSubItem.name.toLowerCase() == "count"){
							return(
									<li key={trendSubIndex}><div className="col-md-4"><div className="ma-checkbox inline sub-analysis"><input className="possibleSubAnalysis" id="trend-count" type="radio" value="count" name="trend-sub"  defaultChecked={trendSubItem.status} onChange={this.handleTrendAnalysis.bind(this)}  /><label htmlFor="trend-count">Count</label></div></div><div class="clearfix"></div></li>
							);
						}else if(trendSubItem.name.toLowerCase().indexOf("specific measure") != -1){
							if(trendSubItem.status){
								specificMeasureClsName ="col-md-8";
								specificMeasureStatus = true;
							}
							return(
								<li key={trendSubIndex} ><div className="col-md-4">
									<div className="ma-checkbox inline sub-analysis"><input className="possibleSubAnalysis" id="trend-specific-measure" type="radio" value="specific measure" name="trend-sub"  defaultChecked={specificMeasureStatus}  onChange={this.handleTrendAnalysis.bind(this)} /><label htmlFor="trend-specific-measure">Specific Measure</label></div>
									</div>
									<div className={specificMeasureClsName}> <select id="specific-trend-measure" className="form-control " onChange={this.handleTrendAnalysis.bind(this)}>
									{store.getState().datasets.dataSetMeasures.map(function(item,index){
										return(<option key={index}>{item.name}</option>)
									})
									}
									</select>
									</div>
								</li>
							);
						}
					})
					return(
						<li key={metaIndex}><div className="ma-checkbox inline"><input id={id} type="checkbox" className="possibleAnalysis" value={metaItem.name} defaultChecked={metaItem.status} onClick={this.handleAnlysisListActions.bind(this)}  /><label htmlFor={id}>{metaItem.displayName}</label></div>
							<ul className="list-unstyled">
								{trendSub}
							</ul>
						</li>);
				}else{
					return(
						<li key={metaIndex}><div className="ma-checkbox inline"><input id={id} type="checkbox" className="possibleAnalysis" value={metaItem.name} defaultChecked={metaItem.status} onClick={this.handleAnlysisListActions.bind(this)}  /><label htmlFor={id}>{metaItem.displayName}</label></div></li>)
				}
			}else{
				if(metaItem.name.indexOf("influencer") != -1){
					associationPlaceholder = "1-"+ (store.getState().datasets.dataSetMeasures.length -1);
					customMaxValue = store.getState().datasets.dataSetMeasures.length -1;
				}
				var countOptions=null, binOptions=null,binTemplate = null,options=[],customValueInput=null,customInputDivClass="col-md-5 md-p-0 visibilityHidden";
				var tooltipText = <Tooltip id="tooltip">Value should be less than or equal to {customMaxValue}</Tooltip>;
				if(metaItem.noOfColumnsToUse!= null){
					options = metaItem.noOfColumnsToUse.map((subItem,subIndex)=>{
						let clsName = "sub-level-analysis-count";
						let name = metaItem.name
						let idName = metaItem.name +"-level-"+subItem.name;
						let labelCls ="btn btn-default";
						let status = false;
						if(subItem.name.indexOf("custom") !=-1){
							let  customClsName = metaItem.name +"-level form-control";
							let customName = metaItem.name;
							let customIdName = metaItem.name +"-level-custom-val";
							if(subItem.status){
								customInputDivClass = "col-md-5 md-p-0";
							}
							customValueInput = <div><OverlayTrigger  placement="top" overlay={tooltipText} disabled={disableElement}><input type="number" id={subIndex} min="1" max={customMaxValue} value={subItem.value===null?"":subItem.value} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault()} onChange={this.handleCustomInput.bind(this)} placeholder={associationPlaceholder} className={customClsName} id={customIdName} name={customName} disabled={disableElement}/></OverlayTrigger><div className="error_pt "></div></div>
						}
						if(subItem.status){
							labelCls ="btn btn-default active";
							status = true;
						}
						return(
							<label key={subIndex} class={labelCls} onClick={this.handleSubLevelAnalysis.bind(this)} disabled={disableElement}><input type="radio" className={clsName} id={idName} name={name} value={subItem.name} defaultChecked={status} disabled={disableElement}/>{subItem.displayName}</label>
						);
					});
					countOptions  = (function(){
						return(
							<div>
								<div className="col-md-7 md-pl-20">
									<div className="btn-group radioBtn" data-toggle="buttons">
										{options}
									</div>
								</div>
								<div className={customInputDivClass} id="divCustomInput">
									{customValueInput}
								</div>
							</div>
						);
					})();
				}
				if(metaItem.hasOwnProperty("binSetting")){
					binTemplate = metaItem.binSetting.map((binItem,binIndex)=>{
						if(!binItem.hasOwnProperty("defaultValue")){
							return (<label className=" xs-pl-20" key={binIndex}><b>{binItem.displayName}</b></label>)
						}else{
							return (<div key={binIndex} className="form-group md-pt-15" id={binIndex}><label for="fl1" className="col-sm-7 xs-pl-20">{binItem.displayName}</label>
								<div className="col-sm-5" style={{padding:"0px 0px 20px 0px"}}>
									<input id={binIndex} type="number" name={metaItem.name}  className="form-control" min={binItem.min} max={binItem.max} placeholder={binItem.defaultValue} defaultValue={binItem.value} onKeyDown={ (evt) => evt.key === 'e' && evt.preventDefault()}   onChange={this.handleBinningInput.bind(this)} disabled={disableElement}/>
									<div className="error_pt "></div>
								</div>
							</div>)
						}
					});

					binOptions  = (function(){
						return(
							<div>
								<div className="col-md-12" style={{padding:"20px 0px 0px 0px"}}>
									{binTemplate}
								</div>
							</div>
						);
					})();
				}

				return(
					<li key={metaIndex}><div className="ma-checkbox inline"><input id={id} type="checkbox" className="possibleAnalysis" value={metaItem.name} defaultChecked={metaItem.status} onClick={this.handleAnlysisListActions.bind(this)} disabled={disableElement} /><label htmlFor={id}>{metaItem.displayName}</label></div>
						<div className="clearfix"></div>
						{countOptions}
						<div className="clearfix"></div>
						{binOptions}
					</li>
				);
			}
		});
		return list;
	}

	render() {
		let dataPrev = store.getState().datasets.dataPreview;
		let renderModalAnalysisList = null;
		if(dataPrev){
			let possibleAnalysisList = store.getState().datasets.dataSetAnalysisList;
			let trendSettings = null;
			if(!$.isEmptyObject(possibleAnalysisList)){
				if(this.props.getVarType == "dimension"){
					possibleAnalysisList = possibleAnalysisList.dimensions.analysis;
					trendSettings = store.getState().datasets.dataSetAnalysisList.dimensions.trendSettings;
					renderModalAnalysisList = this.renderAllAnalysisList(possibleAnalysisList,trendSettings);
				}else if(this.props.getVarType == "measure"){
					possibleAnalysisList = possibleAnalysisList.measures.analysis;
					trendSettings = store.getState().datasets.dataSetAnalysisList.measures.trendSettings;
					renderModalAnalysisList = this.renderAllAnalysisList(possibleAnalysisList,trendSettings);
				}
			}
		}
		return (
			<div id="idAdvanceSettings">
				<Modal show={store.getState().signals.advanceSettingsModal} backdrop="static" onHide={this.closeAdvanceSettingsModal.bind(this)} dialogClassName="modal-colored-header">
					<Modal.Header closeButton>
						<h3 className="modal-title">Advance Settings</h3>
					</Modal.Header>
					<Modal.Body>
						<ul className="list-unstyled">
							{renderModalAnalysisList}
						</ul>
					</Modal.Body>
					<Modal.Footer>
						<div className="error_pt" id="resolveError" style={{float:"left"}}></div>
						<Button onClick={this.closeAdvanceSettingsModal.bind(this)}>Cancel</Button>
						<Button bsStyle="primary" onClick={this.updateAdvanceSettings.bind(this)}>Save</Button>
					</Modal.Footer>
				</Modal>
			</div>
		);
	}
}
