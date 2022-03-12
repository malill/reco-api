import asyncio
import logging
from typing import List, Optional
from fastapi import Request, Body
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReturnDocument

from api.core.db.models.user import BasicUserModel, BasicUserKeys, dummy_user_dict, Reco2jsModel
import api.core.util.config as cfg

logger = logging.getLogger(__name__)


async def get_all_user(conn: AsyncIOMotorClient) -> List[BasicUserModel]:
    """Returns list of all BasicUserModels in user collection."""
    cursor = get_user_collection(conn).find()
    items = await cursor.to_list(None)
    return items


async def get_user_by_uid(conn: AsyncIOMotorClient, user_uid: str) -> BasicUserModel:
    doc = await get_user_collection(conn).find_one(ObjectId(user_uid))
    return BasicUserModel(**doc)


async def get_user_by_reco2js_id(conn: AsyncIOMotorClient, reco2js_id: str) -> BasicUserModel:
    """Probabilistic fetch method for user by keys (currently only reco2js_id is used). If none is found dummy user
    will be returned. This method should only be called when user is available in collection."""
    # TODO: currently reco2js.id is the only deterministic identifier
    u = await get_user_collection(conn).find_one(filter={'keys.reco2js_ids': reco2js_id})
    if u is None:  # should never happen
        # If evidence call (creates user) is to close to other calls the user might not be found initially
        logger.warning(f"Could not find a user for reco2js_id key {reco2js_id} -> try again...")
        await asyncio.sleep(2)  # bad implementation
        u = await get_user_collection(conn).find_one(filter={'keys.reco2js_ids': reco2js_id})
    if u is None:
        logger.error(f"No user found for reco2js_id key {reco2js_id} -> return dummy user")
        u = dummy_user_dict
    return BasicUserModel(**u)


async def get_or_upsert_unique_user(conn: AsyncIOMotorClient, req: Request, user: dict) -> BasicUserModel:
    """Probabilistic fetch method for user by keys (currently only reco2js_id value is used). Method will insert a new
     BasicUserModel when not found."""
    reco2js_id = req.headers.get(cfg.RECO2JS_ID)
    if reco2js_id is None:
        return BasicUserModel(**dummy_user_dict)

    entry_req = prepareBasicUserModel(reco2js_id, user)

    # TODO: currently reco2js.id is the only deterministic identifier
    user = await get_user_collection(conn).find_one_and_update({'keys.reco2js_ids': reco2js_id},
                                                               {"$set": entry_req},
                                                               upsert=True,
                                                               return_document=ReturnDocument.AFTER)
    return BasicUserModel(**user)


async def create_user(conn: AsyncIOMotorClient, user_model: BasicUserModel) -> BasicUserModel:
    """Create a new user object without checking of already existence."""
    res = await get_user_collection(conn).insert_one(document=jsonable_encoder(user_model, exclude_none=True))
    user_model._id = res.inserted_id
    return user_model


async def update_user_group(conn: AsyncIOMotorClient, user: BasicUserModel, group_name: str,
                            group_value: str) -> BasicUserModel:
    """Adds user to group 'group_name' with 'group_value' and stores results in MongoDB."""
    if user.groups is None:
        user.groups = {}
    await get_user_collection(conn).update_one(filter={'_id': user.get_uid()},
                                               update={'$set': {f"groups.{group_name}": group_value}})
    user.groups[group_name] = group_value
    return user


async def delete_users_by_reco2js_id(conn: AsyncIOMotorClient, reco2js_id: str) -> int:
    """Deletes user(s) by reco2js_id value and returns number of deleted objects."""
    res = await get_user_collection(conn).delete_many(filter={'keys.reco2js_ids': reco2js_id})
    return res.deleted_count


def prepareBasicUserModel(reco2js_id: str, user: dict):
    if user is not None:
        entry_req = jsonable_encoder(BasicUserModel(**user, keys=BasicUserKeys(reco2js_ids=[reco2js_id])),
                                     exclude_none=True)
    else:
        entry_req = jsonable_encoder(BasicUserModel(keys=BasicUserKeys(reco2js_ids=[reco2js_id])),
                                     exclude_none=True)
    return entry_req


def get_user_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]
