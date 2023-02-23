import pdb
import time

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ScrapeProperties:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.waitng = WebDriverWait(self.driver, 15)

    def page_is_loaded(self):
        is_loaded = (
            self.driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)
        return is_loaded

    def manage_scrape_property_list(self):
        all_data = []
        while True:
            pdb.set_trace()
            soup = BeautifulSoup(self.driver.page_source, "lxml")

            # 物件リストを取得
            property_li = soup.select("[class='cassetteitem']")

            # 物件リストから一つの要素を取得
            for li in property_li:

                property_data = self.obtain_property_info(li)

                dwelling_unit_data = self.obtain_dwelling_unit_info(li)

                data = [property_data + r for r in dwelling_unit_data]

                all_data.extend(data)

            pdb.set_trace()
            if self.is_last_page():
                return "success"

            self.click_next_page()

    def is_last_page(self) -> bool:
        paginations = self.driver.find_element(
            By.CSS_SELECTOR, "[class='pagination pagination_set-nav']"
        )
        if "次へ" in paginations.text:
            return False

        return True

    def click_next_page(self):
        next_button_css = "#js-leftColumnForm > div.pagination_set > div.pagination.pagination_set-nav > p > a"
        self.driver.find_element(By.CSS_SELECTOR, next_button_css).click()
        self.waitng.until(lambda x: self.page_is_loaded())

    def obtain_property_info(self, li: Tag) -> list[list[str]]:
        # 取得した一つの物件要素から、物件詳細を取得
        details = li.select_one("[class='cassetteitem_content']")
        details = details.text.split("\n")
        return details

    def obtain_dwelling_unit_info(self, li: Tag) -> list[list[str]]:
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
