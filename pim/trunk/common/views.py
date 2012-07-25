# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from catalog.models import Section

def get_default_context(request, _path):
    """
    Gets default context variables for catalog:
    - Subtree of catalog section
    - "New collections"
    """
    context = RequestContext(request)
    catalog_order = Section.objects.values('order').get(path=_path)['order']
    context['catalog_tree'] = context['structure'][1]['nodes'][catalog_order]['nodes']
    return context 

def collections(request):
    context = RequestContext(request)
    return render_to_response('collections.html', context)

def text(request):
    context = get_default_context(request, request.path)
    if 'ajax' in request.GET:
        return render_to_response('text_ajax.html', context)
    return render_to_response('text.html', context)
