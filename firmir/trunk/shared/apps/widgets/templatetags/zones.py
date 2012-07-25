from django import template

register = template.Library()

@register.tag
def render_zone(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'%s' tag takes exactly one argument: Zone object" % bits[0])
    return Zone(bits[1])

class Zone(template.Node):
    def __init__(self, zone):
        self.zone = zone
    def render(self, context):
        zone = template.Variable(self.zone).resolve(context)
        return zone.render(context)
