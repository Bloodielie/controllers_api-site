from hashlib import sha256
from typing import Union

import orm
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: orm.models, password: str):
    # client <class 'models.database.User'>
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_email_verify_postfix(user_name: Union[str, int]) -> str:
    return (sha256(str(user_name).encode()).hexdigest())[:10:2]
