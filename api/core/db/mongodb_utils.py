import logging

from motor.motor_asyncio import AsyncIOMotorClient
import api.core.util.config as cfg
from .mongodb import db

logger = logging.getLogger(__name__)


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
