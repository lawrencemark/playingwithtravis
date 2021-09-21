import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class TestClass():
    def setup_class(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)


    def teardown_class(self):
        pass


    def setup_method(self):
        pass

    def teardown_method(self):
        pass # we will add some fancy webhooks and emails here passed on the status of the tests later
    
    def test_enedtoendCapture(self):

        self.driver.get("http://localhost:5000")
        self.driver.set_window_size(1440, 838)
        self.driver.find_element(By.NAME, "addTo").click()
        self.driver.find_element(By.NAME, "addTo").send_keys("Selenium Test Task")
        self.driver.find_element(By.NAME, "description").send_keys("This is a task to be put in a WIP state")
        self.driver.find_element(By.CSS_SELECTOR, "button").click()