import pdb
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def go_rental_information():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.implicitly_wait(15)

    url = "https://suumo.jp/"
    driver.get(url=url)
    time.sleep(10)

    ## 地方選択 ##
    area_lists = driver.find_element(By.ID, "js-areamap_monthly_background")
    area_lists_boxes = area_lists.find_elements(By.CSS_SELECTOR, "[class^='areabox ']")
    target_area = "関東"

    for area in area_lists_boxes:
        area_title = area.find_element(By.CLASS_NAME, "areabox-title")
        if area_title.text == target_area:
            area.find_element(By.TAG_NAME, "a").click()
            time.sleep(5)
            break

    ## 賃貸物件選択 ##
    real_estate_btns = driver.find_elements(
        By.CSS_SELECTOR, "[class*='ui-btn ui-btn--base areamenu-btn']"
    )
    target_real_estate = "賃貸物件"
    for btn in real_estate_btns:
        if btn.text == target_real_estate:
            btn.click()
            time.sleep(5)
            break

    ## 沿線・エリア選択機能 ##
    target_map = "東京都"
    in_which_way = "エリア"
    areamap_field = driver.find_element(By.CSS_SELECTOR, "[class='areamap-field']")

    for box in areamap_field.find_elements(By.CSS_SELECTOR, "[class^='areabox ']"):
        map_title = box.find_element(By.CSS_SELECTOR, "[class='areabox-title']").text

        if map_title == target_map:
            li = box.find_elements(By.CSS_SELECTOR, "ul.ui-list--hz > li")
            break

    for l in li:
        if l.text == in_which_way:
            l.find_element(By.CSS_SELECTOR, "a").click()
            time.sleep(5)
            break

    ## 市区郡選択 ##
    # 行政区コードで選択する
    japan_postal_codes = [
        13101,
        13102,
        13103,
        13104,
        13105,
        13106,
        13107,
        13108,
        13109,
        13110,
        13111,
        13112,
        13113,
        13114,
        13115,
        13116,
        13117,
        13118,
        13119,
        13120,
        13121,
        13122,
        13123,
    ]
    # FIX:Selenium.common.exceptions.ElementClickInterceptedException
    for code in japan_postal_codes:
        # TODO:対象コードがない場合の処理を追加する
        driver.find_element(By.ID, f"la{code}").click()
        time.sleep(1)

    driver.find_element(
        By.CSS_SELECTOR,
        "[class='ui-btn ui-btn--search btn--large js-shikugunSearchBtn']",
    ).click()

    time.sleep(5)


if __name__ == "__main__":
    go_rental_information()
