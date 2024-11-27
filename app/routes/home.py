from fastapi import APIRouter
from sqlalchemy import select


from app.setup_db import async_session

router = APIRouter(tags=["homepage"])
