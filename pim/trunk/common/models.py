# -*- coding: utf-8 -*-

from django.db import models
from widgets.models import Zone

class Phone(models.Model):
    url_part = models.CharField(verbose_name=u"Корень категории с которой вглубь будет виден данный телефон", max_length=255)
    phone = models.CharField(verbose_name=u"Phone number", max_length=255)

    def __unicode__(self):
        return self.phone
    
    class Meta:
        verbose_name_plural = u'Телефонный номер'

class Banner(models.Model):
    img = models.ImageField(u'Картинка', upload_to="img/")
    url_part = models.CharField(verbose_name=u"Корень категории с которой вглубь будет показана данная картинка", max_length=255)
    url = models.CharField(u'Ссылка', max_length=255, blank=True)

    def __unicode__(self):
        return self.url_part
    
    class Meta:
        verbose_name_plural = u'Баннер'
        
class Footer(models.Model):
    zone = models.OneToOneField(Zone, null=True, blank=True)
