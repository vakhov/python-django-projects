# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Phone, Banner

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone', 'url_part')
    ordering = ('url_part',)
    fields = ('phone', 'url_part')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('img', 'url_part', 'url')

admin.site.register(Phone, PhoneAdmin)
admin.site.register(Banner, BannerAdmin)