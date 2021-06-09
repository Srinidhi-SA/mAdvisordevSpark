import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {Card} from "../signals/Card";
import {STATIC_URL} from "../../helpers/env.js";
import {getStockAnalysis} from "../../actions/appActions";
import {isEmpty} from "../../helpers/helper";
import {hideDataPreview} from "../../actions/dataActions";

@connect((store) => {
  return {signal: store.signals.signalAnalysis};
})

export class AppsStockDocumentMode extends React.Component {
  constructor() {
    super();
  }
  componentWillMount() {
    if (isEmpty(this.props.signal)) {
      this.props.dispatch(getStockAnalysis(this.props.match.params.slug))
    }
  }

  print() {
    window.print();
  }

  searchTree(_Node, cardLists, lastVar) {
		if (_Node.listOfCards.length!=0&&_Node.listOfCards[_Node.listOfCards.length - 1].slug == lastVar) {
     cardLists.push(_Node.listOfCards);
      return cardLists;
    } else {
      var i;
      var result = null;
      cardLists.push(_Node.listOfCards);
      for (i = 0; i < _Node.listOfNodes.length; i++) {
        result = this.searchTree(_Node.listOfNodes[i], cardLists, lastVar);
      }
      return result;
    }
  }

  closeDocumentMode(){
    this.props.dispatch(hideDataPreview());
    this.props.history.push("/apps-stock-advisor");
  }
  render() {
    let cardList = [];
    if (!isEmpty(this.props.signal)) {
      let lastCard = this.props.history.location.state.lastVar;
      cardList = this.searchTree(this.props.signal, cardList, lastCard);
      let docObj = [];
      for (let card of cardList) {
        for (let _card of card) {
          docObj.push(_card);
        }
      }
      docObj.splice(0, 1);
      let objs = [];
      docObj.map(function(item, i) {
        let len = item.cardData.length;
        for (var i = 0; i < len; i++) {
          objs.push(item.cardData[i]);
        }
      })
      
      if (objs) {
        return (
          <div className="side-body" id="side-body">
            <div className="main-content">
              <div className="row">
                <div className="col-md-12">
        					<h3 class="xs-mt-0">{this.props.signal.name}
                    <div className="btn-toolbar pull-right">
                      <div className="btn-group btn-space summaryIcons">
                        <button className="btn btn-default" type="button" onClick={this.print.bind(this)} title="Print Document">
                          <i class="fa fa-print" aria-hidden="true"></i>
                        </button>
                            <Link className="tabs-control right grp_legends_green continue" to={`/apps-stock-advisor/${this.props.match.params.slug}/${this.props.signal.listOfNodes[0].slug}`}>
                              <button type="button" className="btn btn-default" title="Card mode">
                                <i class="fa fa-columns"></i>
                              </button>
                            </Link>
                            <button type="button" className="btn btn-default" disabled="true" title="Document Mode">
                              <i style={{fontSize:16}}class="fa fa-file-text-o fa-2x"></i>
                            </button>
                           <button type="button" className="btn btn-default" onClick = {this.closeDocumentMode.bind(this)}>
                                <i class="fa fa-close"></i>
                              </button>
                          </div>
                        </div>


						</h3>
			      			<div className="clearfix"></div>
                  <div className="panel panel-mAd box-shadow">
                    <div className="panel-body no-border documentModeSpacing">
                      <Card cardData={objs}/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      }
    } else {
      return (
        <div className="side-body">
          <div className="page-head">
            <div class="row">
              <div class="col-md-8">
                <h2>{this.props.signal.name}</h2>
              </div>
            </div>
            <div class="clearfix"></div>
          </div>
          <div className="main-content">
            <img id="loading" src={STATIC_URL + "assets/images/Preloader_2.gif"}/>
          </div>
        </div>
      );
    }
  }
}
