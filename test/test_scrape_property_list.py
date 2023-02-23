import pdb

from constants import list_url

from process.bot.scraping.scraper import Scraper


def test_scrape_property_list():
    with Scraper(default_dl_path="") as bot:
        bot.land_first_page(list_url)
        result = bot.scrape_properties()
        return result


if __name__ == "__main__":
    test_scrape_property_list()
