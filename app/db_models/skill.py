from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from pydantic import BaseModel

from app.setup_db import Base


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column()
    avatar_url: Mapped[str] = mapped_column(String(256))


class SkillCreateModel(BaseModel):
    model_config = {
        "from_attributes": True
    }
    name: str
    level: int
    avatar_url: str


class SkillModel(SkillCreateModel):
    model_config = {
        "from_attributes": True
    }
    id: int

