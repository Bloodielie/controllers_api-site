from datetime import datetime
from typing import Union, Any

from app.client.models import User, UserInfo, UserSecurity, UserEmail
from .pydantic_models import User as user
from .security.auth import get_email_verify_postfix


class UserRepository:
    def __init__(self, main_model=User, model_info=UserInfo, model_security=UserSecurity, model_email=UserEmail):
        self.model = main_model
        self.model_info = model_info
        self.model_security = model_security
        self.model_email = model_email

    async def create_user(self, user: user) -> None:
        user_security = await self.model_security.objects.create(refresh_token=user.refresh_token)
        user_info = await self.model_info.objects.create(user_name=user.user_name, create_at=datetime.now())
        email_postfix = get_email_verify_postfix(user.user_name)
        user_email = await self.model_email.objects.create(email_verify=email_postfix)
        return await self.model.objects.create(user_name=user.user_name, email=user.email, hashed_password=user.hashed_password,
                                               user_info=user_info, user_security=user_security, user_email=user_email)

    async def get_user(self, parameter: str, value: Any) -> Union[User, None]:
        argument = {parameter: value}
        user = await self.model.objects.filter(**argument).all()
        if user:
            return user[0]
        return None

    @staticmethod
    async def get_other_model(attr: str, user: User) -> Union[UserInfo, UserSecurity, UserEmail, None]:
        other_model = getattr(user, attr)
        await other_model.load()
        return other_model

    async def get_email_verify(self, email_verify: str) -> Union[UserEmail, None]:
        user = await self.model_email.objects.filter(email_verify=email_verify).all()
        if user:
            return user[0]
        return None

    async def get_refresh_token_model(self, refresh_token) -> Union[UserSecurity, None]:
        model = await self.model_security.objects.filter(refresh_token=refresh_token).all()
        if model:
            return model[0]
        return None

    async def is_user_exists(self, email: str, user_name: str) -> bool:
        name = await self.get_user('user_name', user_name)
        email = await self.get_user('email', email)
        if not name and not email:
            return False
        return True
