#import re
from utils import dict2htmlattrs

def aphaline_render_zone(fn):
    def new(self, context=None):
        result = fn(self, context)
        user = context.get('user')
        edit_mode = context.get('aphaline_edit_mode')
        if edit_mode and user is not None and user.is_staff:
            definition = {
                'aph-zone-id': self.id
            }
            result = '<div ' + dict2htmlattrs(definition) + '>' + result + '</div>'
        return result
    return new

def aphaline_render_widget(fn):
    def new(widget, context=None):
        result = fn(widget, context)
        user = context.get('user', None)
        edit_mode = context.get('aphaline_edit_mode')
        if edit_mode and user is not None and user.is_staff:
            definition = {
                'aph-widget-id': widget.id,
                'aph-widget-type': widget.type
            }
            result = '<div ' + dict2htmlattrs(definition) + '>' + result + '</div>'
        return result
    return new