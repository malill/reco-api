import os

from dotenv import load_dotenv

load_dotenv()

API_V1_STR: str = os.environ.get('API_V1_STR')
ENVIRONMENT: str = os.environ.get('ENVIRONMENT')

# database
DB_URL: str = os.environ.get('DB_URL')

DATABASE_TABLE_CONTENT = 'content'
DATABASE_TABLE_RECS_FBT = 'recs_fbt'

# CORS
BACKEND_CORS_ORIGINS: str = os.environ.get('BACKEND_CORS_ORIGINS')
