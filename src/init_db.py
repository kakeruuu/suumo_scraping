import os

import pandas as pd
from sqlalchemy import text

from model.cities import City
from model.city_group import CityGroup
from model.prefecture import Prefecture
from model.region import Region
from model.setting import Base, engine, get_db


def init_db():

    gen_db = get_db()
    session = next(gen_db)

    region_df = pd.read_csv("./src/csv/region_table.csv")
    insert_dict = region_df.to_dict(orient="records")
    regions = [Region(**row) for row in insert_dict]
    session.add_all(regions)

    prefecture_df = pd.read_csv("./src/csv/prefecture_table.csv")
    insert_dict = prefecture_df.to_dict(orient="records")
    prefectures = [Prefecture(**row) for row in insert_dict]
    session.add_all(prefectures)

    city_group_df = pd.read_csv("./src/csv/city_group_table.csv")
    insert_dict = city_group_df.to_dict(orient="records")
    city_groups = [CityGroup(**row) for row in insert_dict]
    session.add_all(city_groups)

    city_df = pd.read_csv("./src/csv/city_table.csv")
    insert_dict = city_df.to_dict(orient="records")
    cities = [City(**row) for row in insert_dict]
    session.add_all(cities)

    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    init_db()
