# -*- coding: utf-8 -*-

import pytils

from django.db import models, connection
from structure.models import Section as StructureSection
from widgets.models import Zone
from utils.models import SortableModel
from common.thumbs import ImageWithThumbsField
from questanswer.models import QuestAnswer

from django.db.models import Q
from django.conf import settings
import datetime


class CatalogManager(models.Manager):
    def search(self):
        pass


def _split_join(s):
    b = s.split('/')
    b = '_'.join(b)[:-1]
    b = s.split('-')
    b = '_'.join(b)
    return '%s' % b

NAME_TABLE = 'all_catalog'


class Section(StructureSection):
    class Meta:
        proxy = True
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class ShoeSizeSection(models.Model):
    section = models.OneToOneField('Section',
                                   verbose_name='Раздел сайта',
                                   related_name='catalog_property')
    sizes = models.ManyToManyField('ShoeSize', null=True, blank=True)

    class Meta:
        verbose_name = 'Размеры раздела'
        verbose_name_plural = 'Размеры раздела'

    def __unicode__(self):
        return self.section.path

    def save(self, *args, **kwargs):
        super(ShoeSizeSection, self).save(*args, **kwargs)
        if self.sizes:
            products = Product.objects.filter(section__path__startswith=self.section.path)
            for sizes in self.sizes:
                pass

    def delete(self, *args, **kwargs):
        super(ShoeSizeSection, self).delete(*args, **kwargs)


class Catalog(models.Model):
    section = models.OneToOneField('Section',
                                   verbose_name='Раздел сайта',
                                   related_name='catalog')
    properties = models.ManyToManyField('Property',
                                        verbose_name=u'Свойства',
                                        blank=True)

    def save(self, *args, **kwargs):
        super(Catalog, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.section.caption)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'


# @todo: Handle "Sections" and "Catalogs"
# separately for extended properties manipulation

