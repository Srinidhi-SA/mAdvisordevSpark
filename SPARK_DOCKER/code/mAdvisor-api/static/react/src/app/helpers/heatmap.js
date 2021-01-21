export default function(divId){
  Array.max = function( array ){
        return Math.max.apply( Math, array );
    };


    var red,blue,green,clr = null;
   var  xr = 255;
   var  xg = 255;
    var xb = 255;

    /*yr = 243;
    yg = 32;
    yb = 117;*/
   /*  var yr = 0;
   var yg = 100;
   var yb = 0*/

	var yr = 0;
   var yg = 153;
   var yb = 140

   var n = 100;
  var counts= $("."+divId).find('tbody td').not('.stats-title').map(function() {
      if($(this).attr("value") == undefined)
        return parseFloat($(this).html());
      else
          return parseFloat($(this).attr("value"));
        // .replace('%','').trim()
    }).get();

    // return max value
    var max = Array.max(counts);

    // add classes to cells based on nearest 10 value
    $("."+divId).find('tbody td').not('.stats-title').each(function(){
       //var val = parseFloat($(this).text());
      let val = $(this).text();
      var digitExp = /\d+/g;

      var exp = /[a-z]/i;
      if(exp.test(val)){
        val = parseFloat($(this).attr("value"));
      //  val = parseFloat(val.match(digitExp));
      }else{
         val = parseFloat(val);
      }

        // var pos = parseFloat((Math.round((val/max)*100)).toFixed(0));
        // red = parseFloat((xr + (( pos * (yr - xr)) / (n-1))).toFixed(0));
        // green = parseFloat((xg + (( pos * (yg - xg)) / (n-1))).toFixed(0));
        // blue = parseFloat((xb + (( pos * (yb - xb)) / (n-1))).toFixed(0));
        // clr = 'rgb('+red+','+green+','+blue+')';
        // $(this).css({backgroundColor:clr});

        if(val === 0){
          $(this).css({backgroundColor:"rgb(75,196,188,0.04)"});
        }else if(val>0 && val<0.1){
          $(this).css({backgroundColor:"rgba(75,196,188,0.09)"});
        }else if(val >= 0.1){
          clr = "rgba(0,152,139,"+(val.toFixed(1))+")"
          $(this).css({backgroundColor:clr});
        }else if(val < 0){
          clr = "rgba(230,63,82,"+-(val.toFixed(1))+")"
          $(this).css({backgroundColor:clr});
        }
    });

}
