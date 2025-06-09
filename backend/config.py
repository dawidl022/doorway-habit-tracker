from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    """Configuration for the database connection."""

    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        """The database connection URL"""
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
