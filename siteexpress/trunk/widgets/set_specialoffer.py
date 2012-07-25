# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from models import Widget
from grouping import create_group, add2group
from utils.thumbs import ImageWithThumbsField
from tinymce import models as tinymce_model

create_group('common', 'Другие')

def resize(path, path_in, size):
    original_image_name = path.split('/')[-1]
    name, ext = original_image_name.split('.', 1)

    import Image
    width, height = Image.open(path).size
    factor = float(height) / (float(width) / float(size))
    fp = open(path, 'rb')
    im = Image.open(fp)
    im.resize((size, int(factor)), Image.ANTIALIAS).save('%s/%s.%sx%s.%s' % ( path_in, name, size, size, ext), quality=100)
    fp.close()


@add2group('Спец.предложение', 'common')
class SpecialOffer(Widget):
    image = models.ImageField('Изображение', upload_to='specialoffer_widgets/image/', blank=True, null=True)
    title = models.CharField('Заголовок', max_length=255,)
    desc = tinymce_model.HTMLField('Описание', max_length=255, blank=True,)
    link = models.CharField('Ссылка', max_length=255, blank=True,)

    def save(self, *args, **kwargs):
        super(SpecialOffer, self).save(*args, **kwargs)
        if self.image:
            path = settings.MEDIA_ROOT + self.image.name
            path_in = settings.MEDIA_ROOT + 'specialoffer_widgets/image'
            size_w = 250
            resize(path, path_in, size_w)

    def get_thumb(self):
        splitted_name = self.image.name.split('.', 1)
        name, ext = '.'.join(splitted_name[:-1]), splitted_name[-1]
        new_name = '%s.250x250.%s' % (name, ext)
        return settings.MEDIA_URL + new_name
