def aphaline_edit_mode(request):
    return { 'aphaline_edit_mode': request.session.get('aphaline_edit_mode') }