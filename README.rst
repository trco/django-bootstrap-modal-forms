============================
Django Bootstrap Modal Forms
============================

A Django plugin for creating AJAX driven forms in Bootstrap modal.

Live Demo
=========

Demo_

.. _Demo: http://trco.silkym.com/dbmf/

Installation
============

1. Install ``django-bootstrap-modal-forms``::

    $ pip install django-bootstrap-modal-forms

2. Add ``bootstrap_modal_forms`` to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = [
        ...
        'bootstrap_modal_forms',
        ...
    ]

3. Include Bootstrap, jQuery and ``jquery.bootstrap.modal.forms.js`` on every page where you would like to set up the AJAX driven Django forms in Bootstrap modal.

IMPORTANT: Adjust Bootstrap and jQuery file paths to match yours, but include ``jquery.bootstrap.modal.forms.js`` exactly as in code bellow.

.. code-block:: html+django

    <head>
        <link rel="stylesheet" href="{% static 'assets/css/bootstrap.css' %}">
    </head>

    <body>
        <script src="{% static 'assets/js/bootstrap.js' %}"></script>
        <script src="{% static 'assets/js/jquery.js' %}"></script>
        <script src="{% static 'js/jquery.bootstrap.modal.forms.js' %}"></script>
        <!-- You can alternatively load the minified version -->
        <script src="{% static 'js/jquery.bootstrap.modal.forms.min.js' %}"></script>
    </body>

How it works?
=============
.. code-block:: html

    index.html

    <script type="text/javascript">
    $(document).ready(function() {

        $("#create-book").modalForm({
            formURL: "{% url 'create_book' %}"
        });

    });
    </script>

1. Click event on html element instantiated with ``modalForm`` opens modal
2. Form at ``formURL`` is appended to the modal
3. On submit the form is POSTed via AJAX request to ``formURL``
4. **Unsuccessful POST request** returns errors, which are shown in modal
5. **Successful POST request** submits the form and redirects to ``success_url`` and shows ``success_message``, which are both defined in related Django view

Usage
=====

1. Form
*******

Define BookModelForm and inherit built-in form ``BSModalModelForm``.

.. code-block:: python

    forms.py

    from .models import Book
    from bootstrap_modal_forms.forms import BSModalModelForm

    class BookModelForm(BSModalModelForm):
        class Meta:
            model = Book
            fields = ['title', 'author', 'price']

2. Form's html
**************

Define form's html and save it as Django template.

- Bootstrap 4 modal elements are used in this example.
- Form will POST to ``formURL`` defined in #6.
- Add ``class="invalid"`` or custom ``errorClass`` (see paragraph **Options**) to the elements that wrap the fields.
- ``class="invalid"`` acts as a flag for the fields having errors after the form has been POSTed.

.. code-block:: html

    book/create_book.html

    <form method="post" action="">
      {% csrf_token %}

     <div class="modal-header">
        <h5 class="modal-title">Create new Book</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        {% for field in form %}
          <div class="form-group{% if field.errors %} invalid{% endif %}">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% for error in field.errors %}
              <p class="help-block">{{ error }}</p>
            {% endfor %}
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary">Create</button>
      </div>

    </form>

3. Class-based view
*******************

Define a class-based view BookCreateView and inherit from built-in generic view ``BSModalCreateView``. BookCreateView processes the form defined in #1, uses the template defined in #2 and redirects to ``success_url`` showing ``success_message``.

.. code-block:: python

    views.py

    from django.urls import reverse_lazy
    from .forms import BookModelForm
    from .models import Book
    from bootstrap_modal_forms.generic import BSModalCreateView

    class BookCreateView(BSModalCreateView):
        template_name = 'examples/create_book.html'
        form_class = BookModelForm
        success_message = 'Success: Book was created.'
        success_url = reverse_lazy('index')

4. URL for the view
*******************

Define URL for the view in #3.

.. code-block:: python

    from django.urls import path
    from books import views

    urlpatterns = [
        path('', views.Index.as_view(), name='index'),
        path('create/', views.BookCreateView.as_view(), name='create_book'),
    ]

