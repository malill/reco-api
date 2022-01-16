from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from api.core.db.mongodb import get_database

api_router = APIRouter()


@api_router.get("/personalized/item_based_collaborative_filtering")
def get_item_based_collaborative_filtering_items(item_id_seed: int,
                                                 n_recos: int = 5,
                                                 db: AsyncIOMotorClient = Depends(get_database)):
    """Return list of items from collaborative filtering given a seed item ID.

    Args:
        item_id_seed (int): ID of seed item that is used for finding item-wise similar items.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    # items = crud.get_item_based_collaborative_filtering_items(db, item_id_seed=item_id_seed, n_recos=n_recos)

    # if consumables is None:
    #     raise HTTPException(status_code=404, detail="No recommendations found")
    # return [i.item for i in consumables if i.item is not None]
    return "Hello World"
