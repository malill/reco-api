from fastapi import APIRouter

from api.v1.endpoints import fbt

api_router = APIRouter()
api_router.include_router(fbt.router)
