# -*- coding: utf-8 -*-

from django.contrib import admin
from models import QuestAnswer

class QuestAnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_publication', 'moderator', 'is_public',)

admin.site.register(QuestAnswer, QuestAnswerAdmin)
