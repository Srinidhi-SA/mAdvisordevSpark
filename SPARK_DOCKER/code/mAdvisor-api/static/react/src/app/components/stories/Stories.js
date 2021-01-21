import React from "react";
import {MainHeader} from "../common/MainHeader";

export class Stories extends React.Component {
  constructor() {
    super();
  }
  render() {
    return (
        <div>
          <div className="side-body">
            <MainHeader/>
            <div className="main-content">
              Stories is called!!!!!
            </div>
          </div>
        </div>
      );
  }
}
