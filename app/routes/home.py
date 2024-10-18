from fastapi import APIRouter
from sqlalchemy import select

from app.db_models.skill import Skill, SkillModel
from app.setup_db import async_session

router = APIRouter(tags=["homepage"])
