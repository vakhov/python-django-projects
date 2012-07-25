# -*- coding: utf-8 -*-

from catalog.models import Product, Property

from django.db import connection

class CacheTable():
    cursor = connection.cursor()
    table = 'catalog_cache_table'
    PROPERTY_FIELD_TYPE = (
        'varchar(255) DEFAULT NULL',
        'double DEFAULT NULL',
        'tinyint(1) DEFAULT NULL',
    )

    def create_table(self):
        # получаем список свойств
        sql = self.cursor.execute("""
                SELECT slug, type from catalog_property
            """)
        prop = self.cursor.fetchall()

        # формируем строку создания таблицы
        c = ""
        for i in prop:
            a = i[0]
            if i[1] == 1:
                b = self.PROPERTY_FIELD_TYPE[0]
            elif i[1] == 2:
                b = self.PROPERTY_FIELD_TYPE[1]
            elif i[1] == 3:
                b = self.PROPERTY_FIELD_TYPE[2]
            elif i[1] == 4:
                b = self.PROPERTY_FIELD_TYPE[0]
            c += "`%s` %s, " % (a, b)
        c += "PRIMARY KEY (`id`)"

        # выполняем запрос на создание таблицы
        sql = self.cursor.execute("CREATE TABLE `%s` (`id` int(11) NOT NULL AUTO_INCREMENT, `product_id` int(11) NOT NULL, %s) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;" % (self.table, c))

    def fill_table(self):
        # TODO: заполнять таблицу полностью
        # получаем список продуктов
        sql = self.cursor.execute("""
                SELECT id FROM catalog_product
            """)
        prod = self.cursor.fetchall()

        for i in prod:
            sql = self.cursor.execute("INSERT INTO %s (product_id) VALUE (%d);" % (self.table, i[0]))

    def add_property(self, name, type):
        sql = self.cursor.execute("ALTER TABLE %s add `%s` %s;" % (self.table, name, self.PROPERTY_FIELD_TYPE[type]))

    def remove_property(self, name):
        sql = self.cursor.execute("ALTER TABLE %s DROP COLUMN `%s`;" % (self.table, name))

