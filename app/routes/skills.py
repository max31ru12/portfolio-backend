from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db_models.skill import Skill, SkillModel, SkillCreateModel
from app.setup_db import async_session

router = APIRouter(tags=["skills"])


@router.get("/")
async def get_skills() -> list[SkillModel]:
    async with async_session() as session:
        stmt = select(Skill)
        skills = await session.execute(stmt)
        skills_db = [SkillModel.from_orm(skill) for skill in skills.scalars().all()]
    return skills_db


@router.post("/")
async def add_skill(form_data: SkillCreateModel) -> None:
    async with async_session() as session:
        new_skill = Skill(**form_data.model_dump())
        session.add(new_skill)
        await session.commit()


@router.get("/{skill_id}")
async def get_skill_detail(skill_id: int) -> SkillModel | None:
    async with async_session() as session:
        stmt = select(Skill).filter(Skill.id == skill_id)
        skill = (await session.execute(stmt)).scalars().first()
    if skill is None:
        raise HTTPException(status_code=404, detail="There is no such skill")
    return SkillModel.from_orm(skill)
