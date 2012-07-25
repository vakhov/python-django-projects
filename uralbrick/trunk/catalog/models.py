# -*- coding: utf-8 -*-

import os

from django.db import models
from django.conf import settings
from widgets.models import Zone

from pixelion.utils.sortable import SortableModel

IMAGE_OPTIONS = [ {'type': 'p', 'size': 150, 'quality': 100},
                  {'type': 'w', 'size': 263, 'quality': 100},
                  {'type': 'w', 'size': 345, 'quality': 100},
                  {'type': 'w', 'size': 49,  'quality': 100},
                  {'type': 'h', 'size': 257, 'quality': 100}  ]

def thumbnail(path, image_options, action=True):
    """
    path - путь до изображения
    image_options - словарь содержащий параметры
    action - Действие (True - create, False - delete)
    """
    original_image_name = path.split('/')[-1]
    original_image_path = path.split('/')[0:-1]
    original_image_path = '/'.join(original_image_path)
    name, ext = original_image_name.split('.')

    if action:
        import Image
        width, height = Image.open(settings.MEDIA_ROOT +'/'+ path).size
        fp = open(settings.MEDIA_ROOT + path, 'rb')
        im = Image.open(fp)

        if type(image_options) is list:
            for options in image_options:
                if options['type'] == 'p':
                    if type(options['size']) is tuple:
                        im.thumbnail((options['size'][0], options['size'][1]), Image.ANTIALIAS)
                        im.save('%s/%s/%s_%sx%s.%s' % 
                                (settings.MEDIA_ROOT, original_image_path, name, options['size'][0], \
                                options['size'][1], ext), quality=options['quality'])
                    else:
                        im.thumbnail((options['size'], options['size']), Image.ANTIALIAS)
                        im.save('%s/%s/%s_%sx%s.%s' % 
                                (settings.MEDIA_ROOT, original_image_path, name, options['size'], \
                                options['size'], ext), quality=options['quality'])
                elif options['type'] == 'w':
                    factor = height / (width / options['size'])
                    im.resize((options['size'], factor), Image.ANTIALIAS).save('%s/%s/%s_width_%s.%s' 
                                                                            % (settings.MEDIA_ROOT, original_image_path, name,\
                                                                             options['size'], ext), quality=options['quality'])
                elif options['type'] == 'h':
                    factor = width / (height / options['size'])
                    im.resize((factor, options['size']), Image.ANTIALIAS).save('%s/%s/%s_height_%s.%s' 
                                                                            % (settings.MEDIA_ROOT, original_image_path, name,\
                                                                             options['size'], ext), quality=options['quality'])
        fp.close()
    else:
        image_options.append({'type': 'original'})
        for options in image_options:
            if options['type'] == 'p':
                if type(options['size']) is tuple:
                    path = '%s/%s/%s_%sx%s.%s' % (settings.MEDIA_ROOT, original_image_path, name, options['size'][0], options['size'][1], ext)
                else:
                    path = '%s/%s/%s_%sx%s.%s' % (settings.MEDIA_ROOT, original_image_path, name, options['size'], options['size'], ext)
            elif options['type'] == 'w':
                path = '%s/%s/%s_width_%s.%s' % (settings.MEDIA_ROOT, original_image_path, name, options['size'], ext)
            elif options['type'] == 'h':
                path = '%s/%s/%s_height_%s.%s' % (settings.MEDIA_ROOT, original_image_path, name, options['size'], ext)
            else:
                path = '%s/%s/%s.%s' % (settings.MEDIA_ROOT, original_image_path, name, ext)

            if os.path.exists(path):
                os.remove(path)


