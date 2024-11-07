from datetime import timedelta, datetime
from typing import Any

import jwt
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import AUTH_JWT_SETTINGS
from app.db_models.users import User, TokenData
from app.services.user_services import get_user_by_username
from app.setup_db import async_session


http_bearer = HTTPBearer()


async def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
    token_data: TokenData = decode_jwt(token=credentials.credentials)
    async with async_session() as session:
        user = await get_user_by_username(username=token_data["username"], session=session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    return user


def encode_jwt(
        payload: dict[str, Any],
        private_key: str = AUTH_JWT_SETTINGS.private_key_path.read_text(),
        algorithm: str = AUTH_JWT_SETTINGS.algorithm,
        expire_timedelta: timedelta = AUTH_JWT_SETTINGS.access_token_expire
) -> str:
    to_encode = payload.copy()
    token_created = datetime.now() - timedelta(hours=3)
    expire = token_created + expire_timedelta
    to_encode.update(exp=expire, iat=token_created)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = AUTH_JWT_SETTINGS.public_key_path.read_text(),
        algorithm: str = AUTH_JWT_SETTINGS.algorithm
) -> Any:
    try:
        return jwt.decode(token, public_key, algorithms=[algorithm])
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
