# -*- coding: utf8 -*-

from django.db import models

import md5
import random

def gets_path_without_last_chunk(url):
    url_split = url.split('/')[1:-2]
    url_join = '/'.join(url_split)
    if len(url_join) > 1:
        return '/%s/' % url_join
    else:
        return '/'

class Metatag(models.Model):
    name = models.CharField(u'URL Slug', max_length=255, unique=True)
    title = models.CharField(u'Title', max_length=255, null=True, blank=True)
    description = models.CharField(u'Description', max_length=255, null=True, blank=True)
    keywords = models.CharField(u'Keywords', max_length=255, null=True, blank=True)
    phone = models.CharField(u'Номер телефона (наследуется)', max_length=255, blank=True)
    image = models.ImageField(u'Фоновая картинка (наследуется)', upload_to='background_image', blank=True)
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def get_property(url, property):
        """
        return current property.
        - url: string
        - property: string
        """
        try:
            while True:
                obj = Metatag.objects.extra(
                where=["name=(SELECT max(name) from seo_metatag WHERE locate(name, %s)=1)"], 
                params=[url]
            )[0]
                if obj.__dict__[property] == '':
                    if url == '/':
                        return ''
                    url = gets_path_without_last_chunk(url)
                else:
                    return obj.__dict__[property]
        except:
            return ''
    
    class Meta:
        verbose_name = u'Метатэг'
        verbose_name_plural = u'Метатэги'


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
    def hash2link(hash_string):
        try:
            link = Hash.objects.values('key').get(hash_string=hash_string)['key']
            return link
        except:
            return '#'

    @staticmethod
    def encrypt(key):
        return md5.new(str(random.random()) + str(key)).hexdigest()
