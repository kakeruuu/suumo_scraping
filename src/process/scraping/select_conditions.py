import pdb
import re
import time

from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SelectConditions:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.waitng = WebDriverWait(self.driver, 15)

    def page_is_loaded(self):
        is_loaded = (
            self.driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)
        return is_loaded

    def select_region(self, target_region):
        area_lists = self.driver.find_element(By.ID, "js-areamap_monthly_background")
        area_lists_boxes = area_lists.find_elements(
            By.CSS_SELECTOR, "[class^='areabox ']"
        )

        for area in area_lists_boxes:
            area_title = area.find_element(By.CLASS_NAME, "areabox-title")
            if area_title.text == target_region:
                area.find_element(By.TAG_NAME, "a").click()
                self.waitng.until(lambda x: self.page_is_loaded())
                break

    def select_real_estate(self, target_real_estate):
        real_estate_btns = self.driver.find_elements(
            By.CSS_SELECTOR, "[class*='ui-btn ui-btn--base areamenu-btn']"
        )
        for btn in real_estate_btns:
            if btn.text == target_real_estate:
                btn.click()
                self.waitng.until(lambda x: self.page_is_loaded())
                break

    def select_area_or_line(self, target_prefecture, way):
        areamap_field = self.driver.find_element(
            By.CSS_SELECTOR, "[class='areamap-field']"
        )

        for box in areamap_field.find_elements(By.CSS_SELECTOR, "dl"):
            map_title = box.find_element(
                By.CSS_SELECTOR, "[class='areabox-title']"
            ).text

            if map_title == target_prefecture:
                li = box.find_elements(By.CSS_SELECTOR, "ul.ui-list--hz > li")
                break

        if not li:
            raise ValueError("not exist target_map")

        for l in li:
            if l.text == way:
                l.find_element(By.CSS_SELECTOR, "a").click()
                self.waitng.until(lambda x: self.page_is_loaded())
                break

    def select_main_conditions(self, main_conditions: list[str]):
        city_code_table = self.driver.find_element(
            By.CSS_SELECTOR, "[class='searchtable']"
        )

        city_code_check_boxes = city_code_table.find_elements(By.CSS_SELECTOR, "li")
        for check_box_li in city_code_check_boxes:
            label, quantity = check_box_li.text.split("(")
            quantity = int(re.sub("\D", "", quantity))

            if quantity <= 0 or label not in main_conditions:
                continue

            check_box = check_box_li.find_element(By.CSS_SELECTOR, "input")
            self.driver.execute_script("arguments[0].click();", check_box)
            main_conditions.remove(label)
            time.sleep(1)

    def select_other_conditions(self, other_conditions: dict[str, list[str | int]]):
        while other_conditions:
            other_conditions_box = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#js-shiborikomiForm > div > div.ui-section-body > div.l-refinetable > table > tbody > tr",
            )

            for condition_box in other_conditions_box:
                th = condition_box.find_element(By.CSS_SELECTOR, "th").text
                if th in other_conditions:
                    condition_li_in_box = condition_box.find_elements(
                        By.CSS_SELECTOR, "li"
                    )
                    break

            # 永久ループが起きる=other_conditionsに値が存在し続ける=該当するthがない=condition_li_in_boxがない
            # よって、以下の例外を発生させることで回避
            if not (condition_li_in_box):
                raise ValueError("not exist condition")

            for li in condition_li_in_box:
                label = li.find_element(By.CSS_SELECTOR, "label").text
                if label in other_conditions[th]:
                    input_box = li.find_element(By.CSS_SELECTOR, "input")
                    self.driver.execute_script("arguments[0].click();", input_box)
                    other_conditions[th].remove(label)
                    if not other_conditions[th]:
                        break

            del other_conditions[th]

        search_btn = self.driver.find_element(
            By.CSS_SELECTOR,
            "[class='ui-btn ui-btn--search btn--large js-shikugunSearchBtn']",
        )
        self.driver.execute_script("arguments[0].click();", search_btn)

        self.waitng.until(lambda x: self.page_is_loaded())