5. Bootstrap modal and trigger element
**************************************

Define the Bootstrap modal window and html element triggering modal opening.

- **Single modal** can be used for multiple ``modalForms`` in single template (see #6).
- When using **multiple modals** on the same page each modal should have unique ``id`` and the same value should also be set as ``modalID`` option when instantiating ``modalForm`` on trigger element.
- Trigger element (in this example button with ``id="create-book"``) is used for instantiation of ``modalForm`` in #6.
- Any element can be trigger element as long as ``modalForm`` is bound to it.
- Click event on trigger element loads form's html from #2 within ``<div class="modal-content"></div>`` and sets action attribute of the form to ``formURL`` set in #6.

.. code-block:: html+django

    index.html

    <div class="modal fade" tabindex="-1" role="dialog" id="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content"></div>
      </div>
    </div>

    <!-- Create book button -->
    <button id="create-book" class="btn btn-primary" type="button" name="button">Create book</button>

6. modalForm
************

Add script to the template from #5 and bind the ``modalForm`` to the trigger element. Set BookCreateView URL defined in #4 as ``formURL`` property of ``modalForm``.

- If you want to create **more modalForms in single template using the single modal window** from #5, repeat steps #1 to #4, create new trigger element as in #5 and bind the new ``modalForm`` with unique URL to it.
- Default values for ``modalID``, ``modalContent``, ``modalForm`` and ``errorClass`` are used in this example, while ``formURL`` is customized. If you customize any other option adjust the code of the above examples accordingly.

.. code-block:: html

    index.html

    <script type="text/javascript">
    $(document).ready(function() {

        $("#create-book").modalForm({
            formURL: "{% url 'create_book' %}"
        });

    });
    </script>

Async create/update with or without modal closing on submit
===========================================================

Set ``asyncUpdate`` and ``asyncSettings`` settings to create or update objects without page redirection to ``successUrl`` and define whether a modal should close or stay opened after form submission. See comments in example below and paragraph **modalForm options** for explanation of ``asyncSettings``.
See examples on how to properly reinstantiate modal forms for all CRUD buttons when using async options.

.. code-block:: html

    index.html

    <!-- asyncSettings.dataElementId -->
    <table id="books-table" class="table">
      <thead>
        ...
      </thead>
      <tbody>
      {% for book in books %}
        <tr>
            ...
            <!-- Update book buttons -->
            <button type="button" class="update-book btn btn-sm btn-primary" data-form-url="{% url 'update_book' book.pk %}">
              <span class="fa fa-pencil"></span>
            </button>
            ...
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>

    <script type="text/javascript">
        $(function () {
            ...

            # asyncSettings.successMessage
            var asyncSuccessMessage = [
              "<div ",
              "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
              "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
              "Success: Book was updated.",
              "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>",
              "<span aria-hidden='true'>&times;</span>",
              "</button>",
              "</div>",
              "<script>",
              "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
              "<\/script>"
            ].join();

            # asyncSettings.addModalFormFunction
            function updateBookModalForm() {
              $(".update-book").each(function () {
                $(this).modalForm({
                  formURL: $(this).data("form-url"),
                  asyncUpdate: true,
                  asyncSettings: {
                    closeOnSubmit: false,
                    successMessage: asyncSuccessMessage
                    dataUrl: "books/",
                    dataElementId: "#books-table",
                    dataKey: "table",
                    addModalFormFunction: updateBookModalForm
                  }
                });
              });
            }
            updateBookModalForm();
        
            ...
        });
    </script>

.. code-block:: python

    urls.py

    from django.urls import path
    from . import views

    urlpatterns = [
        ...
        # asyncSettings.dataUrl
        path('books/', views.books, name='books'),
        ...
    ]

.. code-block:: python

    views.py

    from django.http import JsonResponse
    from django.template.loader import render_to_string
    from .models import Book

    def books(request):
        data = dict()
        if request.method == 'GET':
            books = Book.objects.all()
            # asyncSettings.dataKey = 'table'
            data['table'] = render_to_string( 
                '_books_table.html',
                {'books': books},
                request=request
            )
            return JsonResponse(data)

modalForm options
=================

modalID
  Sets the custom id of the modal. ``Default: "#modal"``

modalContent
  Sets the custom class of the element to which the form's html is appended. If you change ``modalContent`` to the custom class, you should also change ``modalForm`` accordingly. To keep Bootstrap's modal style you should than copy Bootstrap's style for ``modal-content`` and set it to your new modalContent class. ``Default: ".modal-content"``

modalForm
  Sets the custom form selector. ``Default: ".modal-content form"``

formURL
  Sets the url of the form's view and html. ``Default: null``

isDeleteForm
  Defines if form is used for deletion. Should be set to ``true`` for deletion forms.  ``Default: false``

errorClass
  Sets the custom class for the form fields having errors. ``Default: ".invalid"``

asyncUpdate
  Sets asynchronous content update after form submission. ``Default: false``

asyncSettings.closeOnSubmit
  Sets whether modal closes or not after form submission. ``Default: false``

asyncSettings.successMessage
  Sets successMessage shown after succesful for submission. Should be set to string defining message element. See ``asyncSuccessMessage`` example above. ``Default: null``

asyncSettings.dataUrl
  Sets url of the view returning new queryset = all of the objects plus newly created or updated one after asynchronous update. ``Default: null``

asyncSettings.dataElementId
  Sets the ``id`` of the element which rerenders asynchronously updated queryset. ``Default: null``

asyncSettings.dataKey
  Sets the key containing asynchronously updated queryset in the data dictionary returned from the view providing updated queryset. ``Default: null``

asyncSettings.addModalFormFunction
  Sets the method needed for reinstantiation of event listeners on buttons (single or all CRUD buttons) after asynchronous update. ``Default: null``

modalForm default settings object and it's structure
****************************************************

.. code-block:: html
  
    triggerElement.modalForm({
        modalID: "#modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: null,
        isDeleteForm: false,
        errorClass: ".invalid",
        asyncUpdate: false,
        asyncSettings: {
            closeOnSubmit: false,
            successMessage: null,
            dataUrl: null,
            dataElementId: null,
            dataKey: null,
            addModalFormFunction: null
        }
    });

Forms
=====

Import forms with ``from bootstrap_modal_forms.forms import BSModalForm``.

BSModalForm
    Inherits PopRequestMixin and Django's forms.Form.

BSModalModelForm
    Inherits PopRequestMixin, CreateUpdateAjaxMixin and Django's forms.ModelForm.

Mixins
======

Import mixins with ``from bootstrap_modal_forms.mixins import PassRequestMixin``.

PassRequestMixin
    Puts the request into the form's kwargs.

PopRequestMixin
    Pops request out of the kwargs and attaches it to the form's instance.

CreateUpdateAjaxMixin
    Saves or doesn't save the object based on the request type.

DeleteMessageMixin
    Deletes object if request is not ajax request.

LoginAjaxMixin
    Authenticates user if request is not ajax request.

Generic views
=============

Import generic views with ``from bootstrap_modal_forms.generic import BSModalFormView``.

BSModalFormView
    Inherits PassRequestMixin and Django's generic.FormView.

BSModalCreateView
    Inherits PassRequestMixin and Django's SuccessMessageMixin and generic.CreateView.

BSModalUpdateView
    Inherits PassRequestMixin and Django's SuccessMessageMixin and generic.UpdateView.

BSModalReadView
    Inherits Django's generic.DetailView.

BSModalDeleteView
    Inherits DeleteMessageMixin and Django's generic.DeleteView.

Examples
========

To see ``django-bootstrap-modal-forms`` in action clone the repository and run the examples locally::

    $ git clone https://github.com/trco/django-bootstrap-modal-forms.git
    $ cd django-bootstrap-modal-forms
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

Tests
=====

Run unit and functional tests inside of project folder::

    $ python manage.py test

Example 1: Signup form in Bootstrap modal
*****************************************

For explanation how all the parts of the code work together see paragraph **Usage**. To test the working solution presented here clone and run **Examples**.

.. code-block:: python

    forms.py

    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User
    from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


    class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                                 UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'password1', 'password2']

