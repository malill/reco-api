import os

from dotenv import load_dotenv

load_dotenv()

API_V1_STR: str = os.environ.get('API_V1_STR')
ENVIRONMENT: str = os.environ.get('ENVIRONMENT')

# CORS
BACKEND_CORS_ORIGINS: str = os.environ.get('BACKEND_CORS_ORIGINS')

# Database connection string
DB_URL: str = os.environ.get('DB_URL')
DB_NAME: str = os.environ.get('DB_NAME')
COLLECTION_NAME_ITEM = os.environ.get('COLLECTION_NAME_ITEM')
COLLECTION_NAME_EVIDENCE: str = os.environ.get('COLLECTION_NAME_EVIDENCE')
COLLECTION_NAME_FREQUENTLY_BOUGHT_TOGETHER: str = os.environ.get('COLLECTION_NAME_FREQUENTLY_BOUGHT_TOGETHER')
COLLECTION_NAME_COLLABORATIVE_FILTERING: str = os.environ.get('COLLECTION_NAME_COLLABORATIVE_FILTERING')

# Endpoints
ENDPOINT_COLLECTION = "/col"
ENDPOINT_EVIDENCE = "/evidence"
ENDPOINT_ITEM = "/item"
ENDPOINT_USER = "/user"

ENDPOINT_RECOMMENDATION = "/rec"

# Tags
TAG_COLLECTION = "Collection"
TAG_EVIDENCE = "Evidence"
TAG_ITEM = "Item"
TAG_RECOMMENDATIONS = "Recommendation"
TAG_USER = "User"
