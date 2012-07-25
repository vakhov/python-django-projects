# -*- coding: utf-8 -*-

import datetime
import urllib

from django.db import models
from django.utils.encoding import smart_str
from widgets.models import Zone

class Group(models.Model):
    name = models.SlugField("URL Slug", max_length=255, unique=True)
    caption = models.CharField("Название", max_length=255)
    group = models.ForeignKey("Group", related_name="subs", null=True, 
                              blank=True, verbose_name="Группа")
    def __unicode__(self):
        if self.group:
            return self.group.__unicode__() + ' / ' + self.caption
        else:
            return self.caption
        
    def slug(self):
        if self.group:
            return self.group.slug() + '/' + self.name
        else:
            return self.name

class Article(models.Model):
    name = models.SlugField("URL Slug", max_length=255, blank=True)
    caption = models.CharField("Заголовок", max_length=255)
    shortdesc = models.TextField("Краткое описание", blank=True)
    date_written = models.DateField("Дата написания", default=datetime.datetime.now)
    publish = models.BooleanField("Публиковать?", default=False)
    author = models.CharField("Имя автора", null=True, blank=True, max_length=255)

    label_text = models.CharField("Текст метки", null=True, blank=True, max_length=255)
    label_color = models.CharField("Цвет метки", null=True, blank=True, max_length=6)

    group = models.ForeignKey(Group, null=True, blank=True, verbose_name="Группа")
    tags = models.ManyToManyField('Tag', blank=True)

    zone = models.OneToOneField(Zone, null=True, blank=True)

    seo_link_1 = models.ForeignKey('Article', related_name='back_seo_link_1', 
                                    null=True, blank=True, on_delete=models.SET_NULL)
    seo_link_2 = models.ForeignKey('Article', related_name='back_seo_link_2',
                                    null=True, blank=True, on_delete=models.SET_NULL)

    seo_link_order = models.PositiveIntegerField(default=0)
    seo_link_chunk = models.PositiveIntegerField(default=0)

    def seo_link(self):
        last_chunk = self.__class__.objects.values('seo_link_chunk') \
                                           .order_by('-seo_link_chunk')[0]
        last_chunk = last_chunk['seo_link_chunk']

        # print 'last_chunk: ' + str(last_chunk)

        last_order = self.__class__.objects.values('seo_link_order') \
                                           .filter(seo_link_chunk=last_chunk) \
                                           .order_by('-seo_link_order')[0]
        last_order = last_order['seo_link_order']        
        
        # print 'last_order: ' + str(last_order)

        if last_order == 10:
            # Creating new chunk
            self.seo_link_chunk = last_chunk + 1
            self.seo_link_order = 1
            # print 'last_order == 10'
        elif last_order == 1:
            # Second element will link to first only
            self.seo_link_chunk = last_chunk
            self.seo_link_order = 2
            self.seo_link_1 = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=last_order
            )
            # print 'last_order == 1'
        elif 2 <= last_order <= 8:
            # Default linking
            self.seo_link_chunk = last_chunk
            self.seo_link_order = last_order + 1
            self.seo_link_1 = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=last_order
            )
            self.seo_link_2 = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=last_order - 1
            )
            # print 'last_order in 2..8'
        elif last_order == 9:
            self.seo_link_chunk = last_chunk
            self.seo_link_order = 10
            self.seo_link_1 = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=last_order
            )
            self.seo_link_2 = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=last_order - 1
            )
            # Finishing chunk
            first = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=1
            )
            second = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=2
            )
            nine = self.__class__.objects.get(
                seo_link_chunk=last_chunk,
                seo_link_order=9
            )
            first.seo_link_1 = nine
            first.seo_link_2 = self
            second.seo_link_2 = self
            first.save()
            second.save()
            # print 'last_order == 9'

    def save(self, *args, **kwargs):
        # Creating zone for new article
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
            super(Article, self).save(*args, **kwargs)
            self.seo_link()
        super(Article, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(Article, self).delete(*args, **kwargs)    

    def __unicode__(self):
        if self.group:
            return self.group.__unicode__() + ' / ' + self.caption
        else:
            return '(No group) / ' + self.caption
    
    def slug(self):
        if self.group:
            return self.group.slug() + '/' + self.name
        else:
            return self.name
        
    def get_absolute_url(self):
        slug = self.slug()
        slug = slug.split('/')[1:]
        slug = '/'.join(slug)
        if slug:
            return "/articles/%s/" % (slug)
        else:
            return '/'
    
class Tag(models.Model):
    name = models.SlugField("URL Slug", max_length=255)
    tag = models.CharField("Имя тэга", max_length=30)

    def __unicode__(self):
            return self.tag + ' (' + self.name + ')'