from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import DB_URL, DEV_MODE
from app.routes import home, todo, skills
from app.setup_db import async_engine, Base

from app.db_models.skill import Skill  # noqa
from app.db_models.todo import Todo  # noqa

app = FastAPI(title="Portfolio API")


@app.on_event("startup")
async def init_database():
    print(DEV_MODE, DB_URL)
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router, prefix="/home")
app.include_router(skills.router, prefix="/skills")
app.include_router(todo.router, prefix="/todo")
