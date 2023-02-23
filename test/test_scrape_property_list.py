import pdb

from model.conditions import Conditions
from process.bot.scraping.scraper import Scraper


def test_scrape_property_list():
    url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&cb=0.0&ct=9999999&et=9999999&md=01&md=02&ts=1&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2="

    with Scraper(default_dl_path="") as bot:
        bot.land_first_page(url)
        bot.manage_scrape_property_list()
        return "success"


if __name__ == "__main__":
    test_scrape_property_list()
