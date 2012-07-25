# -*- coding: utf-8 -*-

import re
from models import Hash

class HashingMiddleware:

    link_pattern = re.compile(r"""<a\s*(?:href=['"](.*?)['"]){0,1}(.*?)hashed_link(.*?)>""")
    widget_pattern = re.compile(r"""<div id='hashed-widget-(\d+)'></div>""")

    def process_response(self, request, response):
        try:
            if request.user.is_staff == True:
                return response
            else:
                # Hashing links
                response.content = self.link_pattern.sub(self._hash_link, response.content)
                # Hashing widgets
                response.content = self.widget_pattern.sub(self._hash_widget, response.content)
                return response
        except AttributeError:
            # redirect detected
            return response 

    def _hash_link(self, m):
        link = m.group(1)
        hashed_link = Hash.link2hash(link)
        return '<a href="#"%shash-string="%s"%s>' % (m.group(2), hashed_link, m.group(3))

    def _hash_widget(self, m):
        widget_id = m.group(1)
        hashed_widget = Hash.widget2hash(widget_id)
        return '<div class="hashed-widget" hash-string="%s"></div>' % (hashed_widget,)