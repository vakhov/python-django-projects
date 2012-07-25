# -*- coding: utf-8 -*-

import datetime
import Image
import ImageEnhance
import os

from django.db import models
from django.conf import settings
from structure.models import Section 
# from utils.colorfield import ColorPickerWidget
from utils.thumbs import ImageWithThumbsField 
from tinymce import models as tinymce_model
from widgets.models import Zone
from utils.sortable import SortableModel


def add_watermark(image, watermark, opacity=1):
    import Image
    import ImageEnhance

    assert opacity >= 0 and opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            self.watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    layer.paste(watermark, (0, (image.size[1]/2)-(watermark.size[1]/2)))
    return Image.composite(layer,  image,  layer)

def thumbnail(path, sizes, watermark=None, ratio=False):
    """
    Функция создания превью с возможностью наложения водяных знаков.
    При этом фото лежит в любой папке, а превью помещаются на уровень выше.
    -path - Полный путь до изображения
    -sizes - Список, содержащий кортежи со значениями высоты и ширины
    -watermark - Полный путь до водяного знака
    """
    import Image
    import os

    original_path = path
    path_to_save = '/'.join(path.split('/')[0:-2])

    splitted_name = (path.split('/')[-1]).split('.')
    name, ext = '.'.join(splitted_name[:-1]), splitted_name[-1]

    if watermark:
        fp = open(path, "rb")
        im = Image.open(fp)
        size = sizes.pop(0)
        im.thumbnail((size[0], size[1]), Image.ANTIALIAS)
        im.save('%s/%s.%s' % (path_to_save, name, ext), quality=100)
        fp.close()
        fp = open(path_to_save + '/' + name + '.' + ext, "rb")
        im_1000 = Image.open(fp)
        mark = Image.open(watermark)
        result = add_watermark(im_1000, mark)
        result.save('%s/%s.%s' % (path_to_save, name, ext), quality=100)
        #result.save('{0}/{1}.{2}x{3}.{4}'.format(path_to_save, name, size[0], size[1], ext), quality=100)
        result.save('%s/%s.%sx%s.%s' % (path_to_save, name, size[0], size[1], ext), quality=100)
        fp.close()
        for size in sizes:
            fp = open(path_to_save + '/' + name + '.' + ext, "rb")
            im_1000 = Image.open(fp)
            im_1000.thumbnail((size[0], size[1]), Image.ANTIALIAS)
            im_1000.save('%s/%s.%sx%s.%s' % (path_to_save, name, size[0], size[1], ext), quality=100)
            #im_1000.save('{0}/{1}.{2}x{3}.{4}'.format(path_to_save, name, size[0], size[1], ext), quality=100)
            fp.close()
        if os.path.exists(path_to_save + '/' + name + '.' + ext):
            os.remove(path_to_save + '/' + name + '.' + ext)
    else:
        for size in sizes:
            im = Image.open(path)
            im.thumbnail((size[0], size[1]), Image.ANTIALIAS)
            im.save('%s/%s.%sx%s.%s' % (path_to_save, name, size[0], size[1], ext), quality=100)
            #im.save('{0}/{1}.{2}x{3}.{4}'.format(path_to_save, name, size[0], size[1], ext), quality=100)
    


def get_image_url(url, sizes):
    result = {}
    url_thumbnail = '/'.join(url.split('/')[0:-2])
    splitted_name = (url.split('/')[-1]).split('.')
    name, ext = '.'.join(splitted_name[:-1]), splitted_name[-1]
    for size in sizes:
        #result.update({ u'{0}x{1}'.format(size[0], size[1]) : u'{0}/{1}.{2}x{3}.{4}'.format(url_thumbnail, name, size[0], size[1], ext)})
        key = '%sx%s' % (size[0], size[1])
        value = '%s/%s.%sx%s.%s' % (url_thumbnail, name, size[0], size[1], ext)
        result.update({ key : value })
    return result





# Общие свойства сайта
class Globals(models.Model):
    prop_slug = models.SlugField("Идентификатор свойства", max_length=32)
    prop_name = models.CharField("Название свойства", max_length=255)
    value = models.CharField("Значение", max_length=255)

    class Meta:
        verbose_name='Общее свойство'
        verbose_name_plural='Общие свойства'
    
    def __unicode__(self):
        return self.prop_name

