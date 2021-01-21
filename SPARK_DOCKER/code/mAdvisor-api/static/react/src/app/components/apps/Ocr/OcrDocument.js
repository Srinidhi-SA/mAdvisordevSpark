import React from "react";
import { connect } from "react-redux";
import { OcrTable } from "./OcrTable";
import { OcrImage } from "./ocrImage";
import {RevDocTable} from './RevDocTable';
@connect((store) => {
  return {
    imageFlag: store.ocr.imageFlag,
    revDocumentFlag:store.ocr.revDocumentFlag,
  };
})

export class OcrDocument extends React.Component {
  constructor(props) {
    super(props);
  }
 
  render() {    
    return (
      <div>
      {this.props.imageFlag ?<OcrImage/> :(this.props.revDocumentFlag?<RevDocTable/>:<OcrTable/>)}
    </div>
    );
  }
}

