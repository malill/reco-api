from typing import List

from fastapi import APIRouter, Depends, Request

import api.core.services.evidence as service_evidence
from api.core.db.models.evidence import BasicEvidenceModel

from api.core.util.config import ENDPOINT_COLLECTION, TAG_EVIDENCE, ENDPOINT_EVIDENCE

from api.core.db.mongodb import AsyncIOMotorClient, get_database

from starlette.responses import JSONResponse

api_router = APIRouter(prefix=ENDPOINT_COLLECTION + ENDPOINT_EVIDENCE, tags=[TAG_EVIDENCE])


@api_router.get("", response_model=List[BasicEvidenceModel])
async def get_all_evidence(db: AsyncIOMotorClient = Depends(get_database)):
    """Lists all evidence objects from db.

    Args:
        db (AsyncIOMotorClient): DB client for persisting evidence model.

    Returns:
        List[BasicEvidenceModel]: List of all objects in evidence collection.
    """
    return await service_evidence.get_all_evidence(db)


@api_router.put("")
async def put_evidence(request: Request,
                       db: AsyncIOMotorClient = Depends(get_database)):
    """Adds a list of evidence models into database without checking references to other objects.

    Args:
        db (AsyncIOMotorClient): DB client for persisting evidence model.
        request (Request): Received request object.

    Returns:
        JSONResponse: Status of insert command.
    """
    evidence = await service_evidence.process_evidence(request)
    return await service_evidence.create_evidence(db, evidence)
