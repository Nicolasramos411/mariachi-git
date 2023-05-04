from pydantic import BaseModel, conint
from datetime import date
from typing import Optional


class User(BaseModel):
    name: str
    phone: conint(gt=0, lt=156997143268)
    points: Optional[int] = 0
    status: Optional[str] = "Vivo"
    last_modified: Optional[date] = date.today()
    created_at: Optional[date] = date.today()
    house_id: Optional[int] = 0

    class Config:
        orm_mode = True


class AddPoints(BaseModel):
    phone: int
    points: int

    class Config:
        orm_mode = True


class RegisterUser(BaseModel):
    name: str
    phone: int
    house_name: str
    house_id: Optional[int] = -1

    class Config:
        orm_mode = True


class House(BaseModel):
    name: str
    points: Optional[int] = 0
    last_modified: Optional[date] = date.today()
    created_at: Optional[date] = date.today()

    class Config:
        orm_mode = True
