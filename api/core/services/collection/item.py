from typing import List

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse
from fastapi import status
import api.core.util.config as cfg
from api.core.db.models.item import BasicItemModel


async def get_all_items(conn: AsyncIOMotorClient) -> List[BasicItemModel]:
    """Returns list of all BasicItemModels from item collection."""
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].find()
    items = await cursor.to_list(None)
    return [BasicItemModel(**i) for i in items]


async def get_item_by_item_id(conn: AsyncIOMotorClient, item_id: str) -> BasicItemModel:
    doc = await conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].find_one(filter={'id': item_id})
    return BasicItemModel(**doc)


async def create_or_update_items(conn: AsyncIOMotorClient, item_models: List[BasicItemModel]):
    """Inserts or updates an existing (match by uid) item object to db."""
    t = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM]
    for item_model in item_models:
        entry_req = jsonable_encoder(item_model, exclude_none=True)
        await t.find_one_and_update({'id': item_model.id, 'type': item_model.type}, {"$set": entry_req},
                                    upsert=True)
    return JSONResponse(status_code=status.HTTP_201_CREATED)


async def delete_items_by_item_id(conn: AsyncIOMotorClient, item_id: str) -> int:
    res = await conn[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].delete_many(filter={'id': item_id})
    return res.deleted_count
