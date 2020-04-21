from typing import Any

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    email: str


class User(UserBase):
    hashed_password: str
    refresh_token: str


class UserAuthIn(BaseModel):
    login: str
    password: str


class UserAuthOut(BaseModel):
    access_token: str
    refresh_token: str


class TokenIn(BaseModel):
    token: str


class TokenOut(BaseModel):
    status: bool


class AccountCreateIn(BaseModel):
    login: str
    email: str
    password: str


class RefreshTokenIn(BaseModel):
    refresh_token: str


class RefreshPasswordIn(BaseModel):
    login: str
    old_password: str
    new_password: str


class AddBusStop(BaseModel):
    bus_stop_name: str
    city: str
    type_bus_stop: str


class Profile(BaseModel):
    user_name: str
    create_at: Any
    add_bus_stop_time: Any
    email_activatet: bool
    email: str
