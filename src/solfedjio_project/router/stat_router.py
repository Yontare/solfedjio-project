from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from db import crud
from db.db_config import get_async_session, User
from schema.schemas import ResponseSchema, StatSchema

stat_router = APIRouter()
current_user = fastapi_users.current_user()


@stat_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(stat: StatSchema, user: User = Depends(current_user),
                 session: AsyncSession = Depends(get_async_session)):
    stat_schema = StatSchema.model_validate(await crud.create_stat(stat_schema=stat, user=user, session=session))
    return ResponseSchema(status="OK", message="Stat created successfully", result=stat_schema)


@stat_router.get("/{level_id}")
async def get_by_level_id(level_id: int, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    stat_schema = StatSchema.model_validate(await crud.get_stat_by_level_id(level_id=level_id, user=user,
                                                                            session=session))
    return ResponseSchema(code=200, status="OK", message="Success get data", result=stat_schema)


@stat_router.get("/")
async def get_by_user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    result = await crud.get_stat_by_user(user=user, session=session)
    return ResponseSchema(code=200, status="OK", message="Success get data", result=result)
