# -*- coding: utf-8 -*-

from seo.models import Metatag
from common.models import Phone, Banner, Footer
from catalog.basket import Basket
from structure.models import *

def _split_join(s):
    c = []
    b = s.split('/')[1:-1]
    i = 0
    path = '/'
    while i < len(b):
        path += b[i]+'/'
        section = Section.objects.get(path=path)
        c.append({'caption': section.caption, 'path': path}) 
        i +=1
    return c

def seo_tags(request):
    try:
        return { 'metatag': Metatag.objects.get(name=request.path) }
    except:
        return {}

def phone(request):
    try:
        phone = Phone.objects.extra(
            where=["url_part=(SELECT max(url_part) from common_phone WHERE locate(url_part, %s)=1)"], 
            params=[request.path]
        )[0]
        return {'phone':phone}
    except:
        return {'phone':''}

def banner(request):
    try:
        banner = Banner.objects.extra(
            where=["url_part=(SELECT max(url_part) from common_banner WHERE locate(url_part, %s)=1)"], 
            params=[request.path]
        )
        return {'banner':banner}
    except:
        return {'banner':''}

def current_section(request):
    return { 'current_section': request.current_section }

def current_path(request):
    return { 'current_path': request.path }

def structure(request):
    return { 'structure': request.structure }

def footer(request):
    return {'footer': Footer.objects.get(pk=1)}

def crumbs(request):
    return {'crumbs': _split_join(str(request.current_section))}

def basket_summary_info(request):
    basket = Basket(request.session)
    return basket.get_summary_info()

def main_links(request):
    return {'main_links':
                {
                'table_size'        :   Section.objects.get(pk=44),
                'payment'           :   Section.objects.get(pk=45),
                'contacts'          :   Section.objects.get(pk=46),
                'news_and_articles' :   Section.objects.get(pk=47),
                'q_and_a'           :   Section.objects.get(pk=48),
                'action'            :   Section.objects.get(pk=49),
                'glossarium'        :   Section.objects.get(pk=155),
                'nova'        :   Section.objects.get(pk=157)
                }
            }
