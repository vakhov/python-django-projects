# -*- coding: utf-8 -*-

import re
from models import Hash

class HashingMiddleware:
    link_pattern = re.compile(r"""<a\s*(?P<attr1>.*?)hashed_link=""(?P<attr2>.*?)\s*(?:href=['"](?P<url>.*?)['"]){0,1}(?P<attr3>.*?)>""")
    
    def process_response(self, request, response):
        try:
            if request.user.is_staff == True:
                return response
            else:
                # Hashing links
                response.content = self.link_pattern.sub(self._hash_link, response.content)
                return response
        except AttributeError:
            # redirect detected
            return response 
    
    def _hash_link(self, m):
        link = m.group('url')
        hashed_link = Hash.link2hash(link)
        return '<a href="#" hash-string="{0}" {1} {2} {3}>'.format(hashed_link, m.group('attr1'), m.group('attr2'), m.group('attr3'))