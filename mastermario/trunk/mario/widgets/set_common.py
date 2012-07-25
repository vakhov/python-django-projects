# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

create_group('common', 'Другие')

@add2group('Контейнер', 'common')
class Container(Widget):
    sub_zones_type = 'container'
    sub_zones_count = 1

@add2group('HR', 'common')
class Hr(Widget):
    pass