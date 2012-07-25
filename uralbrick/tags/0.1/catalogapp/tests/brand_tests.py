# -*- coding: utf-8 -*-

from django.test import TestCase
from catalogapp import api

class TestBrands(TestCase):
    def test_create(self):
        brand_id = api.brands.create("Brand name", "brand_slug")

        self.assertTrue(isinstance(brand_id, int))

    def test_delete(self):
        brand1_id = api.brands.create("Brand name", "brand_slug")
        brand2_id = api.brands.create("Brand name", "brand_slug")

        self.assertTrue(api.brands.delete(brand1_id))
        self.assertEqual(api.brands.Brand.objects.count(), 1)
        self.assertFalse(api.brands.delete(brand1_id))

    def test_rename(self):
        brand_id = api.brands.create("Brand name", "brand_slug")

        self.assertTrue(api.brands.rename(brand_id, "New name"))

        brand = api.brands.get(brand_id)
        self.assertEqual(brand.name, "New name")
        self.assertEqual(brand.slug, "brand_slug")

        self.assertTrue(api.brands.rename(brand_id, "New name", "new_slug"))

        brand = api.brands.get(brand_id)
        self.assertEqual(brand.name, "New name")
        self.assertEqual(brand.slug, "new_slug")

    def test_list(self):
        brand1_id = api.brands.create("Brand name", "brand_slug")
        brand2_id = api.brands.create("Brand name", "brand_slug")
        brand3_id = api.brands.create("Other name", "brand_slug")

        brands = api.brands.list(name="Brand name")
        self.assertEqual(len(brands), 2)

        self.assertTrue(brand1_id in [b.id for b in brands])
        self.assertTrue(brand2_id in [b.id for b in brands])
        self.assertFalse(brand3_id in [b.id for b in brands])

    def test_listIn(self):
        brand1_id = api.brands.create("Brand name", "brand_slug")
        brand2_id = api.brands.create("Brand name", "brand_slug")
        brand3_id = api.brands.create("Other name", "brand_slug")
        
        brands = api.brands.listIn([brand2_id, brand3_id])

        self.assertEqual(len(brands), 2)
