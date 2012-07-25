# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Text
#

create_group('text', 'Текст')

@add2group('Параграф', 'text')
class Paragraph(Widget):
    text = models.TextField("Текст", default="Text")

@add2group('Анонс', 'text')
class Announce(Widget):
    text = models.TextField("Текст", default="Text")

@add2group('Цитата', 'text')
class Quote(Widget):
    text = models.TextField("Текст", default="Text")
    
@add2group('Заметка', 'text')
class Note(Widget):
    text = models.TextField("Текст", default="Text")
