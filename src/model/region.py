from sqlalchemy import Column, Integer, String

from model.setting import Base, engine


class Region(Base):
    __tablename__ = "regions"

    region_id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
