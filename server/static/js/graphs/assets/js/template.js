/*
 * MoonCake v1.1 - Template JS
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
	
	var MoonCake = function( document ) {
		this.document = $(document);
	}

	MoonCake.prototype = {
		
		version: '1.0', 

		init: function( options ) {

			this.bindEventHandlers();
			options.showSidebarToggleButton && this.attachSidebarToggleButton();
			this.setSidebarMinHeight( '#wrapper #sidebar #navigation > ul > li.active:first > .inner-nav' );
			
			return this;
		}, 

		ready: function( fn ) {
			this.document.ready($.proxy(function() {
				fn.call( this.document, this );
			}, this));

			return this;
		}, 

		attachSidebarToggleButton: function() {

			var toggleButton = $( '<li id="sidebar-toggle-wrap"><span id="sidebar-toggle"><span></span></span></li>' );

			toggleButton
				.appendTo( '#wrapper #sidebar #navigation > ul' )
				.children( '#sidebar-toggle' )
				.on( 'click.template', function(e) {
					if( !!$( '#sidebar #navigation > ul > li.active:first .inner-nav' ).length ) {
						$(this).parents( '#content' )
							.toggleClass( 'sidebar-minimized' )
						.end()
							.toggleClass( 'toggled' );
					}
					e.preventDefault();
				})
				.toggleClass( 'disabled', !$( '#sidebar #navigation > ul > li.active:first .inner-nav' ).length )
				.toggleClass( 'toggled', $( '#wrapper #content' ).hasClass( 'sidebar-minimized' ) );
		}, 

		bindEventHandlers: function() {

			// Search and Dropdown-menu inputs
			$( '#header #header-search .search-query')
				.add( $( '.dropdown-menu' )
				.find( ':input' ) )
				.on( 'click.template', function( e ) {
					e.stopPropagation();
				});

			var self = this;
			// Sidebar Navigation
			$( '#sidebar #navigation > ul > li' )
				.filter(':not(#sidebar-toggle-wrap)')
				.on( 'click.template', ' > span', function( e ) {
					var hasInnerNav = !!$( this ).siblings( '.inner-nav' ).length;

					$( this ).parent()
						.siblings().removeClass( 'active open' )
					.end()
						.addClass( 'active' ).toggleClass( 'open' );

					$( '#content' )
						.toggleClass( 'sidebar-minimized', !hasInnerNav );

					$( '#sidebar-toggle' )
						.toggleClass( 'disabled', !hasInnerNav )
						.toggleClass( 'toggled', $( '#content' ).hasClass( 'sidebar-minimized' ) );

					self.setSidebarMinHeight( $( this ).siblings( '.inner-nav' ) ) ;
					
					e.stopPropagation();
				});

			// Collapsible Boxes
			$( '.widget .widget-header [data-toggle=widget]' )
			.each(function(i, element) {
				var p = $( this ).parents( '.widget' );
				if( !p.children( '.widget-inner-wrap' ).length ) {
					p.children( ':not(.widget-header)' )
						.wrapAll( $('<div></div>').addClass( 'widget-inner-wrap' ) );
				}
			}).on( 'click', function(e) {
				var p = $( this ).parents( '.widget' );
				if( p.hasClass('collapsed') ) {
					p.removeClass( 'collapsed' )
						.children( '.widget-inner-wrap' ).hide().slideDown( 250 );
				} else {
					p.children( '.widget-inner-wrap' ).slideUp( 250, function() {
						p.addClass( 'collapsed' );
					});
				}
				e.preventDefault();
			});
		}, 

		setSidebarMinHeight: function( nav ) {
			nav = $( nav )[0];
			$( '#wrapper #sidebar #navigation > ul' )
				.css( 'minHeight', nav? $( nav ).outerHeight() : '');
		}
	};

	$.template = new MoonCake( document ).ready( function( template ) {

		template.init({
			showSidebarToggleButton: true // show or hide the sidebar toggle button
		});

	});

	
}) (jQuery, window, document);