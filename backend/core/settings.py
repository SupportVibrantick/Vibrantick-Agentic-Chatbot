from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.config import ENV_FILE

class Settings(BaseSettings):
    APP_NAME: str = "Vibrantic AI"
    APP_VERSION: str = "1.0.0"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    DEBUG: bool = True

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    
     # -------------------------
    # OpenAI
    # -------------------------
    OPENAI_API_KEY: str = ""

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str


    # -------------------------
    # Email Settings
    # -------------------------

    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    MAIL_FROM: str
    MAIL_FROM_NAME: str

    MAIL_PORT: int
    MAIL_SERVER: str

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    FRONTEND_URL: str

    @cached_property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    EMAIL_PROVIDER: str = "smtp"

settings = Settings()