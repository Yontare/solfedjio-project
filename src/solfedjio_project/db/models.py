import enum
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.db_config import Base


class Level(Base):
    __tablename__ = 'level'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(cascade="all, delete-orphan", lazy="selectin")


class TaskType(enum.Enum):
    one = "one"
    two = "two"
    three = "three"


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[TaskType] = mapped_column(nullable=False, default=TaskType.one)
    attachments: Mapped[List["Attachment"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))


class Attachment(Base):
    __tablename__ = 'attachment'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
