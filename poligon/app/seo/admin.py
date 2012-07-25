# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Metatag

class MetatagAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description', 'keywords', 'phone', 'image')

admin.site.register(Metatag, MetatagAdmin)