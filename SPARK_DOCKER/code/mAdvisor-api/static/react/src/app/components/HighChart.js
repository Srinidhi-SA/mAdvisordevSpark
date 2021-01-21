import React from "react";
import store from "../store";
import {connect} from "react-redux";
import Highcharts from "highcharts";
import ReactHighstock from "react-highcharts/ReactHighstock";
import { showChartData } from "../actions/signalActions";
import {ViewChartData} from "./common/ViewChartData";
import { API } from "../helpers/env";

@connect((store) => {
    return {

    };
  })

export class HighChart extends React.Component {
    constructor(props) {
        super(props);
        this.tableDownload = "";
        this.modalCls = "modal fade chart-modal" + props.classId;
        this.tableCls = "table-responsive table-area table" + props.classId;
        this.chartData = "";
        this.classId = "chart" + this.props.classId + " ct col-md-7 col-md-offset-2 xs-mb-20";
    }

    openZoomChart(flag) {
        this.props.dispatch(showZoomHighChart(flag, this.props.classId));
    }

    openChartData(flag) {
        this.props.dispatch(showChartData(flag,this.props.classId));
    }

    downloadSVG(){
        saveSvgAsPng(document.getElementsByClassName("highChartArea")[0].children[0].children[0].children[0], "Stock Performance Analysis.png", {
            backgroundColor: "white",
            height: "500"
          });
    }

