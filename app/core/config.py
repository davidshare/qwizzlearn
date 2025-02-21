from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    PROJECT_NAME: str = "Qwizzlearn Authentication"
    PROJECT_DESCRIPTION: str = "Authentication service for qwizzlearn"
    PROJECT_VERSION: str = "v1.0.0"
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_URL: str
    API_V1_STR: str = "/api/v1/auth"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6329
    INITIAL_USER: str
    INITIAL_PASSWORD: str
    INITIAL_EMAIL: str
    APP_PORT: int = 8000
    ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
