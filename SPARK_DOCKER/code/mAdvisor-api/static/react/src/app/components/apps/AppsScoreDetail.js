import React from "react";
import {connect} from "react-redux";
import store from "../../store";
import {Card} from "../signals/Card";
import {getListOfCards,getAppsScoreSummary,updateScoreSlug,getAppDetails,updateScoreSummaryFlag, clearScoreSummary} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js";
import {isEmpty} from "../../helpers/helper";
import {API} from "../../helpers/env";
import {Link} from "react-router-dom";


@connect((store) => {
	return {
		scoreSummary:store.apps.scoreSummary,
		currentAppDetails:store.apps.currentAppDetails,
		};
})

export class AppsScoreDetail extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
		this.props.dispatch(getAppDetails(this.props.match.params.AppId));
		if(isEmpty(this.props.scoreSummary)){
			this.props.dispatch(getAppsScoreSummary(this.props.match.params.slug));
			this.props.dispatch(updateScoreSlug(this.props.match.params.slug))
		}
  }
  componentDidMount() {
		window.scrollTo(0, 0);
	  if(!isEmpty(store.getState().apps.scoreSummary)){
		  if(store.getState().apps.scoreSummary.slug != store.getState().apps.scoreSlug)
		  this.props.dispatch(getAppsScoreSummary(store.getState().apps.scoreSlug));
	  }
  }
  updateScoreSummaryFlag(){
		this.props.dispatch(updateScoreSummaryFlag(false));
  }
  render() {
		let scoreSummary = store.getState().apps.scoreSummary;
		let slink = window.location.pathname.includes("analyst")?"/analyst":"/autoML";
		var scoreSlugtoDownload=(store.getState().apps.scoreSlugShared==null||store.getState().apps.scoreSlugShared==undefined)?store.getState().apps.scoreSlug:store.getState().apps.scoreSlugShared;
    var showViewButton = true;
    var showDownloadButton = true;
		if (!$.isEmptyObject(scoreSummary) && (this.props.scoreSummary.slug === this.props.match.params.slug)) {
			showViewButton = scoreSummary.permission_details.download_score;
			showDownloadButton = scoreSummary.permission_details.download_score;
			if(this.props.currentAppDetails != null && this.props.currentAppDetails.app_type == "REGRESSION"){
				var listOfCardList = scoreSummary.data.listOfCards;
				var componentsWidth = 0;
				var skipIndex=[]
				var cardDataList = listOfCardList.map((data, i) => {
					if(skipIndex.includes(i)){ 
						return null;
					}
					var clearfixClass = "col-md-"+data.cardWidth*0.12+" clearfix";
					var nonClearfixClass = "col-md-"+data.cardWidth*0.12;
					if(data.centerAlign){
						var clearfixClass = "col-md-"+data.cardWidth*0.12+" clearfix cardKpi ov_card_boxes";
						var nonClearfixClass = "col-md-"+data.cardWidth*0.12+" cardKpi ov_card_boxes";
					}
					var getList=store.getState().apps.scoreSummary.data.listOfCards;
					var cardDataArray = data.cardData;				
						if(data.cardWidth == 100){
							componentsWidth = 0;
							return (<div class="row"><div className={clearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div></div>)
						}
						else if(i<getList.length-1 && data.cardWidth==50 && getList[i+1].cardWidth==50){
							componentsWidth = 0;
							var hasSubchart=(data.cardData[0].data.chart_c3.subchart!=null && data.cardData[0].data.chart_c3.subchart.show)||(getList[i+1].cardData[0].data.chart_c3.subchart!=null && getList[i+1].cardData[0].data.chart_c3.subchart.show)
              var customClasss=hasSubchart?"row multi hasSubchart":"row multi";
							skipIndex.push(i+1); //adding i+1 to skipIndex array to skip the next itteration
							
							return (<div class={customClasss}><div className={clearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>
							<div className={nonClearfixClass}><Card cardData={getList[i+1].cardData} cardWidth={getList[i+1].cardWidth}/></div>
							</div>)
						}
						else if(componentsWidth == 0 || componentsWidth+data.cardWidth > 100){
							componentsWidth = data.cardWidth;
							return (<div className={clearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
						}
						else{
							componentsWidth = componentsWidth+data.cardWidth;
							return (<div className={nonClearfixClass}><Card cardData={cardDataArray} cardWidth={data.cardWidth}/></div>)
						}			
				});
			}else{
				var listOfCardList = getListOfCards(scoreSummary.data.listOfCards);
				var cardDataList = listOfCardList.map((data, i) => {
					return (<Card key={i} cardData={data} />)
				});
			}
			if(listOfCardList && listOfCardList.length!=0){
				return (
					<div className="side-body">
						<div className="main-content">
							<div className="row">
								<div className="col-md-12">
									<h3 className="xs-mt-0">{store.getState().apps.scoreSummary.name}
										<div className="btn-toolbar pull-right">
											<div className="btn-group summaryIcons">
												<button type="button" className="btn btn-default" disabled = "true" title="Document Mode">
													<i class="fa fa-columns"></i>
												</button>
												<Link className="continue btn btn-default" to={`/apps/${this.props.match.params.AppId}${slink}/scores`} onClick={this.updateScoreSummaryFlag.bind(this,false)}>
													<i class="fa fa-times"></i>
												</Link>
											</div>
										</div>
									</h3>
									<div className="clearfix"></div>
									<div className="panel panel-mAd documentModeSpacing box-shadow">
										<div className="panel-body no-border">
											<div className="row-fluid">
												{cardDataList}
											</div>
											<div className="row">
												<div className="col-md-12 text-right">
													{showViewButton?<Link to={`/apps/${this.props.match.params.AppId}${slink}/scores/${scoreSlugtoDownload}/dataPreview`} className="btn btn-primary xs-pr-10"> View </Link>:""}
													{showDownloadButton?<a  href={`${API}/api/get_score_data_and_return_top_n/?url=${scoreSlugtoDownload}&download_csv=true&count=100`} id="download" className="btn btn-primary" download>Download</a>:""}
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				);
			}
		}else{
			return (
				<div className="side-body">
						<img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
				</div>
			);
		}
	}
	componentWillUnmount(){
		this.props.dispatch(clearScoreSummary())
	}
}
