import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import {getSignalAnalysis} from "../../actions/signalActions";
import renderHTML from 'react-render-html';
import HeatMap from '../../helpers/heatmap';

export class DecisionTreeTable extends React.Component {
  constructor(){
    super();
  }
  componentDidMount() {
    
  }
//currently not using , present in old version
  render() {
   var element = this.props.tableData.tableData;
 
  let renderTableThead = element[0].map((item,i)=>{
	return(
        <th>{item}</th>
	  );

});

   
   var trs=[];
   for (var i=1;i<element.length;i++){
	   let trElement = element[i], tdElement = element[i][1], len=element[i][1].length;
	  // alert(len);
	  //  var renderTableTbody = trElement.map(function(item,index){
			trs[i] = tdElement.map(function(subItem,index){
				 if(index==0){
					 return(
					    <tr>
						   <td rowSpan={len}>{element[i][0]}</td>
						   <td>{element[i][1][index]}</td>
						   <td>{element[i][2][index]}</td>
						</tr>
					 );
					 
				 }else{
					 return(
					    <tr>
						   <td>{element[i][1][index]}</td>
						   <td>{element[i][2][index]}</td>
						</tr>
					 );
					 
				 }
			});
			
		//});
	   
   }// end of for loop
   

   



      return(
              <div className="table-style">
        <table className="table table-bordered idDecisionTreeTable">
               <thead><tr> {renderTableThead}</tr></thead>
               <tbody>{trs}</tbody>
         </table>
         </div>

    );

  }
}
