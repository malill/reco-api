from fastapi import APIRouter

from api.v1.endpoints import consumables

api_router = APIRouter()
api_router.include_router(consumables.api_router)
