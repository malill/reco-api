import logging
from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

import api.core.services.user as service_user
import api.core.util.config as cfg

from api.core.db.models.recommendation import ABTestModel
from api.core.services.recommendations import reco_dict

logger = logging.getLogger(__name__)


async def set_ab_testing_config(conn: AsyncIOMotorClient, name: str, methods: List):
    ab_test = ABTestModel(name=name, methods=methods)
    entry_req = jsonable_encoder(ab_test, exclude_none=True)
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_AB_TESTING_CONFIG]
    await cursor.find_one_and_update({'name': ab_test.name}, {"$set": entry_req},
                                     upsert=True)
    return ab_test


async def get_ab_testing_items(db: AsyncIOMotorClient, name: str, reco_cookie_id: str, item_id_seed: int, n_recos: int):
    try:
        user = await service_user.get_or_create_user_by_cookie(db, cookie_value=reco_cookie_id)
        if (user.groups is not None) and (name in user.groups.keys()):
            logger.info(f"A/B test name '{name}' found for user {str(user._id)} with value {user.groups[name]}")
        else:
            logger.info(f"A/B test name '{name}' NOT found for user {str(user._id)}")
            # TODO: bad since we make 2 MongoDB calls when user is new (create w/o group and then update group)
            user = await service_user.update_user_group(db, user,
                                                        group_name=name,
                                                        group_value=await draw_ab_test_recommendation_method(db, name))

        fun = reco_dict[user.groups[name]]
        recs = await fun(db, item_id_seed=item_id_seed, base="item", n_recos=n_recos)
        return recs
    except KeyError:
        raise NotImplementedError()


async def draw_ab_test_recommendation_method(conn: AsyncIOMotorClient,
                                             name: str):
    """Get a recommendation method from AB test."""
    #
    return "hallo"
