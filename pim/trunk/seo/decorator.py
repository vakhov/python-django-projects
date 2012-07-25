# -*- coding: utf8 -*-

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

def change_page_settings(fn):
    def new(request, *args, **kwargs):
        context = RequestContext(request)
        if request.session.get('time_session') is None:
            return HttpResponse('Access Denied<br /><a href="../">Войти</a>', status=403)
        return fn(request, *args, **kwargs)
    return new