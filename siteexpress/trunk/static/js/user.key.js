$(document).ready(function() {
	$('#key').click(function() {
		box = new Boxy("", {
			title: "Вход в систему управления", 
			modal:true
		});
		box.setContent($('#login'));
		box.center();
		$('#password').focus();
		return false;
	});
});