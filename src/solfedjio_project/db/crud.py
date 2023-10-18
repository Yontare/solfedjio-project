from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Level
from schema.schemas import LevelSchema


async def get_level_by_id(level_id: int, session: AsyncSession):
    result = await session.execute(select(Level).where(Level.id == level_id))
    return result.scalars().one()


async def create_level(level: LevelSchema, session: AsyncSession):
    _level = Level(title=level.title)
    session.add(_level)
    await session.commit()
    return _level


async def delete_level(level_id: int, session: AsyncSession):
    _level = await get_level_by_id(level_id, session)
    await session.delete(_level)
    await session.commit()
