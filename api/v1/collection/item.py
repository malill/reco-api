from typing import List

from fastapi import APIRouter, Depends, Body
import api.core.services.collection.item as service_item
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.item import BasicItemModel
from api.core.db.mongodb import get_database
from api.core.services.authentification.basic_auth import check_basic_auth
from api.core.util.config import ENDPOINT_ITEM, ENDPOINT_COLLECTION, TAG_ITEM

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_ITEM, tags=[TAG_ITEM])


@api_router.get("/all", response_model=List[BasicItemModel])
async def get_all_items(auth: str = Depends(check_basic_auth),
                        db: AsyncIOMotorClient = Depends(get_database)):
    """Lists all evidence objects from db."""
    return await service_item.get_all_items(db)


@api_router.get("", response_model=BasicItemModel)
async def get_items_by_id(item_id: str,
                          db: AsyncIOMotorClient = Depends(get_database)):
    """Returns items by id."""
    return await service_item.get_item_by_item_id(db, item_id)


@api_router.post("", response_model=str)
async def post_items(auth: str = Depends(check_basic_auth),
                     db: AsyncIOMotorClient = Depends(get_database),
                     item_models: List[BasicItemModel] = Body(...)):
    """Adds and/or updates (by item ID) a list of item model entries into database."""
    return await service_item.create_or_update_items(db, item_models)


@api_router.delete("", response_model=int)
async def delete_items_by_item_id(item_id: str,
                                  auth: str = Depends(check_basic_auth),
                                  db: AsyncIOMotorClient = Depends(get_database)):
    """Deletes items with id [item_id] and returns number of deleted entries."""
    return await service_item.delete_items_by_item_id(db, item_id)
