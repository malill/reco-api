from fastapi import APIRouter

from api.v1.analytics import analytics
from api.v1.builder import builder
from api.v1.collection import user, item, evidence
from api.v1.reco import splitting
from api.v1.reco import collaborative_filtering
from api.v1.reco import unpersonalized

api_router = APIRouter()

# Analytics router
api_router.include_router(analytics.api_router)

# Builder router
api_router.include_router(builder.api_router)

# Collection router
api_router.include_router(evidence.api_router)
api_router.include_router(item.api_router)
api_router.include_router(user.api_router)

# Reco router
api_router.include_router(splitting.api_router)
api_router.include_router(collaborative_filtering.api_router)
api_router.include_router(unpersonalized.api_router)
