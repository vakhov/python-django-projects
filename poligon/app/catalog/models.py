# -*- coding: utf8 -*-

import os

from django.db import models
from django.conf import settings

from structure.models import Section as StructureSection
from widgets.models import Zone
from utils.models import SortableModel

IMAGE_OPTIONS = [{'type': 'p', 'size': 150, 'quality': 100},
				{'type': 'w', 'size': 263, 'quality': 100},
				{'type': 'w', 'size': 345, 'quality': 100},
				{'type': 'w', 'size': 49,  'quality': 100},
				{'type': 'h', 'size': 257, 'quality': 100}]

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


class Section(StructureSection):
	class Meta:
		proxy = True
		verbose_name = 'Раздел'
		verbose_name_plural = 'Разделы'



class Catalog(models.Model):
	"""
	docstring for Catalog
	"""
	section = models.OneToOneField(Section, verbose_name='Раздел сайта', related_name='catalog')

	class Meta:
		verbose_name = 'Каталог'
		verbose_name_plural = 'Каталоги'

	def __unicode__(self):
		return unicode(self.section.caption)



class Manufacturer(models.Model):
	"""
	docstring for Manufacturer
	"""
	name = models.CharField('Название', max_length=255)
	desc = models.TextField('Описание', blank=True)

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'

	def __unicode__(self):
		pass



class Type(models.Model):
	"""
	docstring for Type
	"""
	pass

	class Meta:
		verbose_name = 'Тип'
		verbose_name_plural = 'Типы'

	def __unicode__(self):
		pass



class Product(models.Model):
	"""
	Product
	"""

	STATUS_CHOICES = (
		('1', 'Снят с производства'),
		('2', 'Под заказ'),
		('3', 'В наличии'),
		('4', 'Ожидается поступление'),
	)

	DELIVERY_PERIOD_CHOICES = (
		('1', 'A'),
		('2', 'B'),
		('3', 'C'),
		('4', 'D'),
	)

	UNIT_CHOICES = (
		('1', 'ед. - единица'),
		('2', 'изд.'),
		('3', 'кг.'),
		('4', 'л. - литр'),
		('5', 'м.'),
		('6', 'м.(квадратный)'),
		('7', 'м.(кубический)'),
		('8', 'набор'),
		('9', 'метр погонный'),
		('10', 'рул. - рулон'),
		('11', 'т. - тонна'),
		('12', 'упак. - упаковка'),
		('13', 'ч. - час'),
		('14', 'шт.'),
		('15', 'меш. - мешок'),
	)

	name = models.CharField('Имя продукта', max_length=255,)
	desc_full = models.TextField('Полное описание', blank=True)
	desc_short = models.CharField('Краткое описание', max_length=255, blank=True)
	articul = models.CharField('Артикул', max_length=30, blank=True)
	slug = models.SlugField('Slug', max_length=255, blank=True)
	count_in_the_presence = models.FloatField('Кол-во в наличии', blank=True, default=0)
	price = models.DecimalField('Цена', max_digits=10, decimal_places=2, blank=True, null=True)
	discount = models.PositiveIntegerField('Скидка %', blank=True, null=True, default=0)
	status = models.PositiveIntegerField('Статус', choices=STATUS_CHOICES, blank=True, null=True)
	unit = models.PositiveIntegerField('Единицы измерения', choices=UNIT_CHOICES, blank=True, null=True)
	delivery_period = models.PositiveIntegerField('Срок доставки', choices=DELIVERY_PERIOD_CHOICES, blank=True, null=True)
	count_like = models.PositiveIntegerField('Кол-во "лайков"', blank=True, null=True, default=0)

	is_publish = models.BooleanField('Публиковать?', blank=True, default=True)
	is_action = models.BooleanField('Акция?', blank=True, default=True)

	catalog = models.ForeignKey(Catalog, verbose_name='К какому каталогу?', blank=True, null=True)
	manufacturer = models.ForeignKey(Manufacturer, verbose_name='Какой производитель?', blank=True, null=True)

	types = models.ManyToManyField(Type, verbose_name='Тип', blank=True, null=True)
	picture = models.ManyToManyField('Picture', verbose_name='Изображения', blank=True, null=True)


	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'

	def __unicode__(self):
		return '%s' % self.name

	def save(self, *args, **kwargs):
		super(Product, self).save(*args, **kwargs)
		if self.articul == '':
			self.articul = 'A-' + str(self.id)
			super(Product, self).save(*args, **kwargs)

	def discounted(srlf):
		if self.discount == 0:
			return self.price
		else:
			return self.price - (self.price * self.discount/100)



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

	def delete(self, *args, **kwargs):
		original_image = Picture.objects.get(pk=self.id).picture
		thumbnail(original_image.name, IMAGE_OPTIONS, False)

		super(Picture, self).delete(*args, **kwargs)
