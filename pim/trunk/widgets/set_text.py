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
class SimpleText(Widget):

    TEXT_TYPE_CHOICES = (
        (1, 'Анонс'),
        (2, 'Цитата'),
        (3, 'Заметки'),
    )

    text = models.TextField("Текст", default="Text")
    text_type = models.PositiveIntegerField("Тип текстового блока", choices=TEXT_TYPE_CHOICES, default=1)

@add2group('Таблица характеристик', 'text')
class CharsTable(Widget):  
    text = models.TextField("Текст", default="Свойство 1 :: Значение 1\nСвойство 2 :: Значение 2\nСвойство 3 :: Значение 3")

    def get_pairs(self):
        result = []
        lines = self.text.split("\n")
        for line in lines:
            try:
                kv = line.split("::")
                result.append({ 'key': kv[0].strip(), 'value': kv[1].strip() })
            except:
                pass
        return result
