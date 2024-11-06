from fastapi import APIRouter
from sqlalchemy import insert

from app.db_models.users import RegisterUser, User
from app.setup_db import async_session

router = APIRouter(tags=["Authentication"])


@router.post("/signup/")
async def create_user(signup_data: RegisterUser) -> None:
    async with async_session() as session:
        new_user = User(
            username=signup_data.username,
            email=signup_data.email,
            password=User.hash_password(signup_data.password),
        )
        session.add(new_user)
        await session.commit()
