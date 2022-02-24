import logging
import random
from typing import List

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
import api.core.services.user as service_user
import api.core.util.config as cfg
from api.core.db.models.item import BasicItemModel

logger = logging.getLogger(__name__)


async def get_random_items(conn: AsyncIOMotorClient, n_recos=5) -> List[BasicItemModel]:
    """Retrieve random items from 'item' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[BasicItemModel]: List of random items.
    """
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].find()
    res = random.sample(await cursor.to_list(None), n_recos)
    res = [BasicItemModel(**i) for i in res]
    return limit_returned_items(res, n_recos)


async def get_latest_items(conn: AsyncIOMotorClient,
                           n_recos=5) -> List[BasicItemModel]:
    """Retrieve the latest items from 'item' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[BasicItemModel]: List of random items.
    """
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM] \
        .find() \
        .sort([('update_time', pymongo.DESCENDING)])  # TODO: needs to be changed into create_time -> is part of _id
    res = await cursor.to_list(n_recos)  # TODO: check if this returns sorted products of all or n_reco documents
    res = [BasicItemModel(**i) for i in res]
    return limit_returned_items(res, n_recos)


async def get_collaborative_filtering_items(conn: AsyncIOMotorClient,
                                            item_id_seed: int,
                                            base: str,
                                            n_recos=5) -> List[BasicItemModel]:
    """Retrieve item based collaborative filtered items from 'recs' db.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding similar items.
        base (str): Type of filtering, i.e. "item" or "used".
        n_recos (int): Number of items that should be returned.
    Returns:
        List[BasicItemModel]: List of similar (item-wise) items.
    """
    res = []
    pipeline = [
        {'$match': {
            'item_id_seed': str(quick_fix_adjust_item_id(item_id_seed)),
            'base': base
        }},
        {
            '$lookup': {
                'from': cfg.COLLECTION_NAME_ITEM,
                'localField': 'item_id_recommended',
                'foreignField': 'id',
                'as': 'item'
            }
        },
        {'$unwind': '$item'},  # reduces and flattens the item (array) to a single object
        {'$sort': {'similarity': -1}},
        {'$limit': n_recos}
    ]
    async for doc in conn[cfg.DB_NAME][cfg.COLLECTION_NAME_RECOMMENDATIONS].aggregate(pipeline):
        res.append(BasicItemModel(**doc['item']))
    return limit_returned_items(res, n_recos)


async def get_ab_testing_items(db: AsyncIOMotorClient, name: str, reco_cookie_id: str, item_id_seed: int, n_recos: int):
    try:
        user = await service_user.get_or_create_user_by_cookie(conn=db,
                                                               cookie_value=reco_cookie_id)
        if (user.groups is not None) and (name in user.groups.keys()):
            logger.info(f"A/B test name '{name}' found for user {str(user._id)} with value {user.groups[name]}")
        else:
            logger.info(f"A/B test name '{name}' NOT found for user {str(user._id)}")
            # TODO: bad since we make 2 MongoDB calls when user is new (create w/o group and then update group)
            user = await service_user.update_user_group(
                db, user, name, await draw_ab_test_recommendation_method(db, "test"))

        fun = reco_dict[user.groups[name]]
        recs = await fun(db, item_id_seed=item_id_seed, base="item", n_recos=n_recos)
        return recs
    except KeyError:
        logger.error(f"Could not find recommendation method for A/B test [{name}]")
        raise NotImplementedError()


async def draw_ab_test_recommendation_method(conn: AsyncIOMotorClient,
                                             name: str):
    """Get a recommendation method from AB test."""
    return cfg.ITEM_BASED_COLLABORATIVE_FILTERING


def quick_fix_adjust_item_id(item_id: int):
    """ quick fix for variants """
    if len(str(item_id)) > 4:
        item_id = str(item_id)[:-3]
    return int(item_id)


def limit_returned_items(items, n_recos) -> List[BasicItemModel]:
    """ This function should take care of adding items when len(items) < n_recos """
    # TODO: it does not limit but add items if necessary
    if len(items) < n_recos:
        logging.warning(
            f"Number of requested items ({n_recos}) less than number of items ({len(items)}) in database")
    return items[0:n_recos]


reco_dict = {
    cfg.ITEM_BASED_COLLABORATIVE_FILTERING: get_collaborative_filtering_items
}
