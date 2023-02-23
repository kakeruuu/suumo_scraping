import pdb

from model.conditions import Conditions
from process.bot.scraping.scraper import Scraper


def test_run_bot_to_property_list():
    pdb.set_trace()
    url = "https://suumo.jp/"
    main_conditions = [
        "千代田区",
        "中央区",
        "港区",
        "新宿区",
        "文京区",
        "渋谷区",
        "台東区",
        "墨田区",
        "江東区",
        "荒川区",
        "足立区",
        "葛飾区",
        "江戸川区",
        "品川区",
        "目黒区",
        "大田区",
        "世田谷区",
        "中野区",
        "杉並区",
        "練馬区",
        "豊島区",
        "北区",
        "板橋区",
    ]
    other_conditions = {"間取りタイプ": ["ワンルーム", "1K"], "建物種別": ["マンション"]}
    conditions = Conditions(
        "関東", "賃貸物件", "東京都", "エリア", main_conditions, other_conditions
    )
    try:
        with Scraper(default_dl_path="") as bot:
            bot.land_first_page(url)
            bot.go_to_property_list(conditions=conditions)

            return "success"

    except Exception as e:
        print(e)


if __name__ == "__main__":
    test_run_bot_to_property_list()
