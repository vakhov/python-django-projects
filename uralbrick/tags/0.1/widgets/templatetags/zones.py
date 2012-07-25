import re
from django import template
from widgets.models import *

register = template.Library()

@register.tag
def render_zone(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'%s' tag takes one argument" % bits[0])
    return Zone(bits[1])

class Zone(template.Node):

    def __init__(self, zone):
        self.zone = zone
    
    def render(self, context):
        # global brackets
        # zone_tag = self.nodelist.render(context)
        self.zone = template.Variable(self.zone).resolve(context)
        return self.zone.render(context)
