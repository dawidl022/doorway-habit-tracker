import os
from dataclasses import dataclass


def must_get_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or len(value) == 0:
        raise KeyError(f"Environment variable {name} not set")

    return value


class DbConfig:
    """Configuration for the database connection."""

    def __init__(self):
        self.host = must_get_env("DB_HOST")
        self.port = int(must_get_env("DB_PORT"))
        self.user = must_get_env("DB_USER")
        self.password = must_get_env("DB_PASSWORD")
        self.database = must_get_env("DB_NAME")

    @property
    def url(self) -> str:
        """The database connection URL"""
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
