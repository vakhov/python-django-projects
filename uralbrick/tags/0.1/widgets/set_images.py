# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Images and galleries
#

create_group('images', 'Картинки и галереи')

@add2group('Изображение', 'images')
class SingleImage(Widget):
    image = models.ImageField(u"Изображение", upload_to='image')

    alt = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")
