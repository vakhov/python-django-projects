# -*- coding: utf-8 -*-

from django.http import HttpResponse
from models import Article

def article(request, slug):
    return HttpResponse('Article ' + slug)