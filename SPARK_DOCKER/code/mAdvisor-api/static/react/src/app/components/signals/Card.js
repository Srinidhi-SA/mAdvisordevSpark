import React from "react";
import {connect} from "react-redux";
import {pickToggleValue} from "../../actions/signalActions";
import {HighChart} from "../HighChart"
import {CardHtml} from "./CardHtml";
import {CardTable} from "../common/CardTable";
import {PredictionDropDown} from "../common/predictionDropdown";
import { Scrollbars } from 'react-custom-scrollbars';
import {GaugeMeter} from "../common/GaugeMeter";
import {DataBox} from "../common/DataBox";
import {WordCloud} from "../common/WordCloud";
import $ from "jquery";
import {ModelSummeryButton} from "../common/ModelSummeryButton";
import {D3ParallelChartt} from "../D3ParallelChartt";
import { C3ChartNew } from "../C3ChartNew";
import { STATIC_URL } from "../../helpers/env";
import { setLoaderFlagAction } from "../../actions/appActions";

var cardData = {};

@connect((store) => {
    return {
        signal: store.signals.signalAnalysis,
        currentAppDetails: store.apps.currentAppDetails,
        toggleValues: store.signals.toggleValues,
        chartLoaderFlag:store.apps.chartLoaderFlag,
        mmLoaderFlag:store.signals.mmLoaderFlag,
    };
})

