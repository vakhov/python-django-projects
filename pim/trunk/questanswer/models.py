# -*- coding: utf-8 -*-

from django.db import models
import datetime

class QuestAnswer(models.Model):
    author = models.CharField(verbose_name="Пользователь оставивший запись", max_length=255, default="Гость",)
    date_publication = models.DateTimeField(verbose_name="Дата написания", null=True, blank=True, default=datetime.datetime.now,)
    question = models.TextField(verbose_name="Вопрос", )
    moderator = models.CharField(verbose_name="Имя модератора", max_length=255, blank=True, default="Менеджер")
    answer = models.TextField(verbose_name="Ответ", blank=True)
    is_public = models.BooleanField("Опубликовать?", default=False,)
    
    class Meta:
        verbose_name = u'Вопрос-ответ'
        verbose_name_plural = u'Вопрос-ответ'
    
    def __unicode__(self):
        return self.question[:20]
