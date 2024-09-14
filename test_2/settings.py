from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "game"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"

    ALEMBIC_DB_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    DB_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

    MQ_HOST: str = "rabbit"
    MQ_PORT: int = 5672
    MQ_USER: str = "user"
    MQ_PASS: str = "password"


settings = Settings()
