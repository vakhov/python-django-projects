# -*- coding: utf-8 -*-

from catalogapp.models import Section, BaseField
from django.conf import settings
import specfields

def create(name, slug):
    section = Section(name=name, slug=slug)
    section.save()
    return section.id

def delete(id):
    try:
        section = Section.objects.get(id=id)
    except Section.DoesNotExist:
        return False

    section.delete()

    return True

def rename(id, new_name, new_slug=None):
    try:
        section = Section.objects.get(id=id)
    except Section.DoesNotExist:
        return False

    section.name = new_name
    if not new_slug is None:
        section.slug = new_slug
    section.save()
    
    return section.id

def get(id):
    return Section.objects.get(id=id)

def list(**filters):
    return Section.objects.filter(**filters)

def listIn(ids):
    return Section.objects.filter(id__in=ids)

def addFields(section_id, sps_array):
    result = []

    section = Section.objects.get(id=section_id)

    for field in sps_array:
        if field['field_type'] in settings.FIELD_TYPES:
            field['section'] = section
            id = specfields.create(**field)
            result.append(id)
        else:
            return False

    return result

def removeFields(section_id, ids_array):
    section = Section.objects.get(id=section_id)
        
    for id in ids_array:
        try:
            field = BaseField.objects.get(id=id)
            field.delete()
        except BaseField.DoesNotExist:
            return False

    return True

def getFields(section_id):
    section = Section.objects.get(id=section_id)
    fields = section.get_fields()
    return fields