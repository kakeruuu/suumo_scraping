from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from model.setting import Base


class Region(Base):
    __tablename__ = "regions"

    region_id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def read_region_all(cls, session: Session):
        return session.query(cls).all()
