# Django
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
# Local
from .forms import BookForm
from .models import Book


class Index(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'index.html'


class BookCreateView(generic.CreateView):
    template_name = 'books/create_book.html'
    form_class = BookForm
    success_url = reverse_lazy('index')


class BookUpdateView(generic.UpdateView):
    model = Book
    template_name = 'books/update_book.html'
    form_class = BookForm
    success_url = reverse_lazy('index')


class BookReadView(generic.DetailView):
    model = Book
    template_name = 'books/read_book.html'


class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy('index')
