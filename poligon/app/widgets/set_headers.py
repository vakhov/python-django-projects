# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Headers
#

create_group('headers', 'Заголовки')

class HeaderWidget(Widget):
    header = models.CharField("Текст заголовка", max_length=255, blank=True, default="Заголовок")

    class Meta:
        abstract = True

@add2group('H1', 'headers')
class H1(HeaderWidget):
    pass


@add2group('H2', 'headers')
class H2(HeaderWidget):
    pass


@add2group('H3', 'headers')
class H3(HeaderWidget):
    pass
