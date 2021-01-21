import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import {getSignalAnalysis} from "../../actions/signalActions";
import renderHTML from 'react-render-html';
import HeatMap from '../../helpers/heatmap';
import {NORMALTABLE,CONFUSIONMATRIX,HEATMAPTABLE,CIRCULARCHARTTABLE,DECISIONTREETABLE,TEXTHEATMAPTABLE,POPUPDECISIONTREETABLE} from "../../helpers/helper";
import {CircularChartTable} from "./CircularChartTable";
import {ConfusionMatrix} from "./ConfusionMatrix";
import {DecisionTreeTable} from "./decisionTreeTable";
import {HeatMapTable} from "./heatmap";
import {TextHeatMapTable} from "./TextHeatMapTable";
import {NormalTable} from "./NormalTable";
import {PopupDecisionTreeTable} from "./PopupDecisionTreeTable";
import {NormalHideColumn} from "./NormalHideColumn";

export class CardTable extends React.Component {
	constructor(){
		super();
	}

	render() {
		var element = this.props.jsonData;
		let tableEle = "";
		var tableCls = "";
		if(element.tableType == CIRCULARCHARTTABLE){
			tableCls = "text-center tbl_th_center";
			tableEle =  <CircularChartTable  tableData={element} />;
		}
		if(element.tableType == CONFUSIONMATRIX){
			tableEle = <ConfusionMatrix tableData={element}/>;
		}
		if(element.tableType == DECISIONTREETABLE){
			tableEle = <DecisionTreeTable tableData={element}/>;
		}
		if(element.tableType == HEATMAPTABLE){
			tableEle = <HeatMapTable classId={this.props.classId} tableData={element}/>;
		}
		if(element.tableType == TEXTHEATMAPTABLE){
			tableEle = <TextHeatMapTable tableData={element}/>;
		}if(element.tableType == NORMALTABLE){
			tableEle = <NormalTable classId={this.props.classId} tableData={element}/>;
		}
		if(element.tableType == POPUPDECISIONTREETABLE){
            tableEle = <PopupDecisionTreeTable  tableData={element}/>;
        }
		if(element.tableType == "normalHideColumn"){
            tableEle = <NormalHideColumn tableData={element}/>;
        }
		return (
				<div className={tableCls}>
				{tableEle}
				</div>
		);
	}
}
