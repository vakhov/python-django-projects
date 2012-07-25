# -*- coding: utf-8 -*-

from django.db import models
from pixelion.apps.widgets.models import Widget

class SimpleList(Widget):
    LIST_CHOICES = (
        (1, 'Маркированный'),
        (2, 'Нумерованный'),
    )

    content = models.TextField("Список (каждый пункт с новой строки)", blank=True, default="Пункт 1\nПункт 2\nПункт 3")
    list_type = models.PositiveIntegerField("Тип списка", choices=LIST_CHOICES, default='1')

    def get_items(self):
        result = []
        for string in self.content.split("\n"):
            string = string.replace('<li>', '').replace('</li>', "\n")
            if string.isspace() or string == '':
                pass
            else:
                result.append(string)
        return result
    

class UnorderedList(SimpleList):
    def save(self, *args, **kwargs):
        if self.id is None:
            self.list_type = '1'
        self.type = 'SimpleList'
        super(SimpleList, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class NumericList(SimpleList):
    def save(self, *args, **kwargs):
        if self.id is None:
            self.list_type = '2'
        self.type = 'SimpleList'
        super(SimpleList, self).save(*args, **kwargs)

    class Meta:
        proxy = True
