from typing import Union, Any
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
    async def get_user(cls, parameter: str, value: Any) -> Union[User, None]:
        argument = {parameter: value}
        user = await cls.model.objects.filter(**argument).all()
        if user:
            return user[0]
        return None

    @classmethod
    async def get_two_model(cls, first_model: User):
        pk: int = first_model.user_info.pk
        two_model = await cls.model_info.objects.filter(id=pk).all()
        if two_model:
            return two_model[0]
        return None

    @classmethod
    async def is_user_exists(cls, email: str, user_name: str) -> bool:
        name = await cls.get_user('user_name', user_name)
        email = await cls.get_user('email', email)
        if not name and not email:
            return False
        return True
