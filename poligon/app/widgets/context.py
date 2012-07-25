# -*- coding: utf-8 -*-

from brick.widgets.models import *

def create_widgets_context(context, zone_type, zone_pid, zones_count=0):

    context['widgets'] = {}

    for i in xrange(zones_count):
        widgets = Widget.objects.filter(
            zone_type=zone_type,
            zone_primary_id=zone_pid,
            zone_secondary_id=i+1
        )
        context['widgets'][(zone_type, zone_pid, i+1)] = widgets
        for widget in widgets:
            subs_recursive(widget, context['widgets'], zone_type, zone_pid)

    return context


def subs_recursive(widget, result, zone_type, zone_pid):
    subs = widget.subs()
    if subs:
        zone_type = widget.sub_zones_type
        zone_pid = widget.id
        for i in subs:
            widgets = subs[i]
            result[(zone_type, zone_pid, i)] = widgets
            for widget in widgets:
                subs_recursive(widget, result, zone_type, zone_pid)