# Позиция каталога
class Position(SortableModel):
    
    order_isolation_fields = ('section',)
    
    caption = models.CharField(verbose_name="Заголовок", max_length=255,)
    desc_short = models.TextField(verbose_name="Краткое описание", blank=True,)
    desc_full = tinymce_model.HTMLField(verbose_name="Полное (развернутое) описание", editable=False, blank=True,)
    is_exists = models.BooleanField(verbose_name="В наличии?", default=True,)
    article = models.CharField(verbose_name="Артикул", blank=True, max_length=255,)
    price_opt = models.DecimalField(verbose_name="Цена оптовая", max_digits=12, decimal_places=2, blank=True, null=True, editable=False)
    price_rozn = models.DecimalField(verbose_name="Цена розничная", max_digits=12, decimal_places=2, blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name="Раздел каталога")

    picture = models.ImageField("Изображение", upload_to='images/original/', blank=True, null=True)
    
    tags = models.ManyToManyField('Tag', verbose_name='Метки', blank=True)
    
    zone = models.OneToOneField(Zone, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
        super(Position, self).save(*args, **kwargs)
        if self.article == '':
            self.article = 'A-' + str(self.id)
        super(Position,self).save(*args,**kwargs)

        if self.picture:
            import Image
            sizes = [
                (1000, 1000),
                (300, 300),
                (150, 150),
            ]
            image = Position.objects.get(pk=self.id)
            path = image.picture.path
            watermark = settings.MEDIA_ROOT + 'watermark/1000.png'
            thumbnail(path, sizes, watermark)

    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(Position, self).delete(*args, **kwargs)   

    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'
    
    def __unicode__(self):
        return self.caption

    @staticmethod
    def get_image(position_id):
        image = Position.objects.get(pk=position_id)
        sizes = [
            (1000, 1000),
            (300, 300),
            (150, 150),
        ]
        result = []
        s = get_image_url(image.picture.name, sizes)
        result.append({'id': image.id, 'picture': s})
        return result

    def get_thumb(self):
        return get_image_url(self.picture.url, [(150,150)])['150x150']

# Тэги
class Tag(models.Model):
    tag = models.CharField("Имя тэга", max_length=30)
    name = models.SlugField("URL Slug", max_length=255)

    def __unicode__(self):
            return self.tag + ' (' + self.name + ')'
    
    class Meta:
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'

# Позиция "вопрос-ответа"    
class QuestAnswer(models.Model):
    author = models.CharField(verbose_name="Пользователь оставивший запись", max_length=255, default="Гость", editable=False)
    publication_date = models.DateTimeField(verbose_name="Дата написания", null=True, blank=True, default=datetime.datetime.now,)
    question = tinymce_model.HTMLField(verbose_name="Вопрос", )
    moderator = models.CharField(verbose_name="Имя модератора", max_length=255, blank=True, default="Менеджер",)
    answer = tinymce_model.HTMLField(verbose_name="Ответ", blank=True)
    # tags = models.ManyToManyField('Tag', blank=True,)
    is_public = models.BooleanField("Опубликовать?", default=False,)

    class Meta:
        verbose_name='Вопрос-ответ'
        verbose_name_plural='Вопросы-ответы'
    
    def __unicode__(self):
        return self.question
#Позиция "отзыв"
class FeedbackFlora(models.Model):
    author = models.CharField(u"ФИО", max_length=255, default="Гость")
    punkt = models.CharField(u'Населённый пункт', max_length=255, blank=True)
    work = models.CharField(u'Место работы', max_length=255, blank=True)
    question = tinymce_model.HTMLField(u"Текст сообщения", )
    publication_date = models.DateTimeField(u"Дата написания", null=True, blank=True, default=datetime.datetime.now,)
    moderator = models.CharField(u"Имя модератора", max_length=255, blank=True, default="Менеджер",)
    answer = tinymce_model.HTMLField(u"Ответ", blank=True)
    is_public = models.BooleanField(u"Опубликовать?", default=False,)

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'
    
    def __unicode__(self):
        return self.question

# Изображение    
class Image(models.Model):
    caption = models.CharField(verbose_name="Название изображения", max_length=255,)
    picture = ImageWithThumbsField(upload_to='images', sizes=((125,125),(200,200),(1000,1000)))

    class Meta:
        verbose_name='Изображение'
        verbose_name_plural='Изображения'

# Новость
class News(models.Model):
    caption = models.CharField(verbose_name="Заголовок", max_length=255,)
    slug = models.SlugField("URL", max_length=255, blank=True)
    announce = models.CharField(verbose_name="Краткий анонс", max_length=255, blank=True,)
    text = tinymce_model.HTMLField(verbose_name="Текст", blank=True,)
    date = models.DateTimeField(verbose_name="Дата написания", null=True, blank=True, default=datetime.datetime.now,)
    section = models.ForeignKey(Section, verbose_name=u'Раздел')
    zone = models.OneToOneField(Zone, null=True, blank=True, editable=False)

    class Meta:
        verbose_name='Новость'
        verbose_name_plural='Новости'
        
    def save(self, *args, **kwargs):
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
        super(News, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(News, self).delete(*args, **kwargs)
    
# Файл
class File(models.Model):
    caption = models.CharField(verbose_name="Название файла", max_length=255, blank=True,)
    files = models.FileField(upload_to='uploads')

    class Meta:
        verbose_name='Файл'
        verbose_name_plural='Файлы'

# Специальное предложение
class SpecialOffer(models.Model):
    caption = models.CharField(verbose_name="Заголовок спец.предложения", max_length=255,)
    picture = ImageWithThumbsField(upload_to='images', sizes=((125,125),(200,200)), blank=True, null=True)
    description = tinymce_model.HTMLField(verbose_name="Описание спец.предложения", blank=True,)
    price = models.DecimalField(verbose_name="Цена", blank=True, max_digits=12, decimal_places=2,)
    url_link = models.CharField(verbose_name="URL на указанную акцию", blank=True, max_length=255)
    is_active = models.BooleanField("Данная акция активна?", default=False,)

    class Meta:
        verbose_name='Специальное предложение'
        verbose_name_plural='Специальные предложения'
    
    def __unicode__(self):
        return self.caption
    
    @staticmethod
    def get_specialoffer():
        return SpecialOffer.objects.filter(is_active=True)

# "Заявка с сайта"
class Feedback(models.Model):
    sender = models.CharField("ФИО отправителя", max_length=255,)
    contact = tinymce_model.HTMLField("Контактная информация (# телефона, адрес, эл.адрес и т.д.)",)
    message = tinymce_model.HTMLField("Тело сообщения",)

    class Meta:
        verbose_name='Заявка'
        verbose_name_plural='Заявки'

class Pictures(models.Model):

    picture = models.ImageField('Изображение', upload_to='gallery_pictures/original/')
    caption = models.CharField(u'Альтернативая подпись', max_length=255, blank=True)
    model = models.CharField(u'Модель', max_length=50)
    relaition_id = models.IntegerField(u'привязать к id')
    
    class Meta:
        verbose_name=u'Галерея'
        verbose_name_plural=u'Галереи'
    
    def __unicode__(self):
        return self.picture.url

    def save(self, *args, **kwargs):
        super(Pictures, self).save(*args, **kwargs)
        import Image
        sizes = [
            (1000, 1000),
            (300, 300),
            (150, 150),
        ]
        image = Pictures.objects.get(pk=self.id)
        path = image.picture.path
        watermark = settings.MEDIA_ROOT + 'watermark/1000.png'
        thumbnail(path, sizes, watermark)

    @staticmethod
    def get_image(position_id, image_model):
        images = Pictures.objects.filter(relaition_id=position_id).filter(model=image_model)
        sizes = [
            (1000, 1000),
            (300, 300),
            (150, 150),
        ]
        result = []
        for image in images:
            s = get_image_url(image.picture.name, sizes)
            result.append({'id': image.id, 'picture': s})
        return result




# Common zone
class Phoneflora(models.Model):
    zone = models.OneToOneField(Zone, null=True, blank=True)
