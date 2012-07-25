# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from set_filter import *

from models import Group, Catalog, Manufacturer, TypeA, TypeB, Product, Picture, GroupingUnit, Alphabet, ManufacturerZoneUrl, CatalogBrandType

import json

def index(request):
    context = RequestContext(request)
    context['groups'] = Group.objects.all()
    context['alphabet'] = Alphabet.objects.filter(is_action=True).order_by('letter')
    return render_to_response('catalog/index.html', context)

def catalogue(request, slug, product=None, set=None):
    context = RequestContext(request)
    if set:
        context['current_set'] = get_object_or_404(Set, slug=set)
        context['products_set'] = set_catalog(slug, set)
        return render_to_response('catalog/catalog_set.html', context)
    context['catalog'] = get_object_or_404(Catalog, slug=slug)
    if product:
        context['product'] = get_object_or_404(Product, catalog=context['catalog'], slug=product)
        context['image'] = context['product'].picture.all()[0]
        #if ajax popupwindow request
        if request.GET.has_key('ajax'):
            return render_to_response('catalog/catalog_items_ajax.html', context)
        return render_to_response('catalog/catalog_items.html', context)
    else:
        context['types_a'] = TypeA.objects.filter(catalog=context['catalog'], show_on_site=True)
        context['types_b'] = TypeB.objects.filter(catalog=context['catalog'], show_on_site=True)
        context['manufacturers'] = Manufacturer.objects.filter(catalog=context['catalog'], show_on_site=True)
        try:
            context['products'] = get_catalog(slug)
            context['set'] = True
        except:
            context['products'] = Product.objects.filter(catalog=context['catalog'])[0:6]
        return render_to_response('catalog/catalog.html', context)

def type_or_brand(request, catalog, type_or_brand, product=None, set=None):
    """
    В данной функции идёт обработка приходящего урла с выявлением, Тип это или Производитель.
    """
    context = RequestContext(request)
    context['catalog'] = get_object_or_404(Catalog, slug=catalog)
    context['type_or_brand_slug'] = type_or_brand
    context['catalog_slug'] = catalog
    try:
        if Manufacturer.objects.get(catalog=context['catalog'], slug=type_or_brand):
            if set:
                context['current_set'] = get_object_or_404(Set, slug=set)
                context['products_set'] = set_brand(catalog, type_or_brand, set)
                return render_to_response('catalog/catalog_set.html', context)
            context['catalog'] = get_object_or_404(Manufacturer, catalog=context['catalog'], slug=type_or_brand)
            
            #Уникальность зон для производителя
            zones = context['catalog'].get_zone(request.path)
            context['zone_title'] = zones['zone_title']
            context['zone_medium_one'] = zones['zone_medium_one']
            context['zone_medium_two'] = zones['zone_medium_two']
    
            context['type_or_brand_products'] = [type.type.all() for type in CatalogBrandType.objects.filter(catalog=get_object_or_404(Catalog, slug=catalog), brand=context['catalog'])][0]
            context['manufacturer'] = True
    except:
        try:
            if TypeA.objects.get(catalog=context['catalog'], slug=type_or_brand):
                if set:
                    context['current_set'] = get_object_or_404(Set, slug=set)
                    context['products_set'] = set_type(catalog, type_or_brand, set)
                    return render_to_response('catalog/catalog_set.html', context)
                context['catalog'] = get_object_or_404(TypeA, catalog=context['catalog'], slug=type_or_brand)
                context['type_or_brand_products'] = [brand.brand for brand in CatalogBrandType.objects.filter(catalog=get_object_or_404(Catalog, slug=catalog), type=context['catalog'])]
                context['type'] = True
        except:
            if get_object_or_404(TypeB, catalog=context['catalog'], slug=type_or_brand):
                if set:
                    context['current_set'] = get_object_or_404(Set, slug=set)
                    context['products_set'] = set_type(catalog, type_or_brand, set)
                    return render_to_response('catalog/catalog_set.html', context)
                context['catalog'] = get_object_or_404(TypeB, catalog=context['catalog'], slug=type_or_brand)
                context['type_or_brand_products'] = [brand.brand for brand in CatalogBrandType.objects.filter(catalog=get_object_or_404(Catalog, slug=catalog), type=context['catalog'])]
                context['type'] = True
    if product:
        if context.has_key('brand'):
            context['product'] = get_object_or_404(Product, manufacturer=context['brand'], slug=product)
        elif context.has_key('types'):
            context['product'] = get_object_or_404(Product, types=context['types'], slug=product)
        context['image'] = context['product'].picture.all()[0]
        #if ajax popupwindow request
        if request.GET.has_key('ajax'):
            return render_to_response('catalog/catalog_items_ajax.html', context)
        return render_to_response('catalog/catalog_items.html', context)
    return render_to_response('catalog/catalog_type_or_brand.html', context)
    
 

