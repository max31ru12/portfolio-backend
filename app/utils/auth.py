from datetime import timedelta, datetime
from typing import Any

import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import AUTH_JWT_SETTINGS
from app.db_models.users import User, SignIn


async def authenticate_user(signup_data: SignIn, session: AsyncSession) -> User:
    stmt = select(User).filter(User.username == signup_data.username)
    user = (await session.execute(stmt)).scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="There is no such user")
    return user


def encode_jwt(
        payload: dict[str, Any],
        private_key: str = AUTH_JWT_SETTINGS.private_key_path.read_text(),
        algorithm: str = AUTH_JWT_SETTINGS.algorithm,
        expire_timedelta: timedelta = AUTH_JWT_SETTINGS.access_token_expire
) -> str:
    to_encode = payload.copy()
    expire = datetime.now() + expire_timedelta
    to_encode.update(exp=expire, iat=datetime.now())
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = AUTH_JWT_SETTINGS.public_key_path.read_text(),
        algorithm: str = AUTH_JWT_SETTINGS.algorithm
) -> Any:
    return jwt.decode(token, public_key, algorithms=[algorithm])
