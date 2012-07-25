# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Catalog, Section, Product, Property, Choice, Picture, Pricing, ShoeSize, NewCollection, Choice, Action, ShoeSizeSection
from order import Order
from models import CharPropertyValue, NumericPropertyValue, BooleanPropertyValue, MultipleChoicePropertyValue

class LinkedInline(admin.options.InlineModelAdmin):
    template = "admin/tabular_links.html"
    admin_model_path = None

    def __init__(self, *args, **kwargs):
        super(LinkedInline, self).__init__(*args, **kwargs)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()

class CharPVInline(admin.TabularInline):
    model = CharPropertyValue

class NumericPVInline(admin.TabularInline):
    model = NumericPropertyValue

class BooleanPVInline(admin.TabularInline):
    model = BooleanPropertyValue

class MultipleChoicePVInline(admin.TabularInline):
    model = MultipleChoicePropertyValue
    
class PictureInline(admin.TabularInline):
    model = Picture
    extra = 5

class ProductInline(LinkedInline):
    model = Product
    fields = ( 'name', 'slug', 'article', 'price', 'is_exist', 'is_enabled' )

class ChoiceInline(admin.TabularInline):
    model = Choice

class PricingInline(admin.TabularInline):
    model = Pricing
    extra = 15

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('section', )
    filter_horizontal = ('properties',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('caption', 'path', )
    inlines = [ ProductInline, ]
    ordering = ('order', 'path')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article', 'price')
    list_editable = ('slug', 'article', 'price')
    list_filter = ('section__path', )
    ordering = ('order',)
    inlines = [ PricingInline, PictureInline, CharPVInline, NumericPVInline, BooleanPVInline, MultipleChoicePVInline ]
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('wtp',)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug', 'default', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ ChoiceInline, ]
    
class NewCollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ShoeSizeSectionAdmin(admin.ModelAdmin):
    filter_horizontal = ('sizes',)
    pass

admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(ShoeSize)
admin.site.register(NewCollection, NewCollectionAdmin)
admin.site.register(Order)
admin.site.register(Choice)
admin.site.register(Action)
admin.site.register(ShoeSizeSection, ShoeSizeSectionAdmin)