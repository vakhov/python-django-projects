# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse

from models import TagName

def search(request):
    result = {}
    alphabet = json.loads(request.POST['alphabet'])
    for tag in TagName.objects.all():
        length = tag.name.split()
        if length <= 0:
            pass
        elif length == 1:
            if tag.name[0].lower() == alphabet.lower() and tag.name.lower() != u'для' and tag.name.lower() != u'на':
                name = '|' + tag.name[1:]
                name = {'caption': name, 'path': tag.slug}
                if result.has_key(1):
                    result[1].append(name)
                else:
                    result[1] = [name]
        else:
            words = tag.name.split()
            count = 0
            for word in words:
                count += 1
                if word[0].lower() == alphabet.lower() and word.lower() != u'для' and word.lower() != u'на':
                    if word[0] == alphabet:
                        repl = ' |'
                    else:
                        repl = ' ||'
                    name = ' '.join(tag.name.split()[:count-1]) + repl + word[1:] + ' ' + ' '.join(tag.name.split()[count:])
                    name = {'caption': name, 'path': tag.slug}
                    if result.has_key(count):
                        result[count].append(name)
                    else:
                        result[count] = [name]
    return HttpResponse(json.dumps(result)) 