.. code-block:: html

    signup.html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Sign up</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">

        <div class="{% if form.non_field_errors %}invalid{% endif %} mb-2">
          {% for error in form.non_field_errors %}
            {{ error }}
          {% endfor %}
        </div>

        {% for field in form %}
          <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% render_field field class="form-control" placeholder=field.label %}
            <div class="{% if field.errors %} invalid{% endif %}">
              {% for error in field.errors %}
                <p class="help-block">{{ error }}</p>
              {% endfor %}
            </div>
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Sign up</button>
      </div>

    </form>

.. code-block:: python

    views.py

    from django.urls import reverse_lazy
    from bootstrap_modal_forms.generic import BSModalCreateView
    from .forms import CustomUserCreationForm

    class SignUpView(BSModalCreateView):
        form_class = CustomUserCreationForm
        template_name = 'examples/signup.html'
        success_message = 'Success: Sign up succeeded. You can now Log in.'
        success_url = reverse_lazy('index')

.. code-block:: python

    urls.py

    from django.urls import path
    from . import views

    app_name = 'accounts'
    urlpatterns = [
        path('signup/', views.SignUpView.as_view(), name='signup')
    ]


.. code-block:: html

    .html file containing modal, trigger element and script instantiating modalForm

    <div class="modal fade" tabindex="-1" role="dialog" id="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content"></div>
      </div>
    </div>

    <button id="signup-btn" class="btn btn-primary" type="button" name="button">Sign up</button>

    <script type="text/javascript">
      $(function () {
        // Sign up button
        $("#signup-btn").modalForm({
            formURL: "{% url 'signup' %}"
        });
      });
    </script>

