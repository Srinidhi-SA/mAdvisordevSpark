import React from "react";
import { connect } from "react-redux";
import { Button, Modal } from "react-bootstrap";
import {
  openBinsOrLevelsModalAction,
  closeBinsOrLevelsModalAction,
  openTransformColumnModalAction,
  closeTransformColumnModalAction,
  selectedBinsOrLevelsTabAction,
  saveBinLevelTransformationValuesAction,
  saveTopLevelValuesAction,
} from "../../actions/featureEngineeringActions";
import { getRemovedVariableNames } from "../../helpers/helper.js"
import { getDataSetPreview, getValueOfFromParam } from "../../actions/dataActions";
import { Bins } from "./Bins";
import { Levels } from "./Levels";
import { Scrollbars } from 'react-custom-scrollbars';
import { Transform } from "./Transform";
import { statusMessages } from "../../helpers/helper";
import { searchTable, sortTable } from "../../actions/dataCleansingActions";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    datasets: store.datasets,
    binsOrLevelsShowModal: store.datasets.binsOrLevelsShowModal,
    transferColumnShowModal: store.datasets.transferColumnShowModal,
    selectedItem: store.datasets.selectedItem,
    apps_regression_modelName: store.apps.apps_regression_modelName,
    currentAppDetails: store.apps.currentAppDetails,
    featureEngineering: store.datasets.featureEngineering,
    convertUsingBin: store.datasets.convertUsingBin,
    numberOfBins: store.datasets.topLevelData.numberOfBins,
    editmodelFlag:store.datasets.editmodelFlag,
    modelEditconfig: store.datasets.modelEditconfig,
  };
})

export class FeatureEngineering extends React.Component {
  constructor(props) {
    super(props);
    this.buttons = {};
    this.state = {
      filterElement:""
    };
    this.state.topLevelRadioButton = "false";
    this.pickValue = this.pickValue.bind(this);
    this.clearBinsAndIntervals = this.clearBinsAndIntervals.bind(this);
    this.updateLevelsData = this.updateLevelsData.bind(this);
  }

  componentWillMount() {
    if (this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null) {
      let mod =  window.location.pathname.includes("analyst")?"analyst":"autoML"
      this.props.history.replace("/apps/"+this.props.match.params.AppId+"/"+mod+"/models/data/"+this.props.match.params.slug)
    }else{
      this.setState({ featureEngineering: this.props.featureEngineering });
      if (this.props.dataPreview == null || this.props.dataPreview.status == 'FAILED') {
        this.props.dispatch(getDataSetPreview(this.props.match.params.slug));
      }
    }
    this.buttons['proceed'] = {
      url: "/data_cleansing/" + this.props.match.params.slug,
      text: "Proceed"
    };
    if(this.props.editmodelFlag){
      if(this.props.modelEditconfig.config.config.FEATURE_SETTINGS.FEATURE_ENGINEERING.overall_settings[0].selected){
        let binningData = this.props.modelEditconfig.config.config.FEATURE_SETTINGS.FEATURE_ENGINEERING.overall_settings[0];
        this.state.topLevelRadioButton = "true";
        this.props.dispatch(saveTopLevelValuesAction(this.state.topLevelRadioButton, binningData.number_of_bins));
      }
      this.setBinsOnEdit();
      this.setLevelOnEdit();
      this.setTransformOnEdit();
    }
  }

  setBinsOnEdit(){
    let colList = this.props.dataPreview.meta_data.uiMetaData.headersUI;
    let binsList= this.props.modelEditconfig.config.config.FEATURE_SETTINGS.FEATURE_ENGINEERING.column_wise_settings.level_creation_settings.operations;
    
    if(binsList.filter(i=>i.name === "create_custom_bins" && i.selected).length != 0) {
      let customBinData = binsList.filter(i=>i.name === "create_custom_bins" && i.selected)[0].columns;
      for(var i=0; i<customBinData.length; i++){
        let list = colList.filter(j=>j.name===customBinData[i].name)
        let dataToSave = [];
        dataToSave.push({newcolumnname:customBinData[i].actual_col_name, selectBinType:"create_custom_bins",specifyintervals:customBinData[i].list_of_intervals})
        this.props.dispatch(saveBinLevelTransformationValuesAction(list[0].slug,"binData",dataToSave[0]))
      }
    }
    if(binsList.filter(i=>i.name === "create_equal_sized_bins" && i.selected).length != 0) {
      let equalBinData = binsList.filter(i=>i.name === "create_equal_sized_bins" && i.selected)[0].columns;
      for(var i=0; i<equalBinData.length; i++){
        let list = colList.filter(j=>j.name===equalBinData[i].name)
        let dataToSave = [];
        dataToSave.push({newcolumnname:equalBinData[i].actual_col_name, selectBinType:"create_equal_sized_bins",numberofbins:equalBinData[i].number_of_bins})
        if(list[0].slug != "")
          this.props.dispatch(saveBinLevelTransformationValuesAction(list[0].slug,"binData",dataToSave[0]))
      }
    }
  }

