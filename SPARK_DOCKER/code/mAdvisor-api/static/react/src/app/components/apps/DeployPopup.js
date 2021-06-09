import React from "react";
import { connect } from "react-redux";
@connect(store => {
  return {
    deployData: store.apps.deployData,
    deployItem: store.apps.deployItem
  };
})
export class DeployPopup extends React.Component {
  constructor(props) {
    super(props);
    this.pickValue = this.pickValue.bind(this);
    this.state = {};
  }

  getDeployData() {
    if (this.props.deployData != undefined || this.props.deployData != null) {
      var slugData = this.props.deployData[this.props.deployItem];
      if (slugData != undefined && slugData.depData != undefined) {
        return JSON.parse(JSON.stringify(slugData.depData));
      }
    }
    return {};
  }

  pickValue(event) {
    this.props.parentPickValue("deployData", event);
  }

  onchangeInput(event) {
    return event.target.value;
  }

  render() {
    var depData = this.getDeployData();
    return (
      <div class="modal-body">
        <form>
          <div class="xs-m-20" />
          <div class="row form-group">
            <label for="dname" class="col-sm-4 control-label">
              Deployment name
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="name"
                class="form-control"
                placeholder="Name of the deployment"
                defaultValue={depData.deploytrainer}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>
          <div class="row form-group">
            <label for="dname" class="col-sm-4 control-label">
              Dataset name
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="datasetname"
                class="form-control"
                placeholder="Name of dataset"
                defaultValue={depData.datasetname}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>

          <div class="row form-group">
            <label for="txt_dname" class="col-sm-4 control-label">
              S3 bucket name
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="s3Bucket"
                class="form-control"
                placeholder="s3-Bucket"
                defaultValue={depData.s3Bucket}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>
          <div class="row form-group">
            <label for="txt_dname" class="col-sm-4 control-label">
              Source file name
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="file_name"
                class="form-control"
                placeholder="Name of source file"
                defaultValue={depData.file_name}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>
          <div class="row form-group">
            <label for="txt_dname" class="col-sm-4 control-label">
              Access Key
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="access_key_id"
                class="form-control"
                placeholder="Enter Password"
                defaultValue={depData.access_key_id}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>
          <div class="row form-group">
            <label for="txt_dname" class="col-sm-4 control-label">
              Secret Key
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="secret_key"
                class="form-control"
                placeholder="Enter Password"
                defaultValue={depData.secret_key}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
              />
            </div>
          </div>
          <div class="row form-group">
            <label for="txt_dscoring" class="col-sm-4 control-label">
              Frequency of scoring
            </label>
            <div class="col-sm-8">
              <select
                class="form-control"
                name="timing_details"
                defaultValue={depData.timing_details}
                onChange={this.pickValue}
              ><option value="none">
                  --Select--
                </option>
                <option value="monthly">Monthly</option>
                <option value="weekly">Weekly</option>
                <option value="daily">Daily</option>
              </select>
            </div>
          </div>
          <div class="row form-group">
            <label for="txt_dsrclocation" class="col-sm-4 control-label">
              Target Bucket Name
            </label>
            <div class="col-sm-8">
              <input
                type="text"
                name="bucket"
                class="form-control"
                placeholder="Bucket name"
                defaultValue={depData.bucket}
                onInput={this.pickValue}
                onChange={this.onchangeInput.bind(this)}
                disabled
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}
