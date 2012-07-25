# -*- coding: utf-8 -*-

from seo.models import Metatag
from structure.models import *

def _split_join(s):
    c = []
    b = s.split('/')[1:-1]
    i = 0
    path = '/'
    while i < len(b):
        path += b[i]+'/'
        section = Section.objects.get(path=path)
        c.append({'caption': section.caption, 'path': path}) 
        i +=1
    return c

def current_section(request):
    return { 'current_section': request.current_section }

def current_path(request):
    return { 'current_path': request.path }

def structure(request):
    return { 'structure': request.structure }

def crumbs(request):
    return {'crumbs': _split_join(str(request.current_section))}
