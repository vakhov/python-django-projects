from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^chat/$', 'chat.views.login'),
    url(r'^chat/(.*?)/$', 'chat.views.chat'),
    url(r'^meta/$', 'chat.views.meta'),
    
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
    
    # Structure API and admin page
    url(r'^api/structure/admin/$', 'structure.views.admin_page'),
    url(r'^api/structure/list/$', 'structure.views.section_list'),
    url(r'^api/structure/create/$', 'structure.views.create'),
    url(r'^api/structure/rename/$', 'structure.views.rename'),
    url(r'^api/structure/delete/(.*?)/$', 'structure.views.delete'),
    url(r'^api/structure/move/$', 'structure.views.move'),

    url(r'^.*?/$', 'structure.dispatcher.dispatch'),
    url(r'^$', 'structure.dispatcher.dispatch'),
)
