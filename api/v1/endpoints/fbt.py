from fastapi import APIRouter, Depends, HTTPException
from core.db.database import SessionLocal
from sqlalchemy.orm import Session
from core.db import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/fbt/{item_seed_id}")
def get_items(item_seed_id: int, db: Session = Depends(get_db)):
    items = crud.get_items(db, item_seed_id=item_seed_id)
    if items is None:
        raise HTTPException(status_code=404, detail="User not found")
    return items
