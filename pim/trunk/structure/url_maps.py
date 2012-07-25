# -*- coding: utf-8 -*-

"""
Set URL maps for every SectionType here.
Patterns will be applied to "subpaths".

Example: if your path is '/company/news/56/' 
and '/company/news/' is a Section with "news" type,
'56/' will be checked with patterns defined in "news" variable.

"""

from django.conf.urls.defaults import patterns, include, url


index = patterns('',
    url(r'^$', 'catalog.views.index')
)

collections = patterns('catalog.views',
    url(r'^$', 'collections_list'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'collections_list'),
    url(r'^(?P<slug>.*?)/(page-(?P<page>\d+)){0,1}/$', 'collections_item'),
    url(r'^(?P<slug>.*?)/$', 'collections_item'),
)

specials = patterns('catalog.views',
    url(r'^$', 'action_list'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'action_list'),
    url(r'^(?P<slug>.*?)/(page-(?P<page>\d+)){0,1}/$', 'action_item'),
    url(r'^(?P<slug>.*?)/$', 'action_item'),
)

catalog = patterns('catalog.views',
    url(r'^$', 'catalog_list'),
    url(r'^all/$', 'catalog_all'),
    url(r'^shuffle/$', 'catalog_shuffle'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'catalog_list'),
    url(r'^(?P<slug>.*?)/$', 'catalog_item'),
)

text = patterns('',
    url(r'^$', 'common.views.text')
)

qa = patterns('questanswer.views',
    url(r'^$', 'questanswer'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'questanswer'),
)

articles = patterns('articles.views',
    url(r'^(page-(?P<page>\d+)/){0,1}$', 'index'),
    url(r'^tag/(?P<tag>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'tag'),
    url(r'^(?P<article>[-_a-zA-Z0-9.]+)/$', 'article'),
    url(r'^(?P<section>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'section'),
    url(r'^(?P<section>[-_a-zA-Z0-9.]+)/(?P<article>[-_a-zA-Z0-9.]+)/$', 'article'),
)

glossarium = patterns('catalog.views',
    url(r'^$', 'glossarium'),
)

novinki = patterns('catalog.views',
    url(r'^$', 'nova')
)
