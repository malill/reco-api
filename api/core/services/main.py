import logging
import random
from typing import List

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

import api.core.util.config as cfg
from api.core.db.models.consumable import BasicConsumableModel


async def get_random_consumables(conn: AsyncIOMotorClient, n_recos=5) -> List[BasicConsumableModel]:
    """Retrieve random consumables from 'consumable' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving consumables from db.
        n_recos (int): Number of consumables that should be returned.
    Returns:
        List[BasicConsumableModel]: List of random consumables.
    """
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_CONSUMABLE].find()
    res = random.sample(await cursor.to_list(None), n_recos)
    res = [BasicConsumableModel(**i) for i in res]
    return limit_returned_items(res, n_recos)


async def get_latest_consumables(conn: AsyncIOMotorClient,
                                 n_recos=5) -> List[BasicConsumableModel]:
    """Retrieve latest consumables from 'consumable' collection.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving consumables from db.
        n_recos (int): Number of consumables that should be returned.
    Returns:
        List[BasicConsumableModel]: List of random consumables.
    """
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_CONSUMABLE] \
        .find() \
        .sort([('update_time', pymongo.DESCENDING)])  # TODO: needs to be changed into create_time
    res = await cursor.to_list(n_recos)  # TODO: check if this returns sorted products of all or n_reco documents
    res = [BasicConsumableModel(**i) for i in res]
    return limit_returned_items(res, n_recos)


async def get_item_based_collaborative_filtering_items(conn: AsyncIOMotorClient,
                                                       consumable_id_seed: int,
                                                       n_recos=5) -> List[BasicConsumableModel]:
    """Retrieve item based collaborative filtered consumables from 'recs' db.
    Args:
        conn (AsyncIOMotorClient): Session object used for retrieving consumables from db.
        consumable_id_seed (int): ID of seed consumable that is used for finding similar consumables.
        n_recos (int): Number of consumables that should be returned.
    Returns:
        List[BasicConsumableModel]: List of similar (item-wise) consumables.
    """
    res = []
    pipeline = [
        {'$match': {
            'consumable_id_seed': str(quick_fix_adjust_item_id(consumable_id_seed))
        }},
        {
            '$lookup': {
                'from': cfg.COLLECTION_NAME_CONSUMABLE,
                'localField': 'consumable_id_recommended',
                'foreignField': '_id',
                'as': 'consumable'
            }
        },
        {'$unwind': '$consumable'},  # reduces and flattens the consumable (array) to a single object
        {'$sort': {'similarity': -1}},
        {'$limit': n_recos}
    ]
    async for doc in conn[cfg.DB_NAME][cfg.COLLECTION_NAME_COLLABORATIVE_FILTERING].aggregate(pipeline):
        res.append(BasicConsumableModel(**doc['consumable']))
    return limit_returned_items(res, n_recos)


def quick_fix_adjust_item_id(consumable_id: int):
    """ quick fix for variants """
    if len(str(consumable_id)) > 4:
        consumable_id = str(consumable_id)[:-3]
    return int(consumable_id)


def limit_returned_items(consumables, n_recos):
    """ This function should take care of adding items when len(items) < n_recos """
    # TODO: it does not limit but add items if necessary
    if len(consumables) < n_recos:
        logging.warning(
            f"Number of requested items ({n_recos}) less than number of items ({len(consumables)}) in database")
    return consumables[0:n_recos]
