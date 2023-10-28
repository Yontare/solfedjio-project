import asyncio

from fastapi import FastAPI

from auth.auth import auth_backend, fastapi_users
from db.db_config import create_db_and_tables
from router import level_router, task_router
from schema.schemas import UserRead, UserCreate

app = FastAPI()
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Authentication"], )
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["Authentication"], )
app.include_router(level_router.level_router, prefix="/level", tags=["Level"])
app.include_router(task_router.task_router, prefix="/task", tags=["Task"])
asyncio.create_task(create_db_and_tables())
