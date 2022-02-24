import logging
from typing import Optional

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

import api.core.services.user as service_user
import api.core.services.recommendations as service_reco

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
    try:
        # every call to reco-api is expected to contain at least a reco-cookie-id
        user = await service_user.get_user_by_cookie(db, request.cookies[cfg.RECO_COOKIE_ID])
        if (user.groups is not None) and (name in user.groups.keys()):
            print(f"A/B test name '{name}' found for user {str(user._id)} with value {user.groups[name]}")
        else:
            print(f"A/B test name '{name}' NOT found for user {str(user._id)}")
            # TODO: bad since we make 2 MongoDB calls when user is new (create w/o group and then update group)
            user = await service_user.update_user_group(
                db, user, name, await service_reco.draw_ab_test_recommendation_method(db, "test"))

        fun = reco_dict[user.groups[name]]
        recs = await fun(db, item_id_seed=item_id_seed, base="item")
        return recs
    except KeyError:
        print("could not find cookie id in request")
        print("OR could not find recommendation method!")

    return "todo something"
