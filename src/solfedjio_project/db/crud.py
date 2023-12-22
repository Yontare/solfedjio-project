from sqlalchemy import select, text, exists, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import User
from db.models import Level, Task, Attachment, Answer, Stat
from schema.schemas import ShortLevelSchema, LevelSchema, TaskSchema, LevelOrderField, StatSchema


async def get_level_by_id(level_id: int, session: AsyncSession):
    result = await session.execute(select(Level).where(Level.id == level_id))
    return result.scalars().one()


async def get_random_tasks(session: AsyncSession):
    tasks = await session.execute(select(Task).order_by(func.random()).limit(7))
    return tasks.scalars()


async def get_levels(order: LevelOrderField, user: User, session: AsyncSession):
    result = await session.execute(select(Level.id, Level.title).order_by(text(order)))
    return [ShortLevelSchema(id=short_level[0], title=short_level[1],
                             is_finished=await is_level_finished(short_level[0], user, session))
            for short_level in result.all()]


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


async def create_stat(stat_schema: StatSchema, user: User, session: AsyncSession):
    stat = Stat(
        right_answers_count=stat_schema.right_answers_count,
        all_answers_count=stat_schema.all_answers_count,
        level_id=stat_schema.level_id,
        user_id=user.id
    )

    session.add(stat)
    await session.commit()
    return stat


async def is_level_finished(level_id: int, user: User, session: AsyncSession):
    return await session.scalar(exists().where(and_(Stat.user_id == user.id, Stat.level_id == level_id)).select())


async def get_stat_by_level_id(level_id: int, user: User, session: AsyncSession):
    result = await session.execute(select(Stat).where(and_(Stat.level_id == level_id, Stat.user_id == user.id)))
    return result.scalars().one()


async def get_stat_by_user(user: User, session: AsyncSession):
    result = await session.execute(select(Stat).where(Stat.user_id == user.id))
    return [StatSchema.model_validate(stat) for stat in result.scalars()]
