from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse

from .utils import is_ajax


class PassRequestMixin(object):
    """
    Form Mixin which puts the request into the form's kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super(PassRequestMixin, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class PopRequestMixin(object):
    """
    Form Mixin which pops request out of the kwargs and attaches it to the form's
    instance.

    Note: This mixin must precede forms.ModelForm/forms.Form. The form is not
    expecting these kwargs to be passed in, so they must be popped off before
    anything else is done.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PopRequestMixin, self).__init__(*args, **kwargs)


class CreateUpdateAjaxMixin(object):
    """
    ModelForm Mixin which passes or saves object based on request type.
    """

    def save(self, commit=True):
        if not is_ajax(self.request.META) or self.request.POST.get('asyncUpdate') == 'True':
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return instance


class DeleteMessageMixin(object):
    """
    Generic View Mixin which adds message to BSModalDeleteView and only calls the delete method if request
    is not ajax request.
    """
   
    def delete(self, request, *args, **kwargs):
        if not is_ajax(request.META):
            messages.success(request, self.success_message)
            return super(DeleteMessageMixin, self).delete(request, *args, **kwargs)
        else:
            self.object = self.get_object()
            return HttpResponseRedirect(self.get_success_url())


class LoginAjaxMixin(object):
    """
    Generic View Mixin which authenticates user if request is not ajax request.
    """

    def form_valid(self, form):
        if not is_ajax(self.request.META):
            auth_login(self.request, form.get_user())
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class FormValidationMixin(object):
    """
    Generic View Mixin which saves object and redirects to success_url if request is not ajax request. Otherwise resoponse 204 No content is returned.
    """
        
    def form_valid(self, form):
        isAjaxRequest = is_ajax(self.request.META)
        asyncUpdate = self.request.POST.get('asyncUpdate') == 'True'

        if isAjaxRequest:
            if asyncUpdate:
                form.save()
            return HttpResponse(status=204)
        
        form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)   