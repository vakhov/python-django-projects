from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Admin site
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^$', 'common.views.index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),

    # Personal
    url(r'^home/$', 'common.views.home'),

    # Article
    url(r'^articles/(.*?)/$', 'articles.views.article'),

    # Documents
    url(r'^document/(\d+)/$', 'documents.views.root'),
    url(r'^document/(\d+)/structure/$', 'documents.views.structure'),
    url(r'^document/(\d+)/glossary/$', 'documents.views.glossary'),
    url(r'^document/(\d+)/(.*)/$', 'documents.views.part'),

    # Documents API
    url(r'^api/documents/create/$', 'documents.api.create_document'),
    url(r'^api/documents/rename/(\d+)/$', 'documents.api.rename_document'),
    url(r'^api/documents/delete/(\d+)$', 'documents.api.delete_document'),
    
    # Parts API
    url(r'^api/parts/list/$', 'documents.api.list_parts'),
    url(r'^api/parts/create/$', 'documents.api.create_part'),
    url(r'^api/parts/rename/(\d+)/$', 'documents.api.rename_part'),
    url(r'^api/parts/delete/(\d+)/$', 'documents.api.delete_part'),
    url(r'^api/parts/move/$', 'documents.api.move_part'),
    
    # Widgets API
    url(r'^api/widgets/list/$', 'widgets.views.list'),
    url(r'^api/widgets/create/(.*?)/$', 'widgets.views.create'),
    url(r'^api/widgets/move/(.*?)/$', 'widgets.views.move'),
    url(r'^api/widgets/delete/(.*?)/$', 'widgets.views.delete'),
    url(r'^api/widgets/get/(.*?)/$', 'widgets.views.get'),
    url(r'^api/widgets/form/(.*?)/$', 'widgets.views.form'),
    url(r'^api/widgets/change/(.*?)/$', 'widgets.views.change'),

)