from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class GameBase(BaseModel):
    name: str
    min_players: int
    max_players: int


class Game(GameBase):
    class Config:
        orm_mode = True


class AvailabilityBase(BaseModel):
    time_avail: datetime

    class Config:
        orm_mode = True


class Availability(AvailabilityBase):
    class Config:
        orm_mode = True


class AvailabilityCreate(AvailabilityBase):
    user_id: int


class InterestBase(BaseModel):
    user_id: int
    game_id: int


class Interest(InterestBase):
    class Config:
        orm_mode = True


class InterestCreate(InterestBase):
    pass


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    availability: List[Availability] = []
    interest: List[Interest] = []
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class TokenData(BaseModel):
    username: Optional[str] = None
