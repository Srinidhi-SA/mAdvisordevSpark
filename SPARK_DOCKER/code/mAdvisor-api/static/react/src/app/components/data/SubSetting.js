import React from "react";
import {connect} from "react-redux";
import ReactBootstrapSlider from 'react-bootstrap-slider'
import store from "../../store";
import {clearSubset, selDatetimeCol, selDimensionCol, selectAllDimValues, selectDimValues, selMeasureCol, setAlreadyUpdated, setDatetimeColValues, setDimensionColValues, setMeasureColValues, updateSubSetting} from "../../actions/dataActions";
import {decimalPlaces} from "../../helpers/helper.js"
import {Scrollbars} from 'react-custom-scrollbars';
import DatePicker from 'react-bootstrap-date-picker';

@connect((store) => {
  return {
    updatedSubSetting: store.datasets.updatedSubSetting,
    subsettingDone: store.datasets.subsettingDone,
    alreadyUpdated: store.datasets.alreadyUpdated,
    measureColSelected: store.datasets.measureColSelected,
    dimensionColSelected:store.datasets.dimensionColSelected,
    datetimeColSelected:store.datasets.datetimeColSelected,
  };
})

export class SubSetting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      subSettingRs: this.props.updatedSubSetting,
    };
  }

  componentWillMount(){
    this.props.dispatch(setAlreadyUpdated(false));
    let colData = this.props.item;
    if(colData.columnType === "measure"){
      colData.columnStats.map((stats) => {
        if(stats.name == "min"){
          this.props.dispatch(setMeasureColValues("min",stats.value));
          this.props.dispatch(setMeasureColValues("curMin",stats.value));
        }else if(stats.name == "max"){
          this.props.dispatch(setMeasureColValues("max",stats.value));
          this.props.dispatch(setMeasureColValues("curMax",stats.value));
        }
      });
      this.props.dispatch(setMeasureColValues("textboxUpdated",false));
      if(this.props.updatedSubSetting.measureColumnFilters.length>0 && this.props.updatedSubSetting.measureColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selMeasureCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }else if(colData.columnType === "dimension"){
      colData.columnStats.map((stats) => {
        if(stats.name == "LevelCount"){
          this.props.dispatch(setDimensionColValues("dimensionList",stats.value))
          this.props.dispatch(setDimensionColValues("curDimensionList",Object.keys(stats.value)))
          this.props.dispatch(setDimensionColValues("selectedDimensionList",Object.keys(stats.value)))
        }
      });
      if(this.props.updatedSubSetting.dimensionColumnFilters.length>0 && this.props.updatedSubSetting.dimensionColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selDimensionCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }else if(colData.columnType === "datetime"){
      colData.columnStats.map((stats) => {
        if(stats.name === "firstDate"){
          this.props.dispatch(setDatetimeColValues("startDate",stats.value));
          this.props.dispatch(setDatetimeColValues("curstartDate",stats.value));
        }else if(stats.name == "lastDate"){
          this.props.dispatch(setDatetimeColValues("endDate",stats.value));
          this.props.dispatch(setDatetimeColValues("curendDate",stats.value)); 
        }
      });
      if(this.props.updatedSubSetting.timeDimensionColumnFilters.length>0 && this.props.updatedSubSetting.timeDimensionColumnFilters.filter(i=>i.colname===colData.name).length>0){
        this.props.dispatch(selDatetimeCol(colData.name));
        this.props.dispatch(setAlreadyUpdated(true));
      }
    }
  }
  componentDidMount() {
    $(".bslider").slider();
    $('#saveButton').attr('disabled', true);
  }
  changeSliderValue(e) {
    this.props.dispatch(setMeasureColValues("curMin",e.target.value[0]));
    $("#from_value").val(this.props.measureColSelected.curMin);
    this.props.dispatch(setMeasureColValues("curMax",e.target.value[1]));
    $("#to_value").val(this.props.measureColSelected.curMax);
      $("#saveButton").removeClass('btn-alt4')
      $("#saveButton").addClass('btn-primary')
      $("#saveButton").removeAttr('disabled') 
  }
  changeSliderValueFromText(flg,e) {
    if(isNaN(Number(e.target.value))){
      alert("please enter a valid number")
    }else if(flg==="from"){
      this.props.dispatch(setMeasureColValues("curMin",Number(e.target.value)));
      this.props.dispatch(setMeasureColValues("textboxUpdated",true));
      this.forceUpdateHandler();
      $("#saveButton").removeClass('btn-alt4')
      $("#saveButton").addClass('btn-primary')
      $("#saveButton").removeAttr('disabled')
    }else if(flg==="to"){
      this.props.dispatch(setMeasureColValues("curMax",Number(e.target.value)));
      this.props.dispatch(setMeasureColValues("textboxUpdated",true));
      this.forceUpdateHandler();
      $("#saveButton").removeClass('btn-alt4')
      $("#saveButton").addClass('btn-primary')
      $("#saveButton").removeAttr('disabled')
    }
  }
  handleSelectAll(e){
    let items = document.getElementsByClassName("dimension");
    for(let i=0;i<items.length;i++){
      if(e.target.checked){
        items[i].checked=true
      }else{
        items[i].checked=false
      }
    }
    if(e.target.checked){
      this.props.dispatch(selectAllDimValues(true));
    }else{
      this.props.dispatch(selectAllDimValues(false));
    }
    $("#saveButton").removeClass('btn-alt4')
    $("#saveButton").addClass('btn-primary')
    $("#saveButton").removeAttr('disabled')
  }
  handleSelect(e){
    let items = document.getElementsByClassName("dimension");
    for(let i=0;i<items.length;i++){
      if(items[i].value === e.target.value){
        if(e.target.checked){
          items[i].checked=true
        }else
          items[i].checked=false
      }
    }
    if(e.target.checked){
      this.props.dispatch(selectDimValues(e.target.value,true))
    }else{
      this.props.dispatch(selectDimValues(e.target.value,false))
    }
    if(Object.keys(this.props.dimensionColSelected.dimensionList).length === this.props.dimensionColSelected.selectedDimensionList.length){
      document.getElementById("dim").checked = true
    }else{
      document.getElementById("dim").checked = false
    }
    $("#saveButton").removeClass('btn-alt4')
    $("#saveButton").addClass('btn-primary')
    $("#saveButton").removeAttr('disabled')
  }
  handleStartDateChange(formattedValue){
    this.props.dispatch(setDatetimeColValues("curstartDate",formattedValue));
    $("#saveButton").removeClass('btn-alt4')
    $("#saveButton").addClass('btn-primary')
    $("#saveButton").removeAttr('disabled')
  }
  handleEndDateChange(formattedValue){
    this.props.dispatch(setDatetimeColValues("curendDate",formattedValue));
    $("#saveButton").removeClass('btn-alt4')
    $("#saveButton").addClass('btn-primary')
    $("#saveButton").removeAttr('disabled')
  }
  forceUpdateHandler(){
    this.forceUpdate();
  }
  saveSubSetting(){
    switch(this.props.item.columnType){
      case "measure":{
        if(this.props.alreadyUpdated === true){
        let measureColumnFilter = this.props.updatedSubSetting.measureColumnFilters
          this.props.updatedSubSetting.measureColumnFilters.map((changeditem, i) => {
            if(changeditem.colname == this.props.item.name){
              measureColumnFilter[i] = {
                "colname": this.props.item.name,
                "upperBound": Number(this.props.measureColSelected.curMax),
                "lowerBound": Number(this.props.measureColSelected.curMin),
                "filterType": "valueRange"
              };
            }
          });
          this.state.subSettingRs.measureColumnFilters = measureColumnFilter;
        }else{
          this.state.subSettingRs.measureColumnFilters.push({
            "colname":this.props.item.name,
            "lowerBound":this.props.measureColSelected.curMin,
            "upperBound":this.props.measureColSelected.curMax,
            "filterType": "valueRange"
          });
          this.props.dispatch(setAlreadyUpdated(true))
        }
      }
      break;
      case "dimension":{
        let dimensionColumnFilter = this.props.updatedSubSetting.dimensionColumnFilters
        if(this.props.alreadyUpdated === true){
          this.props.updatedSubSetting.dimensionColumnFilters.map((changeditem, i) => {
            if(changeditem.colname == this.props.item.name){
              dimensionColumnFilter[i] = {
                "colname": this.props.item.name,
                "values": this.props.dimensionColSelected.selectedDimensionList,
                "filterType": "valueIn"
              };
            }
          });
          this.state.subSettingRs.dimensionColumnFilters = dimensionColumnFilter;
        }else{
          this.state.subSettingRs.dimensionColumnFilters.push({
            "colname": this.props.item.name,
            "values": this.props.dimensionColSelected.selectedDimensionList,
            "filterType": "valueIn"
          });
        this.props.dispatch(setAlreadyUpdated(true))
        this.props.dispatch(selDimensionCol(this.props.item.name));
        }
      }
      break;
      case "datetime":{
        let timeDimensionColumnFilters = this.props.updatedSubSetting.timeDimensionColumnFilters
        if(this.props.alreadyUpdated == true){
          this.props.updatedSubSetting.timeDimensionColumnFilters.map((changeditem, i) => {
            if (changeditem.colname == this.props.item.name) {
              timeDimensionColumnFilters[i] = {
                "colname": this.props.item.name,
                "upperBound": this.props.datetimeColSelected.curendDate,
                "lowerBound": this.props.datetimeColSelected.curstartDate,
                "filterType": "valueRange"
              };
            }
          });
          this.state.subSettingRs.timeDimensionColumnFilters = timeDimensionColumnFilters;
        }else{
          this.state.subSettingRs.timeDimensionColumnFilters.push({
            "colname": this.props.item.name,
            "upperBound": this.props.datetimeColSelected.curendDate,
            "lowerBound": this.props.datetimeColSelected.curstartDate,
            "filterType": "valueRange"
          });
          this.props.dispatch(setAlreadyUpdated(true))
        }
      }
      break;
    }
    if(this.props.item.columnType == "measure"){
      if ((this.props.measureColSelected.curMin < this.props.measureColSelected.min) || (this.props.measureColSelected.curMin > this.props.measureColSelected.max)) {
        bootbox.alert("Please select a range between " + this.props.measureColSelected.min + " and " + this.props.measureColSelected.max)
        $("#saveButton").removeClass('btn-alt4')
        $("#saveButton").addClass('btn-primary')
        $("#saveButton").removeAttr('disabled')
      }else if((this.props.measureColSelected.curMax <= this.props.measureColSelected.curMin) || (this.props.measureColSelected.curMax > this.props.measureColSelected.max)){
        bootbox.alert("Please select a range between " + this.props.measureColSelected.min + " and " + this.props.measureColSelected.max)
        $("#saveButton").removeClass('btn-alt4')
        $("#saveButton").addClass('btn-primary')
        $("#saveButton").removeAttr('disabled')
      }else{
        $('#saveButton').removeClass('btn-primary')
        $('#saveButton').addClass('btn-alt4')
        $('#saveButton').attr('disabled', true);
        this.props.dispatch(updateSubSetting(this.state.subSettingRs));
      }
    }
    else if(this.props.item.columnType == "datetime"){
      if( Date.parse(this.props.datetimeColSelected.curstartDate) < Date.parse(this.props.datetimeColSelected.startDate) || Date.parse(this.props.datetimeColSelected.curstartDate) > Date.parse(this.props.datetimeColSelected.endDate) ){
        bootbox.alert("Please select a range between " + this.props.datetimeColSelected.startDate + " and " + this.props.datetimeColSelected.endDate)
        $("#saveButton").removeClass('btn-alt4')
        $("#saveButton").addClass('btn-primary')
        $("#saveButton").removeAttr('disabled')
      }
      else if(Date.parse(this.props.datetimeColSelected.curendDate) < Date.parse(this.props.datetimeColSelected.curstartDate) || Date.parse(this.props.datetimeColSelected.curendDate) > Date.parse(this.props.datetimeColSelected.endDate)){
        bootbox.alert("Please select a range between " + this.props.datetimeColSelected.startDate + " and " + this.props.datetimeColSelected.endDate)
        $("#saveButton").removeClass('btn-alt4')
        $("#saveButton").addClass('btn-primary')
        $("#saveButton").removeAttr('disabled')
      }
      else{
        $('#saveButton').removeClass('btn-primary')
        $('#saveButton').addClass('btn-alt4')
        $('#saveButton').attr('disabled', true);
        this.props.dispatch(updateSubSetting(this.state.subSettingRs));
      }
    }
    else if(this.props.item.columnType == "dimension"){
      $('#saveButton').removeClass('btn-primary')
      $('#saveButton').addClass('btn-alt4')
      $('#saveButton').attr('disabled', true);
      this.props.dispatch(updateSubSetting(this.state.subSettingRs));
    }
  }

  getSubSettings(columnType){
    switch(columnType){
      case "measure":{
        let precision = decimalPlaces(this.props.measureColSelected.curMax)
        let step = (1/Math.pow(10, precision));
        let value = [Number(store.getState().datasets.measureColSelected.curMin), Number(store.getState().datasets.measureColSelected.curMax)]
        if(this.props.measureColSelected.curMin === undefined){
          value=[0,Number(store.getState().datasets.measureColSelected.curMax)]
        }else if(this.props.measureColSelected.curMax === undefined) {
          value=[Number(store.getState().datasets.measureColSelected.curMin),0]
        }
        return(
          <div>
            <div id="measure_subsetting">
              <h5 className="xs-pt-5">{this.props.item.name}</h5>
              <div className="xs-pt-20"></div>
              <div className="row">
                <div className="col-xs-5">
                  <input key={Math.random()} type="number" step={step} min={parseFloat(this.props.measureColSelected.min)} max={parseFloat(this.props.measureColSelected.curMax)} className="form-control" id="from_value" defaultValue={Number(store.getState().datasets.measureColSelected.curMin)} onChange={this.changeSliderValueFromText.bind(this,"from")}/>
                </div>
                <div className="col-xs-2 text-center">
                  <label>To</label>
                </div>
                <div className="col-xs-5">
                  <input key={Math.random()} type="number" step={step} min={parseFloat(this.props.measureColSelected.curMin)} max={parseFloat(this.props.measureColSelected.max)} className="form-control" id="to_value" defaultValue={Number(store.getState().datasets.measureColSelected.curMax)} onChange={this.changeSliderValueFromText.bind(this,"to")}/>
                </div>
                <div className="clearfix"></div>
              </div>
              </div>
              <div className="xs-p-20"></div>
              <div className="form-group text-center">
                <ReactBootstrapSlider className="slider" value={[Number(store.getState().datasets.measureColSelected.curMin), Number(store.getState().datasets.measureColSelected.curMax)]}
                 triggerSlideEvent="true" change={this.changeSliderValue.bind(this)} step={step} max={parseFloat(store.getState().datasets.measureColSelected.max)} min={parseFloat(store.getState().datasets.measureColSelected.min)} range="true" tooltip="hide"/>
              </div>
            </div>
          );
        }
        break;
      case "dimension":{
        if(this.props.item.dateSuggestionFlag == false){
          let dimList = this.props.dimensionColSelected.dimensionList
          let curDim = this.props.dimensionColSelected.curDimensionList
          let dimTemplate = ""
          if(dimList){
            dimTemplate = Object.keys(dimList).map((item, i) => {
              const dId = "chk_mes1_" + i;
              return(
                <tr key={i}>
                  <td>
                    <div className="ma-checkbox inline">
                      <input key={Math.random()} id={"chk_mes1_" + i} type="checkbox" className="dimension" value={item} defaultChecked={(curDim.indexOf(item)>-1)?true:false} onClick={this.handleSelect.bind(this)} />
                      <label htmlFor={"chk_mes1_" + i}></label>
                    </div>
                  </td>
                  <td>{item}</td>
                  <td className="pts">{dimList[item]}</td>
                </tr>
              )
            });
          }
          return(
            <div>
              <div id="dimention_subsetting">
                <h5 className="xs-pt-5">{this.props.item.name}</h5>
                <div class="table-responsive">
                  <Scrollbars style={{ height: 170 }} 
                  renderTrackHorizontal={props => <div {...props} className="track-horizontal" style={{display:"none"}}/>}
                  renderThumbHorizontal={props => <div {...props} className="thumb-horizontal" style={{display:"none"}}/>}>
                    <table id="subset" className="tablesorter table table-condensed table-hover table-bordered">
                      <thead>
                        <tr>
                        <th>
                          <div class="ma-checkbox inline">
                            <input key={Math.random()} id="dim" type="checkbox" className="dimention" defaultChecked={(curDim.length == Object.keys(dimList).length)?true:false} onClick={this.handleSelectAll.bind(this)} />
                            <label htmlFor="dim"></label>
                          </div>
                          </th>
                          <th className="tb_srtColumn"><b title={this.props.item.name}>{this.props.item.name}</b></th>
                          <th><b>Count</b></th>
                        </tr>
                      </thead>
                      <tbody>
                        {dimTemplate}
                      </tbody>
                    </table>
                  </Scrollbars>
                </div>
              </div>
            </div>
          );
        }else{
          return (<div id="dimention_subsetting"/>);
        }
      }
      break;
      case "datetime":{
        return (
          <div>
            <div id="date_subsetting">
              <h5>From</h5>
              <div className="row">
                <div className="col-xs-12">
                  <DatePicker key={this.props.datetimeColSelected.startDate} minDate={this.props.datetimeColSelected.startDate} maxDate={this.props.datetimeColSelected.curendDate} id="start-datepicker" className="form-control" value={this.props.datetimeColSelected.curstartDate} onChange={this.handleStartDateChange.bind(this)} showClearButton={false} dateFormat="YYYY-MM-DD"/>
                </div>
              </div>
              <div className="clearfix"></div>
              <div className="xs-p-20"></div>
              <h5>To</h5>
              <div className="row">
                <div className="col-xs-12">
                  <DatePicker key={this.props.datetimeColSelected.endDate} minDate={this.props.datetimeColSelected.curstartDate} maxDate={this.props.datetimeColSelected.endDate} id="end-datepicker" className="form-control" value={this.props.datetimeColSelected.curendDate} onChange={this.handleEndDateChange.bind(this)} showClearButton={false} dateFormat="YYYY-MM-DD"/>
                </div>
              </div>
              <div className="clearfix"></div>
            </div>
          </div>
        );
      }
      break;
    }
  }
  
  render() {
    return (
      <div id="tab_subsettings" className="panel-group accordion accordion-semi">
        <div className="panel panel-default box-shadow">
          <div className="panel-heading">
            <h4 className="panel-title">
              <a data-toggle="collapse" data-parent="#tab_subsettings" href="#pnl_tbset" aria-expanded="true" className="">Sub Setting
                <i className="fa fa-angle-down pull-right"></i>
              </a>
            </h4>
          </div>
          <div id="pnl_tbset" className="panel-collapse collapse in" aria-expanded="true">
            <div className="xs-pt-5 xs-pr-10 xs-pb-5 xs-pl-10">
              {this.getSubSettings(this.props.item.columnType)}
            </div>
            <div class="panel-footer">
              <div class="text-right" id="saveSubSetting">
                <button href="javascript:void(0)" class="btn btn-alt4" id="saveButton" onClick={this.saveSubSetting.bind(this)}>
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
  componentWillUnmount(){
    this.props.dispatch(clearSubset())
  }
}