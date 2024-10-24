from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db_models.todo import CreateTodoModel, Todo, TodoModel
from app.setup_db import async_session

router = APIRouter(tags=["todo"])


@router.post("/")
async def create_todo(form_data: CreateTodoModel) -> None:
    async with async_session() as session:
        new_todo = Todo(**form_data.model_dump())
        session.add(new_todo)
        await session.commit()


@router.get("/")
async def get_todos() -> list[TodoModel]:
    async with async_session() as session:
        stmt = select(Todo)
        result = await session.execute(stmt)
    return [TodoModel.from_orm(todo) for todo in result.scalars().all()]


@router.get("/{todo_id}/")
async def get_todo_detail(todo_id: int) -> TodoModel:
    async with async_session() as session:
        stmt = select(Todo).filter(Todo.id == todo_id)
        todo = (await session.execute(stmt)).scalars().first()
    if todo is None:
        raise HTTPException(status_code=404, detail="There is no such todo")
    return TodoModel.from_orm(todo)
