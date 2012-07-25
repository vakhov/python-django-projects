$(document).ready(function() {

	if (readCookie('voted') == $.md5($('#votequestion').text())) {
		$('#voteform').hide();
	}
	else {
		$('#voteresults').hide();
	}
	
	$('.do_answer').click( function() {
		
		ansid = $(this).attr('id');
		ansid = ansid.substring(ansid.indexOf('_')+1);

		// Создаем запрос
		query = { 
			id: '', query: [
			{ 	type: 'execute',
				rel: 'vote',
				id: '',
				action: { name:'doVote', value:ansid }
			}
		] };
		query = $.toJSON(query);
		
		callback = function() {
			new_total_count = parseInt($('#votecounter').text()) + 1;
			new_answer_count = parseInt($('#votesmall_'+ansid).text()) + 1;

			$('#votecounter').text(new_total_count);
			$('#votesmall_'+ansid).text(new_answer_count);
			
			// бежим по всем голосованиям ...
			$("#voteresults small").each(function() {
			// ... пересчитываем их процент ...
				cur_small_count = $(this).text();
				cur_percent = cur_small_count/new_total_count*100 + "%";
			// ... и назначаем стили
				$(this).parent().css("width",cur_percent);
			});
			// Меняем голосовалку на результаты			
			$('#voteform').hide();
			$('#voteresults').show();
			
			// Пишем куку
			document.cookie = 'voted='+$.md5($('#votequestion').text());
			
		}
						
		$.post('/index.php?port=direct', 'query=' + query, callback);
		
		return false;

	});

});