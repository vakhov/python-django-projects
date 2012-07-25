# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from documents.models import Document
from django.contrib.auth.models import User

def index(request):
    context = RequestContext(request)
    if context['user'].is_anonymous():
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/home/')

def home(request):
    context = RequestContext(request)
    if context['user'].is_anonymous():
        return HttpResponseRedirect('/login/')
    else:
        context['documents'] = Document.objects.filter(owner=context['user'])
        return render_to_response('home.html', context)