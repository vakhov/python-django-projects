# -*- coding: utf-8 -*-

import pytils
from django.db import models
from utils.sortable import SortableModel
from widgets.models import Zone
from utils.tree import build_tree

class Section(SortableModel):

    order_isolation_fields = ('parent',)

    subpath = ''

    caption = models.CharField("Название (наименование, имя)", max_length=255)
    path = models.CharField("Путь URL", max_length=255, editable=False)
    type = models.ForeignKey('SectionType', verbose_name="Тип")
    parent = models.ForeignKey('Section', verbose_name="Родительский раздел", 
                               blank=True, null=True, related_name='children', editable=False)
    is_enabled = models.BooleanField(default=True)

    zone = models.OneToOneField(Zone, null=True, blank=True, editable=False)

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

    def get_slug(self):
        return self.path.split('/')[-2]

    def has_children(self):
        return Section.objects.filter(parent=self)[:1].count() == 1

    def get_descendants(self):
        return Section.objects.filter(path__startswith=self.path).exclude(pk=self.pk)

    def create_child(self, caption, slug='', section_type=None):
        return self.__class__.create_section(self, caption, slug, section_type)

    def create_sibling(self, caption, slug='', section_type=None):
        # @todo check if user tries to create sibling of the root
        return self.__class__.create_section(self.parent, caption, 
                                             slug, section_type)

    def change_slug(self, slug):
        old_path = self.path
        children = self.get_descendants()
        
        while True:
            self.path = self.parent.path + slug + '/'
            if not Section.objects.filter(path=self.path):
                break
            else:
                slug += '_'
                
        self.save()
        
        for child in children:
            child.path = child.path.replace(old_path, self.path)
            child.save()

    def change_parent(self, parent, order=None):
        """ Moves section to another parent """
        if parent != self.parent:
            # Setting order of widget to last in old zone
            # for other widgets to rearrange
            self.move(-1)
            # Changing zone and setting new order
            self.parent = parent
            self.order = 0
            self.save()
            
        if order is not None:
            self.move(order)
        else:
            self.move(-1)

        old_path = self.path
        children = self.get_descendants()
        
        slug = self.get_slug()
        while True:
            self.path = parent.path + slug + '/'
            if not Section.objects.filter(path=self.path):
                break
            else:
                slug += '_'
                
        self.save()
        
        for child in children:
            child.path = child.path.replace(old_path, self.path)
            child.save()

    @staticmethod
    def create_section(parent, caption, slug='', section_type=None):
        """
        Creates new section.
        - parent: Section object
        - caption: string
        - slug: string
        - section_type: SectionType object
        """
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