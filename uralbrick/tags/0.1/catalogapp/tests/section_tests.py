# -*- coding: utf-8 -*-

from django.test import TestCase
from catalogapp import api
from catalogapp import models


class SectionsTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(SectionsTest, self).__init__(*args, **kwargs)
        # Set test sps_array
        self.sps_array = [{
            "field_type": "BooleanField",
            "name": "boolfield",
            "slug": "bool_slug",
            "default_value": True,
            "description": "Some desc",
        },
        {
            "field_type": "TextField",
            "name": "charfield",
            "slug": "char_slug",
            "default_value": "some string",
            "description": "Some desc",
        },]


    def test_create(self):
        result_id = api.sections.create("Name", "slug")

        self.assertTrue(isinstance(result_id, int))

    def test_delete(self):
        result_id = api.sections.create("Name", "slug")
        result = api.sections.delete(result_id)
        self.assertTrue(result)

    def test_rename(self):
        # Test name
        result_id = api.sections.create("Name", "slug")
        api.sections.rename(result_id, "New name")
        section = api.sections.get(result_id)
        self.assertEqual(section.name, "New name")
        self.assertEqual(section.slug, "slug")
        # Test name + slug
        api.sections.rename(result_id, "New name 2", "someslug")
        section = api.sections.get(result_id)
        self.assertEqual(section.name, "New name 2")
        self.assertEqual(section.slug, "someslug")

    def test_addFields(self):
        section_id = api.sections.create("Name", "slug")
        result = api.sections.addFields(section_id, self.sps_array)
        self.assertEqual(result, [1, 2])

    def test_removeFields(self):
        # Create 4 fields
        section_id = api.sections.create("Name", "slug")
        result = api.sections.addFields(section_id, self.sps_array)
        result = api.sections.addFields(section_id, self.sps_array)

        # Direct access to field objects only for test
        c = models.BaseField.objects.filter(section__id=section_id).count()
        self.assertEqual(c, len(self.sps_array)*2)

        result = api.sections.removeFields(section_id, [1,3])

        # Direct access to field objects only for test
        c = models.BaseField.objects.filter(section__id=section_id)

        self.assertEqual(len(c), len(self.sps_array)*2-2)
        self.assertEqual(c[0].id, 2)
        self.assertEqual(c[1].id, 4)

    def test_getFields(self):
        section_id = api.sections.create("Name", "slug")
        
        # Create 4 fields
        result = api.sections.addFields(section_id, self.sps_array)
        result = api.sections.addFields(section_id, self.sps_array)

        fields = api.sections.getFields(section_id)

        self.assertEqual(len(fields), len(self.sps_array)*2)

    def test_list(self):
        api.sections.create("Name", "slug")
        api.sections.create("Name", "slug2")
        sections = api.sections.list(name='Name')

        self.assertEqual(len(sections), 2)

    def test_listIn(self):
        ids = []
        section_id = api.sections.create("Name", "slug")
        ids.append(section_id)
        api.sections.create("Name", "slug2")
        api.sections.create("Name", "slug")
        section_id = api.sections.create("Name", "slug2")
        ids.append(section_id)

        sections = api.sections.listIn(ids)

        self.assertEqual(len(sections), 2)