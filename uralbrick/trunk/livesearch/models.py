# -*- coding: utf8 -*-

from django.db import models

class TestText(models.Model):
    text = models.TextField('Text')
    perevod = models.TextField('Перевод')
    
    class Meta:
        verbose_name = 'Text'
        verbose_name_plural = 'Texts'
    
    def __unicode__(self):
        return self.text
