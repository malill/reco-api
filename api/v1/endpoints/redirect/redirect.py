from fastapi import APIRouter
from starlette.responses import RedirectResponse

api_redirect_router = APIRouter()


@api_redirect_router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect():
    print("hello World")
    return "/docs"
