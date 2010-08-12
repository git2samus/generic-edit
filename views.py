from django.forms import ModelForm
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404

def generic_edit_factory(modelform_class, template):
    """ factory function to generate views that handle create/edit on models and associated modelforms """
    assert(isinstance(modelform_class, ModelForm))

    def generic_edit_view(request, id=None):
        model_class = modelform_class.Meta.model
        model = get_object_or_404(model_class, pk=id) if id is not None else None

        if request.method == 'POST':
            form = modelform_class(request.POST, instance=model)
            if form.is_valid():
                form.save()

                redirect_to = form.instance.get_absolute_url()
                return redirect(redirect_to)
        else:
            form = modelform_class(instance=model)

        return render_to_response(template, {'form': form}, RequestContext(request))

    return generic_edit_view

