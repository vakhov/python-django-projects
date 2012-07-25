# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Client, Site, Domain
from theming import Template, FontTheme, ColorTheme

from utils.colorfield import ColorPickerWidget

admin.site.register(Client)
admin.site.register(Site)
admin.site.register(Domain)
admin.site.register(Template)

class ColorAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'color':
            kwargs['widget'] = ColorPickerWidget
        return super(ColorAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
class FontAdmin(admin.ModelAdmin):
    list_display = ('caption', 'font_theme')

admin.site.register(ColorTheme, ColorAdmin)
admin.site.register(FontTheme, FontAdmin)
