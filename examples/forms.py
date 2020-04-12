from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm, BSForm

from .models import Book


class SimpleForm(BSForm):
    comment = forms.CharField(label="Enter your comment")

    class Meta:
        fields = ["comment"]


class BookForm(BSModalForm):
    publication_date = forms.DateField(
        error_messages={"invalid": "Enter a valid date in YYYY-MM-DD format."}
    )

    class Meta:
        model = Book
        exclude = ["timestamp"]


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
