import React from "react";
import { connect } from "react-redux";
import {handleTopPredictions} from "../../actions/signalActions";
import renderHTML from 'react-render-html';

@connect((store) => {
    return {
        selectedPrediction:store.signals.selectedPrediction,
    };
})

export class NormalHideColumn extends React.Component {
  constructor(props){
    super(props);
  }
  componentDidMount(){
      if(this.props.selectedPrediction)handleTopPredictions()
  }
  componentDidUpdate(){
      handleTopPredictions()
  }
  generateHeaders(table) {
    var cols = table.tableData.map(function(rowData,i){
      var colLength = rowData.length;
      if(i== 0){
        return rowData.map(function(colData,j) {
          if(j == colLength-1)
            return <th class="hidden">{colData}</th>;
          else 
            return<th key={j}>{colData}</th>;
        });
      }
    })
    return cols;
  }
  generateNormalTableRows(table) {
    var tbodyData = table.tableData.map(function(rowData,i){
      var colLength = rowData.length;
      if(i != 0){
        var rows = rowData.map(function(colData,j) {
          if(j == colLength-1)
            return<td key={j} class="hidden">{colData}</td>; 
          else
            return<td class="cursor" key={j}><span title={colData}>{renderHTML(colData.toString().length > 15 ? colData.toString().slice(0, 15).concat("...") : colData.toString())}</span></td>;
        });
        return<tr key={i}>{rows}</tr>;
      }
    })
    return tbodyData;
  }
 
  render() {
   var data = this.props.tableData;
   var headerComponents = this.generateHeaders(data);
   var rowComponents = this.generateNormalTableRows(data);
   return (
      <div class="table-style_2">
        <h5 className="xs-mt-5"><strong>{this.props.selectedPrediction}: Top Observations</strong></h5>
        <table className="table topPredictions table-bordered">
          <thead><tr>{headerComponents}</tr></thead>
          <tbody>{rowComponents}</tbody>
        </table>
      </div>
    );
  }
}
