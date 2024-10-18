from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel

from app.setup_db import Base


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class CreateTodoModel(BaseModel):
    title: str
    description: str


class TodoModel(CreateTodoModel):
    model_config = {
        "from_attributes": True
    }

    id: int
    created_at: datetime

