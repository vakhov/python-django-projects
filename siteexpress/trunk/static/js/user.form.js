$(document).ready(function() {

	if (readCookie('wrote_form') != '') {
		cur_date = new Date();
		msg_date = new Date(readCookie('wrote_form'));
		diff = cur_date.getMinutes() - msg_date.getMinutes();
		if (diff < 1000 && diff > 0) {
		//	$('#r_form').hide();
		//	$('#r_thankyou').show();
		}
	}
	
	$('#r_submit').click( function() {
	
		author = $('#r_autor').val();
		contact = $('#r_cont').val();
		message = $('#r_mes').val();
		
		// Создаем запрос
		query = { 
			id: '', query: [
			{ 	type: 'insert',
				rel: 'simpleform',
				id: '',
				rows: [
					{ field: { name:'author', value:author.replace(/&/g, '%26') } },
					{ field: { name:'contact', value:contact.replace(/&/g, '%26') } },
					{ field: { name:'message', value:message.replace(/&/g, '%26') } }
				]
			}
		] };
		query = $.toJSON(query);
		
		callback = function() {
			document.cookie = 'wrote_form='+new Date();
			$('#r_form').hide();
			$('#r_thankyou').show();
		}
						
		$.post('/index.php?port=direct', 'query=' + query, callback);
		
		return false;

	});

});