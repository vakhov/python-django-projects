# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

def paginate(context, result_key, query, count, page, root):

    if page == '1' or page == 1:
        return HttpResponseRedirect(root)
    elif page is None:
        page = 1
    else:
        page = int(page)

    p = Paginator(query, count)

    if p.num_pages >= page and page is not 0:
        context['pagination'] = {}
        context['pagination']['current_page'] = page
        context['pagination']['root'] = root
        context['pagination']['page_range'] = p.page_range
        context['pagination']['num_pages'] = p.num_pages
        context[result_key] = p.page(page).object_list

        if p.page(page).has_previous() == True:
            context['pagination']['previous_page'] = p.page(page).previous_page_number()

        if p.page(page).has_next() == True:
            context['pagination']['next_page'] = p.page(page).next_page_number()

    else:
        raise Http404

def render_template(request, page, context):
    template = request.site.siteparams.template
    path = template.slug + '/' + page + '.html'
    return render_to_response(path, context)
