from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from model.cities import City
from model.city_group import CityGroup
from model.conditions import Conditions
from model.prefecture import Prefecture
from model.region import Region
from model.setting import get_db
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


@app.post("/test")
async def test(request: Request):
    data = await request.json()
    conditions = Conditions(**data)
    print(conditions)


@app.get("/scrape")
async def execute_scraping(request: Request):
    data = await request.json()
    conditions = Conditions(**data)
    with Scraper(default_dl_path="") as bot:
        bot.land_first_page("https://suumo.jp/")
        bot.go_to_property_list(conditions=conditions)
        results = bot.scrape_properties()
        delete_cols = [0, 15, 16, 17, 18, 19]
        list2csv(results, delete_cols=delete_cols)
        return "success"


@app.get("/read_region")
def read_region(db: Session = Depends(get_db)):
    region = Region()
    data = [e.as_dict() for e in region.read_region_all(db)]
    return JSONResponse(content=data)


@app.get("/read_prefecture")
def read_prefecture_by_region_id(region_id, db: Session = Depends(get_db)):
    prefecture = Prefecture()
    data = [e.as_dict() for e in prefecture.read_by_region_id(db, region_id)]
    return JSONResponse(content=data)


@app.get("/read_city_group")
def read_city_group_by_prefecture_id(prefecture_id, db: Session = Depends(get_db)):
    city_group = CityGroup()
    data = [e.as_dict() for e in city_group.read_by_prefecture_id(db, prefecture_id)]
    return JSONResponse(content=data)


@app.get("/read_city")
def read_city_by_group_id(group_id, db: Session = Depends(get_db)):
    city = City()
    data = [e.as_dict() for e in city.read_by_group_id(db, group_id)]
    return JSONResponse(content=data)


@app.get("/read_other_condtions")
def read_other_condtions():
    data = {
        "間取り": [
            "ワンルーム",
            "1K",
            "1DK",
            "1LDK",
            "2K",
            "2DK",
            "2LDK",
            "3K",
            "3DK",
            "3LDK",
            "4K",
            "4DK",
            "4LDK",
            "5K以上",
        ],
        "建物種別": ["マンション", "アパート", "一戸建て・その他"],
    }
    return JSONResponse(content=data)


"""
TODO:
- ここまでやるならPydanticも導入したいかも
- スクレイピング実行エンドポイントをPostに変更する
- 非同期処理を追加する
- 各ormクラスを一括でimportできるように変更する
- returnの値をjson形式にするべきでは？
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
