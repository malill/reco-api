from typing import List

from fastapi import APIRouter, Depends, HTTPException
from core.db.database import SessionLocal
from sqlalchemy.orm import Session
from core.db import crud, schemas
from core.db.models import Item

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/unpersonalized/random", response_model=List[schemas.Item])
def get_random_items(db: Session = Depends(get_db), n_recos: int = 5) -> List[Item]:
    """Return list of random items.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    return crud.get_random_items(db, n_recos)


@router.get("/unpersonalized/fbt/{item_id_seed}", response_model=List[schemas.Item])
def get_frequently_bought_together_items(item_id_seed: int, db: Session = Depends(get_db),
                                         n_recos: int = 5) -> List[Item]:
    """Return list of frequently bought together items given a seed item ID.

    Args:
        item_id_seed (int): ID of seed item that is used for finding frequently bought together items.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of frequently bought together items.
    """
    items = crud.get_frequently_bought_together_items(db, item_id_seed=item_id_seed, n_recos=n_recos)
    if items is None:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return [i.item for i in items]
