# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Headers
#

create_group('headers', 'Заголовки')

@add2group('Заголовок', 'headers')
class HeaderWidget(Widget):

    HEADER_TYPE_CHOICES = (
        (1, 'H1'),
        (2, 'H2'),
        (3, 'H3'),
    )

    header_type = models.PositiveIntegerField("Тип заголовка", choices=HEADER_TYPE_CHOICES, default=1)
    header = models.CharField("Текст заголовка", default="Заголовок", max_length=255)
