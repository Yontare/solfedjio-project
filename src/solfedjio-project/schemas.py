from typing import List, Optional, Generic, TypeVar
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


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
