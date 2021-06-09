import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import store from "../../store";
import {Tabs,Tab} from "react-bootstrap";
import {Card} from "../signals/Card";
import {getListOfCards,getRoboDataset} from "../../actions/appActions";
import {hideDataPreview} from "../../actions/dataActions";
import {STATIC_URL} from "../../helpers/env.js"
import {isEmpty} from "../../helpers/helper";

@connect((store) => {
	return {
		signal: store.signals.signalAnalysis,
		roboDatasetSlug:store.apps.roboDatasetSlug,
		};
})


export class RoboDocumentMode extends React.Component {
  constructor(props) {
    super(props);
  }
  componentWillMount() {
		this.props.dispatch(hideDataPreview());
		  if (isEmpty(this.props.signal)) {
			  this.props.dispatch(getRoboDataset(this.props.match.params.slug));
		}
	}

  render() {
    const roboSummary = store.getState().signals.signalAnalysis;
	 if (!$.isEmptyObject(roboSummary)) {
		let firstSlug = this.props.signal.slug;
	  let cardModeLink = "/apps-robo/" + store.getState().apps.roboDatasetSlug + "/"+ firstSlug;
	  let listOfCardList = getListOfCards(roboSummary.listOfCards)
		let cardDataList = listOfCardList.map((data, i) => {
			 return (<Card key={i} cardData={data} />)
		                    });
		if(listOfCardList){
			return (
			          <div className="side-body">
			          
			          <div className="main-content">
			          <div className="row">
		                <div className="col-md-12">
								<h3 className="xs-mt-0">{store.getState().apps.roboSummary.name}
							  
							    <div className="btn-toolbar pull-right">
		                        <div className="btn-group btn-space">
		                        <Link className="tabs-control right grp_legends_green continue" to={cardModeLink}>
		                          <button type="button" className="btn btn-default" title="Card mode">
		                            <i class="fa fa-columns"></i>
		                          </button>
		                          </Link>
		                          <button type="button" className="btn btn-default" disabled = "true" title="Document Mode">
		                              <i style={{fontSize:16}} class="fa fa-file-text-o fa-2x"></i>
		                            </button>
							   <Link className="continue" to="/apps-robo">
		                          <button type="button" className="btn btn-default">
		                            <i class="fa fa-times"></i>
		                          </button>
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
