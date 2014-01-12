// Delay Plugin for jQuery
// - http://www.evanbot.com
// - © 2008 Evan Byrne

jQuery.fn.delay = function(time,func){
	this.each(function(){
		setTimeout(func,time);
	});
	return this;
};

jQuery.fn.slideFadeToggle = function(speed, easing, callback) {
  return this.animate({opacity: 'toggle', height: 'toggle'}, speed, easing, callback);  
};

function flash(e, duration) {
  duration = duration || 3000;
  $(e).hide();
  $(e).fadeIn(500, function() {
    $(this).delay(duration, function() {
      $(e).slideFadeToggle(1000);
    }); 
  });
}

