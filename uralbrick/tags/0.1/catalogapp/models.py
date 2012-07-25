## -*- coding: utf-8 -*-
#
## Import models and models stuff
#from django.db import models
#from model_utils.managers import InheritanceManager
#from django_mongodb_engine.contrib import MongoDBManager
#from djangotoolbox.fields import EmbeddedModelField, ListField
#
#import cPickle as pickle
#import copy
#from django.core import exceptions
#
#class Section(models.Model):
#    name = models.CharField(max_length=255)
#    slug = models.SlugField()
#
#    def get_fields_ids(self):
#        return BaseField.objects.filter(section=self).values_list('id', flat=True)
#
#    def get_fields(self):
#        return BaseField.objects.filter(section=self).select_subclasses()
#
#    def __unicode__(self):
#        return self.name
#
#
#class BaseField(models.Model):
#    """ Базовый класс для кастомных полей
#        Он не абстрактный, чтобы не плодить кучу таблиц,
#        но требует переопределения атрибутов"""
#    name = models.CharField(max_length=255)
#    slug = models.SlugField()
#    section = models.ForeignKey(Section)
#    default_value = models.CharField(max_length=255)
#    description = models.TextField()
#
#    objects = InheritanceManager()
#
#    # Представление поля в виде django филда
#    django_field = None # You MUST define it in subclass
#    # Атрибуты Django филда
#    django_field_attrs = {}
#
#    def create_django_field(self, model):
#        """ Создаем новый Django Field """
#        # И передаем ему дополнительные аргументы
#        new_field = getattr(models, self.django_field)(**self.django_field_attrs)
#        # Устанавливаем атрибуты поля из его имени
#        new_field.set_attributes_from_name(self.name)
#        # Устанавливаем модель полю
#        new_field.model = model
#        return new_field
#
#    def add_field(self, model_instance):
#        """ Функция добавления поля """
#        new_field = self.create_django_field(model_instance.__class__)
#        # Добавляем поле в мета модели
#        model_instance._meta.add_field(new_field)
#
#    def __unicode__(self):
#        return self.name
#
#
#class BooleanField(BaseField):
#    django_field = 'BooleanField'
#
#
#class CharField(BaseField):
#    django_field = 'CharField'
#    django_field_attrs = {'max_length': 255}
#
#
#class IntegerField(BaseField):
#    django_field = 'IntegerField'
#
#
#class TextField(BaseField):
#    django_field = 'TextField'
#
#
#class ChoiceField(BaseField):
#    choices_store = models.TextField()
#    django_field = 'IntegerField'
#    django_field_attrs = {'max_length': 255}
#
#    def _get_choices(self):
#        if not hasattr(self, '_choices') or self._choices is None:
#            self._choices = pickle.loads(str(self.choices_store))
#        return self._choices
#
#    def _set_choices(self, value):
#        self._choices = value
#        self.choices_store = pickle.dumps(self._choices)
#
#    choices = property(_get_choices, _set_choices)
#
#    def add_field(self, model_instance):
#        self.django_field_attrs['choices'] = self.choices
#        super(ChoiceField, self).add_field(model_instance)
#
#
#class MultipleChoiceField(BaseField):
#    """ InheritanceManager не поддерживает наследование более 1 уровня,
#        поэтому не наследуемся, а копи-пастим ChoiceField """
#
#    choices_store = models.TextField()
#    django_field = 'CommaSeparatedIntegerField'
#    django_field_attrs = {'max_length': 255}
#
#    def _get_choices(self):
#        if not hasattr(self, '_choices') or self._choices is None:
#            self._choices = pickle.loads(str(self.choices_store))
#        return self._choices
#
#    def _set_choices(self, value):
#        self._choices = value
#        self.choices_store = pickle.dumps(self._choices)
#
#    choices = property(_get_choices, _set_choices)
#
#    def validation(self, value):
#        """ CommaSeparatedIntegerField не поддерживает валидацию чойзов,
#        поэтому она тут. Не уверен, что это верно  """
#        values = value.split(",")
#        for v in values:
#            if not v in map(lambda x: str(x[0]), self.choices):
#                raise exceptions.ValidationError("Invalid choice: %s" % v)
#
#    def add_field(self, model_instance):
#        """ Переопределяем метод добавления филда к модели, присунув наш
#            валидатор """
#        if not self.django_field_attrs.has_key('validation'):
#            self.django_field_attrs['validators'] = []
#        self.django_field_attrs['validators'].append(self.validation)
#        super(MultipleChoiceField, self).add_field(model_instance)
#
#
#class Brand(models.Model):
#    name = models.CharField(max_length=255)
#    slug = models.SlugField()
#
#    def __unicode__(self):
#        return self.name
#
#
#class Good(models.Model):
#    """ Класс продуктов """
#    name = models.CharField(max_length=255)
#    slug = models.SlugField()
#    section_id = models.IntegerField()
#    articul = models.CharField(max_length=255, blank=True)
#    label = models.CharField(max_length=255, blank=True)
#    shortdesc = models.TextField(blank=True)
#    price_in = models.IntegerField()
#    price_out = models.IntegerField()
#    brands = ListField()
#
#    objects = MongoDBManager()
#
#    def __init__(self, *args, **kwargs):
#        self._meta = copy.deepcopy(self._meta)
#        # Достаем section, можем брать как из args, так и из kwargs
#        section_id = None
#        if len(args)>=4:
#            section_id = args[3]
#        else:
#            section_id = kwargs.get('section_id')
#        # Добавляем поля раздела
#        kwargs = self._set_extra_fields(section_id, kwargs)
#        super(Good, self).__init__(*args, **kwargs)
#
#    def _set_extra_fields(self, section_id, kwargs):
#        if not section_id is None:
#            section = Section.objects.get(id=section_id)
#            # Достаем все специфичные поля раздела
#            fields = section.get_fields()
#
#            for field in fields:
#                field.add_field(self)
#                if not field.name in kwargs:
#                    kwargs[field.name] = field.default_value
#        return kwargs
#
#    def __unicode__(self):
#        return self.name
#
#    def save(self):
#        super(Good, self).save()
#
#        if self.articul is None or self.articul == "":
#            self.articul = self.id
#            self.save()