from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_host: str
    postgres_user: str
    postgres_db: str
    postgres_password: str
