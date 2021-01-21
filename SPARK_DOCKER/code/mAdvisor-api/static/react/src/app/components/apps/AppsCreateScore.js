import React from "react";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import {Modal,Button} from "react-bootstrap";
import store from "../../store";
import {showCreateScorePopup,hideCreateScorePopup,updateSelectedAlg,updateModelSummaryFlag,checkCreateScoreToProceed,updateSelectedAlgObj} from "../../actions/appActions";
import {getAllDataList,getDataSetPreview,storeSignalMeta,updateDatasetName} from "../../actions/dataActions";


@connect((store) => {
	return {
		dataPreview: store.datasets.dataPreview,
		appsScoreShowModal:store.apps.appsScoreShowModal,
		dataPreviewFlag:store.datasets.dataPreviewFlag,
	};
})

export class AppsCreateScore extends React.Component {
	constructor(props) {
		super(props);
		this.selectedData="";
	}
	componentWillMount() {
		this.props.dispatch(getAllDataList());
		this.props.dispatch(storeSignalMeta(null,"/apps/"+store.getState().apps.currentAppId+"/analyst/scores"));
		this.props.dispatch(hideCreateScorePopup());
		this.props.dispatch(updateModelSummaryFlag(false));
	}
	openScorePopup(){
		this.props.dispatch(showCreateScorePopup())
	}
	
	findMaxEvaluationMetricValue(algorithms){
		let max=0
		for( let i=0;i<algorithms.length;i++){
			if(algorithms[i].evaluationMetricValue>max)
				max=algorithms[i].evaluationMetricValue
		}
		return max
	}
	
	closeScorePopup(){
		this.props.dispatch(hideCreateScorePopup())
	}
	
	getDataSetPreview(e){
		this.selectedData = $("#score_Dataset").val();
		this.props.dispatch(checkCreateScoreToProceed(this.selectedData));
		this.props.dispatch(updateSelectedAlg($("#algorithms").val()));
		this.props.dispatch(updateSelectedAlgObj($("#algorithms").find(":selected").data("value")));
		this.props.dispatch(getDataSetPreview(this.selectedData));
		this.props.dispatch(hideCreateScorePopup());
	}
	 
	updateDataset(e){
		this.props.dispatch(updateDatasetName(e.target.value));
	}

	render() {
		if(store.getState().datasets.dataPreviewFlag){
			var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
			let _link = "/apps/"+store.getState().apps.currentAppDetails.slug+modeSelected+"/models/"+store.getState().apps.modelSlug+"/data/"+store.getState().datasets.selectedDataSet;
			return(<Redirect to={_link}/>);
		}
		const dataSets = store.getState().datasets.allDataSets.data;
		const algorithms = store.getState().apps.algorithmsList;
		let renderSelectBox = null;
		let algorithmNames = null;
		if(dataSets){
			renderSelectBox = <select id="score_Dataset" name="selectbasic" onChange={this.updateDataset.bind(this)}  class="form-control">
			{dataSets.map(dataSet =>
			<option key={dataSet.slug} value={dataSet.slug}>{dataSet.name}</option>
			)}
			</select>
		}else{
			renderSelectBox = "No Datasets"
		}
		if(algorithms){
			let max_evaluationMetricValue=this.findMaxEvaluationMetricValue(algorithms)	
			var selectedValue=algorithms.filter(algorithm =>(algorithm.evaluationMetricValue==max_evaluationMetricValue))[0].slug
			algorithmNames = <select id="algorithms" defaultValue={selectedValue} name="selectbasic" class="form-control">
				{algorithms.map(algorithm => <option key={algorithm.slug+algorithm['Model Id']} data-value={JSON.stringify(algorithm)} value={algorithm.slug}>{algorithm.name}-{algorithm['Model Id']}-{algorithm.evaluationMetricValue}({algorithm.evaluationMetricName})</option>)
			}
			</select>
		}else{
			algorithmNames = "No Algorithms"
		}
		return (
			<span className="xs-pl-10" onClick={this.openScorePopup.bind(this)}>
				<Button bsStyle="primary">Create Score</Button>
				<div id="newScore"  role="dialog" className="modal fade modal-colored-header">
				<Modal show={this.props.appsScoreShowModal} onHide={this.closeScorePopup.bind(this)} dialogClassName="modal-colored-header">
					<Modal.Header closeButton>
						<h3 className="modal-title">Create Score</h3>
					</Modal.Header>
					<Modal.Body>
				  	<div class="form-group">
				  		<label className="pb-2">Select an existing dataset</label>
							{renderSelectBox}
							<br/>
							<label>Select a Model</label>
							{algorithmNames}
						</div>
					</Modal.Body>
					<Modal.Footer>
						<Button className="btn btn-primary md-close" onClick={this.closeScorePopup.bind(this)}>Close</Button>
						<Button bsStyle="primary"  onClick={this.getDataSetPreview.bind(this)} >Create</Button>
					</Modal.Footer>
				</Modal>
			</div>
		</span>
		)
	}
}
