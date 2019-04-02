from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase

from examples.models import Book


class MixinsTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Life of Jane Doe',
            publication_date='2019-01-01',
            author='Jane Doe',
            price=29.99,
            pages=477,
            book_type=2
        )
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )

    def test_PassRequestMixin_PopRequestMixin(self):
        """
        Test if initial request is attached to the form instance through
        PassRequestMixin and PopRequestMixin.
        """

        # Create object through BSModalCreateView
        response = self.client.get('/create/')
        request_initial = response.wsgi_request
        request_in_form_instance = response.context_data['form'].request

        self.assertEqual(request_initial, request_in_form_instance)

        # Update object through BSModalUpdateView
        response = self.client.post('/update/1')
        request_initial = response.wsgi_request
        request_in_form_instance = response.context_data['form'].request

        self.assertEqual(request_initial, request_in_form_instance)

    def test_CreateUpdateAjaxMixin(self):
        """
        Create object through BSModalCreateView.
        """

        # First post request = ajax request checking if form in view is valid
        response = self.client.post(
            '/create/',
            data={
                'title': 'Life of John Doe',
                'publication_date': '2019-01-01',
                'author': 'John Doe',
                'price': 19.99,
                'pages': 449,
                # Wrong value
                'book_type': 'wrong_value'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Form has errors
        self.assertTrue(response.context_data['form'].errors)
        # No redirection
        self.assertEqual(response.status_code, 200)
        # Object is not created
        books = Book.objects.all()
        self.assertEqual(books.count(), 1)

        # Second post request = non-ajax request creating an object
        response = self.client.post(
            '/create/',
            data={
                'title': 'Life of John Doe',
                'publication_date': '2019-01-01',
                'author': 'John Doe',
                'price': 19.99,
                'pages': 449,
                'book_type': 1
            }
        )

        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        # Object is created
        books = Book.objects.all()
        self.assertEqual(books.count(), 2)

        """
        Update object through BSModalUpdateView.
        """

        # First post request = ajax request checking if form in view is valid
        response = self.client.post(
            '/update/1',
            data={
                'title': 'Life of Jane and John Doe',
                'publication_date': '2019-01-01',
                'author': 'Jane Doe',
                'price': 29.99,
                'pages': 477,
                # Wrong value
                'book_type': 'wrong_value'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Form has errors
        self.assertTrue(response.context_data['form'].errors)
        # No redirection
        self.assertEqual(response.status_code, 200)
        # Object is not update
        book = Book.objects.first()
        self.assertEqual(book.title, 'Life of Jane Doe')

        # Second post request = non-ajax request updating an object
        response = self.client.post(
            '/update/1',
            data={
                'title': 'Life of Jane and John Doe',
                'publication_date': '2019-01-01',
                'author': 'Jane Doe',
                'price': 29.99,
                'pages': 477,
                'book_type': 2
            },
        )

        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        # Object is updated
        book = Book.objects.first()
        self.assertEqual(book.title, 'Life of Jane and John Doe')

    def test_DeleteMessageMixin(self):
        """
        Delete object through BSModalDeleteView.
        """

        # Request to delete view passes message to the response
        response = self.client.post('/delete/1')
        messages = get_messages(response.wsgi_request)
        self.assertEqual(len(messages), 1)

    def test_LoginAjaxMixin(self):
        """
        Login user through BSModalLoginView.
        """

        # First post request = ajax request checking if form in view is valid
        response = self.client.post(
            '/login/',
            data={
                'username': 'user',
                # Wrong value
                'password': 'wrong_password'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Form has errors
        self.assertTrue(response.context_data['form'].errors)
        # No redirection
        self.assertEqual(response.status_code, 200)
        # User is anonymous
        self.assertTrue(response.wsgi_request.user.is_anonymous)

        # Second post request = non-ajax request logging the user in
        response = self.client.post(
            '/login/',
            data={
                'username': 'user',
                'password': 'test1234'
            }
        )

        # Redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        # User is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
