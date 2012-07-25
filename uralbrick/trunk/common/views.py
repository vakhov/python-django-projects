# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from json import dumps

from catalog.models import Catalog

def index(request):
	context = RequestContext(request)
	context['catalogs'] = Catalog.objects.all()
	return render_to_response('index.html', context)

def text(request):
	context = RequestContext(request)
	context['catalogs'] = Catalog.objects.all()
	return render_to_response('text.html', context)

def json(request):
	items = Catalog.objects.values('big_sharp_picture', 'name_long', 'description', 'link_text', 'small_thumb', 'name_short')
	for i in xrange(len(items)):
		items[i]['id'] = i
	json_list = list(items)
	json = dumps(json_list)
	return HttpResponse(json)