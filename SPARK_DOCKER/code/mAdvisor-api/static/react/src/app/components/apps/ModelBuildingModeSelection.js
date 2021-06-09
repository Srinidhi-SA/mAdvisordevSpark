import React from "react";
import {connect} from "react-redux";
import store from "../../store"
import {getAppDetails} from "../../actions/appActions";
import {STATIC_URL} from "../../helpers/env.js";
import {clearDataPreview} from "../../actions/dataUploadActions"
import Link from "react-router-dom/Link";

@connect((store) => {
  return {
    currentAppDetails: store.apps.currentAppDetails,
  };
})

export class ModelBuildingModeSelection extends React.Component {
  componentWillMount() {
    this.props.dispatch(clearDataPreview());
    if(store.getState().apps.currentAppDetails===null){
      this.props.dispatch(getAppDetails(this.props.match.params.AppId))
    }
  }

  render() {
    let autoLink = ""
    let analystLink = ""
    if(store.getState().apps.currentAppDetails!=null || store.getState().apps.currentAppDetails!=undefined){
      autoLink = "/apps/"+store.getState().apps.currentAppDetails.slug+"/autoML/models"
      analystLink = "/apps/"+store.getState().apps.currentAppDetails.slug+"/analyst/models"
    }
    return (
      <div className="side-body">
        <div class="page-head">
			    <h3 class="xs-mt-0 xs-mb-0 text-capitalize"> Please choose the modeling process.</h3>
			  </div>
			  <div className="row mod-processs">
          <div className="col-md-4 col-md-offset-2">
            <div className="mod-process mod-process-table-primary">
              <div className="mod-process-title">For business users</div>
              <div className="mod-process-table-img">
                <img src={ STATIC_URL + "assets/images/mProcess_autoMlmode.png" } className="img-responsive" />
              </div>
              <p className="mProcess">
                Automatic ML modeling process that executes recommended set of data cleansing and transformation operations.
              </p>
              <Link className="btn btn-primary pull-right" to={autoLink} id="auto">
                AUTO ML MODE
              </Link>
            </div>
          </div>
          <div className="col-md-4">
            <div className="mod-process mod-process-table-primary">
              <div className="mod-process-title">For analysts and data scientists</div>
              <div className="mod-process-table-img">
                <img src={ STATIC_URL + "assets/images/mProcess_automode.png" } className="img-responsive" />
              </div>
              <p className="mProcess">Robust set of data cleansing and feature transformation and generation options are provided.<br/></p>
              <Link className="btn btn-primary pull-right" to={analystLink} id="analyst">
                ANALYST MODE
              </Link>
            </div>
          </div>
        </div>
			</div>
    )
  }
}
