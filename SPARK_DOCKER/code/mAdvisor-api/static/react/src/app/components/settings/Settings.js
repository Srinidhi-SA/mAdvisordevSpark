import React from "react";
import {MainHeader} from "../common/MainHeader";

export class Settings extends React.Component {
  constructor() {
    super();
  }
  render() {
    return (
        <div>
          <div className="side-body">
            <MainHeader/>
            <div className="main-content">
              Settings is called!!!!!
            </div>
          </div>
        </div>
      );
  }
}