def brand_type(request, catalog, brand, type, product=None, set=None):
    context = RequestContext(request)
    if set:
        context['current_set'] = get_object_or_404(Set, slug=set)
        #context['products_set'] = set_brand_and_type(catalog, type_or_brand, set)
        return render_to_response('catalog/catalog_set.html', context)
    context['catalog'] = get_object_or_404(Catalog, slug=catalog)
    context['manufacturer'] = get_object_or_404(Manufacturer, catalog=context['catalog'], slug=brand)
    context['type'] = get_object_or_404(TypeA, catalog=context['catalog'], slug=type)
    if product:
        context['product'] = get_object_or_404(Product, types=context['type'], manufacturer=context['manufacturer'], slug=product)
        pics = context['product'].picture.all()
        if pics: context['image'] = pics[0]
        #if ajax popupwindow request
        if request.GET.has_key('ajax'):
            return render_to_response('catalog/catalog_items_ajax.html', context)
        return render_to_response('catalog/catalog_items.html', context) 
    return render_to_response('catalog/catalog_type_or_brand.html', context)

def brand_type_set(request, catalog, brand, type, set, product=None, current_set=None):
    context = RequestContext(request)
    if current_set:
        context['current_set'] = get_object_or_404(Set, slug=set)
        #context['products_set'] = set_brand_and_type(catalog, type_or_brand, current_set)
        return render_to_response('catalog/catalog_set.html', context)
    context['catalog'] = get_object_or_404(Catalog, slug=catalog)
    context['manufacturer'] = get_object_or_404(Manufacturer, catalog=context['catalog'], slug=brand)
    context['type'] = get_object_or_404(TypeA, catalog=context['catalog'], slug=type)
    if product:
        context['product'] = get_object_or_404(Product, types=context['type'], manufacturer=context['manufacturer'], slug=product)
        try:
            context['image'] = context['product'].picture.all()[0]
        except:
            pass
        
        #if ajax popupwindow request
        if request.GET.has_key('ajax'):
            return render_to_response('catalog/catalog_items_ajax.html', context)
        return render_to_response('catalog/catalog_items.html', context)
    context['products'] =Product.objects.filter(types=context['type'], manufacturer=context['manufacturer'])
    return render_to_response('catalog/catalog_type_or_brand.html', context)

def get_many_products(request):
    if request.POST.get('data'):
        context = RequestContext(request)
        data = json.loads(data)
        pos = data['position']
        path = data['path'][1:-1].split('/')[1:]
        
        if path:
            length = len(path)
            if length == 1:
                # /production/catalog/
                context['products'] = Product.objects.filter(catalog=get_object_or_404(Catalog, slug=path[0]))[pos, pos+6]
            elif length == 2:
                # /production/catalog/brand or type/
                try:
                    brand = Manufacturer.objects.get(slug=path[1])
                    context['products'] = Product.objects.filter(catalog=get_object_or_404(Catalog, slug=path[0]), manufacturer=brand)[pos, pos+6]
                except:
                    type = TypeA.objects.get(slug=path[1])
                    context['products'] = Product.objects.filter(catalog=get_object_or_404(Catalog, slug=path[0]), types=type)[pos, pos+6]
            elif length == 3:
                # /production/catalog/type/brand/
                context['products'] = Product.objects.filter(catalog=get_object_or_404(Catalog, slug=path[0]),
                                                             types=get_object_or_404(TypeA, slug=path[1]),
                                                             manufacturer=get_object_or_404(Manufacturer, slug=path[3]))[pos, pos+6]
            if len(context['products']) < 6:
                pass
            return render_to_response('catalog/many_products_ajax.html', context)
        else:
            return 'This is root, not path'
        
    else:
        return 'Not data'

#def grouping_unit(request, catalog, grouping_unit):
#    context = RequestContext(request)
#    context['catalog'] = get_object_or_404(Catalog, slug=catalog)
#    context['unit'] = get_object_or_404(GroupingUnit, slug=grouping_unit)
#    return render_to_response('catalog/grouping_unit.html', context)
#
#def product(request, product):
#    context = RequestContext(request)
#    context['product'] = get_object_or_404(Product, slug=product)
#    context['image'] = context['product'].picture.all()[0]
#    return render_to_response('catalog/catalog_items.html', context)
