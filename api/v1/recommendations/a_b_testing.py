import logging
from typing import Optional, List

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
        reco_cookie_id = request.cookies[cfg.RECO_COOKIE_ID]

        try:
            user = await service_user.get_or_create_user_by_cookie(conn=db,
                                                                   cookie_value=reco_cookie_id)
            if (user.groups is not None) and (name in user.groups.keys()):
                logger.info(f"A/B test name '{name}' found for user {str(user._id)} with value {user.groups[name]}")
            else:
                logger.info(f"A/B test name '{name}' NOT found for user {str(user._id)}")
                # TODO: bad since we make 2 MongoDB calls when user is new (create w/o group and then update group)
                user = await service_user.update_user_group(
                    db, user, name, await service_reco.draw_ab_test_recommendation_method(db, "test"))

            fun = reco_dict[user.groups[name]]
            recs = await fun(db, item_id_seed=item_id_seed, base="item")
            return recs
        except KeyError:
            print(f"Could not find recommendation method for A/B test [{name}]")

    except KeyError:
        logger.error("Could not find cookie id in request")

    logger.error(f"Could not request recommendation method for A/B test [{name}] ... returning random recommendations")
    return await service_reco.get_random_items(conn=db, n_recos=n_recos)
