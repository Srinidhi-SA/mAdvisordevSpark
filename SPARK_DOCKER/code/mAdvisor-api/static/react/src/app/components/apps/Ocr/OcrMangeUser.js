import React from "react";
import { connect } from "react-redux";
import { OcrUserTable } from "./OcrUserTable";
import { OcrTopNavigation } from "./ocrTopNavigation";
@connect((store) => {
  return { 
    };
})

export class OcrManageUser extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render() {
    return (
    <div className="side-body">
      <OcrTopNavigation/>
      <div className="main-content">
        <section className="ocr_section box-shadow">
          <div className="container-fluid">
            <OcrUserTable/>
          </div>
        </section>
      </div>
    </div>
    );
  }
}
