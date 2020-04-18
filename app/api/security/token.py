import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from app.configuration.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Dict, List


def create_tokens(*, data: Dict[str, str]) -> List[bytes]:
    """ Data example {"sub": "ilya"} """
    to_encode_access_token = data.copy()
    to_encode_refresh_toke = data.copy()

    expire_access_token = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_refresh_token = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES*6)

    to_encode_access_token.update({"exp": expire_access_token})
    to_encode_refresh_toke.update({"exp": expire_refresh_token})

    encoded_jwt_access = jwt.encode(to_encode_access_token, SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt_refresh = jwt.encode(to_encode_refresh_toke, SECRET_KEY, algorithm=ALGORITHM)
    return [encoded_jwt_access, encoded_jwt_refresh]
