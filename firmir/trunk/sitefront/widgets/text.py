# -*- coding: utf-8 -*-

from django.db import models
from pixelion.apps.widgets.models import Widget

class SimpleText(Widget):
    TEXT_TYPE_CHOICES = (
        (1, 'Обычный текст'),
        (2, 'Цитата'),
        (3, 'Заметка'),
    )
    text = models.TextField("Текст", default="")
    text_type = models.PositiveIntegerField("Тип текстового блока", choices=TEXT_TYPE_CHOICES, default=1)


class Cite(SimpleText):
    def save(self, *args, **kwargs):
        if self.id is None:
            self.text_type = '2'
        self.type = 'SimpleText'
        super(Cite, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class Tip(SimpleText):
    def save(self, *args, **kwargs):
        if self.id is None:
            self.text_type = '3'
        self.type = 'SimpleText'
        super(Tip, self).save(*args, **kwargs)

    class Meta:
        proxy = True


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
