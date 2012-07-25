# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group
from tinymce import models as tinymce_model

#
# Text
#

create_group('text', 'Текст')

@add2group('Параграф', 'text')
class Paragraph(Widget):
    text = tinymce_model.HTMLField("Текст", default="Text")

@add2group('Анонс', 'text')
class Announce(Widget):
    text = tinymce_model.HTMLField("Текст", default="Text")

@add2group('Цитата', 'text')
class Quote(Widget):
    text = tinymce_model.HTMLField("Текст", default="Text")
    
@add2group('Заметка', 'text')
class Note(Widget):
    text = tinymce_model.HTMLField("Текст", default="Text")
