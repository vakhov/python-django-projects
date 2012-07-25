# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Phone, IconCollection

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone', 'url_part')
    ordering = ('url_part',)
    fields = ('phone', 'url_part')
class IconCollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('caption',)}

admin.site.register(Phone, PhoneAdmin)
admin.site.register(IconCollection, IconCollectionAdmin)
