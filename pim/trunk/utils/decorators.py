from django.http import HttpResponse
from django.template import RequestContext

def staff_required(fn):
    def new(request, *args, **kwargs):
        context = RequestContext(request)
        if not context['user'].is_staff:
            return HttpResponse('Access Denied', status=403)
        return fn(request, *args, **kwargs)
    return new