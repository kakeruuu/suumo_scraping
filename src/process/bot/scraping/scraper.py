import pdb
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
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

    def manage_scrape_property_list(self):
        try:
            pdb.set_trace()
            easy_db = DataFrames()
            property_list = self.find_element(By.ID, "js-bukkenList")
            property_groups = property_list.find_elements(
                By.CSS_SELECTOR, "[class='l-cassetteitem']"
            )

            for group in property_groups:
                property_li = group.find_elements(
                    By.CSS_SELECTOR, "[class='cassetteitem']"
                )
                for li in property_li:
                    # 物件詳細の取得
                    title = li.find_element(
                        By.CSS_SELECTOR, "[class='cassetteitem_content-title']"
                    ).text
                    # MEMO:以下の物件詳細は駅からの徒歩分数データが必ず3つである前提になっている
                    # なので、データ数が前後する可能性を考慮して取得する方が良い？
                    details = li.find_element(
                        By.CSS_SELECTOR, "[class='cassetteitem_detail']"
                    ).text.split("\n")

                    details.insert(0, title)
                    # 住戸情報の取得
                    dwelling_units = li.find_elements(
                        By.CSS_SELECTOR, "[class='js-cassette_link']"
                    )

                    tbody_data = []
                    for tr in dwelling_units:
                        tds = tr.find_elements(By.CSS_SELECTOR, "td")
                        row_data = details + [td.text for td in tds]
                        tbody_data.append(row_data)

                    easy_db.add_df(tbody_data)

            pdb.set_trace()
            next_button_css = "#js-leftColumnForm > div.pagination_set > div.pagination.pagination_set-nav > p > a"
            self.find_element(By.CSS_SELECTOR, next_button_css).click()
            self.waitng.until(lambda x: self.page_is_loaded())

            # TODO:１ページごとに繰り返す処理を追加。
            # TODO:１ページごとの処理時間の改善

        except Exception as e:
            print(traceback.format_exc())
