from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "AI API"
    DEBUG: bool = False

    SECRET_KEY: str

    ALLOWED_ORIGINS: list[str] = []

    DATABASE_URL: str

    AI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()