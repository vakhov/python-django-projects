# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from models import Chat
from models import ChatForm, LoginForm
from chat import ChatClass
from decorator import is_session

import datetime

@is_session
def get_message(request):
    context = RequestContext(request)
    chat = ChatClass(request.session)
    context['messages'] = Chat.objects.filter(session=chat.get_session()).order_by('-id')
    return render_to_response('chat/get_message.html', context)

@is_session
@csrf_exempt
def save_message(request):
    context = RequestContext(request)
    chat = ChatClass(request.session)
    if request.method == 'POST':
        send = Chat(
                    name = chat.get_login(),
                    message = unicode(request.POST['message']),
                    time = datetime.datetime.now(),
                    session = chat.get_session()
                )
        send.save()
    return get_message(request)
    