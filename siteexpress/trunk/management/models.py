# -*- coding: utf-8 -*-
import datetime
from django.db import models

from theming import Template

class Client(models.Model):
    name = models.CharField("Имя контрагента", max_length=255)
    info = models.TextField("Данные контрагента", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Site(models.Model):

    STATE_CHOICES = (
        (0, 'Тестовый режим'),
        (1, 'Активный режим'),
        (2, 'Заблокирован администратором'),
    )

    name = models.CharField("Название", max_length=255)
    state = models.PositiveIntegerField("Состояние", choices=STATE_CHOICES, default=0)
    test_until = models.DateField("Тест по", blank=True, null=True)
    active_until = models.DateField("Активен по", blank=True, null=True)
    client = models.ForeignKey("Client", verbose_name='Контрагент')

    template = models.ForeignKey(Template, verbose_name='Шаблон', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.test_until = datetime.date.today() + datetime.timedelta(days=7)
            super(Site, self).save(*args, **kwargs)
            domain = Domain()
            domain.name = str(self.id).zfill(4) + '.17777.ru'
            domain.site = self
            domain.save()
        else:
            super(Site, self).save(*args, **kwargs)

    def activate(self):
        if not self.active_until:
            self.active_until = datetime.date.today() + datetime.timedelta(days=365)
        else:
            self.active_until = self.active_until + datetime.timedelta(days=365)
        self.state = 1

    def __unicode__(self):
        return str(self.id) + ': ' + self.name

    class Meta:
        verbose_name = 'Сайт (аккаунт)'
        verbose_name_plural = 'Сайты (аккаунты)'

class Domain(models.Model):
    name = models.CharField("Доменное имя (без www)", max_length=255)
    site = models.ForeignKey("Site", verbose_name='Сайт')

    def __unicode__(self):
        return self.name + ' (' + self.site.name + ')'
    
    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'

