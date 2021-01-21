import React from "react";
import { connect } from "react-redux";
import renderHTML from 'react-render-html';
import {predictionLabelClick} from "../../helpers/helper";

@connect((store) => {
    return { selPrediction: store.signals.selectedPrediction};
  })
  
export class CardHtml extends React.Component {
  constructor(props){
    super(props);
  }
  componentDidMount() {
      predictionLabelClick();
  }
  render() {
   var element = this.props.htmlElement;
   if(this.props.classTag == "highlight"){
       return(
               <div class="row" style={{margin:"20px 0px"}}>
               <div class="bg-highlight-parent xs-ml-50 xs-mr-50">
               <div class="col-md-12 col-xs-12 bg-highlight"> 
                {renderHTML(element)}
                </div>
                <div class="clearfix"></div>
                </div>
                </div>
           );   
   }
   else if(this.props.classTag == "hidden"){
     return(
               <div className="modelSummery hidden">
                {renderHTML(element)}
                </div>
           );
   }
   else if(this.props.classTag === "noTable"){
    return(
      <div className="noTable" style={{marginTop:"15px"}}>
       {renderHTML(element)}
       </div>
  ); 
   }else {
     let txtAlign = "";
     if(this.props.htmlElement === "<h4>Sentiment by Concept</h4>" || 
        this.props.htmlElement === "<h4>Impact on Stock Price</h4>" ||
        this.props.htmlElement.includes("<h4>Influence of Key Features on ")){
       txtAlign = "center";
     }else if(this.props.htmlElement === "<h3>Model Summary</h3>"){
       element = "<h3 class="+"modelTitle"+">Model Summary</h3>"
     }else if(this.props.htmlElement === "<h3>Predicting STATUS based on key attributes</h3> "){
       element = "<h3 class="+"modelTitle"+">Predicting STATUS based on key attributes</h3>"
     }else if(this.props.htmlElement === "<h3>Key Factors that drive STATUS</h3>"){
      element = "<h3 class="+"modelTitle"+">Key Factors that drive STATUS</h3>"
     }
       return(
               <div style={{marginTop:"15px", 
                  display:(this.props.htmlElement === "<h3>Top Entities</h3>")?"none":"", 
                  textAlign:txtAlign
                }}>
                {renderHTML(element)}
                </div>
           );   
   }

  }
}
