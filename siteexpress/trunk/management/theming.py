# -*- coding: utf-8 -*-

import os
from django.db import models
from utils.colorfield import ColorField

PATH_CSS = ''

class Template(models.Model):
    name = models.CharField("Название шаблона (человеческое)", max_length=255)
    slug = models.SlugField("Имя папки шаблона", max_length=255)

    def __unicode__(self):
        return self.name + ' (' + self.slug + ')'

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

class ColorTheme(models.Model):
    
    caption = models.CharField(u'Имя цветовой темы', max_length=255, unique=True)

    body = ColorField(u'Задний фон', max_length=6, blank=True)
    menuUlUl = ColorField(u'Меню (выпадающее меню)', max_length=6, blank=True)
    container = ColorField(u'Контейнер', max_length=6, blank=True)
    container_left = ColorField(u'Левая граница контейнера', max_length=6, blank=True)
    container_right = ColorField(u'Правая граница контейнера', max_length=6, blank=True)
    text_bg = models.CharField(u'Прозрачный?', max_length=11, blank=True, choices=(('transparent', 'Установить прозрачный фон'), ('inherit', 'Наследовать значение родителя')))
    header_box_bg = ColorField(u'Задний фон бокса заголовка и Голосовалки', max_length=6, blank=True)
    header_box = ColorField(u'Текст в заголовке', max_length=6, blank=True)
    voteresults = ColorField(u'Задний фон результатов ответа', max_length=6, blank=True)
    voteresults_indicator = ColorField(u'Индикатор в результатах голосования', max_length=6, blank=True)
    specials_hover = ColorField(u'Задний фон нажатых ссылок спецпредложения', max_length=6, blank=True)
    news_data_span = ColorField(u'Задний фон у новостей', max_length=6, blank=True)
    tr_odd_td = ColorField(u'Заливка нечётных ячеек', max_length=6, blank=True)
    tr_even_td = ColorField(u'Заливка чётных ячеек', max_length=6, blank=True)
    catalog_th = ColorField(u'Задний фон заголовка таблицы каталога', max_length=6, blank=True)
    catalog_th_odd_td = ColorField(u'Заливка нечётных ячеек таблицы в каталоге', max_length=6, blank=True)
    catalog_th_even_td = ColorField(u'Заливка чётных ячеек таблицы в каталоге', max_length=6, blank=True)
    footer_background = ColorField(u'Заливка футера', max_length=6, blank=True)
    footer_color = ColorField(u'Цвет текста футера', max_length=6, blank=True)
    footer_a = ColorField(u'Ссылки футера', max_length=6, blank=True)
    footer_a_hover = ColorField(u'Ссылки футера при наведении', max_length=6, blank=True)
    container_color = ColorField(u'Текст контейнера', max_length=6, blank=True)
    specials_a = ColorField(u'Цвет текста ссылки спец предложения', max_length=6, blank=True)
    a_color = ColorField(u'Любая другая ссылка', max_length=6, blank=True)
    a_hover = ColorField(u'Любая другая ссылка при наведении мыши', max_length=6, blank=True)
    b_or_strong = ColorField(u'Тега b или тега strong', max_length=6, blank=True)
    menu_a = ColorField(u'Ссылок в меню', max_length=6, blank=True)
    specials_price = ColorField(u'Специальных цен', max_length=6, blank=True)
    news_date_span = ColorField(u'Цвет даты у новостей', max_length=6, blank=True)
    voteresults_small = ColorField(u'Маленький текст в результатах голосования', max_length=6, blank=True)
    catalog_body = ColorField(u'Цвет границы каталога', max_length=6, blank=True)
    news_date = ColorField(u'Граница даты новостей', max_length=6, blank=True)
    text_td = ColorField(u'Текст в ячейках таблицы', max_length=6, blank=True)
    text_th = ColorField(u'Текст в заголовке таблицы', max_length=6, blank=True)
        
    class Meta:
        verbose_name = 'Цветовая тема'
        verbose_name_plural = 'Цветовые темы'
        ordering = ['caption']
    
    def __unicode__(self):
        return self.caption
    
    def save(self, *args, **kwargs):
        f = open(PATH_CSS + "colors_new.css", "w")
        f.write('''body {background-color:%s;}
                   #menu ul, #menu ul ul {background:%s;}
                   .container {background: %s;border-left: 1px solid %s;border-right: 1px solid %s;}
                   #text_bg {background: %s;}
                   .header_box_bg, #voteresults p {background: %s;}
                   .header_box * {color: %s !important;}
                   #voteresults li {background: %s;}
                   #voteresults .indicator {background-color: %s;}
                   #specials a:hover {background: %s;}
                   #news .date span {background: %s;}
                   tr.odd td {background-color: %s;}
                   tr.even td {background-color: %s;}
                   #catalog th {background-color: %s;}
                   #catalog tr.odd td {background-color: %s;}
                   #catalog tr.even td {background-color: %s;}
                   #footer {background: %s; color: %s;}
                   #footer a {color: %s;}
                   #footer a:hover {color: %s;}
                   .container {color: %s;}
                   #specials a {color: %s;}
                   a {color: %s;}
                   a:hover {color: %s;}
                   b, strong {color: %s;}
                   #menu a {color: %s;}
                   #specials .price {color: %s;}
                   #news .date span {color: %s;}
                   #voteresults small {color: %s;}
                   #specials li img {border: 0;}
                   #catalog_body {border-color: %s;}
                   #news .date {border-color: %s;}
                   #text td {border-color: %s;}
                   #text th {border-color: %s;}
                ''' 

                    % 

                    (
                    self.body,
                    self.menuUlUl,
                    self.container,
                    self.container_left,
                    self.container_right,
                    self.text_bg,
                    self.header_box_bg,
                    self.header_box,
                    self.voteresults,
                    self.voteresults_indicator,
                    self.specials_hover,
                    self.news_data_span,
                    self.tr_odd_td,
                    self.tr_even_td,
                    self.catalog_th,
                    self.catalog_th_odd_td,
                    self.catalog_th_even_td,
                    self.footer_background,
                    self.footer_color,
                    self.footer_a,
                    self.footer_a_hover,
                    self.container_color,
                    self.specials_a,
                    self.a_color,
                    self.a_hover,
                    self.b_or_strong,
                    self.menu_a,
                    self.specials_price,
                    self.news_date_span,
                    self.voteresults_small,
                    self.catalog_body,
                    self.news_date,
                    self.text_td,
                    self.text_th,
                    )
                )
        f.close()

        super(ColorTheme, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
#        if os.path.exists(PATH_CSS + self.slug + '.css'):
#            os.remove(PATH_CSS + self.slug + ".css",)
        if os.path.exists(PATH_CSS + 'colors_new.css'):
            os.remove(PATH_CSS + "colors_new.css",)
                    
        super(ColorTheme, self).delete(*args, **kwargs)


class FontTheme(models.Model):
    FONT_CHOICES = (
        (u'Arial, Arial, Helvetica, sans-serif', u'Arial, Arial, Helvetica, sans-serif'),
        (u'Arial Black, Arial Black, Gadget, sans-serif', u'Arial Black, Arial Black, Gadget, sans-serif'),
        (u'Comic Sans MS, Comic Sans MS, cursive', u'Comic Sans MS, Comic Sans MS, cursive'),
        (u'Courier New, Courier New, Courier, monospace', u'Courier New, Courier New, Courier, monospace'),
        (u'Georgia, Georgia, serif', u'Georgia, Georgia, serif'),
        (u'Impact, Impact, Charcoal, sans-serif', u'Impact, Impact, Charcoal, sans-serif'),
        (u'Lucida Console, Monaco, monospace', u'Lucida Console, Monaco, monospace'),
        (u'Lucida Sans Unicode, Lucida Grande, sans-serif', u'Lucida Sans Unicode, Lucida Grande, sans-serif'),
        (u'Palatino Linotype, Book Antiqua, Palatino, serif', u'Palatino Linotype, Book Antiqua, Palatino, serif'),
        (u'Tahoma, Geneva, sans-serif', u'Tahoma, Geneva, sans-serif'),
        (u'Times New Roman, Times, serif', u'Times New Roman, Times, serif'),
        (u'Trebuchet MS, Helvetica, sans-serif', u'Trebuchet MS, Helvetica, sans-serif'),
        (u'Verdana, Verdana, Geneva, sans-serif', u'Verdana, Verdana, Geneva, sans-serif'),
        (u'Webdings, Webdings (Webdings, Webdings)', u'Webdings, Webdings (Webdings, Webdings)'),
        (u'Wingdings, Zapf Dingbats (Wingdings, Zapf Dingbats)', u'Wingdings, Zapf Dingbats (Wingdings, Zapf Dingbats)'),
        (u'MS Sans Serif, Geneva, sans-serif', u'MS Sans Serif, Geneva, sans-serif'),
        (u'MS Serif, New York, serif', u'MS Serif, New York, serif'),    
    )
    
    caption = models.CharField('Имя шаблона', max_length=255,)
    font_theme = models.CharField('Выбор шрифта', max_length=100, choices=FONT_CHOICES,)
    
    def __unicode__(self):
        return self.caption
    
    class Meta:
        verbose_name = 'Шрифтовая тема'
        verbose_name_plural = 'Шрифтовые темы'
    
    def save(self, *args, **kwargs):
        f = open(PATH_CSS + "font_new.css", "w")
        f.write('body {font-family:%s;}' % self.font_theme)
        f.close()

        super(FontTheme, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if os.path.exists(PATH_CSS + 'font_new.css'):
            os.remove(PATH_CSS + "font_new.css",)
                    
        super(FontTheme, self).delete(*args, **kwargs)