import pdb
import time
import traceback

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from model.conditions import Conditions
from process.bot.scraping.select_conditions import SelectConditions
from utils.df import DataFrames


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
        select_conditions.select_main_conditions(conditions.main_conditions)
        select_conditions.select_other_conditions(conditions.other_condtions)

    # bs4 base
    def manage_scrape_property_list(self):
        try:
            pdb.set_trace()
            all_data = []
            start = time.perf_counter()
            soup = BeautifulSoup(self.page_source, "lxml")

            # 物件リストを取得
            property_li = soup.select("[class='cassetteitem']")

            # 物件リストから一つの要素を取得

            for li in property_li:

                property_data = self.obtain_property_info(li)

                dwelling_unit_data = self.obtain_dwelling_unit(li)

                data = [property_data + r for r in dwelling_unit_data]

                all_data.extend(data)

            end = time.perf_counter()
            print(end - start)
            print(len(all_data))
            pdb.set_trace()
            if self.is_last_page():
                return "success"

            self.click_next_page()

        except Exception as e:
            print(e)

    def is_last_page(self) -> bool:
        paginations = self.find_element(
            By.CSS_SELECTOR, "[class='pagination pagination_set-nav']"
        )
        if "次へ" in paginations.text:
            return False

        return True

    def click_next_page(self):
        next_button_css = "#js-leftColumnForm > div.pagination_set > div.pagination.pagination_set-nav > p > a"
        self.find_element(By.CSS_SELECTOR, next_button_css).click()
        self.waitng.until(lambda x: self.page_is_loaded())

    def obtain_property_info(self, li: Tag) -> list[list[str]]:
        # 取得した一つの物件要素から、物件詳細を取得
        details = li.select_one("[class='cassetteitem_content']")
        details = details.text.split("\n")
        return details

    def obtain_dwelling_unit(self, li: Tag) -> list[list[str]]:
        # 取得した一つの物件要素から、住戸リストを取得
        dwelling_units = li.select("[class='js-cassette_link']")
        tbody_data = []
        # 住戸リストから一つの要素を取得
        for tr in dwelling_units:
            # 一つの住戸要素から、住戸詳細を取得
            tds = tr.select("td")
            row_data = [td.text for td in tds]
            tbody_data.append(row_data)

        return tbody_data
