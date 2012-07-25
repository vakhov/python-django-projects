# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from structure.models import Section

def index(request):
    context = RequestContext(request)
    context['sections'] = Section.objects.filter(type=4).order_by('parent')[0:]
    return render_to_response('catalog/index.html', context)

def section(request, section):
    context = RequestContext(request)
    context['section'] = section = get_object_or_404(Section, slug=section)
    return render_to_response('catalog/landing.html', context)