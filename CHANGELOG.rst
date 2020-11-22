=========
Changelog
=========

2.0.1 (2020-11-22)
==================

- fix file uploads by updating form serialization 

2.0.0 (2020-06-28)
==================

- rename BSModalForm to BSModalModelForm supporting Django's forms.ModelForm
- add support for Django's forms.Form with BSModalForm
- add generic view BSModalFormView
- add support for asynchronous page updating after form submission

1.5.0 (2019-11-23)
==================

- disable submitBtn after submission
- add support for multiple modals with unique ids on single page

1.4.4 (2019-09-29)
==================

- add support for Django development versions

1.4.3 (2019-09-15)
==================

- add support for Django>=1.8

1.4.2 (2019-04-15)
==================

- change sync to async when validating form and fix warning: [Deprecation] Synchronous XMLHttpRequest on the main thread

1.4.1 (2019-04-02)
==================

- add functional tests

1.4.0 (2019-03-31)
==================

- add unit tests
- change DeleteAjaxMixin to DeleteMessageMixin

1.3.2 (2019-03-30)
==================

- add generic views BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView, BSModalLoginView
- add form BSModalForm
- update README.rst

1.3.1 (2018-08-31)
==================

- fix deleted release 1.3.0 at pypi

1.3.0 (2018-08-31)
==================

- support Django messages framework
- fix redirection to success_url
- update README.rst

1.2.1 (2018-08-14)
==================

- fix formURL setup after invalid form submission returns errors via Ajax
- update README.rst

1.2.0 (2018-08-12)
==================

- update formURL setup to support a dynamic setup of form's action attribute
- support Django UpdateView
- update README.rst

1.1.0 (2018-08-11)
==================

- fix redirection to success_url
- update README.rst

1.0 (2018-05-28)
================

Initial release.
