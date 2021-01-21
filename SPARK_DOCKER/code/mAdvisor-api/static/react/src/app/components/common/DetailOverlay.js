import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import renderHTML from 'react-render-html';
import HeatMap from '../../helpers/heatmap';
import {generateHeaders,generateCircularChartRows} from "../../helpers/helper";
var dateFormat = require('dateformat');
//Info of all listing pages
export class DetailOverlay extends React.Component {
  constructor(props){
    super(props);
  }

  getValues(displayName,value,name){
	  return <p className="overlayTooltip">{displayName}&nbsp;:&nbsp;{value}</p>
  }
  getDateValues(displayName,value,name){
	  value = dateFormat(value, "mmm d,yyyy HH:MM");
	 return <p className="overlayTooltip">{displayName}&nbsp;:&nbsp;{value}</p>
  }
  getAnalysisValues(displayName,value,name){
	  value = value.map((key,index) =>{
		  return( <li key={index}><i class="fa fa-check"></i>&nbsp;&nbsp;{key}</li>);
	  })
	 let  analysisList = <ul class="list-unstyled">{value}</ul>;
     return <div className="overlayTooltip">
              <div class="text-primary">List Of Signals</div>
              {analysisList}
            </div>
  }
  render() {
   var details = this.props.details.brief_info;
   let templateList = "";
   let template = {};
   if(typeof details!="undefined")
   {
   template = details.map((key,index) =>{
	  if(key.name == "analysis list"){
		  templateList = this.getAnalysisValues(key.displayName,key.value,key.name)
	  }
	  else if(key.name == "updated_at"){
		  templateList = this.getDateValues(key.displayName,key.value,key.name)
	  }else{
		  templateList = this.getValues(key.displayName,key.value,key.name)
	  }

	 if(index == 1 || index == 3 )
	  return(<div key={index}>{templateList}<hr className="hr-popover"/></div>);
	   else
	  return( <div key={index}>{templateList}</div>);
   })
  }
   return (
		   <div id="myPopover" >
       {
         (template.length>0)?
         (template):(<div>Details cannot be loaded.</div>)
       }
           {/*{template}*/}
         </div>
       );
  }
}
