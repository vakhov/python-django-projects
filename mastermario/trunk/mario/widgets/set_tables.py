# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Tables
#

create_group('tables', 'Таблицы')

@add2group('Таблица', 'tables')
class Table(Widget):

    TABLE_CHOICES = (
        (1, 'Таблица 1'),
        (2, 'Таблица 2'),
        (3, 'Таблица 3'),
    )

    content = models.TextField("Содержимое тега TABLE (без него самого)", blank=True, default="")
    table_type = models.PositiveIntegerField("Тип таблицы", choices=TABLE_CHOICES, default=1)


@add2group('Таблица 2', 'tables')
class Table_2(Table):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.table_type = 2
        self.type = 'Table'
        super(Table, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Таблица 3', 'tables')
class Table_3(Table):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.table_type = 3
        self.type = 'Table'
        super(Table, self).save(*args, **kwargs)

    class Meta:
        proxy = True

