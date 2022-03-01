import logging
from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

import api.core.services.reco.splitting as service_split
from api.core.db.models.item import BasicItemModel
from api.core.db.models.splitting import BasicSplittingModel

from api.core.db.mongodb import get_database
from api.core.services.authentification.basic_auth import check_basic_auth
import api.core.util.config as cfg

api_router = APIRouter(prefix=cfg.ENDPOINT_RECOMMENDATION + cfg.ENDPOINT_SPLITTING, tags=[cfg.TAG_SPLITTING])

logger = logging.getLogger(__name__)


@api_router.get("/config", response_model=BasicSplittingModel)
async def get_splitting(name: str,
                        db: AsyncIOMotorClient = Depends(get_database),
                        auth: str = Depends(check_basic_auth)):
    splitting = await service_split.get_splitting(db, name)
    return splitting


@api_router.get("/config/all", response_model=List[BasicSplittingModel])
async def get_all_splittings(db: AsyncIOMotorClient = Depends(get_database),
                             auth: str = Depends(check_basic_auth)):
    return await service_split.get_all_splittings(db)


@api_router.post("/config", response_model=BasicSplittingModel)
async def set_splitting(name: str,
                        methods: list,
                        db: AsyncIOMotorClient = Depends(get_database),
                        auth: str = Depends(check_basic_auth)):
    """Route to create a A/B testing setup."""
    splitting = await service_split.set_splitting(db, name, methods)
    return splitting


@api_router.delete("/config", response_model=int)
async def delete_splitting(name: str,
                           db: AsyncIOMotorClient = Depends(get_database),
                           auth: str = Depends(check_basic_auth)):
    return await service_split.delete_splitting(db, name)


@api_router.get("/", response_model=List[BasicItemModel])
async def get_split_recos(name: str,
                          req: Request,
                          item_id_seed: int,
                          db: AsyncIOMotorClient = Depends(get_database),
                          n_recos: int = cfg.N_RECOS_DEFAULT):
    """Endpoint that returns split recommendations (= recos from a method that is defined in a splitting).

    Args:
        name (str): Name of splitting (used to fetch respective reco algorithms).
        req (Request): Object to retrieve identifying values from call.
        item_id_seed (str): ID of item for which reco are needed.
        db (Session): Session object used for retrieving items from db.
        n_recos (int): Number of items that should be returned.

    Returns:
        List[Item]: List of recommendations.
    """
    user_uid = req.headers.get(cfg.RECO_USER_UID)
    return await service_split.get_split_recommendations_by_user_uid(db, name, user_uid,
                                                                         item_id_seed, n_recos)
