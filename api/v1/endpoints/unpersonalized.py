from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.mongodb import get_database
from api.core.services.main import get_random_consumables, get_latest_consumables, \
    get_item_based_collaborative_filtering_items

api_router = APIRouter()


@api_router.get("/unpersonalized/random")
async def random_consumables(db: AsyncIOMotorClient = Depends(get_database), n_recos: int = 5):
    """Return list of random items.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    return await get_random_consumables(db, n_recos)


@api_router.get("/unpersonalized/latest")
async def latest_consumables(db: AsyncIOMotorClient = Depends(get_database), n_recos: int = 5):
    """Return list of most recently added items.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of latest n_recos items.
    """
    return await get_latest_consumables(db, n_recos)


@api_router.get("/personalized/item_based_collaborative_filtering")
async def item_based_collaborative_filtering_items(item_id_seed: int,
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
    return await get_item_based_collaborative_filtering_items(db, item_id_seed=item_id_seed, n_recos=n_recos)
