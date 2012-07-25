# -*- coding: utf8 -*-

from django.contrib import admin

from models import Catalog, Manufacturer, Type, Product, Picture

class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	filter_horizontal = ('types', 'picture')

admin.site.register(Catalog)
admin.site.register(Manufacturer)
admin.site.register(Type)
admin.site.register(Product, ProductAdmin)
admin.site.register(Picture)
