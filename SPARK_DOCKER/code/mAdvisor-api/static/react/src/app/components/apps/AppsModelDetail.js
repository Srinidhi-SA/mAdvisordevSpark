import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import {Button} from "react-bootstrap";
import {AppsCreateScore} from "./AppsCreateScore";
import {Card} from "../signals/Card";
import {getAppsModelSummary,updateModelSlug,handleExportAsPMMLModal,getAppDetails,updateModelSummaryFlag, getAppsAlgoList, clearAppsAlgoList} from "../../actions/appActions";
import {storeSignalMeta} from "../../actions/dataActions";
import {STATIC_URL} from "../../helpers/env.js"
import {isEmpty} from "../../helpers/helper";
import {Link} from "react-router-dom";
import {ExportAsPMML} from "./ExportAsPMML";
import {AppsModelHyperDetail} from "./AppsModelHyperDetail"

@connect((store) => {
	return {
		modelList:store.apps.modelList,
		modelSummary:store.apps.modelSummary,
		modelSlug:store.apps.modelSlug,
		currentAppId:store.apps.currentAppId,
		currentAppDetails:store.apps.currentAppDetails,
	};
})


export class AppsModelDetail extends React.Component {
  constructor(props) {
    super(props);
		this.state={
			showHyperparameterSummary:false
		}
  }
  componentWillMount() {
		this.props.dispatch(storeSignalMeta(null,this.props.match.url));
		if(this.props.currentAppDetails == null)
			this.props.dispatch(getAppDetails(this.props.match.params.AppId));
		if(isEmpty(this.props.modelSummary)){
			this.props.dispatch(getAppsModelSummary(this.props.match.params.slug));
			this.props.dispatch(updateModelSlug(this.props.match.params.slug));
		}
		this.props.dispatch(clearAppsAlgoList());
	}
	
	print() {
		window.print();
	}

	componentDidMount() {
		if(document.getElementsByClassName("noTable")[0] !=undefined){
			document.getElementsByClassName("noTable")[0].parentElement.parentElement.nextElementSibling.className = "col-md-8 col-md-offset-2"
			let element = document.getElementsByClassName("noTable")[0].parentElement.parentElement.nextElementSibling.children[0].firstElementChild;
			element.remove()
		}
		if(Object.keys(this.props.modelList).length != 0 && this.props.modelList.data.filter(i=>i.slug === this.props.modelSlug)[0].viewed === false){
			$(".notifyBtn").trigger('click');
		}
		window.scrollTo(0, 0);
		if(!isEmpty(store.getState().apps.modelSummary)){
			if(store.getState().apps.modelSummary.slug != store.getState().apps.modelSlug)
			this.props.dispatch(getAppsModelSummary(store.getState().apps.modelSlug));
		}
		this.props.dispatch(getAppsAlgoList(1));
		
		let selAlgoList = Object.values(this.props.modelSummary.TrainAlgorithmMapping)
		let noOfHeads = $(".sm-mb-20").length;
			for(var i=0;i<noOfHeads;i++){
				let algoNam = $(".sm-mb-20")[i].innerText.replace(/ /g,'').toLocaleUpperCase();
				let regAlgoName=$(".sm-mb-20")[i].textContent
				let algorithmName = ""
				if(algoNam === "LOGISTICREGRESSION")
					algorithmName = "LG"
				else if(algoNam === "XGBOOST")
					algorithmName = "XG"
				else if(algoNam === "RANDOMFOREST")
					algorithmName = "RF"
				else if(algoNam === "NAIVEBAYES")
					algorithmName = "NB"
				else if(algoNam === "NEURALNETWORK(PYTORCH)")
					algorithmName = "PT"
				else if(algoNam === "NEURALNETWORK(TENSORFLOW)")
				  algorithmName = "TF"
				else if(algoNam === "NEURALNETWORK(SKLEARN)")
				  algorithmName = "NN"
				else if(algoNam === "ENSEMBLE")
				  algorithmName = "EN"
				else if(algoNam === "ADABOOST")
					algorithmName = "ADAB"
				else if(algoNam === "LIGHTGBM")
					algorithmName = "LGBM"
				else if(regAlgoName ==="Gradient Boosted Tree RegressionSummary")
		      algorithmName = "GB"
				else if(regAlgoName==="Random Forest RegressionSummary")
			   	algorithmName = "RFR"
				else if(regAlgoName==="Decision Tree RegressionSummary")
			  	algorithmName = "DT"
				else if(regAlgoName==="Linear RegressionSummary")
				  algorithmName = "LR"
				else if(regAlgoName==="Neural Network (TensorFlow)Summary")
				  algorithmName = "TF"
				else 
					algorithmName = ""
				
				if(algorithmName != ""){
					let info = document.createElement('a');
					var att = document.createAttribute("class");
					att.value = this.props.currentAppId==13?"summaryLinkReg":"summaryLink";
					info.setAttributeNode(att);
					var modelName= store.getState().apps.modelSummary.name;
					let sel = selAlgoList.filter(i => (i.model_id).includes(algorithmName+"_"))
					this.props.currentAppId==13? document.getElementsByTagName('small')[i].hidden=true:"";
					if( (sel.length!=0) && (!modelName.includes("shared")) ){
						info.innerText = "(For More Info Click Here)";
						info.href = this.props.match.url.replace("models/"+this.props.modelSlug,"modelManagement/"+sel[0].slug);
						this.props.currentAppId==13?$(".sm-mb-20")[i].parentNode.appendChild(info):$(".sm-mb-20")[i].parentNode.parentNode.appendChild(info);
					}
				}
			}
	}

