from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    email: str


class User(UserBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
