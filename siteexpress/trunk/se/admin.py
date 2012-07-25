# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Globals, Position, QuestAnswer, Image, News, File, SpecialOffer, Feedback, FeedbackFlora, Tag, Pictures
# from utils.colorfield import ColorPickerWidget

class GlobalsAdmin(admin.ModelAdmin):
    list_display = ('prop_name', 'value')

class QuestAnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'question', 'publication_date', 'moderator', 'is_public',)
    # filter_horizontal = ('tags',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('caption', 'announce', 'text', 'date',)
    prepopulated_fields = {'slug': ('caption',) }

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'publication_date')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('article', 'caption')
    filter_horizontal = ('tags',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name',)
    ordering = ('tag',)
    prepopulated_fields = {'name': ('tag',)}


admin.site.register(Globals, GlobalsAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(QuestAnswer, QuestAnswerAdmin)
admin.site.register(Image)
admin.site.register(News, NewsAdmin)
admin.site.register(File)
admin.site.register(SpecialOffer)
admin.site.register(Feedback)
admin.site.register(FeedbackFlora)
admin.site.register(Tag, TagAdmin)
admin.site.register(Pictures)
