from sqlalchemy import Column, ForeignKey, Integer, String

from model.setting import Base, engine


class Prefecture(Base):
    __tablename__ = "prefectures"

    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    prefecture_id = Column(Integer, primary_key=True)
    prefecture = Column(String, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
