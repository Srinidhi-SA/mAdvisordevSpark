import React from "react";
import {connect} from "react-redux";
import {API} from "../../helpers/env";
import {getUserDetailsOrRestart,statusMessages} from "../../helpers/helper";
import {Modal,Button} from "react-bootstrap";
import store from "../../store";
import {closeModelPopup,openModelPopup,updateSelectedVariable,getRegressionAppAlgorithmData,createModel,getAllModelList,selectMetricAction,saveSelectedValuesForModel, clearDataPreview} from "../../actions/appActions";
import {getAllDataList,getDataSetPreview,storeSignalMeta,updateDatasetName,clearDataCleansing,clearFeatureEngineering,dispatchDataPreviewAutoML,resetSelectedVariables} from "../../actions/dataActions";
import {DataSourceList} from "../data/DataSourceList";
import {dataUpload} from "../../actions/dataUploadActions";
import {ACCESSDENIED} from "../../helpers/helper";
import Link from "react-router-dom/Link";

@connect((store) => {
	return {
		appsModelShowModal: store.apps.appsModelShowModal,
		dataPreview: store.datasets.dataPreview,
		currentAppId:store.apps.currentAppId,
		selectedDataSrcType:store.dataSource.selectedDataSrcType,
		currentAppDetails:store.apps.currentAppDetails,
		allModelList: store.apps.allModelList,
		editmodelFlag:store.datasets.editmodelFlag,
		};
})

export class AppsCreateModel extends React.Component {
	constructor(props) {
		super(props);
		this.selectedData="";
		this.state={
			autoMlVal:"",
			countVal:'',
		}
	}

	getHeader(token){
		return {
			'Authorization': token,
			'Content-Type': 'application/json'
		};
	}

	componentWillMount() {
		this.props.dispatch(clearDataPreview())
		this.props.dispatch(getAllDataList());
		this.props.dispatch(storeSignalMeta(null,this.props.match.url));
		this.props.dispatch(closeModelPopup());
		this.props.dispatch(clearDataCleansing());
		this.props.dispatch(clearFeatureEngineering());
		if(window.location.href.includes("autoML")){
			this.props.dispatch(getRegressionAppAlgorithmData(this.props.currentAppDetails.app_type));
		}
	}

	componentDidMount(){
		this.props.dispatch(getAllModelList(this.props.currentAppId));
	}
	
	openModelPopup(){
		this.props.dispatch( resetSelectedVariables(true) );
		this.props.dispatch(saveSelectedValuesForModel("","",""));
    this.props.dispatch(selectMetricAction("","","")); 
		this.props.dispatch(openModelPopup());
	}
	
	closeModelPopup(){
		this.props.dispatch(closeModelPopup())
	}

  getDataSetPreview(e){
		if(document.getElementById("model_Dataset").value === "--Select dataset--"){
			document.getElementById("modelErrorMsg").innerText = "Please select dataset";
			e.preventDefault();
			return false;
		}
		if(store.getState().dataSource.selectedDataSrcType == "fileUpload"){
    	this.selectedData = document.getElementById("model_Dataset").value;
    	this.props.dispatch(getDataSetPreview(this.selectedData));
		}else{
			this.props.dispatch(dataUpload())
		}
	}

