from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    # Basic setUp & tearDown
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, class_name=None, element_id=None, tag=None, xpath=None):
        return WebDriverWait(self.browser, 20).until(
            expected_conditions.element_to_be_clickable
            ((By.ID, element_id) if element_id else
             (By.CLASS_NAME, class_name) if class_name else
             (By.TAG_NAME, tag) if tag else
             (By.XPATH, xpath))
        )

    def wait_for_table_rows(self):
        tbody = self.wait_for(xpath="//table/tbody")
        return tbody.find_elements_by_tag_name('tr')

    def check_table_row(self, table_row, cells_count, cells_values):
        cells = table_row.find_elements_by_tag_name('td')
        # Compare cells count in table row with expected value
        self.assertEqual(len(cells), cells_count)
        # Compare content of cells in table row with expected values
        for i in range(len(cells_values)):
            if cells_values[i] is not None:
                self.assertEqual(cells[i].text, cells_values[i])
