# -*- coding: utf-8 -*-

import json
import pytils
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from utils.decorators import staff_required
from models import Section, SectionType

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
def create(request):
    try:
        if not request.POST.get('pid', ''):
            return HttpResponse('You did not specify a parent ID.')
        else:
            parent = Section.objects.get(pk = request.POST['pid'])
    except:
        return HttpResponse('The specified ID # ' + request.POST['pid'] + ' does not exist.', status=400)
    
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
    
    Section.create_section(parent, caption, slug, section_type)
    return HttpResponse('OK')


@staff_required
def section_list(request):
    structure = Section.get_structure()
    index_page = structure[1]
    ch(index_page)
    result = json.dumps(index_page)
    return HttpResponse(result)


@staff_required
def admin_page(request):
    context = RequestContext(request)
    return render_to_response('admin/list.html', context)


@staff_required
def rename(request):
    try:
        section = Section.objects.get(pk = request.POST['id'])
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
def delete(request, section_id):
    try:
        section = Section.objects.get(pk=section_id)
        section.delete()
        return HttpResponse('Section number ' + str(section_id) + ' has been deleted.')
    except:
        return HttpResponse('The current section does <u>not exist</u> or it has already been <u>removed</u>.', status=400)
    
@staff_required
def move(request):
    try:
        section_to_move = Section.objects.get(pk=request.POST['id'])
        new_parent = Section.objects.get(pk=request.POST['newpid'])
        new_order = request.POST.get('order')
        section_to_move.change_parent(new_parent, new_order)
        return HttpResponse('OK')
    except:
        return HttpResponse('Move failed', status=400)
