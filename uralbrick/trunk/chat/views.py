# -*- coding: utf8 -*-

import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from models import Chat
from models import ChatForm, LoginForm
from chat import ChatClass

from decorator import is_session

@csrf_exempt
def login(request, name=None):
    context = RequestContext(request)
    
    if request.method == 'GET':
        context['form'] = LoginForm()
    else:
        session = ChatClass(request.session, unicode(request.POST['login']))
        
        return HttpResponseRedirect('room/')
    
    return render_to_response('chat/login.html', context)

@is_session
@csrf_exempt
def room(request):
    context = RequestContext(request)
    context['form'] = ChatForm()
    return render_to_response('chat/room.html', context)

def clear(request):
    context = RequestContext(request)
    chat = ChatClass(request.session)
    chat.clear()
    return render_to_response('chat/logout.html', context)
