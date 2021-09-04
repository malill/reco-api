from fastapi import FastAPI
from v1.api import api_router

from core.config import settings

version = settings.API_V1_STR

app = FastAPI(title="Recommendation API",
              version=0.1,
              openapi_url=f"{version}/openapi.json",
              description=f"REST API that exposes calculated recommendations from Recommender Builder. "
                          f"App is running in {settings.ENVIRONMENT} mode.")

app.include_router(api_router, prefix=version)

print(f"running app in {settings.ENVIRONMENT} mode ...")
