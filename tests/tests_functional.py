from selenium.webdriver.support.select import Select

from examples.models import Book
from .base import FunctionalTest


class SignUpLoginTest(FunctionalTest):
    def test_signup_login(self):
        # User visits homepage and checks the content
        self.browser.get(self.live_server_url)
        self.assertIn('django-bootstrap-modal-forms', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('django-bootstrap-modal-forms', header_text)

        # User clicks Sign up button
        self.browser.find_element_by_id('signup-btn').click()

        # Sign up modal opens
        modal = self.wait_for(element_id='modal')

        # User fills in and submits sign up form with misspelled second password
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        password1_field = form.find_element_by_id('id_password1')
        password2_field = form.find_element_by_id('id_password2')
        username_field.send_keys('user')
        password1_field.send_keys('pass12345')
        password2_field.send_keys('wrong12345')
        form.submit()

        # User sees error in form
        error = self.wait_for(class_name='help-block')
        self.assertEqual(error.text, 'The two password fields didn’t match.')

        # User fills in and submits sign up form correctly
        form = modal.find_element_by_tag_name('form')
        password1_field = form.find_element_by_id('id_password1')
        password2_field = form.find_element_by_id('id_password2')
        password1_field.send_keys('pass12345')
        password2_field.send_keys('pass12345')
        form.submit()

        # User sees success message after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')
        # Slice removes '\nx' since alert is dismissible and contains 'times' button
        success_msg = self.wait_for(class_name='alert').text[:-2]
        self.assertEqual(success_msg, 'Success: Sign up succeeded. You can now Log in.')

        # User clicks log in button
        self.browser.find_element_by_id('login-btn').click()

        # Log in modal opens
        modal = self.wait_for(element_id='modal')

        # User fills in and submits log in form with misspelled username
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        password_field = form.find_element_by_id('id_password')
        username_field.send_keys('wrong')
        password_field.send_keys('pass12345')
        form.submit()

        # User sees error in form
        error = self.wait_for(class_name='invalid').text
        self.assertEqual(
            error,
            'Please enter a correct username and password. Note that both fields may be case-sensitive.',
        )

        # User fills in and submits log in form correctly
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        username_field.clear()
        password_field = form.find_element_by_id('id_password')
        username_field.send_keys('user')
        password_field.send_keys('pass12345')
        form.submit()

        # User sees log out button after page redirection
        logout_btn_txt = self.wait_for(element_id='logout-btn').text
        self.assertEqual(logout_btn_txt, 'Log out')
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')


class CRUDActionsTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.book = Book.objects.create(
            title='Life of John Doe',
            publication_date='2017-02-02',
            author='John Doe',
            price=19,
            pages=477,
            book_type=1,
        )

    def test_create_object(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User clicks create book button
        self.browser.find_element_by_id('create-book-sync').click()

        # Create book modal opens
        modal = self.wait_for(element_id='create-modal')

        # User fills in and submits the form with wrong date format
        form = self.wait_for(tag='form')

        title_field = form.find_element_by_id('id_title')
        publication_date_field = form.find_element_by_id('id_publication_date')
        author_field = form.find_element_by_id('id_author')
        price_field = form.find_element_by_id('id_price')
        pages_field = form.find_element_by_id('id_pages')
        book_type = form.find_element_by_id('id_book_type')
        book_type_select = Select(book_type)

        title_field.send_keys('Life of Jane Doe')
        publication_date_field.send_keys('01.01.2019')
        author_field.send_keys('Jane Doe')
        price_field.send_keys(21)
        pages_field.send_keys(464)
        book_type_select.select_by_index(1)

        form.submit()

        # User sees error in form
        error = self.wait_for(class_name='help-block').text
        self.assertEqual(error, 'Enter a valid date in YYYY-MM-DD format.')

        # User corrects the date and submits the form
        form = modal.find_element_by_tag_name('form')
        
        publication_date_field = form.find_element_by_id('id_publication_date')
        publication_date_field.clear()
        publication_date_field.send_keys('2019-01-01')
        
        form.submit()

        # User sees success message after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')

        # Slice removes '\nx' since alert is dismissible and contains 'times' button
        success_msg = self.wait_for(class_name='alert').text[:-2]
        self.assertEqual(success_msg, 'Success: Book was created.')

        # User sees created book in table
        table_entries = self.wait_for_table_rows()
        self.assertEqual(len(table_entries), 2)

        # Check content of second table entry
        self.check_table_row(
            table_entries[1],
            7,
            ['Life of Jane Doe', 'Jane Doe', 'Hardcover', 'Jan. 1, 2019', '464', '21.00', None],
        )

    def test_filter_object(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User clicks filter book button
        self.wait_for(element_id='filter-book').click()

        # Update filter modal opens
        modal = self.wait_for(element_id='modal')

        # User changes book type
        form = modal.find_element_by_tag_name('form')   
        
        book_type = self.browser.find_element_by_id("id_type")
        book_type_select = Select(book_type)
        book_type_select.select_by_index(0)

        form.submit()

        # User is redirected to the homepage with a querystring with the filter
        self.wait_for(class_name='filtered-books')
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/?type=1$')

    def test_update_object(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User clicks update book button
        self.browser.find_element_by_class_name('update-book').click()

        # Update book modal opens
        modal = self.wait_for(element_id='modal')

        # User changes price and book type
        form = modal.find_element_by_tag_name('form')
        
        title_field = form.find_element_by_id('id_title')
        title_field.clear()
        book_type = form.find_element_by_id('id_book_type')
        book_type_select = Select(book_type)

        title_field.send_keys('Life of Jane and John Doe')
        book_type_select.select_by_index(2)

        form.submit()

        # User sees success message after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')

        # Slice removes '\nx' since alert is dismissible and contains 'times' button
        success_msg = self.wait_for(class_name='alert').text[:-2]
        self.assertEqual(success_msg, 'Success: Book was updated.')

        # User sees updated book in table
        table_entries = self.wait_for_table_rows()
        self.assertEqual(len(table_entries), 1)

        # Check content of first table entry
        self.check_table_row(
            table_entries[0],
            7,
            [
                'Life of Jane and John Doe',
                'John Doe',
                'Paperback',
                'Feb. 2, 2017',
                '477',
                '19.00',
                None,
            ],
        )

    def test_read_object(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User clicks Read book button
        self.browser.find_element_by_class_name('read-book').click()

        # Read book modal opens
        modal = self.wait_for(element_id='modal')

        # User sees book content
        modal_body = modal.find_element_by_class_name('modal-body')
        divs = modal_body.find_elements_by_tag_name('div')
        self.assertEqual(divs[0].text, 'Title: Life of John Doe')
        self.assertEqual(divs[1].text, 'Author: John Doe')
        self.assertEqual(divs[2].text, 'Price: 19.00 €')
        self.assertEqual(divs[3].text, 'Pages: 477')
        self.assertEqual(divs[4].text, 'Type: Hardcover')
        self.assertEqual(divs[5].text, 'Publication date: Feb. 2, 2017')

    def test_delete_object(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User clicks Delete book button
        self.browser.find_element_by_class_name('delete-book').click()

        # Delete book modal opens
        modal = self.wait_for(element_id='modal')
        delete_text = modal.find_element_by_class_name('delete-text').text
        self.assertEqual(
            delete_text, 'Are you sure you want to delete book with title Life of John Doe?'
        )

        # User clicks delete button
        delete_btn = modal.find_element_by_id('delete-btn')
        delete_btn.click()

        # User sees success message after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')

        # Slice removes '\nx' since alert is dismissible and contains 'times' button
        alert = self.wait_for(class_name='alert')
        self.assertEqual(alert.text[:-2], 'Success: Book was deleted.')

        # There is no books in database anymore
        books = Book.objects.all()
        self.assertEqual(books.count(), 0)
