# -*- coding: utf-8 -*-

from catalogapp import models
from catalogapp.models import BaseField

def create(field_type, name, slug, section, default_value, description, choices=None):
    # Get field class
    field_class = getattr(models, field_type)
    # Create new instance
    new_field = field_class(
        name=name, slug=slug, section=section,
        default_value=default_value, description=description
        )
    # Only for Choice and MultipleChoice fields
    if (field_type=='ChoiceField' or field_type=='MultipleChoiceField') and not choices is None:
        new_field.choices = choices
    new_field.save()

    return new_field.id

def change(id, name, slug, default_value, description):
    try:
        field = BaseField.objects.get_subclass(id=id)
    except BaseField.DoesNotExist:
        return False
    
    field.name = name
    field.slug = slug
    field.default_value = default_value
    field.description = description
    field.save()

    return field.id

def get(id):
    try:
        basefield = BaseField.objects.get_subclass(id=id)
    except BaseField.DoesNotExist:
        return False
        
    return basefield

def list(**filters):
    return BaseField.objects.filter(**filters).select_subclasses()

def listIn(ids):
    return BaseField.objects.filter(id__in=ids).select_subclasses()