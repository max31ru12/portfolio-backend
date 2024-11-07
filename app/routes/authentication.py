from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy import select

from app.db_models.users import SignUp, User, SignIn, TokenInfo
from app.setup_db import async_session
from app.utils.auth import authenticate_user, encode_jwt

router = APIRouter(tags=["Authentication"])


@router.post("/signup/")
async def sign_up(signup_data: SignUp) -> None:

    async with async_session() as session:
        stmt = select(User).filter(User.username == signup_data.username)
        if (await session.execute(stmt)).scalars().first() is not None:
            raise HTTPException(status_code=409, detail="This username is already in use")

        new_user = User(
            username=signup_data.username,
            email=signup_data.email,
            password=User.hash_password(signup_data.password),
        )
        session.add(new_user)
        await session.commit()


@router.post("/signin/", summary="Sign in to an account", response_model=TokenInfo)
async def sign_in(auth_data: SignIn) -> TokenInfo:

    async with async_session() as session:
        user = await authenticate_user(auth_data, session)
        if user is None or not user.verify_password(auth_data.password):
            raise HTTPException(status_code=404, detail="Wrong username or password")

        jwt_payload = {"username": user.username, "email": user.email}
        access_token = encode_jwt(jwt_payload)

    return TokenInfo(access_token=access_token, token_type="Bearer")
