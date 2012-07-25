# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Text
#

create_group('text', 'Текст')

@add2group('Параграф', 'text')
class SimpleText(Widget):

    TEXT_TYPE_CHOICES = (
        (1, 'Обычный'),
        (2, 'Примечание'),
        (3, 'Заметка'),
        (4, 'Цитата'),
    )

    is_bold = models.BooleanField("Bold", default=False)
    is_italic = models.BooleanField("Italic", default=False)
    is_capital = models.BooleanField("Буквица", default=False)
    
    is_alert = models.BooleanField("Пометка", default=False)
    alert_text = models.CharField("Текст пометки", max_length=255, blank=True)

    top_border = models.BooleanField("Верхняя граница", default=False)
    bottom_border = models.BooleanField("Нижняя граница", default=True)

    font_color = models.CharField("Цвет текста (rrggbb)", max_length=6, blank=True)
    bg_color = models.CharField("Цвет фона (rrggbb)", max_length=6, blank=True)

    text = models.TextField("Текст", default="Text")
    text_type = models.PositiveIntegerField("Тип текстового блока", choices=TEXT_TYPE_CHOICES, default=1)

@add2group('Сноска', 'text')
class FootNote(SimpleText):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.text_type = '2'
        self.type = 'SimpleText'
        super(SimpleText, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Заметка', 'text')
class Tip(SimpleText):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.text_type = '3'
        self.type = 'SimpleText'
        super(SimpleText, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Цитата', 'text')
class Blockquote(SimpleText):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.text_type = '4'
        self.type = 'SimpleText'
        super(SimpleText, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Малый анонс', 'text')
class SmallAnnounce(SimpleText):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.is_italic = True
        self.type = 'SimpleText'
        super(SimpleText, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Большой анонс', 'text')
class BigAnnounce(SimpleText):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.is_bold = True
            self.is_capital = True
        self.type = 'SimpleText'
        super(SimpleText, self).save(*args, **kwargs)

    class Meta:
        proxy = True


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
