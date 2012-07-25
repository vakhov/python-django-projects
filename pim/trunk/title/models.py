# -*- coding: utf-8 -*-

from django.db import models

class Title(models.Model):
    TITLE_POSITION_CHOICES = (
        (1, '#-^--'),
        (2, '-#^--'),
        (3, '--^#-'),
        (4, '--^-#')
    )
    
    position = models.PositiveIntegerField('Позиция', choices= TITLE_POSITION_CHOICES)
    title = models.CharField('Заголовок', max_length=255, blank=True)
        
    class Meta:
        verbose_name = 'Шаблон заголовков'
        verbose_name_plural = 'Шаблоны заголовков'
        
    def __unicode__(self):
        return '%s (%s)' % (self.title, self.get_position_display())

class ChangeTitle(models.Model):
    path = models.CharField('PATH', max_length=255)
    title = models.CharField('Заголовок', max_length=255)
    
    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'
    
    def __unicode__(self):
        return self.title
