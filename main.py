from fastapi import FastAPI
from core.config import settings
from api.v1.api import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Recommendation API",
              version="0.1",
              openapi_url=f"{settings.API_V1_STR}/openapi.json",
              description=f"REST API that exposes calculated recommendations from Recommender Builder. "
                          f"App is running in {settings.ENVIRONMENT} mode.")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

print(f"running app version {settings.API_V1_STR} in {settings.ENVIRONMENT} mode ...")
