# -*- coding: utf-8 -*-

from django import template
from django.db import models
from managers import WidgetManager, WidgetLeafManager
from pixelion.utils.sortable import SortableModel

class Zone(models.Model):
    """
    Zone is the place where widgets could be inserted.
    Don't try to get widgets using "widget_set", because
    it will return instances of "Widget" class.
    Use "Widget.objects.filter(zone=current_zone)" instead.
    """

    def render(self, context=None):
        """ Renders zone (recursively) """
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
    subclasses = {}

    def __unicode__(self):
        return self.type + '#' + str(self.id)

    def save(self, *args, **kwargs):
        # Setting type
        if self.type is None:
            self.type = self.__class__.__name__
        # Saving
        super(Widget, self).save(*args, **kwargs)
    
    def as_leaf_class(self):
        """ Returns derived class instance """
        widget_type = self.type
        if widget_type == 'Widget':
            return self
        else:
            return self.__getattribute__(widget_type.lower())
    
    def render(self, context=None):
        """ Renders widget with its template """
        widget_type = self.type.lower()
        if context is None:
            context = template.Context()
        context.push()
        try:
            # self."widget_type" directs to subclass object
            context['current_widget'] = self.__getattribute__(widget_type)
        except:
            context['current_widget'] = self
        if self.own_template is not None:
            tpl = self.own_template + '.html'
        else:
            tpl = widget_type + '.html'
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
    
    # Patch for SortableModel 
    # (without it, subclasses was used to get order within subclass objects)
    def _get_class(self):
        return Widget
