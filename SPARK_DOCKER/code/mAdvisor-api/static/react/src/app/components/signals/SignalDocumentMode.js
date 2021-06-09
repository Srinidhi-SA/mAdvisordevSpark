import React from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import store from "../../store";
import {Card} from "./Card";
import {STATIC_URL} from "../../helpers/env.js";
import {getSignalAnalysis} from "../../actions/signalActions";
import {isEmpty,getUserDetailsOrRestart} from "../../helpers/helper";
import {hideDataPreview} from "../../actions/dataActions";

@connect((store) => {
  return {signal: store.signals.signalAnalysis};
})

export class SignalDocumentMode extends React.Component {
  constructor() {
    super();
  }
  componentWillMount() {
    if (isEmpty(this.props.signal)) {
        this.props.dispatch(getSignalAnalysis(getUserDetailsOrRestart.get().userToken, this.props.match.params.slug));
    }
  }

  print() {
    window.print();
  }

  searchTree(_Node, cardLists, lastVar) {
    if(_Node.name!="Prediction" && _Node.listOfCards.length!=0&&_Node.listOfCards[_Node.listOfCards.length - 1].slug == lastVar) {
      cardLists.push(_Node.listOfCards);
      return cardLists;
    } else {
      var i;
      var result = null;
      if(_Node.name==="Prediction" && _Node.listOfCards===undefined){
        for(let i=0;i<Object.keys(_Node).length;i++){
          var clone_Node = JSON.parse(JSON.stringify(_Node));
          if(Object.keys(clone_Node)[i].includes("Depth Of Tree")){
            let node = clone_Node[Object.keys(clone_Node)[i]].listOfCards;
            if(!clone_Node[Object.keys(clone_Node)[i]].listOfCards[0].cardData[0].data.includes("Depth") ){
              clone_Node[Object.keys(clone_Node)[i]].listOfCards[0].cardData[0].data = "<h3 style=text-align:left;padding-bottom:15px>" + Object.keys(clone_Node)[i] + ": "+ /<h3>(.*?)<\/h3>/g.exec(clone_Node[Object.keys(clone_Node)[i]].listOfCards[0].cardData[0].data)[1] + "</h3>"
            }
            clone_Node[Object.keys(clone_Node)[i]].listOfCards[0].cardData.filter(i=>i.dataType==="dropdown")[0]["dropdownName"] = clone_Node[Object.keys(clone_Node)[i]].name
            clone_Node[Object.keys(clone_Node)[i]].listOfCards[0].cardData.filter(i=>i.dataType==="table")[0].data["name"] = clone_Node[Object.keys(clone_Node)[i]].name
            cardLists.push(node);
          }
        }
      }else{
        cardLists.push(_Node.listOfCards);
        for (i = 0; i < _Node.listOfNodes.length; i++) {
          result = this.searchTree(_Node.listOfNodes[i], cardLists, lastVar);
        }
      }
      return result;
    }
  }

  closeDocumentMode(){
    this.props.dispatch(hideDataPreview());
    window.location.pathname = "/signals"
  }
  render() {
    let regression_app=false

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
      if(!regression_app)
      docObj.splice(0, 1);

      let objs = [];
      docObj.map(function(item, i) {
        let len = item.cardData.length;

        for (var i = 0; i < len; i++) {
          objs.push(item.cardData[i]);

        }

      })
      let firstOverviewSlug = this.props.signal.listOfNodes[0].slug;
      let cardModeLink = "/signals/" + this.props.match.params.slug + "/" + firstOverviewSlug;
      if (objs) {
        return (
          <div>
            <div className="side-body" id="side-body">
              <div className="page-head">
              </div>
              <div className="main-content">
                <div className="row">
                  <div className="col-md-12">
					
					<h3 className="xs-mt-0">{this.props.signal.name}
							<div className="btn-toolbar pull-right">
								<div className="btn-group summaryIcons">
								<button type="button" className="btn btn-default" onClick={this.print.bind(this)} title="Print Document"><i className="fa fa-print"></i></button>
								<Link className="btn btn-default continue" to={cardModeLink} title="Card mode">
								<i class="fa fa-columns"></i>
								</Link>
								<button type="button" className="btn btn-default" disabled="true" title="Document Mode">
								<i  style={{fontSize:16}} class="fa fa-file-text-o"></i>
								</button>
								<button type="button" className="btn btn-default" onClick = {this.closeDocumentMode.bind(this)}>
								<i class="fa fa-times"></i>
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