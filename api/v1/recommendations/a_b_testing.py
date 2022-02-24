import logging
from typing import Optional

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

import api.core.services.user as service_user

from api.core.db.mongodb import get_database
from api.core.util.config import ENDPOINT_RECOMMENDATION, TAG_RECOMMENDATIONS
import api.core.util.config as cfg
from api.v1.recommendations.recommendation_dict import reco_dict

api_router = APIRouter(prefix=ENDPOINT_RECOMMENDATION + cfg.ENDPOINT_TESTING, tags=[TAG_RECOMMENDATIONS])

logger = logging.getLogger(__name__)


@api_router.get("/ab")
async def a_b_testing(name: str,
                      request: Request,
                      db: AsyncIOMotorClient = Depends(get_database),
                      item_id_seed: Optional[int] = None,
                      n_recos: int = 5):
    """Endpoint that enables A/B testing between recommendation types.

    Args:
        name (str): Name of A/B Test (used to fetch respective recommendations algorithms).
        item_id_seed (str): ID of item for which recommendations are needed.
        request (Request): Object to retrieve identifying values from call.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of random items.
    """
    reco_cookie_value = None
    try:
        # every call to reco-api is expected to contain a reco-cookie-id
        reco_cookie_value = request.cookies[cfg.RECO_COOKIE_ID]
        user = await service_user.get_user(db, reco_cookie_value)  # will always return a user even if new user
        if name in user.groups.keys():
            # user is assigned to AB test group
            print(f"A/B test name '{name}' found for user {str(user.uid)} with value {user.groups[name]}")
            fun = reco_dict[user.groups[name]]
            # TODO: bad implementation (can also be moved after if/else clause)
            recs = await fun(db, item_id_seed=item_id_seed, base="item")
            return recs
        else:
            # user is not assigned to AB test group (new user or already existing but first calling user)
            print(f"A/B test name '{name}' NOT found for user {str(user.uid)}")
            await service_user.update_user_group(db, user, name, "dummy_group")
    except KeyError:
        print("could not find cookie id in request")
        print("OR could not find recommendation method!")

    return reco_cookie_value
