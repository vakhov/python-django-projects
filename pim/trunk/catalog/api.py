# -*- coding: utf-8 -*-

from django.http import HttpResponse
from basket import Basket

def add(request, product_id, size_id=0):
    basket = Basket(request.session)
    new_count = basket.add(product_id, size_id)
    return HttpResponse(str(new_count))

def delete(request, product_id, size_id=0):
    basket = Basket(request.session)
    new_count = basket.delete(product_id, size_id)
    return HttpResponse(str(new_count))

def change_size(request, product_id, old_size_id, new_size_id):
    basket = Basket(request.session)
    basket.change_size(product_id, old_size_id, new_size_id)
    return HttpResponse('OK')

def clear(request):
    basket = Basket(request.session)
    basket.clear()
    return HttpResponse('OK')

