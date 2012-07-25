$(document).ready(function() {
	$('#change_collection').click(function(event) {
		$.fancybox({
            'width'				: '90%',
            'height'			: '90%',
            'autoScale'     	: false,
            'transitionIn'		: 'elastic',
            'transitionOut'		: 'elastic',
            'type'				: 'iframe',
            'overlayOpacity'	: 0.9,
            'href'				: $(this).attr('href'),
            'onClosed'			: function() {
            	location.reload();
            }
        });
		return false;
	});
    
    $('ul#collection_list a+div').css('display', 'none');
	
	$('ul#collection_list a').click(function(event) {
		var id = $(this).attr('id');
		if($('#' + id + '+div').text()){
			$('#' + id).next().slideToggle();
		}else{
			$.ajax({
				async: true,
				type: 'POST',
				url: '/api/add_collection/catalog/' + $('input[type=hidden]').val() + '/',
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
       $('.collection_catalog_image').each(function(event) {
    	   $(this).unbind('click');
    	   $(this).click(function() {
    		   var currentThis = $(this)
    		   if($(this).hasClass('check')){
    			   $.ajax({
    					async: true,
    					type: 'POST',
    					url: '/api/add_collection/del/' + $('input[type=hidden]').val() + '/' + $(this).attr('wtp_id') + '/',
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
   					url: '/api/add_collection/add/' + $('input[type=hidden]').val() + '/' + $(this).attr('wtp_id') + '/',
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
    
    interval_collection = setInterval(check, 100);
});
