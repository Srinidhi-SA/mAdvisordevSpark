import React from "react";
import { connect } from "react-redux";
import { Tab, Row, Col } from "react-bootstrap";
import { binningOptionsOnChangeAction } from "../../actions/featureEngineeringActions";
@connect((store) => {
  return {
    selectedItem: store.datasets.selectedItem,
    dataPreview: store.datasets.dataPreview,
    isNoOfBinsEnabled: store.datasets.isNoOfBinsEnabled,
    isSpecifyIntervalsEnabled: store.datasets.isSpecifyIntervalsEnabled,
    featureEngineering: store.datasets.featureEngineering,
    editmodelFlag: store.datasets.editmodelFlag,
    modelEditconfig: store.datasets.modelEditconfig,
  };
})

export class Bins extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillMount() {
    if(this.props.editmodelFlag){
      if(this.props.featureEngineering[this.props.selectedItem.slug]!=undefined && this.props.featureEngineering[this.props.selectedItem.slug].binData.selectBinType == "create_equal_sized_bins"){
        this.props.dispatch(binningOptionsOnChangeAction(false,true));
      }else{
        this.props.dispatch(binningOptionsOnChangeAction(true,false));
      }
    }
  }

  getBindata() {
    if (this.props.featureEngineering != undefined || this.props.featureEngineering != null) {
      var slugData = this.props.featureEngineering[this.props.selectedItem.slug];
      if (slugData != undefined && slugData.binData != undefined) {
        return JSON.parse(JSON.stringify(slugData.binData));
      }
    }
    return {};
  }

  binningOptionsOnChange(event) {
    var selectedValue = event.target.value;
    document.getElementById("fileErrorMsg").innerText = ""
    document.getElementById('numberofbins').value = "";
    document.getElementById('specifyintervals').value = "";
    if (selectedValue == "create_equal_sized_bins") {
      this.props.dispatch(binningOptionsOnChangeAction(false, true));
    }else if (selectedValue == "create_custom_bins") {
      this.props.dispatch(binningOptionsOnChangeAction(true, false));
    }
    this.props.clearBinsAndIntervals(event);
    this.pickValue(event);
  }

  pickValue(event) {
    this.props.parentPickValue("binData", event);
  }

  onchangeInput(event) {
    document.getElementById("fileErrorMsg").innerText = ""
    return event.target.value;
  }

  render() {
    var binData = this.getBindata();
    var binningOptions =  (this.props.dataPreview.meta_data.uiMetaData.fe_config.fe.measure.level_creation_settings.operations.map(item => 
      <option key={item.name} value={item.name}>{item.displayName}</option>))
    return (
      <div>
        <Tab.Container id="left-tabs-example">
          <Row className="clearfix">
            <Col sm={15}>
              <Tab.Content animation>
                <Tab.Pane>
                  <form id="binsForm" className="featureEnggFormLabel">
                      <label for="sel_tobg" >{"Column name"}</label>
                      <input id="colName" type="text" title="Column name " placeholder="Column name" name="name" value={this.props.selectedItem.name} disabled className="form-control" />
                      <label for="sel_tobg" >Type of binning<span className="text-danger">*</span></label>
                      <select className="form-control" id="selectBinType" name="selectBinType" defaultValue={binData.selectBinType} onChange={this.binningOptionsOnChange.bind(this)}> 
                        <option value="">--Select--</option>
                        {binningOptions}
                      </select>
                      <label for="sel_tobg" >{"Number of bins"} <span className="text-danger">*</span></label>
                      <input id="binNo" type="number" min="0" title="Number of bins " placeholder="Number of bins" id="numberofbins" name="numberofbins" defaultValue={binData.numberofbins} disabled={this.props.isNoOfBinsEnabled} onInput={this.pickValue.bind(this)} onChange={this.onchangeInput.bind(this)} className="form-control" />
                      <label for="sel_to bg" >{"Specify intervals"} <span className="text-danger">*</span></label>
                      <input id="SpecifyInt" type="text" title="Specify intervals" placeholder="Specify intervals" id="specifyintervals" name="specifyintervals" defaultValue={binData.specifyintervals} disabled={this.props.isSpecifyIntervalsEnabled} onChange={this.onchangeInput.bind(this)} className="form-control" onInput={this.pickValue.bind(this)} />
                      <label for="sel_tobg" >{"New column name"} <span className="text-danger">*</span></label>
                      <input id="newColName" type="text" title="New column name " placeholder="New column name" name="newcolumnname" defaultValue={binData.newcolumnname} onChange={this.onchangeInput.bind(this)} className="form-control" onInput={this.pickValue.bind(this)} />
                    </form>
                </Tab.Pane>
              </Tab.Content>
            </Col>
          </Row>
        </Tab.Container>
      </div>
    );
  }
}