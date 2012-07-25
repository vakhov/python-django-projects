# -*- coding: utf-8 -*-

from django import template

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

class CreateArrayNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        context[self.name] = []
        return ''

class AddToArrayNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name].append(self.value.resolve(context, True))
        return ''

def do_assign(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

def do_create_array(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'%s' tag takes one argument" % bits[0])
    return CreateArrayNode(bits[1])

def do_add_to_array(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AddToArrayNode(bits[1], value)

register = template.Library()
register.tag('assign', do_assign)
register.tag('create_array', do_create_array)
register.tag('add_to_array', do_add_to_array)
