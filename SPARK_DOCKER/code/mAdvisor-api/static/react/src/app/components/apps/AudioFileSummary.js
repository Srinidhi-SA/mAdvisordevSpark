import React from "react";
import { connect } from "react-redux";
import store from "../../store";
import {STATIC_URL} from "../../helpers/env.js"
import {isEmpty} from "../../helpers/helper";
import {getAudioFile,getListOfCards,updateAudioFileSummaryFlag} from "../../actions/appActions";
import {Card} from "../signals/Card";
import {Link} from "react-router-dom";

@connect((store) => {
	return {
		audioFileSummary:store.apps.audioFileSummary,
	};
})

export class AudioFileSummary extends React.Component {
	constructor(){
		super();
	}
	componentWillMount() {
		//It will trigger when refresh happens on url
		if(isEmpty(this.props.audioFileSummary)){
			this.props.dispatch(getAudioFile(this.props.match.params.audioSlug));   
		}
	}

	componentDidMount() {
		if(!$.isEmptyObject(store.getState().apps.audioFileSummary)){
			if(store.getState().apps.audioFileSummary.slug != store.getState().apps.audioFileSlug)
				this.props.dispatch(getAudioFile(store.getState().apps.audioFileSlug));
		}else{
			this.props.dispatch(getAudioFile(store.getState().apps.audioFileSlug));
		}
	}
	updateAudioFlag(){
		this.props.dispatch(updateAudioFileSummaryFlag(false))
	}
	render() {
		const audioSummary = store.getState().apps.audioFileSummary;

		if (!$.isEmptyObject(audioSummary)) {
			let listOfCardList = getListOfCards(audioSummary.meta_data.listOfCards)
			let cardDataList = listOfCardList.map((data, i) => {
				if(i == 1)
					return (<div className="col-md-4"><Card key={i} cardData={data} /></div>)
			    if(i == 2)
					return (<div><div className="col-md-8"><Card key={i} cardData={data} /></div><div class="clearfix"></div></div>)
				else return (<Card key={i} cardData={data} />)

			});
			if(listOfCardList){
				return (
						<div className="side-body">

						<div className="page-head">
			          <div class="clearfix"></div>
			      </div>
			            
						<div className="main-content">
						<div className="row">
						<div className="col-md-12">

						<div className="panel panel-mAd documentModeSpacing box-shadow">
						<div className="panel-heading">
						<h3 className="xs-mt-0">{store.getState().apps.audioFileSummary.name}

						<div className="btn-toolbar pull-right">
						<div className="btn-group btn-space">

						<button type="button" className="btn btn-default" disabled="true" title="Document Mode">
                              <i class="fa fa-columns"></i>
                        </button>
						<Link className="continue btn btn-default" onClick={this.updateAudioFlag.bind(this)} to="/apps/audio">						 
						<i class="fa fa-times"></i>						 
						</Link>
						</div>
						</div>
</h3>
						<div className="clearfix"></div>
						</div>
						<div className="panel-body no-border">
						<div className="row-fluid"> 

						{cardDataList}

						</div>

						</div>
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

