# -*- coding: utf-8 -*-

from datetime import date
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Group, Article, Tag
from utils.shortcuts import paginate
from utils.tree import build_tree

ARTICLES_ON_PAGE = 10

def index(request, page=None):
    context = RequestContext(request)
    # create_widgets_context(context, 'articles_index', 1, 1)
    groups = Group.objects.all().order_by('id').values()
    context['groups'] = build_tree(groups, 'group_id')
    paginate(
        context, 'articles', 
        Article.objects.order_by('-date_written'),
        count=ARTICLES_ON_PAGE, page=page, 
        root=request.current_section.path
    )
    return render_to_response('articles/index.html', context)

def section(request, section, page=None):
    context = RequestContext(request)
    groups = Group.objects.all().order_by('id').values()
    context['groups'] = build_tree(groups, 'group_id')
    context['section'] = get_object_or_404(Group, name=section)
    paginate(
        context, 'articles', 
        query=context['section'].article_set.all(), 
        count=ARTICLES_ON_PAGE, page=page, 
        root=request.current_section.path+section+'/'
    )
    return render_to_response('articles/section.html', context)

def article(request, section, article):
    article = get_object_or_404(Article, name=article)
    context = RequestContext(request)
    groups = Group.objects.all().order_by('id').values()
    context['groups'] = build_tree(groups, 'group_id')
    context['section'] = get_object_or_404(Group, name=section)
    context['article'] = article
    return render_to_response('articles/article.html', context)

def tag(request, tag, page=None):
    context = RequestContext(request)
    groups = Group.objects.all().order_by('id').values()
    context['groups'] = build_tree(groups, 'group_id')
    context['tagview'] = get_object_or_404(Tag, name=tag)
    paginate(
        context, 'articles', 
        query=Article.objects.filter(tags__name__exact=tag).order_by('-date_written'),
        count=ARTICLES_ON_PAGE, page=page, 
        root=request.current_section.path+tag+'/'
    )
    return render_to_response('articles/tag.html', context)
