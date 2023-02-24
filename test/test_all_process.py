import pdb

from constants import first_page_url, main_conditions, other_conditions

from model.conditions import Conditions
from process.bot.scraping.scraper import Scraper


def test_all_process():
    pdb.set_trace()

    conditions = Conditions(
        "関東", "賃貸物件", "東京都", "エリア", main_conditions, other_conditions
    )

    try:
        with Scraper(default_dl_path="") as bot:
            bot.land_first_page(first_page_url)
            bot.go_to_property_list(conditions=conditions)
            results = bot.scrape_properties()

            return results
            # TODO:取得したリストをcsv化して保存する処理を追加する
            # データフレームに直してからCSV化する
            # その場合、CSV化する前に不要な列を削除する必要がある

    except Exception as e:
        print(e)
