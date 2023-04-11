from typing import TypeVar, Any

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest

from .utils import *

AuthForm = TypeVar('AuthForm', bound=AuthenticationForm)
DjangoModel = TypeVar('DjangoModel', bound=Model)


class PassRequestMixin:
    """
    Mixin which puts the request into the form's kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self: DjangoView) -> Any:
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PopRequestMixin:
    """
    Mixin which pops request out of the kwargs and attaches it to the form's
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
    Mixin which passes or saves object based on request type.
    """

    def save(self: DjangoView, commit: bool = True) -> DjangoModel:
        if not is_ajax(self.request.META) or self.request.POST.get('asyncUpdate') == 'True':
            return super().save(commit=commit)
        else:
            return super().save(commit=False)


class DeleteMessageMixin:
    """
    Mixin which adds message to BSModalDeleteView and only calls the delete method if request
    is not ajax request.
    """
   
    def delete(self: DeleteMessageMixinProtocol, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        if not is_ajax(request.META):
            messages.success(request, self.success_message)
            return super().delete(request, *args, **kwargs)
        else:
            self.object = self.get_object()
            return HttpResponseRedirect(self.get_success_url())


class LoginAjaxMixin:
    """
    Mixin which authenticates user if request is not ajax request.
    """

    def form_valid(self: LoginAjaxMixinProtocol, form: AuthForm) -> HttpResponseRedirect:
        if not is_ajax(self.request.META):
            auth_login(self.request, form.get_user())
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