  setLevelOnEdit(){
    let colList = this.props.dataPreview.meta_data.uiMetaData.headersUI;
    let levelsList= this.props.modelEditconfig.config.config.FEATURE_SETTINGS.FEATURE_ENGINEERING.column_wise_settings.level_creation_settings.operations;
    
    if(levelsList.filter(i=>i.name === "create_new_levels" && i.selected).length != 0) {
      let dLevelData = levelsList.filter(i=>i.name === "create_new_levels" && i.selected)[0].columns;
      for(var i=0; i<dLevelData.length; i++){
        let list = colList.filter(j=>j.name===dLevelData[i].name)
        let levelsValue = Object.entries(dLevelData[i].mapping_dict);
        let levelLen = levelsValue.length;
        let dataToSave = [];
        for(let i=0;i<levelLen;i++){
          dataToSave.push({inputValue:levelsValue[i][0],multiselectValue:levelsValue[i][1]})
        }
        if(list[0].slug != "")
          this.props.dispatch(saveBinLevelTransformationValuesAction(list[0].slug,"levelData",dataToSave))
      }
    }

    if(levelsList.filter(i=>i.name === "create_new_datetime_levels" && i.selected).length != 0) {
      let dtLevelData = levelsList.filter(i=>i.name === "create_new_datetime_levels" && i.selected)[0].columns;
      for(var i=0; i<dtLevelData.length; i++){
        let list = colList.filter(j=>j.name===dtLevelData[i].name)
        let levelsValue = Object.entries(dtLevelData[i].mapping_dict);
        let levelLen = levelsValue.length;
        let dataToSave = [];

        for(let i=0;i<levelLen;i++){
          let sDate = levelsValue[i][1][0].split("/").reverse().join("-");
          let eDate = levelsValue[i][1][1].split("/").reverse().join("-")
          dataToSave.push({inputValue:levelsValue[i][0],startDate:sDate,endDate:eDate})
        }
        if(list[0].slug != "")
          this.props.dispatch(saveBinLevelTransformationValuesAction(list[0].slug,"levelData",dataToSave))
      }
    }
  }

