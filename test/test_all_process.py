import pdb

from constants import first_page_url, main_conditions, other_conditions

from model.conditions import Conditions
from modules.list2csv import list2csv
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
            delete_cols = [0, 15, 16, 17, 18, 19]
            list2csv(results, delete_cols=delete_cols)

            return "success"

    except Exception as e:
        print(e)
