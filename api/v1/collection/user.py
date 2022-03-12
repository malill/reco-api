from typing import List

from fastapi import APIRouter, Depends, Request, Body
from pydantic import BaseModel

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
async def get_user(auth: str = Depends(check_basic_auth),
                   db: AsyncIOMotorClient = Depends(get_database),
                   reco2js_id: str = None):
    """Returns most probabilistic user matching keys. Returns dummy user when none is found."""
    return await service_user.get_user_by_reco2js_id(db, reco2js_id)


@api_router.post("", response_model=str)
async def user_unique_identifier(req: Request,
                                 user: dict = Body(...),
                                 db: AsyncIOMotorClient = Depends(get_database)):
    """Returns most probabilistic user uid matching reco2js_id from header or creates new user when none is found,
    takes body and inserts or updates data."""
    user = await service_user.get_or_upsert_unique_user(db, req, user)
    return str(user.get_uid())


# @api_router.post("")
# async def post_user(auth: str = Depends(check_basic_auth),
#                     db: AsyncIOMotorClient = Depends(get_database),
#                     user: BasicUserModel = Body(...)):
#     """Adds a new user model entry into database (no identity check)."""
#     return await service_user.create_user(db, user)


@api_router.delete("", response_model=int)
async def delete_users_by_reco2js_id(reco2js_id: str,
                                     auth: str = Depends(check_basic_auth),
                                     db: AsyncIOMotorClient = Depends(get_database)):
    """Deletes users that contain reco2js_id and returns number of deleted entries."""
    return await service_user.delete_users_by_reco2js_id(db, reco2js_id)
