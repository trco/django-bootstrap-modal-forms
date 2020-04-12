from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class BSForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.Form):
    pass


class BSModalForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    pass
