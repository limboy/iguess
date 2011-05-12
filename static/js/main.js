//{{{Placeholder
/*****************************************************************************
jQuery Placeholder 1.1.1

Copyright (c) 2010 Michael J. Ryan (http://tracker1.info/)

Dual licensed under the MIT and GPL licenses:
	http://www.opensource.org/licenses/mit-license.php
	http://www.gnu.org/licenses/gpl.html

------------------------------------------------------------------------------

Sets up a watermark for inputted fields... this will create a LABEL.watermark 
tag immediately following the input tag, the positioning will be set absolute, 
and it will be positioned to match the input tag.

To activate on all tags with a 'data-watermark' attribute:

	$('input[placeholder],textarea[placeholder]').placeholder();


To style the tags as appropriate (you'll want to make sure the font matches):

	label.placeholder {
		cursor: text;				<--- display a cursor to match the text input

		padding: 4px 4px 4px 4px;   <--- this should match the border+padding 
											for the input field(s)
		color: #999999;				<--- this will display as faded
	}

You'll also want to have the color set for browsers with native support
	input:placeholder, textarea:placeholder {
		color: #999999;
	}
	input::-webkit-input-placeholder, textarea::-webkit-input-placeholder {
		color: #999999;
	}

------------------------------------------------------------------------------

Thanks to...
	http://www.alistapart.com/articles/makingcompactformsmoreaccessible
	http://plugins.jquery.com/project/overlabel

	This works similar to the overlabel, but creates the actual label tag
	based on a data-watermark attribute on the input tag, instead of 
	relying on the markup to provide it.

*****************************************************************************/
(function($){
	
	var ph = "PLACEHOLDER-INPUT";
	var phl = "PLACEHOLDER-LABEL";
	var boundEvents = false;
	var default_options = {
		labelClass: 'placeholder'
	};
	
	//check for native support for placeholder attribute, if so stub methods and return
	var input = document.createElement("input");
	if ('placeholder' in input) {
		$.fn.placeholder = $.fn.unplaceholder = function(){}; //empty function
		delete input; //cleanup IE memory
		return;
	};
	delete input;

	$.fn.placeholder = function(options) {
		bindEvents();

		var opts = $.extend(default_options, options)

		this.each(function(){
			var rnd=Math.random().toString(32).replace(/\./,'')
				,input=$(this)
				,label=$('<label style="position:absolute;display:none;top:0;left:0;"></label>');

			if (!input.attr('placeholder') || input.data(ph) === ph) return; //already watermarked

			//make sure the input tag has an ID assigned, if not, assign one.
			if (!input.attr('id')) input.attr('id') = 'input_' + rnd;

			label	.attr('id',input.attr('id') + "_placeholder")
					.data(ph, '#' + input.attr('id'))	//reference to the input tag
					.attr('for',input.attr('id'))
					.addClass(opts.labelClass)
					.addClass(opts.labelClass + '-for-' + this.tagName.toLowerCase()) //ex: watermark-for-textarea
					.addClass(phl)
					.text(input.attr('placeholder'));

			input
				.data(phl, '#' + label.attr('id'))	//set a reference to the label
				.data(ph,ph)		//set that the field is watermarked
				.addClass(ph)		//add the watermark class
				.after(label);		//add the label field to the page

			//setup overlay
			itemIn.call(this);
			itemOut.call(this);
		});
	};

	$.fn.unplaceholder = function(){
		this.each(function(){
			var	input=$(this),
				label=$(input.data(phl));

			if (input.data(ph) !== ph) return;
				
			label.remove();
			input.removeData(ph).removeData(phl).removeClass(ph);
		});
	};


	function bindEvents() {
		if (boundEvents) return;

		//prepare live bindings if not already done.
		$('.' + ph)
			.live('click',itemIn)
			.live('focusin',itemIn)
			.live('focusout',itemOut);
		bound = true;

		boundEvents = true;
	};

	function itemIn() {
		var input = $(this)
			,label = $(input.data(phl));

		label.css('display', 'none');
	};

	function itemOut() {
		var that = this;

		//use timeout to let other validators/formatters directly bound to blur/focusout work first
		setTimeout(function(){
			var input = $(that);
			$(input.data(phl))
				.css('top', input.position().top + 'px')
				.css('left', input.position().left + 'px')
				.css('display', !!input.val() ? 'none' : 'block');
		}, 200);
	};

}(jQuery));
//}}}

