from django.template import Node, Variable, VariableDoesNotExist
from django.http import QueryDict

class QueryStringNode(Node):
    """ custom tag to update query_string arguments from templates """
    def __init__(self, args, take_from=None, set_in_context=None):
        super(QueryStringNode, self).__init__()
        self.args, self.take_from, self.set_in_context = args, take_from, set_in_context

    def render(self, context):
        args, take_from, set_in_context = self.args, self.take_from, self.set_in_context

        if take_from is not None:
            try:
                source = QueryDict(take_from.resolve(context), mutable=True)
            except VariableDoesNotExist:
                return ''
        elif 'request' in context:
            request = context['request']
            source = request.GET.copy()
        else:
            return ''

        try:
            args = [arg.resolve(context) if isinstance(arg, Variable) else arg for arg in args]
        except VariableDoesNotExist:
            return ''

        if args:
            source.setlist(args[0], args[1:])

        query_string = source.urlencode()

        if set_in_context is not None:
            context[set_in_context] = query_string
            return ''

        return query_string

