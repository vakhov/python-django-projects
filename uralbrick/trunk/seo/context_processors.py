# -*- coding: utf-8 -*-

from models import Metatag

def seo_tags(request):
    try:
        return { 'metatag': Metatag.objects.get(name=request.path) }
    except:
        return {}

def phone(request):
    return {'phone': Metatag.get_property(request.path, 'phone')}
    
def background(request):
    return {'background': Metatag.get_property(request.path, 'image')}