import traceback

from process.bot.scraping_classes.hoge import scraping_classes


def run_bot(default_dl_path):
    try:
        with scraping_classes(default_dl_path=default_dl_path) as bot:
            bot.land_first_page(url)
            bot.login_page(id, password)

        return "success"

    except Exception as e:
        print(e)
        return traceback.format_exc()
