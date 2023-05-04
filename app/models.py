from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, Date, BigInteger, func


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(BigInteger)
    points = Column(Integer, default=0)
    status = Column(String, default="Vivo")
    last_modified = Column(Date, default=func.current_date())
    created_at = Column(Date, default=func.current_date())
    house_id = Column(Integer)


class House(Base):
    __tablename__ = 'house'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    points = Column(Integer)
    last_modified = Column(Date)
    created_at = Column(Date)
