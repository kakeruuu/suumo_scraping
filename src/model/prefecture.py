from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from model.setting import Base, engine


class Prefecture(Base):
    __tablename__ = "prefectures"

    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    prefecture_id = Column(Integer, primary_key=True)
    prefecture = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def read_by_region_id(cls, session: Session, region_id):
        """region_idに該当するレコードを取得する"""
        return session.query(cls).filter_by(region_id=region_id).all()
