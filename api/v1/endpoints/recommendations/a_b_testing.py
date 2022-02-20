import logging

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

import api.core.services.user as service_user

from api.core.db.mongodb import get_database
from api.core.util.config import ENDPOINT_RECOMMENDATION, TAG_RECOMMENDATIONS
import api.core.util.config as cfg

api_router = APIRouter(prefix=ENDPOINT_RECOMMENDATION, tags=[TAG_RECOMMENDATIONS])

logger = logging.getLogger(__name__)


@api_router.get("/testing/ab")
async def a_b_testing_with_item_id(item_id_seed: int,
                                   request: Request,
                                   db: AsyncIOMotorClient = Depends(get_database),
                                   n_recos: int = 5):
    """Endpoint that enables A/B testing between recommendation types.

    Args:
        request (Request): Object to retrieve identifying values from call.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    reco_js_cookie_id = None
    try:
        reco_js_cookie_id = request.cookies[cfg.RECO_JS_COOKIE_ID]
        user = await service_user.get_user(db, reco_js_cookie_id)
        # Note: get_user will always return a user (even if she is new)
        # TODO: check if user already has role
        # TODO: if no set role for her
        # TODO: call specific reco function (!) to return items
    except KeyError:
        # this should not happen since every call to reco-api is performed via reco-js that provides a cookie-id
        # TODO: handle exception (e.g. raise error?)
        logger.error("could not find cookie id in request")

    return reco_js_cookie_id
