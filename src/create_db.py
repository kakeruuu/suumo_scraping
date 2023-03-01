from model.cities import City
from model.city_group import CityGroup
from model.prefecture import Prefecture
from model.region import Region
from model.setting import *

Base.metadata.create_all(bind=engine)