  setTransformOnEdit(){
    let colList = this.props.dataPreview.meta_data.uiMetaData.headersUI;
    let transList= this.props.modelEditconfig.config.config.FEATURE_SETTINGS.FEATURE_ENGINEERING.column_wise_settings.transformation_settings.operations;
    //for measure
    let dataToSave = [];
    let mTransData1 ={replace_values_with:false,replace_values_with_input:"",replace_values_with_selected:""};
    let mTransData2 ={feature_scaling:false,perform_standardization_select:""};
    let mTransData3 ={variable_transformation:false,variable_transformation_select:""};
    let transSlug = "";

    if(transList.filter(i=>i.name === "replace_values_with" && i.selected).length != 0){
      let transData = transList.filter(i=>i.name === "replace_values_with" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        mTransData1 = transList.filter(i=>i.name === "replace_values_with" && i.selected)[0].columns[0];
        mTransData1.replace_values_with=true;
        transSlug = list[0].slug;
      }
    }
    if(transList.filter(i=>i.name === "perform_standardization" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "perform_standardization" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        mTransData2 = transList.filter(i=>i.name === "perform_standardization" && i.selected)[0].columns[0];
        mTransData2.feature_scaling=true;
        transSlug = list[0].slug;
      } 
    }
    if(transList.filter(i=>i.name === "variable_transformation" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "variable_transformation" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        mTransData3 = transList.filter(i=>i.name === "variable_transformation" && i.selected)[0].columns[0];
        mTransData3.variable_transformation=true;
        transSlug = list[0].slug;
      } 
    }
    dataToSave.push({replace_values_with:mTransData1.replace_values_with,replace_values_with_input:mTransData1.replace_value,replace_values_with_selected:mTransData1.replace_by,
        feature_scaling:mTransData2.feature_scaling,perform_standardization_select:mTransData2.standardization_type,
        variable_transformation:mTransData3.variable_transformation,variable_transformation_select:mTransData3.transformation_type})
    
    if(transSlug != "") 
      this.props.dispatch(saveBinLevelTransformationValuesAction(transSlug,"transformationData",dataToSave[0]));
  
    //for dimension
    let dataToSave1 = [];
    let dimData1 ={encoding_dimensions:false,encoding_type:""};
    let dimData2 ={return_character_count:false};
    let dimData3 ={is_custom_string_in:false,is_custom_string_in_input:""};
    let transSlug1 = "";

    if(transList.filter(i=>i.name === "encoding_dimensions" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "encoding_dimensions" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dimData1 = transList.filter(i=>i.name === "encoding_dimensions" && i.selected)[0].columns[0];
        dimData1.encoding_dimensions=true;
        transSlug1 = list[0].slug;
      }
    }
    if(transList.filter(i=>i.name === "return_character_count" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "return_character_count" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dimData2 = transList.filter(i=>i.name === "return_character_count" && i.selected)[0].columns[0];
        dimData2.return_character_count=true;
        transSlug1 = list[0].slug;
      } 
    }
    if(transList.filter(i=>i.name === "is_custom_string_in" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "is_custom_string_in" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dimData3 = transList.filter(i=>i.name === "is_custom_string_in" && i.selected)[0].columns[0];
        dimData3.is_custom_string_in=true;
        transSlug1 = list[0].slug;
      } 
    }
    dataToSave1.push({encoding_dimensions:dimData1.encoding_dimensions,encoding_type:dimData1.encoding_type,
      return_character_count:dimData2.return_character_count,
      is_custom_string_in:dimData3.is_custom_string_in,is_custom_string_in_input:dimData3.user_given_string})
      
    if(transSlug1 != "")
      this.props.dispatch(saveBinLevelTransformationValuesAction(transSlug1,"transformationData",dataToSave1[0]));
  
    //For datetime
    let dataToSave2 = [];
      let dtData1 ={is_date_weekend:false};
      let dtData2 ={extract_time_feature:false,extract_time_feature_select:""};
      let dtData3 ={time_since:false,time_since_input:""};
      let transSlug2 = "";

    if(transList.filter(i=>i.name === "is_date_weekend" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "is_date_weekend" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dtData1 = transList.filter(i=>i.name === "is_date_weekend" && i.selected)[0].columns[0];
        dtData1.is_date_weekend=true;
        transSlug2 = list[0].slug;
      }
    }
    if(transList.filter(i=>i.name === "extract_time_feature" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "extract_time_feature" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dtData2 = transList.filter(i=>i.name === "extract_time_feature" && i.selected)[0].columns[0];
        dtData2.extract_time_feature=true;
        transSlug2 = list[0].slug;
      } 
    }
    if(transList.filter(i=>i.name === "time_since" && i.selected).length != 0) {
      let transData = transList.filter(i=>i.name === "time_since" && i.selected)[0].columns;
      for(var i=0; i<transData.length; i++){
        let list = colList.filter(j=>j.name===transData[i].name)
        dtData3 = transList.filter(i=>i.name === "time_since" && i.selected)[0].columns[0];
        dtData3.time_since_is_true=true;
        transSlug2 = list[0].slug;
        dtData3.time_since_input = transData[0].time_since.split("/").reverse().join("-")
      } 
    }
    dataToSave2.push({is_date_weekend:dtData1.is_date_weekend,
      extract_time_feature:dtData2.extract_time_feature, extract_time_feature_select:dtData2.time_feature_to_extract,
      time_since:dtData3.time_since_is_true, time_since_input:dtData3.time_since_input})
    
    if(transSlug2 != "")
      this.props.dispatch(saveBinLevelTransformationValuesAction(transSlug2,"transformationData",dataToSave2[0]));
  }

  componentDidMount() {
    var selectElements = document.getElementsByTagName("select");
    var i,j;
    for (i = 0; i < selectElements.length; i++) {
      for(j=0;j<selectElements[i].options.length;j++){
        if(selectElements[i].options[j].selected)
         selectElements[i].options[j].style.display = 'none';
        else
          selectElements[i].options[j].style.display = 'inline';
      }
    }
    const from = getValueOfFromParam();
    if (from === 'algorithm_selection') {
    }else if(!this.props.editmodelFlag){
      this.props.dispatch(saveTopLevelValuesAction(this.props.convertUsingBin,0));
    }
  }

  clearBinsAndIntervals() {
    if (this.state[this.props.selectedItem.slug] != undefined && this.state[this.props.selectedItem.slug]["binData"] != undefined) {
      this.state[this.props.selectedItem.slug]["binData"]["numberofbins"] = ""
      this.state[this.props.selectedItem.slug]["binData"]["specifyintervals"] = ""
      this.setState({ state: this.state });
    }
  }

  pickValue(actionType, event) {
    if (this.state[this.props.selectedItem.slug] == undefined) {
      this.state[this.props.selectedItem.slug] = {}
    }
    if (this.state[this.props.selectedItem.slug][actionType] == undefined) {
      this.state[this.props.selectedItem.slug][actionType] = {}
    }
    if (event.target.type == "checkbox") {
      this.state[this.props.selectedItem.slug][actionType][event.target.name] = event.target.checked;
    } else {
      this.state[this.props.selectedItem.slug][actionType][event.target.name] = event.target.value;
    }
  }

  updateLevelsData(data) {
    if (!this.state[this.props.selectedItem.slug]) {
      this.state[this.props.selectedItem.slug] = {};
    }
    this.state[this.props.selectedItem.slug]["levelData"] = data;
  }

