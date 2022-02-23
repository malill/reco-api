from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.mongodb import get_database
import api.core.services.recommendations as rec_service
from api.core.util.config import ENDPOINT_RECOMMENDATION, TAG_RECOMMENDATIONS, ENDPOINT_PERSONALIZED, \
    ENDPOINT_COLLABORATIVE_FILTERING

api_router = APIRouter(prefix=ENDPOINT_RECOMMENDATION + ENDPOINT_PERSONALIZED, tags=[TAG_RECOMMENDATIONS])


@api_router.get(ENDPOINT_COLLABORATIVE_FILTERING)
async def get_collaborative_filtering(item_id_seed: int,
                                      base: str = "item",
                                      n_recos: int = 5,
                                      db: AsyncIOMotorClient = Depends(get_database)):
    """Return list of items from collaborative filtering given a seed item ID.
    Args:
        item_id_seed (int): ID of seed item that is used for finding item-wise similar items.
        base (str): Type of filtering, i.e. "item" or "used".
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    return await rec_service.get_collaborative_filtering_items(db, item_id_seed=item_id_seed, base=base,
                                                               n_recos=n_recos)
