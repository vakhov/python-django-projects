# -*- coding: utf-8 -*-

from django.db import models

class Domain(models.Model):
    name = models.CharField("Доменное имя (без www)", max_length=255)
    site = models.ForeignKey("Site", verbose_name='Сайт')

    def __unicode__(self):
        return self.name + ' (' + self.site.name + ')'
    
    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'

class Site(models.Model):

    name = models.CharField("Название", max_length=255)

    def save(self, *args, **kwargs):
        if self.id is None:
            domain = Domain()
            domain.name = str(self.id).zfill(4) + '.firmir.local'
            domain.site = self
            domain.save()
        super(Site, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id) + ': ' + self.name

    class Meta:
        verbose_name = 'Сайт (аккаунт)'
        verbose_name_plural = 'Сайты (аккаунты)'