from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Level, Task, Attachment, Answer
from schema.schemas import ShortLevelSchema, LevelSchema, TaskSchema, LevelOrderField


async def get_level_by_id(level_id: int, session: AsyncSession):
    result = await session.execute(select(Level).where(Level.id == level_id))
    return result.scalars().one()


async def get_levels(order: LevelOrderField, session: AsyncSession):
    result = await session.execute(select(Level.id, Level.title).order_by(text(order)))
    return [ShortLevelSchema(id=short_level[0], title=short_level[1]) for short_level in result.all()]


async def create_level(level_schema: LevelSchema, session: AsyncSession):
    level = Level(
        title=level_schema.title
    )
    if level_schema.tasks is not None:
        level.tasks = [Task(**task.model_dump(exclude={"id", "attachments", "answers"}),
                            attachments=[Attachment(**attachment.model_dump(exclude={"id"})) for attachment in
                                         task.attachments],
                            answers=[Answer(**answer.model_dump(exclude={"id"})) for answer in task.answers]) for task
                       in level_schema.tasks]
    else:
        level.tasks = []
    session.add(level)
    await session.commit()
    return level


async def delete_level(level_id: int, session: AsyncSession):
    _level = await get_level_by_id(level_id, session)
    await session.delete(_level)
    await session.commit()


async def create_task(task_schema: TaskSchema, session: AsyncSession):
    task = Task(
        text=task_schema.text,
        type=task_schema.type
    )
    if task_schema.attachments is not None:
        task.attachments = [Attachment(**attachment.model_dump(exclude={"id"})) for attachment in
                            task_schema.attachments]
    else:
        task.attachments = []
    if task_schema.answers is not None:
        task.answers = [Answer(**answer.model_dump(exclude={"id"})) for answer in task_schema.answers]
    else:
        task.answers = []
    session.add(task)
    await session.commit()
    return task


async def update_task(task_id: int, task: TaskSchema, session: AsyncSession):
    _task = await get_task_by_id(task_id, session)
    _task.text = task.text
    _task.type = task.type
    _task.attachments = [Attachment(**attachment.model_dump()) for attachment in task.attachments]
    await session.commit()
    return _task


async def get_task_by_id(task_id: int, session: AsyncSession):
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalars().one()


async def delete_task(task_id: int, session: AsyncSession):
    _task = await get_task_by_id(task_id, session)
    await session.delete(_task)
    await session.commit()
