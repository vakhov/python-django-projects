# -*- coding: utf-8 -*-

from seo.models import Metatag
from common.models import Phone

def seo_tags(request):
    try:
        return { 'metatag': Metatag.objects.get(name=request.path) }
    except:
        return {}

def phone(request):
    try:
        phone = Phone.objects.extra(
            where=["url_part=(SELECT max(url_part) from globals_phone WHERE locate(url_part, %s)=1)"], 
            params=[request.path]
        )[0]
        return {'phone':phone}
    except:
        return {'phone':''}

def current_section(request):
    return { 'current_section': request.current_section }

def structure(request):
    return { 'structure': request.structure }