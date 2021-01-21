import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {Card} from "./Card";
import {STATIC_URL} from "../../helpers/env.js"
import {clearToggleValue} from "../../actions/signalActions";

@connect((store) => {
	return {
		 signal: store.signals.signalAnalysis
	};
})

export class MasterSummary extends React.Component {
  constructor() {
    super();
  }

  componentDidMount(){
    this.props.dispatch(clearToggleValue());    
  }
  render() {
    let heading = this.props.signal.name;
    var summary, mText, dText, tText,cardData,count
    cardData = this.props.signal.listOfCards[0].cardData
		count = [cardData.noOfDimensions,cardData.noOfMeasures,cardData.noOfTimeDimensions]
		summary = cardData.summaryHtml;
    dText = count[0] > 1 ? "Dimensions" : "Dimension";
  	mText = count[1] > 1 ? "Measures" : "Measure";
    tText = count[2] > 1 ? "Time Dimensions": "Time Dimension";

		let firstOverviewSlug = this.props.signal.listOfNodes[0].slug;
		
		var texts=[dText,mText,tText]
		var images=['s_d_carIcon.png','s_m_carIcon.png','s_timeDimension.png']
	  var renderBoxContent=count.map((item,i)=>
			 <div key={i} className="col-md-4 wow bounceIn" data-wow-offset="20" data-wow-iteration="20">
				<div className="box-shadow xs-p-10 summaryCardHeight">
					<div className="col-xs-9">
						<h4 class="xs-mt-15">
							<img src={STATIC_URL + "assets/images/"+images[i]} /> {texts[i]}
						</h4>
					</div>
						<h2 style={{marginLeft:'225px'}}> 							
						{item}
						</h2>
				</div>
			</div>
		)

    const overViewLink = "/signals/" + this.props.signalId + "/" + firstOverviewSlug;
    return (
			<div className="side-body">
				<div className="page-head">
				</div>
				<div className="main-content">
					<div class="row">
						<div class="col-md-12">
								<h3 className="xs-mt-0 xs-mb-0 text-capitalize"> {heading}</h3>
							</div>
					</div>
					<div class="row xs-pt-50" >
						<div class="col-md-3 wow bounceIn" data-wow-offset="10"  data-wow-iteration="10">
							<img src={STATIC_URL + "assets/images/data_overview.png"} className="img-responsive xs-mt-50"/>
						</div>
						<div class="col-md-9">
							<div class="row xs-mt-30">					
								{renderBoxContent}
							</div>
									
							<div class="row wow bounceIn" data-wow-offset="20"  data-wow-iteration="20">					
								<div className="col-md-12 xs-pt-50">
									<Card cardData={summary}/>
								</div>
							</div>
									
							<div class="row wow bounceIn" data-wow-offset="20"  data-wow-iteration="20">					
								<div className="col-md-12 xs-pt-50 text-right">
									<Link to={overViewLink} className="btn btn-primary btn-md xs-pl-20 xs-pr-20 xs-pt-10 xs-pb-10">
											<i className="fa fa-file-text-o"></i>  View Summary
										</Link>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
    );
	}
}