  getLevelsData() {
    if (this.props.featureEngineering[this.props.selectedItem.slug]) {
      var levelsData = this.props.featureEngineering[this.props.selectedItem.slug]["levelData"];
      if (levelsData) {
        return JSON.parse(JSON.stringify(levelsData));
      }
    }
    return []
  }

  handleCreateClicked(actionType, event) {
    if (actionType == "binData") {
      this.validateBinData(actionType);
    } else if (actionType == "levelData") {
      this.validateLevelData(actionType);
    } else if (actionType == "transformationData") {
      this.validateTransformdata(actionType);
    } else {
      var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
      this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
      this.closeBinsOrLevelsModal();
      this.closeTransformColumnModal();
    }
  }

  validateBinData(actionType) {
    var slugData = this.state[this.props.selectedItem.slug];
    if (slugData != undefined && this.state[this.props.selectedItem.slug][actionType] != undefined) {
      var binData = this.state[this.props.selectedItem.slug][actionType];
      if (binData.selectBinType == undefined || binData.selectBinType == "none") {
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please select type of binning");
        $("select[name='selectBinType']").focus();
        return;
      } else {
        if (binData.selectBinType == "create_equal_sized_bins") {
          if (binData.numberofbins == undefined || binData.numberofbins == null || binData.numberofbins == "") {
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Please enter number of bins");
            $("input[name='numberofbins']").focus();
            return;
          }
          else if (parseInt(binData.numberofbins) <= 0) {
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Please enter number greater than zero");
            $("input[name='numberofbins']").focus();
            return;
          }
        } else if (binData.selectBinType == "create_custom_bins") {
          if (binData.specifyintervals == undefined || binData.specifyintervals == null || binData.specifyintervals == "") {
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Please enter 'Specify Intervals' field");
            $("input[name='specifyintervals']").focus();
            return;
          }
        }
      }
      if (binData.newcolumnname == undefined || binData.newcolumnname == null || binData.newcolumnname == "") {
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter the new column name");
        $("input[name='newcolumnname']").focus();
        return;
      }
      var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
      this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
      this.closeBinsOrLevelsModal();
      this.closeTransformColumnModal();
    } else {
      $("#fileErrorMsg").removeClass("visibilityHidden");
      $("#fileErrorMsg").html("Please enter Mandatory fields * ");
    }
  }

  validateLevelData(actionType) {
    var lvlar;
    if(this.props.selectedItem.columnType == "dimension"){
      let totalOptions=0;
      lvlar = this.state[this.props.selectedItem.slug];
      if(lvlar === undefined){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Please enter some values");
        return false;
      }
      var lvl = lvlar.levelData;
      let lvllen=lvl.length;
      for(i in lvl){ 
        if(lvl[i].inputValue == "" || undefined){
          $("#fileErrorMsg").removeClass("visibilityHidden");
          $("#fileErrorMsg").html("Please enter the new column name");
          $("input[name='newcolumnname']").focus();
          return;
        }else if(lvl[i].multiselectValue == "" || undefined){
          $("#fileErrorMsg").removeClass("visibilityHidden");
          $("#fileErrorMsg").html("Please Select Options");
          $("input[name='multiselect-demo']").focus();
          return;
        }
        totalOptions+=lvl.map(j=>j)[i].multiselectValue.length
      }
      var noOfRows = this.props.dataPreview.meta_data.scriptMetaData.metaData.filter(rows=>rows.name=="noOfRows").map(i=>i.value)[0];
      var rowCount = Math.round(Math.sqrt(noOfRows));
      var noOfLvls = this.props.selectedItem.columnStats.filter(lc=>lc.name=="numberOfUniqueValues").map(i=>i.value)[0];
      var lvlCount = noOfLvls-totalOptions+lvllen;
      if(lvlCount>Math.min(200,rowCount)){
        $("#fileErrorMsg").removeClass("visibilityHidden");
        $("#fileErrorMsg").html("Add more levels so that total level count is less than "+ Math.min(200,rowCount));
        return;
      }
    }
    
    var slugData = this.state[this.props.selectedItem.slug];
    if (slugData != undefined && this.state[this.props.selectedItem.slug][actionType] != undefined) {
      var levelData = this.state[this.props.selectedItem.slug][actionType];
      if(this.props.selectedItem.columnType == "datetime"){
        for (var i = 0; i < levelData.length; i++) {
          var startDate = levelData[i].startDate;
          var endDate = levelData[i].endDate;
          var inputValue = levelData[i].inputValue;
          var multiselect = levelData[i].multiselectValue;
          if((startDate == "" || undefined) || (endDate == "" || undefined) ){
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Enter Dates");
            return;
          }
          else if ((Date.parse(startDate) > Date.parse(endDate))) {
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Start Date should be before End Date");
            return;
          }
          else if (inputValue == undefined || inputValue == null || inputValue == "") {
            $("#fileErrorMsg").removeClass("visibilityHidden");
            $("#fileErrorMsg").html("Please enter level name");
            $("input[name='newcolumnname']").focus();
            return;
          }
        }
      }
      var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
      this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
      this.closeBinsOrLevelsModal();
      this.closeTransformColumnModal();
    } else {
      $("#fileErrorMsg").removeClass("visibilityHidden");
      $("#fileErrorMsg").html("Please enter new level ");
    }
  }

