import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import {Tabs,Tab,Button} from "react-bootstrap";
import {Card} from "../signals/Card";
import {getAppsModelSummary,updateModelSlug,getAppDetails,sendSelectedAlgorithms,clearSelectedModelsCount,clearModelSummary} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {AppsModelDetail} from "./AppsModelDetail"

@connect((store) => {
	return {
		modelSummary:store.apps.modelSummary,
		currentAppDetails:store.apps.currentAppDetails,
		};
})


export class AppsModelHyperDetail extends React.Component {
  constructor(props) {
    super(props);
		this.state = {
			selectedName:"",
			showSummery:false
    };
  }
  componentWillMount() {
		if(this.props.currentAppDetails == null)
			this.props.dispatch(getAppDetails(this.props.match.params.AppId));
		this.props.dispatch(clearModelSummary());
		this.props.dispatch(getAppsModelSummary(this.props.match.params.slug));
		this.props.dispatch(updateModelSlug(this.props.match.params.slug));
	}
  componentDidMount() {
		window.scrollTo(0, 0);
		this.props.dispatch(clearSelectedModelsCount());
  }
  componentWillReceiveProps(){
	  this.setState({showSummery:false});
  }
  saveAndShowModelSummary(){
	  if(!store.getState().apps.modelSummary.data.modelSelected)
	  this.props.dispatch(sendSelectedAlgorithms(this.props.match.params.slug));
	  this.setState({ showSummery:true});
  }
  changeAlgo(e){
	  var that = this;
	  setTimeout(function(){
			that.setState({
				selectedName:e,
			});
		}, 250);
	}

  render() {
	  const modelSummary = store.getState().apps.modelSummary;
	  var hyperParameterData;
	  var pageData = "";
	  if(!$.isEmptyObject(modelSummary))
		  hyperParameterData = store.getState().apps.modelSummary.data.model_hyperparameter;
	  if(!$.isEmptyObject(hyperParameterData) && !$.isEmptyObject(modelSummary) && this.state.showSummery || $.isEmptyObject(hyperParameterData) && !$.isEmptyObject(modelSummary))
	  	return(<AppsModelDetail match={this.props.match}/>)
		if(!$.isEmptyObject(hyperParameterData)){
			hyperParameterData = JSON.stringify(hyperParameterData);
			hyperParameterData = JSON.parse(hyperParameterData);
			var pageData = hyperParameterData.map((data) =>{
				var clearfixClass = "col-md-"+data.cardWidth*0.12+" xs-pl-30 xs-pl-30 xs-pt-5 clearfix removeBreak";
				var cardDataArray = data.cardData;
				var cardId = "id_"+data.slug;
				return(
					<Tab eventKey={data.slug} title={data.name} key={cardId}>
						<div className="row" key={cardId}>
							<div className="form-group">
								<div className={clearfixClass}><Card key={cardId} id={cardId} cardData={cardDataArray} cardWidth={data.cardWidth}/></div>
							</div>
						</div>
					</Tab>
				);
			});
			if(pageData != ""){
				return (
					<div className="side-body">
						<div className="page-head">
							<div className="row">
								<div className="col-md-8">
									<h3 class="xs-mt-0 text-capitalize">{store.getState().apps.modelSummary.name}</h3>
								</div>
							</div>
							<div className="clearfix"></div>
						</div>
						<div className="main-content">
							<div class="row predictions">
								<div class="col-md-12">
									<Tabs id="tabsName" onSelect={this.changeAlgo.bind(this)} className="tab-container">
										{pageData}
									</Tabs>
								</div>
							</div>
							<div className="row">
								<div className="col-lg-12 text-right">
									<Button type="button" onClick={this.saveAndShowModelSummary.bind(this)} bsStyle="primary">{(store.getState().apps.modelSummary.data.modelSelected)?"Model summary":"Save and show Model summary"}</Button>
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
