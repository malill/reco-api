from fastapi import APIRouter

from api.v1.endpoints import nonpersonalized

api_router = APIRouter()
api_router.include_router(nonpersonalized.router)
