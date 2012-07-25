# -*- coding: utf-8 -*-

from django.core.urlresolvers import RegexURLResolver
import url_maps

class LameRegexURLResolver(RegexURLResolver):
    def _get_url_patterns(self):
        return self.urlconf_module

def dispatch(request):
    section_type = request.current_section.type.slug
    subpath = request.current_section.subpath
    url_map = url_maps.__dict__[section_type]
    resolver = LameRegexURLResolver('', url_map)
    func, args, kwargs = resolver.resolve(subpath)
    kwargs['request'] = request
    return func(*args, **kwargs)