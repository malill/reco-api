import logging
from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from api.core.db.models.user import BasicUserModel, BasicUserKeys
import api.core.util.config as cfg

logger = logging.getLogger(__name__)


async def get_all_user(conn: AsyncIOMotorClient) -> List[BasicUserModel]:
    """Returns list of all BasicUserModels in user collection."""
    cursor = get_user_collection(conn).find()
    items = await cursor.to_list(None)
    return items


async def get_user_by_keys(conn: AsyncIOMotorClient, cookie_value: str) -> List:
    """Return list of BasicUserModels that contain a cookie with value [cookie_value]."""
    cursor = get_user_collection(conn).find(filter={'keys.cookie': cookie_value})
    return [BasicUserModel(**u) for u in await cursor.to_list(None)]


async def get_or_create_user_by_cookie(conn: AsyncIOMotorClient, cookie_value: str) -> BasicUserModel:
    """Probabilistic fetch method for user based on cookie. Method will insert a new BasicUserModel when not found."""
    entry_req = jsonable_encoder(BasicUserModel(keys=BasicUserKeys(cookie=[cookie_value])), exclude_none=True)
    # TODO: handle multiple user / probabilistic fetch
    user = await get_user_collection(conn).find_one_and_update({'keys.cookie': cookie_value},
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


async def delete_users_by_cookie(conn: AsyncIOMotorClient, cookie_value: str) -> int:
    """Deletes user(s) by cookie value and returns number of deleted objects."""
    res = await get_user_collection(conn).delete_many(filter={'keys.cookie': cookie_value})
    return res.deleted_count


def get_user_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]