//{{{color
/*
 * jQuery Color Animations
 * Copyright 2007 John Resig
 * Released under the MIT and GPL licenses.
 */

(function(jQuery){

	// We override the animation for all of these color styles
	jQuery.each(['backgroundColor', 'borderBottomColor', 'borderLeftColor', 'borderRightColor', 'borderTopColor', 'color', 'outlineColor'], function(i,attr){
		jQuery.fx.step[attr] = function(fx){
			if ( fx.state == 0 ) {
				fx.start = getColor( fx.elem, attr );
				fx.end = getRGB( fx.end );
			}

			fx.elem.style[attr] = "rgb(" + [
				Math.max(Math.min( parseInt((fx.pos * (fx.end[0] - fx.start[0])) + fx.start[0]), 255), 0),
				Math.max(Math.min( parseInt((fx.pos * (fx.end[1] - fx.start[1])) + fx.start[1]), 255), 0),
				Math.max(Math.min( parseInt((fx.pos * (fx.end[2] - fx.start[2])) + fx.start[2]), 255), 0)
			].join(",") + ")";
		}
	});

	// Color Conversion functions from highlightFade
	// By Blair Mitchelmore
	// http://jquery.offput.ca/highlightFade/

	// Parse strings looking for color tuples [255,255,255]
	function getRGB(color) {
		var result;

		// Check if we're already dealing with an array of colors
		if ( color && color.constructor == Array && color.length == 3 )
			return color;

		// Look for rgb(num,num,num)
		if (result = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(color))
			return [parseInt(result[1]), parseInt(result[2]), parseInt(result[3])];

		// Look for rgb(num%,num%,num%)
		if (result = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(color))
			return [parseFloat(result[1])*2.55, parseFloat(result[2])*2.55, parseFloat(result[3])*2.55];

		// Look for #a0b1c2
		if (result = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(color))
			return [parseInt(result[1],16), parseInt(result[2],16), parseInt(result[3],16)];

		// Look for #fff
		if (result = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(color))
			return [parseInt(result[1]+result[1],16), parseInt(result[2]+result[2],16), parseInt(result[3]+result[3],16)];

		// Otherwise, we're most likely dealing with a named color
		return colors[jQuery.trim(color).toLowerCase()];
	}
	
	function getColor(elem, attr) {
		var color;

		do {
			color = jQuery.curCSS(elem, attr);

			// Keep going until we find an element that has color, or we hit the body
			if ( color != '' && color != 'transparent' || jQuery.nodeName(elem, "body") )
				break; 

			attr = "backgroundColor";
		} while ( elem = elem.parentNode );

		return getRGB(color);
	};
	
	// Some named colors to work with
	// From Interface by Stefan Petre
	// http://interface.eyecon.ro/

	var colors = {
		aqua:[0,255,255],
		azure:[240,255,255],
		beige:[245,245,220],
		black:[0,0,0],
		blue:[0,0,255],
		brown:[165,42,42],
		cyan:[0,255,255],
		darkblue:[0,0,139],
		darkcyan:[0,139,139],
		darkgrey:[169,169,169],
		darkgreen:[0,100,0],
		darkkhaki:[189,183,107],
		darkmagenta:[139,0,139],
		darkolivegreen:[85,107,47],
		darkorange:[255,140,0],
		darkorchid:[153,50,204],
		darkred:[139,0,0],
		darksalmon:[233,150,122],
		darkviolet:[148,0,211],
		fuchsia:[255,0,255],
		gold:[255,215,0],
		green:[0,128,0],
		indigo:[75,0,130],
		khaki:[240,230,140],
		lightblue:[173,216,230],
		lightcyan:[224,255,255],
		lightgreen:[144,238,144],
		lightgrey:[211,211,211],
		lightpink:[255,182,193],
		lightyellow:[255,255,224],
		lime:[0,255,0],
		magenta:[255,0,255],
		maroon:[128,0,0],
		navy:[0,0,128],
		olive:[128,128,0],
		orange:[255,165,0],
		pink:[255,192,203],
		purple:[128,0,128],
		violet:[128,0,128],
		red:[255,0,0],
		silver:[192,192,192],
		white:[255,255,255],
		yellow:[255,255,0]
	};
	
})(jQuery);

