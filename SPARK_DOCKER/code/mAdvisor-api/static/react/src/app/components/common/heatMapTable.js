import React from "react";
import HeatMap from '../../helpers/heatmap';

export class HeatMapTable extends React.Component {
  constructor(){
    super();
  }
  componentDidMount() {
    HeatMap("heat-table-map");
    $(function(){
      $(".idDecisionTreeTable").each(function () {
        var $tds = $(this).find('td');
        var $divs  =  $tds.eq(1).find('div');
        var $div2  =  $tds.eq(2).find('div');
        for(var j=0;j<$divs.length;j++){
          $($div2[j]).height($($divs[j]).height());
        }
        $($div2[$divs.length-1]).css({"border-bottom":"0px"});
        $($divs[$divs.length-1]).css({"border-bottom":"0px"});
      });
    });
  }

  render() {
    var element = this.props.htmlElement;
    let renderTableThead = element.tableData[0].map((item,i)=>{
      return(
        <tr key={i}>
          <th style="border-bottom: 0px;">{item[0]}</th>
          <th width="70%">{item[1]}</th>
          <th width="10%">{item[2]}</th>
        </tr>
      );
    });

    let renderTableTbody = element.tableData.map((item,i)=>{
      if(i!=0){
        let secondTd =item[1].map((secondItem,secondI)=>{
          return(
            <div key={secondI} style="min-height:20px;padding:8px;overflow-y:auto;border-bottom:1px solid #e6e6e6;width:100%;" id="id_rule_0">
              {secondItem}
            </div>
          );
        });
        let thirdTd =item[1].map((thirdItem)=>{
          return(
            <div style="min-height: 20px; padding: 8px; overflow-y: auto; border-bottom: 1px solid rgb(230, 230, 230); width: 100%; height: 41px;" id="id_prop_0">
              {thirdItem}
            </div>
          );
        });
        return(
          <tr key={i}>
            <td  style="border-top: 0px;">{item[0]}</td>
            <td style="padding:0px;">{secondTd}</td>
            <td style="padding:0px">{thirdTd}</td>
          </tr>
        );
      }
    });

    return(
      <div className="table-style">
        <table className="table table-bordered idDecisionTreeTable">
          <thead> {renderTableThead}</thead>
          <tbody>{renderTableTbody}</tbody>
        </table>
      </div>
    );
  }
}
