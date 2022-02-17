from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status
from starlette.responses import JSONResponse

from api.core.db.models.user import BasicUserModel
import api.core.util.config as cfg


async def get_user(conn: AsyncIOMotorClient, keys: dict):
    """Probabilistic fetch method for user based on key values."""
    # TODO: implement service
    print(keys)
    return "Hello User"


async def create_or_update_users(conn: AsyncIOMotorClient, user_models: List[BasicUserModel]):
    """Create or update user in db."""
    # TODO: need to find existing user by 'keys' attribute(s) of user
    t = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_USER]
    await t.insert_many([jsonable_encoder(e, exclude_none=True) for e in user_models])
    return JSONResponse(status_code=status.HTTP_201_CREATED)
