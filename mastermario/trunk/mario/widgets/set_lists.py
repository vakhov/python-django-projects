# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Lists
#

create_group('lists', 'Списки')

@add2group('Простой список', 'lists')
class SimpleList(Widget):

    LIST_CHOICES = (
        (1, 'Без маркеров'),
        (2, 'Нумерованный'),
        (3, 'Маркированный тире'),
        (4, 'Маркированный оранж')
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
    

@add2group('Нумерованный список', 'lists')
class NumericList(SimpleList):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.list_type = '2'
        self.type = 'SimpleList'
        super(SimpleList, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Маркированный список', 'lists')
class UnorderedList(SimpleList):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.list_type = '3'
        self.type = 'SimpleList'
        super(SimpleList, self).save(*args, **kwargs)

    class Meta:
        proxy = True

