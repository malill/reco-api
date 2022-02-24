import os

from dotenv import load_dotenv

load_dotenv()

API_V1_STR: str = os.environ.get('API_V1_STR')
ENVIRONMENT: str = os.environ.get('ENVIRONMENT')

# (Basic) Auth
AUTH_USER: str = os.environ.get('AUTH_USER')
AUTH_PASS: str = os.environ.get('AUTH_PASS')

# CORS
BACKEND_CORS_ORIGINS: str = os.environ.get('BACKEND_CORS_ORIGINS')

# Database connection string
DB_URL: str = os.environ.get('DB_URL')
DB_NAME: str = os.environ.get('DB_NAME')

# Database collection names
COLLECTION_NAME_EVIDENCE = "evidence"
COLLECTION_NAME_ITEM = "item"
COLLECTION_NAME_RECOMMENDATIONS = "recommendations"
COLLECTION_NAME_SPLITTING_CONFIG = "splitting_config"
COLLECTION_NAME_USER = "user"

# Database column names
COLUMN_CONFIDENCE = "confidence"
COLUMN_ITEM_ID_SEED = "item_id_seed"
COLUMN_ITEM_ID = "item_id"
COLUMN_ORDER_CODE = "order_code"
COLUMN_ITEM_ID_RECOMMENDED = "item_id_recommended"
COLUMN_SIMILARITY = "similarity"
COLUMN_SUPPORT = "support"
COLUMN_USER_ID = "user_id"

COLUMNS_RECS_FBT = [COLUMN_ITEM_ID_SEED, COLUMN_ITEM_ID_RECOMMENDED, COLUMN_CONFIDENCE, COLUMN_SUPPORT]
COLUMNS_RECS_ICF = [COLUMN_ITEM_ID_SEED, COLUMN_ITEM_ID_RECOMMENDED, COLUMN_SIMILARITY]

# reco-js
RECO_COOKIE_ID = "reco-cookie-id"

# Recommendation types
TYPE_COLLABORATIVE_FILTERING = "cf"
TYPE_ITEM_BASED_COLLABORATIVE_FILTERING = TYPE_COLLABORATIVE_FILTERING + "_ib"
TYPE_USER_BASED_COLLABORATIVE_FILTERING = TYPE_COLLABORATIVE_FILTERING + "_ub"

TYPE_FREQUENTLY_BOUGHT_TOGETHER = "fbt"
TYPE_RANDOM_RECOMMENDATIONS = "rnd"

# Routes 1st level
ENDPOINT_BUILDER = "/bld"
ENDPOINT_COLLECTION = "/col"
ENDPOINT_RECOMMENDATION = "/rec"
# Routes 2nd level
ENDPOINT_EVIDENCE = "/evidence"
ENDPOINT_ITEM = "/item"
ENDPOINT_PERSONALIZED = "/pers"
ENDPOINT_SPLITTING = "/split"
ENDPOINT_UNPERSONALIZED = "/unpers"
ENDPOINT_USER = "/user"
# Routes 3rd level
ENDPOINT_COLLABORATIVE_FILTERING = "/cf"

# Tags
TAG_BUILDER = "Builder"
TAG_COLLECTION = "Collection"
TAG_EVIDENCE = "Evidence"
TAG_ITEM = "Item"
TAG_RECOMMENDATIONS = "Recommendation"
TAG_USER = "User"
