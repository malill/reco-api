import logging

import pandas as pd
from fastapi import Request

from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi import status
from pydantic import ValidationError
from starlette.responses import JSONResponse

import api.core.util.config as cfg
from motor.motor_asyncio import AsyncIOMotorClient

from api.core.db.models.evidence import BasicEvidenceModel
from api.core.db.mongodb_utils import MongoDBHelper

logger = logging.getLogger(__name__)


class EvidencePipeline:
    """Class to provide evidence from collection to builders."""

    def __init__(self):
        pass

    def get_raw_evidence(self):
        with MongoDBHelper(cfg.DB_NAME) as db:
            return pd.DataFrame(
                list(
                    db[cfg.COLLECTION_NAME_EVIDENCE].find({}, {'_id': False})
                ))


async def get_all_evidence(conn: AsyncIOMotorClient) -> List[BasicEvidenceModel]:
    """Returns all objects from evidence collection.

    Method will throw an error when object different to BasicEvidenceModel are persisted in item collection.

    Returns:
        List[BasicEvidenceModel]: Complete list of evidence entries in item collection.
    """
    cursor = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_EVIDENCE].find()
    evidence = await cursor.to_list(None)
    return evidence


async def create_evidence(conn: AsyncIOMotorClient, evidence_list: List[BasicEvidenceModel]) -> int:
    """Inserts list of evidence objects to db."""
    t = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_EVIDENCE]
    res = await t.insert_many([jsonable_encoder(e, exclude_none=True) for e in evidence_list])
    return len(res.inserted_ids)


def add_evidence_model_to_list(evidence_list: List, o: dict):
    """Convert dict object into evidence model and add to list."""
    try:
        evidence_list.append(BasicEvidenceModel(**o))
    except ValidationError as e:
        logger.warning(f"Invalid object provided in collection list:{o}", e)


async def process_evidence(object_list: List[BasicEvidenceModel]) -> List[BasicEvidenceModel]:
    """Modify objects to prepare list of BasicEvidenceModels."""
    return object_list
