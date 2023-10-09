from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import LevelSchema, RequestLevel, Response
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create(req: RequestLevel, db: Session = Depends(get_db)):
    _level = crud.create_level(db, level=req.parameter)
    return Response(code=200, status="OK", message="Level created successfully", result=_level).dict(exclude_none=True)


@router.get("/{id}")
async def get_by_id(id: int, db: Session = Depends(get_db)):
    _level = crud.get_level_by_id(db, id)
    return Response(code=200, status="OK", message="Success get data", result=_level).dict(exclude_none=True)


@router.get("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    crud.remove_level(db, level_id=id)
    return Response(code=200, status="OK", message="Success delete data").dict(exclude_none=True)