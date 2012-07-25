# -*- coding: utf-8 -*-

from django.test import TestCase
from catalogapp import api
from catalogapp import models


class SpecFieldsTest(TestCase):
    def test_create(self):
        api.sections.create("Name", "slug")
        section = api.sections.get(1)

        test_query = {
            "field_type": "BooleanField",
            "name": "Bool Field",
            "slug": "bool_slug",
            "section": section,
            "default_value": True,
            "description": "Some desc",
        }
        result_id = api.specfields.create(**test_query)
        result = api.specfields.get(result_id)
        self.assertEqual(type(result), models.BooleanField)
        del test_query['field_type']
        test_query['default_value'] = str(test_query['default_value'])
        for attr in test_query:
            self.assertEqual(getattr(result, attr), test_query[attr])

    def test_change(self):
        api.sections.create("Name", "slug")
        section = api.sections.get(1)

        test_query = {
            "field_type": "BooleanField",
            "name": "Bool Field",
            "slug": "bool_slug",
            "section": section,
            "default_value": True,
            "description": "Some desc",
        }
        result_id = api.specfields.create(**test_query)

        new_name = "new name"
        new_slug = "new_slug"
        new_default = "False"
        new_desc = "new desc"
        result_id = api.specfields.change(result_id, new_name, new_slug,
                                          new_default, new_desc)

        result = api.specfields.get(result_id)
        self.assertEqual(result.name, new_name)
        self.assertEqual(result.slug, new_slug)
        self.assertEqual(result.default_value, new_default)
        self.assertEqual(result.description, new_desc)