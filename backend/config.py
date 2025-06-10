import os

from check_ins.routes import bp as check_ins_bp
from habits.routes import bp as habits_bp
from validation import HabitNotFoundError, ValidationError


def register_routes(app):
    app.register_blueprint(habits_bp)
    app.register_blueprint(check_ins_bp)
    app.register_error_handler(ValidationError, ValidationError.handle)
    app.register_error_handler(HabitNotFoundError, HabitNotFoundError.handle)


def must_get_env(name: str) -> str:
    """Read an environment variable, or raise an exception is the
    environment variable is not set"""

    value = os.getenv(name)

    if value is None or len(value) == 0:
        raise KeyError(f"Environment variable {name} not set")

    return value


class Config:
    """Configuration for the application."""

    def __init__(self):
        self.frontend_url = must_get_env("FRONTEND_URL")
        self.db = DbConfig()


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
