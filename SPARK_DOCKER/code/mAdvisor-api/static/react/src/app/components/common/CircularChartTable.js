import React from "react";
import {generateHeaders,generateCircularChartRows} from "../../helpers/helper";

export class CircularChartTable extends React.Component {
  constructor(){
    super();
  }
  render() {
   var data = this.props.tableData;
   var headerComponents = generateHeaders(data);
   var rowComponents = generateCircularChartRows(data);
   return (
           <table className="table table_borderless" style={{"width":"100%"}}>
               <thead><tr>{headerComponents}</tr></thead>
               <tbody >{rowComponents}</tbody>
           </table>
       );
  }
}
