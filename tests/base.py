from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from setup import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class FunctionalTest(StaticLiveServerTestCase):
    """
    Download your driver of choice, copy & paste it into the root directory of this project and change
    the `BROWSER_DRIVER_PATH` variable to your downloaded driver file.

    FireFox
        - Driver Download: https://github.com/mozilla/geckodriver/releases
        - Compatibility: https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html
    Chrome
        - Driver Download: https://chromedriver.chromium.org/downloads
        - Compatibility: https://chromedriver.chromium.org/downloads/version-selection
    Edge (May also work with preinstalled version. Just try it. If it works, you're good. If not, download the files.)
        - Driver Download: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
        - Compatibility: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    Safari (May also work with preinstalled version. Just try it. If it works, you're good. If not, download the files.)
        - Driver Download: https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari
        - Compatibility: https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari
    """

    BROWSER = None
    # Change this, to your browser type of choice
    BROWSER_TYPE = webdriver.Chrome
    # Change this, to your driver file of your chosen browser
    BROWSER_DRIVER_PATH: Path = Path(settings.BASE_DIR, 'chromedriver')
    # If you're using Firefox, and you have installed firefox in a none-standard directory, change this to the executable wherever
    # you have installed Firefox. E.g.: Path('C:/My/None/Standard/directory/firefox.exe')
    FIRE_FOX_BINARY = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BROWSER = cls.get_browser()
        # cls.BROWSER.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.BROWSER.quit()
        super().tearDownClass()

    @classmethod
    def get_browser(cls):
        if cls.BROWSER_TYPE is webdriver.Firefox:
            if cls.BROWSER_DRIVER_PATH is None:
                raise ValueError('Firefox needs a path to a browser driver file!')
            else:
                if cls.FIRE_FOX_BINARY is None:
                    return webdriver.Firefox(executable_path=cls.BROWSER_DRIVER_PATH)
                else:
                    return webdriver.Firefox(firefox_binary=str(cls.FIRE_FOX_BINARY), executable_path=cls.BROWSER_DRIVER_PATH)
        elif cls.BROWSER_TYPE is webdriver.Chrome:
            if cls.BROWSER_DRIVER_PATH is None:
                raise ValueError('Chrome needs a path to a browser driver file!')
            else:
                return webdriver.Chrome(executable_path=cls.BROWSER_DRIVER_PATH)
        elif cls.BROWSER_TYPE is webdriver.Edge:
            if cls.BROWSER_DRIVER_PATH is None:
                return webdriver.Edge()
            else:
                return webdriver.Edge(executable_path=cls.BROWSER_DRIVER_PATH)
        elif cls.BROWSER_TYPE is webdriver.Safari:
            if cls.BROWSER_DRIVER_PATH is None:
                return webdriver.Safari()
            else:
                return webdriver.Safari(executable_path=cls.BROWSER_DRIVER_PATH)
        else:
            raise RuntimeError(f'Unsupported browser type: {cls.BROWSER_TYPE}')

    def wait_for(self, class_name=None, element_id=None, tag=None, xpath=None):
        return WebDriverWait(self.BROWSER, 20).until(
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
