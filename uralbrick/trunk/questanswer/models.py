# -*- coding: utf-8 -*-

from django.db import models
import datetime

class QuestAnswer(models.Model):
    author = models.CharField(verbose_name="Пользователь оставивший запись", max_length=255, default="Гость",)
    date_publication = models.DateTimeField(verbose_name="Дата написания", null=True, blank=True, default=datetime.datetime.now,)
    question_short = models.CharField(verbose_name="Краткий вопрос", max_length=255, blank=True)
    question = models.TextField(verbose_name="Вопрос")
    moderator = models.CharField(verbose_name="Имя модератора", max_length=255, blank=False)
    position = models.CharField(verbose_name="Должность модератора", max_length=255, blank=False)
    answer = models.TextField(verbose_name="Ответ", blank=True)
    is_public = models.BooleanField("Опубликовать?", default=False)
    tag = models.ManyToManyField("TagName", verbose_name="Тэг", blank=True, null=True)

    def __unicode__(self):
    	return self.author

    class Meta:
        verbose_name = u'Вопрос-ответ'
        verbose_name_plural = u'Вопрос-ответ'

class TagName(models.Model):
    name = models.CharField("Тэг", max_length=255, blank=False)
    slug = models.SlugField("Слаг", max_length=255, blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        #alphabet
        ### прикрутить юникод
        words = self.name.split()
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
        super(TagName, self).save(*args, **kwargs)

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