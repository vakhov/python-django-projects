$(document).ready(function() {
	$('<div rel="hideLink" style="display:none;"></div>').appendTo($('body'));
	
	var i = 0;
	$('.catalogItem__small dt a, .catalogItem dt a').each(function() {
		i++
		$('<a href="' + $(this).attr('href') + '" id="popUp' + i + '" rel="hidePopUp">' + $(this).text() + '</a>').appendTo('div[rel=hideLink]');
		$(this).attr('id', 'Up' + i);
		$(this).unbind('click').click(function() {
			$.fancybox.showActivity;
			$('#pop' + $(this).attr('id')).click();
			return false;
		});
		$(this).parent().parent().find('.photo a').unbind('click').attr('id', 'Up' + i).click(function() {
			$.fancybox.showActivity;
			$('#pop' + $(this).attr('id')).click();
			return false;
		});
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
});