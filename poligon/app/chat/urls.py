# -*- coding: utf8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('chat.views',
	url(r'^chat/reg/$', 'reg'),
	url(r'^$', 'index'),
)