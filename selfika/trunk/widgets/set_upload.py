# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

create_group('upload', 'Загрузка')

@add2group('Файл', 'upload')
class UploadFile(Widget):
    title = models.CharField('Заголовок', max_length=255, blank=True)
    caption = models.CharField('Название', max_length=50, blank=True)
    file  = models.FileField(upload_to='upload_widget/file')