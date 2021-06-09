import React from "react";
import { connect } from "react-redux";
import { saveEncodingValuesAction } from "../../actions/featureEngineeringActions";

@connect((store) => {
  return {
    dataPreview: store.datasets.dataPreview,
    selectedItem: store.datasets.selectedItem,
    featureEngineering:store.datasets.featureEngineering,
  };
})

export class Transform extends React.Component {
  constructor(props) {
    super(props);
    this.pickValue = this.pickValue.bind(this);
    this.state = {};
    this.state.encodingRadioButton;
  }

  componentDidMount(){
  if(this.props.selectedItem.columnType=="measure"){
    if(document.getElementById("replace_values_with_input").value != "" || document.getElementById("replace_values_with_selected").value != ""){
      document.getElementById("replace_values_with").checked=true;
      document.getElementById("replace_values_with_input").disabled=false;
      document.getElementById("replace_values_with_selected").disabled=false;
    }
    if(document.getElementById("perform_standardization_select").value != ""){
      document.getElementById("feature_scaling").checked=true;
      document.getElementById("perform_standardization_select").disabled=false;
    }
    if(document.getElementById("variable_transformation_select").value != ""){
      document.getElementById("variable_transformation").checked=true;
      document.getElementById("variable_transformation_select").disabled=false;
    }
  }else if(this.props.selectedItem.columnType=="dimension"){
    if(document.getElementById("encoding_dimensions").checked){
      $("#one_hot_encoding").parent().removeClass("disabled");
      $("#label_encoding").parent().removeClass("disabled");
    }
    if(document.getElementById("is_custom_string_in_input").value != ""){
      document.getElementById("is_custom_string_in").checked=true;
      document.getElementById("is_custom_string_in_input").disabled=false;
    }
  }else{
    if(document.getElementById("extract_time_feature_select").value !=""){
      document.getElementById("extract_time_feature").checked=true;
      document.getElementById("extract_time_feature_select").disabled=false;
    }
    if(document.getElementById("time_since_input").value !=""){
      document.getElementById("time_since").checked=true;
      document.getElementById("time_since_input").disabled=false;
    }
  }

  if(this.props.selectedItem.columnType=="measure"){
    $('#replace_values_with').change(function() {
      if ($(this).prop('checked')) {
        document.getElementById("replace_values_with_input").disabled=false;
        document.getElementById("replace_values_with_selected").disabled=false;
      }else {
        document.getElementById("replace_values_with_input").disabled=true;
        document.getElementById("replace_values_with_selected").disabled=true;
      }
    });

    $('#feature_scaling').change(function() {
      if ($(this).prop('checked')) {
        document.getElementById("perform_standardization_select").disabled=false;
      }else {
        document.getElementById("perform_standardization_select").disabled=true;
      }
    });

    $('#variable_transformation').change(function() {
      if ($(this).prop('checked')) {
        document.getElementById("variable_transformation_select").disabled=false;
      }else {
        document.getElementById("variable_transformation_select").disabled=true;
      }
    });

  }else if(this.props.selectedItem.columnType=="dimension"){
    $('#encoding_dimensions').change(function() {
        if ($(this).prop('checked')) {
          $("#one_hot_encoding").parent().removeClass("disabled");
          $("#label_encoding").parent().removeClass("disabled");
          $("#one_hot_encoding").removeAttr('disabled');
          $("#label_encoding").removeAttr('disabled');
        }
        else {
          $("#one_hot_encoding").parent().addClass("disabled");
          $("#label_encoding").parent().addClass("disabled");
          $("#one_hot_encoding").attr('disabled','disabled');
          $("#label_encoding").attr('disabled','disabled');
        }
      });
      $('#is_custom_string_in').change(function() {
        if ($(this).prop('checked')) {
          document.getElementById("is_custom_string_in_input").disabled=false;
        }else {
          document.getElementById("is_custom_string_in_input").disabled=true;
        }
      });
    }else{
      $('#extract_time_feature').change(function() {
        if ($(this).prop('checked')) {
          document.getElementById("extract_time_feature_select").disabled=false;
        }else {
          document.getElementById("extract_time_feature_select").disabled=true;
        }
      });
      $('#time_since').change(function() {
        if ($(this).prop('checked')) {
          document.getElementById("time_since_input").disabled=false;
        }else {
          document.getElementById("time_since_input").disabled=true;
        }
      });
    }
  }
  
  getTranformDataValue(name){
    var transformationData = {};
    if(this.props.featureEngineering != undefined || this.props.featureEngineering !=null){
      var slugData = this.props.featureEngineering[this.props.selectedItem.slug];
      if(slugData != undefined ){
        if(slugData.transformationData != undefined)
          transformationData = slugData.transformationData;
      }
    }
    var value = transformationData[name];
    return value
  }

