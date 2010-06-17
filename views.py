from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404

def generic_edit_factory(model_class, form_class, template, redirect_func=None):
    """ factory function to generate views that handle create/edit on models and associated modelforms """

    def generic_edit_view(request, id=None, extra_context=None, **kwargs):
        model = get_object_or_404(model_class, pk=id) if id is not None else None
        if request.method == 'POST':
            form = form_class(request.POST, instance=model)
            if form.is_valid():
                form.save()

                if redirect_func is not None:
                    redirect_to = redirect_func(form.instance)
                else:
                    redirect_to = form.instance.get_absolute_url()
                return redirect(redirect_to)
        else:
            form = form_class(instance=model)

        if extra_context is None:
            extra_context = {}
        extra_context['form'] = form
        return direct_to_template(request, template, extra_context=extra_context, **kwargs)

    return generic_edit_view

