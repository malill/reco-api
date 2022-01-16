from fastapi import APIRouter

from api.v1.endpoints import unpersonalized, personalized

api_router = APIRouter()
api_router.include_router(unpersonalized.api_router)
api_router.include_router(personalized.api_router)
