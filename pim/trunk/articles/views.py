# -*- coding: utf-8 -*-

from datetime import date
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Article
from utils.shortcuts import paginate

ARTICLES_ON_PAGE = 10

def index(request, page=None):
    context = RequestContext(request)
    paginate(
        context, 'articles', 
        Article.objects.order_by('-date_written'),
        count=ARTICLES_ON_PAGE, page=page, 
        root=request.current_section.path
    )
    return render_to_response('articles/index.html', context)

def section(request, section, page=None):
    context = RequestContext(request)
    paginate(
        context, 'articles', 
        query=context['section'].article_set.all(),
        count=ARTICLES_ON_PAGE, page=page, 
        root=request.current_section.path+section+'/'
    )
    return render_to_response('articles/section.html', context)

def article(request, article, section = None):
    article = get_object_or_404(Article, name=article)
    context = RequestContext(request)
    context['article'] = article
    return render_to_response('articles/article.html', context)
