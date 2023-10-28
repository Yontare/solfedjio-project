import uuid
from enum import Enum
from typing import Optional, Generic, TypeVar

from fastapi_users import schemas
from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel

from db.models import TaskType

T = TypeVar('T')


class AttachmentSchema(BaseModel):
    id: Optional[int] = None
    path: Optional[str] = None

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    type: Optional[TaskType] = None
    attachments: list[AttachmentSchema] | None = None

    class Config:
        from_attributes = True


class LevelSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    tasks: list[TaskSchema] | None = None

    class Config:
        from_attributes = True


class ShortLevelSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None


class LevelOrderField(str, Enum):
    ID = "id"
    TITLE = "title"


class RequestLevel(BaseModel):
    parameter: LevelSchema = Field(...)


class RequestTask(BaseModel):
    parameter: TaskSchema = Field(...)


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class ResponseSchema(GenericModel, Generic[T]):
    status: str
    message: str
    result: Optional[T]
