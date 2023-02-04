import pdb
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


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

    def select_region(self, target_region):
        area_lists = self.find_element(By.ID, "js-areamap_monthly_background")
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
        real_estate_btns = self.find_elements(
            By.CSS_SELECTOR, "[class*='ui-btn ui-btn--base areamenu-btn']"
        )
        for btn in real_estate_btns:
            if btn.text == target_real_estate:
                btn.click()
                time.sleep(2)
                break

    def select_area_or_line(self, target_map, way):
        # TODO:wayの入力値を使って直接エリアか沿線を詮索できた方がいい？
        areamap_field = self.find_element(By.CSS_SELECTOR, "[class='areamap-field']")

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
            # TODO:対象コードがない場合の処理を追加する
            try:
                checkbox = self.find_element(By.ID, f"la{code}")
                self.execute_script("arguments[0].click();", checkbox)
                time.sleep(1)
            # 対象の行政区コードに対象物件が存在しない場合は次のコードへ行く
            # TODO:NoSuchElementExceptionの発生までに時間がかかるので、最初に存在する行政区コードを集計した方がいいかもしれない
            except NoSuchElementException as e:
                continue

        search_btn = self.find_element(
            By.CSS_SELECTOR,
            "[class='ui-btn ui-btn--search btn--large js-shikugunSearchBtn']",
        )
        self.execute_script("arguments[0].click();", search_btn)

        time.sleep(5)

    # select_boxは処理できないためエラーになるので、分岐させる必要がある
    def select_other_conditions(self, condition, select_labels: list):
        other_conditions = self.find_elements(
            By.CSS_SELECTOR, "[class='l-refinetable > table > tbody > tr']"
        )
        for condition_box in other_conditions:
            th = condition_box.find_element(By.CSS_SELECTOR, "th").text
            if th == condition:
                condition_li_in_box = condition_box.find_elements(By.CSS_SELECTOR, "li")
                break

        if not (condition_li_in_box):
            raise ValueError("not exist condition")

        for li in condition_li_in_box:
            label = li.find_element(By.CSS_SELECTOR, "label").text
            if label in select_labels:
                input_box = li.find_element(By.CSS_SELECTOR, "input")
                self.execute_script("arguments[0].click();", input_box)
                select_labels.remove(label)
