# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import json

from models import TestText

def index(request):
    context = RequestContext(request)
    context['sample'] = TestText.objects.all().order_by('?')[0]
    return render_to_response('livesearch/index.html', context)

@csrf_exempt
def livesearch(request):
#    try:
        translation = {}
        context = RequestContext(request)
        results = TestText.objects.filter(text__icontains=request.POST['search'])
        for result in results:
            translation[result.id] = {
                            'perevod': result.perevod,
                            'text': result.text,
                        }
        return HttpResponse(json.dumps(translation))
#    except:
#        return HttpResponse(json.dumps({}))