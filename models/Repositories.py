from .models import User
from typing import Union
import orm
from .database import User, UserInfo
from datetime import datetime


class UserRepository:
    def __init__(self):
        self.model = User
        self.model_info = UserInfo

    async def create_user(self, user: User) -> None:
        user_info = await self.model_info.objects.create(user_name=user.user_name, create_at=datetime.now())
        return await self.model.objects.create(user_name=user.user_name, email=user.email, hashed_password=user.hashed_password, user_info=user_info)

    async def get_user_by_email(self, email: str) -> Union[None, dict]:
        try:
            return await self.model.objects.get(email=email)
        except orm.exceptions.NoMatch:
            return None

    async def get_user_by_name(self, user_name: str) -> Union[None, dict]:
        try:
            return await self.model.objects.get(user_name=user_name)
        except orm.exceptions.NoMatch:
            return None

    async def get_user_id(self, id: int) -> Union[None, dict]:
        try:
            return await self.model.objects.get(id=id)
        except orm.exceptions.NoMatch:
            return None

    async def get_two_model(self, pk: int):
        try:
            return await self.model_info.objects.get(id=pk)
        except orm.exceptions.NoMatch:
            return None

    async def is_user_exists(self, email: str, user_name: str) -> bool:
        try:
            await self.get_user_by_name(user_name)
            await self.get_user_by_email(email)
            return True
        except orm.exceptions.NoMatch:
            return False