Example 2: Login form in Bootstrap modal
****************************************

For explanation how all the parts of the code work together see paragraph **Usage**. To test the working solution presented here clone and run **Examples**.

You can set the login redirection by setting the ``LOGIN_REDIRECT_URL`` in ``settings.py``.

You can also set the custom login redirection by:

1. Adding ``success_url`` to the ``extra_context`` of ``CustomLoginView``
2. Setting this ``success_url`` variable as a value of the ``hidden input field`` with ``name="next"`` within the Login form html

.. code-block:: python

    forms.py

    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth.models import User

    class CustomAuthenticationForm(AuthenticationForm):
        class Meta:
            model = User
            fields = ['username', 'password']

.. code-block:: html

    login.html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Log in</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">

        <div class="{% if form.non_field_errors %}invalid{% endif %} mb-2">
          {% for error in form.non_field_errors %}
            {{ error }}
          {% endfor %}
        </div>

        {% for field in form %}
          <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% render_field field class="form-control" placeholder=field.label %}
            <div class="{% if field.errors %} invalid{% endif %}">
              {% for error in field.errors %}
                <p class="help-block">{{ error }}</p>
              {% endfor %}
            </div>
          </div>
        {% endfor %}

        <!-- Hidden input field for custom redirection after successful login -->
        <input type="hidden" name="next" value="{{ success_url }}">
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Log in</button>
      </div>

    </form>

.. code-block:: python

    views.py

    from django.urls import reverse_lazy
    from bootstrap_modal_forms.generic import BSModalLoginView
    from .forms import CustomAuthenticationForm

    class CustomLoginView(BSModalLoginView):
        authentication_form = CustomAuthenticationForm
        template_name = 'examples/login.html'
        success_message = 'Success: You were successfully logged in.'
        extra_context = dict(success_url=reverse_lazy('index'))

.. code-block:: python

    urls.py

    from django.urls import path
    from . import views

    app_name = 'accounts'
    urlpatterns = [
        path('login/', views.CustomLoginView.as_view(), name='login')
    ]

.. code-block:: html

    .html file containing modal, trigger element and script instantiating modalForm

    <div class="modal fade" tabindex="-1" role="dialog" id="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content"></div>
      </div>
    </div>

    <button id="login-btn" class="btn btn-primary" type="button" name="button">Sign up</button>

    <script type="text/javascript">
      $(function () {
        // Log in button
        $("#login-btn").modalForm({
            formURL: "{% url 'login' %}"
        });
      });
    </script>

