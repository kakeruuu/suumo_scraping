import pdb
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.process.bot.scraping.select_conditions import SelectConditions


class Scraper(webdriver.Chrome):
    def __init__(self, default_dl_path=""):
        self.driver_path = ChromeDriverManager().install()
        self.default_dl_path = default_dl_path
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        if not self.default_dl_path == "":
            options.add_experimental_option(
                "prefs", {"download.default_directory": self.default_dl_path}
            )
        super(Scraper, self).__init__(executable_path=self.driver_path, options=options)
        self.implicitly_wait(15)
        self.set_script_timeout(5)
        # self.waitng = Waiting(self)

    def __exit__(self, exc_type, exc, traceback):
        self.quit()

    def land_first_page(self, url):
        self.get(url)
        # self.waitng.wait_main_loaded()

    def go_to_property_list(self, conditions):
        select_conditions = SelectConditions(self)
        select_conditions.select_region()
        select_conditions.select_real_estate()
        select_conditions.select_area_or_line()
        select_conditions.select_city()
        select_conditions.select_other_conditions()
