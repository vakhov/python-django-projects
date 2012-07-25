# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms import ModelForm

from utils.decorators import staff_required

from models import *

@staff_required
def create(request, widget_type):
    try:
        widget_class = globals()[widget_type]
    except KeyError:
        return HttpResponse('Invalid widget type', status=400)

    if not issubclass(widget_class, Widget):
        return HttpResponse('Invalid widget type', status=400)

    if request.GET.get('zone_id', None) is None:
        return HttpResponse('Zone ID is required', status=400)

    try:
        zone = Zone.objects.get(pk=request.GET.get('zone_id'))
    except DoesNotExist:
        return HttpResponse('Zone with given ID is not exist', status=400)

    widget = widget_class(zone=zone)
    widget.save()

    order = request.GET.get('order', None)
    if order is not None:
        widget.move(int(order))

    context = RequestContext(request)
    return HttpResponse(widget.render(context))

@staff_required
def delete(request, id):
    try:
        widget = Widget.objects.filter(pk=id)[0]
        widget.delete()
        widget = Widget.objects.get(pk=id)
        widget.delete()
        return HttpResponse("Widget #" + str(id) + " is deleted")
    except:
        return HttpResponse("No such widget")

@staff_required  
def move(request, id):
    try:
        widget = Widget.objects.get(pk=id)
        order = request.GET.get('order', None)
        zone = Zone.objects.get(pk=request.GET['zone_id'])
        widget.move_to_zone(zone, order)
        return HttpResponse("Okay")
    except:
        return HttpResponse("Error", 500)

@staff_required    
def list(request):
    from grouping import get_groups
    data = get_groups()
    data = json.dumps(data)
    return HttpResponse(data)

@staff_required
def get(request, id):
    try:
        widget = Widget.objects.get(pk=id).as_leaf_class()
    except:
        return HttpResponse("No such widget")
    
    context = RequestContext(request)
    return HttpResponse(widget.render(context))

@staff_required
def form(request, id):
    try:
        widget = Widget.objects.get(pk=id).as_leaf_class()
    except:
        return HttpResponse("No such widget")

    class WidgetForm(ModelForm):
        class Meta:
            model = widget.__class__
            exclude = ('zone', 'order', 'type')
    
    path = request.GET.get('path', '')
    form = WidgetForm(instance=widget)
    result = """
        <form method="post" enctype="multipart/form-data" 
              action="/api/widgets/change/%s/">
            <table>
                %s
                <tr>
                    <td colspan="2" style="text-align: center">
                        <input type="hidden" name="current_section" value="%s" />
                        <input type="submit" name="submit_widget_form" value="Save" />
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <input type="button" name="submit_and_add_widget" 
                               value="Save and add another" />
                    </td>
                </tr>
            </table>
        </form>
    """ % (str(id), form.as_table(), path)

    return HttpResponse(result)

@staff_required
def change(request, id):
    try:
        widget = Widget.objects.get(pk=id).as_leaf_class()
    except:
        return HttpResponse("No such widget")

    class WidgetForm(ModelForm):
        class Meta:
            model = widget.__class__
            exclude = ('zone', 'order', 'type')
    
    form = WidgetForm(request.POST, request.FILES, instance=widget)
    form.save()

    context = RequestContext(request)
    return HttpResponse(widget.render(context))
