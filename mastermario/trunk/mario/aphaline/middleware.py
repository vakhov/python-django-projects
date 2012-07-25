# -*- coding: utf-8 -*-

import re

class AphalineMiddleware:

    aph_pattern = re.compile(r"""aph-[-_a-zA-Z]+=['"](.*?)['"]""")
    
    def process_request(self, request):
        if request.GET.get('v') == 'edit':
            request.session['aphaline_edit_mode'] = True
        elif request.GET.get('v') == 'default':
            request.session['aphaline_edit_mode'] = False
        elif request.session.get('aphaline_edit_mode') is None:
            request.session['aphaline_edit_mode'] = False

    def process_response(self, request, response):
        try:

            if request.user.is_staff == False or not request.session.get('aphaline_edit_mode'): 
                response.content = self.aph_pattern.sub('', response.content)
            
            if request.user.is_staff == False:
                return response
            elif (
                request.session.get('aphaline_edit_mode') is None
                or request.session['aphaline_edit_mode'] == False
            ):
                response.set_cookie('aphaline_edit_mode', 0)
                return response
            else:
                response.set_cookie('aphaline_edit_mode', 1)
                return response
        except AttributeError:
            # redirect detected
            return response 