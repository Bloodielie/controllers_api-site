from typing import Union
import orm
from .models import User, UserInfo
from datetime import datetime


class UserRepository:
    model: orm.Model = User
    model_info: orm.Model = UserInfo

    @classmethod
    async def create_user(cls, user: User) -> None:
        user_info = await cls.model_info.objects.create(user_name=user.user_name, create_at=datetime.now())
        return await cls.model.objects.create(user_name=user.user_name, email=user.email, hashed_password=user.hashed_password,
                                              user_info=user_info)

    @classmethod
    async def get_user_by_email(cls, email: str) -> Union[None, dict]:
        try:
            return await cls.model.objects.get(email=email)
        except orm.exceptions.NoMatch:
            return None

    @classmethod
    async def get_user_by_name(cls, user_name: str) -> Union[None, dict]:
        try:
            return await cls.model.objects.get(user_name=user_name)
        except orm.exceptions.NoMatch:
            return None

    @classmethod
    async def get_user_id(cls, id: int) -> Union[None, dict]:
        try:
            return await cls.model.objects.get(id=id)
        except orm.exceptions.NoMatch:
            return None

    @classmethod
    async def get_two_model(cls, pk: int):
        try:
            return await cls.model_info.objects.get(id=pk)
        except orm.exceptions.NoMatch:
            return None

    @classmethod
    async def is_user_exists(cls, email: str, user_name: str) -> bool:
        name = await cls.get_user_by_name(user_name)
        email = await cls.get_user_by_email(email)
        if not name and not email:
            return False
        return True
