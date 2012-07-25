Aphaline.Legacy = (function() {
	
	/*
	 * Last mouse X and Y while moving around #adminblock (to handle moving to buttons) 
	 */
	var mousecache = {
		x: 0,
		y: 0
	};

	/*
	 * Here will be the object which is under administration 
	 */
	var context = {};

	/*
	 * Function to initialize TinyMCEs
	 */
//	var init_tinymce = function() {
//		var mces = $('.fck');
//		mces.each(function() {
//			var id = $(this).attr('id');
//			tinyMCE.execCommand("mceAddControl", false, id);
//		});
//	}

		
	/*
	 * Handling aph-blocks' mouseenter
	 */
	$('[aph-block-type]')
	.css ({
		'border': '1px dashed #aaa',
		'cursor': 'pointer',
		'min-height': '20px'
	})
	.mouseenter (
		function(evt) {
			var offset = $(this).offset();
			var w = $(this).outerWidth();
			var h = $(this).outerHeight();
			var mouseX = mousecache.x = evt.pageX;
			var mouseY = mousecache.y = evt.pageY;
			$('#adminblock').css({
				'width': 	w + 'px', 
				'height': 	h + 'px',
				'top': 		offset.top + 'px',
				'left': 	offset.left + 'px'
			}).show();
			$('#adminbutton').css({
				'top': 		mouseY - 3 + 'px',
				'left':		mouseX + 10 + 'px'
			}).show();
			$('#adminbutton div').css({
				'border-radius': '0',
				'-moz-border-radius': '0',
				'-webkit-border-radius': '0',
				'opacity': '0.7'
			}).hide();
			var type = $(this).attr('aph-block-type');
			if (type.indexOf('e') != -1) $('#adminbutton #aph-button-edit').show();
			if (type.indexOf('g') != -1) $('#adminbutton #aph-button-go').show();
			if (type.indexOf('d') != -1) $('#adminbutton #aph-button-delete').show();
			$('#adminbutton div:visible').first().css({
				'-webkit-border-bottom-left-radius': '20px',
				'-moz-border-radius-bottomleft': '20px',
				'border-bottom-left-radius': '20px',
				'-webkit-border-top-left-radius': '20px',
				'-moz-border-radius-topleft': '20px',
				'border-top-left-radius': '20px',
				'opacity': '1'
			});
			$('#adminbutton div:visible').last().css({
				'-webkit-border-bottom-right-radius': '20px',
				'-moz-border-radius-bottomright': '20px',
				'border-bottom-right-radius': '20px',
				'-webkit-border-top-right-radius': '20px',
				'-moz-border-radius-topright': '20px',
				'border-top-right-radius': '20px'
			});
			context = $(this);
		}
	);
	
	/*
	 * Handling some interface stuff about admin blocks and buttons
	 */
	$('#adminblock')
	.mouseout (
		function(evt) {
			if (
				evt.relatedTarget 
				&& evt.relatedTarget.className != 'adminbutton'
				&& evt.relatedTarget.id != 'adminbutton'
			) {
				$(this).hide();
				$('#adminbutton').hide();
				$('#adminbutton div').hide().css({
					'border-radius': '0',
					'-moz-border-radius': '0',
					'-webkit-border-radius': '0'
				});
			}
		}
	)
	.mousemove (
		function(evt) {
			var mouseX = evt.pageX;
			var mouseY = evt.pageY;
			var offset = $('#adminbutton').offset();
			var h = $('#adminbutton').height();
			var w = $('#adminbutton').width();
			if (
				mouseX < mousecache.x 
				|| mouseY < mousecache.y 
				|| mouseY > offset.top + h 
				|| mouseX > offset.left + w
			) {
				$('#adminbutton').css({
					'top': 		mouseY - 3 + 'px',
					'left':		mouseX + 10 + 'px'
				});
			}
			mousecache.x = mouseX;
			mousecache.y = mouseY;
		}
	)
	.click (
		function() {
			$('#adminbutton div:visible').first().trigger('click');
		}
	);

	$('#adminbutton')
	.mouseout (
		function(evt) {
			if (evt.relatedTarget && evt.relatedTarget.id != 'adminblock' && evt.relatedTarget.className != 'adminbutton') {
				$(this).hide();
				$('#adminblock').hide();
				$('#adminbutton div').hide();
			}
		}
	);

	$('#adminbutton div').hover(
		function() {
			$('#adminbutton div').css('opacity', '0.7');
			$(this).css('opacity', '1');
		},
		function() {
			$('#adminbutton div').css('opacity', '0.7');
			$('#adminbutton div:visible').first().css('opacity', '1');
		}
	);

	/*
	 * Redirector
	 */
	$('#aph-button-go').click(function() {
		var url = context.attr('aph-redirect-url');
		if (url) window.location.href = url;
		return false;
	});
	
	/*
	 * Deleter
	 */
	$('#aph-button-delete').click(function() {
		Boxy.ask('Вы действительно хотите удалить этот элемент?', ['Удалить', 'Отмена'], function(response) {
            if (response == 'Удалить') {
            	var callback = function(result) {
            		window.location.reload();
            	}
            	var errback = function(error) {
            		var message = 'При удалении элемента возникла ошибка. <br/><br/>Описание ошибки: <b>"'+error.message+'"</b>.<br/>Пожалуйста, сообщите о ней администратору сайта.<br/><br/>';
            		Boxy.alert(message);
            	}
            	var model = context.attr('aph-model');
            	var id = context.attr('aph-id');
            	if (!model || !id) {
            		errback({message: 'EmptyModelOrConditions'});
            	}
            	else {
            		Aphaline.API.Legacy.delete(model, id, callback, errback);
            	}
            }
        });
		return false;
	});
	
	/*
	 * Editor-updater
	 */
	$('#aph-button-edit').click(function() {
		// Creating the form
		var model = context.attr('aph-model');
		var id = context.attr('aph-id');
		
		// Setting callbacks and errbacks
		var callback = function() {}
		var errback = function() {}

		var form = Aphaline.API.Legacy.form(model, id, {}, callback, errback);
		Aphaline.Editor.openContent(form);
		
		return false;
	});

	/*
	 * Finaly, adder. Adder is kinda special thing.
	 */
	$('[aph-adder]').click(function() {
		// Creating the form
		var model = $(this).attr('aph-model');
		
		// Setting callbacks and errbacks
		var callback = function() {}
		var errback = function() {}

		var initial = $(this).attr('aph-initial');
			var data = {}
			if (initial) {
				var foo = initial.trim().split(',');
				for (var i in foo) {
					var bar = foo[i].trim().split('=');
					data[bar[0]] = bar[1];
				}
			}
		var form = Aphaline.API.Legacy.form(model, null, data, callback, errback);
		Aphaline.Editor.openContent(form, "Создание объекта");
		
		return false;
	});
	
	return {}

})();