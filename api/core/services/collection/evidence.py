import logging

import pandas as pd
from fastapi import Request

from typing import List

from fastapi.encoders import jsonable_encoder

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


async def get_evidence_for_user(conn: AsyncIOMotorClient, user_uid: str) -> List[BasicEvidenceModel]:
    res = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_EVIDENCE].find(filter={'user_uid': user_uid})
    return await res.to_list(None)


async def process_evidence(req: Request, object_list: List[BasicEvidenceModel]) -> List[BasicEvidenceModel]:
    """Adds user UID to evidence objects."""
    return [BasicEvidenceModel(**o.dict(skip_defaults=True), user_uid=req.headers.get(cfg.RECO_USER_UID)) for o in
            object_list]


async def create_evidence(conn: AsyncIOMotorClient, evidence_list: List[BasicEvidenceModel]) -> int:
    """Inserts list of evidence objects to db."""
    t = conn[cfg.DB_NAME][cfg.COLLECTION_NAME_EVIDENCE]
    res = await t.insert_many([jsonable_encoder(e, exclude_none=True) for e in evidence_list])
    return len(res.inserted_ids)


async def delete_evidence(conn: AsyncIOMotorClient, user_uid: str):
    res = await conn[cfg.DB_NAME][cfg.COLLECTION_NAME_EVIDENCE].delete_many(filter={'user_uid': user_uid})
    return res.deleted_count
