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

    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://2PyxOR4WcncHrbmc6Pht:ZbBRqN7PWUrd3dtnV50i@wp13.pixelx.cloud:3306" \
                                   "/reco_builder_dev?charset=utf8"

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='core/envs/dev.env',
                    _env_file_encoding='utf-8')