export class Card extends React.Component {
    constructor() {
        super();

    }
    componentDidMount() {
	  if(this.props.currentAppDetails&&this.props.currentAppDetails.app_type&&this.props.currentAppDetails.app_type == "REGRESSION")
      $('#box0').parent('div').addClass('text-center');
    }
    showMore(evt){
        evt.preventDefault();
        $.each(evt.target.parentElement.querySelectorAll(".paramList"),function(k1,v1){
            $.each(v1.children,function(k2,v2){
                if(v2.className == "modelSummery hidden"){
                    v2.className = "modelSummery";
                }
                else if(v2.className == "modelSummery"){
                    v2.className = "modelSummery hidden";
                }
            })
        });
        if(evt.target.innerHTML == "Show More"){
            evt.target.innerHTML = "Show Less";
        }else{
            evt.target.innerHTML = "Show More";
        }
    }
    handleCheckBoxEvent(event){
        this.props.dispatch(pickToggleValue(event.target.id, event.target.checked));
        if (this.props.toggleValues[event.target.id] == true) {
            $(".toggleOff").removeClass("hidden");
            $(".toggleOn").addClass("hidden")
          } else {
            $(".toggleOn").removeClass("hidden");
            $(".toggleOff").addClass("hidden")
          }
    }
    calculateWidth(width){
        let colWidth  = parseInt((width/100)*12)
        let divClass="col-md-"+colWidth;
        return divClass;
    }
    renderCardData(cardData,toggleTable,cardWidth){
        let that = this;
        var htmlData = cardData.map((story, i) => {
            let randomNum = Math.random().toString(36).substr(2,8);
            switch (story.dataType) {
            case "html":
                if(!story.hasOwnProperty("classTag"))story.classTag ="none";
                if(story.data!="" || story.data!=undefined)
                    return (<CardHtml key={randomNum} htmlElement={story.data} type={story.dataType} classTag={story.classTag}/>);
                else
                    return ""
                break;
            case "c3Chart":
                let chartInfo=[]
                if(!$.isEmptyObject(story.data) && !$.isEmptyObject(story.data.chart_c3) ){
                   if(story.chartInfo){
                     chartInfo=story.chartInfo
                   }
                    if(story.widthPercent &&  story.widthPercent != 100){
                        let width  = parseInt((story.widthPercent/100)*12)
                        let divClass="col-md-"+width;
                        let sideChart=false;
                        if(story.widthPercent < 50)sideChart=true;
                        return (<div key={randomNum} class={divClass}><C3ChartNew chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div>);
                    }else if(story.widthPercent == 100){
                        let divClass="";
                        let parentDivClass = "col-md-12";
                        if(!cardWidth || cardWidth > 50)
                        divClass = "col-md-8 col-md-offset-2"
                        else
                        divClass = "col-md-12";
                        let sideChart=false;

                        if(window.location.pathname.includes("apps-stock-advisor"))
                            divClass = "col-md-7 col-md-offset-2"
                        if(story.data.chart_c3.title.text === "Stock Performance Analysis"|| story.data.chart_c3.title.text === "Stock Price Trend")
                            return (<div key={randomNum} className={parentDivClass}><div class={divClass} ><HighChart chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div></div>);
                        else if(window.location.pathname.includes("\modelManagement")){
                            return(
                                <div key={randomNum} className={parentDivClass} style={{height:"350px"}}>
                                    {that.props.mmLoaderFlag && 
                                        <div style={{position:"absolute",display:"flex",alignItems:"center"}}>
                                            <img src={STATIC_URL+"assets/images/loaderChart.gif"} style={{padding:"175px 200px"}}></img>
                                        </div>
                                    }
                                    <div class={divClass} style={{display:(that.props.mmLoaderFlag?"none":"inline-block")}}>
                                        <C3ChartNew chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/>
                                        <div className="clearfix"/>
                                    </div>
                                </div>
                            );
                        }
                        else
                            return (<div key={randomNum} className={parentDivClass}><div class={divClass} ><C3ChartNew chartInfo={chartInfo} sideChart={sideChart} classId={randomNum}  widthPercent = {story.widthPercent} data={story.data.chart_c3}  yformat={story.data.yformat} y2format={story.data.y2format} guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div></div>);
                    }else{
                        let parentDivClass = "col-md-12";
                        return (<div className={parentDivClass}><div key={randomNum}><C3ChartNew chartInfo={chartInfo} classId={randomNum} data={story.data.chart_c3} yformat={story.data.yformat} y2format={story.data.y2format}  guage={story.data.gauge_format} tooltip={story.data.tooltip_c3} tabledata={story.data.table_c3} tabledownload={story.data.download_url} xdata={story.data.xdata}/><div className="clearfix"/></div></div>);
                    }
                }else{
                    return ""
                }
                break;
            case "table":
                if(!story.tableWidth)story.tableWidth = 100;
                var colClass= this.calculateWidth(story.tableWidth)
                colClass = colClass;
                if(story.data.tableData!=undefined && story.data.tableData.length!=0)
                    return (<div className={colClass} key={randomNum}><CardTable classId={toggleTable} jsonData={story.data} type={story.dataType}/></div>);
                else
                    return ""
                break;
            case "dropdown":
                if(story.data.length!=0 && story.data!=undefined)
                    return (<PredictionDropDown key={randomNum} label={story.label} dropdownName={story.dropdownName!=undefined?story.dropdownName:""} jsonData={story.data} type={story.dataType}/>);
                else
                    return ""
                break;
            case "gauge":
                return (<GaugeMeter key={randomNum} jsonData={story.data} type={story.dataType}/>);
                break;
            case "dataBox":
                if(story.data.length!=0 && story.data!=undefined)
                    return (<DataBox key={randomNum} jsonData={story.data} type={story.dataType}/>);
                else
                    return ""
                break;
            case "wordCloud":
                if(story.data.length!=0 && story.data!=undefined)
                    return (<WordCloud key={randomNum} jsonData={story.data} type={story.dataType}/>);
                else
                    return ""
                break;
            case "toggle":
                if(!$.isEmptyObject(story.data) && story.data!=undefined){
                    var varId = story.data.toggleon.data.tableData[0][0];
                    if(this.props.toggleValues[varId] == true){
                        var toggleClass = "toggleOn hidden"
                        var toggleClass1 = "toggleOff"
                    }
                    else{
                        var toggleClass = "toggleOn"
                        var toggleClass1 = "toggleOff hidden"
                    }
                    var tableData = [];
                    tableData.push(story.data.toggleon);
                    var toggleData =  this.renderCardData(tableData,toggleClass);
                    tableData = [];
                    tableData.push(story.data.toggleoff);
                    var toggleData1 = this.renderCardData(tableData,toggleClass1);                    
                    if(this.props.toggleValues[varId] == true)
                        var idchecked = true
                    else if(this.props.toggleValues[varId] == false)
                        var idchecked = false
                    else
                        var idchecked = false
                    var inputChk =  <div className="switch-button switch-button-yesno col-md-1 col-md-offset-11">
                                        <input type="checkbox" id={varId} name={varId} value={varId} defaultChecked={idchecked} onChange={this.handleCheckBoxEvent.bind(this)} />
                                        <span><label for={varId}></label></span>
                                    </div>
                    return (<div key={varId}>{inputChk}{toggleData}{toggleData1}</div>);
                }else
                    return ""
                break;
            case "kpi":
                let boxData = story.data;
                let divClass = "text-center";
                if(story.widthPercent &&  story.widthPercent != 100){
                    divClass="col-md-4 bgStockBox";
                }
                if(!$.isEmptyObject(story.data))
                    return(
                        <div key={i}className={divClass}>
                            <h3 className="text-center xs-m-0">{boxData.value}<br/>
                                <small>{boxData.text}</small>
                            </h3>
                        </div>
                    );
                else
                    return ""
            break;
            case "button":
                if(!$.isEmptyObject(story.data) && !$.isEmptyObject(story.data.chart_c3))
                    return (<ModelSummeryButton key={randomNum} data={story.data.chart_c3} tabledownload={story.data.download_url} classId={randomNum} type={story.dataType}/>);
                else
                    return ""
                break;
            case "parallelCoordinates":
            return(<D3ParallelChartt key={randomNum} data={story.data} hideColumns={story.hideColumns} hideaxes={story.ignoreList} id={this.props.id} evaluationMetricColName={story.evaluationMetricColName} columnOrder={story.columnOrder}/>);
            break;
            }

        });
        return htmlData;
    }
    render() {
        cardData = this.props.cardData;
		let stockClassName = "";
        if(window.location.pathname.includes("\modelManagement"))
            stockClassName = "col-md-12"
        if(cardData[0].data!=undefined && cardData[0].data === "<h4><center>Algorithm Parameters </center></h4>")
            stockClassName = "algoParams"
		if (window.location.pathname.indexOf("apps-stock-advisor")>-1)
		    stockClassName = "stockClassName";
        let cardWidth = this.props.cardWidth;
        const cardElements = this.renderCardData(cardData,'',cardWidth);
        var isHideData = $.grep(cardData,function(val){
            return(val.dataType == "html" && val.classTag == "hidden");
        });
        return (
            stockClassName === "algoParams"?
                <div className={stockClassName}>
                    {cardElements[0]}
                    <Scrollbars autoHeight autoHeightMin={200} autoHeightMax={330} style={{marginTop:"25px"}}>
                        <div className="paramList">{cardElements.slice(1)}</div>
                        </Scrollbars>
                        {isHideData.length>0?<a href="" onClick={this.showMore.bind(this)}>Show More</a>:""}
                </div>
                :
                <div className = {stockClassName} onLoad={()=>this.props.dispatch(setLoaderFlagAction(false))}>
                { this.props.chartLoaderFlag && 
                    <div style={{display:"flex",height:"400px"}}>
                        <img src={STATIC_URL+"assets/images/Preloader_2.gif"} style={{margin:"auto"}}></img>
                    </div>
                }
                {!this.props.chartLoaderFlag && cardElements}
                </div>
        );

    }
}
