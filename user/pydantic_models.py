from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    email: str


class User(UserBase):
    hashed_password: str