  componentDidUpdate(){
		$(".chart-data-icon").next("div").next("div").removeClass("col-md-7 col-md-offset-2").addClass("col-md-10")
  }
  handleExportAsPMMLModal(flag){
		this.props.dispatch(handleExportAsPMMLModal(flag))
  }
  updateModelSummaryFlag(flag){
		this.props.dispatch(updateModelSummaryFlag(flag))
  }
	gotoHyperparameterSummary(){
		this.setState({showHyperparameterSummary:true})
	}
  render() {
		if(document.querySelector(".sm-pb-10")!= null ){
			let FE = document.querySelector(".sm-pb-10")
			if(FE.innerText==="Feature Importance") {
				FE.style.display = "none";
				document.querySelector(".chart-area").style.display = "none";
			}
		}
		if(this.state.showHyperparameterSummary)
			return(<AppsModelHyperDetail match={this.props.match}/>)
  	const modelSummary = store.getState().apps.modelSummary;
	 	var showExportPmml = true;
		var showCreateScore = true;
		var hyperParameterData;
		let mlink = window.location.pathname.includes("analyst")?"/analyst":"/autoML"
		if (!$.isEmptyObject(modelSummary)) {
			hyperParameterData = store.getState().apps.modelSummary.data.model_hyperparameter;
      showExportPmml = modelSummary.permission_details.downlad_pmml;
			showCreateScore = modelSummary.permission_details.create_score;
			var failedAlgorithms =	modelSummary.data.config.fail_card.filter(i=>i.success==="False").map(i=>i.Algorithm_Name).map(a => a.charAt(0).toUpperCase() + a.substr(1)).join(', ');
			var listOfCardList = modelSummary.data.model_summary.listOfCards;	
			var componentsWidth = 0;
			var cardDataList = "";
			if(!$.isEmptyObject(listOfCardList)){
				cardDataList = listOfCardList.map((data, i) => {
					var clearfixClass = "col-md-"+data.cardWidth*0.12+" clearfix";
					var nonClearfixClass = "col-md-"+data.cardWidth*0.12;
					var cardDataArray = data.cardData;
					if(cardDataArray.length>0){
						if((cardDataArray.filter(i=>(i.dataType==="table" && i.data.tableData.length===1))).length!=0 ){
							let newData = {}
							newData = cardDataArray[0]
							cardDataArray = []
							cardDataArray[0] = newData
							cardDataArray[0].classTag = "noTable"
						}
						if(data.cardWidth == 100){
							componentsWidth = 0;
							return (<div key={i} className={clearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
						}else if(componentsWidth == 0 || componentsWidth+data.cardWidth > 100){
							componentsWidth = data.cardWidth;
							return (<div key={i} className={clearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
						}else{
							componentsWidth = componentsWidth+data.cardWidth;
							return (<div key={i} className={nonClearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
						}
					}else{
						componentsWidth = componentsWidth+data.cardWidth;
						return (<div key={i} className={nonClearfixClass}></div>)
					}
				});
			}
			if(listOfCardList){
				return(
					<div className="side-body">
						<div className="main-content">
							<div className="row">
								<div className="col-md-12">
								<h3 className="xs-mt-0">{store.getState().apps.modelSummary.name}
									<div className="btn-toolbar pull-right">
										<div className="btn-group summaryIcons">
											<button type="button" className="btn btn-default" onClick={this.print.bind(this)} title="Print Document"><i className="fa fa-print"></i></button>
											<button type="button" className="btn btn-default" disabled = "true" title="Document Mode">
												<i class="fa fa-columns"></i>
											</button>
											<Link className="btn btn-default continue btn-close" to={`/apps/${this.props.match.params.AppId}${mlink}/models`} onClick={this.updateModelSummaryFlag.bind(this,false)}>
												<i class="fa fa-times"></i>
											</Link>
										</div>
									</div>
								</h3>
								<div className="clearfix"></div>
								<div className={this.props.match.params.AppId === "regression-app-6u8ybu4vdr"?"panel panel-mAd documentModeSpacing box-shadow regSpacing":"panel panel-mAd documentModeSpacing box-shadow"}>
									<div className="panel-body no-border">
										<div className="container-fluid">
											{cardDataList}
										</div>
										{failedAlgorithms.length>0 && <div>* Failed Algorithms: {failedAlgorithms}.</div>}
										<div className="col-md-12 text-right xs-mt-30">
											{!$.isEmptyObject(hyperParameterData)?
												<span>
													<Button bsStyle="primary" onClick={this.gotoHyperparameterSummary.bind(this,true)}><i className="fa fa-undo"></i> Back</Button>
													<span className="xs-pl-10"></span>
												</span>:""
											}
											{showExportPmml?<Button bsStyle="primary" onClick={this.handleExportAsPMMLModal.bind(this,true)}>Export As PMML</Button>:""}
											{showCreateScore? <AppsCreateScore match={this.props.match}/>:""}
										</div>   
									</div>
									<ExportAsPMML/>
								</div>
							</div>
						</div>
					</div>
				</div>
				);
			}
		}
		else{
			return (
				<div className="side-body">
						<img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
				</div>
			);
		}
	}
}
