# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from structure.models import Section, SectionType
from utils.tree import build_tree
import pytils 

class Document(models.Model):
    caption = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.caption
        if self.id is None:
            super(Document, self).save(*args, **kwargs)
            section_type = SectionType.objects.get(pk=1)
            Part.objects.create(caption=self.caption, document=self, path='/', type=section_type)
        else:
            super(Document, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.caption

    def create_part(self, parent, caption, slug='', section_type=None):
        section_type = SectionType.objects.get(pk=1)
        part = Part.create_section(self, parent, caption, slug, section_type)
        return part

    def get_parts_tree(self):
        nodes = Part.objects.filter(document=self).values()
        return build_tree(nodes)

    def get_part_by_path(self, path):
        path = '/' + path + '/'
        node = Part.objects.extra(
            select={ "subpath": "SUBSTR(%s, LENGTH(path)+1)" },
            select_params=(path,),
            where=[""" 
                path = (
                    SELECT max(path) 
                    FROM structure_section ss
                    INNER JOIN documents_part dp
                    ON ss.id = dp.section_ptr_id 
                    WHERE locate(ss.path, %s) = 1
                    AND dp.document_id = %s                    
                )
            """], 
            params=(path, self.id)
        )[0]
        return node

    
class Part(Section):
    order_isolation_fields = ('document', 'parent')    
    document = models.ForeignKey(Document)

    # x_x

    @staticmethod
    def create_section(document, parent, caption, slug='', section_type=None):
        section = Part()
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
        section.document = document
        section.save()
        return section