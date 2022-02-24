import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

import api.core.util.config as cfg
from .mongodb import db

logger = logging.getLogger(__name__)


# Synchronous ->

class MongoDBHelper:
    """Helper class for Recommendation Builder Class(!) to connect to MongoDB.

    Use class in 'with' construct. Note, that builder classes store reco synchronous into
    MongoDB (<> collection-/reco-services store/retrieve asynchronous)
    """

    def __init__(self, collection):
        self.client = MongoClient(cfg.DB_URL)
        # TODO: class needs attribute to control "how much" evidence (e.g. age-based) should be fetch for calculations
        self.db = self.client[collection]

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


# Asynchronous ->

async def connect_to_mongo_db():
    logger.info("connect to MongoDB...")
    db.client = AsyncIOMotorClient(cfg.DB_URL,
                                   maxPoolSize=10,
                                   minPoolSize=10)
    logger.info("connection to MongoDB successful!")


async def close_mongo_db_connection():
    logger.info("close connection to MongoDB...")
    db.client.close()
    logger.info("connection to MongoDB closed!")
