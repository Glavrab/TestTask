from functools import cached_property

from pydantic import BaseSettings, Field, SecretStr

MAIN_VIEW_PREFIX = '/user'
BASE_USER_BALANCE = 100


class Settings(BaseSettings):
    pg_host: str = Field(..., env='POSTGRES_HOST')
    pg_user: str = Field(..., env='POSTGRES_USER')
    pg_password: SecretStr = Field(..., env='POSTGRES_PASSWORD')
    pg_db: str = Field(..., env='POSTGRES_DB')
    pg_port: int = Field(default=5432, env='POSTGRES_PORT')

    @cached_property
    def db_uri(self) -> str:
        uri_pattern = 'postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
        return uri_pattern.format(
            pg_user=self.pg_user,
            pg_password=self.pg_password.get_secret_value(),
            pg_host=self.pg_host,
            pg_db=self.pg_db,
            pg_port=self.pg_port,
        )

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)


project_settings = Settings()
