import logging
from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from api.core.db.models.user import BasicUserModel
import api.core.util.config as cfg

logger = logging.getLogger(__name__)


async def get_all_user(conn: AsyncIOMotorClient) -> List[BasicUserModel]:
    cursor = get_user_collection(conn).find()
    items = await cursor.to_list(None)
    return items


async def get_users_by_cookie(conn: AsyncIOMotorClient, cookie_value: str) -> List:
    cursor = get_user_collection(conn).find(filter={'keys.cookie': cookie_value})
    return await cursor.to_list(None)


async def get_or_create_user_by_cookie(conn: AsyncIOMotorClient, cookie_value: str) -> BasicUserModel:
    """Probabilistic fetch method for user based on cookie value.
    Method will insert a new BasicUserModel when not found."""
    users = await get_users_by_cookie(conn, cookie_value)
    if len(users) == 0:
        logger.info(f"No user found for cookie_value {cookie_value} -> creating new user")
        return await create_user(conn, BasicUserModel(keys={"cookie": [cookie_value]}))
    elif len(users) > 1:
        # TODO: handle multiple users -> maybe probabilistic fetch?
        logger.error(f"Found more than one user for cookie_value: {cookie_value}")
        raise HTTPException(status_code=300, detail="Multiple users found")
    else:
        return BasicUserModel(**users[0])


async def create_user(conn: AsyncIOMotorClient, user_model: BasicUserModel) -> BasicUserModel:
    """Create a new user object."""
    res = await get_user_collection(conn).insert_one(document=jsonable_encoder(user_model, exclude_none=True))
    user_model._id = res.inserted_id
    return user_model


async def update_user_group(conn: AsyncIOMotorClient, user: BasicUserModel, group_name: str,
                            group_value: str) -> BasicUserModel:
    """Adds user to group 'group_name' with 'group_value' and stores results in MongoDB."""
    if user.groups is None:
        user.groups = {}
    await get_user_collection(conn).update_one(filter={'_id': user._id},
                                               update={'$set': {f"groups.{group_name}": group_value}})
    user.groups[group_name] = group_value
    return user


def get_user_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]
