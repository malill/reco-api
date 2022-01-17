from fastapi import APIRouter

from api.v1.endpoints import unpersonalized

api_router = APIRouter()
api_router.include_router(unpersonalized.api_router)
