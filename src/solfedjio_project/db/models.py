from sqlalchemy import Column, Integer, String
from db.db_config import Base


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    title = Column(String)
