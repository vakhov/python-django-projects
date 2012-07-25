# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Document

def root(request, document_id):
    context = RequestContext(request)
    context['document'] = get_object_or_404(Document, pk=document_id)
    return render_to_response('root.html', context)

def part(request, document_id, path):
    context = RequestContext(request)
    context['document'] = get_object_or_404(Document, pk=document_id)
    context['part'] = context['document'].get_part_by_path(path)
    return render_to_response('part.html', context)

def structure(request, document_id):
    context = RequestContext(request)
    context['document'] = get_object_or_404(Document, pk=document_id)
    context['structure'] = context['document'].get_parts_tree()
    return render_to_response('structure.html', context)

def glossary(request, document_id):
    context = RequestContext(request)
    context['document'] = get_object_or_404(Document, pk=document_id)
    return render_to_response('glossary.html', context)

