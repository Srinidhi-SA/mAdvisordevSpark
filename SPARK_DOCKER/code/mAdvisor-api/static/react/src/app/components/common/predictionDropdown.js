import React from "react";
import { connect } from "react-redux";
import {showPredictions,handleDecisionTreeTable,handleTopPredictions} from "../../actions/signalActions";

@connect((store) => {
  return { selPrediction: store.signals.selectedPrediction};
})

export class PredictionDropDown extends React.Component {
  constructor(props){
    super(props);
  }
   componentDidUpdate(){
      var sel =$('#prediction_dropdown').val();
			this.props.dispatch(showPredictions(sel));
   }
	componentWillMount(){
		var sel= null;
	  var data = this.props.jsonData;
	  for (var prop in data) {
	      if(data[prop].selected){
	          sel= data[0].name;
	          break;
	      }
	  }
	  this.props.dispatch(showPredictions(sel));
	}
 checkSelection(e){
	  var sel =$('#prediction_dropdown').val();
	 this.props.dispatch(showPredictions(sel));
	 handleDecisionTreeTable();
	 handleTopPredictions();
 }
 
  render() {
   var data = this.props.jsonData;
   var optionsTemp =[], desc=""; 
   for (var prop in data) {
        optionsTemp.push(<option key={prop} className={prop} value={data[prop].name}>{data[prop].displayName}</option>);
    }
	
   return (
          <div> <div className="clearfix"></div>
           <div className="row">
           <div className="col-md-6">
           <div className="form-group">
           <label class="control-label pull-left xs-pr-10 xs-pt-5" for="rulesFor">{this.props.label} :</label>
		    <select id="prediction_dropdown" name="selectbasic" class="form-control" onChange={this.checkSelection.bind(this)}>
				{optionsTemp}
				</select>
		   </div></div>
		   </div></div>
       );
  }
}
