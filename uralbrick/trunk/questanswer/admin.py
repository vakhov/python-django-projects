# -*- coding: utf-8 -*-

from django.contrib import admin
from models import QuestAnswer, TagName, Alphabet

class QuestAnswerAdmin(admin.ModelAdmin):
    # list_display = ('author', 'date_publication', 'moderator', 'is_public',)
    filter_horizontal = ('tag',)
    # prepopulated_fields = {'slug': ('name',)}
    # pass

admin.site.register(QuestAnswer, QuestAnswerAdmin)
admin.site.register(TagName)
admin.site.register(Alphabet)
