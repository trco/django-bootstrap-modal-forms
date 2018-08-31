# Django
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
# Project
from .forms import BookForm
from .models import Book
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin


class Index(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'index.html'


# Create
class BookCreateView(PassRequestMixin, SuccessMessageMixin,
                     generic.CreateView):
    template_name = 'books/create_book.html'
    form_class = BookForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


# Update
class BookUpdateView(PassRequestMixin, SuccessMessageMixin,
                     generic.UpdateView):
    model = Book
    template_name = 'books/update_book.html'
    form_class = BookForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


# Read
class BookReadView(generic.DetailView):
    model = Book
    template_name = 'books/read_book.html'


# Delete
class BookDeleteView(DeleteAjaxMixin, generic.DeleteView):
    model = Book
    template_name = 'books/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')
