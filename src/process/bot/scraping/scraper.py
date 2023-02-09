import pdb
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from model.conditions import Conditions
from process.bot.scraping.select_conditions import SelectConditions


class Scraper(webdriver.Chrome):
    def __init__(self, default_dl_path="", is_headless=False):
        self.driver_path = ChromeDriverManager().install()
        self.default_dl_path = default_dl_path
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless")
        if not self.default_dl_path == "":
            options.add_experimental_option(
                "prefs", {"download.default_directory": self.default_dl_path}
            )
        super(Scraper, self).__init__(executable_path=self.driver_path, options=options)
        self.implicitly_wait(15)
        self.set_script_timeout(5)
        self.waitng = WebDriverWait(self, 15)

    def __exit__(self, exc_type, exc, traceback):
        self.quit()

    def page_is_loaded(self):
        is_loaded = self.execute_script("return document.readyState") == "complete"
        time.sleep(2)
        return is_loaded

    def land_first_page(self, url):
        self.get(url)
        self.waitng.until(lambda x: self.page_is_loaded())

    def go_to_property_list(self, conditions: Conditions):
        select_conditions = SelectConditions(self)
        select_conditions.select_region(conditions.region)
        select_conditions.select_real_estate(conditions.real_estate)
        select_conditions.select_area_or_line(conditions.map, conditions.way)
        select_conditions.select_city(conditions.city_codes)
        select_conditions.select_other_conditions(conditions.other_condtions)
