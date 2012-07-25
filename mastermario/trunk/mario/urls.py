from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import Sitemap, GenericSitemap, FlatPageSitemap
from articles.models import Article
from structure.models import Section

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

generic_sitemaps = {
    'generic': GenericSitemap({
        'queryset': Article.objects.all()
    }, priority=0.6)
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mario.views.home', name='home'),
    # url(r'^mario/', include('mario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': generic_sitemaps}),
    url(r'^admin/', include(admin.site.urls)),

    # Login / logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    
    # Aphaline API
    url(r'^api/aphaline/(\w+)/form/(?:(\d+)/){0,1}$', 'aphaline.api.form'),
    url(r'^api/aphaline/(\w+)/change/(?:(\d+)/){0,1}$', 'aphaline.api.change'),
    url(r'^api/aphaline/(\w+)/delete/(\d+)/$', 'aphaline.api.delete'),

    # Hashing API
    url(r'^api/hashing/links/$', 'seo.views.hashes2links'),
    url(r'^api/hashing/widgets/$', 'seo.views.hashes2widgets'),

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

    # # Articles page
    # url(r'^articles/(page-(?P<page>\d+)/){0,1}$', 'mario.articles.views.index'),
    # url(r'^articles/tag/(?P<tag>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'mario.articles.views.tag'),
    # url(r'^articles/(?P<section>[-_a-zA-Z0-9.]+)/(page-(?P<page>\d+)/){0,1}$', 'mario.articles.views.section'),
    # url(r'^articles/(?P<section>[-_a-zA-Z0-9.]+)/(?P<article>[-_a-zA-Z0-9.]+)/$', 'mario.articles.views.article'),

    # # Catalog pages
    # url(r'^catalog/$', 'mario.catalogapp.views.index'),
    # url(r'^catalog/(?P<section>[-_a-zA-Z0-9.]+)/$', 'mario.catalogapp.views.section'),

    # Any page
    # url(r'^.*/$', 'common.views.index'),

    url(r'^.*?/$', 'structure.dispatcher.dispatch'),
    url(r'^$', 'structure.dispatcher.dispatch'),
    
)
