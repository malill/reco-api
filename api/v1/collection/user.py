from typing import Optional

from fastapi import APIRouter, Depends, Body
import api.core.services.user as service_user
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.user import BasicUserModel
from api.core.db.mongodb import get_database
from api.core.services.auth import check_basic_auth

from api.core.util.config import ENDPOINT_COLLECTION, ENDPOINT_USER, TAG_USER

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_USER, tags=[TAG_USER])


@api_router.get("", response_model=BasicUserModel)
async def get_user(auth: str = Depends(check_basic_auth),
                   db: AsyncIOMotorClient = Depends(get_database),
                   cookie_value: Optional[str] = None):
    """Returns most probabilistic user matching keys."""
    # TODO: current service get_user returns deterministic user by cookie value
    return await service_user.get_user(db, cookie_value)


@api_router.post("")
async def post_user(auth: str = Depends(check_basic_auth),
                    db: AsyncIOMotorClient = Depends(get_database),
                    user: BasicUserModel = Body(...)):
    """Adds a list of user model entries into database."""
    return await service_user.create_user(db, user)
