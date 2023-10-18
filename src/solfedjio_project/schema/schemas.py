import uuid
from typing import Optional, Generic, TypeVar

from fastapi_users import schemas
from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel

T = TypeVar('T')


class LevelSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True


class RequestLevel(BaseModel):
    parameter: LevelSchema = Field(...)


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
