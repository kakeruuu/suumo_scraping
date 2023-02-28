from sqlalchemy import Column, ForeignKey, Integer, String

from model.setting import Base, engine


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    prefecture = Column(String, nullable=False)
    prefecture_id = Column(
        Integer, ForeignKey("prefectures.prefecture_id"), nullable=False
    )
    city_group = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("city_groups.group_id"), nullable=False)
    city = Column(String, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