  validateTransformdata(actionType) {
    var slugData = this.state[this.props.selectedItem.slug];
    if (slugData != undefined && this.state[this.props.selectedItem.slug][actionType] != undefined) {
      var transformationData = this.state[this.props.selectedItem.slug][actionType];

      if(this.props.selectedItem.columnType == "measure"){
        if(!$('#replace_values_with').prop('checked') && !$('#feature_scaling').prop('checked') && !$('#variable_transformation').prop('checked')){
          $("#fileErrorMsg").removeClass("visibilityHidden");
          $("#fileErrorMsg").html("No fields Selected");
        }else{
          if (transformationData.replace_values_with == true || $('#replace_values_with').prop('checked') ) {
            if (transformationData.replace_values_with_input == undefined || transformationData.replace_values_with_input == null || transformationData.replace_values_with_input == "" || $('#replace_values_with_input').val() == "") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Enter value");
              $("input[name='replace_values_with_input']").focus();
              return;
            }
            else if (transformationData.replace_values_with_selected == undefined || transformationData.replace_values_with_selected == null || transformationData.replace_values_with_selected == "" || $('#replace_values_with_selected').val() == "" || $('#replace_values_with_selected').val() == "None") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Select value to replace with");
              $("select[name='replace_values_with_selected']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }

            if((transformationData.feature_scaling == true) || $('#feature_scaling').prop('checked')){
              if (transformationData.perform_standardization_select == undefined || transformationData.perform_standardization_select == null || transformationData.perform_standardization_select == "" || $('#perform_standardization_select').val() == "" || $('#perform_standardization_select').val() == "None") {
                $("#fileErrorMsg").removeClass("visibilityHidden");
                $("#fileErrorMsg").html("Select value for feature scaling");
                $("select[name='perform_standardization_select']").focus();
                return;
              }else{
                $("#fileErrorMsg").addClass("visibilityHidden");
              }
            }

          if (transformationData.variable_transformation == true || $('#variable_transformation').prop('checked')) {
            if (transformationData.variable_transformation_select == undefined || transformationData.variable_transformation_select == null || transformationData.variable_transformation_select == ""|| $('#variable_transformation_select').val() == "" || $('#variable_transformation_select').val() == "None") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Select value for variable transformation");
              $("select[name='variable_transformation_select']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }

          var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
          this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
          dataToSave.encoding_dimensions?dataToSave.encoding_type=dataToSave.encoding_type:dataToSave.encoding_type="";
          this.closeBinsOrLevelsModal();
          this.closeTransformColumnModal();
        }
      }
      else if(this.props.selectedItem.columnType == "dimension"){
        if(!document.getElementById("encoding_dimensions").checked && !document.getElementById("return_character_count").checked && !document.getElementById("is_custom_string_in").checked){
          $("#fileErrorMsg").removeClass("visibilityHidden");
          $("#fileErrorMsg").html("No fields Selected");
        }else{
          if (transformationData.encoding_dimensions == true || document.getElementById("encoding_dimensions").checked) {
            if (transformationData.encoding_type == undefined || transformationData.encoding_type == null || transformationData.encoding_type == "" || $("#encoding_type").val() == "") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Select Encoding Type");
              $("select[name='encoding_type']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }

          if (transformationData.is_custom_string_in == true || document.getElementById("is_custom_string_in").checked) {
            if (transformationData.is_custom_string_in_input == undefined || transformationData.is_custom_string_in_input == null || transformationData.is_custom_string_in_input == "" || $("input[name='is_custom_string_in_input']").val() == "") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Enter value for custom String");
              $("input[name='is_custom_string_in_input']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }
          var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
          this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
          dataToSave.encoding_dimensions?dataToSave.encoding_type=dataToSave.encoding_type:dataToSave.encoding_type="";
          this.closeBinsOrLevelsModal();
          this.closeTransformColumnModal();
        }
      }else if(this.props.selectedItem.columnType == "datetime"){
        if(!document.getElementById("extract_time_feature").checked && !document.getElementById("time_since").checked && !document.getElementById("is_date_weekend").checked ){
          $("#fileErrorMsg").removeClass("visibilityHidden");
          $("#fileErrorMsg").html("No fields Selected");
        }else{
          if (transformationData.extract_time_feature == true || document.getElementById("extract_time_feature").checked) {
            if (transformationData.extract_time_feature_select == undefined || transformationData.extract_time_feature_select == null || transformationData.extract_time_feature_select == "" || $("select[name='extract_time_feature_select']").val() == "" ){
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Select value for time feature");
              $("select[name='extract_time_feature_select']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }

          if (transformationData.time_since == true || document.getElementById("time_since").checked) {
            if (transformationData.time_since_input == undefined || transformationData.time_since_input == null || transformationData.time_since_input == "" || $("input[name='time_since_input']").val()== "") {
              $("#fileErrorMsg").removeClass("visibilityHidden");
              $("#fileErrorMsg").html("Enter value for Time Since");
              $("input[name='time_since_input']").focus();
              return;
            }else
              $("#fileErrorMsg").addClass("visibilityHidden");
          }
          var dataToSave = JSON.parse(JSON.stringify(this.state[this.props.selectedItem.slug][actionType]));
          this.props.dispatch(saveBinLevelTransformationValuesAction(this.props.selectedItem.slug, actionType, dataToSave));
          dataToSave.encoding_dimensions?dataToSave.encoding_type=dataToSave.encoding_type:dataToSave.encoding_type="";
          this.closeBinsOrLevelsModal();
          this.closeTransformColumnModal();
        }
      }
    }else{
      $("#fileErrorMsg").removeClass("visibilityHidden");
      $("#fileErrorMsg").html("Please enter some values");
      return false;
    }
  }

  handleTopLevelRadioButtonOnchange(event) {
    this.state.topLevelRadioButton = event.target.value;
    this.saveTopLevelValues();
  }
  handleTopLevelInputOnchange(event) {
    var datasetRow = this.props.dataPreview.meta_data.uiMetaData.metaDataUI[0].value
    if(this.props.convertUsingBin === "true" && document.getElementById("flight_number").value === ""){
      $("#binErrorMsg").removeClass("visibilityHidden");
      $("#binErrorMsg").html("Please enter number of bins");
      return false;
    }
    else if(0 >= document.getElementById("flight_number").value || document.getElementById("flight_number").value >= datasetRow){
      $("#binErrorMsg").removeClass("visibilityHidden");
      $("#binErrorMsg").html("Value should be greater than 0 and less than "+ datasetRow +"");
      return false;
    }
    else if(!Number.isInteger(parseFloat(event.target.value))){
      $("#binErrorMsg").removeClass("visibilityHidden");
      $("#binErrorMsg").html("Value should be a positive interger");
      return false;
    }
    else{
      $("#binErrorMsg").addClass("visibilityHidden");
      $("#binErrorMsg").html("");
      this.state.topLevelInput = event.target.value;
      this.saveTopLevelValues();
    }
  }
  saveTopLevelValues() {
    this.props.dispatch(saveTopLevelValuesAction(this.state.topLevelRadioButton, this.state.topLevelInput));
    this.setState({ state: this.state });
  }
  handleProcedClicked(dataPreview,event) {
    var datasetRow = dataPreview.meta_data.uiMetaData.metaDataUI[0].value
    if(this.props.convertUsingBin === "true" && document.getElementById("flight_number").value === "" ){
      bootbox.alert(statusMessages("warning", "Please resolve errors", "small_mascot"));
      return false;
    }else if( this.props.convertUsingBin === "true" && (0 >= document.getElementById("flight_number").value || document.getElementById("flight_number").value >= datasetRow) ){
      bootbox.alert(statusMessages("warning", "Please resolve errors", "small_mascot"));
      return false;
    }
    else{
      var proccedUrl = this.props.match.url.replace('featureEngineering', 'algorithmSelection');
      this.props.history.push(proccedUrl);
    }
  }
  isBinningOrLevelsDisabled(item) {
    return ((this.state.topLevelRadioButton == "true" && item.columnType == "measure") || (item.columnType != item.actualColumnType))
  }

  handleBack=()=>{
    const appId = this.props.match.params.AppId;
    const slug = this.props.match.params.slug;
    this.props.history.replace(`/apps/${appId}/analyst/models/data/${slug}/createModel/dataCleansing?from=feature_Engineering`);
  }
  filterFeTable(e){
    var table = document.getElementById("fetable");
    var tr = table.getElementsByTagName("tr");
     document.getElementById("search").value=""

    for(var i=0;i<tr.length-1;i++){
     tr[i].style.display = ""
    }
    if(tr[tr.length-1].children[0].className=="searchErr")
    document.getElementById("fetable").deleteRow(tr.length-1)

    var select = document.getElementById('sdataTypeFe');
    this.setState({filterElement:e.target.value})
    var selectedOption = e.target.value
     
    for(var i=0;i<select.options.length;i++){
     if(select.options[i].value==selectedOption)
       select.options[i].style.display='none'
       else
       select.options[i].style.display='inline'
    }
  }
  searchTable() {
    searchTable("fetable",0,4);
  }

  sortTable(n) {
    sortTable(n,"fetable")
  }

  render() {
    var feHtml = "", binsOrLevelsPopup = "", transformColumnPopup = "", binOrLevels = "", binOrLevelData = "";
    var removedVariables = getRemovedVariableNames(this.props.datasets);
    var numberOfSelectedMeasures = 0, numberOfSelectedDimensions = 0;

    if(this.props.dataPreview != null)
      var considerItems = this.props.datasets.dataPreview.meta_data.uiMetaData.columnDataUI.filter(i => ((i.consider === false) && (i.ignoreSuggestionFlag === false)) || ((i.consider === false) && (i.ignoreSuggestionFlag === true) && (i.ignoreSuggestionPreviewFlag === true))).map(j => j.name);

    var unselectedvar = [];
    for (var key in this.props.datasets.selectedVariables) {
      if (!this.props.datasets.selectedVariables[key])
        unselectedvar.push(key);
    }
    if (this.props.dataPreview != null) {
      feHtml = this.props.dataPreview.meta_data.scriptMetaData.columnData.map((item, key) => {
        if (removedVariables.indexOf(item.name) != -1 || unselectedvar.indexOf(item.slug) != -1 || considerItems.indexOf(item.name) != -1){
          return null
        }else{
          if (item.columnType == "measure")
            numberOfSelectedMeasures += 1;
        else
          numberOfSelectedDimensions += 1;
        }
        if (removedVariables.indexOf(item.name) != -1 || unselectedvar.indexOf(item.slug) != -1 || considerItems.indexOf(item.name) != -1||(this.state.filterElement!="" && item.columnType!=this.state.filterElement))
          return null;
        return (
          <tr key={key} className={('all ' + item.columnType)}>
            <td className="text-left"> {item.name}</td>
            <td> {item.columnType.charAt(0).toUpperCase() + item.columnType.slice(1)}</td>
            <td> <Button className= "btn btn-cst_button" id={`bin_${item.name}`} onClick={this.openBinsOrLevelsModal.bind(this, item)} disabled={this.isBinningOrLevelsDisabled(item)} >Create Bins or Levels</Button></td>
            <td> <Button className= "btn btn-cst_button" id={`tranform_${item.name}`} onClick={this.openTransformColumnModal.bind(this, item)} >Transform</Button></td>
          </tr>
        );
      })
    }
    if (this.props.selectedItem.columnType == "measure") {
      binOrLevels = <Bins parentPickValue={this.pickValue} clearBinsAndIntervals={this.clearBinsAndIntervals} />
      binOrLevelData = "binData";
    }else if (this.props.selectedItem.columnType == "dimension") {
      binOrLevels = <Levels parentPickValue={this.pickValue} parentUpdateLevelsData={this.updateLevelsData} levelsData={this.getLevelsData()} />
      binOrLevelData = "levelData";
    }else {
      binOrLevels = <Levels parentPickValue={this.pickValue} parentUpdateLevelsData={this.updateLevelsData} levelsData={this.getLevelsData()} />
      binOrLevelData = "levelData";
    }

    binsOrLevelsPopup = (
      <div id="binsOrLevels" role="dialog" className="modal fade modal-colored-header">
        <Modal show={this.props.binsOrLevelsShowModal} onHide={this.closeBinsOrLevelsModal.bind(this)} dialogClassName="modal-colored-header modal-md" style={{ overflow: 'inherit' }} >
          <Modal.Header closeButton>
            <h3 className="modal-title">Create {(this.props.selectedItem.columnType == "measure") ? "Bins" : "Levels"}</h3>
          </Modal.Header>
          <Modal.Body>
            <div>
              <h4>What you want to do?</h4>
              {binOrLevels}
            </div>
            <div id="errorMsgs" className="text-danger"></div>
          </Modal.Body>
          <Modal.Footer>
            <Button id="binsCancel" onClick={this.closeBinsOrLevelsModal.bind(this)}>Cancel</Button>
            <Button id="binsCreate" bsStyle="primary" form="binsForm" content="Submit" value="Submit" onClick={this.handleCreateClicked.bind(this, binOrLevelData)}>Create</Button>
          </Modal.Footer>
        </Modal>
      </div>
    )
    transformColumnPopup = (
      <div class="col-md-3 xs-mb-15 list-boxes" >
        <div id="transformColumnPopup" role="dialog" className="modal fade modal-colored-header">
          <Modal show={this.props.transferColumnShowModal} onHide={this.closeTransformColumnModal.bind(this)} dialogClassName="modal-colored-header">
            <Modal.Header closeButton>
              <h3 className="modal-title">Transform {this.props.selectedItem.columnType} column</h3>
            </Modal.Header>
            <Modal.Body>
              <Transform parentPickValue={this.pickValue} />
            </Modal.Body>
            <Modal.Footer>
              <Button id="transformCancel"  onClick={this.closeTransformColumnModal.bind(this)}>Cancel</Button>
              <Button id="transformCreate"  bsStyle="primary" onClick={this.handleCreateClicked.bind(this, "transformationData")}>Create</Button>
            </Modal.Footer>
          </Modal>
        </div>
      </div>
    )

    return (
        <div className="side-body">
          <div class="page-head">
            <h3 class="xs-mt-0 xs-mb-0 text-capitalize">Feature Engineering</h3>
          </div>
          {binsOrLevelsPopup}
          {transformColumnPopup}
          <div className="main-content">
            <div class="row">
              <div class="col-md-12">
                <div class="panel box-shadow xs-m-0">
                  <div class="panel-body no-border xs-p-20">
                    <h4> The dataset contains {numberOfSelectedMeasures + numberOfSelectedDimensions} columns or features ({numberOfSelectedMeasures} measures and {numberOfSelectedDimensions} dimensions).  If you would like to transform the existing features or create new features from the existing data, you can use the options provided below. </h4><hr />
                    <p class="inline-block">
                      <i class="fa fa-angle-double-right text-primary"></i> Do you want to convert all measures into dimension using binning? &nbsp;&nbsp;&nbsp;
                  </p>
                    <span onChange={this.handleTopLevelRadioButtonOnchange.bind(this)} className="inline">
                      <div class="ma-checkbox inline">
                        <input type="radio" id="mTod-binning1" value="true" name="mTod-binning" defaultChecked={this.props.convertUsingBin === "true"} />
                        <label for="mTod-binning1">Yes</label>
                      </div>
                      <div class="ma-checkbox inline">
                        <input type="radio" id="mTod-binning2" value="false" name="mTod-binning" defaultChecked={this.props.convertUsingBin === "false"} />
                        <label for="mTod-binning2">No </label>
                      </div>
                    </span>
                    {(this.props.convertUsingBin === "true") ?
                        <div id="box-binning" class="xs-ml-20 block-inline">
                          <div class="inline-block"> Number of bins : 
                            <input type="number" onInput={this.handleTopLevelInputOnchange.bind(this)} class="test_css form-control" id="flight_number" name="number" defaultValue={this.props.numberOfBins} />
                          </div>
                          <div class="row form-group">
                            <div className="text-danger visibilityHidden" id="binErrorMsg">ha</div>     
                          </div>
                      </div> : ""}
                  </div>
                </div>
                <div className="panel box-shadow ">
                  <div class="panel-body no-border xs-p-20">
                    <div class="row xs-mb-10">
                      <div className="col-md-6">
                        <div class="form-inline" >
                          <div class="form-group">
                            <label for="sdataTypeFe">Filter By Datatype: </label>
                            <select id="sdataTypeFe" onChange={this.filterFeTable.bind(this)} className="form-control cst-width">
                              <option value="">All</option>
                              <option value="measure">Measure</option>
                              <option value="dimension">Dimension</option>
                              <option value="datetime">Datetime</option>
                            </select>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-6">
                        <div class="form-inline" >
                          <div class="form-group pull-right">
                            <input type="text" id="search" className="form-control" onKeyUp={this.searchTable.bind(this)} placeholder="Search..."></input>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="table-responsive noSwipe xs-pb-5">
                      <Scrollbars style={{height: 500}}>
                        <table id="fetable" className="table table-striped table-bordered break-if-longText">
                          <thead>
                            <tr key="trKey" className="myHead">
                              <th className="text-left addSort" onClick={this.sortTable.bind(this,0)}><b>Variable name</b></th>
                              <th className="addSort" onClick={this.sortTable.bind(this,1)}><b>Data type</b></th>
                              <th></th>
                              <th></th>
                            </tr>
                          </thead>                    
                          <tbody className="no-border-x">{(feHtml!="" && feHtml.filter(i=>i!=null).length>=1) ? feHtml: (<tr><td className='text-center' colSpan={4}>"No data found for your selection"</td></tr>)}</tbody>
                        </table>
                      </Scrollbars>
                    </div>
                  </div>
                  <div className="panel-body box-shadow">
                  <Button id="FeBack" onClick={this.handleBack} bsStyle="primary"><i class="fa fa-angle-double-left"></i> Back</Button>
                    <div className="buttonRow" id="dataPreviewButton" style={{float:"right",display:"inline-block"}}>
                      <Button id="FeProceed" onClick={this.handleProcedClicked.bind(this,this.props.dataPreview)} bsStyle="primary">{this.buttons.proceed.text} <i class="fa fa-angle-double-right"></i></Button>
                    </div>
                    <div class="xs-p-10"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    );
  }

  openBinsOrLevelsModal(item) {
    this.props.dispatch(openBinsOrLevelsModalAction(item));
   }

  closeBinsOrLevelsModal(event) {
    this.props.dispatch(closeBinsOrLevelsModalAction());
  }
  openTransformColumnModal(item) {
    this.props.dispatch(openTransformColumnModalAction(item));
  }

  closeTransformColumnModal() {
    this.props.dispatch(closeTransformColumnModalAction());
  }

  handleSelect(selectedKey) {
    this.props.dispatch(selectedBinsOrLevelsTabAction(selectedKey));
  }

  createLevels(slug) {
    this.props.dispatch();
  }
}