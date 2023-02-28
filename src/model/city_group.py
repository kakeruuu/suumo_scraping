from sqlalchemy import Column, ForeignKey, Integer, String

from model.setting import Base, engine


class CityGroup(Base):
    __tablename__ = "city_groups"

    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    prefecture_id = Column(
        Integer, ForeignKey("prefectures.prefecture_id"), nullable=False
    )
    group_id = Column(Integer, primary_key=True)
    city_group = Column(String, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
