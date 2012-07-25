from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
#from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^admin/filebrowser/', include('filebrowser.urls')),
#    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    
    # Aphaline API
    url(r'^api/aphaline/(\w+)/form/(?:(\d+)/){0,1}$', 'aphaline.api.form'),
    url(r'^api/aphaline/(\w+)/change/(?:(\d+)/){0,1}$', 'aphaline.api.change'),
    url(r'^api/aphaline/(\w+)/delete/(\d+)/$', 'aphaline.api.delete'),
    
    # Login / logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    # Widgets API
    url(r'^api/widgets/list/$', 'widgets.views.list'),
    url(r'^api/widgets/create/(.*?)/$', 'widgets.views.create'),
    url(r'^api/widgets/move/(.*?)/$', 'widgets.views.move'),
    url(r'^api/widgets/delete/(.*?)/$', 'widgets.views.delete'),
    url(r'^api/widgets/get/(.*?)/$', 'widgets.views.get'),
    url(r'^api/widgets/form/(.*?)/$', 'widgets.views.form'),
    url(r'^api/widgets/change/(.*?)/$', 'widgets.views.change'),
    
    # Structure API and admin page
    url(r'^api/structure/admin/$', 'structure.views.admin_page'),
    url(r'^api/structure/list/$', 'structure.views.section_list'),
    url(r'^api/structure/create/$', 'structure.views.create'),
    url(r'^api/structure/rename/$', 'structure.views.rename'),
    url(r'^api/structure/delete/(.*?)/$', 'structure.views.delete'),
    url(r'^api/structure/move/$', 'structure.views.move'),
    
    # Position move
    url(r'^api/catalog/move/(\d+)/(\d+)/$', 'se.views.move_position'),
    
    url(r'^tag/(?P<tag>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'se.views.tag'),
    url(r'^.*?/$', 'structure.dispatcher.dispatch'),
    url(r'^$', 'structure.dispatcher.dispatch'),
)
