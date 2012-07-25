# -*- coding: utf-8 -*-

from django.conf import settings
from models import Widget, Zone

def widgets_list():
    """
    Returns widget groups and clases list
    """
    try:
        return settings.WIDGETS
    except:
        return {}


def create_widget(widget_type, zone_id, order=None):
    """
    Creates widget in given zone with given order
    
    @param widget_type: Widget type (class name)
    @param zone_id: Zone ID
    @param order: Order (or None for last position)
    """
    widget_class = Widget.subclasses[widget_type]
    zone = Zone.objects.get(pk=zone_id)
    widget = widget_class.objects.create(zone=zone)
    if order is not None:
        widget.move(int(order))
        
def delete_widget(widget_id):
    """
    Deletes widget with its subclasses data
    
    @param widget_id: Widget ID
    """
    widget = Widget.objects.filter(pk=widget_id)[0]
    widget.delete()

def move_widget(widget_id, order=None, zone_id=None):
    """
    Moves widget to given order and/or zone
    
    @param widget_id: Widget ID
    @param order: Order (or -1 for last position)
    @param zone_id: Zone ID 
    """
    widget = Widget.objects.get(pk=widget_id)
    if zone_id is None:
        zone = widget.zone
    else:
        zone = Zone.objects.get(pk=zone_id)
    widget.move_to_zone(zone, order)

def get_widget_as_dict(widget_id):
    """
    Returns widget data as dictionary
    
    @param widget_id: Widget ID
    """
    widget = Widget.objects.get(pk=widget_id).as_leaf_class()
    dict_widget = widget.__dict__
    del dict_widget['_state']
    return dict_widget
