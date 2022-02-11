import logging

from fastapi import FastAPI
import api.core.util.config as cfg
from api.core.db.mongodb_utils import connect_to_mongo_db, close_mongo_db_connection
from api.core.util.log_config import LogConfig
from api.v1.api import api_router
from starlette.middleware.cors import CORSMiddleware

from api.v1.endpoints.redirect.redirect import api_redirect_router

log_config = LogConfig()
logger = logging.getLogger(__name__)

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

app.add_event_handler("startup", connect_to_mongo_db)
app.add_event_handler("shutdown", close_mongo_db_connection)

app.include_router(api_router, prefix=cfg.API_V1_STR)
app.include_router(api_redirect_router)

logger.info(f"running app version {cfg.API_V1_STR} in {cfg.ENVIRONMENT} mode ...")
