# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Article, Group, Tag

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name',)
    ordering = ('tag',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Group)
admin.site.register(Tag, TagAdmin)
