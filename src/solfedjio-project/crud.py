from sqlalchemy.orm import Session
from models import Level
from schemas import LevelSchema


def get_level_by_id(db: Session, level_id: int):
    return db.query(Level).filter(Level.id == level_id).first()


def create_level(db: Session, level: LevelSchema):
    _level = Level(title=level.title)
    db.add(_level)
    db.commit()
    db.refresh(_level)
    return _level


def remove_level(db: Session, level_id: int):
    _level = get_level_by_id(db, level_id)
    db.delete(_level)
    db.commit()