Example 3: Django's forms.ModelForm (CRUD forms) in Bootstrap modal
*******************************************************************

For explanation how all the parts of the code work together see paragraph **Usage**. To test the working solution presented here clone and run **Examples**.

.. code-block:: python

    forms.py

    from .models import Book
    from bootstrap_modal_forms.forms import BSModalModelForm


    class BookModelForm(BSModalModelForm):
        class Meta:
            model = Book
            exclude = ['timestamp']

.. code-block:: html

    create_book.html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Create Book</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">

        <div class="{% if form.non_field_errors %}invalid{% endif %} mb-2">
          {% for error in form.non_field_errors %}
            {{ error }}
          {% endfor %}
        </div>

        {% for field in form %}
          <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% render_field field class="form-control" placeholder=field.label %}
            <div class="{% if field.errors %} invalid{% endif %}">
              {% for error in field.errors %}
                <p class="help-block">{{ error }}</p>
              {% endfor %}
            </div>
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Create</button>
      </div>

    </form>

.. code-block:: html

    update_book.html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Update Book</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        <div class="{% if form.non_field_errors %}invalid{% endif %} mb-2">
          {% for error in form.non_field_errors %}
            {{ error }}
          {% endfor %}
        </div>

        {% for field in form %}
          <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% render_field field class="form-control" placeholder=field.label %}
            <div class="{% if field.errors %} invalid{% endif %}">
              {% for error in field.errors %}
                <p class="help-block">{{ error }}</p>
              {% endfor %}
            </div>
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Update</button>
      </div>

    </form>

.. code-block:: html

    read_book.html

    {% load widget_tweaks %}

    <div class="modal-header">
      <h3 class="modal-title">Book details</h3>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>

    <div class="modal-body">
      <div class="">
        Title: {{ book.title }}
      </div>
      <div class="">
        Author: {{ book.author }}
      </div>
      <div class="">
        Price: {{ book.price }} €
      </div>
    </div>

    <div class="modal-footer">
      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
    </div>

.. code-block:: html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Delete Book</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        <p>Are you sure you want to delete book with title
          <strong>{{ book.title }}</strong>?</p>
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-danger">Delete</button>
      </div>

    </form>

.. code-block:: python

    views.py

    from django.urls import reverse_lazy
    from django.views import generic
    from .forms import BookModelForm
    from .models import Book
    from bootstrap_modal_forms.generic import (
      BSModalCreateView,
      BSModalUpdateView,
      BSModalReadView,
      BSModalDeleteView
    )

    class Index(generic.ListView):
        model = Book
        context_object_name = 'books'
        template_name = 'index.html'

    # Create
    class BookCreateView(BSModalCreateView):
        template_name = 'examples/create_book.html'
        form_class = BookModelForm
        success_message = 'Success: Book was created.'
        success_url = reverse_lazy('index')

    # Update
    class BookUpdateView(BSModalUpdateView):
        model = Book
        template_name = 'examples/update_book.html'
        form_class = BookModelForm
        success_message = 'Success: Book was updated.'
        success_url = reverse_lazy('index')

    # Read
    class BookReadView(BSModalReadView):
        model = Book
        template_name = 'examples/read_book.html'

    # Delete
    class BookDeleteView(BSModalDeleteView):
        model = Book
        template_name = 'examples/delete_book.html'
        success_message = 'Success: Book was deleted.'
        success_url = reverse_lazy('index')

.. code-block:: python

    urls.py

    from django.urls import path
    from books import views

    urlpatterns = [
        path('', views.Index.as_view(), name='index'),
        path('create/', views.BookCreateView.as_view(), name='create_book'),
        path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
        path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
        path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_book')
    ]

