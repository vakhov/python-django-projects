# -*- coding: utf8 -*-

from models import TextOnPage

def textonpage(request):
    try:
        return {'textonpage': TextOnPage.objects.get(url=request.path)}
    except:
        return {}