class Product(SortableModel):

    order_isolation_fields = ('section',)

    name = models.CharField(u'Имя продукта', max_length=255,)
    slug = models.SlugField(u'Slug', max_length=255, blank=True)
    article = models.CharField(u'Артикул', max_length=255, blank=True,)
    desc_short = models.CharField('Краткое описание продукта',
                                  max_length=255,
                                  blank=True,)
    price = models.DecimalField(u'Цена', max_digits=10, decimal_places=2, blank=True, null=True,)
    section = models.ForeignKey('Section', verbose_name=u'К какому разделу?')
    catalog = models.ForeignKey('Catalog', verbose_name=u'К какому каталогу?', blank=True, null=True)
    discount = models.PositiveIntegerField(u'Процент скидки', blank=True, null=True, default=0)

    date = models.DateField('Дата добавления', blank=True, default=datetime.datetime.now())

    is_special = models.BooleanField("Акция", default=False)
    is_free_delivery = models.BooleanField("Бесплатная доставка", default=False)

    is_exist = models.BooleanField("В наличии?", default=True)
    on_main = models.BooleanField(u'Выводить на главную?', default=True)
    is_enabled = models.BooleanField(u'Включена?', default=False)

    wtp = models.ManyToManyField('self', verbose_name=u'С этим товаром так же покупают', blank=True, null=True, symmetrical=False, editable=False)  # wtp - with this product

    zone = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    upper_zone = models.OneToOneField(Zone, related_name="upper_zone", null=True, blank=True, editable=False)

    sizes = models.ManyToManyField('ShoeSize', through='Pricing', null=True, blank=True, editable=False)

    qa = models.ManyToManyField(QuestAnswer, verbose_name='Связь продукта с вопросами', null=True, blank=True)

    class Meta:
        ordering = ['-is_exist', 'order']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        if self.id is None and not self.slug:
            order_slug = slug = pytils.translit.slugify(self.name)
            order = 0
            while Product.objects.filter(slug=order_slug):
                order += 1
                order_slug = '{0}-{1}'.format(str(order), slug)
            self.slug = order_slug

        try:
            product = Product.objects.get(slug=self.slug)
            if product.id != self.id:
                order_slug = slug = self.slug
                order = 0
                while Product.objects.filter(slug=order_slug):
                    order += 1
                    order_slug = '{0}-{1}'.format(str(order), slug)
                self.slug = order_slug
        except:
            pass

        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
            upper_zone = Zone()
            upper_zone.save()
            self.upper_zone = upper_zone
        # @todo: add the row to the render table

        # Checking "catalog"
        cs = self.section
        if Catalog.objects.filter(section=cs):
            self.catalog = Catalog.objects.get(section=cs)
        elif Catalog.objects.filter(section=cs.parent):
            self.catalog = Catalog.objects.get(section=cs.parent)
        elif Catalog.objects.filter(section=cs.parent.parent):
            self.catalog = Catalog.objects.get(section=cs.parent.parent)
        else:
            self.catalog = Catalog.objects.get(section=cs.parent.parent.parent)

        if not self.is_exist:
            product = Product.objects.get(pk=self.pk)
            sizes = Pricing.objects.filter(product=product)
            for size in sizes:
                size.is_exist = False
                size.save()

        if not self.date:
            self.date = datetime.datetime.now()

        super(Product, self).save(*args, **kwargs)
        if self.article == '':
            self.article = 'A-' + str(self.id)
            super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.zone.delete()
        self.upper_zone.delete()

    def __unicode__(self):
        return self.name

    def picture(self):
        try:
            return self.picture_set.all()[0].picture
        except:
            return None

    def discounted(self):
        if self.discount == 0:
            return self.price
        else:
            return self.price - (self.price * self.discount / 100)

    @staticmethod
    def filter(catalog, from_price=None, to_price=None, size=None):
        result = {}
        products = []
        section = Section.objects.filter(path__startswith=catalog)
        for sec in section:
            for p in Product.objects.filter(section=sec):
                products.append(p)
        if not size:
            result = Product.objects.filter(section__path__startswith=catalog).\
                                    filter(Q(price__range=(from_price, to_price)) | Q(pricing__price__range=(from_price, to_price))).distinct()
        elif not from_price and not to_price:
            result = Product.objects.filter(section__path__startswith=catalog).\
                            filter(pricing__size__in=size).distinct()
        else:
            result = Product.objects.filter(section__path__startswith=catalog).\
                            filter(pricing__size__in=size).\
                            filter(Q(price__range=(from_price, to_price)) | Q(pricing__price__range=(from_price, to_price))).distinct()
        return result

    def size_is_exists(self):
        for size in self.pricing_set.all():
            if size.is_exist:
                return True

    def position_pricing_if_exists(self):
        if Pricing.objects.filter(product=self).order_by('size'):
            return True

    def nova(self):
        if self.date:
            delta = datetime.date.today() - self.date
            if delta.days <= settings.DELTA_DATE:
                return True
        return False


