# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

index = patterns('se.views',
    url(r'^$', 'index'),
)

text = patterns('se.views',
    url(r'^$', 'text'),
)

qa = patterns('se.views',
    url(r'^$', 'questanswer'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'questanswer'),
)

feedback = patterns('se.views',
    url(r'^$', 'feedbackflora'),
    url(r'^(page-(?P<page>\d+)){0,1}/$', 'feedbackflora'),
)

news = patterns('se.views',
    url(r'^$', 'news'),
    url(r'^(page-(?P<page>\d+)/){0,1}$', 'news'),
    url(r'^(item-(?P<item_news>\d+)){0,1}/$', 'news'),
    url(r'^(?P<slug>[-_a-zA-Z0-9.]+)/$', 'news'),
)

article = patterns('se.views',
    url(r'^$', 'article'),
    url(r'^(page-(?P<page>\d+)/){0,1}$', 'article'),
    url(r'^(item-(?P<item_news>\d+)){0,1}/$', 'article'),
    url(r'^(?P<slug>[-_a-zA-Z0-9.]+)/$', 'article'),
)

catalog = patterns('se.views',
    url(r'^(?:page-(?P<page>\d+)/){0,1}$', 'catalog_list'),
    url(r'^(?:item-(?P<position_id>\d+))/$', 'catalog_item'),
    url(r'^all/$', 'catalog_all'),
#    url(r'^tag/(?P<tag>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'tag'),
#    url(r'^add_to_basket/(?P<position_id>\d+)/$', 'add_to_basket'),
#    url(r'^del_from_basket/(?P<position_id>\d+)/$', 'del_from_basket'),
)

form = patterns('se.views',
    url(r'^$', 'form'),
    url(r'^rem/$', 'rem_from_basket'),
    url(r'^(item-(?P<position_id>\d+))/add/(?P<redirect>\w+)/$', 'add_to_basket'),
    url(r'^(item-(?P<position_id>\d+))/del/(?P<redirect>\w+)/$', 'del_from_basket'),
)
