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


class AttachmentType(enum.Enum):
    photo = "photo"
    audio = "audio"


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[TaskType] = mapped_column(nullable=False, default=TaskType.one)
    attachments: Mapped[List["Attachment"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    answers: Mapped[List["Answer"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))


class Attachment(Base):
    __tablename__ = 'attachment'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str]
    type: Mapped[AttachmentType]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))


class Answer(Base):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_right: Mapped[bool]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))


class Stat(Base):
    __tablename__ = 'stat'

    id: Mapped[int] = mapped_column(primary_key=True)
    right_answers_count: Mapped[int]
    all_answers_count: Mapped[int]
    level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
