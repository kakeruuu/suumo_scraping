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


if __name__ == "__main__":
    go_rental_information()
