export default function(divId){
  Array.max = function( array ){
    return Math.max.apply( Math, array );
  };

  var clr = null;

  var counts= $("."+divId).find('tbody td').not('.stats-title').map(function() {
      if($(this).attr("value") == undefined)
        return parseFloat($(this).html());
      else
        return parseFloat($(this).attr("value"));
    }).get();

    $("."+divId).find('tbody td').not('.stats-title').each(function(){
      let val = $(this).text();
      var exp = /[a-z]/i;
      if(exp.test(val)){
        val = parseFloat($(this).attr("value"));
      }else{
         val = parseFloat(val);
      }

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
