import React from "react";
import {generateHeaders,generateNormalTableRows} from "../../helpers/helper";
import { Scrollbars } from 'react-custom-scrollbars';

export class NormalTable extends React.Component {
  constructor(){
    super();
  }
  render() {
   var data = this.props.tableData;
   var className = "table table-bordered  table-condensed table-striped break-if-longText"
   var headerComponents = generateHeaders(data);
   var rowComponents = generateNormalTableRows(data);
   return (
      <div className="table-style" style={{marginBottom:"40px", marginTop:(this.props.tableData.topHeader === "Model Comparison" || this.props.tableData.topHeader === "Distribution of Predicted Values")?"40px":null}}>
        <Scrollbars autoHeight autoHeightMax={400}>
          <table className={className}>
            <thead><tr>{headerComponents}</tr></thead>
            <tbody>{rowComponents}</tbody>
          </table>
        </Scrollbars>
      </div>
    );
  }
}
