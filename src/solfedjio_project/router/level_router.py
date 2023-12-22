from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from db import crud
from db.db_config import get_async_session, User
from schema.schemas import RequestLevel, ResponseSchema, LevelSchema, LevelOrderField, TaskSchema
import time

level_router = APIRouter()
current_user = fastapi_users.current_user()


@level_router.get('/check_permissions')
async def check_permissions(user: User = Depends(current_user)):
    return ResponseSchema(code=200, status="OK", message="Successfully check permissions")


@level_router.get('/check_username')
async def check_username(user: User = Depends(current_user)):
    return ResponseSchema(code=200, status="OK", message="Successfully get username", result=user.email)


@level_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(req: RequestLevel, session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_user)):
    level_schema = LevelSchema.model_validate(await crud.create_level(level_schema=req.parameter, session=session))
    return ResponseSchema(code=200, status="OK", message="Level created successfully", result=level_schema)


@level_router.get("/{level_id}")
async def get_by_id(level_id: int, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    level_schema = LevelSchema.model_validate(await crud.get_level_by_id(level_id=level_id, session=session))
    random_tasks = await crud.get_random_tasks(session)
    level_schema.tasks = [TaskSchema.model_validate(random_task) for random_task in random_tasks]
    return ResponseSchema(code=200, status="OK", message="Success get data", result=level_schema)


@level_router.get("/")
async def level_list(order: LevelOrderField, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    levels = await crud.get_levels(order=order, user=user, session=session)
    time.sleep(0.15)
    return ResponseSchema(code=200, status="OK", message="Success get data", result=levels)


@level_router.delete("/{level_id}")
async def delete_by_id(level_id: int, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    await crud.delete_level(level_id=level_id, session=session)
    return ResponseSchema(code=200, status="OK", message="Success delete data").dict(exclude_none=True)
