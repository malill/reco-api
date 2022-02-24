from typing import List

from fastapi import APIRouter, Depends, Body
import api.core.services.collection.item as service_item
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.item import BasicItemModel
from api.core.db.mongodb import get_database
from api.core.services.authentification.basic_auth import check_basic_auth
from api.core.util.config import ENDPOINT_ITEM, ENDPOINT_COLLECTION, TAG_ITEM

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_ITEM, tags=[TAG_ITEM])


@api_router.get("", response_model=List[BasicItemModel])
async def get_all_items(auth: str = Depends(check_basic_auth),
                        db: AsyncIOMotorClient = Depends(get_database)):
    """Lists all evidence objects from db."""
    return await service_item.get_all_items(db)


@api_router.post("")
async def post_items(auth: str = Depends(check_basic_auth),
                     db: AsyncIOMotorClient = Depends(get_database),
                     item_models: List[BasicItemModel] = Body(...)):
    """Adds a list of item model entries into database."""
    return await service_item.create_or_update_items(db, item_models)
