from fastapi import APIRouter

from api.v1.endpoints.collection import evidence
from api.v1.endpoints.collection import item
from api.v1.endpoints.collection import user
from api.v1.endpoints.recommendations import item_based

api_router = APIRouter()

# Collection router
api_router.include_router(evidence.api_router)
api_router.include_router(item.api_router)
api_router.include_router(user.api_router)

# Recommendation router
api_router.include_router(item_based.api_router)
