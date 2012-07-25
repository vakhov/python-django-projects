# -*- coding: utf8 -*-

"""
Set URL maps for every SectionType here.
Patterns will be applied to "subpaths".

Example: if your path is '/company/news/56/' 
and '/company/news/' is a Section with "news" type,
'56/' will be checked with patterns defined in "news" variable.

"""

from django.conf.urls.defaults import patterns, include, url


index = patterns('',
    url(r'^$', 'common.views.index')
)

text = patterns('',
    url(r'^$', 'common.views.text')
)

catalog = patterns('catalog.views',
    # Стартовая каталога /production/
    url(r'^$', 'index'),
    # Каталог /production/catalog/
    url(r'^(?P<slug>[-a-zA-Z0-9_]+)/(pos-(?P<product>[-a-zA-Z0-9_]+)/)?$', 'catalogue'),
    url(r'^(?P<slug>[-a-zA-Z0-9_]+)/(set-(?P<set>[-a-zA-Z0-9_]+)/)?$', 'catalogue'),
    #Тип /production/catalog/type/
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<type_or_brand>[-a-zA-Z0-9_]+)/(pos-(?P<product>[-a-zA-Z0-9_]+)/)?$', 'type_or_brand'),
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<type_or_brand>[-a-zA-Z0-9_]+)/(set-(?P<set>[-a-zA-Z0-9_]+)/)?$', 'type_or_brand'),
    #Тип+Бренд /production/brand/catalog/type/
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<brand>[-a-zA-Z0-9_]+)/(?P<type>[-a-zA-Z0-9_]+)/(pos-(?P<product>[-a-zA-Z0-9_]+)/)?$', 'brand_type'),
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<brand>[-a-zA-Z0-9_]+)/(?P<type>[-a-zA-Z0-9_]+)/(set-(?P<set>[-a-zA-Z0-9_]+)/)?$', 'brand_type'),
    #Тип+Бренд+Коллекция /production/brand/catalog/type/set/
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<brand>[-a-zA-Z0-9_]+)/(?P<type>[-a-zA-Z0-9_]+)/(set-(?P<set>[-a-zA-Z0-9_]+)/)?$', 'brand_type_set'),
    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<brand>[-a-zA-Z0-9_]+)/(?P<type>[-a-zA-Z0-9_]+)/(set-(?P<set>[-a-zA-Z0-9_]+))/(pos-(?P<product>[-a-zA-Z0-9_]+)/)?$', 'brand_type_set'),
#    # Группа
#    url(r'^groups/(?P<slug>[-a-zA-Z0-9_]+)/$', 'group'),
#    #Позиция
#    url(r'^product/(?P<product>[-a-zA-Z0-9]+)/$', 'product'),
#    # Производитель/тип
#    url(r'^(?P<catalog>[-a-zA-Z0-9_]+)/(?P<grouping_unit>[-a-zA-Z0-9_]+)/$', 'grouping_unit'),
)

qa = patterns('questanswer.views',
    url(r'^$', 'questanswer'),
    url(r'^page-(?P<page>[\d]+)/$', 'questanswer'),
    url(r'^(?P<id>[\d]+)/$', 'question'),
    url(r'^tag/(?P<slug>[-a-zA-Z0-9_]+)/$', 'tag'),
)