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



@router.get("/random")
def get_random_items(db: Session = Depends(get_db)):
    return crud.get_random_items(db)

@router.get("/fbt/{item_id_seed}")
def get_frequently_bought_together_items(item_id_seed: int, db: Session = Depends(get_db)):
    items = crud.get_frequently_bought_together_items(db, item_id_seed=item_id_seed)
    if items is None:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return [i.item for i in items]
