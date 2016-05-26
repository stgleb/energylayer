/*
 * MoonCake v1.1 - FileInput Plugin JS
 *
 * This file is part of MoonCake, an Admin template build for sale at ThemeForest.
 * For questions, suggestions or support request, please mail me at maimairel@yahoo.com
 *
 * Development Started:
 * July 28, 2012
 * Last Update:
 * October 10, 2012
 *
 * 'Highly configurable' mutable plugin boilerplate
 * Author: @markdalgleish
 * Further changes, comments: @addyosmani
 * Licensed under the MIT license
 *
 */

;(function( $, window, document, undefined ) {
	// our plugin constructor
	function FileInput( element, options ) {
		if( arguments.length ) {
			this._init( element, options );
		}
    };
	
	// the plugin prototype
	FileInput.prototype = {
		defaults: {
			placeholder: 'No file selected...', 
			buttontext: 'Browse...', 
			inputSize: 'large'
		}, 

		_init: function( element, options ) {
			this.element = $( element );
			this.options = $.extend( {}, this.defaults, options, this.element.data() );

			this._build();
		}, 

		_build: function () {

			this.element.css( {
				'position': 'absolute', 
				'top': 0, 
				'right': 0, 
				'margin': 0, 
				'cursor': 'pointer', 
				'fontSize': '99px', 
				'opacity': 0, 
				'filter': 'alpha(opacity=0)'
			} )
			.on( 'change.fileupload', $.proxy( this._change, this) );

			this.container = $( '<div class="fileinput-holder input-append"></div>' )
				.append( $( '<div class="fileinput-preview uneditable-input" style="cursor: text; text-overflow: ellipsis; "></div>' )
						.addClass( 'input-' + this.options.inputSize ).text( this.options.placeholder ) )
				.append( $( '<span class="fileinput-btn btn" style="overflow: hidden; position: relative; cursor: pointer; "></span>' )
						.text( this.options.buttontext ) )
				.insertAfter( this.element );

			this.element.appendTo( this.container.find( '.fileinput-btn' ) );

		}, 

		_change: function ( e ) {
			
			var file = e.target.files !== undefined ? e.target.files[0] : { name: e.target.value.replace(/^.+\\/, '') };
			if ( !file ) return;
			
			this.container.find( '.fileinput-preview ' ).text(file.name);
		}, 

		option: function( key, value ) {
			
			if ( arguments.length === 0 ) {
				// don't return a reference to the internal hash
				return $.extend( {}, this.options );
			}

			if  (typeof key === "string" ) {
				if ( value === undefined ) {
					return this.options[ key ];
				}

				switch(key) {
					case 'value':
						value = Math.max(0, Math.min(value, this.options.maxValue));
						break;
					default:
						break;
				}

				this.options[ key ] = value;
				this._draw();
			}

			return this;
		}
	}

	$.fn.fileInput = function( options ) {

		var isMethodCall = typeof options === "string",
			args = Array.prototype.slice.call( arguments, 1 ),
			returnValue = this;

		// prevent calls to internal methods
		if ( isMethodCall && options.charAt( 0 ) === "_" ) {
			return returnValue;
		}

		if ( isMethodCall ) {
			this.each(function() {
				var instance = $.data( this, 'fileinput' ),
					methodValue = instance && $.isFunction( instance[options] ) ?
						instance[ options ].apply( instance, args ) :
						instance;

				if ( methodValue !== instance && methodValue !== undefined ) {
					returnValue = methodValue;
					return false;
				}
			});
		} else {
			this.each(function() {
				var instance = $.data( this, 'fileinput' );
				if ( !instance ) {
					$.data( this, 'fileinput', new FileInput( this, options ) );
				}
			});
		}

		return returnValue;
	};

	/* DATA-API
	* ================== */

	$(function () {
		$('[data-provide="fileinput"]').each(function () {
			var $input = $(this);
			$input.fileInput($input.data());
		});
	});

})( jQuery, window , document );
