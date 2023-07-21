import os
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl
from databases import DatabaseURL


class Settings(BaseSettings):
    PASS: str = "ROOT_PASS"
    SECRET_KEY: str = "SECRET_KEY"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173"]

    # MongoDB config
    MONGODB_MAX_CONNECTIONS_COUNT: int = 10
    MONGODB_MIN_CONNECTIONS_COUNT: int = 10
    MONGODB_HOST: str = os.environ.get('MONGODB_HOST')
    MONGODB_PORT: int = os.environ.get('MONGODB_PORT')
    MONGODB_DB: str = os.environ.get('MONGODB_DB')
    MONGODB_CONN_STRING = DatabaseURL(
        f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
    )

    USERS_COLLECTION = 'users'
    BOOKS_COLLECTION = 'books'

    class Config:
        case_sensitive = True


settings = Settings()