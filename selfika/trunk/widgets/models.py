# -*- coding: utf-8 -*-

#import hashlib
#import random

from core import *

from django import template
from django.db import models
from utils.sortable import SortableModel

from aphaline.decorators import aphaline_render_widget, aphaline_render_zone

class Zone(models.Model):
    """
    Zone is the place where widgets could be inserted.
    Don't try to get widgets using "widget_set", because
    it will return instances of "Widget" class.
    Use "Widget.objects.filter(zone=current_zone)" instead.
    """

    @aphaline_render_zone
    def render(self, context=None):
        """ Renders zone (recursively, admin-compatible (?)) """
        result = ''
        widgets = Widget.objects.filter(zone=self)
        if context is None:
            context = template.Context()
        for widget in widgets:
            result += widget.render(context)
        return result

    def __unicode__(self):
        return '#' + str(self.id)

class Widget(SortableModel):
    """
    Widget is a piece of content with own type, template and properties.
    It must be placed into zone.
    """

    zone = models.ForeignKey('Zone', verbose_name="Зона для виджета")
    type = models.CharField("Widget type (lowercase classname)", max_length=255, 
                            null=True, blank=True)
    
    is_hashed = models.BooleanField(default=False)
    is_commentable = models.BooleanField(default=False)

    base_objects = WidgetManager()
    objects = WidgetLeafManager()

    order_isolation_fields = ('zone',)
    own_template = None

    def __unicode__(self):
        return self.type + '#' + str(self.id)

    def save(self, *args, **kwargs):
        # Setting type
        if self.type is None:
            self.type = self.__class__.__name__
        # Saving
        super(Widget, self).save(*args, **kwargs)
    
    def as_leaf_class(self):
        """ Method to return derived class instance """
        widget_type = self.type
        child_class = globals()[widget_type]
        if widget_type == 'Widget':
            return self
        else:
            return child_class.objects.get(pk=self.id)
    
    @aphaline_render_widget
    def render(self, context=None):
        widget_type = self.type.lower()
        if context is None:
            context = template.Context()
        context.push()
        try:
            context['current_widget'] = self.__getattribute__(widget_type)
        except:
            context['current_widget'] = self
        if self.own_template is not None:
            tpl = 'widgets/' + self.own_template + '.html'
        else:
            tpl = 'widgets/' + widget_type + '.html'
        render = template.loader.render_to_string(tpl, context)
        context.pop()
        return render
    
    def move_to_zone(self, zone, order=None):
        """ Moves widget to given zone """
        if zone != self.zone:
            # Setting order of widget to last in old zone
            # for other widgets to rearrange
            self.move(-1)
            # Changing zone and setting new order
            self.zone = zone
            self.order = 0
            self.save()
        if order is not None:
            self.move(order)
        else:
            self.move(-1)
    
    # Patch for ordering (subclasses used to order within subclass objects)
    def _get_class(self):
        return Widget

from set_grid import *
from set_headers import *
from set_text import *
from set_lists import *
# from set_tables import *
from set_media import *
from set_common import *
# from set_upload import *
