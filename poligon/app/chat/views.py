# -*- coding: utf8 -*-

import json
import hashlib
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404

from models import *

TIME_DELTA = 600 #seconds = 10 min


def dumps(dict):
	return json.dumps(dict)

def loads(str):
	return json.loads(str)

def time_now():
	return datetime.datetime.now()


def index(req):
	return HttpResponse('OK')

# def reg(req):
# 	context = RequestContext(req)
# 	context['form'] = UserForm()
# 	return render_to_response('chat/reg.html', context)

@csrf_exempt
def login(req):
	context = RequestContext(req)
	if req.method == 'POST':
		form = UserForm(req.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				user = User.objects.get(login=cd['login'])
				pwd = hashlib.md5(cd['login']).hexdigest()
				return HttpResponse('ok')
				if user.password != pwd:
					context['error_pwd'] = u'Пароль не верен'
					return render_to_response('chat/login.html', context)
				else:
					session = req.session
					time_now = time_now()
					session[hashlib.md5(time_now).hexdigest()] = dumps({
										'time': time_now,
										'id': user.id
									})
					return HttpResponseRedirect('chat/%s/' % (session['hash'],))
			except:
				context['error_login'] = u'Пользователь с логином %s не существует' % cd['login']
				return render_to_response('chat/login.html', context)

		context['form'] = form
		return render_to_response('chat/login.html', context)

	context['form'] = UserForm()
	return render_to_response('chat/login.html', context)

def chat(req, hash):
	context = RequestContext(req)
	try:
		auth = load(req.session[hash])
		time_delta = time_now() - auth['time']
		if time_delta > TIME_DELTA:
			del req.session['hash']
			return HttpResponse('Сессия закрыта')
		else:
			return HttpResponse('Приветствуем')
	except:
		return HttpResponseRedirect('/chat/')

def meta(req):
	val = req.session.items()
	val.sort()
	html=[]
	for k,v in val:
		html.append('<tr><td>%s</td><td>%s</td></tr>'%(k,v))
	return HttpResponse('<table>%s</table>'%'\n'.join(html))
