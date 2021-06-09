import React from "react";
import { connect } from "react-redux";
import {handleDecisionTreeTable} from "../../actions/signalActions";
import renderHTML from 'react-render-html';
import {openDTModalAction} from "../../actions/dataActions"
import {MAXTEXTLENGTH} from "../../helpers/helper";
import {DecisionTree} from "../common/DecisionTree";
@connect((store) => {
    return { 
      dtModelShow:store.datasets.dtModelShow,
      dtName:store.datasets.dtName,
    };
  })

export class PopupDecisionTreeTable extends React.Component {
  constructor(props){
    super(props);
  }
  showDecisionTreePopup =(rule,path,name)=>{
    this.props.dispatch(openDTModalAction(rule,path,name));
  }
  componentDidMount(){
    handleDecisionTreeTable();
  }
  componentDidUpdate(){
    handleDecisionTreeTable();
  }

  generatePredTableHeaders(table) {
    var cols = table.tableData.map(function(rowData,i){
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
          if(j > 3)
            return <th className={classHidden} key={j}>{colData}</th>
          else if(j == 0) 
            return <th className={classStyle}  style={{width:"60%"}}  key={j}>{colData}</th>;
          else 
            return <th class={classCenter} key={j}>{colData}</th>;
        });
      }
    })
    return cols;
  }

  generateDecisionTreeRows(table) {
    var that = this;
    var tbodyData = table.tableData.map(function(rowData,i){
      if(i != 0){
        var rule = rowData[rowData.length-1]
        var path = rowData[rowData.length-2]
        var rows = rowData.map(function(colData,j) {
          if(j == 0){
            return <td key={j} className="cursor">{renderHTML(colData.length > MAXTEXTLENGTH ? colData.slice(0, MAXTEXTLENGTH).concat("...") : colData)}</td>;
          }else if(j > 3)
            return  <td class="hidden" key={j}>{colData}</td>
          else 
            return  <td class="text-center" key={j}>{colData}</td>
        });
        return<tr key={i}>{rows}<td class="cursor text-center" onClick={that.showDecisionTreePopup.bind(this,rule,path,that.props.tableData.name)}><a data-toggle="modal" class="btn btn-space btn-default btn-round btn-xs"><i class="fa fa-info"></i></a></td></tr>;
      }
    })
    return tbodyData;
  }

  callTableSorter() {
    let clsName = this.props.tableData.name!=undefined?this.props.tableData.name.replace(/ +/g, ""):""
    $(function() {
      let len = document.querySelectorAll("#sorter").length
      if(len===1){
        $("#sorter").tablesorter({
          theme: 'ice',
          headers: { 0: { sorter: false} },
          sortList: [[1,1]]
        });
      }else{
        for(let i=0;i<len;i++){
          if(document.querySelectorAll("#sorter")[i].className.includes(clsName)){
            $("#sorter."+clsName).tablesorter({
              theme: 'ice',
              headers: { 0: { sorter: false } },
              sortList: [[1,1]]
            });
          }
        }
      }
    });
  }

  render() {
    var data = this.props.tableData;
    var className = (data.name!=undefined)? `table table-bordered popupDecisionTreeTable ${data.name.replace(/ +/g, "")}` : "table table-bordered popupDecisionTreeTable"
    this.callTableSorter()
    let dtFlag = false;
    if(this.props.dtModelShow && this.props.dtName===data.name){
      dtFlag = true
    }else if(this.props.dtModelShow && this.props.dtName===""){
      dtFlag = true
    }
    return (
      <div class="table-style_2">
        {dtFlag?<DecisionTree/>:""}
        <table id="sorter" className={className}>
          <thead>
            <tr>
              {this.generatePredTableHeaders(data)}
              <th className="sorter-false" width="2%">Details</th>
            </tr>
          </thead>
          <tbody>{this.generateDecisionTreeRows(data)}</tbody>
        </table>
      </div>
    );
  }
}
