# -*- coding: utf8 -*-

from django.db import models

class TextOnPage(models.Model):
    url = models.CharField('привязать к URL', max_length=255)
    caption = models.CharField('Заголовок', max_length=255, blank=True)
    desc = models.TextField('Полное описание', blank=True)
    
    class Meta:
        verbose_name = 'Текст на странице'
        verbose_name_plural = 'Тексты на страницах'
    
    def __unicode__(self):
        return '({0}): {1}'.format(self.url, self.caption)
