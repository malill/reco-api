import logging

from motor.motor_asyncio import AsyncIOMotorClient

import api.core.services.analytics.behavior as service_analytics_behavior
from fastapi import APIRouter, Depends

from api.core.db.mongodb import get_database
from api.core.services.authentification.basic_auth import check_basic_auth
from api.core.util.config import TAG_ANALYTICS, ENDPOINT_ANALYTICS

api_router = APIRouter(prefix=ENDPOINT_ANALYTICS, tags=[TAG_ANALYTICS])

logger = logging.getLogger(__name__)


@api_router.get("/get_csv")
async def get_evidence_dataframe(auth: str = Depends(check_basic_auth),
                                 db: AsyncIOMotorClient = Depends(get_database)):
    return await service_analytics_behavior.get_click_behavior(db)