class Property(models.Model):

    TYPE_CHOICES = (
        (1, 'Текстовый'),
        (2, 'Числовой'),
        (3, 'Да/нет'),
        (4, 'Выбор значений'),
    )

    type = models.PositiveIntegerField("Какой тип", choices=TYPE_CHOICES)
    name = models.CharField(u'Имя', max_length=255)
    slug = models.SlugField(u'Slug', max_length=255)
    default = models.CharField(u'Значение по умолчанию', max_length=255, blank=True,)
    description = models.TextField(u'Описание', blank=True)

    is_filter = models.BooleanField('Является фильтром', default=False)
    is_important = models.BooleanField('Является важной', default=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id is None:
            # @todo: create the column for rendered section table
            pass
        # @todo: check the type of the field to change rendered-column type
        # @todo: change default value somehow o_O
        # @old @todo: handle options change as well
        super(Property, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'


class Choice(models.Model):
    property = models.ForeignKey('Property', verbose_name='Свойство', limit_choices_to={'type': 4})
    value = models.CharField("Вариант", max_length=255, blank=True)
    is_default = models.BooleanField('По умолчанию?', default=False)

    description = models.TextField(u'Описание', blank=True)

    def __unicode__(self):
        return self.value

    def save(self, *args, **kwargs):
        super(Choice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'


class PropertyValue(models.Model):
    position = models.ForeignKey('Product', verbose_name=u'Позиция')

    def __unicode__(self):
        return self.property.name + ': ' + unicode(self.value)

    def save(self, *args, **kwargs):
        # @todo: put the value into the render table
        super(PropertyValue, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # @todo: throw the value out of the render table
        super(PropertyValue, self).delete(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = 'Значение свойства'
        verbose_name_plural = 'Значения свойств'


class CharPropertyValue(PropertyValue):
    property = models.ForeignKey('Property', verbose_name=u'Свойство', limit_choices_to={'type': 1})
    value = models.CharField("Значение", max_length=255)


class NumericPropertyValue(PropertyValue):
    property = models.ForeignKey('Property', verbose_name=u'Свойство', limit_choices_to={'type': 2})
    value = models.FloatField("Значение (число)")


class BooleanPropertyValue(PropertyValue):
    property = models.ForeignKey('Property', verbose_name=u'Свойство', limit_choices_to={'type': 3})
    value = models.BooleanField("Значение (да/нет)")


class MultipleChoicePropertyValue(PropertyValue):
    property = models.ForeignKey('Property', verbose_name=u'Свойство', limit_choices_to={'type': 4})
    value = models.ForeignKey('Choice', verbose_name=u'Вариант значения')

# # # Additional stuff


class Picture(models.Model):
    name = models.CharField("Подпись", max_length=255, blank=True)
    picture = ImageWithThumbsField("Изображение", upload_to='catalog/pictures',
                                    sizes=((130, 130), (50, 50), (300, 400)))
    product = models.ForeignKey(Product, verbose_name='Позиция')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class NewCollection(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL-slug', max_length=255, blank=True)
    desc = models.TextField(u'Описание', blank=True)
    picture = models.ImageField(u'Изображение', upload_to='collection/pictures', blank=True)
    is_active = models.BooleanField('Активна?', default=True)
    products = models.ManyToManyField(Product, verbose_name='Позиции',
                                      blank=True, null=True, editable=False)

    zone_top = models.OneToOneField(Zone, related_name='Zone Top', null=True, blank=True, editable=False)
    zone_bottom = models.OneToOneField(Zone, related_name='Zone Bottom', null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Новая Коллекция'
        verbose_name_plural = 'Новые Коллекции'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.slug == ''):
            self.slug = pytils.translit.slugify(self.name)
        if self.id == None:
            zone_top = Zone()
            zone_top.save()
            self.zone_top = zone_top
            zone_bottom = Zone()
            zone_bottom.save()
            self.zone_bottom = zone_bottom
        super(NewCollection, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.zone_top.delete()
        self.zone_bottom.delete()
        super(Action, self).delete(*args, **kwargs)


class ShoeSize(models.Model):
    mm = models.PositiveIntegerField('Размер в мм')
    cm = models.PositiveIntegerField('Размер в см')
    st = models.PositiveIntegerField('Размер стандарт')

    def __unicode__(self):
        return str(self.mm) + '/' + str(self.cm) + '/' + str(self.st)

    class Meta:
        ordering = ('mm', )
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Pricing(models.Model):
    size = models.ForeignKey(ShoeSize, verbose_name='Размер')
    product = models.ForeignKey(Product, verbose_name='Позиция')
    is_exist = models.BooleanField('Наличие', default=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, blank=True, null=True)

    def discounted(self):
        # Not discounted
        if not self.product.discount:
            # Size price
            if self.price:
                return self.price
            # Product price
            else:
                return self.product.price
        # Discounted
        else:
            # Size discounted price
            if self.price:
                return self.price - (self.price * self.product.discount / 100)
            # Product discounted price
            else:
                return self.product.discounted()

    class Meta:
        verbose_name = 'Цена за размер'
        verbose_name_plural = 'Цены за размер'


class Action(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL-slug', max_length=255, blank=True)
    desc = models.TextField(u'Описание', blank=True)
    picture = models.ImageField(u'Изображение', upload_to='action/pictures', blank=True)
    is_active = models.BooleanField('Активна?', default=True)
    products = models.ManyToManyField(Product, verbose_name='Позиции',
                                      blank=True, null=True, editable=False)

    zone_top = models.OneToOneField(Zone, related_name='Zone_Action_Top', null=True, blank=True, editable=False)
    zone_bottom = models.OneToOneField(Zone, related_name='Zone_Action_Bottom', null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.slug == ''):
            self.slug = pytils.translit.slugify(self.name)
        if self.id == None:
            zone_top = Zone()
            zone_top.save()
            self.zone_top = zone_top
            zone_bottom = Zone()
            zone_bottom.save()
            self.zone_bottom = zone_bottom
        super(Action, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.zone_top.delete()
        self.zone_bottom.delete()
        super(Action, self).delete(*args, **kwargs)

from order import Order
