//$('a').addClass('hide');

$(document).ready(function() {
	
	$('#modal1, #modal2, #modal3').each(function() {
		$(this).fancybox({
			'width'				: '100%',
			'height'			: '100%',
	        'autoScale'     	: false,
	        'transitionIn'		: 'none',
			'transitionOut'		: 'none',
			'type'				: 'iframe',
			'overlayOpacity'	: 0.9,
			'href'				: $(this).attr('href') + '?ajax=1',
			'title'				: $(this).text(),
			});
	});

//------------popUp Window Position----------------------
	$('<div rel="hideLink" style="display:none;"></div>').appendTo($('body'));
	
	var i = 0;
	$('a[class*=catalog_list]').each(function() {
		$('<a href="' + $(this).attr('href') + '" id="popUp' + ++i + '" rel="hidePopUp">' + $(this).find('.catalog_list_name').text() + '</a>').appendTo('div[rel=hideLink]');
	});
	
	$('a[rel=hidePopUp]').each(function() {
		$(this).fancybox({
            'width'				: '85%',
            'height'			: '95%',
            'autoScale'     	: false,
            'transitionIn'		: 'elastic',
            'transitionOut'		: 'elastic',
            'type'				: 'iframe',
            'overlayOpacity'	: 0.7,
            'href'				: $(this).attr('href') + '?ajax=1',
            'title'				: $(this).text(),
        });
	});
	
	var j = 0;
	$('.submitPopUp').each(function() {
		$(this).attr('id', 'Up' + ++j);
		$(this).click(function() {
			$.fancybox.showActivity;
			$('#pop' + $(this).attr('id')).click();
			return false;
		});
	});
	
	
//------------popUp Window Position----------------------

//----------------WTP START----------------
	$('#wtp').click(function(event) {
		$.fancybox({
            'width'				: '90%',
            'height'			: '90%',
            'autoScale'     	: false,
            'transitionIn'		: 'elastic',
            'transitionOut'		: 'elastic',
            'type'				: 'iframe',
            'overlayOpacity'	: 0.9,
            'href'				: $(this).attr('href'),
            //'title'				: $(this).text(),
            'onClosed'			: function() {
            	location.reload();
            }
        });
		return false;
	});
    
    $('ul#wtp_list a+div').css('display', 'none');
	
	$('ul#wtp_list a').click(function(event) {
		var id = $(this).attr('id');
		if($('#' + id + '+div').text()){
			$('#' + id).next().slideToggle();
		}else{
			$.ajax({
				async: true,
				type: 'POST',
				url: '/api/wtp/wtp_catalog/' + $('input[type=hidden]').val() + '/',
				data: {
					'current_section' : $(this).attr('href')
				},
				success: function(data){
					$('#' + id).next().slideToggle();
					$('#' + id + '+div').html(data);
				}
			});
		}
		return false;
	});
    
    function check() {
       $('.wtp_catalog_image').each(function(event) {
    	   $(this).unbind('click');
    	   $(this).click(function() {
    		   var currentThis = $(this)
    		   if($(this).hasClass('check')){
    			   $.ajax({
    					async: true,
    					type: 'POST',
    					url: '/api/wtp/del/' + $('input[type=hidden]').val() + '/' + $(this).attr('wtp_id') + '/',
    					data: {
    						'current_section' : $(this).attr('href')
    					},
    					success: function(data){
    						currentThis.removeClass('check');
    					}
    				});
    		   }else{
    			   $.ajax({
   					async: true,
   					type: 'POST',
   					url: '/api/wtp/add/' + $('input[type=hidden]').val() + '/' + $(this).attr('wtp_id') + '/',
   					data: {
   						'current_section' : $(this).attr('href')
   					},
   					success: function(data){
   						currentThis.addClass('check');
   					}
   				});
    		   }
    	   });
       });
    }
    
    setInterval(check, 100);
//----------------WTP STOP----------------
    
});
