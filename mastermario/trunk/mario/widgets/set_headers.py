# -*- coding: utf-8 -*-

from django.db import models
from models import Widget
from grouping import create_group, add2group

#
# Headers
#

create_group('headers', 'Заголовки')

class HeaderWidget(Widget):

    BORDER_CHOICES = (
        (1, 'Оранжевый'),
        (2, 'Синий'),
        (3, 'Черный'),
        (4, 'Морской волны'),
        (5, 'Зеленый'),
    )

    FONT_CHOICES = (
        (1, 'Tahoma'),
        (2, 'Arial'),
    )

    header = models.CharField("Текст заголовка", max_length=255, blank=True, default="Заголовок")
    border = models.PositiveIntegerField("Цвет подчеркивания", choices=BORDER_CHOICES, default=1)
    font_style = models.PositiveIntegerField("Шрифт", choices=FONT_CHOICES, default=1)
    free_border = models.CharField("Специальный цвет подчеркивания (rrggbb)", max_length=6, blank=True)

    is_span = models.BooleanField("SPAN", default=False)

    is_bold = models.BooleanField("Bold", default=False)
    is_italic = models.BooleanField("Italic", default=False)

    class Meta:
        abstract = True


@add2group('Заголовок 1', 'headers')
class H1(HeaderWidget):
    link_href = models.CharField("Адрес ссылки", max_length=255, blank=True)
    link_text = models.CharField("Текст ссылки", max_length=255, blank=True)


@add2group('Заголовок 2', 'headers')
class H2(HeaderWidget):
    link_href = models.CharField("Адрес ссылки", max_length=255, blank=True)
    link_text = models.CharField("Текст ссылки", max_length=255, blank=True)
    icon = models.ImageField("Иконка", upload_to="icons", blank=True)


@add2group('Заголовок 3', 'headers')
class H3(HeaderWidget):
    icon = models.ImageField("Иконка", upload_to="icons", blank=True)
    is_dashed = models.BooleanField("Подчеркивание пунктиром", default=False)


@add2group('Заголовок 4', 'headers')
class H4(HeaderWidget):
    icon = models.ImageField("Иконка", upload_to="icons", blank=True)
    is_dashed = models.BooleanField("Подчеркивание пунктиром", default=False)
