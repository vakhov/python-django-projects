# -*- coding: utf-8 -*-

from seo.models import Metatag
from structure.models import *
from catalog.models import Catalog, TypeA, TypeB, Manufacturer, Product, Set

def render_crumbs(path):
    crumbs = []
    collected_path = '/'
    position = None
    set = None
    
    section = path[1:-1].split('/')[0]
    other_path = path[1:-1].split('/')[1:]
    length = len(other_path)
    collected_path += section + '/'
    try:
        section = Section.objects.get(path=collected_path)
        crumbs.append({'caption': section.caption, 'path': collected_path})
        if section.type.slug == 'catalog' and length:
            #есть ли в пути позиция
            if other_path[-1].find('pos-') >= 0:
                position = other_path.pop()
                length = len(other_path)
            
            #/catalog/
            if length == 1:
                collected_path += other_path[0] + '/'
                catalog = Catalog.objects.get(slug=other_path[0])
                crumbs.append({'caption': catalog.name_short, 'path': collected_path})
    
            #/(type or manufacturer)/
            if length == 2:
                collected_path += other_path[0] + '/'
                catalog = Catalog.objects.get(slug=other_path[0])
                crumbs.append({'caption': catalog.name_short, 'path': collected_path})
                
                collected_path += other_path[1] + '/'
                type_or_manufacturer_path = other_path[1]
                try:
                    try:
                        type_or_manufacturer = TypeA.objects.get(catalog=catalog, slug=type_or_manufacturer_path)
                    except:
                        type_or_manufacturer = TypeB.objects.get(catalog=catalog, slug=type_or_manufacturer_path)
                except:
                    type_or_manufacturer = Manufacturer.objects.get(catalog=catalog, slug=type_or_manufacturer_path)
                crumbs.append({'caption': type_or_manufacturer.name, 'path': collected_path})
                
         
            #/type/brand/
            if length == 3:
                collected_path += other_path[0] + '/'
                catalog = Catalog.objects.get(slug=other_path[0])
                crumbs.append({'caption': catalog.name_short, 'path': collected_path})

                collected_path += other_path[1] + '/'
                manufacturer = Manufacturer.objects.get(catalog=catalog, slug=other_path[1])
                crumbs.append({'caption': manufacturer.name, 'path': collected_path})
                
                collected_path += other_path[2] + '/'
                try:
                    type = TypeA.objects.get(catalog=catalog, slug=other_path[2])
                except:
                    type = TypeB.objects.get(catalog=catalog, slug=other_path[2])
                crumbs.append({'caption': type, 'path': collected_path})
    
            #/type/brand/set/
            if length == 4:
                collected_path += other_path[0] + '/'
                catalog = Catalog.objects.get(slug=other_path[0])
                crumbs.append({'caption': catalog.name_short, 'path': collected_path})

                collected_path += other_path[1] + '/'
                manufacturer = Manufacturer.objects.get(catalog=catalog, slug=other_path[1])
                crumbs.append({'caption': manufacturer.name, 'path': collected_path})

                collected_path += other_path[2] + '/'
                try:
                    type = TypeA.objects.get(catalog=catalog, slug=other_path[2])
                except:
                    type = TypeB.objects.get(catalog=catalog, slug=other_path[2])
                crumbs.append({'caption': type, 'path': collected_path})
                
                collected_path += other_path[3] + '/'
                set = Set.objects.get(catalog=catalog, slug=other_path[3][4:])
                crumbs.append({'caption': set, 'path': collected_path})
            
            if position:
                position = Product.objects.get(catalog=catalog, slug=position[4:])
                crumbs.append({'caption': position.name, 'path': 'pos'})
            if set and length < 4:
                set = Set.objects.get(slug=set[4:])
                crumbs.append({'caption': set.name, 'path': 'pos'})
            
        return crumbs
    except:
        return {}

def current_section(request):
    return { 'current_section': request.current_section }

def current_path(request):
    return { 'current_path': request.path }

def structure(request):
    return { 'structure': request.structure }

def crumbs(request):
    return {'crumbs': render_crumbs(str(request.path))}

def header_menu(request):
    return {'header_menu': Section.objects.get(path='/').children.order_by('order').values()}