.. code-block:: html

    .html file containing modal, trigger elements and script instantiating modalForms

    <!-- Modal 1 with id="create-book"-->
    <div class="modal fade" id="create-modal" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
        </div>
      </div>
    </div>

    <!-- Modal 2 with id="modal" -->
    <div class="modal fade" tabindex="-1" role="dialog" id="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content"></div>
      </div>
    </div>

    <!-- Create book button -->
    <button id="create-book" class="btn btn-primary" type="button" name="button">Create book</button>

    {% for book in books %}
        <div class="text-center">
          <!-- Read book buttons -->
          <button type="button" class="read-book bs-modal btn btn-sm btn-primary" data-form-url="{% url 'read_book' book.pk %}">
            <span class="fa fa-eye"></span>
          </button>
          <!-- Update book buttons -->
          <button type="button" class="update-book bs-modal btn btn-sm btn-primary" data-form-url="{% url 'update_book' book.pk %}">
            <span class="fa fa-pencil"></span>
          </button>
          <!-- Delete book buttons -->
          <button type="button" class="delete-book bs-modal btn btn-sm btn-danger" data-form-url="{% url 'delete_book' book.pk %}">
            <span class="fa fa-trash"></span>
          </button>
        </div>
    {% endfor %}

    <script type="text/javascript">
      $(function () {

        // Read book buttons
        $(".read-book").each(function () {
            $(this).modalForm({formURL: $(this).data("form-url")});
        });

        // Delete book buttons - formURL is retrieved from the data of the element
        $(".delete-book").each(function () {
            $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
        });

        // Create book button opens form in modal with id="create-modal"
        $("#create-book").modalForm({
            formURL: "{% url 'create_book' %}",
            modalID: "#create-modal"
        });

      });
    </script>

- See the difference between button triggering Create action and buttons triggering Read, Update and Delete actions.
- Within the for loop in .html file the ``data-form-url`` attribute of each Update, Read and Delete button should be set to relevant URL with pk argument of the object to be updated, read or deleted.
- These ``data-form-url`` URLs should than be set as ``formURLs`` for ``modalForms`` bound to the buttons.

Example 4: Django's forms.Form in Bootstrap modal
*************************************************

For explanation how all the parts of the code work together see paragraph **Usage**. To test the working solution presented here clone and run **Examples**.

.. code-block:: python

    forms.py

    from bootstrap_modal_forms.forms import BSModalForm

    class BookFilterForm(BSModalForm):
        type = forms.ChoiceField(choices=Book.BOOK_TYPES)

        class Meta:
            fields = ['type']

.. code-block:: html

    filter_book.html

    {% load widget_tweaks %}

    <form method="post" action="">
      {% csrf_token %}

      <div class="modal-header">
        <h3 class="modal-title">Filter Books</h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        <div class="{% if form.non_field_errors %}invalid{% endif %} mb-2">
          {% for error in form.non_field_errors %}
            {{ error }}
          {% endfor %}
        </div>

        {% for field in form %}
          <div class="form-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {% render_field field class="form-control" placeholder=field.label %}
            <div class="{% if field.errors %} invalid{% endif %}">
              {% for error in field.errors %}
                <p class="help-block">{{ error }}</p>
              {% endfor %}
            </div>
          </div>
        {% endfor %}
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Filter</button>
      </div>

    </form>

.. code-block:: python

    views.py

    class BookFilterView(BSModalFormView):
        template_name = 'examples/filter_book.html'
        form_class = BookFilterForm

        def form_valid(self, form):
            self.filter = '?type=' + form.cleaned_data['type']
            response = super().form_valid(form)
            return response

        def get_success_url(self):
            return reverse_lazy('index') + self.filter

.. code-block:: python

    urls.py

    from django.urls import path
    from . import views

    app_name = 'accounts'
    urlpatterns = [
        path('filter/', views.BookFilterView.as_view(), name='filter_book'),
    ]

.. code-block:: html

    index.html
      
      ...
      <button id="filter-book" class="filter-book btn btn-primary" type="button" name="button" data-form-url="{% url 'filter_book' %}">
        <span class="fa fa-filter mr-2"></span>Filter books
      </button>
      ...

      <script type="text/javascript">
        $(function () {
          ...
          $("#filter-book").each(function () {
              $(this).modalForm({formURL: $(this).data('form-url')});
          });
          ...
        });
      </script>

Contribute
==========

This is an Open Source project and any contribution is appreciated.

License
=======

This project is licensed under the MIT License.
