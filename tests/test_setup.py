from motor.motor_asyncio import AsyncIOMotorClient

import api.core.util.config as cfg
from api.core.db.mongodb import DataBase

async def test_prepare_db():
    # TODO: find local option for test MongoDB
    db = DataBase()
    db.client = AsyncIOMotorClient(cfg.DB_URL,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    if "testing" in cfg.DB_NAME.lower():
        # this is dangerous since if test environmental variable DB_NAME is not set properly it could
        # delete productive data
        await db.client[cfg.DB_NAME][cfg.COLLECTION_NAME_ITEM].drop()
        await db.client[cfg.DB_NAME][cfg.COLLECTION_NAME_USER].drop()
        await db.client[cfg.DB_NAME][cfg.COLLECTION_NAME_RELATIONS].drop()