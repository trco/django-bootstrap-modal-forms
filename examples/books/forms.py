# Django
from django import forms
# Local
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['timestamp']
