from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from model.setting import Base, engine


class CityGroup(Base):
    __tablename__ = "city_groups"

    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    prefecture_id = Column(
        Integer, ForeignKey("prefectures.prefecture_id"), nullable=False
    )
    group_id = Column(Integer, primary_key=True)
    city_group = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def read_by_prefecture_id(cls, session: Session, prefecture_id):
        """prefecture_idに該当するレコードを取得する"""
        return session.query(cls).filter_by(prefecture_id=prefecture_id).all()
