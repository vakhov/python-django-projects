# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

create_group('media', 'Мультимедиа')

@add2group('Изображение', 'media')
class SimpleImage(Widget):
    image = models.ImageField("Изображение", upload_to='media_widgets/image')
    alt = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")
    link = models.CharField(u'Ссылка', max_length=255, blank=True, default="")

@add2group('Видео', 'media')
class SimpleVideo(Widget):
    video = models.FileField("Видео", upload_to='media_widgets/video')
    alt = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")

