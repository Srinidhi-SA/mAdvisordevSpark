import React from "react";
import {connect} from "react-redux";
import {Button} from "react-bootstrap";
import {getRegressionAppAlgorithmData,updateAlgorithmData,checkAtleastOneSelected,saveParameterTuning,parameterTuningVisited,saveRegressionAppAlgorithmData} from "../../actions/appActions";
import {AppsLoader} from "../common/AppsLoader";
import {STATIC_URL} from "../../helpers/env.js";
import {statusMessages} from "../../helpers/helper";

@connect((store) => {
    return {
        manualAlgorithmData:store.apps.regression_algorithm_data_manual,
        apps_regression_modelName:store.apps.apps_regression_modelName,
        currentAppDetails:store.apps.currentAppDetails,
        parameterTuningFlag:store.apps.parameterTuningFlag,
        modelEditconfig:store.datasets.modelEditconfig,
        editmodelFlag:store.datasets.editmodelFlag,
    };
})

export class AlgorithmSelection extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showParameterTuning:false
        };
    }
    componentWillMount() {
        if(this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null){
            let mod =  window.location.pathname.includes("analyst")?"analyst":"autoML"
            this.props.history.replace("/apps/"+this.props.match.params.AppId+"/"+mod+"/models/data/"+this.props.match.params.slug)
        }else if(this.props.editmodelFlag){
          this.props.dispatch(saveRegressionAppAlgorithmData(this.props.modelEditconfig.config.config))
        }else if(!this.props.parameterTuningFlag)
            this.props.dispatch(getRegressionAppAlgorithmData(this.props.match.params.slug,this.props.currentAppDetails.app_type));
    }
    componentDidMount() {
        $("#manualBlock_111").addClass("dispnone");
        $("#automaticBlock_111").removeClass("dispnone");
    }

    createModel(event){
        event.preventDefault();
        this.props.dispatch(parameterTuningVisited(true))
        let isSelected = checkAtleastOneSelected();
        if(isSelected == false){
            let msg= statusMessages("warning","Please select at least one algorithm that you want to use for prediction.","small_mascot");
            bootbox.alert(msg);
            return false;
        }
        this.props.dispatch(saveParameterTuning());
        var proccedUrl = this.props.match.url.replace('algorithmSelection', 'parameterTuning');
        this.props.history.push(proccedUrl);
    }

    changeAlgorithmSelection(data){
        this.props.dispatch(updateAlgorithmData(data.algorithmSlug));
    }
  
    handleBack=()=>{
        const appId = this.props.match.params.AppId;
        const slug = this.props.match.params.slug;
        this.props.history.replace(`/apps/${appId}/analyst/models/data/${slug}/createModel/featureEngineering?from=algorithm_selection`);
    }

    render() {
        var algorithmData = this.props.manualAlgorithmData;
        var algoClass = "col-md-3";
        if (!$.isEmptyObject(algorithmData)){
            var pageData = "";
            pageData = algorithmData.map((data,Index) =>{
                var checkboxId = "check"+Index;
                return(                       
                    <div key={Index} className= {algoClass}>
                        <div className="bg-highlight-parent xs-mb-10 cst-panel-shadow">
                            <div className="checkbox">
                                <div className="ma-checkbox">
                                    <input type="checkbox" checked={data.selected} id={checkboxId} onChange={this.changeAlgorithmSelection.bind(this,data)}/><label for={checkboxId}> {data.algorithmName}</label>
                                </div>							
                                <div className="xs-mt-5"><p>{data.description}</p></div>
                            </div>
                        </div>
                    </div>
                );
            });
            return(
                <div className="side-body">
                    <div className="page-head">
                        <h3 class="xs-mt-0 text-capitalize">{"Algorithm Selection"}</h3>
                    </div>
                    <div className="main-content">
                        <div className="panel panel-mAd xs-p-20 box-shadow">                               
                            <div className="panel-heading xs-ml-0 xs-mb-10">
                                Please use the following learning algorithms for prediction
                            </div>
                            <div className="panel-body no-border">
                                <div className="row algSelection xs-mb-20">
                                    {pageData}
                                </div>
                            </div>
                            <div className="clearfix"></div>
                            <Button onClick={this.handleBack} bsStyle="primary"><i class="fa fa-angle-double-left"></i> Back</Button>
                            <Button id="algoSelectionProceed" type="button" bsStyle="primary xs-pl-20 xs-pr-20" style={{float:'right'}} onClick={this.createModel.bind(this)}>{"Proceed"} <i class="fa fa-angle-double-right"></i></Button>
                            <div className="clearfix"></div>
                        </div>
                    </div>
                    <AppsLoader match={this.props.match}/>
                </div>
            );
        }else{
            return (
                <div className="side-body">
                    <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
                </div>
            );
        }
    }
}