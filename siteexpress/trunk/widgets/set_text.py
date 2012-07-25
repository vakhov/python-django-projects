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
        (1, 'Обычный текст'),
        (2, 'Цитата'),
        (3, 'Заметка'),
    )

    text_type = models.PositiveIntegerField("Тип текстового блока", choices=TEXT_TYPE_CHOICES, default=1)
    text = tinymce_model.HTMLField("Текст", default="Text")

@add2group('Таблица характеристик', 'text')
class CharsTable(Widget):  
    text = tinymce_model.HTMLField("Текст", default="Свойство 1 :: Значение 1\nСвойство 2 :: Значение 2\nСвойство 3 :: Значение 3")

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
