from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import DB_URL

async_engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(bind=async_engine)
db_meta = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = db_meta
