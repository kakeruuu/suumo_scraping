import pdb
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class SelectConditions:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def select_region(self, target_region):
        area_lists = self.driver.find_element(By.ID, "js-areamap_monthly_background")
        area_lists_boxes = area_lists.find_elements(
            By.CSS_SELECTOR, "[class^='areabox ']"
        )

        for area in area_lists_boxes:
            area_title = area.find_element(By.CLASS_NAME, "areabox-title")
            if area_title.text == target_region:
                area.find_element(By.TAG_NAME, "a").click()
                time.sleep(5)
                break

    def select_real_estate(self, target_real_estate):
        real_estate_btns = self.driver.find_elements(
            By.CSS_SELECTOR, "[class*='ui-btn ui-btn--base areamenu-btn']"
        )
        for btn in real_estate_btns:
            if btn.text == target_real_estate:
                btn.click()
                time.sleep(2)
                break

    def select_area_or_line(self, target_map, way):
        # TODO:wayの入力値を使って直接エリアか沿線を詮索できた方がいい？
        areamap_field = self.driver.find_element(
            By.CSS_SELECTOR, "[class='areamap-field']"
        )

        for box in areamap_field.find_elements(By.CSS_SELECTOR, "[class^='areabox ']"):
            map_title = box.find_element(
                By.CSS_SELECTOR, "[class='areabox-title']"
            ).text

            if map_title == target_map:
                li = box.find_elements(By.CSS_SELECTOR, "ul.ui-list--hz > li")
                break

        if not (li):
            raise ValueError("not exist target_map")

        for l in li:
            if l.text == way:
                l.find_element(By.CSS_SELECTOR, "a").click()
                time.sleep(5)
                break

    def select_city(self, city_codes):
        for code in city_codes:
            try:
                checkbox = self.driver.find_element(By.ID, f"la{code}")
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(1)
            # 対象の行政区コードに対象物件が存在しない場合は次のコードへ行く
            # TODO:NoSuchElementExceptionの発生までに時間がかかるので、最初に存在する行政区コードを集計した方がいいかもしれない
            except NoSuchElementException as e:
                continue

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
            pdb.set_trace()
            del other_conditions[th]

        search_btn = self.driver.find_element(
            By.CSS_SELECTOR,
            "[class='ui-btn ui-btn--search btn--large js-shikugunSearchBtn']",
        )
        self.driver.execute_script("arguments[0].click();", search_btn)

        time.sleep(5)
