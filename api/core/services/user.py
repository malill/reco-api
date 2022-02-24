import logging

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status, HTTPException
from starlette.responses import JSONResponse

from api.core.db.models.user import BasicUserModel
import api.core.util.config as cfg

logger = logging.getLogger(__name__)


async def get_user(conn: AsyncIOMotorClient, cookie_value) -> BasicUserModel:
    """Probabilistic fetch method for user based on cookie value.
    Method will always return a BasicUserModel even when not found."""
    cursor = get_user_collection(conn).find({'keys.cookie': cookie_value})
    res = await cursor.to_list(None)
    if len(res) == 0:
        logger.info(f"No user found for cookie_value {cookie_value} -> creating new user")
        return await create_user(conn, BasicUserModel(keys={"cookie": [cookie_value]}))
    elif len(res) > 1:
        # TODO: handle multiple users -> maybe probabilistic fetch?
        logger.warning(f"Found more than one user for cookie_value: {cookie_value}")
        raise HTTPException(status_code=300, detail="Multiple users found")
    else:
        return BasicUserModel(**res[0])


async def create_user(conn: AsyncIOMotorClient, user_model: BasicUserModel):
    """Create or update user in db based on user's '_id' attribute."""
    res = await get_user_collection(conn). \
        insert_one(jsonable_encoder(user_model, exclude_none=True))
    user_model._id = res.inserted_id
    return user_model


async def update_user_group(conn: AsyncIOMotorClient, user_model: BasicUserModel, group_name: str,
                            group_value: str) -> BasicUserModel:
    """Adds user to group 'group_name' with 'group_value'."""
    if user_model.groups is None:
        user_model.groups = {}
    await get_user_collection(conn).update_one({'_id': user_model._id},
                                               {'$set': {f"groups.{group_name}": group_value}})
    user_model.groups[group_name] = group_value
    return user_model


def get_user_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]
