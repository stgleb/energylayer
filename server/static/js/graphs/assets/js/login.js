/*
 * MoonCake v1.1 - Login JS
 *
 * This file is part of MoonCake, an Admin template build for sale at ThemeForest.
 * For questions, suggestions or support request, please mail me at maimairel@yahoo.com
 *
 * Development Started:
 * July 28, 2012
 * Last Update:
 * October 10, 2012
 *
 */

;(function( $, window, document, undefined ) {
	
	var LoginScreen = function() { }

	LoginScreen.prototype = {

		init: function() {
			this.transitionFn = this['_fade'];

			$( '#login-buttons .btn' ).each($.proxy(function(i, btn) {
				var target = $($(btn).data( 'target' ));

				if( target && target.length ) {
					$(btn).toggleClass('disabled', $(target).is('.active'))
						.on('click', $.proxy(this._clickHandler, this));
				}
			}, this));

			return this;
		}, 

		_clickHandler: function(e) {
			var btn = $(e.currentTarget), 
				target = $(btn.data( 'target' ));

			if( !btn.is('.disabled') ) {
				this.transitionFn.call(this, target);
				$( '#login-buttons .btn' ).not(btn.addClass('disabled')).removeClass('disabled');
			}

			e.preventDefault();
		}, 

		_fade: function(target) {
			$( '.login-inner-form.active' ).fadeOut( 'normal', function() {
				target.addClass( 'active' ).fadeIn();
				$(this).removeClass( 'active' );
			});
		}
	};

	$.loginScreen = new LoginScreen();

	$( document ).ready( function( e ) {

		$.loginScreen.init();

		// Style checkboxes and radios
		$.fn.uniform && $(':radio.uniform, :checkbox.uniform').uniform();

		// IE Placeholder
		$.fn.placeholder && $('[placeholder]').placeholder();
	});

	
}) (jQuery, window, document);
