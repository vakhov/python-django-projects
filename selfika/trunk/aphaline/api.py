# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.forms import ModelForm
from django.db.models import Model

# from utils.decorators import staff_required

from se.models import *

# @staff_required
def delete(request, model, id):
    model_class = globals()[model]
    if not issubclass(model_class, Model):
        return HttpResponse('Invalid model', status=400)
    
    model_class.objects.get(pk=id).delete()
    return HttpResponse('Ok')

# @staff_required
def form(request, model, id=None):

    model_class = globals()[model]
    if not issubclass(model_class, Model):
        return HttpResponse('Invalid model', status=400)

    class AutoForm(ModelForm):
        class Meta:
            model = model_class
            # exclude = ('zone', 'order', 'type', 'is_hashed', 'is_commentable')
    
    if id is not None:    
        item = model_class.objects.get(pk=id)
        form = AutoForm(instance=item)
    else:
        id = ''
        form = AutoForm()
    
    path = request.GET.get('path', '')
    
    result = """
        <form method="post" enctype="multipart/form-data" 
              action="/api/aphaline/%s/change/%s/">
            <table>
                %s
                <tr>
                    <td colspan="2" style="text-align: center">
                        <input type="hidden" name="current_section" value="%s" />
                        <input type="submit" name="submit_legacy" value="%s" />
                    </td>
                </tr>
            </table>
        </form>
    """ % (model, str(id), form.as_table(), path, u"Сохранить")
    
    return HttpResponse(result)

# @staff_required
def change(request, model, id=None):
    model_class = globals()[model]
    if not issubclass(model_class, Model):
        return HttpResponse('Invalid model', status=400)

    class AutoForm(ModelForm):
        class Meta:
            model = model_class
            # exclude = ('zone', 'order', 'type', 'is_hashed', 'is_commentable')
    
    if id is not None:    
        item = model_class.objects.get(pk=id)
        form = AutoForm(request.POST, request.FILES, instance=item)
    else:
        form = AutoForm(request.POST, request.FILES)

    form.save()

    return HttpResponse('Ok')
