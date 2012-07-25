# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Section, SectionType

class SectionAdmin(admin.ModelAdmin):
    list_display = ('caption', 'path', 'id')
    prepopulated_fields = {'path': ('caption',)}

class SectionTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('caption',)}

admin.site.register(Section, SectionAdmin)
admin.site.register(SectionType, SectionTypeAdmin)
