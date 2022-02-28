import logging
from typing import List

import numpy as np
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

import api.core.services.reco.recommendation as service_reco
import api.core.services.collection.user as service_user
import api.core.util.config as cfg
from api.core.db.models.splitting import BasicSplittingModel

from api.core.services.reco.recommendation import reco_str2fun

logger = logging.getLogger(__name__)


async def get_splitting(conn: AsyncIOMotorClient, name: str):
    res = await get_splitting_collection(conn).find_one({'name': name})
    return res


async def get_all_splittings(conn: AsyncIOMotorClient):
    return await get_splitting_collection(conn).find().to_list(None)


async def set_splitting(conn: AsyncIOMotorClient, name: str, methods: List):
    splitting = BasicSplittingModel(name=name, methods=methods)
    entry_req = jsonable_encoder(splitting, exclude_none=True)
    await get_splitting_collection(conn).find_one_and_update({'name': splitting.name}, {"$set": entry_req},
                                                             upsert=True)
    return splitting


async def delete_splitting(conn: AsyncIOMotorClient, name: str) -> int:
    """Deletes splitting by name and returns number of deleted objects."""
    res = await get_splitting_collection(conn).delete_one({'name': name})
    return res.deleted_count


async def get_split_recommendations_by_user_cookie(db: AsyncIOMotorClient,
                                                   split_name: str,
                                                   reco_cookie_id: str,
                                                   item_id_seed: int,
                                                   n_recos: int):
    """Retrieve recommendations for users with a reco-cookie-id from a split method."""
    user = None
    if reco_cookie_id is None:
        logger.error(f"No {cfg.RECO_COOKIE_ID} found in request header -> returning random recommendations.")
        items = await service_reco.get_random_items(db, n_recos)
        return items
    user = await service_user.get_user_by_keys(db, cookie_value=reco_cookie_id)
    user = user[0]
    if (user.groups is not None) and (split_name in user.groups.keys()):
        logger.info(
            f"Splitting [{split_name}] found in user [{str(user._id)}]")
    else:
        logger.info(f"Splitting [{split_name}] NOT found for user [{str(user._id)}]")
        user = await service_user.update_user_group(db, user,
                                                    group_name=split_name,
                                                    group_value=await draw_splitting_method(db, split_name))
    reco_method = reco_str2fun.get(user.groups.get(split_name))
    return await reco_method(db, n_recos=n_recos, item_id_seed=item_id_seed, base="item")


async def draw_splitting_method(conn: AsyncIOMotorClient,
                                split_name: str) -> str:
    """Draw a reco method from splitting."""
    splitting = await get_splitting(conn, split_name)
    if splitting is None:
        logger.error(f"Splitting [{split_name}] not found in collection -> use fallback recommendation method")
        return cfg.TYPE_FALLBACK
    split_model = BasicSplittingModel(**splitting)
    method_str = np.random.choice(split_model.methods)
    if method_str in reco_str2fun.keys():
        return method_str
    else:
        logger.error(
            f"Recommendation method shortcut drawn from splitting [{split_name}] with value [{method_str}] "
            f"is unknown ... using fallback recommendations")
        return cfg.TYPE_FALLBACK


def get_splitting_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_SPLITTING_CONFIG]
