# Django
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('index')
