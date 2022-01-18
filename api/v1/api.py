from fastapi import APIRouter

from api.v1.endpoints import items

api_router = APIRouter()
api_router.include_router(items.api_router)
