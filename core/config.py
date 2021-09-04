from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='core/envs/dev.env',
                    _env_file_encoding='utf-8')
