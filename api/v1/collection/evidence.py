import logging
from typing import List

from fastapi import APIRouter, Depends, Request
import api.core.services.collection.evidence as service_evidence
from api.core.db.models.evidence import BasicEvidenceModel
from api.core.services.authentification.basic_auth import check_basic_auth

from api.core.util.config import ENDPOINT_COLLECTION, TAG_EVIDENCE, ENDPOINT_EVIDENCE

from api.core.db.mongodb import AsyncIOMotorClient, get_database

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_EVIDENCE, tags=[TAG_EVIDENCE])

logger = logging.getLogger(__name__)


@api_router.get("", response_model=List[BasicEvidenceModel])
async def get_all_evidence(auth: str = Depends(check_basic_auth),
                           db: AsyncIOMotorClient = Depends(get_database)):
    """Lists all evidence objects from db."""
    return await service_evidence.get_all_evidence(db)


@api_router.put("", response_model=int)
async def put_evidence(object_list: List[BasicEvidenceModel],
                       req: Request,
                       conn: AsyncIOMotorClient = Depends(get_database)):
    """Adds a list of evidence models into MongoDB, returns number of inserted evidence objects."""
    object_list = await service_evidence.process_evidence(req, object_list)
    return await service_evidence.create_evidence(conn, object_list)
