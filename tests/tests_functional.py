from .base import FunctionalTest


class SignUpLoginTest(FunctionalTest):

    def test_signup_login(self):
        # User visits homepage and checks the content
        self.browser.get(self.live_server_url)
        self.assertIn('django-bootstrap-modal-forms', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('django-bootstrap-modal-forms', header_text)

        # User clicks Sign up button
        self.browser.find_element_by_class_name('signup-btn').click()

        # Sign up modal opens
        modal = self.wait_for_modal()
        # User fills in and submits sign up form with misspelled second password
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        password1_field = form.find_element_by_id('id_password1')
        password2_field = form.find_element_by_id('id_password2')
        username_field.send_keys('user')
        password1_field.send_keys('pass12345')
        password2_field.send_keys('wrong12345')
        signup_btn = modal.find_element_by_class_name('submit-btn')
        signup_btn.click()

        # User sees error in form after modal refreshes
        error = modal.find_element_by_class_name('help-block').text
        self.assertEqual(error, 'The two password fields didn\'t match.')

        # User fills in and submits signup form correctly
        form = modal.find_element_by_tag_name('form')
        password1_field = form.find_element_by_id('id_password1')
        password2_field = form.find_element_by_id('id_password2')
        password1_field.send_keys('pass12345')
        password2_field.send_keys('pass12345')
        signup_btn = modal.find_element_by_class_name('submit-btn')
        signup_btn.click()

        # User sees success message after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')
        # Slice removes '\nx' since alert is dismissible and contains 'times' button
        success_msg = self.browser.find_element_by_class_name('alert').text[:-2]
        self.assertEqual(
            success_msg,
            'Success: Sign up succeeded. You can now Log in.'
        )

        # User click Log in button
        self.browser.find_element_by_class_name('login-btn').click()

        # Log in modal opens
        modal = self.wait_for_modal()
        # User fills in and submits log in form with misspelled username
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        password_field = form.find_element_by_id('id_password')
        username_field.send_keys('wrong')
        password_field.send_keys('pass12345')
        login_btn = modal.find_element_by_class_name('submit-btn')
        login_btn.click()

        # User sees error in form after modal refreshes
        error = modal.find_element_by_class_name('invalid').text
        self.assertEqual(
            error,
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'
        )

        # User fills in and submits login form correctly
        form = modal.find_element_by_tag_name('form')
        username_field = form.find_element_by_id('id_username')
        username_field.clear()
        password_field = form.find_element_by_id('id_password')
        username_field.send_keys('user')
        password_field.send_keys('pass12345')
        login_btn = modal.find_element_by_class_name('submit-btn')
        login_btn.click()

        # User sees logout button after page redirection
        redirect_url = self.browser.current_url
        self.assertRegex(redirect_url, '/')
        logout_btn_txt = self.browser.find_element_by_class_name('logout-btn').text
        self.assertEqual(logout_btn_txt, 'Log out')


class CreateObjectTest(FunctionalTest):
    pass


class UpdateObjectTest(FunctionalTest):
    pass


class ReadObjectTest(FunctionalTest):
    pass


class DeleteObjectTest(FunctionalTest):
    pass
