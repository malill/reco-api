from fastapi import FastAPI
from v1.api import api_router

from core.config import settings

app = FastAPI(title="Recommendation API",
              version=settings.VERSION,
              openapi_url=f"{settings.ENDPOINT_STR}/openapi.json",
              description=f"REST API that exposes calculated recommendations from Recommender Builder. "
                          f"App is running in {settings.ENVIRONMENT} mode.")

app.include_router(api_router, prefix=settings.ENDPOINT_STR)

print(f"running app version {settings.VERSION} in {settings.ENVIRONMENT} mode ...")
