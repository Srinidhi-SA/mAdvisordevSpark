// http://bl.ocks.org/3687826
d3.divgrid = function(config) {
  var columns = [];
  settings = config;
  var dg = function(selection) {
    if (columns.length == 0) columns = d3.keys(selection.data()[0][0]);
    if(columns[columns.length-1] != "Select for Scoring")columns.push("Select for Scoring");

    if(settings.columnOrder.length > 0){
      if(selection.attr('id') == settings.id){
        columns = settings.columnOrder;
        if(columns[columns.length-1] != "Select for Scoring")columns.push("Select for Scoring");
      }
    }
    else{
      $.each(settings.ignoleTableList,function(key,val){
        columns.splice( columns.indexOf(val), 1 );
      });
    }
    var rowhead = selection.selectAll(".rowhead")
      .data([true]);

      rowhead.enter().append("tr").attr("class","rowhead");
 rowhead.exit().remove();

            var rowHcell = selection.selectAll(".rowhead").selectAll(".cell").data(columns);

            rowHcell.enter().append("th").classed("cell", true);
           // tr.appendChile(th)

    // rows
    var rows = selection.selectAll(".rowbody")
        .data(function(d) { return d; })

    rows.enter().append("tr")
        .attr("class", "rowbody")

    rows.exit().remove();
    var cells = selection.selectAll(".rowbody").selectAll(".cell")
        .data(function(d) { 
          return columns.map(function(col){
            if(d[col] == undefined && col == "Select for Scoring"){
              if (settings.fromModel){
                if(d["alwaysSelected"] == "True")
                return ('<input type="checkbox" checked class="chkBoxTop" disabled />');
                else if(d["Selected"] == "True" && settings.selectedModelCount <= 10)
                return ('<input type="checkbox" checked class="chkBoxSelect" data-name='+d["algorithmName"].replace(/ /g,"_")+' data-slug='+d["Slug"]+' data-model='+d["Model Id"]+' data-key='+d[settings.evaluationMetricColName]+' data-acc='+d[d[settings.evaluationMetricColName]]+' />');
                else if (d["Selected"] == "False" && settings.selectedModelCount == 10)
                return ('<input type="checkbox" class="chkBox" disabled data-name='+d["algorithmName"].replace(/ /g,"_")+' data-slug='+d["Slug"]+' data-model='+d["Model Id"]+' data-key='+d[settings.evaluationMetricColName]+' data-acc='+d[d[settings.evaluationMetricColName]]+' />');
                else if (d["Selected"] == "False" && settings.selectedModelCount < 10)
                return ('<input type="checkbox" class="chkBox" data-name='+d["algorithmName"].replace(/ /g,"_")+' data-slug='+d["Slug"]+' data-model='+d["Model Id"]+' data-key='+d[settings.evaluationMetricColName]+' data-acc='+d[d[settings.evaluationMetricColName]]+' />');
              }
              else{
                if(d["Selected"] == "True")
                return ('<input type="checkbox" checked class="chkBox" disabled/>');
                else
                return ('<input type="checkbox" disabled class="chkBox"/>');
              }
            }
            else
            return d[col];
          })
         });
    // cells
    cells.enter().append("td")
      .attr("class", function(d,i) { return "col-" + i; })
      .classed("cell", true)

    cells.exit().remove();

    selection.selectAll(".cell")
      .html(function(d) { return d; }
    );


    return dg;
  };

  dg.columns = function(_) {
    if (!arguments.length) return columns;
    columns = _;
    return this;
  };

  return dg;
};
