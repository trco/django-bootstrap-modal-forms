from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class BSModalForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    pass
