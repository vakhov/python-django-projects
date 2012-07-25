# -*- coding: utf-8 -*-

from models import ZoneProductHead, ZoneProductFoot

def zone_product_head(request):
    return {'zone_product_head': ZoneProductHead.objects.get(pk=1)}

def zone_product_foot(request):
    return {'zone_product_foot': ZoneProductFoot.objects.get(pk=1)}