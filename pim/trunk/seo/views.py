# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from models import Hash

def hashes2links(request):
    if request.raw_post_data:
        hashes = json.loads(request.raw_post_data)
        result = {}
        for h in hashes:
            result[h] = Hash.hash2link(h)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps({}))