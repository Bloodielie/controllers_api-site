from datetime import datetime, timedelta
from typing import Dict, List, Union
import time

import jwt
from fastapi.encoders import jsonable_encoder
from jwt import PyJWTError

from app.configuration.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.client.user_repository import UserRepository


def generate_token(data: Dict[str, str], token_type: str) -> str:
    to_encode_token = data.copy()
    expire_token = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if token_type == 'refresh_token':
        expire_token += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES*40)
    to_encode_token.update({"exp": expire_token, "type": token_type})
    return jsonable_encoder(jwt.encode(to_encode_token, SECRET_KEY, algorithm=ALGORITHM))


def create_tokens(*, data: Dict[str, str]) -> List[str]:
    """
    Data example {"sub": "ilya"}
    return [access_token, refresh_token]
    """
    access_token = generate_token(data, 'access_token')
    refresh_token = generate_token(data, 'refresh_token')

    return [access_token, refresh_token]


class TokenTools:
    @staticmethod
    def get_token_payload(token) -> Union[dict, None]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except PyJWTError:
            return None

    def get_user_name_in_token(self, token) -> Union[str, None]:
        payload = self.get_token_payload(token)
        if payload is None:
            return None
        return payload.get("sub")

    async def check_token(self, token: str) -> bool:
        username = self.get_user_name_in_token(token)
        if username is None:
            return False
        user = await UserRepository().get_user('user_name', username)
        if not user:
            return False
        token_data = self.get_token_payload(token)
        exp = token_data.get('exp')
        if exp < int(time.time()):
            return False
        return True
