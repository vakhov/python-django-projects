# -*- coding: utf8 -*-

from models import *

from django.shortcuts import get_object_or_404

#first
def get_catalog(catalog):
    set = {}
    catalog = get_object_or_404(Catalog, slug=catalog)
    products = Product.objects.filter(catalog=catalog)
    for product in products:
        for setgroup in product.setgroup_set.all():
            set[setgroup.set.id] = setgroup.set
    return set.values()

def get_brand(catalog, brand):
    set = {}
    catalog = get_object_or_404(Catalog, slug=catalog)
    brand = get_object_or_404(Manufacturer, slug=catalog)
    products = Product.objects.filter(catalog=catalog, manufacturer=brand)
    for product in products:
        for setgroup in product.setgroup_set.all():
            set[setgroup.set.id] = setgroup.set
    return set.values()

def get_type(catalog, type):
    set = {}
    catalog = get_object_or_404(Catalog, slug=catalog)
    type = get_object_or_404(TypeA, slug=catalog)
    products = Product.objects.filter(catalog=catalog, types=type)
    for product in products:
        for setgroup in product.setgroup_set.all():
            set[setgroup.set.id] = setgroup.set
    return set.values()

def get_brand_and_type(brand, type):
    set = {}
    catalog = get_object_or_404(Catalog, slug=catalog)
    type = get_object_or_404(TypeA, slug=catalog)
    brand = get_object_or_404(Manufacturer, slug=catalog)
    products = Product.objects.filter(catalog=catalog, types=type, manufacturer=brand)
    for product in products:
        for setgroup in product.setgroup_set.all():
            set[setgroup.set.id] = setgroup.set
    return set.values()

#second
def set_catalog(catalog, set):
    result = []
    set = Set.objects.get(slug=set)
    catalog = get_object_or_404(Catalog, slug=catalog)
    for setgroup in set.setgroup_set.all():
        products = {}
        for product in setgroup.product.filter(catalog=catalog):
            products[product.id] = product
        result.append({'setgroup': setgroup.name, 'products': products.values()})
    return result

def set_brand(catalog, brand, set):
    result = []
    set = Set.objects.get(slug=set)
    catalog = get_object_or_404(Catalog, slug=catalog)
    brand = get_object_or_404(Manufacturer, catalog=catalog, slug=brand)
    for setgroup in set.setgroup_set.all():
        products = {}
        for product in setgroup.product.filter(catalog=catalog, manufacturer=brand):
            products[product.id] = product
        result.append({'setgroup': setgroup.name, 'products': products.values()})
    return result

def set_type(catalog, type, set):
    result = []
    set = Set.objects.get(slug=set)
    catalog = get_object_or_404(Catalog, slug=catalog)
    type = get_object_or_404(TypeA, catalog=catalog, slug=type)
    for setgroup in set.setgroup_set.all():
        products = {}
        for product in setgroup.product.filter(catalog=catalog, types=type):
            products[product.id] = product
        result.append({'setgroup': setgroup.name, 'products': products.values()})
    return result

# def set_brand_and_type(catalog, brand, type, set):
#     result = []
#     set = Set.objects.get(slug=set)
#     catalog = get_object_or_404(Catalog, slug=catalog)
#     type = get_object_or_404(TypeA, catalog=catalog, slug=type)
#     brand = get_object_or_404(Manufacturer, catalog=catalog, slug=brand)
#     for setgroup in set.setgroup_set.all():
#         products = {}
#         for product in setgroup.product.filter(catalog=catalog, types=type, manufacturer=brand):
#             products[product.id] = product
#         result.append({'setgroup': setgroup.name, 'products': products.values()})
#     return result
