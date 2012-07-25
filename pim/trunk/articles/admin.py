# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('caption',)}

admin.site.register(Article, ArticleAdmin)
