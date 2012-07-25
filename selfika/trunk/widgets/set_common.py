# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

create_group('common', 'Другие')

@add2group('Горизонтальная черта', 'common')
class Hr(Widget):
    pass