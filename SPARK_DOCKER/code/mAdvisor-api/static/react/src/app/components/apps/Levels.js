import React from "react";
import { connect } from "react-redux";
import { MultiSelect } from 'primereact/multiselect';
import { Tab, Row, Col } from "react-bootstrap";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    selectedItem: store.datasets.selectedItem,
    featureEngineering: store.datasets.featureEngineering,
    datasets: store.datasets,
  };
})

export class Levels extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = { levelsArray: this.props.levelsData }    
  }

  getAllOptions() {
    let levelOptions = Object.keys(this.props.dataPreview.meta_data.scriptMetaData.columnData.filter(item => item.slug == this.props.selectedItem.slug)[0].columnStats.filter(options => (options.name == "LevelCount"))[0].value)
    levelOptions.sort();
    return levelOptions
  }

  getMultiSelectOptions(idx) {
    var allSelectedItemsExceptCur = this.getAllSelectedOptionsExceptCurrent(idx);
    return this.getAllOptions().filter(item => !allSelectedItemsExceptCur.has(item)).map(function (elem) {
      return { "label": elem, "value": elem };
    });
  }

  getAllSelectedOptionsExceptCurrent(idx) {
    this.getAllOptions();
    var allSelectedItems = new Set();
    this.state.levelsArray.map(function (elem, elemIdx) {
      if (elemIdx != idx) {
        allSelectedItems = new Set([...allSelectedItems, ...elem.multiselectValue])
      }
    });
    var storeValue = this.state.levelsArray.map(i=>i.multiselectValue);
    var reducestoreValue = storeValue.reduce((acc, val) => acc.concat(val), []);
    if(this.getAllOptions().length == reducestoreValue.length){
        $(".addn").addClass("noDisplay");
    }else{
      $(".addn").removeClass("noDisplay");
    }
    return allSelectedItems;
  }

  componentWillMount() {
    this.addNewLevel();  
  }

  componentWillUpdate() {
   this.props.parentUpdateLevelsData(this.state.levelsArray);
  }

  componentDidMount() {
    if((($('ul').last().find('li')).length == 0 ) ){
       $(".form_withrowlabels").last().css("display","none");
    }
    if ($('#dimSEdate').hasClass('wide-modal')) {
      $('.modal-colored-header').addClass('modal-lg-dimSEdate');
    }
    $('.p-multiselect-item label').prop('title', function () { return $(this).text(); });
    
  }

  addNewLevel() {
    var newObj = { "inputValue": "", "multiselectValue": "", "startDate": "", "endDate": "" };
      this.setState({
        levelsArray: this.state.levelsArray.concat([newObj,])
      });
   
  };

  handleRemoveLevel(idx) {
    this.setState({
      levelsArray: this.state.levelsArray.filter((s, sidx) => idx !== sidx)
    });
    this.props.parentUpdateLevelsData(this.state.levelsArray);
  };

  getLevelData() {
    var levelData = {};
    if (this.props.featureEngineering != undefined || this.props.featureEngineering != null) {
      var slugData = this.props.featureEngineering[this.props.selectedItem.slug];
      if (slugData != undefined) {
        levelData = slugData.levelData;
      }
    }
    return levelData;
  }

  inputOnChangeHandler(idx, valueToChange, event) {
    document.getElementById("fileErrorMsg").innerText = ""
    var newArray = this.state.levelsArray;
    newArray[idx][valueToChange] = event.target.value;
    this.setState({
      levelsArray: newArray
    });
  }

  multiSelectOnChangeHandler(idx, event) {
    document.getElementById("fileErrorMsg").innerText = ""
    var newArray = this.state.levelsArray;
    newArray[idx]["multiselectValue"] = event.target.value;
    this.setState({
      levelsArray: newArray
    });
  }

  render() {
    if (this.props.selectedItem.columnType == "dimension") {
      var levelData = this.getLevelData();
      var levels = "";
      levels = (
        <Tab.Pane>
          <div>
            {this.state.levelsArray.map((level, idx) => (
              <div className="form_withrowlabels form-inline" key={idx} >
                <div className="form-group">
                  <label for="txt_lName1">{`${idx + 1}`}&nbsp;&nbsp;&nbsp;</label>
                 <input id={`Level#${idx + 1}`} type="text" value={level.inputValue} name={`name #${idx + 1}`} name="newcolumnname" className="form-control levelrequired" placeholder={`Level #${idx + 1} name`} defaultValue={levelData.inputValue}  onInput={this.inputOnChangeHandler.bind(this, idx, "inputValue")} required/>
               </div>
                <div className="form-group">
                  <label for="txt_sPeriod">&nbsp;&nbsp;&nbsp; Which will include:&nbsp;</label>
                </div>
                <div className="form-group">
                  <div className="content-section implementation multiselect-demo">
                    <MultiSelect value={level.multiselectValue!=""?level.multiselectValue:null} options={this.getMultiSelectOptions(idx)} defaultValue={levelData.multiselectValue} onChange={this.multiSelectOnChangeHandler.bind(this, idx)}
                      style={{ minWidth: '12em' }}  filter={true} placeholder="choose" />
                  </div>
                </div>
                <div className="form-group">
                  &nbsp;<button className="btn btn-grey b-inline" data-levelIndex={idx} onClick={this.handleRemoveLevel.bind(this, idx)} ><i className="fa fa-close"></i></button>
                </div>
              </div>
            ))}
            <button className="btn btn-primary b-inline addn" onClick={this.addNewLevel.bind(this)} ><i className="fa fa-plus"> Add</i></button>
          </div>
        </Tab.Pane>
      )
    }
    else {
      var dtlevels = "";
      var cname = this.props.datasets.dataPreview.meta_data.scriptMetaData.columnData.filter(item => (item.slug == this.props.selectedItem.slug)).map(name => {
        return (<span>{name.name}</span>);
      })
      var startDate = this.props.dataPreview.meta_data.scriptMetaData.columnData.filter(item => item.slug == this.props.selectedItem.slug)[0].columnStats.filter(options => (options.name == "firstDate"))[0].value
      var endDate = this.props.dataPreview.meta_data.scriptMetaData.columnData.filter(item => item.slug == this.props.selectedItem.slug)[0].columnStats.filter(options => (options.name == "lastDate"))[0].value
      dtlevels = (
        <Tab.Pane>
          <p>Please create new levels based on <b> {cname} </b>column by selecting start and end between "<i>{startDate}</i>" and "<i>{endDate}</i>". </p>
          <div id="dimSEdate" className="wide-modal">
            {this.state.levelsArray.map((level, idx) => (
              <div className="form_withrowlabels form-inline" key={idx} >
                <div className="form-group">
                  <label for="txt_lName1">{`${idx + 1}`}&nbsp;&nbsp;&nbsp;</label>
                  <input type="text" id="txt_lName1" value={level.inputValue} name="inputVal" defaultValue={level.newcolumnname} className="form-control" placeholder={`Level #${idx + 1} name`} onInput={this.inputOnChangeHandler.bind(this, idx, "inputValue")} />&nbsp;&nbsp;&nbsp;
                </div> 
                <div class="form-group">
                  <label for="txt_sPeriod1">&nbsp;&nbsp;&nbsp; Start period:</label>
                  <input type="date" id="txt_sPeriod1" value={level.startDate} min={startDate} max={endDate} defaultValue={startDate} className="form-control" onInput={this.inputOnChangeHandler.bind(this, idx, "startDate")} />
                </div>
                <div class="form-group">
                  <label for="txt_ePeriod1">&nbsp;&nbsp;&nbsp; End period:</label>
                  <input type="date" id="txt_ePeriod1" value={level.endDate} min={startDate} max={endDate} defaultValue={endDate} className="form-control" onInput={this.inputOnChangeHandler.bind(this, idx, "endDate")} />
                </div>
                <div className="form-group">
                  &nbsp;<button className="btn btn-grey b-inline" data-levelIndex={idx} onClick={this.handleRemoveLevel.bind(this, idx)} ><i className="fa fa-close"></i></button>
                </div>
              </div>
            ))}
            <button className="btn btn-primary b-inline addn" onClick={this.addNewLevel.bind(this)} ><i className="fa fa-plus"> Add</i></button>
          </div>
        </Tab.Pane>
      )
    }

    return (
      <div className="binsLevelsHeight">
        <Tab.Container id="left-tabs-example">
          <Row className="clearfix">
            <Col sm={15}>
              <Tab.Content animation>{(this.props.selectedItem.columnType == "dimension") ? levels : dtlevels}</Tab.Content>
            </Col>
          </Row>
        </Tab.Container>
      </div>
    );
  }
}