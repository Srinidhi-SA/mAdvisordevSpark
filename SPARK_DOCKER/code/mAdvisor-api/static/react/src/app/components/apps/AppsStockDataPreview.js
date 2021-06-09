import React from "react";
import {Button} from "react-bootstrap";
import {DataPreview} from "../data/DataPreview";
import {StockUploadDomainModel} from "../apps/StockUploadDomainModel";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {connect} from "react-redux";
import {hideDataPreviewRightPanels,updateUploadStockPopup,getConceptsList,updateStockSlug,clearDataPreview,uploadStockAnalysisFlag} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js"
import {getStockDataSetPreview} from "../../actions/dataActions";
import {AppsLoader} from "../common/AppsLoader";

@connect((store) => {
	return {
		dataPreview: store.datasets.dataPreview,
		stockSlug:store.apps.stockSlug,
		stockAnalysisFlag:store.apps.stockAnalysisFlag,
		signal: store.signals.signalAnalysis,
	};
})

export class AppsStockDataPreview extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount(){
		this.props.dispatch(clearDataPreview());
		this.props.dispatch(getStockDataSetPreview(this.props.match.params.slug));
		this.props.dispatch(updateStockSlug(this.props.match.params.slug));
	}
  componentDidMount(){
		hideDataPreviewRightPanels();
		this.props.dispatch(getConceptsList());
	}
  componentWillUpdate(){
	  hideDataPreviewRightPanels();
  }
  componentDidUpdate(){
	  hideDataPreviewRightPanels();
  }
  updateUploadStockPopup(flag){
  	this.props.dispatch(updateUploadStockPopup(flag))
  }
  clearDataPreview(){
	  this.props.dispatch(clearDataPreview());
	  this.props.dispatch(uploadStockAnalysisFlag(false));
  }
  render() {
	  if(store.getState().apps.stockAnalysisFlag && !this.props.showPreview){
			return (<Redirect to={"/apps-stock-advisor/"+store.getState().apps.stockSlug+ "/" + this.props.signal.listOfNodes[0].slug} />);
	 	}
		if(!$.isEmptyObject(store.getState().datasets.dataPreview)){
			return (
				<div>
					<DataPreview history={this.props.history} match={this.props.match}/>          
					<div className="row buttonRow buttonRowChat" >
						<div class="col-md-11 col-md-offset-1 xs-pl-0">
							<div class="panel">
								<div class="panel-body no-border">
									<div className="navbar xs-mb-0 text-right">
										{this.props.showPreview?
											<ul className="nav navbar-nav navbar-right">
												<li className="text-right"><Button onClick={this.props.updatePreviewState} bsStyle="primary"> Close </Button></li>
											</ul>
											:
											<span>
												<Link to="/apps-stock-advisor"><Button onClick={this.clearDataPreview.bind(this)}> Close </Button> </Link>
												&nbsp;&nbsp;&nbsp;
												<Button bsStyle="primary" onClick={this.updateUploadStockPopup.bind(this,true)}> Proceed</Button>
											</span>
										}
									</div>
								</div>
							</div>
						</div>
					</div>
					<StockUploadDomainModel/>
					<AppsLoader match={this.props.match}/>
				</div>
			);
		}else{
			return (
				<div>
					<img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif"} />
				</div>
			);
		}
  }
}
