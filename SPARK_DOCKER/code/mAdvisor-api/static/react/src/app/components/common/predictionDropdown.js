import React from "react";
import { connect } from "react-redux";
import {showPredictions,handleDecisionTreeTable,handleTopPredictions, showDepthPredictions} from "../../actions/signalActions";

@connect((store) => {
  return { selPrediction: store.signals.selectedPrediction};
})

export class PredictionDropDown extends React.Component {
  constructor(props){
    super(props);
  }
  componentDidUpdate(){
    this.showPredictionsFunc($('#prediction_dropdown').val());
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
    this.showPredictionsFunc(sel);
	}
  checkSelection(e){
    this.showPredictionsFunc(e.target.value);
	  handleDecisionTreeTable();
	  handleTopPredictions();
  }
  showPredictionsFunc(sel){
    this.props.dropdownName !=""?
      this.props.dispatch(showDepthPredictions(sel,this.props.dropdownName.replace(/ +/g, "")))
        :this.props.dispatch(showPredictions(sel));
  }
 
  render() {
    var data = this.props.jsonData;
    var optionsTemp =[];
    for (var prop in data) {
      optionsTemp.push(<option key={prop} className={prop} value={data[prop].name}>{data[prop].displayName}</option>);
    }
 
  return (
    <div>
      <div className="clearfix"></div>
        <div className="row">
          <div className="col-md-6">
            <div className="form-group">
              <label class="control-label pull-left xs-pr-10 xs-pt-5" for="rulesFor">{this.props.label} :</label>
		          <select id="prediction_dropdown" name="selectbasic" class="form-control" onChange={this.checkSelection.bind(this)}>
				        {optionsTemp}
      				</select>
            </div>
          </div>
        </div>
      </div>
    );
  }
}