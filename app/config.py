import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application
    """
    mongo_host = "mongo"
    db_url: str = os.getenv("MONGO_URL", "")
    db_name: str = os.getenv("MONGO_DB", "")
    collection: str = os.getenv("MONGO_COLLECTION", "")


@lru_cache
def get_settings():
    return Settings()
