import React from "react";
import { NavLink } from "react-router-dom";
import { getUserDetailsOrRestart } from "../../../helpers/helper";
import { saveDocumentPageFlag,selectedReviewerDetails } from '../../../actions/ocrActions';
import { API } from "../../../helpers/env";
import { dashboardMetrics } from '../../../actions/ocrActions';
import { connect } from "react-redux";

@connect((store) => {
  return {
    dashboardMetrics: store.ocr.dashboardMetrics,
  };
})

export class OcrTopNavigation extends React.Component {
  constructor(props) {
    super(props);
    this.getITEDashboardMetrics();
  }

  handleRoute(){ //Making docFlag false on click of navLink,to load project & reviewer table,Without this proDoc table is getting loaded
  this.props.dispatch(saveDocumentPageFlag(false)) 
  this.props.dispatch(selectedReviewerDetails('',''))
  this.props.dispatch(selectedProjectDetails('',''))


  }
  getHeader = (token) => {
    return {
      'Authorization': token,
      'Content-Type': 'application/json',
    }
  }

  getITEDashboardMetrics=()=>{
      return fetch(API + '/ocr/get_dashboard_metrics/', {
        method: 'get',
        headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
      }).then(response => response.json())
      .then(data=>{
        if(data != ""){
          this.props.dispatch(dashboardMetrics(data));
        }
      })

}

  render() {
    let reviewTab = getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole ==  "Superuser" ? "Reviewers" : "Projects";
    return (
        <div className="page-head">
          <div className="row">
            <div className="col-md-4">
              <h3 className="nText xs-mt-0">Intelligent Text Extractor</h3>
            </div>
            <div className="col-md-8">
              <ul className="nav nav-tabs cst_ocr_tabs pull-right">
                <li>
                  <NavLink exact={true} to="/apps/ocr-mq44ewz7bp/" activeClassName="active" title="Dashboard">
                    <i className="fa fa-tachometer fa-lg"></i> Dashboard
                  </NavLink>
                </li>

                {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole ==  "Superuser") &&
                  <li><NavLink to="/apps/ocr-mq44ewz7bp/project/" onClick={this.handleRoute.bind(this)} activeClassName="active">
                    <i className="fa fa-book fa-lg"></i> Projects
                  </NavLink>
                  </li>
                }
                {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole ==  "Superuser") &&
                  <li><NavLink to="/apps/ocr-mq44ewz7bp/configure/" activeClassName="active">
                    <i className="fa fa-sliders fa-lg"></i> Configure
                    </NavLink>
                  </li>
                }

                <li><NavLink to="/apps/ocr-mq44ewz7bp/reviewer/" onClick={this.handleRoute.bind(this)} activeClassName="active">
                  <i className="fa fa-users fa-lg"></i> {reviewTab}
                    </NavLink>
                </li>
                {(getUserDetailsOrRestart.get().userRole == "Admin" || getUserDetailsOrRestart.get().userRole == "Superuser") &&
                  <li><NavLink to="/apps/ocr-mq44ewz7bp/manageUser/" activeClassName="active">
                    <i className="fa fa-user fa-lg"></i> Users
                    </NavLink>
                  </li>
                }
              </ul>
            </div>
          </div>
        </div>
    );
  }

}
