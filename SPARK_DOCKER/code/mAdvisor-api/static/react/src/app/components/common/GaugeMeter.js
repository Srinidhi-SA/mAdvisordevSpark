import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import renderHTML from 'react-render-html';
import HeatMap from '../../helpers/heatmap';
import {generateHeaders,generateCircularChartRows} from "../../helpers/helper";
import ReactSpeedometer from "react-d3-speedometer";


export class GaugeMeter extends React.Component {
  constructor(){
    super();
  }
  render() {
   var data = this.props.jsonData;
   return (
          <div className="gauageMeter">
        	    <ReactSpeedometer
        	        minValue={data.min}
        	        maxValue={data.max}
        	        value={data.value}
        	        segments={data.segments}
        	        needleColor="#333"
        	        endColor="#005662"
        	         startColor="#0fc4b5"
        	    />
        	    <label className="guageMeterValue">{data.value}</label>
        	</div>
       );
  }
}
