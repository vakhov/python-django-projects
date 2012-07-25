# -*- coding: utf-8 -*-

from models import Product, Catalog, Section, Pricing, ShoeSize 

from django.db.models import Max, Min

def filter(request):
    cs = request.current_section
    non_sized_prices = Product.objects.filter(section__path__startswith=cs.path).aggregate(Min("price"), Max("price"))
    sized_prices = Pricing.objects.filter(product__section__path__startswith=cs.path).aggregate(Min("price"), Max("price"))
    sizes = ShoeSize.objects.filter(pricing__product__section__path__startswith=cs.path).distinct()
    
    if non_sized_prices['price__max'] > sized_prices['price__max']:
        price_max = non_sized_prices['price__max']
    else:
        price_max = sized_prices['price__max']
        
    if non_sized_prices['price__min'] > sized_prices['price__min']:
        price_min = non_sized_prices['price__min']
    else:
        price_min = sized_prices['price__min']

    if not price_min: price_min = 0
    if not price_max: price_max = 0
    if not sizes: sizes = None
    
    return {'filter': {'price_max': int(price_max), 'price_min': int(price_min), 'size': sizes }}

def nova(request):
    products = Product.objects.all().order_by('-date')
    for product in products:
        if product.nova():
            return {'nova': True}
    return {}