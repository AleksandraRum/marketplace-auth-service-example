from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str | None = None
    postgres_host: str | None = None
    postgres_database_name: str | None = None
    postgres_password: str | None = None
    postgres_port: int | None = None
    postgres_username: str | None = None

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    jwt_refresh_expire_days: int = 30

    # @property
    # def database_url(self) -> str:
    #     return f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database_name}"
    def get_database_url(self) -> str:
        if self.database_url is not None:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_username}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_database_name}"
        )
