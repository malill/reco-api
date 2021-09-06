from fastapi import FastAPI
import core.config as cfg
from api.v1.api import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Recommendation API",
              version="0.1",
              openapi_url=f"{cfg.API_V1_STR}/openapi.json",
              description=f"REST API that exposes calculated recommendations from Recommender Builder. "
                          f"App is running in {cfg.ENVIRONMENT} mode.")

# Set all CORS enabled origins
if cfg.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=cfg.API_V1_STR)

print(f"running app version {cfg.API_V1_STR} in {cfg.ENVIRONMENT} mode ...")
