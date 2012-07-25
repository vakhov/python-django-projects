# -*- coding: utf-8 -*-

from catalogapp.models import Good

def create(name, section_id, articul='', initial={}):
    """ Создание нового объекта класса Good
        Используй его если необходима проверка на корректность передаваемых
        атрибутов """
    good = Good(name=name, section_id=section_id, articul='', **initial)
    
    good.full_clean()
    good.save()

    return good.id

def delete(id):
    try:
        good = Good.objects.get(id=id)
    except Good.DoesNotExist:
        return False
    
    good.delete()

    return True

def change(id, data):
    try:
        good = Good.objects.get(id=id)
    except Good.DoesNotExist:
        return False

    for key in data:
        setattr(good, key, data[key])

    good.save()
    
    return good.id

def list(**filters):
    return Good.objects.filter(**filters)

def listIn(ids):
    return Good.objects.filter(id__in=ids)

def get(id):
    return Good.objects.get(id=id)