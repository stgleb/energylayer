/*
 * MoonCake v1.1 - Wizard Plugin
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

;(function($, window, document, undefined) {
	// our plugin constructor
	var Wizard = function( element, options ) {
		if( arguments.length ) {
			this._init( element, options );
		}
    };
	
	// the plugin prototype
	Wizard.prototype = {
		defaults: {
			// Elements
			element: '.wizard-step', 
			navLabelElement: '.wizard-label', 
			buttonContainer: '.wizard-actions', 
			
			// Class Names
			navContainerClass: 'wizard-nav', 
			buttonContainerClass: 'form-actions btn-toolbar', 
			
			// Transition Callback
			transition: null, // function(wizard, prev, current);
			
			// Wizard Callbacks
			onStepLeave: null, // function(wizard, step);
			onStepShown: null, // function(wizard, step);
			onBeforeSubmit: null, // function(wizard, form);
			
			// Wizard Options
			forwardOnly: false, 
			orientation: 'horizontal', // (horizontal | vertical)
			
			// Ajax Submit [Requires jQuery Form Plugin]
			ajaxSubmit: true, 
			ajaxOptions: {}, 
			
			// Button Classes
			defaultButtonClass: 'btn', 
			responsiveNextButtonClass: 'responsive-next-btn', 
			responsivePrevButtonClass: 'responsive-prev-btn', 
			submitButtonClass: 'btn-primary pull-right', 
			
			// Button Labels
			responsiveNextButtonLabel: '<i class="icon-caret-right"></i>', 
			responsivePrevButtonLabel: '<i class="icon-caret-left"></i>', 
			nextButtonLabel: 'Next', 
			prevButtonLabel: 'Prev', 
			submitButtonLabel: 'Submit'
		}, 
		
		// Private Variables
		
		/* The Current Active Step ID */
		_activeStepId: null, 
		
		/* The Collection of Wizard Steps */
		_steps: null, 
		
		/* The Collection of Nav Buttons */
		_buttons: null, 
		
		/* The Main Wizard Navigation Container */
		_nav: null, 
		
		_init: function( element, options ) {

			this.element = $( element );
			this.options = $.extend( {}, this.defaults, options, this.element.data() );
			
			if( !$.inArray( this.options.orientation, ['horizontal', 'vertical'] ) )
				this.options.orientation = 'horizontal';
				
			$.fn.ajaxForm && this.options.ajaxSubmit && this.element.ajaxForm( this.options.ajaxOptions );
			
			this.element.addClass( 'wizard-form ' + 'wizard-form-' + this.options.orientation );
				
			this._steps = this.element.find(this.options.element)
			this._nav = this._buildNavigation().insertBefore(this.element);
			this._buttons = this._buildButtons();
			
			this.reset();
		}, 
		
		_buildNavigation: function() {
			var navContainer = $('<div></div>', { 
					'class': this.options.navContainerClass + ' ' + this.options.navContainerClass + '-' + this.options.orientation
				}), 
				ul = $('<ul></ul>'), 
				self = this, 
				navItem = $('<li><span></span></li>'), 
				guid = this._generateRandomId();
			
			this._steps.each(function(k, v) {
				var nav = $(v).find(self.options.navLabelElement).first(), 
					nItem = navItem.clone(), 
					stepId = guid + '_' + k;
				
				nItem.find('span').html(nav && nav.length? nav.html() : 'Step ' + k)
					.appendTo(nItem.appendTo(ul).attr('data-step-id', stepId));
					
				$(v).attr('data-step-id', stepId);
				
				nav.hide();
			});
			
			return navContainer.on('click.wizard', 'li', function(e) {
				self._activateStep($(this).data('step-id'));
			}).append(ul);
			
		}, 
		
		_buildButtons: function() {
			var self = this, 
				btnContainer = this.element.find(this.options.buttonContainer), 
				$btn = $('<button type="button"></button>').addClass(this.options.defaultButtonClass);
				
			var prevButton = $btn.clone().addClass(this.options.prevButtonClass).html(this.options.prevButtonLabel), 
				responsivePrevButton = $btn.clone().addClass(this.options.responsivePrevButtonClass).html(this.options.responsivePrevButtonLabel), 
				nextButton = $btn.clone().addClass(this.options.nextButtonClass).html(this.options.nextButtonLabel), 
				responsiveNextButton = $btn.clone().addClass(this.options.responsiveNextButtonClass).html(this.options.responsiveNextButtonLabel), 
				submitButton = $btn.clone().addClass(this.options.submitButtonClass).html(this.options.submitButtonLabel);
				
				prevButton.add(responsivePrevButton).on('click.wizard', function(e) {
					self.prevStep();
					e.preventDefault();
				});
				
				nextButton.add(responsiveNextButton).on('click.wizard', function(e) {
					self.nextStep();
					e.preventDefault();
				});
				
				submitButton.on('click.wizard', function(e) {
					self.submitForm();
					e.preventDefault();
				})
			
			if(!btnContainer.length)
				btnContainer = $('<div></div>').appendTo(this.element);
			
			btnContainer.contents().hide().end().addClass(this.options.buttonContainerClass);
			
			if(!this.options.forwardOnly)
				btnContainer.append(prevButton);
				
			btnContainer.append(nextButton, submitButton);
			this._nav.append(responsivePrevButton, responsiveNextButton);
			
			return { 
				prevButton: prevButton, 
				responsivePrevButton: responsivePrevButton, 
				nextButton: nextButton, 
				responsiveNextButton: responsiveNextButton, 
				submitButton: submitButton
			};
		}, 
		
		_activateStep: function(stepId) {
			if(this._locked || (this._activeStepId === stepId)) return;
			
			var step = this._getStepById(stepId), 
				activeStep = this._getStepById(this._activeStepId);
			
			if(!this.options.onStepLeave || 
			   (this.options.onStepLeave && $.isFunction(this.options.onStepLeave) && 
				(false !== this.options.onStepLeave.apply(this, [ this, activeStep ])))) {
				
				this._activateNav(stepId);
				step && (activeStep? this._transition($(activeStep), $(step)) : $(step).show());					
				this._activeStepId = stepId;
			}
		}, 
		
		_activateNav: function(stepId) {
			this._nav
				.find('li')
				.removeClass('current')
				.filter(function() { return $(this).data('step-id') === stepId; })
				.addClass('current');
		}, 
		
		_transition: function(prev, current) {
			if(current) {
				var self = this;
				
				self._beforeTransition();
				
				prev?
				(this.options.transition?
					this.options.transition.apply(this, [this, prev, current]) : 
					prev.fadeOut('fast', function()
					{
						current.fadeIn('fast', function()
						{
							self._afterTransition();
						});
					})
				) : current.show();
			}
		}, 
		
		_isLastStep: function(stepId) {
			return stepId && this._steps.last().data('step-id') === stepId;
		}, 
		
		_isFirstStep: function(stepId) {
			return stepId && this._steps.first().data('step-id') === stepId;
		}, 
		
		_getStepById: function(stepId) {
			return this._steps.filter(function() { return $(this).data('step-id') === stepId; })[ 0 ];
		}, 
		
		_getNavById: function(stepId) {
			return $('li', this._nav).filter(function() { return $(this).data('step-id') === stepId; })[ 0 ];
		}, 
		
		_refreshButtons: function() {
			this._buttons.prevButton.attr('disabled', this._isFirstStep(this._activeStepId) && !this.options.forwardOnly);
			this._buttons.nextButton.attr('disabled', this._isLastStep(this._activeStepId));
			
			this._buttons.responsivePrevButton.attr('disabled', this._isFirstStep(this._activeStepId) && !this.options.forwardOnly);
			this._buttons.responsiveNextButton.attr('disabled', this._isLastStep(this._activeStepId));
			
			this._buttons.submitButton.attr('disabled', !this._isLastStep(this._activeStepId));
		}, 
		
		_generateRandomId: function() {
			var guid = new Date().getTime().toString(32), i;

			for (i = 0; i < 5; i++) {
				guid += Math.floor(Math.random() * 65535).toString(32);
			}

			return 'wzd_' + guid;
		}, 
		
		_beforeTransition: function() {
			this._locked = true;
		}, 

		_afterTransition: function() {
			this.options.onStepShown && $.isFunction(this.options.onStepShown) && 
				this.options.onStepShown.apply(this, [ this, this._activeStep ]);
				
			this._locked = false;
			this._refreshButtons();
		}, 
		
		// Public methods
		prevStep: function() {
			if(!this._isFirstStep(this._activeStepId)) {
				var step = this._getStepById(this._activeStepId);
				if(step) {
					var prevStep = $(step).prev(this.options.element);
					if(prevStep && prevStep.length)
						this._activateStep(prevStep.data('step-id'));
				}
			}
		}, 
		
		nextStep: function() {
			if(!this._isLastStep(this._activeStepId)) {
				var step = this._getStepById(this._activeStepId);
				if(step) {
					var nextStep = $(step).next(this.options.element);
					if(nextStep && nextStep.length)
						this._activateStep(nextStep.data('step-id'));
				}
			}
		}, 
		
		submitForm: function() {
			var shouldSubmit = true;
			if(this.options.onBeforeSubmit && $.isFunction(this.options.onBeforeSubmit)) {
				shouldSubmit = this.options.onBeforeSubmit.apply(self, [this, this, this.element[0]])
			}
			
			shouldSubmit && this.element.submit();
		}, 
		
		reset: function() {
			this._steps.hide();
			this.goToStep(1);
			this._refreshButtons();
		}, 
		
		goToStep: function(step) {
			if(--step < 0 || step++ >= this._steps.length
				|| !(stepId = $(this._steps[ step - 1 ]).attr('data-step-id'))) return;
			
			this._activateStep(stepId);
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

				this.options[ key ] = value;
			}

			return this;
		}
	}
	
	$.fn.wizard = function(options) {

		var isMethodCall = typeof options === "string",
			args = Array.prototype.slice.call( arguments, 1 ),
			returnValue = this;

		// prevent calls to internal methods
		if ( isMethodCall && options.charAt( 0 ) === "_" ) {
			return returnValue;
		}

		if ( isMethodCall ) {
			this.each(function() {
				var instance = $.data( this, 'wizard' ),
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
				var instance = $.data( this, 'wizard' );
				if ( !instance ) {
					$.data( this, 'wizard', new Wizard( this, options ) );
				}
			});
		}

		return returnValue;
	};

})(jQuery, window , document);
