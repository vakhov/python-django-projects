var interval = 10000;
var intervalID;


function keyValue(evt)
		{
			if(!evt) evt = event;
			if(evt.keyCode == 13 && evt.ctrlKey) sendMessage();
		}
		

function trim(message)
{
	var messageTrim = message.value.replace(/^\s+/, "").replace(/\s+$/, "");;
	if(messageTrim.length)
		return messageTrim;
	else
		return false;
}

function sendMessage()
{
	var message = window.document.getElementById('id_message');
	if(!message.value)
	{
		message.className = 'error';
		alert('Поле отправки пусто. Введите сообщение!');
		message.focus();
	}
	else if(!trim(message))
	{
		message.className = 'error';
		alert('Вы не ввели текст сообщения. Введите сообщение!');
		message.value = '';
		message.focus();
	}
	else
	{
		$.post("/api/chat/get/",
				{
					'message': $('textarea').val(),
					'csrfmiddlewaretoken': $('input').val()
				},
				function (out){
					getMessage();
					Interval(interval);
				}
		);
		message.value = '';
		message.focus();
		Interval(interval);
		return false;
	}
}

function getMessage(){
	$("#window_chat").load("/api/chat/message/");
}

function Interval(time){
	if(intervalID){
		clearInterval(intervalID)
	}
	intervalID = setInterval(getMessage, interval);
}

function locate(href){
	location.replace(href);
}

$(document).ready(function() {
	window.document.getElementById('button').onclick = sendMessage;
	window.document.getElementById('id_message').onkeydown = keyValue;
	getMessage();
	Interval(interval);
});

