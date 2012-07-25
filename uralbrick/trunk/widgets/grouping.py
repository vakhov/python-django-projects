# -*- coding: utf-8 -*-

groups = {}

def create_group(slug, name):
    if slug not in groups:
        groups[slug] = { 'group': name, 'slug': slug, 'items': [] }

def add2group(title, group):
    def decorate(cls):
        obj = { 'name': cls.__name__, 'title': title }
        if group not in groups:
            return cls
        else:
            groups[group]['items'].append(obj)
        return cls
    return decorate

def get_groups():
    return groups