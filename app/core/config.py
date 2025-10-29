from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Database ---
    MONGO_URI: str
    DATABASE_NAME: str

    # --- Optional AI / external integrations ---
    GEMINI_API_KEY: str | None = None

    # --- Email / Notification settings ---
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str = "noreply@portflow.ai"

    # Pydantic settings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instantiate settings globally
settings = Settings()
