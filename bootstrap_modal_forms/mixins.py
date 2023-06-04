from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse

class PassRequestMixin:
    """
    Form Mixin which puts the request into the form's kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PopRequestMixin:
    """
    Form Mixin which pops request out of the kwargs and attaches it to the form's
    instance.

    Note: This mixin must precede forms.ModelForm/forms.Form. The form is not
    expecting these kwargs to be passed in, so they must be popped off before
    anything else is done.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class CreateUpdateAjaxMixin:
    """
    ModelForm Mixin which passes or saves object based on request type.
    """

    def save(self, commit=True):
        isAjaxRequest = is_ajax(self.request.META)
        asyncUpdate = self.request.POST.get('asyncUpdate') == 'True'

        if not isAjaxRequest or asyncUpdate:
            return super().save(commit=commit)
        if isAjaxRequest:
            return super().save(commit=False)


class DeleteMessageMixin:
    """
    Generic View Mixin which adds message to BSModalDeleteView and only calls the post method if request
    is not ajax request. In case request is ajax post method calls delete method, which redirects to success url.
    """

    def post(self, request, *args, **kwargs):
        if not is_ajax(request.META):
            messages.success(request, self.success_message)
            return super().post(request, *args, **kwargs)
        else:
            self.object = self.get_object()
            return HttpResponseRedirect(self.get_success_url())


class LoginAjaxMixin:
    """
    Generic View Mixin which authenticates user if request is not ajax request.
    """

    def form_valid(self, form):
        if not is_ajax(self.request.META):
            auth_login(self.request, form.get_user())
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class FormValidationMixin:
    """
    Generic View Mixin which saves object and redirects to success_url if request is not ajax request. Otherwise response 204 No content is returned.
    """

    def get_success_message(self):
        if hasattr(self, 'success_message'):
            return self.success_message

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

    def form_valid(self, form):
        isAjaxRequest = is_ajax(self.request.META)
        asyncUpdate = self.request.POST.get('asyncUpdate') == 'True'

        if isAjaxRequest:
            if asyncUpdate:
                form.save()
            return HttpResponse(status=204)

        form.save()
        messages.success(self.request, self.get_success_message())
        return HttpResponseRedirect(self.get_success_url())


def is_ajax(meta):
    return 'HTTP_X_REQUESTED_WITH' in meta and meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'
