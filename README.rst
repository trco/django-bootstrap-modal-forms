
============================
Django Bootstrap Modal Forms
============================

A jQuery plugin for creating AJAX driven Django forms in Bootstrap modal.

Installation
============

1. Install django-bootstrap-modal-forms::

    $ pip install django-bootstrap-modal-forms

2. Add "bootstrap_modal_forms" to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'bootstrap_modal_forms',
        ...
    ]

3. Include Bootstrap, jQuery and jquery.bootstrap.modal.forms.js on every page where you would like to set up the AJAX driven Django forms in Bootstrap modal.

IMPORTANT: Adjust Bootstrap and jQuery file paths to match yours, but include jquery.bootstrap.modal.forms.js exactly as in code bellow.

.. code-block:: html+django

    <head>
        <link rel="stylesheet" href="{% static 'assets/css/bootstrap.css' %}">
    </head>

    <body>
        <script src="{% static 'assets/js/bootstrap.js' %}"></script>
        <script src="{% static 'assets/js/jquery.js' %}"></script>
        <script src="{% static 'js/jquery.bootstrap.modal.forms.js' %}"></script>
    </body>

Usage
=====

1. Form
*******

Define either Django Form or ModelForm. django-bootstrap-modal-forms works with both.

.. code-block:: python

    forms.py

    from django import forms
    from .models import Test

    class TestForm(forms.ModelForm):
        class Meta:
            model = Test
            fields = ['test_one', 'test_two', ]

2. Form's html
**************

.. code-block:: html

    test/test.html

    <form method="post" action="">
      {% csrf_token %}

     <div class="modal-header">
        <h5 class="modal-title">Create a new test</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        {% for field in form %}
          <div class="form-group{% if field.errors %} invalid{% endif %}">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% field %}
            {% for error in field.errors %}
              <p class="help-block">{{ error }}</p>
            {% endfor %}
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary" formnovalidate="formnovalidate">Create</button>
      </div>

    </form>

- Define form's html and save it as Django template.
- Bootstrap 4 modal elements are used in this example.
- Form will POST to ``formURL`` defined in #6.
- Add "invalid" class or custom errorClass to the elements that wrap the fields.
- ``invalid`` class acts as a flag for the fields having errors after the form has been POSTed.

3. Class-based view
*******************

Define a class-based view TestFormView that processes the form defined in #1 and uses the template defined in #2. Define also the success_url for TestFormView and separate SuccessView with your own success.html.

.. code-block:: python

    views.py

    from django.shortcuts import render
    from django.urls import reverse_lazy
    from django.views.generic.base import TemplateView
    from django.views.generic.edit import CreateView, UpdateView

    from .forms import TestForm

    class TestCreateView(CreateView):
        template_name = 'test/test.html'
        form_class = TestForm
        success_url = reverse_lazy('test:success_view')

    class TestUpdateView(CreateView):
        model = Test
        template_name = 'test/test.html'
        form_class = TestForm
        success_url = reverse_lazy('test:success_view')

    class SuccessView(TemplateView):
        template_name = "test/success.html"

4. URL for the view
*******************

Define URL for the views in #3.

.. code-block:: python

    from django.urls import path

    from . import views

    app_name = 'test'
    urlpatterns = [
        path('', views.index, name='index'),
        path('test/create-test/', views.TestCreateView.as_view(), name='create_test')
        path('test/update-test/<int:pk>', views.TestUpdateView.as_view(), name='update_test')
        path('test/success/', views.SuccessView.as_view(), name='success_view')
    ]

5. Bootstrap modal and trigger element
**************************************

Define the Bootstrap modal window and trigger elements.

.. code-block:: html+django

    test/index.html

    <div class="modal fade" tabindex="-1" role="dialog" id="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">

        </div>
      </div>
    </div>

    <!-- Create test button -->
    <button type="button" class="create-test btn btn-primary">
      <span class="fa fa-plus fa-sm"></span>
      Create
    </button>

    <!-- Update test buttons -->
    {% for test in test_queryset %}
      <button type="button" class="update-test btn btn-primary" data-id="test.id">
        <span class="fa fa-plus fa-sm"></span>
        Update
      </button>
    {% endfor %}

- Same modal window can be used for multiple modalForms in single template (see #6).
- Form's html from #2 is loaded within ``<div class="modal-content"></div>`` and action attribute of the form is set to ``formURL`` set in #6.
- Trigger element (in this example buttons) selected with class selector is used for instantiation of ``modalForm`` in #6.
- Any element can be trigger element as long as modalForm is bound to it.

IMPORTANT: See the difference between buttons triggering Create and Update. Extra ``data-id`` attribute should be set for Update buttons to allow dynamic construction of appropriate ``formURLs`` in #6.

6. modalForm
************

Add script to the template from #5 and bind the ``modalForm`` to the trigger elements. Set TestCreateView and TestUpdateView URLs defined in #4 as ``formURL`` and SuccessView URL as ``successURL`` properties of ``modalForm``.

If you want to create **more modalForms in single template using the same modal window** from #5, repeat steps #1 to #4, create new trigger element as in #5 and bind the new ``modalForm`` with unique URLs to it.

IMPORTANT: Default values for ``modalID``, ``modalContent``, ``modalForm`` and ``errorClass`` are used in this example, while ``formURL`` and ``successURL`` are customized. If you customize any other option adjust the code of the above examples accordingly.

.. code-block:: html

    test/index.html

    <script type="text/javascript">
    $(document).ready(function() {

        $(".create-test").modalForm({
            formURL: "{% url 'test:create_test' %}",
            successURL: "{% url 'test:success_view' %}"
        });

        // Bind modalForm to each Update button and set formURL to unique url
        // via data-id from #5
        $(".update-test").each(function () {
          $(this).modalForm({
            formURL: "{% url 'test:update_test' $(this).data('id') %}",
            successURL: "{% url 'test:success_view' %}"
          });
        });

    });
    </script>

Options
=======

modalID
  Sets the custom id of the modal. ``Default: "#modal"``

modalContent
  Sets the custom class of the element to which the form's html is appended. ``Default: ".modal-content"``

modalForm
  Sets the custom form selector. ``Default: ".modal-content form"``

formURL
  Sets the url of the form's view and html. ``Default: null``

successURL
  Sets the url for redirection after successful form submission. ``Default: "/"``

errorClass
  Sets the custom errorClass for the form fields. ``Default: ".invalid"``


How it works
============

1. Click event on trigger element opens modal with ``modalID``
2. Form at ``formURL`` is appended to the element with ``modalContent`` class
3. On submit the form is POSTed via AJAX request to ``formURL``
4. **Unsuccessful POST request** returns errors, which are shown under form fields in modal
5. **Successful POST request** redirects to ``successURL``

Contribute
==========

This is an Open Source project and any contribution is appriciated.

License
=======

This project is licensed under the MIT License.
