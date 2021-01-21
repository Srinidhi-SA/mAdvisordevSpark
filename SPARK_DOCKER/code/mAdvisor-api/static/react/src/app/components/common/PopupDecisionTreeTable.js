import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import store from "../../store";
import {getSignalAnalysis,handleDecisionTreeTable} from "../../actions/signalActions";
import renderHTML from 'react-render-html';
import {openDTModalAction} from "../../actions/dataActions"
import {MAXTEXTLENGTH} from "../../helpers/helper";
import {DecisionTree} from "../common/DecisionTree";


@connect((store) => {
    return { selPrediction: store.signals.selectedPrediction};
  })
//Used in Score Summary Table
export class PopupDecisionTreeTable extends React.Component {
  constructor(props){
    super(props);

  }
  // showDecisionTreePopup(rule){
  //    bootbox.alert({title: "Prediction Rule",
  //            message: rule});
  // }
  showDecisionTreePopup =(rule,path)=>{
  this.props.dispatch(openDTModalAction(rule,path));
 }
  componentDidMount(){
      handleDecisionTreeTable();
  }
  componentDidUpdate(){
      handleDecisionTreeTable();
      }

  generatePredTableHeaders(table) {
      var cols = table.tableData.map(function(rowData,i){
          var colLength = rowData.length;
        if(i== 0){
            return rowData.map(function(colData,j) {
              let classForNoSort=" sorter-false"
              let classHidden="hidden"
              let classCenter="text-center"
              let classStyle=""
              if(!(colData=="Probability"||colData=="Freq")){
                classHidden+=classForNoSort,
                classCenter+=classForNoSort,
                classStyle+=classForNoSort
              }

                if(j > 3)return <th className={classHidden} key={j}>{colData}</th>
                else if(j == 0) return <th className={classStyle}  style={{width:"60%"}}  key={j}>{colData}</th>;
                else return <th class={classCenter} key={j}>{colData}</th>;
                 });
        }
      })
    return cols;
  }
generateDecisionTreeRows(table) {
    var that = this;
      var tbodyData = table.tableData.map(function(rowData,i){
          var colLength = rowData.length;
          if(i != 0){
              var rule = rowData[rowData.length-1]
              var path = rowData[rowData.length-2]
              var rows = rowData.map(function(colData,j) {

                   if(j == 0){
                       return<td key={j} className="cursor">{renderHTML(colData.length > MAXTEXTLENGTH ? colData.slice(0, MAXTEXTLENGTH).concat("...") : colData)}</td>;
                   }
                      else if(j > 3)return  <td class="hidden" key={j}>{colData}</td>
                      else return  <td class="text-center" key={j}>{colData}</td>

              });
              return<tr key={i}>{rows}<td class="cursor text-center" onClick={that.showDecisionTreePopup.bind(this,rule,path)}><a data-toggle="modal" class="btn btn-space btn-default btn-round btn-xs"><i class="fa fa-info"></i></a></td></tr>;
          }
        })
      return tbodyData;
      }

      callTableSorter() {
        $(function() {
          $('#sorter').tablesorter({
            theme: 'ice',
            headers: {
              0: {
                sorter: false
              }
            },
            sortList: [[1,1]]
          });
        });
      }

  render() {
   var data = this.props.tableData;
   var className = "table table-bordered popupDecisionTreeTable"
   var headerComponents = this.generatePredTableHeaders(data);
   var rowComponents = this.generateDecisionTreeRows(data);

   this.callTableSorter()
   return (
           <div class="table-style_2">
             <DecisionTree/>
           <table id="sorter" className={className}>
               <thead><tr>{headerComponents}<th className="sorter-false" width="2%">Details</th></tr></thead>

               <tbody>{rowComponents}</tbody>

           </table>
           </div>
       );
  }
}
