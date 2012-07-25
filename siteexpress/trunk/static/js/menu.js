// Menu

$(document).ready(function(){
	/*$("#menu li a").click(function() {
		$(this).parent().parent().find("ul").fadeOut();
		$("#menu li a").removeClass("nolink");
		if ($(this).parent().parent().parent().attr("id")!="menu") $(this).parent().parent().parent().find("a:first").addClass("nolink")
		if($(this).parent().find("ul").length!=0) {
			if ($(this).parent().find("ul:first").css("display")=="none") {$(this).parent().find("ul:first").fadeIn(); $(this).addClass("nolink"); }
			else {$(this).parent().find("ul:first").fadeOut(); $(this).removeClass("nolink"); }
			return false;
		}
	});
	$("#menu").mouseout(function() {
		$("body").click(function() { $("#menu ul ul").fadeOut(); $("#menu li a").removeClass("nolink"); })
	});
	*/
	if ($('#section-id').length) {
		var id = $('#section-id').text();
		
		//$('#menu ul:has(#item-'+id+')').show();
		$('#item-'+id).parents('ul').show();
		$('#item-'+id).children().show();

		//$('#menu ul:has(#item-'+id+')').children('li').children('ul').show();
		$('#item-'+id).children('a').css('font-style', 'italic').css('text-decoration', 'none');
	}
			
});