//}}}

$(function(){
    $('#entity-list').delegate('.c-answer', 'click', function(e){
        e.preventDefault();
        $(this).next().show();
    });

    $('#publish form').submit(function(e){
        e.preventDefault();
        var $self = $(this);
		var $sub_btn = $self.find('.btn');
		if($sub_btn.hasClass('disabled')){
			return false;
		}

		$sub_btn.addClass('disabled');
		$sub_btn.val('正在提交...');
	
        $.post('/publish', $self.serialize(), function(result) {
            if(result.status == 'ok') {
                $tpl = $('#segment-tpl').clone();
                $tpl.removeAttr('id');
                $tpl.find('.sentence').text(result.content.sentence);
                $tpl.find('.answer').text(result.content.answer);
                $('#segment-tpl').after($tpl);
                $tpl.css('background', '#FBF9EA').show().animate({
                    'backgroundColor': '#fff'
                }, 2000, function(){
                    $tpl.css('background', 'transparent')
                });

				$self.find('textarea').text('').get(0).focus();
				$self.find('input[type="text"]').val('');
				$sub_btn.addClass('disabled');
				$sub_btn.val('让他们猜去吧');

            }
        }, 'json');
    });

	var sentence_entered = false;
	var answer_entered = false;

	$('#publish form').find('textarea').keyup(function(e) {
		var $form = $('#publish form');
		if($.trim($(this).val()) != '') {
			sentence_entered = true;
			if(answer_entered) {
				$form.find('.btn').removeClass('disabled');
			}
		} else {
			sentence_entered = false;
			$form.find('.btn').addClass('disabled');
		}
	});

	$('#publish form').find('input[type="text"]').keyup(function(e) {
		var $form = $('#publish form');
		if($.trim($(this).val()) != '') {
			answer_entered = true;
			if(sentence_entered) {
				$form.find('.btn').removeClass('disabled');
			}
		} else {
			answer_entered = false;
			$form.find('.btn').addClass('disabled');
		}
	});

    var deal_vote = function($vote_btn, mark) {
        if($vote_btn.hasClass('disabled'))
            return;

        $parent = $vote_btn.parent();
        $parent.find('a').addClass('disabled');
        var $mark = $parent.find('.mark');
        var origin_mark = parseInt($mark.text());
        $mark.text(origin_mark+parseInt(mark));

        var id = $vote_btn.parent().parent().attr('id');
        $.post('/vote', {'entity': id, 'mark': mark}, function(result) {
            if(result.status == 'ok') {
            }
        }, 'json');
    }

    $('#entity-list').delegate('.upvote', 'click', function(e) {
        e.preventDefault();
        deal_vote($(this), 1);
    });

    $('#entity-list').delegate('.downvote', 'click', function(e) {
        e.preventDefault();
        deal_vote($(this), -1);
    });

	var loc = window.location.toString();
	if (loc.indexOf('/hot') != -1){
		$('#entity-list .hot').addClass('selected');
	} else if (loc.indexOf('/top') != -1) {
		$('#entity-list .top').addClass('selected');
	} else {
		$('#entity-list .latest').addClass('selected');
	}

	$('.page_btn').live('click', function(e){
		e.preventDefault();
		var $self = $(this);
		var href = $self.attr('href');
		$.getJSON(href, function(result){
			$self.hide().after(result.content.html);
		});
	});

    if($.browser.webkit) {
        $('ul.type li').css('line-height', '27px');
    }
});
