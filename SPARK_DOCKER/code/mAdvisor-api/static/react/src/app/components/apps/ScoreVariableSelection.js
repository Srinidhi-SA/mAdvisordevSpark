import React from "react";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import store from "../../store";
import {Button,Form,FormGroup} from "react-bootstrap";
import {DataVariableSelection} from "../data/DataVariableSelection";
import {createScore,getAppsModelSummary,getAppDetails} from "../../actions/appActions";
import {AppsLoader} from "../common/AppsLoader";
import {getDataSetPreview,variableSlectionBack,SaveScoreName} from "../../actions/dataActions";
import {statusMessages} from "../../helpers/helper";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    scoreSummaryFlag: store.apps.scoreSummaryFlag
  };
})

export class ScoreVariableSelection extends React.Component {
  constructor(props) {
    super(props);
  }

  createScore(event){
    event.preventDefault();
    let letters = /^[0-9a-zA-Z\d-_\s]+$/;
    if(letters.test(document.getElementById("createScoreName").value) == false){
      bootbox.alert(statusMessages("warning", "Please enter score name in a correct format.It should not contain special characters @,#,$,%,!,&.", "small_mascot"));
      $('#createSname').val("").focus();
      return false;
    }
    this.props.dispatch(createScore($("#createScoreName").val(),$("#createScoreAnalysisList").val()))
  }

  componentWillMount() {
    this.props.dispatch(getAppDetails(this.props.match.params.AppId));
    if(this.props.dataPreview == null){
      this.props.history.replace("/apps/"+this.props.match.params.AppId+"/analyst/models/"+this.props.match.params.modelSlug+"/data/"+this.props.match.params.slug)
      this.props.dispatch(getDataSetPreview(this.props.match.params.slug));
      this.props.dispatch(getAppsModelSummary(this.props.match.params.modelSlug));
    }
  }

  handleBack=()=>{
    this.props.dispatch(variableSlectionBack(true));
    this.props.dispatch(SaveScoreName($("#createScoreName").val()))
    this.props.history.replace(`/apps/${this.props.match.params.AppId}/analyst/models/${this.props.match.params.modelSlug}/data/${this.props.match.params.slug}#?from=variableSelection`);      
  }

  render() {
    if(this.props.scoreSummaryFlag){
      let mod = window.location.pathname.includes("analyst")?"/analyst":"/autoML"
      return(<Redirect to={`/apps/${this.props.match.params.AppId}${mod}/scores/${store.getState().apps.scoreSlug}`}/>);
    }
    let dataPrev = store.getState().datasets.dataPreview;
    let renderSelectBox = null;
    if(dataPrev){
      const metaData =  dataPrev.meta_data.uiMetaData.varibaleSelectionArray;
      if(metaData){
        renderSelectBox =  <select disabled className="form-control" id="createScoreAnalysisList">
          <option key={store.getState().apps.modelTargetVariable} value={store.getState().apps.modelTargetVariable}>{store.getState().apps.modelTargetVariable}</option>
        </select>
      }
    }

    return(
      <div className="side-body">
        <div className="page-head">
          <h3 class="xs-mt-0 text-capitalize">Variable Selection</h3>
          <div className="clearfix"></div>
        </div>
        <div className="main-content">
          <div className="panel panel-default box-shadow">
            <div className="panel-body">
              <Form onSubmit={this.createScore.bind(this)} className="form-horizontal">
                <FormGroup role="form">
                  <label className="col-lg-2 control-label cst-fSize" for="createScoreAnalysisList">I want to analyse</label>
                  <div className="col-lg-4"> {renderSelectBox}</div>
                </FormGroup>
                <FormGroup role="form">
                  <DataVariableSelection match={this.props.match}/>
                </FormGroup>
                <FormGroup role="form">
                  <div className="col-lg-5 col-lg-offset-7">
                    <div class="input-group xs-mb-15">
                      <input type="text" name="createScoreName" required={true} id="createScoreName" defaultValue={store.getState().datasets.varibleSelectionBackFlag?store.getState().datasets.scoreName:""} className="form-control" placeholder="Create Score Name"/>
                      <span class="input-group-btn">
                        <button type="submit" class="btn btn-primary">Score Model</button>
                      </span>
                    </div>
                  </div>
                  <div class="col-md-8">
                    <Button id="ScoreVariableselectionBack"  onClick={this.handleBack}  bsStyle="primary"><i class="fa fa-angle-double-left"></i> Back</Button>
                  </div>
                </FormGroup>
              </Form>
            </div>
          </div>
        </div>
        <AppsLoader match={this.props.match}/>
      </div>
    );
  }
}
