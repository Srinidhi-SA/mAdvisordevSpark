import React from "react";
import {generateHeaders,generateRows} from "../../helpers/helper";
import { Scrollbars } from 'react-custom-scrollbars';

export class ConfusionMatrix extends React.Component {
  constructor(){
    super();
  }
  render() {
   var data = this.props.tableData;
   var headerComponents = generateHeaders(data);
   var rowComponents = generateRows(data);
   return (
           <div className="table-style">
		   <Scrollbars style={{ height: 250 }}>
           <table className="table table-bordered apps_table_style">
               <thead><tr>
				<th colSpan={data.tableData.length+3} class="text-center">Actual</th>
				</tr></thead>
               <tbody><tr><th rowSpan={data.tableData.length} class="left_highlilght">Predicted</th>
				{headerComponents}</tr>{rowComponents}</tbody>
           </table>
		   </Scrollbars>
           </div>
       );
  }
}
