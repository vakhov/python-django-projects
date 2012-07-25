# -*- coding: utf-8 -*-

from django.db import models

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