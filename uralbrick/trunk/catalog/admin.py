# -*- coding: utf8 -*-

from django.contrib import admin

from models import Catalog, Manufacturer, TypeA, TypeB, Product, Picture, Group, Alphabet, Set, SetGroup, CatalogBrandType

class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	filter_horizontal = ('types', 'picture', 'type_b')

class CatalogAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name_short',)}

class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class GroupingUnitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SetAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
#	filter_horizontal = ('product', )

class SetGroupAdmin(admin.ModelAdmin):
#	filter_horizontal = ('product',)
	pass

admin.site.register(Group, GroupAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Manufacturer, GroupingUnitAdmin)
admin.site.register(TypeA, GroupingUnitAdmin)
admin.site.register(TypeB, GroupingUnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Picture)
admin.site.register(Alphabet)
admin.site.register(Set, SetAdmin)
admin.site.register(SetGroup, SetGroupAdmin)
admin.site.register(CatalogBrandType)