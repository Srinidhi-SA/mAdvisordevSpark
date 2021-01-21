$(function () {
/** In small device sidebar will dis-appear, with the help of below jq will appear the side menu **/
		$('.navbar-toggle').click(function () {
			$('.navbar-nav').toggleClass('slide-in');
			$('.side-body').toggleClass('body-slide-in');
		});

	/*	.for more 'text' collapsible script
	$('.crop').click(function() {
		$(this).toggleClass('crop');
	}); */

/*** Popover function **
$('[rel="popover"]').popover({
	container: 'body',
	html: true,
	trigger: 'focus',
	placement: 'auto right',
	content: function () {
		var clone = $($(this).data('popover-content')).clone(true).removeClass('hide');
		return clone;
	}
}).click(function(e) {
	e.preventDefault();
});*/

/** Below Script for main tab content slide buttons *Next and *Previous *
$('.continue').click(function(){
  $('.nav-tabs > .active').next('li').find('a').trigger('click');
});
$('.back').click(function(){
  $('.nav-tabs > .active').prev('li').find('a').trigger('click');
});*/
/* var hidWidth;
 * Below code is for subnavigation ** 
var scrollBarWidths = 40;

var widthOfList = function(){
  var itemsWidth = 0;
  $('.list li').each(function(){
    var itemWidth = $(this).outerWidth();
    itemsWidth+=itemWidth;
  });
  return itemsWidth;
};

var widthOfHidden = function(){
  return (($('.wrapper').outerWidth())-widthOfList()-getLeftPosi())-scrollBarWidths;
};

var getLeftPosi = function(){
  return $('.list').position().left;
};

var reAdjust = function(){
  if (($('.wrapper').outerWidth()) < widthOfList()) {
    $('.scroller-right').hide();
  }
  else {
    $('.scroller-right').show();
  }

  if (getLeftPosi()<0) {
    $('.scroller-left').show();
  }
  else {
    $('.item').animate({left:"-="+getLeftPosi()+"px"},'slow');
  	$('.scroller-left').hide();
  }
}

reAdjust();

$(window).on('resize',function(e){
  	reAdjust();
});

$('.scroller-right').click(function() {
  $('.scroller-left').fadeIn('slow');
  $('.scroller-right').fadeOut('slow');
  $('.list').animate({left:"+="+widthOfHidden()+"px"},'slow',function(){
  });
});

$('.scroller-left').click(function() {
	$('.scroller-right').fadeIn('slow');
	$('.scroller-left').fadeOut('slow');
  	$('.list').animate({left:"-="+getLeftPosi()+"px"},'slow',function(){
  	});
});
*/
/** Slide Panel **

$('[data-toggle=offcanvas]').click(function () {
    $('.row-offcanvas').toggleClass('active');
	if ($('.row-offcanvas-left').hasClass('active')){
		$('.sdbar_switch i').removeClass('sw_on');
		$('.sdbar_switch i').addClass('sw_off');
    } else {
		$('.sdbar_switch i').addClass('sw_on');
		$('.sdbar_switch i').removeClass('sw_off');
	};
  });*/

 /*** Seach Visible **
$("#search-button, #search-icon").click(function(e){
 e.preventDefault();
 $("#search-button, #search-form").toggle();
});*/




});
