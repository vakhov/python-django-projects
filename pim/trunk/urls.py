# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pim.views.home', name='home'),
    # url(r'^mario/', include('pim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    
#    url(r'glossarium/', 'catalog.views.glossarium'),
    
    # Login / logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    
    # Aphaline API
    url(r'^api/aphaline/(\w+)/form/(?:(\d+)/){0,1}$', 'aphaline.api.form'),
    url(r'^api/aphaline/(\w+)/change/(?:(\d+)/){0,1}$', 'aphaline.api.change'),
    url(r'^api/aphaline/(\w+)/delete/(\d+)/$', 'aphaline.api.delete'),

    # Widgets API
    url(r'^api/widgets/list/$', 'widgets.views.list'),
    url(r'^api/widgets/create/(.*?)/$', 'widgets.views.create'),
    url(r'^api/widgets/move/(.*?)/$', 'widgets.views.move'),
    url(r'^api/widgets/delete/(.*?)/$', 'widgets.views.delete'),
    url(r'^api/widgets/get/(.*?)/$', 'widgets.views.get'),
    url(r'^api/widgets/form/(.*?)/$', 'widgets.views.form'),
    url(r'^api/widgets/change/(.*?)/$', 'widgets.views.change'),
    
    # Hashing API
    url(r'^api/hashing/links/$', 'seo.views.hashes2links'),
    
    # Structure API and admin page
    url(r'^api/structure/admin/$', 'structure.views.admin_page'),
    url(r'^api/structure/list/$', 'structure.views.section_list'),
    url(r'^api/structure/create/$', 'structure.views.create'),
    url(r'^api/structure/rename/$', 'structure.views.rename'),
    url(r'^api/structure/delete/(.*?)/$', 'structure.views.delete'),
    url(r'^api/structure/move/$', 'structure.views.move'),
    
    # Position move
    url(r'^api/catalog/move/(\d+)/(\d+)/$', 'catalog.views.move_position'),
    
    #WTP
    url(r'^api/wtp/(\d+)/$', 'catalog.views.wtp'),
    url(r'^api/wtp/wtp_catalog/(\d+)/$', 'catalog.views.wtp_catalog'),
    url(r'^api/wtp/add/(\d+)/(\d+)/$', 'catalog.views.wtp_add'),
    url(r'^api/wtp/del/(\d+)/(\d+)/$', 'catalog.views.wtp_del'),
    
    #add, delete or change item collection
    url(r'^api/add_collection/(\d+)/$', 'catalog.views.collection_index'),
    url(r'^api/add_collection/catalog/(\d+)/$', 'catalog.views.collection_catalog'),
    url(r'^api/add_collection/add/(\d+)/(\d+)/$', 'catalog.views.collection_add'),
    url(r'^api/add_collection/del/(\d+)/(\d+)/$', 'catalog.views.collection_del'),
    
    #add, delete or change item action
    url(r'^api/add_action/(\d+)/$', 'catalog.views.action_index'),
    url(r'^api/add_action/catalog/(\d+)/$', 'catalog.views.action_catalog'),
    url(r'^api/add_action/add/(\d+)/(\d+)/$', 'catalog.views.action_add'),
    url(r'^api/add_action/del/(\d+)/(\d+)/$', 'catalog.views.action_del'),

    #Карта сайта
    url(r'^sitemap/$', 'structure.views.sitemap'),
    
    # Basket API
    url(r'^api/basket/add/(\d+)/(\d+)/$', 'catalog.api.add'),
    url(r'^api/basket/change_size/(\d+)/(\d+)/(\d+)/$', 'catalog.api.change_size'),
    url(r'^api/basket/clear/$', 'catalog.api.clear'),
    url(r'^api/basket/delete/(\d+)/(\d+)/$', 'catalog.api.delete'),

    url(r'^basket/$', 'catalog.views.basket_list'),
    
    #filter
    url(r'filter/', 'catalog.views.filter'),
    
    #change_property
    url(r'api/property/', 'catalog.views.change_property'),

    url(r'^.*?/$', 'structure.dispatcher.dispatch'),
    url(r'^$', 'structure.dispatcher.dispatch'),
    
)
