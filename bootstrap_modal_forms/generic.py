from django.views import generic
from django.contrib.auth.views import LoginView

from .mixins import PassRequestMixin, DeleteMessageMixin, LoginAjaxMixin, FormValidationMixin


class BSModalLoginView(LoginAjaxMixin, LoginView):
    pass


class BSModalFormView(PassRequestMixin, generic.FormView):
    pass


class BSModalCreateView(PassRequestMixin, FormValidationMixin, generic.CreateView):
    pass


class BSModalUpdateView(PassRequestMixin, FormValidationMixin, generic.UpdateView):
    pass


class BSModalReadView(generic.DetailView):
    pass


class BSModalDeleteView(DeleteMessageMixin, generic.DeleteView):
    pass
