from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union

from app.configuration.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

import jwt
from jwt import PyJWTError

from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param

from starlette.requests import Request
from starlette.responses import Response

from app.user.models import User
import orm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_cookie(response: Response, token: str, max_age: int) -> None:
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=max_age,
        expires=max_age,
    )


def cookie_check(request: Request) -> Union[str, None]:
    cookie_authorization: str = request.cookies.get("Authorization")

    cookie_scheme, cookie_param = get_authorization_scheme_param(
        cookie_authorization
    )

    if cookie_scheme.lower() == "bearer":
        authorization = True
        scheme = cookie_scheme
        param = cookie_param
    else:
        authorization = False

    if not authorization or scheme.lower() != "bearer":
        return None
    return param


async def get_current_user(token=Depends(cookie_check)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except PyJWTError:
        return None
    try:
        user = await User.objects.get(user_name=username)
    except orm.exceptions.NoMatch:
        return None
    return user


def authorization_check(request: Request) -> Union[str, None]:
    authorization: str = request.cookies.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() == "basic":
        return None
    return param


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(user: orm.models, password: str):
    # user <class 'models.database.User'>
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, minute: int = None) -> bytes:
    to_encode = data.copy()
    if minute:
        expire = datetime.utcnow() + timedelta(minutes=minute)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