  pickValue(event){
    document.getElementById("fileErrorMsg").innerText = ""
    if(this.props.selectedItem.columnType == "measure"){ 
      if(document.getElementById("replace_values_with").checked){
        document.getElementById("replace_values_with_input").disabled= false;
        document.getElementById("replace_values_with_selected").disabled= false;
      }else{
        document.getElementById("replace_values_with_input").disabled= true;
        document.getElementById("replace_values_with_selected").disabled= true;
        document.getElementById("replace_values_with_input").value= "";
        document.getElementById("replace_values_with_selected").value= "";
      }
      if(document.getElementById("feature_scaling").checked){
        document.getElementById("perform_standardization_select").disabled=false;
      }else{
        document.getElementById("perform_standardization_select").disabled=true;
        document.getElementById("perform_standardization_select").value= "";
      }
      if(document.getElementById("variable_transformation").checked){
        document.getElementById("variable_transformation_select").disabled=false;
      }else{
        document.getElementById("variable_transformation_select").disabled=true;
        document.getElementById("variable_transformation_select").value= "";
      }
    }else if(this.props.selectedItem.columnType == "dimension"){
      if(document.getElementById('encoding_dimensions').checked){
        $("#one_hot_encoding").parent().removeClass("disabled");
        $("#label_encoding").parent().removeClass("disabled");
      }else{
        $("#one_hot_encoding").parent().addClass("disabled");
        $("#label_encoding").parent().addClass("disabled");
        document.getElementById('one_hot_encoding').checked = false ;
        document.getElementById('label_encoding').checked = false ;
        document.getElementById("one_hot_encoding").value= "";
        document.getElementById("label_encoding").value= "";
      }
      if(document.getElementById("is_custom_string_in").checked){
        document.getElementById("is_custom_string_in_input").disabled=false;
      }else{
        document.getElementById("is_custom_string_in_input").disabled=true;
        document.getElementById("is_custom_string_in_input").value= "";
      }
    }else{ 
      if(document.getElementById("extract_time_feature").checked){
        document.getElementById("extract_time_feature_select").disabled=false;
      }else{
        document.getElementById("extract_time_feature_select").disabled=true;
        document.getElementById("extract_time_feature_select").value= "";
      }
      if(document.getElementById("time_since").checked){
        document.getElementById("time_since_input").disabled=false;
      }else{
        document.getElementById("time_since_input").disabled=true;
        document.getElementById("time_since_input").value= "";
      }
    }
    this.props.parentPickValue("transformationData", event);
  }

  handleEncodingRadioButtonOnchange(event){
    this.state.encodingRadioButton = event.target.value;
    this.props.dispatch(saveEncodingValuesAction(this.state.encodingRadioButton));
    this.setState({ state: this.state });
  }

