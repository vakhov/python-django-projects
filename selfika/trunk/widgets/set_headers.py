# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Headers
#

create_group('headers', 'Заголовки')

class HeaderWidget(Widget):

    HEADER_TYPE_CHOICES = (
        (1, 'H1'),
        (2, 'H2'),
        (3, 'H3'),
    )

    header_type = models.PositiveIntegerField("Тип заголовка", choices=HEADER_TYPE_CHOICES, default=1)
    header = models.CharField("Текст заголовка", default="Заголовок", max_length=255)


@add2group('Заголовок 1', 'headers')
class H1(HeaderWidget):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.header_type = '1'
        self.type = 'HeaderWidget'
        super(H1, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Заголовок 2', 'headers')
class H2(HeaderWidget):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.header_type = '2'
        self.type = 'HeaderWidget'
        super(H2, self).save(*args, **kwargs)

    class Meta:
        proxy = True


@add2group('Заголовок 3', 'headers')
class H3(HeaderWidget):
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.header_type = '3'
        self.type = 'HeaderWidget'
        super(H3, self).save(*args, **kwargs)

    class Meta:
        proxy = True
