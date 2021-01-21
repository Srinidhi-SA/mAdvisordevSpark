import React from "react";

import {BreadCrumb} from "./BreadCrumb";

export class MainHeader extends React.Component {

  render() {
    return (
      <div className="page-head">
        <div class="row">
          <div class="col-md-12">
            <BreadCrumb/>
          </div>
          <div class="col-md-8">
            <h2>TODO: need to fill this</h2>
          </div>
          </div>
        <div class="clearfix"></div>
      </div>
    );
  };
}
