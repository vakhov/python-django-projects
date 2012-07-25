# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

def image_upload_path(instance, filename):
    url = instance._current_section
    path = 'files/' + url + filename
    return path

#
# Images and galleries
#

create_group('images', 'Картинки и галереи')

@add2group('Изображение', 'images')
class SingleImage(Widget):

    image = models.ImageField("Изображение", upload_to=image_upload_path)

    has_border = models.BooleanField("Border", default=False)
    is_zoomable = models.BooleanField("Увеличивается при клике", default=False)
    is_scalable = models.BooleanField("Ресайзится вместе с окном браузера", default=False)

    description_top = models.TextField("Описание сверху", blank=True, null=True)
    description_bottom = models.TextField("Описание снизу", blank=True, null=True)
    description_below = models.TextField("Описание под картинкой", blank=True, null=True)

    alt = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")
