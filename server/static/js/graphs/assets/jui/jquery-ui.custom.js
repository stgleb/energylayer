/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
 *
 * MoonCake v1.1 - Extended jquery-ui Widgets
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
 
/* jquery-ui Extended Slider v1.0
 *
 * This extends jquery-ui Slider with Tooltip and Ticks
 *
 * Options:
 *    ticks: An array that contains tick values to show below/beside the slider
 *    tooltip: none | always | ondrag
 *          This specify which event will toggle the tooltip
 *
================================================== */

(function( $, prototype ) {
	$.extend( prototype.options, {		
		ticks: [], 		
		tooltip: 'always' // none | always | ondrag

	});

	this._isExtended = false;
	this._mouseIn = false;
	this._sliding = false;
	
	var _base_create = prototype._create;
	prototype._create = function() {
		_base_create.call( this );
	
		var self = this, 
			tooltip = '<span class="ui-slider-handle-tooltip ui-state-default" style="display: none; "></span>', 
			tooltips = [];
		
		this.handles.each(function( i ) {
			tooltips.push( tooltip );
		});
		
		this.tooltips = $( tooltips.join('') ).appendTo( self.element );
			
		if( this.options.tooltip === "always" ) {
			self.handles.each( function( i, handle ) {
				$( handle )
					.on( "mouseenter.slider", { 'index': i }, $.proxy( self._mouseEnter, self ))
					.on( "mouseleave.slider", { 'index': i }, $.proxy( self._mouseLeave, self ));
			});
		}
		
			
		if( this.options.ticks && this.options.ticks.length ) {
			var ticks = $('<div></div>', { 'class': 'ui-slider-ticks' }), 
				s = this.options.ticks, 
				prc = (100.0 / ( s.length - 1 ) );
			
			for( var i =  0; i < s.length; i++ ) {
				
				if( this.orientation === "horizontal" )
					ticks.append('<span style="left: ' + (i * prc) + '%">' + ( s[i] != '|' ? '<ins>' + s[i] + '</ins>' : '' ) + '</span>');
				else
					ticks.append('<span style="bottom: ' + (i * prc) + '%">' + ( s[i] != '|' ? '<ins>' + s[i] + '</ins>' : '' ) + '</span>');
			};
			
			this.ticks = ticks.appendTo( this.element );
		}
		
		this._isExtended = true;
		
		this._refreshValue();
	}
	
	var _base_start = prototype._start;
	prototype._start = function( event, index ) {
		if( this.options.tooltip === "ondrag" ) {
			$( this.tooltips[ index ] ).fadeIn();
		}
		else if( this.options.tooltip === "always" ) {
			this._sliding = true;
		}
		
		return _base_start.call( this, event, index );
	}
	
	var _base_stop = prototype._stop;
	prototype._stop = function( event, index ) {
		if( this.options.tooltip === "ondrag" ) {
			$( this.tooltips[ index ] ).fadeOut();
		}
		else if( this.options.tooltip === "always" ) {
			this._sliding = false;
			if( !this._mouseIn ) {
				$( this.tooltips[ index ] ).fadeOut();
			}
		}
		
		return _base_stop.call( this, event, index );
	}
	
	// todo in 1.1
	var _base_setOption = prototype._setOption;
	prototype._setOption = function( key, value ) {
		_base_setOption.call( this, key, value );

		switch ( key ) {
			case "ticks":
				break;
			case "tooltip":
				break;
		}
	}
	
	var _base_refreshValue = prototype._refreshValue;
	prototype._refreshValue = function() {
		_base_refreshValue.call( this );
		
		if( this._isExtended ) {
			var o = this.options,
				self = this,
				animate = ( !this._animateOff ) ? o.animate : false,
				valPercent,
				_css = {},
				t, 
				value,
				valueMin,
				valueMax;
			
			if ( o.values && o.values.length ) {
				this.handles.each(function( i, j ) {					
					t = $( self.tooltips[ i ] );
					if( t && t.length ) {
						valPercent = ( self.values(i) - self._valueMin() ) / ( self._valueMax() - self._valueMin() ) * 100;
						
						t.text( self._formatNumber( self.values(i) ) );
						
						if( self.orientation === "horizontal" ) {
							_css[ "marginLeft" ] = -( t.outerWidth() / 2 );
							_css[ "left" ] = valPercent + "%";
						} else {
							_css[ "marginBottom" ] = -( t.outerHeight() / 2 );
							_css[ "bottom" ] = valPercent + "%";
						}
							
						t.css( _css );
					}
				});
			} else {				
				t = $( self.tooltips[ 0 ] );
				if( t && t.length ) {
					value = this.value();
					valueMin = this._valueMin();
					valueMax = this._valueMax();
					valPercent = ( valueMax !== valueMin ) ?
							( value - valueMin ) / ( valueMax - valueMin ) * 100 :
							0;
							
					t.text( self._formatNumber( value ) );
					
					if( self.orientation === "horizontal" ) {
						_css[ "marginLeft" ] = -( t.outerWidth() / 2 );
						_css[ "left" ] = valPercent + "%";
					} else {
						_css[ "marginBottom" ] = -( t.outerHeight() / 2 );
						_css[ "bottom" ] = valPercent + "%";
					}
						
					t.css( _css );
				}
			}
		}
	}
	
	var _base_destroy = prototype.destroy;
	prototype.destroy = function() {
		
		if( this._isExtended ) {
			var self = this;
			
			self.handles.each(function( i, handle ) {
				$( handle ).off( ".slider");
			});
			
			self.tooltips.remove();
			self.ticks.remove();
		}
		
		_base_destroy.call( this );
	}
	
	$.extend( prototype, {
		_formatNumber: function( value ){
			value = value.toString().replace(/,/gi, ".").replace(/ /gi, "");
			
			return new Number(value);
		}, 
		_mouseEnter: function( ev ) {
			if( !this._mouseIn ) {
				this._mouseIn = true;
				$( this.tooltips[ ev.data.index ] ).stop(true, true).fadeIn();
			}
		}, 
		_mouseLeave: function( ev ) {
			if( this._mouseIn ) {				
				if( !this._sliding )
					$( this.tooltips[ ev.data.index ] ).stop(true, true).fadeOut();
				this._mouseIn = false;
			}
		}
	});
	
}( jQuery, jQuery.ui.slider.prototype ) );


