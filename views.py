from django.forms import ModelForm
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from .utils import sort_q, paginate_q

def generic_edit_factory(modelform_class, template_name):
    def generic_edit_view(request, id=None, **context):
        model_class = modelform_class.Meta.model
        instance = get_object_or_404(model_class, pk=id) if id is not None else None

        if request.method == 'POST':
            form = modelform_class(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                redirect_to = form.instance.get_absolute_url()
                return redirect(redirect_to)
        else:
            form = modelform_class(instance=instance)

        context.update({
            'form': form,
        })
        return render_to_response(template_name, context, RequestContext(request))

    assert(isinstance(modelform_class, ModelForm))
    return generic_edit_view


def generic_list_factory(queryset, template_name, sort_fields, default_sort, table_columns, results_per_page=None):
    def generic_list_view(request, **context):
        queryset, sort_mode = sort_q(request, queryset, sort_fields, default_sort)
        paginator, pagenum, resultset = paginate_q(request, queryset, results_per_page)

        context.update({
            'sort_mode': sort_mode,
            'table_columns': table_columns,
            'paginator': paginator,
            'pagenum': pagenum,
            'resultset': resultset,
        })
        return render_to_response(template_name, context, RequestContext(request))

    return generic_list_view

