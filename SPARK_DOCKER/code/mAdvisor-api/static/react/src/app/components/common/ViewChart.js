import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import {Modal,Button} from "react-bootstrap";
import {showZoomChart} from "../../actions/signalActions";
import renderHTML from 'react-render-html';
import { Scrollbars } from 'react-custom-scrollbars';
import {downloadSVGAsPNG} from '../../helpers/helper';
import {API} from "../../helpers/env";
import { C3ChartNew } from "../C3ChartNew";

@connect((store) => {
    return {login_response: store.login.login_response,
        signal: store.signals.signalAnalysis,
        modelSummaryFlag:store.apps.modelSummaryFlag,
        viewChartFlag:store.signals.viewChartFlag,
        viewChartClassId:store.signals.chartClassId,
    };
})

export class ViewChart extends React.Component {

    constructor(props){
        super(props);
    }
    openCloseZoomChart(flag){
        this.props.dispatch(showZoomChart(flag,""));
    }
    shouldComponentUpdate(){
        if(store.getState().signals.chartClassId == this.props.classId)
            return true;
        else if(store.getState().signals.chartClassId == "")return true;
        else return false;
    }

    render() {
        var imgDetails = "c3ChartScroll"+this.props.classId;
        return(
            <Modal show={store.getState().signals.viewChartFlag} backdrop="static" onHide={this.openCloseZoomChart.bind(this,false)} dialogClassName={(this.props.chartData.data.type === "pie"|| this.props.chartData.data.type === "donut")?"modal-colored-header modal-lg-chart":"modal-colored-header modal-lg"}>
                <Modal.Header closeButton>
                    <h3 className="modal-title">View Chart</h3>
                </Modal.Header>
                <Modal.Body className="viewChartPopup">
                    <Scrollbars className="thumb-horizontal" autoHeight autoHeightMin={200} autoHeightMax={500}  >
                        <C3ChartNew classId={imgDetails} data={this.props.chartData} xdata={this.props.xdata} yformat={this.props.yformat} y2format={this.props.y2format} tabledata={this.props.tabledata}/>
                    </Scrollbars>
                </Modal.Body>
            </Modal>
        );
    }

}
