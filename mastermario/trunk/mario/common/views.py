# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)

def text(request):
    context = RequestContext(request)
    return render_to_response('text.html', context)
