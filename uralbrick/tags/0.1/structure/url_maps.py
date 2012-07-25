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
    url(r'^$', 'common.views.index')
)

text = patterns('',
    url(r'^$', 'common.views.text')
)

articles = patterns('articles.views',
    url(r'^(page-(?P<page>\d+)/){0,1}$', 'index'),
    url(r'^tag/(?P<tag>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'tag'),
    url(r'^(?P<section>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'section'),
    url(r'^(?P<section>[-_a-zA-Z0-9.]+)/(?P<article>[-_a-zA-Z0-9.]+)/$', 'article'),
)

production = patterns('catalogapp.views',
    url(r'^$', 'index'),
    url(r'^(?P<section>[-_a-zA-Z0-9.]+)/$', 'section'),    
)
