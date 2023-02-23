import pdb

from constants import first_page_url, main_conditions, other_conditions

from model.conditions import Conditions
from process.bot.scraping.scraper import Scraper


def test_go_to_property_list():
    pdb.set_trace()

    conditions = Conditions(
        "関東", "賃貸物件", "東京都", "エリア", main_conditions, other_conditions
    )
    try:
        with Scraper(default_dl_path="") as bot:
            bot.land_first_page(first_page_url)
            bot.go_to_property_list(conditions=conditions)

            return "success"

    except Exception as e:
        print(e)


if __name__ == "__main__":
    test_go_to_property_list()
