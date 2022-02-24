from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
import api.core.services.reco.recommendation as rec_service
from api.core.db.mongodb import get_database
from api.core.util.config import ENDPOINT_RECOMMENDATION, TAG_RECOMMENDATIONS, ENDPOINT_UNPERSONALIZED

api_router = APIRouter(prefix=ENDPOINT_RECOMMENDATION + ENDPOINT_UNPERSONALIZED, tags=[TAG_RECOMMENDATIONS])


@api_router.get("/random")
async def get_random_items(db: AsyncIOMotorClient = Depends(get_database), n_recos: int = 5):
    """Return list of random items.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    return await rec_service.get_random_items(db, n_recos)


@api_router.get("/latest")
async def get_latest_items(db: AsyncIOMotorClient = Depends(get_database), n_recos: int = 5):
    """Return list of most recently added items.

    Args:
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of latest n_recos items.
    """
    return await rec_service.get_latest_items(db, n_recos)
