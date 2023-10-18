from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import crud
from db.db_config import get_async_session, User
from auth.auth import fastapi_users
from schema.schemas import RequestLevel, Response

level_router = APIRouter()
current_user = fastapi_users.current_user()


@level_router.post('/create')
async def create_level(req: RequestLevel, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    _level = await crud.create_level(level=req.parameter, session=session)
    return Response(code=200, status="OK", message="Level created successfully", result=_level).dict(exclude_none=True)


@level_router.get("/{level_id}")
async def get_level_by_id(level_id: int, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    _level = await crud.get_level_by_id(level_id=level_id, session=session)
    return Response(code=200, status="OK", message="Success get data", result=_level).dict(exclude_none=True)


@level_router.delete("/{level_id}")
async def delete(level_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    await crud.delete_level(level_id=level_id, session=session)
    return Response(code=200, status="OK", message="Success delete data").dict(exclude_none=True)