	submitAutoMlVal(mode){
		document.getElementById("modelErrorMsg").innerText = "";
		let letters = /^[0-9a-zA-Z\-_\s]+$/;
		var target=$("#createModelTarget option:selected").text();
		var datasetSlug=model_Dataset.value;
		var levelCount=$("#createModelLevelCount").val();
		var modelName= $("#modelName").val();
		
		if ($("#model_Dataset").val() === "--Select dataset--") {
			document.getElementById("modelErrorMsg").innerText = "Please select dataset";
			return false;
		}else if(modelName === "") {
			document.getElementById("modelErrorMsg").innerText = "Please enter model name";
			return false;
		}else if ($("#createModelTarget").val() === "--Select--") {
			document.getElementById("modelErrorMsg").innerText = "Please select target variable";
			return false;
		}else if (levelCount === "--Select--") {
			document.getElementById("modelErrorMsg").innerText = "Please select sub value";
			return false;
		}else if (modelName != "" && modelName.trim() == "") {
			document.getElementById("modelErrorMsg").innerText = "Please enter a valid model name";
			return false;
		}else if (letters.test(modelName) == false){
			document.getElementById("modelErrorMsg").innerText = "Model name cannot contain special characters .,@,#, $,%,!,&";
			return false;
		}else if(!(Object.values(this.props.allModelList).filter(i=>(i.name).toLowerCase() == modelName.toLowerCase()) == "") ){
			document.getElementById("modelErrorMsg").innerText = "Model by name \""+ modelName +"\" already exists. Please enter a new name.";
			return false;
		}
		this.props.dispatch(createModel(modelName,target,levelCount,datasetSlug,mode))
		this.props.dispatch(closeModelPopup())
	}

	fetchDataAutoML(slug) {
		return fetch(API+'/api/datasets/'+slug+'/',{
			method: 'get',
			headers: this.getHeader(getUserDetailsOrRestart.get().userToken)
		}).then((response) => response.json())
		.then((responseJson) => {
			this.setState({ autoMlVal:responseJson })
			this.props.dispatch(dispatchDataPreviewAutoML(responseJson,"1dnjnsj"));
		})
	}

	updateDataset(e){
		document.getElementById("modelErrorMsg").innerText = "";
		this.selectedData = e.target.value;
		if(window.location.pathname.includes("autoML")){
			this.fetchDataAutoML(e.target.value);
		}
		this.props.dispatch(updateDatasetName(e.target.value));
		this.levelCountsForAutoMl(e)
	}
	
	levelCountsForAutoMl(event) {
		var selOption = event.target.childNodes[event.target.selectedIndex];
		var varText = selOption.text;
		if(this.state.autoMlVal != "")
			var uniqueValData = this.state.autoMlVal.meta_data.uiMetaData.columnDataUI.filter(i => i.name==varText).map(j=>j.columnStats)[0];
		if(this.state.autoMlVal !="" && uniqueValData!=undefined && uniqueValData.filter(k=>k.name=="LevelCount")[0] != undefined){ 
			var option = uniqueValData.filter(k=>k.name=="LevelCount")[0].value;
			var category= Object.keys(option);	
			this.setState({countVal:category});
		}else{
			this.setState({countVal:""})
		}
	}
	
