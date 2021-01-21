;(function($) {
	var methods = {
		init: function(settings) {

			return this.each(function() {
				var self = this;
				if (typeof self.pleaseWait != 'undefined')
					return;				
				self.pleaseWait = {
					opt:  $.extend(true, {}, $.fn.pleaseWait.defaults, settings),
					cog: document.createElement('img'),
					timer: false,
					overlay: document.createElement('div'),
                    degrees: 1
				};
                
				var targetWidth = $(self).outerWidth();
				var targetHeight = $(self).outerHeight();
				var verticalMidpoint = (targetHeight / 2) - (self.pleaseWait.opt.height / 2);
				var horizontalMidpoint = (targetWidth / 2) - (self.pleaseWait.opt.width / 2);
				var offset = $(self).offset();

				$(self.pleaseWait.cog).css({
					'position':'absolute',
					'z-index':'999999',
					'left':offset.left + horizontalMidpoint,
					'top':offset.top + verticalMidpoint
				});
				$(document.body).append(self.pleaseWait.cog);

				self.pleaseWait.overlay = document.createElement('div');
				$(self.pleaseWait.overlay).css({
					'position':'absolute',
					'z-index':'999998',
					'left':offset.left,
					'top':offset.top,
					'width':targetWidth,
					'height':targetHeight,
					'background-color':'rgba(48, 47, 47, 0.8)',
					/*'background-image':'url(http://mksp.gov.in/images/loading.gif)',
					'background-position':'center',
					'background-repeat':'no-repeat',*/
					'display':'none'
				});
				$(document.body).append(self.pleaseWait.overlay);

				if (self.pleaseWait.opt.imageType != 'encoded' && self.pleaseWait.opt.image.length > 0) {
					self.pleaseWait.cog.src = image;
				} else {
					self.pleaseWait.cog.src = self.pleaseWait.opt.image;
				}

				$(self).attr('data-pleaseWait', '1');

				methods.start.call(self);

      		});
    	},
		start: function () {
			var self = $(this);
			if (typeof self.length != 'undefined' && self.length > 0)
				self = self[0];
			if (typeof self.pleaseWait == 'undefined')
				return;

			var targetWidth = $(self).outerWidth();
			var targetHeight = $(self).outerHeight();
			var verticalMidpoint = (targetHeight / 2) - (self.pleaseWait.opt.height / 2);
			var horizontalMidpoint = (targetWidth / 2) - (self.pleaseWait.opt.width / 2);
			var offset = $(self).offset();
			$(self.pleaseWait.cog).css({
				'left':offset.left + horizontalMidpoint,
				'top':offset.top + verticalMidpoint
			});
			$(self.pleaseWait.overlay).css({
				'left':offset.left,
				'top':offset.top,
				'width':targetWidth,
				'height':targetHeight,
			});

			$(self.pleaseWait.cog).css('display', '');
			$(self.pleaseWait.overlay).css('display', '');
	    	if (self.pleaseWait.timer != false)
	    		clearTimeout(self.pleaseWait.timer);
	    	var drawMethod = methods.draw;
			var removeMethod = methods.remove;
			self.pleaseWait.timer = setInterval(function () {
				if (document.body.contains(self)) {
					drawMethod.call(self)
				} else {
					removeMethod.call(self);
				}
			},self.pleaseWait.opt.speed);
			return self;
		},
		stop: function () {
			var self = $(this);
			if (typeof self.length != 'undefined' && self.length > 0)
				self = self[0];
			if (typeof self.pleaseWait == 'undefined')
				return;
    		if (self.pleaseWait.timer != false)
    			clearTimeout(self.pleaseWait.timer);
			self.pleaseWait.timer = false;
			$(self.pleaseWait.cog).css('display', 'none');
			$(self.pleaseWait.overlay).css('display', 'none');
			return self;
		},
		draw: function () {
			var self = this;
			if (typeof self.length != 'undefined' && self.length > 0)
				self = self[0];
			if (typeof self.pleaseWait == 'undefined')
				return;
/*
            var rotateTarget = self.pleaseWait.cog;
            if (self.pleaseWait.opt.crazy)
                rotateTarget = self;
            
            if(navigator.userAgent.match("MSIE")){
                rotateTarget.style.msTransform = "rotate("+self.pleaseWait.degrees+"deg)";
            } else if(navigator.userAgent.match("Opera")){
                rotateTarget.style.OTransform = "rotate("+self.pleaseWait.degrees+"deg)";
            } else {
                rotateTarget.style.transform = "rotate("+self.pleaseWait.degrees+"deg)";
            }
            self.pleaseWait.degrees = parseInt(self.pleaseWait.degrees) + parseInt(self.pleaseWait.opt.increment);
            if(self.pleaseWait.degrees > 359){
                self.pleaseWait.degrees = 1;
            } */
	    },
	    remove: function () {
			var self = this;
			if (typeof self.length != 'undefined' && self.length > 0)
				self = self[0];
    		if (typeof self.pleaseWait != 'undefined'){
    			if (self.pleaseWait.timer != false)
    				clearTimeout(self.pleaseWait.timer);

				$(self.pleaseWait.cog).remove();
				$(self.pleaseWait.overlay).remove();
	
				$(self).removeAttr('data-pleaseWait');
				delete self.pleaseWait.overlay;
	      		delete self.pleaseWait.opt;
			    delete self.pleaseWait.cog;
			    delete self.pleaseWait.timer;
			    delete self.pleaseWait;
			}
		}
	};
	$.fn.pleaseWait = function(method) {
		if (!methods[method]) {
			var attr = $(this).attr('data-pleaseWait');
			if (typeof attr == 'undefined' || attr == false)
				return methods.init.apply(this, arguments);
			method = 'start';
		}
    	if (methods[method]) {
      		return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    	} else if (typeof method === 'object' || !method) {
      		return methods.init.apply(this, arguments);
    	} else {
      		$.error('pleaseWait plugin :: method "' + method + '" does not exist!');
    	}
	};
	// reverse image
	// 'iVBORw0KGgoAAAANSUhEUgAAAEEAAABBCAYAAACO98lFAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABEFJREFUeNrsW1tIFFEYPpuG2ZppGl3QUInAl8igCxZdiKCHKKwIeuitCCKoHoIopHqo6CGKqCB66SIEPtiFiOglwgysSBGiCCnBJK00b+ul3Xb6f+YbPJ40d2Yvs7tnfvjYOcPOmdlv/tv5/7M+wzCE7jLNpfseJxjAeV1J8DQhHUnII+xKZRIyo7g2g7CPcJTgJ3wgvNdNE/4QNhFyQchZXc3hDMhgWUmo0pEEVv8aaXyMMF1Hx3iB0IvjEsIBHUnoBRGWHCbM1zFPqJEiA0eKah1JYOd4UhpXwVFqlzG+JjyTxqd0TZtPE4I4rkiVkDkZCcUO52sj3JDG1fARSS2+CeoJawmXCQ8J1wndNufkH10vRYirhHPKd5ZJPqMZppQ0JHCiUytpwiDhJs4FbczLZnANx98JK2xe7yoJ+YQThI3K99oJVwjPbcxdi7B5idCfauYg8OY4BS5Tzr+CqXxOp3qC7z81RnaaOwgHsVK0JEyog60PpjsJluQQDoEQOZr0w3HWgZi0JsESNo0jhErlPJvGRUKjDiRYsk6Y1SQ1l9grzOqSFiRYoXQ3YT/M5SW0ROhEgiUFcJy3EEa1JCHtQ6RHgkeCR4KeJHALbY3D698R7qY6CdyGm0tY7PD6jnTQBK8rDXNgTZjt8PoBQpfnGL3o4JHgkeCRMF7mEX6IxFeXMnBPw00SsglbCRuEWVl+kWASOKr5hFnmG3GDhPWE7WKsuxQQZrcpkCAC/EpYHyX0EUKJIGGJMCtKamntE+E24WeCSMgGCWqyF0DuEo4HCYXC3KZXoZzn7hJXm5tcynZniX97nWEQEYgVCVmELYTNYvxeJFa/p8JsxYeEu5IJrchSzodgIqPRkLCasFOMb7ywNBAeiORrrc3As6p7M0fwrCE7JJQQ9uBTljbCPXxGImUwl2i7VHlQ7Ugauj6YR47iLwzJXxhTkTBHmJsy5Ql6CPeFvfa5Hw6UH6oZCDtwfsWwe36GLzb9BWvFTOX8MOHXVEtpvlk9jpn5J8LcfWJ3/8Aq+BBWzVKHCU0GCLBeTo6Na5nwXiRxv6Xzg5Gagx++4DFIsSu8OWObNH5E6FS+w0Wcchy3isk7V6UggGWI8NEhodl4IQORFlXYdu44JIDVXy7VtU5AgB35KpkRq3a+w3mGJyMgHpUlfrsFkjlF26QNwrlaUhSHZ47phOwDlkvjphil0d+kyMD3WJDMJFRI3ph/fEuM5g3DLORVa1YyksDhaKk0bozx0rpH8uw+4XyLYVxJqJTm6oRDjLW0S5FhthQ+k4KERYCVmTXEKS0eUiJWEbTCdRJ8WGNYwvG+W8RPOpSQWZgMJJQjtxfIzN7EeZEURLSwZKGI7s9sMSPBkuZIlq0xkC7pPpnSS3CNBN7//Ba22iISIwac5BAqWlFXs9wquUe6dkhYiUp78Uhw0RxypRVhnxj7S6Er8leAAQAs1TY2lWgC2wAAAABJRU5ErkJggg=='
 	$.fn.pleaseWait.defaults = {
        crazy:false,
    	speed:5,
        increment: 2,
		image:'https://documentation.devexpress.com/HelpResource.ashx?help=WPF&document=img118763.jpg',
		imageType: 'encoded',
		height:65,
		width:65
	};
})(jQuery);