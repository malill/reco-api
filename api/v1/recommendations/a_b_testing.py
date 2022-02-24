import logging
from typing import Optional, List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

import api.core.services.recommendations as service_reco

from api.core.db.mongodb import get_database
from api.core.util.config import ENDPOINT_RECOMMENDATION, TAG_RECOMMENDATIONS
import api.core.util.config as cfg

api_router = APIRouter(prefix=ENDPOINT_RECOMMENDATION + cfg.ENDPOINT_TESTING, tags=[TAG_RECOMMENDATIONS])

logger = logging.getLogger(__name__)


@api_router.post("/ab/config")
async def a_b_testing_config(name: str, methods: list, db: AsyncIOMotorClient = Depends(get_database)):
    """Route to create a A/B testing setup."""
    ab_test = await service_reco.set_ab_testing_config(db, name, methods)
    return ab_test


@api_router.get("/ab")
async def a_b_testing(name: str,
                      request: Request,
                      item_id_seed: int,
                      db: AsyncIOMotorClient = Depends(get_database),
                      n_recos: int = 5):
    """Endpoint that enables A/B testing between recommendation types.

    Args:
        name (str): Name of A/B Test (used to fetch respective recommendations algorithms).
        request (Request): Object to retrieve identifying values from call.
        item_id_seed (str): ID of item for which recommendations are needed.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    try:
        reco_cookie_id = request.cookies[cfg.RECO_COOKIE_ID]
        items = await service_reco.get_ab_testing_items(db, name, reco_cookie_id, item_id_seed, n_recos)
        return items
    except KeyError:
        logger.error("Could not find cookie id in request")
    except NotImplementedError:
        logger.error(f"No recommendation method found for A/B test [{name}]")

    logger.error(f"Could not request recommendation method for A/B test [{name}] ... returning random recommendations")
    return await service_reco.get_random_items(db, n_recos)