    render(){
        if (this.props.tabledownload) {
            this.tableDownload = API + this.props.tabledownload;
        }
        let chartData = this.props.data;
        var axesList = [];
        for(let i=0;i<chartData.data.columns.length;i++){
            if(chartData.data.columns[i][0] != "date"){
                axesList.push({});
                let j=1;
                let array1 = []
                axesList[axesList.length-1].color=chartData.color.pattern[i+1]
                axesList[axesList.length-1].name=chartData.data.columns[i][0];
                axesList[axesList.length-1].id="series"+(axesList.length-1);
                axesList[axesList.length-1]["data"]=[];
                // axesList[axesList.length-1]["yAxis"]=axesList.length-1;          //Creates multiple y axis lines
                for(j=1;j<chartData.data.columns[i].length;j++){
                    axesList[axesList.length-1]["data"].push([Date.parse(this.props.xdata[j-1]),chartData.data.columns[i][j]])
                    array1.push(chartData.data.columns[i][j])
                }
                axesList[axesList.length-1].high = Date.parse(this.props.xdata[array1.indexOf(Math.max(...array1))])
                axesList[axesList.length-1].low = Date.parse(this.props.xdata[array1.indexOf(Math.min(...array1))])
            }
        }

        let getAxesList = []
        let flagList = []
        for(let i=0;i<axesList.length;i++){
            flagList.push({});
                flagList[i].type="flags";
                flagList[i].onSeries="series"+i;
                flagList[i].shape="squarepin";
                flagList[i].states={}
                // flagList[i].states.hover.fillColor="#395c84"
                flagList[i].data=[];
                flagList[i].data[0] = {};
                flagList[i].data[1] = {};

                flagList[i].data[0]["x"] = axesList[i].high;
                flagList[i].data[0]["title"]="H"+(i+1);
                flagList[i].data[0]["text"]="High";

                flagList[i].data[1]["x"] = axesList[i].low;
                flagList[i].data[1]["title"]="L"+(i+1);
                flagList[i].data[1]["text"]="Low";          
        }
        getAxesList = axesList.concat(flagList)

        let getYAxis = [];
        getYAxis.push({});
        getYAxis[0].opposite=false;
        getYAxis[0].min=0;
        getYAxis[0].crosshair = {};
        getYAxis[0].crosshair.width = 2;
        getYAxis[0].crosshair.color = "#80bdf3";
        getYAxis[0].title = {};
        getYAxis[0].title.text = chartData.axis.y.label.text;
        getYAxis[0].title.offset = 40;
        getYAxis[0].title.style = {}
        getYAxis[0].title.style.fontSize = "13px"
        
        for(let i=1;i<axesList.length;i++){
            getYAxis.push({});
            // getYAxis[0].visible= false;
            getYAxis[i].crosshair = {};
            getYAxis[i].crosshair.width = 2;
            getYAxis[i].crosshair.color = "#80bdf3";
        }
        //To be added for bar chart
        // resize: { enabled: false },
        // height: '80%',
        // {
        //     labels: { enabled: false },
        //     top:"80%",
        //     height: '20%',
        // }

        const config = {
            chart: { type: "spline" },
            credits: { enabled: false },
            title: { text: chartData.title.text },
            // navigator: { enabled: false },
            scrollbar: { enabled: false },
            legend : chartData.legend.show,
            rangeSelector: {
                inputEnabled:false,
                buttons: [
                    { type: 'month',count: 1,text: '1m' },
                    { type: 'month',count: 3,text: '3m' },
                    { type: 'all',text: 'All'}
                ],
                buttonTheme: {
                    fill: "none",
                    r:4,
                    style: { color: "#32b5a6", fontWeight: 'bold' },
                    states: {
                        select: {
                            fill: "#32b5a6",
                            style: { color: "white" }
                        }
                    }
                }
            },
            xAxis: {
                type: 'datetime',
                align: "left",
                labels:{ format:"{value:%d %b \'%y}" },
                crosshair : { width:2, color:"#80bdf3" },
                title: { 
                    text: "<span style=color:#333333>"+chartData.axis.x.label.text+"</span>",
                    style: { fontSize:"13px" },
                    offset: 40,
                },
            },
            yAxis: getYAxis,
            tooltip: {
                useHTML: true,
                headerShape: 'callout',
                style:{fontSize:"12px"},
                backgroundColor: "white",
                formatter: function() {
                    if(this.series != undefined){
                        var htmlTip = ""
                        for(let i=0;i<this.series.userOptions.data.length;i++){
                            if(this.series.userOptions.data[i].x === this.x){
                                htmlTip = "<span>"+Highcharts.dateFormat('%B %e, %Y', this.x) +"</br>"+this.series.userOptions.data[i].text+" :"+this.y+"</span>"
                            }
                        }
                        return htmlTip;
                    }
                    else{
                        var htmlTip = "<table class='tooltip-table'><thead><tr class='text-center'><th colspan=4>"+ Highcharts.dateFormat('%B %e, %Y', this.x) +"</th></tr></thead><tbody>"
                        $.each(this.points, function(i, point) {
                            htmlTip = htmlTip+"<tr><td><span style=color:" + point.color + ">\u25FC</span></td><td>"+ point.series.name+"</td><td> |  </td> <td>"+point.y +"</td></tr>" ;
                        });
                        htmlTip = htmlTip +"</tbody></table>"
                        return htmlTip;
                    }
                }
            },
            plotOptions :{
                series:{
                    color:"#0fc4b5",
                    marker:{ enabled:false }
                }
            },
            series : getAxesList
        };

        return(
            <div className="chart-area">
                <div className="chart-data-icon">
                    <div class="btn-group pull-right">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                            <i className="fa fa-more-img" aria-hidden="true"></i>
                        </button>
                        <ul role="menu" class="dropdown-menu dropdown-menu-right">
                            <li>
                            <a href="javascript:;" id="button" onClick={this.downloadSVG.bind(this)}>
                                <i class="fa fa-picture-o" aria-hidden="true"></i>&nbsp;
                                Download as PNG</a>
                            </li>
                            <li>
                            <a href="javascript:;" onClick={this.openChartData.bind(this, true)}>
                                <i class="fa fa-eye" aria-hidden="true"></i>&nbsp;
                                View Chart Data</a>
                            </li>
                            <li>
                            <a href={this.tableDownload}>
                                <i class="fa fa-cloud-download" aria-hidden="true"></i>&nbsp;
                                Download Chart Data</a>
                            </li>
                        </ul>
                    </div>
                    <div className="clearfix"></div>
                </div>
                <div id="" className={this.modalCls} role="dialog">
                    <div className="modal-colored-header uploadData modal-dialog ">
                        <ViewChartData tabledata={this.props.tabledata} tableCls={this.tableCls} classId={this.props.classId} tableDownload={this.tableDownload}/>
                    </div>
                </div>
                <div className="highChartArea">
                    <ReactHighstock config={config} constructorType={"chart"} ref={"chart"}/>
                </div>
            </div>
        );
    }
}