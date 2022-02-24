from typing import List

from fastapi import APIRouter, Depends

import api.core.services.collection.evidence as service_evidence
from api.core.db.models.evidence import BasicEvidenceModel
from api.core.services.authentification.basic_auth import check_basic_auth

from api.core.util.config import ENDPOINT_COLLECTION, TAG_EVIDENCE, ENDPOINT_EVIDENCE

from api.core.db.mongodb import AsyncIOMotorClient, get_database

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_EVIDENCE, tags=[TAG_EVIDENCE])


@api_router.get("", response_model=List[BasicEvidenceModel])
async def get_all_evidence(auth: str = Depends(check_basic_auth),
                           db: AsyncIOMotorClient = Depends(get_database)):
    """Lists all evidence objects from db."""
    return await service_evidence.get_all_evidence(db)


@api_router.put("", response_model=str)
async def put_evidence(evidence: List[BasicEvidenceModel],
                       db: AsyncIOMotorClient = Depends(get_database)):
    """Adds a list of evidence models into MongoDB."""
    evidence = await service_evidence.process_evidence(evidence)
    return await service_evidence.create_evidence(db, evidence)
