# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Title, ChangeTitle

class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')
    list_filter = ('position',)

admin.site.register(Title, TitleAdmin)
admin.site.register(ChangeTitle)