class Group(SortableModel):
    name = models.CharField("Имя", max_length=255)
    slug = models.SlugField("URL Slug", max_length=255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    

class Catalog(models.Model):
    """
    docstring for Catalog
    """
    group = models.ManyToManyField(Group, verbose_name="Группы")
    
    name_short = models.CharField("Короткое имя", max_length=255)
    slug = models.SlugField("URL Slug", max_length=255)
    name_long = models.CharField("Название на главной", max_length=255, blank=True)
        
    description = models.TextField("Описание", blank=True)
    link_text = models.CharField("Текст ссылки", max_length=255, blank=True, default="Узнайте больше")
    type_a_name = models.CharField('Тип A', max_length=255, blank=True,)
    type_b_name = models.CharField('Тип B', max_length=255, blank=True,)
    
    big_sharp_picture = models.ImageField("Большое четкое изображение на главную", upload_to="catalogs", blank=True)
    big_blurry_picture = models.ImageField("Большое размытое изображение на внутреннюю", upload_to="catalogs", blank=True)
    medium_thumb = models.ImageField("Среднее изображение в список каталогов", upload_to="catalogs", blank=True)
    small_thumb = models.ImageField("Малое изображение во всплывающую панель", upload_to="catalogs", blank=True)

    zone_title = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    zone_medium_one = models.OneToOneField(Zone, related_name="medium_one_zone", null=True, blank=True, editable=False)
    zone_medium_two = models.OneToOneField(Zone, related_name="medium_two_zone", null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __unicode__(self):
        return unicode(self.name_short)
    
    def save(self, *args, **kwargs):
        if self.id == None:
            zone_title = Zone()
            zone_title.save()
            self.zone_title = zone_title
            zone_medium_one = Zone()
            zone_medium_one.save()
            self.zone_medium_one = zone_medium_one
            zone_medium_two = Zone()
            zone_medium_two.save()
            self.zone_medium_two = zone_medium_two
            
            #alphabet
            words = self.name_short.split()
            for word in words:
                letter = word[0].upper()
                try:
                    current_letter = Alphabet.objects.get(letter=letter)
                    if not current_letter.is_action:
                        current_letter.is_action = True
                        current_letter.save()
                except Alphabet.DoesNotExist:
                    letter = Alphabet(letter=letter, is_action=True)
                    letter.save()
        super(Catalog, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone_title.delete()
        self.zone_medium_one.delete();
        self.zone_medium_two.delete(); 


class GroupingUnit(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL Slug')
    description = models.TextField('Описание', blank=True)
    
    show_on_site = models.BooleanField('Показать на сайте?', default=True)
    
    big_blurry_picture = models.ImageField("Большое размытое изображение на внутреннюю", upload_to="groupings", blank=True)
    medium_thumb = models.ImageField("Среднее изображение в список каталогов", upload_to="groupings", blank=True)

    catalog = models.ManyToManyField(Catalog, verbose_name='Каталог')

    def __unicode__(self):
        return self.name

class Manufacturer(GroupingUnit):

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def get_zone(self, path):
        try:
            zones = ManufacturerZoneUrl.objects.get(url=path)
            return {'zone_title': zones.zone_title,
                    'zone_medium_one': zones.zone_medium_one,
                    'zone_medium_two': zones.zone_medium_two}
        except:
            zones = ManufacturerZoneUrl(url=path)
            zones.save()
            zones = ManufacturerZoneUrl.objects.get(url=path)
            return {'zone_title': zones.zone_title,
                    'zone_medium_one': zones.zone_medium_one,
                    'zone_medium_two': zones.zone_medium_two}

class TypeA(GroupingUnit):
    
    zone_title = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    zone_medium_one = models.OneToOneField(Zone, related_name="TypeA_medium_one_zone", null=True, blank=True, editable=False)
    zone_medium_two = models.OneToOneField(Zone, related_name="TypeA_medium_two_zone", null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = 'ТипA'
        verbose_name_plural = 'ТипыA'
    
    def save(self, *args, **kwargs):
        if self.id == None:
            zone_title = Zone()
            zone_title.save()
            self.zone_title = zone_title
            zone_medium_one = Zone()
            zone_medium_one.save()
            self.zone_medium_one = zone_medium_one
            zone_medium_two = Zone()
            zone_medium_two.save()
            self.zone_medium_two = zone_medium_two
        super(TypeA, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone_title.delete()
        self.zone_medium_one.delete()
        self.zone_medium_two.delete()

class TypeB(GroupingUnit):
    
    zone_title = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    zone_medium_one = models.OneToOneField(Zone, related_name="TypeB_medium_one_zone", null=True, blank=True, editable=False)
    zone_medium_two = models.OneToOneField(Zone, related_name="TypeB_medium_two_zone", null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = 'ТипB'
        verbose_name_plural = 'ТипыB'
    
    def save(self, *args, **kwargs):
        if self.id == None:
            zone_title = Zone()
            zone_title.save()
            self.zone_title = zone_title
            zone_medium_one = Zone()
            zone_medium_one.save()
            self.zone_medium_one = zone_medium_one
            zone_medium_two = Zone()
            zone_medium_two.save()
            self.zone_medium_two = zone_medium_two
        super(TypeB, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone_title.delete()
        self.zone_medium_one.delete()
        self.zone_medium_two.delete()

class Product(models.Model):
    """
    Product
    """

    STATUS_CHOICES = (
        (1, 'Снят с производства'),
        (2, 'Под заказ'),
        (3, 'В наличии'),
        (4, 'Ожидается поступление'),
    )

    DELIVERY_PERIOD_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )

    UNIT_CHOICES = (
        (1, 'ед. - единица'),
        (2, 'изд.'),
        (3, 'кг.'),
        (4, 'л. - литр'),
        (5, 'м.'),
        (6, 'м.(квадратный)'),
        (7, 'м.(кубический)'),
        (8, 'набор'),
        (9, 'метр погонный'),
        (10, 'рул. - рулон'),
        (11, 'т. - тонна'),
        (12, 'упак. - упаковка'),
        (13, 'ч. - час'),
        (14, 'шт.'),
        (15, 'меш. - мешок'),
    )

    name = models.CharField('Имя продукта', max_length=255,)
    desc_full = models.TextField('Полное описание', blank=True)
    desc_short = models.CharField('Краткое описание', max_length=255, blank=True)
    articul = models.CharField('Артикул', max_length=30, blank=True)
    slug = models.SlugField('Slug', max_length=255, blank=True)
    count_in_the_presence = models.FloatField('Кол-во в наличии', blank=True, default=0)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.PositiveIntegerField('Скидка %', blank=True, max_length=2, null=True, default=0)
    status = models.PositiveIntegerField('Статус', choices=STATUS_CHOICES, blank=True, null=True)
    unit = models.PositiveIntegerField('Единицы измерения', choices=UNIT_CHOICES, blank=True, null=True)
    delivery_period = models.PositiveIntegerField('Срок доставки', choices=DELIVERY_PERIOD_CHOICES, blank=True, null=True)
    count_like = models.PositiveIntegerField('Кол-во "лайков"', blank=True, null=True, default=0)
    
    top_order = models.IntegerField('Рейтинг товара', blank=True, null=True, default=0)

    is_publish = models.BooleanField('Публиковать?', blank=True, default=True)
    is_action = models.BooleanField('Акция?', blank=True, default=True)

    catalog = models.ForeignKey(Catalog, verbose_name='К какому каталогу?', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Какой производитель?', blank=True, null=True)

    types = models.ManyToManyField(TypeA, blank=True, null=True)
    type_b = models.ManyToManyField(TypeB, blank=True, null=True)
    picture = models.ManyToManyField('Picture', blank=True, null=True)
    
    zone = models.OneToOneField(Zone, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if not self.discount:
            self.discount = 0
        if not self.count_in_the_presence:
            self.count_in_the_presence = 0
        if not self.price:
            self.price = 0
        super(Product, self).save(*args, **kwargs)
        if self.articul == '':
            self.articul = 'A-' + str(self.id)
            super(Product, self).save(*args, **kwargs)

    def discounted(self):
        if self.discount == 0:
            return self.price
        else:
            return self.price - (self.price * self.discount/100)

    def get_unit(self):
        unit = ('', 'ед. - единица', 'изд.', 'кг', 'л. - литр', 'м.', 'м<sup>2</sup>', 'м<sup>3</sup>', 'набор', 
                'метр погонный', 'рул. - рулон', 'т. - тонна', 'упак. - упаковка', 'ч. - час', 'шт.', 'меш. - мешок')
        return unit[self.unit]
    
    def get_url(self):
        path = '/production/'
        if self.catalog.slug:
            path += self.catalog.slug + '/'
        if self.manufacturer.slug:
            path += self.manufacturer.slug + '/'
        if self.types.all():
            path += self.types.all()[0].slug + '/'
        if self.setgroup_set.all():
            path += 'set-' + self.setgroup_set.all()[0].set.slug + '/'
        path += 'pos-' + self.slug + '/'
        return path


class CatalogBrandType(models.Model):
    brand = models.ForeignKey(Manufacturer, verbose_name='Производитель')
    catalog = models.ForeignKey(Catalog, verbose_name='Каталог')
    type = models.ManyToManyField(TypeA, verbose_name='Типы', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Связь производителя с каталогом и типами'
        verbose_name_plural = 'Связь производителя с каталогом и типами'
    
    def __unicode__(self):
        return '%s(%s)' % (self.brand.name, self.catalog.name_short)


class Picture(models.Model):
    picture = models.ImageField('Изображение', upload_to='catalog/pictures/')
    name = models.CharField('Название', max_length=255, blank=True)
    alt = models.CharField('alt', max_length=255, blank=True)
    title = models.CharField('title', max_length=255, blank=True)
    link = models.CharField('Ссылка', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __unicode__(self):
        if self.name == '':
            return 'noname'
        else:
            return self.name

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Picture, self).save(*args, **kwargs)
            original_image = Picture.objects.get(pk=self.id).picture
            thumbnail(original_image.name, IMAGE_OPTIONS)
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        original_image = Picture.objects.get(pk=self.id).picture
        thumbnail(original_image.name, IMAGE_OPTIONS, False)

        super(Picture, self).delete(*args, **kwargs)
                    
    def get_image(self):
        original_image = Picture.objects.get(pk=self.id).picture
        original_image_name = original_image.name.split('/')[-1]
        original_image_path = '/'.join(original_image.name.split('/')[0:-1])
        name, ext = original_image_name.split('.')
        image= []
        for option in IMAGE_OPTIONS:
                if option['type'] == 'p':
                    image.append('%s%s/%s_%sx%s.%s' % (settings.MEDIA_URL, original_image_path, name, option['size'], option['size'], ext))
                elif option['type'] == 'h':
                    image.append('%s%s/%s_height_%s.%s' % (settings.MEDIA_URL, original_image_path, name, option['size'], ext))
                elif option['type'] == 'w':
                    image.append('%s%s/%s_width_%s.%s' % (settings.MEDIA_URL, original_image_path, name, option['size'], ext))
                
        return image

#class instance of Zones

class Zones(models.Model):
    zone = models.OneToOneField(Zone, null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone_title = zone
        super(self.__class__.__name__, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(self.__class__.__name__, self).delete(*args, **kwargs)

class ZoneProductHead(Zones):
    pass

class ZoneProductFoot(Zones):
    pass

class Alphabet(models.Model):
    letter = models.CharField('Буква', max_length=1)
    is_action = models.BooleanField('Активна?', default=True)
    
    class Meta:
        verbose_name = 'Алфавит'
        verbose_name_plural = 'Алфавит'
    
    def __unicode__(self):
        if self.is_action:
            return '%s' % (self.letter)
        else:
            return '!%s' % (self.letter)

class Set(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('SLUG', max_length=255, unique=True)
    
    zone_one = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    zone_two = models.OneToOneField(Zone, related_name="two_zone", null=True, blank=True, editable=False)
    zone_three = models.OneToOneField(Zone, related_name="three_zone", null=True, blank=True, editable=False)
    zone_four = models.OneToOneField(Zone, related_name="four_zone", null=True, blank=True, editable=False)
    
    top_order = models.IntegerField('Рейтинг сэта', blank=True, null=True, default=0)
    
    picture = models.ManyToManyField(Picture, blank=True, null=True)
    
    catalog = models.ForeignKey(Catalog)
    brand = models.ForeignKey(Manufacturer, blank=True, null=True)
    type_a = models.ForeignKey(TypeA, blank=True, null=True)
    product = models.ManyToManyField(Product, verbose_name="Продукты", blank=True)

    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сет'
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id == None:
            zone_one = Zone()
            zone_one.save()
            self.zone_one = zone_one
            zone_two = Zone()
            zone_two.save()
            self.zone_two = zone_two
            zone_three = Zone()
            zone_three.save()
            self.zone_three = zone_three
            zone_four = Zone()
            zone_four.save()
            self.zone_four = zone_four
            super(Set, self).save(*args, **kwargs)
            
            set = Set.objects.get(pk=self.id)
            set_group = SetGroup(name="Основная группа", set=set)
            set_group.save()
            
        super(Set, self).save(*args, **kwargs)
    
    def delete(self):
        self.zone_one.delete()
        self.zone_two.delete()
        self.zone_three.delete()
        self.zone_four.delete()

    def get_url(self):
        result =  '/production/'
        result += self.catalog.slug + '/'
        if self.type_a:
            result += self.type_a.slug + '/'
        if self.brand:
            result += self.brand.slug + '/'
        
        result += 'set-' + self.slug
        return result


class SetGroup(models.Model):
    name = models.CharField('Название', max_length=255)
    set = models.ForeignKey(Set, verbose_name='К какому сету?', blank=True, null=True)
    product = models.ManyToManyField(Product, verbose_name="Продукты", blank=True)
    
    class Meta:
        verbose_name = 'Группа Сэта'
        verbose_name_plural = 'Группы Сэтов'
    
    def __unicode__(self):
        return self.name
    
class ManufacturerZoneUrl(models.Model):
    url = models.CharField('URL', max_length=255)
    
    zone_title = models.OneToOneField(Zone, null=True, blank=True, editable=False)
    zone_medium_one = models.OneToOneField(Zone, related_name="Manufacturer_medium_one_zone", null=True, blank=True, editable=False)
    zone_medium_two = models.OneToOneField(Zone, related_name="Manufacturer_medium_two_zone", null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = 'Зона с привязкой к url для производителя'
        verbose_name_plural = 'Зоны с привязкой к url для производителя'

    def __unicode__(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if self.id == None:
            zone_title = Zone()
            zone_title.save()
            self.zone_title = zone_title
            zone_medium_one = Zone()
            zone_medium_one.save()
            self.zone_medium_one = zone_medium_one
            zone_medium_two = Zone()
            zone_medium_two.save()
            self.zone_medium_two = zone_medium_two
        super(ManufacturerZoneUrl, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.zone_title.delete()
        self.zone_medium_one.delete()
        self.zone_medium_two.delete()
        super(ManufacturerZoneUrl, self).delete(*args, **kwargs)
