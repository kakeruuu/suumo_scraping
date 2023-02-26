from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.list2csv import list2csv
from process.scraping.scraper import Scraper

app = FastAPI()
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/scrape")
def execute_scraping(conditions):
    with Scraper(default_dl_path="") as bot:
        bot.land_first_page("https://suumo.jp/")
        bot.go_to_property_list(conditions=conditions)
        results = bot.scrape_properties()
        delete_cols = [0, 15, 16, 17, 18, 19]
        list2csv(results, delete_cols=delete_cols)
        return "success"
