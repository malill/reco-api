from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status
from starlette.responses import JSONResponse

from api.core.db.models.user import BasicUserModel
import api.core.util.config as cfg


def get_user_collection(conn: AsyncIOMotorClient):
    return conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]


async def get_user(conn: AsyncIOMotorClient, cookie_key) -> BasicUserModel:
    """Non-probabilistic fetch method for user based on cookie value."""
    cursor = get_user_collection(conn).find({'keys.cookie': cookie_key})
    res = await cursor.to_list(None)
    if len(res) > 1:
        print(f"Found more than one user for cookie_value: {cookie_key}")
    return res[0]


async def create_or_update_users(conn: AsyncIOMotorClient, user_models: List[BasicUserModel]):
    """Create or update user in db."""
    # TODO: need to find existing user by 'keys' attribute(s) of user
    await get_user_collection(conn). \
        insert_many([jsonable_encoder(e, exclude_none=True) for e in user_models])
    return JSONResponse(status_code=status.HTTP_201_CREATED)
