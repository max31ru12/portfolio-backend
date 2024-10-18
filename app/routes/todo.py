from fastapi import APIRouter

from app.db_models.todo import CreateTodoModel, Todo
from app.setup_db import async_session

router = APIRouter(tags=["todo"])


@router.post("/")
async def create_todo(form_data: CreateTodoModel) -> None:
    async with async_session() as session:
        instance = Todo(**form_data.model_dump())
        session.add(instance)
        await session.commit()


@router.get("/")
async def get_todos():
    return "hello"
