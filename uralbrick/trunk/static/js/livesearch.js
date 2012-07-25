//function parseJSON(data) {
//    return window.JSON && window.JSON.parse ? window.JSON.parse( data ) : (new Function("return " + data))(); 
//}
var auto = [];

function livesearch(){
	var search = $("#livesearch").val();
	if(search.length >= 2){
		$.ajax({
			type: 'POST',
			url: "/api/livesearch/",
			data: {'search': search},
			success: function(response){
				if(response){
					var html = '';
					auto = [];
					response = JSON.parse(response)
					$.each(response, function() {
						html += 'Слово: ' + this.text.replace(search, '<span style="background:green;">' + search + '</span>') + ', перевод: ' + this.perevod + '<br />';
						auto.push(this.text);
					});
					console.log(auto);
					$("#livesearch").autocomplete(auto, {
						width: 200,
					});
					$("#liveoutput").html(html);
				}else{
					$('#liveoutput').html('')
				}
			},
			error:function(e,r,s){
				$("#liveoutput").html('Error' + e.responseText);
			}
		});
	}else{
		$("#liveoutput").html("");
	}
	return false;
}
$(document).ready(function() {
	$("#livesearch").keyup(livesearch);
	$("#livesearch").change(function(){
		window.setTimeout(livesearch, 110);
	});
});