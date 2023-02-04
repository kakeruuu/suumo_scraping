import traceback

from process.bot.scraping.scraper import Scraper


# TODO:Select処理に必要な引数をどのように持ってくるか別途考える
def run_bot(default_dl_path):
    url = "https://suumo.jp/"
    try:
        with Scraper(default_dl_path=default_dl_path) as bot:
            bot.land_first_page(url)
            bot.select_region(target_region="")
            bot.select_real_estate(target_real_estate="")
            bot.select_area_or_line(target_map="", way="")
            bot.select_city(city_codes="")

        return "success"

    except Exception as e:
        print(e)
        return traceback.format_exc()
