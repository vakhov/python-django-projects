# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# ...
#

create_group('icon', 'Иконка')

@add2group('Иконка', 'icon')
class SingleIcon(Widget):
    icon = models.ImageField("Изображение", upload_to='images/icon', blank=True, null=True)

    title = models.CharField('Текст заголовка', max_length=255, blank=True, null=True)
    url = models.CharField('URL (без http)', max_length=255, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
