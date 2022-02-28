from typing import Optional, List

from fastapi import APIRouter, Depends, Body
import api.core.services.collection.user as service_user
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.user import BasicUserModel
from api.core.db.mongodb import get_database
from api.core.services.authentification.basic_auth import check_basic_auth

from api.core.util.config import ENDPOINT_COLLECTION, ENDPOINT_USER, TAG_USER

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_USER, tags=[TAG_USER])


@api_router.get("/all", response_model=List[BasicUserModel])
async def get_all_user(auth: str = Depends(check_basic_auth),
                       db: AsyncIOMotorClient = Depends(get_database)):
    return await service_user.get_all_user(db)


@api_router.get("/id", response_model=BasicUserModel)
async def get_user_by_keys(auth: str = Depends(check_basic_auth),
                           db: AsyncIOMotorClient = Depends(get_database),
                           cookie_value: str = None):
    """Returns most probabilistic user matching keys. Returns dummy user when none is found."""
    return await service_user.get_user_by_keys(db, cookie_value)


@api_router.get("", response_model=str)
async def get_user_uid(auth: str = Depends(check_basic_auth),
                       db: AsyncIOMotorClient = Depends(get_database),
                       cookie_value: Optional[str] = None):
    """Returns most probabilistic user uid matching keys or creates new user when none is found."""
    user = await service_user.get_or_create_user_by_cookie(db, cookie_value)
    return str(user.get_uid())


@api_router.post("")
async def post_user(auth: str = Depends(check_basic_auth),
                    db: AsyncIOMotorClient = Depends(get_database),
                    user: BasicUserModel = Body(...)):
    """Adds a new user model entry into database (no identity check)."""
    return await service_user.create_user(db, user)


@api_router.delete("", response_model=int)
async def delete_users_by_cookie(cookie_value: str,
                                 auth: str = Depends(check_basic_auth),
                                 db: AsyncIOMotorClient = Depends(get_database)):
    """Deletes users that contain a cookie key with value [cookie_value] and returns number of deleted entries."""
    return await service_user.delete_users_by_cookie(db, cookie_value)
