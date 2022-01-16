import logging
import random

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

import api.core.util.config as cfg


def limit_returned_items(items, n_recos):
    """ This function should take care of adding items when len(items) < n_recos """
    # TODO: it does not limit but add items if necessary
    if len(items) < n_recos:
        logging.warning(f"Number of requested items ({n_recos}) less than number of items ({len(items)}) in database")
    return items[0:n_recos]


async def get_random_consumables(conn: AsyncIOMotorClient, n_recos=5):
    """Retrieve random items from 'consumable' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[Item]: List of random items.
    """
    cursor = conn[cfg.DB_NAME_EVIDENCE][cfg.COLLECTION_NAME_CONSUMABLE].find()
    return random.sample(await cursor.to_list(None), n_recos)


async def get_latest_consumables(conn: AsyncIOMotorClient,
                                 n_recos=5):
    """Retrieve latest items from 'consumable' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[Item]: List of random items.
    """
    cursor = conn[cfg.DB_NAME_EVIDENCE][cfg.COLLECTION_NAME_CONSUMABLE] \
        .find() \
        .sort([('update_time', pymongo.DESCENDING)])  # TODO: needs to be changed into create_time
    return await cursor.to_list(n_recos)


async def get_item_based_collaborative_filtering_items(conn: AsyncIOMotorClient,
                                                       item_id_seed: int,
                                                       n_recos=5):
    """Retrieve item based collaborative filtered items from 'recs' db.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving items from db.
        item_id_seed (int): ID of seed item that is used for finding similar items.
        n_recos (int): Number of items that should be returned.
    Returns:
        List[Item]: List of similar (item-wise) items.
    """
    cursor = conn[cfg.DB_NAME_RECS][cfg.COLLECTION_NAME_COLLABORATIVE_FILTERING] \
        .find({'consumable_id_seed': item_id_seed}, {'_id': False}) \
        .sort([('similarity', pymongo.DESCENDING)])
    sorted_el = await cursor.to_list(None)  # no limit, since we need to retrieve all
    ids = [str(e['consumable_id_recommended']) for e in sorted_el][:n_recos]
    print(ids)

    # TODO: use aggregate function to join collections

    cursor = conn[cfg.DB_NAME_EVIDENCE][cfg.COLLECTION_NAME_CONSUMABLE].find({'_id': {'$in': ids}})
    res = await cursor.to_list(None)

    for i in ids:
        for e in res:
            if e['_id'] == i:
                print(e)

    return res


def quick_fix_adjust_item_id(item_id: int):
    """ quick fix for variants """
    if len(str(item_id)) > 4:
        item_id = str(item_id)[:-3]
    return int(item_id)
