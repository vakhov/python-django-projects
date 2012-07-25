# -*- coding: utf-8 -*-

import md5
import random

from django.db import models
from widgets.models import Widget

class Metatag(models.Model):
    name = models.CharField(verbose_name="Metatag URL Slug", max_length=255, unique=True)
    title = models.TextField(verbose_name="Metatag Title", null=True, blank=True)
    description = models.TextField(verbose_name="Metatag Description", null=True, blank=True)
    keywords = models.TextField(verbose_name="Metatag Keywords", null=True, blank=True)

    def __unicode__(self):
        return self.name

class Hash(models.Model):
    type = models.CharField(max_length=32)
    key = models.CharField(max_length=255)
    hash_string = models.CharField(max_length=32)

    @staticmethod
    def link2hash(link):
        try:
            hash_string = Hash.objects.values('hash_string') \
                                      .get(type='link', key=link)['hash_string']
            return str(hash_string)
        except:
            hash_string = Hash.encrypt(link)
            new_hash = Hash(type='link', key=link, hash_string=hash_string)
            new_hash.save()
            return hash_string

    @staticmethod
    def widget2hash(widget_id):
        widget_id = str(widget_id)
        try:
            hash_string = Hash.objects.values('hash_string') \
                                      .get(type='widget', key=widget_id)['hash_string']
            return str(hash_string)
        except:
            hash_string = Hash.encrypt(widget_id)
            new_hash = Hash(type='widget', key=widget_id, hash_string=hash_string)
            new_hash.save()
            return hash_string

    @staticmethod
    def hash2link(hash_string):
        try:
            link = Hash.objects.values('key').get(hash_string=hash_string)['key']
            return link
        except:
            return '#'

    @staticmethod
    def hash2widget(hash_string):
        try:
            widget_id = Hash.objects.values('key').get(hash_string=hash_string)['key']
            widget = Widget.objects.get(pk=widget_id).as_leaf_class()
            return widget.render(force_unhashed=True)
        except:
            return ''

    @staticmethod
    def encrypt(key):
        return md5.new(str(random.random()) + str(key)).hexdigest()
    

