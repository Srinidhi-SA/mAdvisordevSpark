export const c3Functions={

get_colors: function(color, d){
  return colors[d.index];
},


set_tooltip:  function (d, defaultTitleFormat, defaultValueFormat, color) {
                   console.log(d[0].value);

                                 //    return "Working";
          return "<table class='tooltip-table'><thead><th colspan=2><b>"+ toolLegend[toolData[1].indexOf(d[0].value)]+"</b></th></thead><tbody><tr><td>"+ toolData[0][0]+"   </td><td> | " + d3.format('.2f')(toolData[0][toolData[1].indexOf(d[0].value)]) + "</td></tr><tr><td>"+ toolData[1][0]+"  </td><td> | "+ d3.format('.2f')(d[0].value)+ "</td></tr></tbody></table>";

},

set_negative_color: function(color, d){
            //alert(d);
            if(d.value<0){
              return '#f47b16';
             }else{
              return '#00AEB3';
            }
        },


set_pie_labels: function (value, ratio, id) {
                      if(pieformatrobo == 'm'){
                        return d3.format('.2s')(value);
                      }else if(pieformatrobo == '$'){
                          return d3.format('$')(value);
                      }else if(pieformatrobo == '$m'){
                          return d3.format('$,.2s')(value);
                      }else if(pieformatrobo == 'f'){
                          return d3.format('.2f')(value);
                      }

                   },

set_donut_labels: function (value, ratio, id) {
                                 if(pieformatrobo == 'm'){
                                   return d3.format('.2s')(value);
                                 }else if(pieformatrobo == '$'){
                                     return d3.format('$')(value);
                                 }else if(pieformatrobo == '$m'){
                                     return d3.format('$,.2s')(value);
                                 }else if(pieformatrobo == 'f'){
                                     return d3.format('.2f')(value);
                                 }

                              }

// set_format_m: d3.format(".2s"),
//
// set_format_$: d3.format("$"),
//
// set_format_$m: d3.format("$,.2s")

}
