from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView,
    BSModalFormView,
)
from .forms import (
    SimpleModalForm,
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm)
from .models import Book


class Index(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(book_type=int(self.request.GET['type']))
        return qs


class SimpleFormView(SuccessMessageMixin, BSModalFormView):
    template_name = 'examples/simple.html'
    form_class = SimpleModalForm
    success_message = 'Success: your comment \'%(comment)s\' was taken into account!'
    success_url = reverse_lazy('index')


class BookFilterView(BSModalFormView):
    template_name = 'examples/filter_book.html'
    form_class = BookFilterForm

    def form_valid(self, form):
        if "clear" in self.request.POST:
            # the user has clicked on the 'Clear' button
            self.filter = ''
        else:
            # the user has filtered the list of books
            self.filter = f'?type={form.cleaned_data["type"]}'

        # call the base form_valid (that will call the get_success_url)
        resp = super().form_valid(form)
        return resp

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


class BookCreateView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = Book
    template_name = 'examples/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


class BookReadView(BSModalReadView):
    model = Book
    template_name = 'examples/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = Book
    template_name = 'examples/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'examples/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')
