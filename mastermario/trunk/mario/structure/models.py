# -*- coding: utf-8 -*-

import pytils
import urllib

from django.db import models
from django.utils.encoding import smart_str
from utils.models import SortableModel
from widgets.models import Zone
from utils.tree import build_tree

class Section(SortableModel):

    order_isolation_fields = ('parent',)

    subpath = ''

    caption = models.CharField("Название (наименование, имя)", max_length=255)
    path = models.CharField("Путь URL", max_length=255)
    type = models.ForeignKey('SectionType', verbose_name="Тип")
    parent = models.ForeignKey('Section', verbose_name="Родительский раздел", 
                               blank=True, null=True, related_name='children')
    is_enabled = models.BooleanField(default=True)

    zone = models.OneToOneField(Zone, null=True, blank=True)

    def __unicode__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
        super(Section, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(Section, self).delete(*args, **kwargs)    

    def create_child(self, caption, slug='', section_type=None):
        return self.__class__.create_section(self, caption, slug, section_type)

    def create_sibling(self, caption, slug='', section_type=None):
        # @todo check if user tries to create sibling of the root
        return self.__class__.create_section(self.parent, caption, 
                                             slug, section_type)
    def get_absolute_url(self):
        return "%s" % urllib.quote(smart_str(self.path))

    @staticmethod
    def create_section(parent, caption, slug='', section_type=None):
        section = Section()
        section.caption = caption

        if slug == '':
            slug = pytils.translit.slugify(caption)

        if section_type is None:
            section.type = parent.type.inherit_type
        else:
            section.type = section_type

        while True:
            section.path = parent.path + slug + '/'
            if not Section.objects.filter(path=section.path):
                break
            else:
                slug += '_'
        
        section.parent = parent
        section.save()
        return section
    
    @staticmethod
    def get_structure():
        nodes = Section.objects.filter(is_enabled=True).values()
        return build_tree(nodes)

    @staticmethod
    def get_node_by_path(path):
        node = Section.objects.filter(is_enabled=True).extra(
            select={ "subpath": "SUBSTR(%s, LENGTH(path)+1)" },
            select_params=(path,),
            where=[""" 
                path = (
                    SELECT max(path) 
                    FROM structure_section 
                    WHERE locate(path, %s) = 1
                    AND is_enabled = 1
                )
            """], 
            params=(path,)
        )[0]
        return node

class SectionType(SortableModel):
    caption = models.CharField("Название (по-человечески)", max_length=255)
    slug = models.CharField("Идентификатор (slug)", max_length=255)
    description = models.TextField("Описание", blank=True)
    inherit_type = models.ForeignKey('SectionType', 
                                     verbose_name="Тип потомков по умолчанию", 
                                     blank=True, null=True, 
                                     on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.caption