  render() {
    if(this.props.selectedItem.columnType == "measure"){
      return (
        <div class="modal-body">
          <h4>What would you like to do with {this.props.selectedItem.name} column?</h4>
          <p>Please select any of the options provided below that will help in transforming the chosen column into multiple new features.
            Each option will create an additional feature derived out of the original column.</p>
          <hr/>
          <form class="form_withrowlabels" id="binsForm">
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="replace_values_with" name="replace_values_with" defaultValue={this.getTranformDataValue("replace_values_with")} type="checkbox" class="needsclick" onInput={this.pickValue} />
                  <label for="replace_values_with">Replace Values:</label>
                </div>
              </div>
              <div class="col-md-3 col-sm-3">
                <input type="number" id="replace_values_with_input" name="replace_values_with_input" class="form-control" placeholder="Value" defaultValue={this.getTranformDataValue("replace_values_with_input")} onInput={this.pickValue} disabled/>
              </div>
              <label for="replace_values_with_selected" class="col-md-1 col-sm-1 control-label xs-p-0 xs-mt-5 text-right">With</label>
              <div class="col-md-3 col-sm-3">
                <select class="form-control" id="replace_values_with_selected" name="replace_values_with_selected" defaultValue={this.getTranformDataValue("replace_values_with_selected")} onInput={this.pickValue} disabled>
                  <option value="" > None</option>
                  <option value="mean">Mean</option>
                  <option value="median">Median</option>
                  <option value="mode" >Mode</option>
                </select>
              </div>
            </div>
              <div class="row form-group">
                <div class="col-md-5 col-sm-5">
                  <div class="ma-checkbox inline">
                    <input id="feature_scaling" name="feature_scaling" type="checkbox" defaultChecked={this.getTranformDataValue("feature_scaling")} class="needsclick" onInput={this.pickValue}/>
                    <label for="feature_scaling">Feature Scaling:</label>
                  </div>
                </div>
                <div class="col-md-4 col-sm-4">
                  <select class="form-control" id="perform_standardization_select"   name="perform_standardization_select" defaultValue={this.getTranformDataValue("perform_standardization_select")} onInput={this.pickValue} disabled>
                    <option value=""> None</option>
                    <option value="normalization">Normalization</option>
                    <option value="standardization">Standardization</option>
                  </select>
                </div>
              </div>
              <div class="row form-group">
                <div class="col-md-5 col-sm-5">
                  <div class="ma-checkbox inline">
                    <input id="variable_transformation" name="variable_transformation" defaultChecked={this.getTranformDataValue("variable_transformation")} type="checkbox" class="needsclick" onInput={this.pickValue}/>
                    <label for="variable_transformation">Variable Transformation:</label>
                  </div>
                </div>
                <div class="col-md-4 col-sm-3">
                  <select class="form-control" id="variable_transformation_select" name="variable_transformation_select" defaultValue={this.getTranformDataValue("variable_transformation_select")} onInput={this.pickValue} disabled>
                  <option value=""> None</option>
                    <option value="log_transform"> Log</option>
                    <option value="square_root_transform">Square root</option>
                    <option value="cube_root_transform">Cube root</option>
                    <option value="modulus_transform" > Modulus</option>
                  </select>
                </div>
              </div>
          </form>
        </div>
      );
    }
    else if(this.props.selectedItem.columnType == "dimension"){
      return (
        <div class="modal-body">
          <h4>What would you like to do with {this.props.selectedItem.name} column?</h4>
          <p>Please select any of the options provided below that will help in transforming the chosen column into multiple new features.
            Each option will create an additional feature derived out of the original column.</p>
          <hr />
          <form class="form_withrowlabels" id="binsForm">
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="encoding_dimensions" name="encoding_dimensions" type="checkbox" defaultChecked={this.getTranformDataValue("encoding_dimensions")} class="needsclick" onInput={this.pickValue}/>
                  <label for="encoding_dimensions">Perform Encoding:</label>
                </div>
              </div>
              <span className="inline">
              <div class="col-md-7 col-sm-6">
                <div class="ma-checkbox inline oneHot disabled" id="oneHot">
                  <input type="radio" id="one_hot_encoding" name="encoding_type"  value="one_hot_encoding"  defaultChecked={this.getTranformDataValue("encoding_type") === "one_hot_encoding" } onInput={this.pickValue}/>
                  <label for="one_hot_encoding">One hot encoding</label>
                </div>
                <div class="ma-checkbox inline labelEncode disabled" id="labelEncode">
                  <input type="radio" id="label_encoding" name="encoding_type"  value="label_encoding" defaultChecked={this.getTranformDataValue("encoding_type") === "label_encoding"} onInput={this.pickValue}/>
                  <label for="label_encoding">Label encoding</label>
                </div>
              </div>
            </span>
            </div>

            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="return_character_count" name="return_character_count" type="checkbox" defaultChecked={this.getTranformDataValue("return_character_count")} class="needsclick" onInput={this.pickValue}/>
                  <label for="return_character_count">return Character Count</label>
                </div>
              </div>
            </div>
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="is_custom_string_in" name="is_custom_string_in" type="checkbox" defaultChecked={this.getTranformDataValue("is_custom_string_in")} class="needsclick" onInput={this.pickValue}/>
                  <label for="is_custom_string_in">Is custom string in:</label>
                </div>
              </div>
              <div class="col-md-3 col-sm-3">
                <input type="text" id="is_custom_string_in_input" name="is_custom_string_in_input" class="form-control" placeholder="Please Type" defaultValue={this.getTranformDataValue("is_custom_string_in_input")} onInput={this.pickValue} disabled/>
              </div>
            </div>
          </form>
        </div>
      );
    }
    else{
      return (
        <div class="modal-body">
          <h4>What would you like to do with {this.props.selectedItem.name} column?</h4>
          <p>Please select any of the options provided below that will help in transforming the chosen column into multiple new features.
            Each option will create an additional feature derived out of the original column.</p>
          <hr/>
          <form class="form_withrowlabels" id="binsForm">
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="is_date_weekend" name="is_date_weekend" type="checkbox" defaultChecked={this.getTranformDataValue("is_date_weekend")} class="needsclick" onInput={this.pickValue}/>
                  <label for="is_date_weekend">Is Date Weekend or Not?</label>
                </div>
              </div>
            </div>
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="extract_time_feature" name="extract_time_feature" type="checkbox" defaultChecked={this.getTranformDataValue("extract_time_feature")} class="needsclick" onInput={this.pickValue}/>
                  <label for="extract_time_feature">Extract Time Feature:</label>
                </div>
              </div>
              <div class="col-md-4 col-sm-3">

                <select class="form-control" id="extract_time_feature_select" name="extract_time_feature_select" defaultValue={this.getTranformDataValue("extract_time_feature_select")} onInput={this.pickValue} disabled>
                  <option value="" selected> None</option>
                  <option value="day_of_week" >Day of week</option>
                  <option value="month_of_year">Month of Year</option>
                </select>
              </div>
            </div>
            <div class="row form-group">
              <div class="col-md-5 col-sm-5">
                <div class="ma-checkbox inline">
                  <input id="time_since" name="time_since" type="checkbox" defaultChecked={this.getTranformDataValue("time_since")} class="needsclick" onInput={this.pickValue}/>
                  <label for="time_since">Time Since Some Event:</label>
                </div>
              </div>
              <div class="col-md-4 col-sm-3">
                <input type="date" name="time_since_input" id="time_since_input" class="form-control" placeholder="Please Type" defaultValue={this.getTranformDataValue("time_since_input")} onInput={this.pickValue} disabled/>
              </div>
            </div>
          </form>
        </div>
      );
    }
  }
}
