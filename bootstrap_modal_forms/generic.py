import django
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .mixins import PassRequestMixin, DeleteMessageMixin, LoginAjaxMixin

DJANGO_VERSION = django.get_version().split('.')
DJANGO_MAJOR_VERSION = int(DJANGO_VERSION[0])
DJANGO_MINOR_VERSION = int(DJANGO_VERSION[1])

# Import custom LoginView for Django versions < 1.11 
if DJANGO_MAJOR_VERSION == 1 and DJANGO_MINOR_VERSION < 11:
    from .compatibility import LoginView
else:
    from django.contrib.auth.views import LoginView

class BSModalLoginView(LoginAjaxMixin, SuccessMessageMixin, LoginView):
    pass


class BSModalCreateView(PassRequestMixin, SuccessMessageMixin,
                        generic.CreateView):
    pass


class BSModalUpdateView(PassRequestMixin, SuccessMessageMixin,
                        generic.UpdateView):
    pass


class BSModalReadView(generic.DetailView):
    pass


class BSModalDeleteView(DeleteMessageMixin, generic.DeleteView):
    pass
