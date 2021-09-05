from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str
    ENVIRONMENT: str

    # database
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='core/envs/dev.env',
                    _env_file_encoding='utf-8')
