from django.template import Library, TemplateSyntaxError, Variable
from django.utils.text import unescape_string_literal
from .templatetags.generic_edit.QueryString import QueryStringNode

def _process_arg(arg):
    try:
        return unescape_string_literal(arg)
    except ValueError:
        return Variable(arg)


register = Library()

@register.tag
def query_string(parser, token):
    split_contents = token.split_contents()
    tag_name, args = split_contents[0], split_contents[1:]

    if len(args) >= 2 and args[0] == 'from':
        take_from = Variable(args[1])
        args = args[2:]

    if len(args) >= 2 and args[-2] == 'as':
        set_in_context = args[-1]
        args = args[:-2]

    args = map(_process_arg, args)

    local_vars = locals()
    return QueryStringNode(*(local_vars.get(key) for key in ('args', 'take_from', 'set_in_context')))

