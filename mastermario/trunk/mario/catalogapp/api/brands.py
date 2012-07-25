# -*- coding: utf-8 -*-

from catalogapp.models import Brand

def create(name, slug):
    brand = Brand(name=name, slug=slug)
    brand.save()
    return brand.id

def delete(id):
    try:
        brand = Brand.objects.get(id=id)
    except Brand.DoesNotExist:
        return False

    brand.delete()

    return True

def rename(id, new_name, new_slug=None):
    try:
        brand = Brand.objects.get(id=id)
    except Brand.DoesNotExist:
        return False

    brand.name = new_name
    if not new_slug is None:
        brand.slug = new_slug

    brand.save()

    return brand.id

def list(**filters):
    return Brand.objects.filter(**filters)

def listIn(ids):
    return Brand.objects.filter(id__in=ids)

def get(id):
    return Brand.objects.get(id=id)