# -*- coding: utf-8 -*-

import json
from math import ceil
from itertools import izip_longest
from operator import attrgetter

from django.http import HttpResponse

from models import Catalog

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def search(request):
    result = {}
    alphabet = json.loads(request.POST['alphabet'])
    catalogs = Catalog.objects.all().order_by('name_short')
    for catalog in catalogs:
        length = catalog.name_short.split()
        l = len(length)
        if l <= 0:
            continue
        elif l == 1:
            if catalog.name_short[0].lower() == alphabet.lower() and catalog.name_short.lower() != u'для' and catalog.name_short.lower() != u'на':
                name = '|' + catalog.name_short[1:]
                name = {'caption': name, 'path': catalog.slug}
                if result.has_key(1):
                    result[1].append(name)
                else:
                    result[1] = [name]
        else:
            words = catalog.name_short.split()
            count = 0
            for word in words:
                count += 1
                if word[0].lower() == alphabet.lower() and word.lower() != u'для' and word.lower() != u'на':
                    if word[0] == alphabet:
                        repl = ' |'
                    else:
                        repl = ' ||'
                    name = ' '.join(catalog.name_short.split()[:count-1]) + repl + word[1:] + ' ' + ' '.join(catalog.name_short.split()[count:])
                    name = {'caption': name, 'path': catalog.slug}
                    if result.has_key(count):
                        result[count].append(name)
                    else:
                        result[count] = [name]

    plain_list = []
    for i in result.values():
        plain_list.extend(i)

    rows = int(ceil(float(len(plain_list))/3))

    matrix = grouper(rows, plain_list)
    matrix = list(map(lambda *x:x, *matrix))

    final_result = []
    for i in matrix:
        final_result.extend(i)

    return HttpResponse(json.dumps(final_result))