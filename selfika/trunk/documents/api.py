# -*- coding: utf-8 -*-

import json
import pytils
from django.http import HttpResponse
from utils.decorators import staff_required
from models import Document, Part
from structure.models import SectionType

def _split_join(s):
    b = s.split('-')
    b = '/'.join(b)
    return '/%s/' % b

def ch(node):
    node['data'] = node['caption']
    del node['caption']
    keys = ('id', 'path', 'is_enabled', 'type_id', 'parent_id', 'order', 'zone_id')
    node['attr'] = dict([(x,node[x]) for x in keys])
    for x in keys:
        del node[x]
    node['children'] = node['nodes'].values()
    del node['nodes']
    for child in node['children']:
        ch(child)

@staff_required
def create_document(request):
    document_caption = request.GET.get('caption')
    Document.objects.create(caption=document_caption, 
                            title=document_caption, 
                            owner=request.user)
    
    return HttpResponse('Ok')

@staff_required
def delete_document(request, document_id):
    doc = Document.objects.get(pk=document_id)
    doc.delete()
    return HttpResponse('Ok')

@staff_required
def rename_document(request, document_id):
    doc = Document.objects.get(pk=document_id)
    new_caption = request.POST.get('caption', 'Без имени') 
    doc.caption = new_caption
    return HttpResponse('Ok')

@staff_required
def create_part(request):
    try:
        if not request.POST.get('pid', ''):
            return HttpResponse('You did not specify a parent ID.')
        else:
            parent = Part.objects.get(pk = request.POST['pid'])
    except:
        return HttpResponse('The specified ID # ' + request.POST['pid'] + ' does not exist.', status=400)
    
    document = parent.document
    
    if not request.POST.get('caption', ''):
        return HttpResponse('Name is not specified for the new section.')
    else:
        caption = unicode(request.POST['caption'])
    
    if request.POST.get('slug', ''):
        slug = request.POST['slug']
    else:
        slug = ''
        
    try:
        if request.POST.get('type', ''):
            section_type = SectionType.objects.get(pk = request.POST['type'])
        else:
            section_type = None
    except:
        return HttpResponse('Current type <b>' + request.POST['type'] + '</b> does not exist.', status=400)
    
    document.create_part(parent, caption, slug, section_type)
    return HttpResponse('OK')


@staff_required
def list_parts(request):
    document_id = request.POST.get('document_id', 0)
    document = Document.objects.get(pk=document_id)
    structure = document.get_parts_tree()
    index_page = structure.values().pop()
    ch(index_page)
    result = json.dumps(index_page)
    return HttpResponse(result)

@staff_required
def rename_part(request, section_id):
    try:
        section = Part.objects.get(pk=section_id)
    except:
        return HttpResponse('Section with ID # ' + request.POST['id'] + ' does not exist.')
    
    if not request.POST.get('caption', ''):
        return HttpResponse('Caption is not passed.')
    else:
        caption = request.POST['caption']
    
    if request.POST.get('slug', ''):
        slug = request.POST['slug']
    else:
        try:
            slug = pytils.translit.slugify(caption)
        except:
            return HttpResponse('In the transliteration of the title was an error, try again, or change the title.', status=400)
    
    section.caption = caption
    section.change_slug(slug)
    
    section.save()
    return HttpResponse('OK')
    

@staff_required
def delete_part(request, section_id):
    try:
        section = Part.objects.get(pk=section_id)
        section.delete()
        return HttpResponse('Section number ' + str(section_id) + ' has been deleted.')
    except:
        return HttpResponse('The current section does <u>not exist</u> or it has already been <u>removed</u>.', status=400)
    
@staff_required
def move_part(request):
    try:
        section_to_move = Part.objects.get(pk=request.POST['id'])
        new_parent = Part.objects.get(pk=request.POST['newpid'])
        new_order = request.POST.get('order')
        section_to_move.change_parent(new_parent, new_order)
        return HttpResponse('OK')
    except:
        return HttpResponse('Move failed', status=400)
