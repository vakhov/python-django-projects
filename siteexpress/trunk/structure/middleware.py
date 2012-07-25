# -*- coding: utf-8 -*-

from models import Section

class StructureMiddleware:
    def process_request(self, request):
        try:
            request.current_section = Section.get_node_by_path(request.path)
            request.structure = Section.get_structure()
        except:
            request.current_section = None
            request.structure = {}