  setPossibleList(event) {
		document.getElementById("modelErrorMsg").innerText = "";
		if(this.props.currentAppDetails.app_id === 13){
			let target =  $("#createModelTarget option:selected").text();
			let targetUniqueVal= this.props.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i => i.name=== target)[0].columnStats.filter(j=>j.displayName === "Unique Values")[0].value
			targetUniqueVal <=5 &&
			bootbox.alert(statusMessages("warning","Please proceed with automated prediction to get better results as this dataset has less than 5 unique value for the selected target column"));
		}
		this.levelCountsForAutoMl(event);
		this.props.dispatch(updateSelectedVariable(event));
	}

	clearErrMsg(){
		document.getElementById("modelErrorMsg").innerText = "";
	}

	render() {
	 	const dataSets = store.getState().datasets.allDataSets.data;
		let renderSelectBox = null;
		let hideCreate=false
		if(dataSets){
			renderSelectBox = (
				<div>
					<select id="model_Dataset" name="selectbasic"  onChange={this.updateDataset.bind(this)} class="form-control">
						<option>--Select dataset--</option>
						{dataSets.map(dataSet => <option key={dataSet.slug} value={dataSet.slug}>{dataSet.name}</option>)}
					</select>
					{window.location.href.includes("autoML")&&
						<div>
							<label className="pb-2 pt-10">Model Name</label>
							<input type="text" className="form-control" autoComplete="off" placeholder="model name" id="modelName" onInput={this.clearErrMsg.bind(this)}></input>
							<label className="pb-2 pt-10">Select target variable:</label>
							<select className="form-control" id="createModelTarget" onChange={this.setPossibleList.bind(this)}>
								<option>--Select--</option>
									{this.state.autoMlVal!=""?
										this.props.currentAppDetails.app_id == 13 ?
											this.state.autoMlVal.meta_data.uiMetaData.varibaleSelectionArray.sort((a, b) => {
												if (a.name < b.name)
													return -1;
												if (a.name > b.name)
													return 1;
												return 0;
											}).map(metaItem => {
												if(metaItem.columnType == "measure" && !metaItem.dateSuggestionFlag && !metaItem.uidCol) {
													return (<option key={metaItem.slug} name={metaItem.slug} value={metaItem.columnType}>{metaItem.name}</option>)
												}
											}):
											this.state.autoMlVal.meta_data.uiMetaData.varibaleSelectionArray.sort((a, b) => {
												if (a.name < b.name)
													return -1;
												if (a.name > b.name)
													return 1;
												return 0;
											}).map(metaItem => {
												if (metaItem.columnType != "measure" && metaItem.columnType != "datetime" && !metaItem.dateSuggestionFlag && !metaItem.uidCol) {
													return (<option key={metaItem.slug} name={metaItem.slug} value={metaItem.columnType}>{metaItem.name}</option>)
												}
											})
										: "" }
							</select>
							{this.state.countVal !="" &&
								<div>
									<label className="pb-2 pt-10">Select subvalue:</label>
									<select className="form-control" id="createModelLevelCount" onChange={this.clearErrMsg.bind(this)}>
										<option>--Select--</option>
										{this.state.countVal!=""?
											this.state.countVal.sort().map(item => {
												return (<option key={item} name={item} value={item}>{item}</option>)
											})
											:""
										}
									</select>
								</div>
							}
						</div>
					}
				</div>)
		}else{
			renderSelectBox = "No Datasets"
			if(this.props.selectedDataSrcType=="fileUpload")
				hideCreate=true
		}
		let cls = "newCardStyle firstCard"
		let title = "";
		if(!this.props.isEnableCreate){
			cls += " disable-card";
			title= ACCESSDENIED
		}
		var modeType = window.location.pathname.includes("autoML")?'AutoML':'Analyst';
		return (
			<div class="col-md-3 xs-mb-15 list-boxes xs-mt-20" title={title}>
				<div className={cls} onClick={this.openModelPopup.bind(this)}>
					<div class="card-header"></div>
					<div class="card-center newStoryCard">
						<h2 class="text-center"><i class="fa fa-file-text-o fa-2x"></i> Create Model </h2>				
					</div>
				</div>
				<div id="newModel"  role="dialog" className="modal fade modal-colored-header">
					<Modal show={store.getState().apps.appsModelShowModal} onHide={this.closeModelPopup.bind(this)} dialogClassName="modal-colored-header uploadData">
						<Modal.Header closeButton>
							<h3 className="modal-title">Create Model - {modeType}</h3>
						</Modal.Header>
						<Modal.Body>
							<DataSourceList type="model" renderDatasets={renderSelectBox}/>
						</Modal.Body>
						<Modal.Footer>
	            <div className="text-danger" id="modelErrorMsg" style={{float:"left",textAlign:"left",width:"65%"}}></div>
							<Button className="btn btn-primary md-close" onClick={this.closeModelPopup.bind(this)}>Close</Button>
							{
								window.location.href.includes("autoML")?
								<Button bsStyle="primary" id="modalCreateButtonAutoML" onClick={this.submitAutoMlVal.bind(this,"autoML")}>Create Model</Button>	:
								<Link className="btn btn-primary" id="modalCreateButton" disabled={hideCreate} onClick={this.getDataSetPreview.bind(this)} to={this.props.match.url+"/data/"+store.getState().datasets.selectedDataSet}>Create</Link>
							}
						</Modal.Footer>
					</Modal>
				</div>
			</div>
		)
	}
}