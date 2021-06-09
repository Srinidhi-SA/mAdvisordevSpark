import React from "react";
import {setDateFormatHelper} from "../../helpers/helper";
export class DetailOverlay extends React.Component {
  constructor(props){
    super(props);
  }

  getValues(displayName,value){
	  return <p className="overlayTooltip">{displayName}&nbsp;:&nbsp;{value}</p>
  }
  getDateValues(displayName,value){
	  value = setDateFormatHelper(value);
    return <p className="overlayTooltip">{displayName}&nbsp;:&nbsp;{value}</p>
  }
  getAnalysisValues(value){
	  value = value.map((key,index) =>{
		  return( <li key={index}><i class="fa fa-check"></i>&nbsp;&nbsp;{key}</li>);
	  })
    let analysisList = <ul class="list-unstyled">{value}</ul>;
    return <div className="overlayTooltip">
        <div class="text-primary">List Of Signals</div>
        {analysisList}
      </div>
  }
  render() {
    var details = this.props.details.brief_info;
    let templateList = "";
    let template = {};
    if(typeof details!="undefined"){
      template = details.map((key,index) =>{
	      if(key.name == "analysis list"){
		      templateList = this.getAnalysisValues(key.value)
	      }else if(key.name == "updated_at"){
		      templateList = this.getDateValues(key.displayName,key.value)
	      }else{
		      templateList = this.getValues(key.displayName,key.value)
	      }

        if(index == 1 || index == 3 )
	        return(<div key={index}>{templateList}<hr className="hr-popover"/></div>);
	      else
      	  return( <div key={index}>{templateList}</div>);
      })
    }
    return (
      <div id="myPopover" >
        {(template.length>0)?template:<div>Details cannot be loaded.</div>}
      </div>
    );
  }
}