/* jquery-ui Extended ProgressBar v1.0
 *
 * This integrates jquery-ui ProgressBar with Bootstrap.
 *
 * Options:
 *    striped: enable Bootstrap striped progress bar style
 *    active: enable animation on striped progress bar
 *    showValue: show the progress bar value
 *    type: info | success | warning | danger, 
 *          This specifies which Bootstrap progress bar style
 *
================================================== */

(function( $, prototype ) {
	$.extend( prototype.options, {
		striped: false, 
		active: false, 
		showValue: false, 
		type: '' // info | success | warning | danger
	});
	
	var _base_create = prototype._create;
	prototype._create = function() {
		_base_create.call( this );
		
		this.element
			.addClass( 'progress' );
			
		if( this.options.striped )
			this.element.addClass( 'progress-striped' );
			
		if( this.options.active )
			this.element.addClass( 'active' );
			
		if( $.inArray( this.options.type, ['info', 'success', 'warning', 'danger'] ) )
			this.element.addClass( 'progress-' + this.options.type );
			
		this.valueDiv
			.addClass( 'bar' )
			.append( $( '<span></span>' ).toggle( this.options.showValue ) );
			
		this._refreshValue();
	}
	
	var _base_refreshValue = prototype._refreshValue;
	prototype._refreshValue = function() {
		
		_base_refreshValue.call( this );
		
		var value = this.value();

		this.valueDiv
			.find( ' > span' )
			.text( value + '%' );
	}
	
	var _base_destroy = prototype.destroy;
	prototype.destroy = function() {
		
		this.element
			.removeClass( 'progress progress-striped active' );
		
		_base_destroy.call( this );
	}
	
}( jQuery, jQuery.ui.progressbar.prototype ) );

/* jquery-ui Extended Autocomplete v1.0
 *
 * This matches jquery-ui Autocomplete styles with Bootstrap's Typeahead
 *
================================================== */

(function( $, prototype ) {

	var _base_create = prototype._create;
	prototype._create = function() {
		_base_create.call( this );
		
		this.menu.element.addClass( 'typeahead dropdown-menu' );
	}
	
}( jQuery, jQuery.ui.autocomplete.prototype ) );
