import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    # Basic setUp & tearDown
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_text_in_body(self, *args, not_in=None):
        start_time = time.time()
        # Infinite loop
        while True:
            try:
                body = self.browser.find_element_by_tag_name('body')
                body_text = body.text
                # Check that text is in body
                if not not_in:
                    for arg in args:
                        self.assertIn(arg, body_text)
                # Check there is no text in body
                else:
                    for arg in args:
                        self.assertNotIn(arg, body_text)
                return
            except (AssertionError, WebDriverException) as e:
                # Return exception if more than 10s pass
                if time.time() - start_time > MAX_WAIT:
                    raise e
                # Wait for 0.5s and retry
                time.sleep(0.5)

    def wait_for_modal(self):
        start_time = time.time()
        # Infinite loop
        while True:
            try:
                modal = self.browser.find_element_by_class_name('modal')
                return modal
            except (AssertionError, WebDriverException) as e:
                # Return exception if more than 10s pass
                if time.time() - start_time > MAX_WAIT:
                    raise e
                # Wait for 0.5s and retry
                time.sleep(0.5)
