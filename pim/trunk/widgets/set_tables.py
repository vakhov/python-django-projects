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

    content = models.TextField("Содержимое тега TABLE (без него самого)", blank=True, default="")
