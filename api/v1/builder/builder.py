from fastapi import APIRouter

from api.core.util.config import ENDPOINT_BUILDER, TAG_BUILDER

api_router = APIRouter(prefix=ENDPOINT_BUILDER, tags=[TAG_BUILDER])


@api_router.put("")
def hello_builder():
    return "Hello Builder!"
