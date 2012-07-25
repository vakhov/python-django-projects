# -*- coding: utf-8 -*-

from django.db import models

class Phone(models.Model):
    url_part = models.CharField(verbose_name="Корень категории с которой в глубь будет виден данный телефон", max_length=255)
    phone = models.CharField(verbose_name="Phone number", max_length=255)

    def __unicode__(self):
        return self.phone

class IconCollection(models.Model):
    section = models.ForeignKey('self', blank=True)
    caption = models.CharField('Название', max_length=255)
    slug = models.SlugField('SLUG', max_length=255)
    icon = models.ImageField('Иконка', upload_to='imagesssss')
    
    class Meta:
        verbose_name_plural = 'Коллекция иконок'
    
    def __unicode__(self):
        return self.caption
