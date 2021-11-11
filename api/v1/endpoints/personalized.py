from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from requests import Session

from core.db.database import SessionLocal
from core.db.models import Item
from core.db import crud, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/personalized/item_based_collaborative_filtering", response_model=List[schemas.Item])
def get_item_based_collaborative_filtering_items(item_id_seed: int,
                                                 db: Session = Depends(get_db),
                                                 n_recos: int = 5) -> List[Item]:
    """Return list of items from collaborative filtering given a seed item ID.

    Args:
        item_id_seed (int): ID of seed item that is used for finding item-wise similar items.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    items = crud.get_item_based_collaborative_filtering_items(db, item_id_seed=item_id_seed, n_recos=n_recos)
    if items is None:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return [i.item for i in items if i.item is not None]
