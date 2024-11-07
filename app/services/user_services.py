from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models.users import User


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    stmt = select(User).filter(User.username == username)
    return (await session.execute(stmt)).scalars().first()
