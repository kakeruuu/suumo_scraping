from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def read_by_group_id(cls, session: Session, group_id):
        """group_idに該当するレコードを取得する"""
        return session.query(cls).filter_by(group_id=group_id).all()
