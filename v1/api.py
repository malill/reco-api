from fastapi import APIRouter

from v1.endpoints import fbt

api_router = APIRouter()
api_router.include_router(fbt.router)


@api_router.get("/")
def hello():
    return {"message": "Hello V1 RECO-REST API..."}
