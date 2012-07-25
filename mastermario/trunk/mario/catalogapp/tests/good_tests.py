# -*- coding: utf-8 -*-

from django.test import TestCase
from catalogapp import api
from django.core.exceptions import ValidationError


class TestGoods(TestCase):
    good_valid_attrs = {"name": "name", "section_id": 1, "articul": "articul"}
    good_valid_initial = {"slug": "slug", "price_in": 1, "price_out": 2,
                          "shortdesc": 'desc', "label": "label"}
    def test_add(self):
        sps_array = [{
            "field_type": "BooleanField",
            "name": "boolfield",
            "slug": "bool_slug",
            "default_value": True,
            "description": "Some desc",
        },
        {
            "field_type": "CharField",
            "name": "charfield",
            "slug": "char_slug",
            "default_value": "some string",
            "description": "Some desc",
        },]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        initial = {"slug": "slug", "price_in": 1, "price_out": 2,
                   "boolfield": False, "charfield": "xxx"}
        good_id = api.goods.create(name="name", section_id=1, initial=initial)
        
        self.assertTrue(isinstance(good_id, unicode))

    def test_get(self):
        sps_array = [{
            "field_type": "BooleanField",
            "name": "boolfield",
            "slug": "bool_slug",
            "default_value": True,
            "description": "Some desc",
        },
        {
            "field_type": "CharField",
            "name": "charfield",
            "slug": "char_slug",
            "default_value": "some string",
            "description": "Some desc",
        },]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)
    
        initial = {"slug": "slug", "price_in": 1, "price_out": 2,
                   "boolfield": False, "charfield": "xxx"}
        good_id = api.goods.create(name="name", section_id=1, initial=initial)

        good = api.goods.get(id=good_id)

        self.assertEqual(good.name, "name")

    def test_delete(self):
         initial = {"slug": "slug", "price_in": 1, "price_out": 2,
                    "boolfield": False, "charfield": "xxx"}
         good_id = api.goods.create(name="name", section_id=1, initial=initial)
         api.goods.delete(good_id)
         self.assertEqual(api.goods.Good.objects.count(), 0)

    def test_boolean(self):
        sps_array = [{
            "field_type": "BooleanField",
            "name": "boolfield",
            "slug": "bool_slug",
            "default_value": True,
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        # Тестируем верное значение True
        initial = self.good_valid_initial.copy()
        initial['boolfield'] = True

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем верное значение False
        initial = self.good_valid_initial.copy()
        initial['boolfield'] = False

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем не верное значение "wrong"
        initial = self.good_valid_initial.copy()
        initial['boolfield'] = "wrong"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        self.assertRaises(ValidationError, api.goods.create, **create_attr)

    def test_charfield(self):
        sps_array = [{
            "field_type": "CharField",
            "name": "charfield",
            "slug": "char_slug",
            "default_value": "",
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)
        

        # Тестируем верное значение "test"
        initial = self.good_valid_initial.copy()
        initial['charfield'] = "test"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

    def test_integer(self):
        sps_array = [{
            "field_type": "IntegerField",
            "name": "integerfield",
            "slug": "integer_slug",
            "default_value": 0,
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        # Тестируем верное значение 5
        initial = self.good_valid_initial.copy()
        initial['integerfield'] = 5

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем не верное значение "wrong"
        initial = self.good_valid_initial.copy()
        initial['integerfield'] = "wrong"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        self.assertRaises(ValidationError, api.goods.create, **create_attr)

    def test_textfield(self):
        sps_array = [{
            "field_type": "TextField",
            "name": "textfield",
            "slug": "text_slug",
            "default_value": "",
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        # Тестируем верное значение "test"
        initial = self.good_valid_initial.copy()
        initial['textfield'] = "test"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

    def test_choicefield(self):
        sps_array = [{
            "field_type": "ChoiceField",
            "name": "choicefield",
            "slug": "choice_slug",
            "choices": [(1, 'Choice 1'), (2, 'Choice 2')],
            "default_value": "",
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        # Тестируем верное значение 1
        initial = self.good_valid_initial.copy()
        initial['choicefield'] = 1

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем не верное значение 3
        initial = self.good_valid_initial.copy()
        initial['choicefield'] = 3

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        self.assertRaises(ValidationError, api.goods.create, **create_attr)

    def test_multiplechoicefield(self):
        sps_array = [{
            "field_type": "MultipleChoiceField",
            "name": "mchoicefield",
            "slug": "mchoice_slug",
            "choices": [(1, 'Choice 1'), (2, 'Choice 2')],
            "default_value": "",
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        # Тестируем верное значение 1
        initial = self.good_valid_initial.copy()
        initial['mchoicefield'] = 1

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем верное значение [1, 2]
        initial = self.good_valid_initial.copy()
        initial['mchoicefield'] = "1,2"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        good = api.goods.create(**create_attr)

        # Тестируем не верное значение 3
        initial = self.good_valid_initial.copy()
        initial['mchoicefield'] = 3

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        self.assertRaises(ValidationError, api.goods.create, **create_attr)

        # Тестируем не верное значение [1, 3]
        initial = self.good_valid_initial.copy()
        initial['mchoicefield'] = "1,3"

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = initial

        self.assertRaises(ValidationError, api.goods.create, **create_attr)

    def test_default_value(self):
        sps_array = [{
            "field_type": "CharField",
            "name": "charfield",
            "slug": "char_slug",
            "default_value": "default",
            "description": "Some desc",
        }]
        section_id = api.sections.create("Name", "slug")
        api.sections.addFields(section_id, sps_array)

        create_attr = self.good_valid_attrs.copy()
        create_attr['initial'] = self.good_valid_initial

        good_id = api.goods.create(**create_attr)
        good = api.goods.get(good_id)

        self.assertEqual(good.charfield, "default")

    def tearDown(self):
        # В отличие от sqlite3 (не знаю про другие базы), монга не чистит после каждого теста
        # Сделаем чтобы прибирала за собой
        api.goods.Good.objects.all().delete()