$(document).ready(function() {

	if (readCookie('wrote_qa') != '') {
		cur_date = new Date();
		msg_date = new Date(readCookie('wrote_qa'));
		diff = cur_date.getMinutes() - msg_date.getMinutes();
		//alert(diff);
		if (diff < 1) {
			$('#q_form').hide();
			$('#q_thankyou').show();
		}
	}
	
	$('#q_submit').click( function() {
	
		author = $('#q_autor').val();
		message = $('#q_mes').val();
		
		// Создаем запрос
		query = { 
			id: '', query: [
			{ 	type: 'insert',
				rel: 'qa',
				id: '',
				rows: [
					{ field: { name:'author', value:author.replace(/&/g, '%26') } },
					{ field: { name:'message', value:message.replace(/&/g, '%26') } }
				]
			}
		] };
		query = $.toJSON(query);
		
		callback = function() {
			// Пишем куку
			document.cookie = 'wrote_qa='+new Date();
			// Перезагружаем страничку
			window.location.reload();
		}
						
		$.post('/index.php?port=direct', 'query=' + query, callback);
		
		return false;

	});

});