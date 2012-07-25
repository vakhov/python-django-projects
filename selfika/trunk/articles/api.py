# -*- coding: utf-8 -*-

from django.http import HttpResponse
from models import Article

def article_create(request):
    return HttpResponse('Creating article')

def article_edit(request, id):
    return HttpResponse('Editing article')

def article_delete(request, id):
    return HttpResponse('Deleting article')
