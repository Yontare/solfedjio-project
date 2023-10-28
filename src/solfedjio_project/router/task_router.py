from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from db import crud
from db.db_config import get_async_session, User
from schema.schemas import RequestTask, ResponseSchema, TaskSchema

task_router = APIRouter()
current_user = fastapi_users.current_user()


@task_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(req: RequestTask, session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_user)):
    task_schema = TaskSchema.model_validate(await crud.create_task(task=req.parameter, session=session))
    return ResponseSchema(status="OK", message="Task created successfully", result=task_schema)


@task_router.post('/update/{task_id}')
async def update(task_id: int, req: RequestTask, session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_user)):
    task_schema = TaskSchema.model_validate(
        await crud.update_task(task_id=task_id, task=req.parameter, session=session))
    return ResponseSchema(status="OK", message="Task updated successfully", result=task_schema)


@task_router.get("/{task_id}")
async def get_by_id(task_id: int, response: Response, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    try:
        task_schema = TaskSchema.model_validate(await crud.get_task_by_id(task_id=task_id, session=session))
        return ResponseSchema(status="OK", message="Success get data", result=task_schema)
    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND


@task_router.delete("/{task_id}")
async def delete_by_id(task_id: int, response: Response, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        await crud.delete_task(task_id=task_id, session=session)
        return ResponseSchema(status="OK", message="Success delete data")
    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
