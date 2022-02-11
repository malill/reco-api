from typing import List

from fastapi import APIRouter, Depends, Body
import api.core.services.item as service_item
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.item import BasicItemModel
from api.core.db.mongodb import get_database
from api.core.util.config import ENDPOINT_ITEM, ENDPOINT_COLLECTION, TAG_COLLECTION, TAG_ITEM

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_ITEM, tags=[TAG_COLLECTION, TAG_ITEM])


@api_router.post("")
async def post_items(db: AsyncIOMotorClient = Depends(get_database),
                     item_models: List[BasicItemModel] = Body(...)):
    """Adds a single item model entry into database."""
    return await service_item.create_or_update_items(db, item_models)

# @api_router.get("")
# async def get_all_items(db: AsyncIOMotorClient = Depends(get_database)):
#     """Lists all evidence objects from db.
#
#     Args:
#         db (AsyncIOMotorClient): DB client for persisting evidence model.
#
#     Returns:
#         List[BasicEvidenceModel]: List of all objects in evidence collection.
#     """
#     return await service_con.get_all_items(db)
