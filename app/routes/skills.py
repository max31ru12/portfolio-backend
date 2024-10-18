from typing import Annotated

from fastapi import APIRouter, Path
from sqlalchemy import select

from app.db_models.skill import Skill, SkillModel
from app.setup_db import async_session

router = APIRouter(tags=["skills"])


@router.get("/")
async def get_skills() -> list[SkillModel]:
    async with async_session() as session:
        stmt = select(Skill)
        skills = await session.execute(stmt)
        skills_db = [SkillModel.from_orm(skill) for skill in skills.scalars().all()]
    return skills_db


@router.get("/{skill_id}")
async def get_skill_detail(skill_id: int) -> SkillModel:
    async with async_session() as session:
        stmt = select(Skill).where(Skill.id == skill_id)
        skill = await session.execute(stmt)
    return SkillModel.from_orm(skill.scalars().all()[0])

