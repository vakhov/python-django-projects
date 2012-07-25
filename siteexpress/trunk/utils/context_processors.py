# -*- coding: utf-8 -*-

# from seo.models import Metatag
#from common.models import Phone

from se.models import Globals, Phoneflora
from widgets.models import Zone

# def seo_tags(request):
#     try:
#         return { 'metatag': Metatag.objects.get(name=request.path) }
#     except:
#         return {}

def phone(request):
    try:
        phone = Globals.objects.get(prop_slug='phone')
        return {'phone': phone.value}
    except:
        return {'phone': ''}

def footer_zone(request):
    try:
        zone_id = Globals.objects.get(prop_slug='footer-zone').value
        zone = Zone.objects.get(pk=zone_id)
        return {'footer_zone': zone}
    except:
        return {'footer_zone': None}

def current_section(request):
    return { 'current_section': request.current_section }

def structure(request):
    return { 'structure': request.structure }

def phone_flora(request):
    return { 'phone_flora': Phoneflora.objects.get(pk=1)}
